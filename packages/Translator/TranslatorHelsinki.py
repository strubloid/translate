from packages.Translator.Translator import Translator
from transformers import MarianMTModel, MarianTokenizer
import torch

## Local translator using MarianMT (English → Portuguese)
class TranslatorHelsinki(Translator):

    def __init__(self, config=None):
        super().__init__(config)

        # Correct model for Romance language translation (including pt-BR)
        # model_name = "Helsinki-NLP/opus-mt-en-ROMANCE"
        model_name = "Helsinki-NLP/opus-mt-tc-big-en-pt"


        # Load tokenizer and model
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

        # Move model to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

        ## Small change for pt-br fix
        self.targetLanguage = "pt" if self.targetLanguage == "pt-br" else self.targetLanguage

    ## Here we will be using the MarianMT model to translate text.
    # => The function takes the text to be translated and an optional client parameter (unused).
    # => It constructs a prompt for translation, tokenizes the input, and generates the translation.
    # => The translated text is decoded and returned.
    def translate(self, text, client=None):  # client is unused
        
        if self.config and hasattr(self.config, "getOutputFile"):
            path = self.config.getOutputFile()
            with open(path, "w", encoding="utf-8") as f:
                f.truncate()

        # Add language tag for Portuguese
        prompt = f">>{self.targetLanguage}<< {text.strip()}"

        # Tokenize and move input to the correct device
        tokens = self.tokenizer(prompt, return_tensors="pt", padding=True).to(self.device)

        # Generate translation
        translated = self.model.generate(**tokens)

        # Decode and return
        output = self.tokenizer.decode(translated[0], skip_special_tokens=True)

        # Optional: write to output file if configured
        if self.config and hasattr(self.config, "getOutputFile"):
            self.writeToOBS(self.config.getOutputFile(), output)

        return output