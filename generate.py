import os
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
from datetime import datetime

# ==============================================================================
# CONFIGURATION
# Modify these variables before running the script
# ==============================================================================
spoken_dialogue = "I'm telling you, the killer is still in the building."
voice_description = "A gruff, exhausted detective whispering frantically."
# ==============================================================================

def main():
    # Setup output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Device configuration
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    if device == "cpu":
        print("WARNING: CUDA is not available. Generation will be very slow.")

    # Strictly use the mini model to fit within 6GB VRAM constraint
    model_name = "parler-tts/parler-tts-mini-v1"
    print(f"Loading model {model_name}...")

    try:
        model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    print("Generating audio...")
    print(f"Voice: {voice_description}")
    print(f"Dialogue: {spoken_dialogue}")

    # Tokenize
    input_ids = tokenizer(voice_description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(spoken_dialogue, return_tensors="pt").input_ids.to(device)

    # Generate
    try:
        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
        audio_arr = generation.cpu().numpy().squeeze()
    except Exception as e:
        print(f"Error generating audio: {e}")
        return

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"output_{timestamp}.wav")

    try:
        sf.write(output_path, audio_arr, model.config.sampling_rate)
        print(f"Success! Audio saved to: {output_path}")
    except Exception as e:
        print(f"Error saving audio: {e}")

if __name__ == "__main__":
    main()
