import os

VERBOSE = True
GENERATED_DIR = "generated"
AUDIO_FILE = os.path.join(GENERATED_DIR, "mic.wav")
OUTPUT_FILE = os.path.join(GENERATED_DIR, "translation.txt")
MODEL_SIZE = "small"  # Options: tiny, base, small, medium, large
TRANSLATION_MODEL = "gpt-3.5-turbo"  # Use gpt-4 if needed

## Log function, it works by this main VERBOSE variable
def log(msg):
    if VERBOSE:
        print(msg)
