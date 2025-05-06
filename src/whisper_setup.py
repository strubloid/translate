import whisper
from config import MODEL_SIZE, log

import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

## This function loads the Whisper model and returns a model object.
# => It uses the whisper library to load the model specified by MODEL_SIZE.
# => If the model fails to load, it raises a RuntimeError with the error message.
# => The function also logs the loading process, indicating whether it was successful or not.
def load_whisper_model():
    log("🔄 Loading Whisper model...")
    try:
        model = whisper.load_model(MODEL_SIZE)
        log("✅ Whisper model loaded.")
        return model
    except Exception as e:
        raise RuntimeError(f"❌ Whisper model failed to load: {e}")