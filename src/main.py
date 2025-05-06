from microphone import Microphone
from config import GENERATED_DIR, log
from env_setup import load_env
from openai_setup import setup_openai
from whisper_setup import load_whisper_model
from translator import translate
from audio_processor import process_audio
import os

def main():
    try:
        api_key = load_env()
        # if not os.path.exists(GENERATED_DIR):
        #     os.makedirs(GENERATED_DIR)
        #     log(f"📁 Created output directory: {GENERATED_DIR}")

        client = setup_openai(api_key)
        model = load_whisper_model()
        mic = Microphone()

        log("🎙️ Ready to listen. Speak into the microphone...")

        while True:
            audio_path = mic.listen_until_silence()
            process_audio(model, client, translate, file_path=audio_path)
            os.remove(audio_path)

    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'mic' in locals():
            mic.terminate()

if __name__ == "__main__":
    main()
