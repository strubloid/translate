from ConfigObject import ConfigObject
from MicrophoneObject import MicrophoneObject
from OpenAIObject import OpenAIObject
from WhisperObject import WhisperObject
from TranslatorObject import TranslatorObject
from LogObject import LogObject
import os
import time
import torch

def main():

    try:

        ## Loading the environment variables and returning an api_key
        config = ConfigObject()
        config.checkingEnvironmentVariables()

        ## starting the client
        openAiObject = OpenAIObject(config)

        ## loading the client of OpenAI
        client = openAiObject.setup(openAiObject.getKey())
        
        ## Loading the whisper model and getting eh model
        whisperObject = WhisperObject(config)
        model = whisperObject.getModel()

        ## Loading the microphone object
        mic = MicrophoneObject(config)
        language = TranslatorObject.language()
        print(f"🌐 Translate to {language} ")
        print(f"🗣️ CUDA: {torch.cuda.is_available()}")

        LogObject.log("🎙️ Ready to listen. Speak into the microphone...")

        while True:
            
            try:

                ## the mic object will listen until silence
                audio_path = mic.listenUntilSilence()

                trasncriptionTime = time.perf_counter()
                result = model.transcribe(audio_path, fp16=False)
                print(f"⏱️ Transcription took: {time.perf_counter() - trasncriptionTime:.2f}s")

                transcribed_text = result["text"].strip()

                if transcribed_text:

                    ## Prints out the transcribed text on OUTPUT_TRANSCRIPTION_FILE
                    with open(config.getOutputTranscriptionFile(), "w", encoding="utf-8") as f:
                        f.write(transcribed_text)
                    
                    ## Getting the the text translated to the TRANSLATION_LANGUAGE
                    translationTime = time.perf_counter()
                    translated = TranslatorObject.translate(transcribed_text, client)
                    print(f"⏱️ Translation took: {time.perf_counter() - translationTime:.2f}s")

                    ## Prints out the translated text on OUTPUT_FILE
                    with open(config.getOutputFile(), "w", encoding="utf-8") as f:
                        f.write(translated)
                else:
                    ## cleans it, in case of no text detected
                    with open(config.getOutputFile(), "w", encoding="utf-8") as f:
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
