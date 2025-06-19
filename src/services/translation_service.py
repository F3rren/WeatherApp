from utils.translations_data import TRANSLATIONS
from utils.config import DEFAULT_LANGUAGE, UNIT_SYSTEMS # Added UNIT_SYSTEMS

class TranslationService:

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
            return DEFAULT_LANGUAGE  # Default to lowercase 'en'
        
        normalized_code = code.replace("-", "_").lower()
        
        # Special cases like zh_cn should be preserved if they exist as keys
        if normalized_code in TRANSLATIONS:
            return normalized_code
        
        # General case: try the main part of the language code (e.g., 'en' from 'en_us')
        main_lang_part = normalized_code.split("_")[0]
        if main_lang_part in TRANSLATIONS:
            return main_lang_part
            
        # Fallback if no specific or main part match is found
        return DEFAULT_LANGUAGE # Default to 'en' if no match

    @classmethod
    def get_unit_symbol(cls, quantity: str, unit_system: str) -> str: # Removed language parameter
        """Get the unit symbol from UNIT_SYSTEMS in config.py."""
        try:
            # Corrected access to UNIT_SYSTEMS
            return UNIT_SYSTEMS[unit_system][quantity]
        except KeyError:
            print(f"[TranslationService] Unit symbol not found for unit_system='{unit_system}', quantity='{quantity}'")
            # Fallback to a default or handle error as appropriate
            # For example, returning the quantity name or a placeholder
            if unit_system == "standard" and quantity == "temperature":
                 return "K" # Kelvin for standard temperature
            return "?" # Placeholder for unknown units

    @classmethod
    def translate_weekday(cls, day_key: str, language: str) -> str:
        """
        Traduce il giorno della settimana usando solo il file translations_data.py.
        """
        lang = cls.normalize_lang_code(language)
        day_key_lower = str(day_key).lower()
        # Prova nella lingua richiesta
        if lang in TRANSLATIONS and day_key_lower in TRANSLATIONS[lang]:
            return TRANSLATIONS[lang][day_key_lower]
        # Fallback inglese
        if day_key_lower in TRANSLATIONS.get("en", {}):
            return TRANSLATIONS["en"][day_key_lower]
        # Fallback: restituisci la chiave originale
        return day_key

    @classmethod
    def get_chemical_elements(cls, language_code: str) -> dict:
        """Returns the dictionary of chemical elements for the given language."""
        from utils.translations_data import TRANSLATIONS
        target_lang = cls.normalize_lang_code(language_code)
        try:
            elements = TRANSLATIONS.get(target_lang, {}).get("chemical_elements", {})
            if not elements and target_lang != 'en':  # Fallback to English
                elements = TRANSLATIONS.get('en', {}).get("chemical_elements", {})
            return elements
        except KeyError:
            # Fallback to English if the language itself is not found or chemical_elements key is missing
            return TRANSLATIONS.get('en', {}).get("chemical_elements", {})
        
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
            for aqi_range, description in TRANSLATIONS[DEFAULT_LANGUAGE]["aqi_descriptions"].items():
                min_aqi, max_aqi = map(int, aqi_range.split("-"))
                if min_aqi <= aqi_value <= max_aqi:
                    return description
        except Exception as e:
            print(f"[TranslationService] Error in English AQI description fallback: {e}")
        
        return TRANSLATIONS[DEFAULT_LANGUAGE]["aqi_descriptions"].get("default", "")

    @classmethod
    def translate(cls, key, language=None):
        """
        Restituisce la traduzione per la chiave richiesta in base alla lingua selezionata.
        language va passato esplicitamente (es. da state_manager.get_state("language")).
        """
        from utils.translations_data import TRANSLATIONS
        from utils.config import DEFAULT_LANGUAGE
        lang = cls.normalize_lang_code(language or DEFAULT_LANGUAGE)
        if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
            return TRANSLATIONS[lang][key]
        if key in TRANSLATIONS.get("en", {}):
            return TRANSLATIONS["en"][key]
        return key

    @classmethod
    def translate_from_dict(cls, dict_key, key, language=None):
        """
        Restituisce la traduzione per la chiave richiesta all'interno di un sotto-dizionario strutturato.
        dict_key: es. 'main_information_items', 'weekly_forecast_items', ...
        key: la chiave da tradurre all'interno del sotto-dizionario
        language: codice lingua
        """
        from utils.translations_data import TRANSLATIONS
        from utils.config import DEFAULT_LANGUAGE
        lang = cls.normalize_lang_code(language or DEFAULT_LANGUAGE)
        if lang in TRANSLATIONS and dict_key in TRANSLATIONS[lang]:
            subdict = TRANSLATIONS[lang][dict_key]
            if key in subdict:
                return subdict[key]
        # Fallback su inglese
        if dict_key in TRANSLATIONS.get("en", {}):
            subdict = TRANSLATIONS["en"][dict_key]
            if key in subdict:
                return subdict[key]
        return key
