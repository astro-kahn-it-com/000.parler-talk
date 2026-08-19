# Local Parler-TTS Generator

A completely standalone, locally-running Python tool for generating character dialogue using Parler-TTS. Designed to work efficiently within a 6GB VRAM limit (RTX 2060).

## Repository Structure

```
.
├── generate.py           # The main Python script that handles model loading and audio generation
├── start_generation.bat  # Windows one-click entry point. Sets up the venv, installs dependencies, and runs generate.py
├── README.md             # This file
├── output/               # Directory where generated .wav files are saved (created automatically)
└── venv/                 # Python virtual environment (created automatically on first run)
```

## Usage

1. Open `generate.py` in a text editor.
2. Edit the two variables at the very top of the script:
   * `spoken_dialogue`: The actual text the character will say.
   * `voice_description`: The text-based acting prompt.
3. Save `generate.py`.
4. Double-click `start_generation.bat`.

The very first time you run `start_generation.bat`, it will take a few minutes to create the virtual environment and download the necessary dependencies (PyTorch, transformers, Parler-TTS) and models. Subsequent runs will be much faster.

Generated audio files will be saved in the `output/` folder.
