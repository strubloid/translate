import os
import time
from config import GENERATED_DIR, AUDIO_FILE, log
from env_setup import load_env
from openai_setup import setup_openai
from whisper_setup import load_whisper_model
from translator import translate
from audio_processor import process_audio


def main():
    try:
        api_key = load_env()

        ## maybe check if the folder exists sometimes might be slowing down the process, check if you can remake without this
        if not os.path.exists(GENERATED_DIR):
            os.makedirs(GENERATED_DIR)
            log(f"📁 Created output directory: {GENERATED_DIR}")
        ####################################################################################################################    

        ## getting the openai client
        client = setup_openai(api_key)

        ## loading the whisper model
        model = load_whisper_model()

        log("✅ All systems go.")
        
        log(f"🧠 Polling '{AUDIO_FILE}' for changes... Press Ctrl+C to stop.")

        last_mtime = 0
        while True:
            if os.path.exists(AUDIO_FILE):
                mtime = os.path.getmtime(AUDIO_FILE)
                if mtime != last_mtime:
                    log("📂 Detected new or updated audio file.")
                    last_mtime = mtime
                    time.sleep(0.3)
                    process_audio(model, client, translate)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully.")
    except Exception as e:
        print(e)

## just in case you want to run this file directly
if __name__ == "__main__":
    main()
