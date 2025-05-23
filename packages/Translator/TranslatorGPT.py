import os
from dotenv import load_dotenv
from packages.Translator.Translator import Translator

# Load environment variables from .env file (used to configure model and language)
load_dotenv()

## This class is used to manage the translation process using OpenAI's chat completion API.
# It handles the translation model, target language, and the actual translation process.
# It also provides methods to retrieve the target language and translation model.
# The class is initialized with a configuration object that contains various settings.
# The translation process is done using the OpenAI API, and the translated text is returned.
class TranslatorGPT(Translator):

    def __init__(self, config=None):
        print("Initializing TranslatorGPT...")
        # Call the parent class constructor
        super().__init__(config)
    
    # This function translates text using OpenAI's chat completion API.
    # => It takes the text to be translated and the OpenAI client as parameters.
    # => The function constructs a prompt for translation and sends it to the OpenAI API.
    # => The response is parsed to extract the translated text, which is returned.
    # => If the text is longer than a specified threshold, it uses streaming to handle the response.
    def translate(self, text, client):
        
        if not isinstance(text, str):
            text = str(text)

        if self.config and hasattr(self.config, "getOutputFile"):
            open(self.config.getOutputFile(), "w").close()


        prompt = f"Translate to {self.getTargetLanguage()}: {text}"

        response = client.chat.completions.create(
            model=self.getTranslationModel(),
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        translated_text = ""
        for chunk in response:
            content_part = getattr(chunk.choices[0].delta, "content", None)
            if content_part:
                self.writeToOBS(self.config.getOutputFile(), content_part)
                translated_text += content_part


        return translated_text.strip()