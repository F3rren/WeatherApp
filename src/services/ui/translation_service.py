import logging
import os

from dotenv import load_dotenv
from utils.config import UNIT_SYSTEMS
from utils.translations_data import TRANSLATIONS

class TranslationService:
    _global_instance = None  # Class variable for global instance

    def __init__(self, session=None):  # Modified to accept session
        load_dotenv()
        self.session = session
        if session is None:
            try:
                # Try to get session from page if available
                if hasattr(self, 'page') and self.page and hasattr(self.page, 'session'):
                    self.session = self.page.session
            except Exception:
                pass
                
        if self.session is None:
            logging.debug("TranslationService initialized without session - using static methods only")

    @classmethod
    def get_global_instance(cls):
        """Get the global translation service instance if available."""
        return cls._global_instance

    def get_current_language(self):  # Added instance method
        """Get current language from session or fallback to default."""
        if self.session:
            try:
                lang = self.session.get("current_language")
                return lang if lang is not None else os.getenv("DEFAULT_LANGUAGE")
            except Exception as e:
                logging.debug(f"Error accessing session language: {e}")
                
        # Try global instance if available
        if self._global_instance and self._global_instance.session:
            try:
                lang = self._global_instance.session.get("current_language")
                return lang if lang is not None else os.getenv("DEFAULT_LANGUAGE")
            except Exception:
                pass
                
        return os.getenv("DEFAULT_LANGUAGE")

    def update_session(self, session):
        """Update the session reference after initialization."""
        self.session = session
        logging.debug("TranslationService session updated")

    @classmethod
    def get_instance_with_session(cls, session):
        """Factory method to create instance with session."""
        return cls(session)

    @classmethod
    def normalize_lang_code(cls, code):  # Renamed from _normalize_lang_code
        if not code:
            return os.getenv("DEFAULT_LANGUAGE")  # Default to lowercase os.getenv("DEFAULT_LANGUAGE")
        
        normalized_code = code.replace("-", "_").lower()
        
        # Special cases like zh_cn should be preserved if they exist as keys
        if normalized_code in TRANSLATIONS:
            return normalized_code
        
        # General case: try the main part of the language code (e.g., os.getenv("DEFAULT_LANGUAGE") from 'en_us')
        main_lang_part = normalized_code.split("_")[0]
        if main_lang_part in TRANSLATIONS:
            return main_lang_part
            
        # Fallback if no specific or main part match is found
        return os.getenv("DEFAULT_LANGUAGE") # Default to os.getenv("DEFAULT_LANGUAGE") if no match

    @classmethod
    def get_unit_symbol(cls, quantity: str, unit_system: str) -> str: # Removed language parameter
        """Get the unit symbol from UNIT_SYSTEMS in config.py."""
        try:
            # Corrected access to UNIT_SYSTEMS
            return UNIT_SYSTEMS[unit_system][quantity]
        except KeyError:
            logging.error(f"[TranslationService] Unit symbol not found for unit_system='{unit_system}', quantity='{quantity}'")
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
            if not elements and target_lang != os.getenv("DEFAULT_LANGUAGE"):  # Fallback to English
                elements = TRANSLATIONS.get(os.getenv("DEFAULT_LANGUAGE"), {}).get("chemical_elements", {})
            return elements
        except KeyError:
            # Fallback to English if the language itself is not found or chemical_elements key is missing
            return TRANSLATIONS.get(os.getenv("DEFAULT_LANGUAGE"), {}).get("chemical_elements", {})
        
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
            logging.error(f"[TranslationService] Error getting AQI description: {e}")
        
        # Fallback to English if no suitable description is found
        try:
            for aqi_range, description in TRANSLATIONS[os.getenv("DEFAULT_LANGUAGE")]["aqi_descriptions"].items():
                min_aqi, max_aqi = map(int, aqi_range.split("-"))
                if min_aqi <= aqi_value <= max_aqi:
                    return description
        except Exception as e:
            logging.error(f"[TranslationService] Error in English AQI description fallback: {e}")
        
        return TRANSLATIONS[os.getenv("DEFAULT_LANGUAGE")]["aqi_descriptions"].get("default", "")

    @classmethod
    def translate(cls, key, language=None):
        """
        Restituisce la traduzione per la chiave richiesta in base alla lingua selezionata.
        language va passato esplicitamente (es. da state_manager.get_state("language")).
        """
        from utils.translations_data import TRANSLATIONS
        lang = cls.normalize_lang_code(language or os.getenv("DEFAULT_LANGUAGE"))
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
        lang = cls.normalize_lang_code(language or os.getenv("DEFAULT_LANGUAGE"))
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
