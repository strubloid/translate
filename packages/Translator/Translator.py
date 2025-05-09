import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables from .env file (used to configure model and language)
load_dotenv()

## Abstract base class for translation functionality.
class Translator(ABC):

    def __init__(self, config=None):
        # Initialize the translation model and configuration
        self.config = config
        self.translationModel = os.getenv("TRANSLATION_MODEL", "gpt-3.5-turbo")
        self.targetLanguage = os.getenv("TRANSLATION_LANGUAGE", "pt-br")

    # Public method to retrieve the target translation language.
    def getTargetLanguage(self):
        return self.targetLanguage

    # Public method to retrieve the translation model.
    def getTranslationModel(self):
        return self.translationModel

    # Abstract method for translation, to be implemented by child classes.
    @abstractmethod
    def translate(self, text, client):
        pass

    # Public method to write the translated text to a file.
    def writeToOBS(self, path, content):
        # Use "a" to append instead of overwriting
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
            # Forces the buffer to write immediately
            f.flush()  