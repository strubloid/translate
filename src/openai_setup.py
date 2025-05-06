from openai import OpenAI, AuthenticationError
from config import log

def setup_openai(api_key):
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()
        log("✅ OpenAI connection verified.")
        return client
    except AuthenticationError:
        raise RuntimeError("❌ OpenAI authentication failed. Check your API key.")
    except Exception as e:
        raise RuntimeError(f"❌ OpenAI error: {e}")
