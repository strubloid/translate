from transformers import MarianMTModel, MarianTokenizer
import torch

model_name = "Helsinki-NLP/opus-mt-en-ROMANCE"

tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
model = model.to(device)

text = "This is a test."
tokens = tokenizer(f"{text}", return_tensors="pt", padding=True).to(device)
translated = model.generate(**tokens)
output = tokenizer.decode(translated[0], skip_special_tokens=True)

print(output)  # "Isto é um teste."
