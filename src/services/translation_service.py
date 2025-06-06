from deep_translator import GoogleTranslator
from .translations_data import TRANSLATIONS


class TranslationService:
    @classmethod
    def get_text(cls, key_or_text, target_language, source_language="en"):
        """
        Traduci in modo intelligente:
        1. Se la lingua è supportata e la chiave è presente, usa la traduzione locale.
        2. Altrimenti, traduci il testo passato con deep-translator.
        3. Mantieni la maiuscola iniziale se il testo originale la aveva.
        """
        # Normalizza lingua
        target = (target_language or "en").split("-")[0].lower()
        source = (source_language or "en").split("-")[0].lower()
        # Prova dizionario centralizzato
        if target in TRANSLATIONS and key_or_text in TRANSLATIONS[target]:
            translated = TRANSLATIONS[target][key_or_text]
        elif source in TRANSLATIONS and key_or_text in TRANSLATIONS[source]:
            # Se la chiave esiste solo in inglese, traduci il valore inglese
            base_text = TRANSLATIONS[source][key_or_text]
            if target == source:
                translated = base_text
            else:
                try:
                    translated = GoogleTranslator(source=source, target=target).translate(base_text)
                except Exception as e:
                    print(f"[TranslationService] Translation error: {e}")
                    translated = base_text
        else:
            # Fallback: traduci direttamente il testo passato
            if target == source:
                translated = key_or_text
            else:
                try:
                    translated = GoogleTranslator(source=source, target=target).translate(key_or_text)
                except Exception as e:
                    print(f"[TranslationService] Translation error: {e}")
                    translated = key_or_text
        # Mantieni la maiuscola iniziale se il testo originale la aveva
        if key_or_text and key_or_text[0].isupper() and translated:
            return translated[0].upper() + translated[1:]
        return translated
