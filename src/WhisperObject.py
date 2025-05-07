import whisper
from config import MODEL_SIZE, log

import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

class WhisperObject:

    model = None
    modelSize = None

    def __init__(self):
        self.modelSize = MODEL_SIZE
        self.model = self.loadingWhisperModel()

    ## This function loads the Whisper model and returns a model object.
    # => It uses the whisper library to load the model specified by MODEL_SIZE.
    # => If the model fails to load, it raises a RuntimeError with the error message.
    # => The function also logs the loading process, indicating whether it was successful or not.
    def loadingWhisperModel(self):

        log("🔄 Loading Whisper model...")
        try:
            model = whisper.load_model(self.modelSize)
            log("✅ Whisper model loaded.")
            return model
        
        except Exception as e:
            raise RuntimeError(f"❌ Whisper model failed to load: {e}")

    ## Gets the Whisper model    
    def getModel(self):

        ## double checking if was loaded or not
        if not self.model:
            self.model = self.loadingWhisperModel()

        return self.model       