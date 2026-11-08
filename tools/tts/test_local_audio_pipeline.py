#!/usr/bin/env python3
"""End-to-end offline tests for EnglishTale's local Piper-to-WAV pipeline.

The fake Piper executable writes deterministic PCM fixtures. No voice model,
network access, API key, or GPU is needed for these pipeline tests.
"""
from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

from tools.tts import generate_local_english as generator
from tools.tts import build_english_track as assembler


class LocalAudioPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.manifest_path = self.root / "voice-manifest.json"
        self.output_dir = self.root / "en"
        self.output_wav = self.root / "episode.wav"
        self.model = self.root / "licensed-test-model.onnx"
        self.model.write_bytes(b"test fixture only")
        self.fake_piper = self.root / "piper-fixture"
        self.fake_piper.write_text(
            "#!/usr/bin/env python3\n"
            "import argparse, sys, wave, struct\n"
            "p=argparse.ArgumentParser()\n"
            "p.add_argument('--model'); p.add_argument('--output_file', required=True)\n"
            "a=p.parse_args()\n"
            "text=sys.stdin.read().strip()\n"
            "frames=max(22050, min(22050*3, len(text)*350))\n"
            "with wave.open(a.output_file, 'wb') as w:\n"
            " w.setnchannels(1); w.setsampwidth(2); w.setframerate(22050)\n"
            " w.writeframes(b''.join(struct.pack('<h', 900) for _ in range(frames)))\n",
            encoding="utf-8",
        )
        self.fake_piper.chmod(self.fake_piper.stat().st_mode | stat.S_IXUSR)
        source = json.loads(generator.MANIFEST.read_text(encoding="utf-8"))
        self.manifest_path.write_text(json.dumps(source), encoding="utf-8")
        self.original_generator_manifest = generator.MANIFEST
        self.original_assembler_manifest = assembler.MANIFEST
        generator.MANIFEST = self.manifest_path
        assembler.MANIFEST = self.manifest_path

    def tearDown(self):
        generator.MANIFEST = self.original_generator_manifest
        assembler.MANIFEST = self.original_assembler_manifest
        self.temp.cleanup()

    def run_generator(self, *args):
        argv = [
            "generate_local_english.py",
            "--model", str(self.model),
            "--output", str(self.output_dir),
            *args,
        ]
        with patch.object(sys, "argv", argv), patch.object(
            generator.shutil, "which", return_value=str(self.fake_piper)
        ):
            return generator.main()

    def test_manifest_has_48_usable_english_cues(self):
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        cues = manifest["cues"]
        self.assertEqual(len(cues), 48)
        self.assertEqual([cue["id"] for cue in cues], list(range(1, 49)))
        for cue in cues:
            self.assertTrue(cue["english_text"].strip())
            self.assertTrue(cue["role"].strip())
            self.assertLess(assembler.ms(cue["start"]), assembler.ms(cue["end"]))

    def test_generator_creates_48_wavs_and_assembler_builds_seven_minutes(self):
        self.assertEqual(self.run_generator(), 0)
        self.assertEqual(len(list(self.output_dir.glob("*.wav"))), 48)
        argv = [
            "build_english_track.py",
            "--input", str(self.output_dir),
            "--output", str(self.output_wav),
            "--duration", "420",
        ]
        with patch.object(sys, "argv", argv):
            self.assertEqual(assembler.main(), 0)
        with wave.open(str(self.output_wav), "rb") as wav:
            self.assertEqual(wav.getnchannels(), 1)
            self.assertEqual(wav.getsampwidth(), 2)
            self.assertEqual(wav.getframerate(), 22050)
            self.assertEqual(wav.getnframes(), 420 * 22050)

    def test_generator_resumes_without_overwriting_existing_cues(self):
        self.assertEqual(self.run_generator("--limit", "2"), 0)
        first = self.output_dir / "001.wav"
        before = first.stat().st_mtime_ns
        self.assertEqual(self.run_generator("--limit", "2"), 0)
        self.assertEqual(first.stat().st_mtime_ns, before)
        self.assertEqual(len(list(self.output_dir.glob("*.wav"))), 2)

    def test_assembler_fails_when_a_clip_is_missing(self):
        self.assertEqual(self.run_generator("--limit", "1"), 0)
        argv = [
            "build_english_track.py",
            "--input", str(self.output_dir),
            "--output", str(self.output_wav),
        ]
        with patch.object(sys, "argv", argv):
            self.assertEqual(assembler.main(), 1)
        self.assertFalse(self.output_wav.exists())


if __name__ == "__main__":
    unittest.main()
