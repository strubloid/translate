import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configurations from environment variables
VERBOSE = os.getenv("VERBOSE", "True").lower() in ("true", "1", "yes")
GENERATED_DIR = os.getenv("GENERATED_DIR", "generated")
AUDIO_FILE = os.path.join(GENERATED_DIR, os.getenv("AUDIO_FILE", "mic.wav"))
OUTPUT_FILE = os.path.join(GENERATED_DIR, os.getenv("OUTPUT_FILE", "translation.txt"))

# Options: tiny, base, small, medium, large
MODEL_SIZE = os.getenv("MODEL_SIZE", "small")
TRANSLATION_MODEL = os.getenv("TRANSLATION_MODEL", "gpt-3.5-turbo")  # Use gpt-4 if needed

# Log function, it works by this main VERBOSE variable
def log(msg):
    if VERBOSE:
        print(msg)