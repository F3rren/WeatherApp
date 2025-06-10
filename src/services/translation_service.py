from deep_translator import GoogleTranslator
from utils.translations_data import TRANSLATIONS
from utils.config import DEFAULT_LANGUAGE

class TranslationService:
    
    TRANSLATIONS = TRANSLATIONS

    def __init__(self, session=None):  # Modified to accept session
        self.session = session

    def get_current_language(self):  # Added instance method
        if self.session:
            lang = self.session.get("current_language")
            return lang if lang is not None else DEFAULT_LANGUAGE
        return DEFAULT_LANGUAGE

    @classmethod
    def normalize_lang_code(cls, code):  # Renamed from _normalize_lang_code
        """
        Normalizza il codice lingua per l'accesso al dizionario locale.
        Esempio: 'en', 'En', 'en-US' -> 'en'. 'zh-cn' -> 'zh_cn'
        """
        if not code:
            return "en"  # Default to lowercase 'en'
        
        normalized_code = code.replace("-", "_").lower()
        
        # Special cases like zh_cn should be preserved if they exist as keys
        if normalized_code in cls.TRANSLATIONS:
            return normalized_code
        
        # General case: try the main part of the language code (e.g., 'en' from 'en_us')
        main_lang_part = normalized_code.split("_")[0]
        if main_lang_part in cls.TRANSLATIONS:
            return main_lang_part
            
        # Fallback if no specific or main part match is found
        return "en" # Default to 'en' if no match

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
        target_lang = cls.normalize_lang_code(language if language else DEFAULT_LANGUAGE)

        try:
            return cls.TRANSLATIONS[target_lang]["unit_symbols"][unit_system][quantity]
        except KeyError:
            print(f"[TranslationService] Unit symbol not found for lang='{target_lang}', unit_system='{unit_system}', quantity='{quantity}'")
            # Fallback to English (lowercase 'en') if the specific language symbol is not found
            if target_lang != 'en': # Compare with lowercase 'en'
                try:
                    return cls.TRANSLATIONS['en']["unit_symbols"][unit_system][quantity] # Use lowercase 'en' for fallback
                except KeyError:
                    print(f"[TranslationService] English fallback failed for unit_system='{unit_system}', quantity='{quantity}'")
                    pass # English fallback also failed
            return "" # Default empty string if no symbol is found

    @classmethod
    def translate_weekday(cls, day_key: str, language: str) -> str:
        """Translates a weekday key (e.g., 'mon', 'tue') to the target language."""
        target_lang = cls.normalize_lang_code(language) # Updated call
        day_key_lower = str(day_key).lower() # Ensure key is lowercased string

        try:
            # Attempt to find the translation directly under the language key
            return cls.TRANSLATIONS[target_lang][day_key_lower]
        except KeyError:
            # Fallback for missing translations
            print(f"[TranslationService] Weekday translation not found for lang='{target_lang}', day_key='{day_key_lower}'")
            # Fallback to English if the specific language translation is not found
            if target_lang != 'en':
                try:
                    return cls.TRANSLATIONS['en'][day_key_lower] # Use lowercase 'en' for fallback
                except KeyError:
                    # If English fallback also fails, return the original key or a placeholder
                    print(f"[TranslationService] English fallback failed for weekday_key=\'{day_key_lower}\'")
                    pass # Fallback failed
            return day_key_lower.capitalize() # Capitalize as a last resort if no translation found

    @classmethod
    def get_chemical_elements(cls, language_code: str) -> dict: # Added class method
        """Returns the dictionary of chemical elements for the given language."""
        target_lang = cls.normalize_lang_code(language_code)
        try:
            elements = cls.TRANSLATIONS.get(target_lang, {}).get("chemical_elements", {})
            if not elements and target_lang != 'en': # Fallback to English
                elements = cls.TRANSLATIONS.get('en', {}).get("chemical_elements", {})
            return elements
        except KeyError:
            # Fallback to English if the language itself is not found or chemical_elements key is missing
            return cls.TRANSLATIONS.get('en', {}).get("chemical_elements", {})

    @classmethod
    def get_aqi_description(cls, aqi_value: int, lang_code: str) -> str:
        """Returns the translated description for an AQI value."""
        lang_code = cls.normalize_lang_code(lang_code)
        try:
            # Assuming AQI descriptions are structured as {range: description}
            for aqi_range, description in TRANSLATIONS[lang_code]["aqi_descriptions"].items():
                min_aqi, max_aqi = map(int, aqi_range.split("-"))
                if min_aqi <= aqi_value <= max_aqi:
                    return description
        except Exception as e:
            print(f"[TranslationService] Error getting AQI description: {e}")
        
        # Fallback to English if no suitable description is found
        try:
            for aqi_range, description in TRANSLATIONS["en"]["aqi_descriptions"].items():
                min_aqi, max_aqi = map(int, aqi_range.split("-"))
                if min_aqi <= aqi_value <= max_aqi:
                    return description
        except Exception as e:
            print(f"[TranslationService] Error in English AQI description fallback: {e}")
        
        return TRANSLATIONS["en"]["aqi_descriptions"].get("default", "")
