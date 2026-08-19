# Parler-TTS Standalone Generator

A completely standalone, local Python repository that generates character dialogue using [Parler-TTS](https://github.com/huggingface/parler-tts).

This tool is designed to be lightweight, running entirely locally without dependencies on external web frameworks or complex routing systems. It is optimized for environments with VRAM limitations (e.g., RTX 2060 with 6GB VRAM) by strictly utilizing the `parler-tts-mini-v1` model.

## Folder Structure

Once executed, the repository will look like this:

```
project_folder/
├── generate.py            # Main inference script (change settings here)
├── start_generation.bat   # One-click Windows entry point
├── .gitignore             # Git ignore file
├── README.md              # This documentation
├── venv/                  # (Auto-generated) Python virtual environment
└── output/                # (Auto-generated) Directory where .wav files are saved
    └── output.wav         # The generated audio file
```

## How to Use

1. **Configure Dialogue and Acting Prompt:**
   Open `generate.py` in any text editor. At the very top, you will find two variables you can modify:
   - `spoken_dialogue`: The actual text the character will speak.
   - `voice_description`: The acting prompt (e.g., tone, emotion, gender, pacing).

2. **Generate Audio:**
   Double-click the `start_generation.bat` file.
   - On the first run, it will automatically create a local `venv` and install the required dependencies (`torch` with CUDA, `transformers`, `soundfile`, and `parler-tts`).
   - It will then run the script.
   - Generation might take a moment. The script will pause at the end so you can review any output or errors.

3. **Locate Your File:**
   The finished audio file will be saved in the `output/` directory as `output.wav`.

## Requirements
- Windows OS (due to the `.bat` file format).
- Python 3.8+ installed and added to your System PATH.
- (Optional but highly recommended) An NVIDIA GPU with at least 6GB VRAM to run inference via CUDA.