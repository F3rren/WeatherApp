from deep_translator import GoogleTranslator
from langdetect import detect

class Translator:

    def __init__(self, language):
        self.lang = language

    def getLanguage(self):
        return self.lang

    def translate(self, text):
        try:
            source_language = detect(text)
            text = GoogleTranslator(source=source_language, target=self.lang).translate(source_language)
            return text
        except Exception as e:
            print(f"Errore nella traduzione: {e}")
            return None


       