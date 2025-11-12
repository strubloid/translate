from packages.Translator.Translator import Translator
from transformers import MBart50TokenizerFast, MBartForConditionalGeneration
import torch
from packages.Translator.LanguageMap import LanguageMap

class TranslatorFacebook(Translator):

    def __init__(self, config=None):
        super().__init__(config)

        model_name = "facebook/mbart-large-50-many-to-many-mmt"

        # Load model + tokenizer
        self.tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
        self.model = MBartForConditionalGeneration.from_pretrained(model_name)

        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def translate(self, text, client=None):
        self.cleanFile(self.config.getOutputFile())

        # Load mapped language codes from JSON
        source_lang_code = LanguageMap.getMBartLanguageCode(self.config.getFromTranslationLanguage())
        target_lang_code = LanguageMap.getMBartLanguageCode(self.config.getTranslationLanguage())

        # Set source language
        self.tokenizer.src_lang = source_lang_code

        # Tokenize and move to device
        encoded = self.tokenizer(text.strip(), return_tensors="pt").to(self.device)

        # Force BOS token in the target language
        forced_bos_token_id = self.tokenizer.lang_code_to_id[target_lang_code]

        # Translate
        translated = self.model.generate(**encoded, forced_bos_token_id=forced_bos_token_id)
        output = self.tokenizer.decode(translated[0], skip_special_tokens=True)

        # Optionally write to file
        if self.config and hasattr(self.config, "getOutputFile"):
            self.writeToOBS(self.config.getOutputFile(), output)

        return output
