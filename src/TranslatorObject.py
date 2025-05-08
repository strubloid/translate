import os
from dotenv import load_dotenv

# Load environment variables from .env file (used to configure model and language)
load_dotenv()
## This class is used to manage the translation process using OpenAI's chat completion API.
# It handles the translation model, target language, and the actual translation process.
# It also provides methods to retrieve the target language and translation model.
# The class is initialized with a configuration object that contains various settings.
# The translation process is done using the OpenAI API, and the translated text is returned.
class TranslatorObject:

    def __init__(self, config=None):
        # Initialize the translation model and configuration
        self.config = config
        self.translationModel = os.getenv("TRANSLATION_MODEL", "gpt-3.5-turbo")
        self.targetLanguage = os.getenv("TRANSLATION_LANGUAGE", "pt-br")

    # Method to retrieve the target translation language.
    def getTargetLanguage(self):
        return self.targetLanguage
    
    ## Method to retrieve the translation model.
    def getTranslationModel(self):
        return self.translationModel
    
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
                # Uncomment the following lines if you want to print the content part to the console
                # print(content_part, end='', flush=True)
                # with open(content_part, "a", encoding="utf-8") as f:  # Use "a" to append instead of overwriting
                #     f.write(translated_text)
                #     f.flush() # Forces the buffer to write immediately
                translated_text += content_part


        return translated_text.strip()

    ## Method to write the translated text to a file.
    def writeToOBS(self, path, content):
        # Use "a" to append instead of overwriting
        with open(path, "a", encoding="utf-8") as f:  
                    f.write(content)
                    f.flush()  # Forces the buffer to write immediately