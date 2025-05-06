from config import TRANSLATION_MODEL

## This function translates text using OpenAI's chat completion API.
# => It takes the text to be translated, the OpenAI client, and the target language as parameters.
# => The function constructs a prompt for translation and sends it to the OpenAI API.
# => The response is parsed to extract the translated text, which is returned.
def translate(text, client, target_language="pt"):
    prompt = f"Translate to {target_language}: {text}"
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()