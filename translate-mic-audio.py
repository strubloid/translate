import time
import whisper
import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError

# Toggle verbosity
VERBOSE = True  # Set to False to suppress logs except final translation

def log(msg):
    if VERBOSE:
        print(msg)

# Load .env
log("🔍 Checking environment...")
if not os.path.exists(".env"):
    print("❌ Missing .env file.")
    exit(1)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not found in .env.")
    exit(1)

log("✅ .env loaded and API key found.")

# Create OpenAI client
try:
    client = OpenAI(api_key=api_key)
    client.models.list()
    log("✅ OpenAI connection verified.")
except AuthenticationError:
    print("❌ OpenAI authentication failed. Check your API key.")
    exit(1)
except Exception as e:
    print(f"❌ OpenAI error: {e}")
    exit(1)

# Load Whisper model
log("🔄 Loading Whisper model...")
try:
    # model = whisper.load_model("tiny")  # Faster dev model
    model = whisper.load_model("base")
    log("✅ Whisper model loaded.")
except Exception as e:
    print(f"❌ Whisper model failed to load: {e}")
    exit(1)

# File paths
AUDIO_FILE = "mic.wav"
OUTPUT_FILE = "translation.txt"
last_modified = None
current_model = "gpt-4"
# current_model = "gpt-3.5-turbo"

def translate(text, target_language="pt"):
    prompt = f"Translate to Brazilian Portuguese: {text}"
    response = client.chat.completions.create(
        model=current_model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

log("✅ All systems go.")
log("🧠 Waiting for audio... Press Ctrl+C to stop.")

try:
    while True:
        if os.path.exists(AUDIO_FILE):
            new_time = os.path.getmtime(AUDIO_FILE)
            if new_time != last_modified:
                try:
                    log("🎙️ Transcribing...")
                    result = model.transcribe(AUDIO_FILE)
                    transcribed_text = result["text"].strip()

                    if transcribed_text:
                        log("📝 " + transcribed_text)
                        translated = translate(transcribed_text)
                        print("🌍", translated)
                        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                            f.write(translated)
                    else:
                        log("🤐 Nothing meaningful to transcribe.")
                        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                            f.write("")  # Clear file

                    last_modified = new_time
                except Exception as e:
                    print(f"⚠️ Transcription or translation failed: {e}")
        else:
            log("⌛ Waiting for mic.wav to appear...")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n👋 Exiting gracefully. See you next time!")
