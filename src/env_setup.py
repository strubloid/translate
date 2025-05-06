import os
from dotenv import load_dotenv

from config import log

## Basic rules to load the environment variables, just a small check before starting the program
def load_env():
    
    log("🔍 Checking environment...")
    if not os.path.exists(".env"):
        raise FileNotFoundError("❌ Missing .env file.")

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    ## This will raise an error if the API key is not found
    if not api_key:
        raise ValueError("❌ OPENAI_API_KEY not found in .env.")
    
    return api_key
