#!/usr/bin/env python3
"""Unit tests for the dependency-free voice asset validator."""
import importlib.util
import tempfile
import unittest
import wave
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate_voice_assets.py")
SPEC = importlib.util.spec_from_file_location("validate_voice_assets", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VoiceAssetTests(unittest.TestCase):
    def make_wav(self, path: Path, *, rate=24000, channels=1, width=2, frames=2400, amplitude=1200):
        path.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(path), "wb") as wav:
            wav.setnchannels(channels)
            wav.setsampwidth(width)
            wav.setframerate(rate)
            sample = int(amplitude).to_bytes(width, "little", signed=True)
            wav.writeframes(sample * frames * channels)

    def test_accepts_valid_mono_pcm(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "clip.wav"
            self.make_wav(path)
            info, problems = MODULE.inspect_wav(path, 1.0, 0.12)
            self.assertEqual(problems, [])
            self.assertEqual(info["sample_rate"], 24000)

    def test_rejects_silent_clip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "silent.wav"
            self.make_wav(path, amplitude=0)
            _, problems = MODULE.inspect_wav(path, 1.0, 0.12)
            self.assertTrue(any("silent" in item for item in problems))

    def test_rejects_clip_longer_than_slot(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "long.wav"
            self.make_wav(path, rate=24000, frames=30000)
            _, problems = MODULE.inspect_wav(path, 1.0, 0.12)
            self.assertTrue(any("exceeds slot" in item for item in problems))

    def test_blocks_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                MODULE.safe_asset_path(Path(tmp), "../outside.wav")


if __name__ == "__main__":
    unittest.main()
