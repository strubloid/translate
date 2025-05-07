import os
from dotenv import load_dotenv

# Load environment variables from .env file (used to configure model and language)
load_dotenv()

class TranslatorObject:
    # Load the translation model from environment variables, default to "gpt-3.5-turbo"
    translationModel = os.getenv("TRANSLATION_MODEL", "gpt-3.5-turbo")

    ##  Static method to retrieve the target translation language from environment variables.
    ## Returns "pt" (Portuguese) by default if not specified.
    @staticmethod
    def language():
        return os.getenv("TRANSLATION_LANGUAGE", "pt")

    ## This function translates text using OpenAI's chat completion API.
    # => It takes the text to be translated, the OpenAI client, and the target language as parameters.
    # => The function constructs a prompt for translation and sends it to the OpenAI API.
    # => The response is parsed to extract the translated text, which is returned.
    # => If the text is longer than a specified threshold, it uses streaming to handle the response.
    @classmethod
    def translate(cls, text, client, stream_threshold=40):
        
        # Ensure the text is a string to avoid type comparison errors
        if not isinstance(text, str):
            # print(f"⚠️ 'text' should be a string, got {type(text).__name__}: {text}")
            text = str(text)

        # Load the target translation language (default: Portuguese)
        target_language = os.getenv("TRANSLATION_LANGUAGE", "pt")
        
        # Compose the prompt for the OpenAI model
        prompt = f"Translate to {target_language}: {text}"

        # Decide whether to use streaming based on the text length
        use_stream = len(text) > stream_threshold

        if use_stream:
            print("🔄 Using streaming for translation...")
            # Streamed translation for large texts
            response = client.chat.completions.create(
                model=cls.translationModel,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            translated_text = ""

            # Process streamed chunks and build translated result
            for chunk in response:
                content_part = getattr(chunk.choices[0].delta, "content", None)
                if content_part:
                    translated_text += content_part

            return translated_text.strip()

        else:
            print("🔄 Non-streaming mode")
            # Non-streaming translation for short texts
            response = client.chat.completions.create(
                model=cls.translationModel,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.choices[0].message.content.strip()
