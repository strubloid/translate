import json
import os
from functools import lru_cache

## This class is used to load a language map from a JSON file.
## The language map is a dictionary that maps language codes to language names.
class LanguageMap:

    LANGUAGE_MAP_FILE = "languageMap.json"
    NLLB_MAP_FILE = "nllbLanguageMap.json"

    @staticmethod
    @lru_cache(maxsize=1)
    def getMap():
        ## Load the language map from a JSON file.
        ## The file should be in the same directory as this script.
        path = os.path.join(os.path.dirname(__file__), LanguageMap.LANGUAGE_MAP_FILE)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    ## Get the language name by its code.
    ## The code is converted to lowercase to ensure case-insensitive matching.
    ## an example of the code is "pt-BR" and the language is "Portuguese (Brazil)"
    ## another example is "en" and the language is "English"
    @staticmethod
    def getLanguageByCode(code: str) -> str:
        return LanguageMap.getMap().get(code.lower(), "Unknown")
    

    @staticmethod
    @lru_cache(maxsize=1)
    def getMBartLanguageMap():
        path = os.path.join(os.path.dirname(__file__), LanguageMap.NLLB_MAP_FILE)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def getMBartLanguageCode(code: str) -> str:
        return LanguageMap.getMBartLanguageMap().get(code.lower(), "en_XX")
