import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LogObject:
    verbose = os.getenv("VERBOSE", "True").lower() in ("true", "1", "yes")

    @classmethod
    def log(cls, msg):
        if cls.verbose:
            print(msg)