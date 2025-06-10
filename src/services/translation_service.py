from deep_translator import GoogleTranslator
from utils.translations_data import TRANSLATIONS
from utils.config import DEFAULT_LANGUAGE

class TranslationService:
    
    TRANSLATIONS = TRANSLATIONS

    @classmethod
    def normalize_lang_code(cls, code):  # Renamed from _normalize_lang_code
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
        target = cls.normalize_lang_code(target_language)  # Updated call
        source = cls.normalize_lang_code(source_language)  # Updated call
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

    @classmethod
    def get_unit_symbol(cls, quantity: str, unit_system: str, language: str = None) -> str:
        """Get the translation for a unit symbol."""
        # Use the provided language, or fall back to the default language.
        # Ensure that language normalization is handled if necessary, similar to get_text.
        # This example assumes direct use of language codes as keys in TRANSLATIONS.
        target_lang = cls.normalize_lang_code(language if language else DEFAULT_LANGUAGE) # Updated call

        try:
            # Navigate through the translations dictionary to find the unit symbol.
            return cls.TRANSLATIONS[target_lang]["unit_symbols"][unit_system][quantity]
        except KeyError:
            # Fallback for missing translations: return an empty string or a default symbol.
            # Consider logging this event for missing translations.
            print(f"[TranslationService] Unit symbol not found for lang='{target_lang}', unit_system='{unit_system}', quantity='{quantity}'")
            # Fallback to English if the specific language symbol is not found
            if target_lang != 'en':
                try:
                    return cls.TRANSLATIONS['en']["unit_symbols"][unit_system][quantity]
                except KeyError:
                    pass # English fallback also failed
            return "" # Default empty string if no symbol is found

    @classmethod
    def translate_weekday(cls, day_key: str, language: str) -> str:
        """Translates a weekday key (e.g., 'mon', 'tue') to the target language."""
        target_lang = cls.normalize_lang_code(language) # Updated call
        day_key_lower = day_key.lower() # Ensure key is lowercase for matching

        try:
            # Attempt to find the translation directly under the language key
            return cls.TRANSLATIONS[target_lang][day_key_lower]
        except KeyError:
            # Fallback for missing translations
            print(f"[TranslationService] Weekday translation not found for lang='{target_lang}', day_key='{day_key_lower}'")
            # Fallback to English if the specific language translation is not found
            if target_lang != 'en':
                try:
                    return cls.TRANSLATIONS['en'][day_key_lower]
                except KeyError:
                    # If English fallback also fails, return the original key or a placeholder
                    return day_key_lower.capitalize() # Capitalize as a simple default
            return day_key_lower.capitalize() # Default if English key is also missing

    @classmethod
    def get_chemical_elements(cls, language: str) -> list[tuple[str, str]]:
        """Gets the translated list of chemical element symbols and their descriptions."""
        target_lang = cls.normalize_lang_code(language)
        default_elements = [
            ("CO", "Carbon Monoxide"),
            ("NO", "Nitrogen Monoxide"),
            ("NO2", "Nitrogen Dioxide"),
            ("O3", "Ozone"),
            ("SO2", "Sulphur Dioxide"),
            ("PM2.5", "Fine Particulate Matter"),
            ("PM10", "Coarse Particulate Matter"),
            ("NH3", "Ammonia"),
        ]

        try:
            elements = cls.TRANSLATIONS[target_lang]["chemical_elements"]
            # Ensure it's a list of tuples/lists with 2 strings each
            if not isinstance(elements, list) or not all(isinstance(el, (list, tuple)) and len(el) == 2 and isinstance(el[0], str) and isinstance(el[1], str) for el in elements):
                print(f"[TranslationService] chemical_elements for lang='{target_lang}' is not in the expected format. Using English fallback.")
                return cls.TRANSLATIONS['en'].get("chemical_elements", default_elements)
            return elements
        except KeyError:
            print(f"[TranslationService] Chemical elements not found for lang='{target_lang}'. Using English fallback.")
            # Fallback to English if the specific language elements are not found
            if target_lang != 'en':
                try:
                    return cls.TRANSLATIONS['en']["chemical_elements"]
                except KeyError:
                    print("[TranslationService] English chemical_elements also not found. Using hardcoded default.")
                    return default_elements # Hardcoded default as ultimate fallback
            return default_elements # Default if English key is also missing
