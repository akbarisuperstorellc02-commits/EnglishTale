[CmdletBinding()]
param(
    [switch]$Overwrite,
    [switch]$SkipVideo
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Push-Location $repoRoot

try {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCommand) {
        throw "Python 3.11+ was not found. Install Python and enable 'Add Python to PATH'."
    }
    & python -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
    if ($LASTEXITCODE -ne 0) { throw "Python 3.11 or newer is required." }

    $venvPython = Join-Path $repoRoot ".venv-englishtale\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Host "[1/9] Creating local Python environment..."
        & python -m venv (Join-Path $repoRoot ".venv-englishtale")
        if ($LASTEXITCODE -ne 0) { throw "Could not create Python virtual environment." }
    }

    Write-Host "[2/9] Installing local Piper TTS runtime..."
    & $venvPython -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed." }
    & $venvPython -m pip install -r "tools/tts/local-requirements.txt"
    if ($LASTEXITCODE -ne 0) { throw "Piper installation failed." }

    Write-Host "[3/9] Downloading and verifying British English voice model..."
    & $venvPython "tools/tts/download_british_voice.py"
    if ($LASTEXITCODE -ne 0) { throw "Voice model download or checksum validation failed." }

    Write-Host "[4/9] Generating the 48 English dialogue cues..."
    $ttsArgs = @(
        "tools/tts/generate_local_english.py",
        "--model", "models/piper/en_GB-vctk-medium/en_GB-vctk-medium.onnx",
        "--voices-json", "tools/tts/episode-001-voices.json"
    )
    if ($Overwrite) { $ttsArgs += "--overwrite" }
    & $venvPython @ttsArgs
    if ($LASTEXITCODE -ne 0) { throw "English voice generation failed." }

    Write-Host "[5/9] Validating all English WAV files..."
    & $venvPython "tools/tts/validate_voice_assets.py" --strict
    if ($LASTEXITCODE -ne 0) { throw "One or more English WAV clips failed validation." }

    Write-Host "[6/9] Assembling the 7-minute English track and retiming subtitles..."
    & $venvPython "tools/tts/build_english_track.py"
    if ($LASTEXITCODE -ne 0) { throw "English audio assembly failed." }
    & $venvPython "tools/tts/retime_subtitles.py"
    if ($LASTEXITCODE -ne 0) { throw "Subtitle retiming failed." }

    if (-not $SkipVideo) {
        Write-Host "[7/9] Checking FFmpeg and installing SVG renderer..."
        if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue) -or
            -not (Get-Command ffprobe -ErrorAction SilentlyContinue)) {
            throw "FFmpeg and FFprobe are required for video rendering. Install them from https://ffmpeg.org/download.html or rerun with -SkipVideo."
        }
        & $venvPython -m pip install -r "tools/video-pipeline/requirements.txt"
        if ($LASTEXITCODE -ne 0) { throw "CairoSVG installation failed." }

        $shotListArgs = @()
        $blenderCommand = Get-Command blender -ErrorAction SilentlyContinue
        if ($blenderCommand) {
            Write-Host "[8/9] Rendering the 18-angle Blender 3D still library..."
            New-Item -ItemType Directory -Force -Path "build/3d-shots" | Out-Null
            & $blenderCommand.Path -b -t 2 --python "tools/blender/render_character_lookdev.py" -- --shot-library --shots-dir "build/3d-shots" --width 1920 --height 1080
            if ($LASTEXITCODE -ne 0) { throw "Blender 3D shot-library render failed." }
            $shotCount = @(Get-ChildItem "build/3d-shots/shot-*.png" -ErrorAction Stop).Count
            if ($shotCount -ne 18) { throw "Expected 18 Blender 3D stills, found $shotCount." }
            $shotListArgs = @("--shot-list", "episodes/001-english-at-the-airport/render-shotlist-3d.json")
        }
        else {
            Write-Warning "Blender was not found. The master will use the documented SVG 2.5D fallback."
        }

        Write-Host "[9/9] Rendering the 720p review cut and 1080p30 master candidate..."
        $reviewArgs = @(
            "tools/video-pipeline/render_episode.py",
            "--output", "build/episode-001-review-720p.mp4",
            "--width", "1280", "--height", "720", "--fps", "24",
            "--english-audio", "build/audio/episode-001-en.wav",
            "--subtitles-en", "build/subtitles/episode-001-en-retimed.srt",
            "--subtitles-fa", "build/subtitles/episode-001-fa-retimed.srt"
        )
        & $venvPython @reviewArgs
        if ($LASTEXITCODE -ne 0) { throw "720p review render failed." }

        $masterArgs = @(
            "tools/video-pipeline/render_episode.py",
            "--output", "build/episode-001-master-1080p.mp4",
            "--width", "1920", "--height", "1080", "--fps", "30",
            "--english-audio", "build/audio/episode-001-en.wav",
            "--subtitles-en", "build/subtitles/episode-001-en-retimed.srt",
            "--subtitles-fa", "build/subtitles/episode-001-fa-retimed.srt"
        )
        $masterArgs += $shotListArgs
        & $venvPython @masterArgs
        if ($LASTEXITCODE -ne 0) { throw "1080p30 master candidate render failed." }
    }

    Write-Host ""
    Write-Host "ENGLISHTALE EPISODE 001 BUILD COMPLETED"
    Write-Host "English audio: build/audio/episode-001-en.wav"
    Write-Host "English captions: build/subtitles/episode-001-en-retimed.srt"
    Write-Host "Afghan Dari captions: build/subtitles/episode-001-fa-retimed.srt"
    if (-not $SkipVideo) {
        Write-Host "720p review: build/episode-001-review-720p.mp4"
        Write-Host "1080p30 master candidate: build/episode-001-master-1080p.mp4"
    }
    Write-Host "VCTK CC BY 4.0 attribution: models/piper/en_GB-vctk-medium/ATTRIBUTION.txt"
    Write-Host "Human review is still required before YouTube publication."
}
catch {
    Write-Error $_
    exit 1
}
finally {
    Pop-Location
}
