import whisper
import os
import time
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError

# === CONFIG ===
VERBOSE = True
GENERATED_DIR = "generated"
AUDIO_FILE = os.path.join(GENERATED_DIR, "mic.wav")
OUTPUT_FILE = os.path.join(GENERATED_DIR, "translation.txt")
MODEL_SIZE = "small"  # Options: tiny, base, small, medium, large
TRANSLATION_MODEL = "gpt-3.5-turbo"  # Use gpt-4 if needed

# === UTILITIES ===
def log(msg):
    if VERBOSE:
        print(msg)

# === ENV SETUP ===
log("🔍 Checking environment...")
if not os.path.exists(".env"):
    print("❌ Missing .env file.")
    exit(1)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not found in .env.")
    exit(1)

# === CREATE OUTPUT DIR ===
if not os.path.exists(GENERATED_DIR):
    os.makedirs(GENERATED_DIR)
    log(f"📁 Created output directory: {GENERATED_DIR}")

# === OPENAI SETUP ===
try:
    client = OpenAI(api_key=api_key)
    client.models.list()  # Test API call
    log("✅ OpenAI connection verified.")
except AuthenticationError:
    print("❌ OpenAI authentication failed. Check your API key.")
    exit(1)
except Exception as e:
    print(f"❌ OpenAI error: {e}")
    exit(1)

# === WHISPER SETUP ===
log("🔄 Loading Whisper model...")
try:
    model = whisper.load_model(MODEL_SIZE)
    log("✅ Whisper model loaded.")
except Exception as e:
    print(f"❌ Whisper model failed to load: {e}")
    exit(1)

# === TRANSLATE FUNCTION ===
def translate(text, target_language="pt"):
    prompt = f"Translate to Brazilian Portuguese: {text}"
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# === AUDIO PROCESSING ===
def process_audio():
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
                f.write("")
    except Exception as e:
        print(f"⚠️ Transcription or translation failed: {e}")

# === MAIN LOOP (Polling Method) ===
log("✅ All systems go.")
log(f"🧠 Polling '{AUDIO_FILE}' for changes... Press Ctrl+C to stop.")

last_mtime = 0

try:
    while True:
        if os.path.exists(AUDIO_FILE):
            mtime = os.path.getmtime(AUDIO_FILE)
            if mtime != last_mtime:
                log("📂 Detected new or updated audio file.")
                last_mtime = mtime
                time.sleep(0.3)  # Brief delay to ensure file is fully written
                process_audio()
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Exiting gracefully.")
