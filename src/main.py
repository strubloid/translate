from config import checkingEnvironmentVariables, OUTPUT_FILE, OUTPUT_TRANSCRIPTION_FILE,TRANSLATION_LANGUAGE, log
from MicrophoneObject import MicrophoneObject
from OpenAIObject import OpenAIObject
from WhisperObject import WhisperObject
from translator import translate
import os

def main():

    try:

        ## Loading the environment variables and returning an api_key
        checkingEnvironmentVariables()

        ## starting the client
        openAiObject = OpenAIObject()

        ## loading the client of OpenAI
        client = openAiObject.setup(openAiObject.getKey())
        
        ## Loading the whisper model and getting eh model
        whisperObject = WhisperObject()
        model = whisperObject.getModel()

        ## Loading the microphone object
        mic = MicrophoneObject()

        log("🎙️ Ready to listen. Speak into the microphone...")

        while True:
            
            try:

                ## the mic object will listen until silence
                audio_path = mic.listenUntilSilence()
                result = model.transcribe(audio_path, fp16=False)
                transcribed_text = result["text"].strip()

                if transcribed_text:

                    ## Prints out the transcribed text on OUTPUT_TRANSCRIPTION_FILE
                    with open(OUTPUT_TRANSCRIPTION_FILE, "w", encoding="utf-8") as f:
                        f.write(transcribed_text)
                    
                    ## Getting the the text translated to the TRANSLATION_LANGUAGE
                    translated = translate(transcribed_text, client, TRANSLATION_LANGUAGE)

                    ## Prints out the translated text on OUTPUT_FILE
                    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                        f.write(translated)
                else:
                    ## cleans it, in case of no text detected
                    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                        f.write("")

            except Exception as e:
                print(f"⚠️ Transcription or translation failed: {e}")

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
