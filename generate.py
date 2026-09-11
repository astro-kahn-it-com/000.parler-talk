import os
import sys
from datetime import datetime

# ==============================================================================
# 1. DIRECTORY CONTAINMENT & ENVIRONMENT LOCK
# ==============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(SCRIPT_DIR, "models")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
TEMP_DIR = os.path.join(SCRIPT_DIR, "cache", "temp")
PROMPT_FILE = os.path.join(SCRIPT_DIR, "prompt.txt")

# Ensure required local folders exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Force all Hugging Face and PyTorch caches into the project folder
os.environ["HF_HOME"] = MODELS_DIR
os.environ["HUGGINGFACE_HUB_CACHE"] = MODELS_DIR
os.environ["TORCH_HOME"] = MODELS_DIR
os.environ["TEMP"] = TEMP_DIR
os.environ["TMP"] = TEMP_DIR

# Import third-party modules after setting environment paths
import torch
import soundfile as sf
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration

MODEL_ID = "parler-tts/parler-tts-mini-v1"


# ==============================================================================
# 2. EXTERNAL PROMPT PARSER
# ==============================================================================
def load_prompt_file(filepath):
    if not os.path.exists(filepath):
        # Create a default template if the file doesn't exist yet
        default_content = (
            "[DESCRIPTION]\n"
            "A male speaker delivers urgent, breathless dialogue in a deep, raspy voice. "
            "The recording is close-up, muffled slightly by radio static, spoken very fast with high tension.\n\n"
            "[DIALOGUE]\n"
            "The perimeter fence is down. We have about two minutes before they breach the lower airlock.\n"
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(default_content)
        print(f"[Notice] No prompt.txt found. Created default template at: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    description = ""
    dialogue = ""

    # Parse sections demarcated by tags
    if "[DESCRIPTION]" in content and "[DIALOGUE]" in content:
        desc_part = content.split("[DESCRIPTION]")[1].split("[DIALOGUE]")[0]
        dial_part = content.split("[DIALOGUE]")[1]
        description = desc_part.strip()
        dialogue = dial_part.strip()
    else:
        raise ValueError(
            "Invalid format in prompt.txt. Ensure the file contains both [DESCRIPTION] and [DIALOGUE] tags."
        )

    if not description:
        raise ValueError("[DESCRIPTION] section in prompt.txt cannot be empty.")
    if not dialogue:
        raise ValueError("[DIALOGUE] section in prompt.txt cannot be empty.")

    return description, dialogue


# ==============================================================================
# 3. INFERENCE PIPELINE
# ==============================================================================
def run_generation():
    print("=" * 60)
    print(" Parler-TTS Local Generation Pipeline")
    print("=" * 60)

    # 1. Load External Prompt
    print(f"[Input]    Reading prompt file from: {PROMPT_FILE}")
    voice_description, spoken_dialogue = load_prompt_file(PROMPT_FILE)

    print("\n--- Loaded Configuration ---")
    print(f"Description: {voice_description}")
    print(f"Dialogue:    {spoken_dialogue}")
    print("-" * 60)

    # 2. Hardware Allocation
    if torch.cuda.is_available():
        device = "cuda:0"
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
        print(f"[Hardware] Using GPU: {gpu_name} ({vram_gb:.2f} GB Total VRAM)")
    else:
        device = "cpu"
        print("[Hardware] CUDA not detected. Running on CPU.")

    print(f"[Storage]  Models Directory: {MODELS_DIR}")
    print(f"[Storage]  Output Directory: {OUTPUT_DIR}")
    print("-" * 60)

    # 3. Load Model and Tokenizer
    print(f"[Loader]   Loading tokenizer for '{MODEL_ID}'...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    print(f"[Loader]   Loading model weights into {device}...")
    model = ParlerTTSForConditionalGeneration.from_pretrained(MODEL_ID).to(device)

    # 4. Tokenization
    print("[Pipeline] Tokenizing voice description...")
    description_inputs = tokenizer(voice_description, return_tensors="pt").to(device)

    print("[Pipeline] Tokenizing spoken text...")
    prompt_inputs = tokenizer(spoken_dialogue, return_tensors="pt").to(device)

    # 5. Audio Synthesis
    print("[Pipeline] Generating audio tensors (please wait)...")
    with torch.inference_mode():
        generation = model.generate(
            input_ids=description_inputs.input_ids,
            attention_mask=description_inputs.attention_mask,
            prompt_input_ids=prompt_inputs.input_ids,
            prompt_attention_mask=prompt_inputs.attention_mask,
        )

    # 6. Save Audio
    audio_arr = generation.cpu().numpy().squeeze()
    sampling_rate = model.config.sampling_rate

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"dialogue_{timestamp}.wav"
    output_filepath = os.path.join(OUTPUT_DIR, filename)

    print(f"[Output]   Writing {sampling_rate} Hz WAV file...")
    sf.write(output_filepath, audio_arr, sampling_rate)

    print("-" * 60)
    print(f"[SUCCESS] Audio generated and saved to:")
    print(f"          -> {output_filepath}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_generation()
    except Exception as e:
        print(f"\n[ERROR] Execution failed:\n{e}", file=sys.stderr)
        sys.exit(1)