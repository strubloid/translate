# import whisper
from packages.Config.ConfigObject import ConfigObject
from packages.Log.LogObject import LogObject
from faster_whisper import WhisperModel
import torch

import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


class WhisperObject:

    model = None
    modelSize = None

    ## Starting the WhisperObject class
    # => It initializes the class with a configuration object.
    # => It sets the model size and loads the Whisper model.
    # => The model size is obtained from the configuration object.
    # => The startingWhisperModel function is called to load the model.
    def __init__(self, config : ConfigObject):
        self.config = config
        self.modelSize = config.getModelSize()
        self.model = self.startingWhisperModel()

    ## This function loads the Whisper model and returns a model object.
    # => It uses the whisper library to load the model specified by MODEL_SIZE.
    # => If the model fails to load, it raises a RuntimeError with the error message.
    # => The function also logs the loading process, indicating whether it was successful or not.
    def startingWhisperModel(self):

        LogObject.log("🔄 Loading Whisper model...")
        try:
            # model = whisper.load_model(self.modelSize)
            model = WhisperModel("base", device="cuda" if torch.cuda.is_available() else "cpu")
            LogObject.log("✅ Whisper model loaded.")
            return model
        
        except Exception as e:
            raise RuntimeError(f"❌ Whisper model failed to load: {e}")

    ## Gets the Whisper model    
    def getModel(self):

        ## double checking if was loaded or not
        if not self.model:
            self.model = self.startingWhisperModel()

        return self.model       