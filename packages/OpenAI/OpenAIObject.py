from openai import OpenAI, AuthenticationError
from packages.Config.ConfigObject import ConfigObject
from packages.Log.LogObject import LogObject
import os

class OpenAIObject:

    client = None
    key = None
    config = None

    ## Main constructor will just setup the variables
    def __init__(self, config : ConfigObject):
        self.client = None
        self.key = self.getKey()
        self.config = config

    # Sets up the OpenAI client with the API key
    def setup(self, api_key):
        try:
            self.client = OpenAI(api_key=api_key)
            self.client.models.list()
            LogObject.log("✅ OpenAI connection verified.")
            return self.client
        
        except AuthenticationError:
            raise RuntimeError("❌ OpenAI authentication failed. Check your API key.")
        except Exception as e:
            raise RuntimeError(f"❌ OpenAI error: {e}")

    # Retrieves the OpenAI API key from environment variables
    def getKey(self):

        ## It will try to see if was set already
        if self.key:
            return self.key

        ## if isnt set, we will try to load by the environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY not found in .env.")
        
        return api_key
    
    # Retrieves the OpenAI client
    def getClient(self):

        if not self.client:
            raise ValueError("❌ client not found. Please setup the client first.")

        return self.client
