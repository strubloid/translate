from packages.Translator.Translator import Translator

## Here we will be doing the logic for the local translator.
class TranslatorLocal(Translator):

    def __init__(self, config=None):
        # Call the parent class constructor
        super().__init__(self, config)

    def translate(self, text, client):
        print(f"Translating:")
