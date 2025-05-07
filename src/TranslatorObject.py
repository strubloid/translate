import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TranslatorObject:
    translationModel = os.getenv("TRANSLATION_MODEL", "gpt-3.5-turbo")

    @classmethod
    ## This function translates text using OpenAI's chat completion API.
    # => It takes the text to be translated, the OpenAI client, and the target language as parameters.
    # => The function constructs a prompt for translation and sends it to the OpenAI API.
    # => The response is parsed to extract the translated text, which is returned.
    def translate(self, text, client, target_language="pt"):
        prompt = f"Translate to {target_language}: {text}"
        response = client.chat.completions.create(
            model=self.translationModel,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()