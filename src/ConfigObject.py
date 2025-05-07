import os
from dotenv import load_dotenv
from LogObject import LogObject

# Load environment variables from .env file
load_dotenv()

class ConfigObject:

    ## This class is used to manage the configuration settings for the application.
    def __init__(self):
        self.openaiApiKey = os.getenv("OPENAI_API_KEY", "")
        self.generatedDir = os.getenv("GENERATED_DIR", "generated")
        self.audioFile = os.path.join(self.generatedDir, os.getenv("AUDIO_FILE", "mic.wav"))
        self.outputTranscriptionFile = os.path.join(self.generatedDir, os.getenv("OUTPUT_TRANSCRIPTION_FILE", "transcription.txt"))
        self.outputFile = os.path.join(self.generatedDir, os.getenv("OUTPUT_FILE", "translation.txt"))
        self.modelSize = os.getenv("MODEL_SIZE", "small")
        self.translationModel = os.getenv("TRANSLATION_MODEL", "gpt-3.5-turbo")
        self.translationLanguage = os.getenv("TRANSLATION_LANGUAGE", "pt")
        self.microphoneIndex = os.getenv("MICROPHONE" , "1")

    # Getters for each variable
    def getOpenaiApiKey(self):
        return self.openaiApiKey
      
    def getMicrophoneIndex(self):
        return self.microphoneIndex

    def getGeneratedDir(self):
        return self.generatedDir

    def getAudioFile(self):
        return self.audioFile

    def getOutputTranscriptionFile(self):
        return self.outputTranscriptionFile

    def getOutputFile(self):
        return self.outputFile

    def getModelSize(self):
        return self.modelSize

    def getTranslationModel(self):
        return self.translationModel

    def getTranslationLanguage(self):
        return self.translationLanguage

    # Environment variable check
    def checkingEnvironmentVariables(self):
        LogObject.log("🔍 Checking environment...")
        if not os.path.exists(".env"):
            raise FileNotFoundError("❌ Missing .env file.")
