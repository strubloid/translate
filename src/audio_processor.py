import os
from config import AUDIO_FILE, OUTPUT_FILE, log

## This function will be used to translate the text
# => It takes the text to be translated, the OpenAI client, and the target language as parameters.
# => The function constructs a prompt for translation and sends it to the OpenAI API.
# => The response is parsed to extract the translated text, which is returned.
def process_audio(model, client, translate_func, file_path=None):
    try:
        audio_path = file_path or AUDIO_FILE

        log("🎙️ Transcribing...")
        result = model.transcribe(audio_path)
        transcribed_text = result["text"].strip()

        if transcribed_text:
            log("📝 " + transcribed_text)
            # translated = translate_func(transcribed_text, client)
            # print("🌍", translated)
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(transcribed_text)
        else:
            log("🤐 Nothing meaningful to transcribe.")
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write("")
    except Exception as e:
        print(f"⚠️ Transcription or translation failed: {e}")
