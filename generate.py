import os
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

# ==========================================
# USER SETTINGS
# ==========================================
# The actual text the character will say.
spoken_dialogue = "I'm telling you, the killer is still in the building."

# The text-based acting prompt (e.g., emotion, pacing, tone).
voice_description = "A gruff, exhausted detective whispering frantically"
# ==========================================

def main():
    print("Initializing Parler-TTS Generator...")

    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "output.wav")

    # Use CUDA if available
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load Model and Tokenizer
    # Strictly using the mini model to keep VRAM usage under 6GB limit for RTX 2060
    model_name = "parler-tts/parler-tts-mini-v1"
    print(f"Loading model: {model_name}...")

    try:
        model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    print("Model loaded successfully. Preparing input...")

    # Process Inputs
    input_ids = tokenizer(voice_description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(spoken_dialogue, return_tensors="pt").input_ids.to(device)

    print("Generating audio... (this may take a moment)")

    # Generate Audio
    try:
        with torch.no_grad(): # Use no_grad to reduce memory footprint during inference
            generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
            audio_arr = generation.cpu().numpy().squeeze()
    except Exception as e:
        print(f"Error during audio generation: {e}")
        return

    # Save to file
    try:
        sf.write(output_file, audio_arr, model.config.sampling_rate)
        print(f"Success! Audio saved to: {output_file}")
    except Exception as e:
        print(f"Error saving audio file: {e}")

if __name__ == "__main__":
    main()
