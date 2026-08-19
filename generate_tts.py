import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

# Dynamic inputs
PROMPT = "A gruff, exhausted detective whispering frantically"
TEXT = "I'm telling you, the killer is still in the building."

device = "cuda:0" if torch.cuda.is_available() else "cpu"

model_name = "parler-tts/parler-tts-mini-v1"
model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

input_ids = tokenizer(PROMPT, return_tensors="pt").input_ids.to(device)
prompt_input_ids = tokenizer(TEXT, return_tensors="pt").input_ids.to(device)

generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
audio_arr = generation.cpu().numpy().squeeze()
sf.write("out.wav", audio_arr, model.config.sampling_rate)

print("Audio saved to out.wav")
