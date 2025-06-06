from deep_translator import GoogleTranslator
from utils.translations_data import TRANSLATIONS

class TranslationService:
    TRANSLATIONS = TRANSLATIONS

    @classmethod
    def _normalize_lang_code(cls, code):
        """
        Normalizza il codice lingua per l'accesso al dizionario locale.
        Esempio: 'zh-cn', 'ZH_CN', 'zh_CN' -> 'zh_CN'
        """
        if not code:
            return "en"
        code = code.replace("-", "_").lower()
        # Gestione speciale per cinese semplificato
        if code in ("zh_cn", "zh-hans", "zh_sg"):
            return "zh_CN"
        # Gestione speciale per cinese tradizionale (se aggiungi zh_TW)
        if code in ("zh_tw", "zh-hant"):
            return "zh_TW"
        # Altri codici: usa solo la parte principale (es: 'it', 'fr')
        return code.upper() if code.upper() in cls.TRANSLATIONS else code.split("_")[0]

    @classmethod
    def get_text(cls, key_or_text, target_language, source_language="en"):
        """
        1. Se la lingua è supportata e la chiave è presente, usa la traduzione locale.
        2. Altrimenti, traduci il testo passato con deep-translator.
        3. Mantieni la maiuscola iniziale se il testo originale la aveva.
        """
        target = cls._normalize_lang_code(target_language)
        source = cls._normalize_lang_code(source_language)
        # Prova dizionario locale
        if target in cls.TRANSLATIONS and key_or_text in cls.TRANSLATIONS[target]:
            translated = cls.TRANSLATIONS[target][key_or_text]
        elif source in cls.TRANSLATIONS and key_or_text in cls.TRANSLATIONS[source]:
            # Se la chiave esiste solo in inglese, traduci il valore inglese
            base_text = cls.TRANSLATIONS[source][key_or_text]
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
