"""
Modern Translation Manager for MeteoApp.
Provides a modular, scalable approach to handling translations across the application.
"""

import logging
from typing import Dict, Any, Optional, List

# Import language configuration
from .languages import SUPPORTED_LANGUAGES, get_language_by_code, get_all_language_codes

# Import translation modules
from .modules.navigation import MENU_TRANSLATIONS
from .modules.weather import WEATHER_TRANSLATIONS
from .modules.air_quality import AIR_QUALITY_TRANSLATIONS, AIR_QUALITY_INDICATORS
from .modules.settings import SETTINGS_TRANSLATIONS
from .modules.charts import CHARTS_TRANSLATIONS
from .modules.alerts import ALERTS_TRANSLATIONS
from .modules.popup_menu import POPUP_MENU_TRANSLATIONS
from .modules.maps import maps_alert_dialog_items
from .modules.units import unit_items


class TranslationManager:
    """
    Modern translation manager with modular structure.
    Handles loading, caching, and retrieving translations efficiently.
    """
    
    def __init__(self):
        self._translations_cache = {}
        self._loaded_modules = {}
        self._fallback_language = "en"
        self._initialize_translations()
    
    def _initialize_translations(self):
        """Initialize all translation modules."""
        try:
            # Load core modules
            self._loaded_modules.update({
                "navigation": MENU_TRANSLATIONS,
                "weather": WEATHER_TRANSLATIONS,
                "air_quality": AIR_QUALITY_TRANSLATIONS,
                "settings": SETTINGS_TRANSLATIONS,
                "charts": CHARTS_TRANSLATIONS,
                "alerts": ALERTS_TRANSLATIONS,
                "popup_menu": POPUP_MENU_TRANSLATIONS,
                "maps": {"maps_alert_dialog_items": maps_alert_dialog_items},
                "units": {"unit_items": unit_items}
            })
            
            # Build unified translation cache for faster access
            self._build_translation_cache()
            
            logging.info(f"TranslationManager: Loaded {len(self._loaded_modules)} translation modules")
            
        except Exception as e:
            logging.error(f"TranslationManager: Error initializing translations: {e}")
    
    def _build_translation_cache(self):
        """Build a unified cache for faster translation lookups."""
        try:
            # Create language-first structure for faster lookups
            for lang_code in get_all_language_codes():
                self._translations_cache[lang_code] = {}
                
                # Merge all modules for this language
                for module_name, module_data in self._loaded_modules.items():
                    self._translations_cache[lang_code][module_name] = {}
                    
                    for section_key, section_data in module_data.items():
                        self._translations_cache[lang_code][module_name][section_key] = {}
                        
                        for text_key, text_data in section_data.items():
                            if isinstance(text_data, dict) and lang_code in text_data:
                                self._translations_cache[lang_code][module_name][section_key][text_key] = text_data[lang_code]
                                
        except Exception as e:
            logging.error(f"TranslationManager: Error building translation cache: {e}")
    
    def get_translation(self, module: str, section: str, key: str, language: str = None) -> str:
        """
        Get a translation using the modular structure.
        
        Args:
            module: Module name (e.g., 'navigation', 'weather', 'air_quality')
            section: Section within module (e.g., 'popup_menu_items', 'air_condition_items')
            key: Translation key (e.g., 'weather', 'humidity')
            language: Target language code (defaults to fallback)
            
        Returns:
            Translated string or fallback text
        """
        try:
            target_lang = language or self._fallback_language
            
            # Try from cache first
            if (target_lang in self._translations_cache and 
                module in self._translations_cache[target_lang] and
                section in self._translations_cache[target_lang][module] and
                key in self._translations_cache[target_lang][module][section]):
                
                return self._translations_cache[target_lang][module][section][key]
            
            # Fallback to direct module lookup
            if module in self._loaded_modules:
                module_data = self._loaded_modules[module]
                if section in module_data and key in module_data[section]:
                    text_data = module_data[section][key]
                    if isinstance(text_data, dict):
                        return text_data.get(target_lang, text_data.get(self._fallback_language, key))
            
            # Final fallback
            logging.warning(f"TranslationManager: Missing translation for {module}.{section}.{key} in {target_lang}")
            return key
            
        except Exception as e:
            logging.error(f"TranslationManager: Error getting translation: {e}")
            return key
    
    def get_air_quality_indicator(self, indicator_type: str, level: str, language: str = None) -> str:
        """
        Get air quality indicator translation.
        
        Args:
            indicator_type: Type of indicator (e.g., 'humidity', 'uv_index', 'pressure')
            level: Quality level (e.g., 'excellent', 'good', 'poor')
            language: Target language code
            
        Returns:
            Translated indicator text
        """
        try:
            target_lang = language or self._fallback_language
            
            if indicator_type in AIR_QUALITY_INDICATORS:
                indicator_data = AIR_QUALITY_INDICATORS[indicator_type]
                if level in indicator_data:
                    level_data = indicator_data[level]
                    return level_data.get(target_lang, level_data.get(self._fallback_language, level))
            
            return level
            
        except Exception as e:
            logging.error(f"TranslationManager: Error getting air quality indicator: {e}")
            return level
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of all supported languages."""
        return SUPPORTED_LANGUAGES
    
    def is_language_supported(self, language_code: str) -> bool:
        """Check if a language is supported."""
        return language_code in get_all_language_codes()
    
    def get_language_info(self, language_code: str) -> Optional[Dict[str, str]]:
        """Get metadata for a specific language."""
        return get_language_by_code(language_code)
    
    def reload_translations(self):
        """Reload all translation modules (useful for development)."""
        logging.info("TranslationManager: Reloading translations...")
        self._translations_cache.clear()
        self._loaded_modules.clear()
        self._initialize_translations()
    
    def add_custom_module(self, module_name: str, module_data: Dict[str, Any]):
        """
        Add a custom translation module at runtime.
        
        Args:
            module_name: Name for the new module
            module_data: Translation data in the standard format
        """
        try:
            self._loaded_modules[module_name] = module_data
            # Rebuild cache to include new module
            self._build_translation_cache()
            logging.info(f"TranslationManager: Added custom module '{module_name}'")
            
        except Exception as e:
            logging.error(f"TranslationManager: Error adding custom module: {e}")
    
    def get_translation_stats(self) -> Dict[str, Any]:
        """Get statistics about loaded translations."""
        stats = {
            "modules": len(self._loaded_modules),
            "languages": len(get_all_language_codes()),
            "module_breakdown": {}
        }
        
        for module_name, module_data in self._loaded_modules.items():
            section_count = len(module_data)
            total_keys = sum(len(section) for section in module_data.values())
            stats["module_breakdown"][module_name] = {
                "sections": section_count,
                "total_keys": total_keys
            }
        
        return stats


# Global instance for easy access
translation_manager = TranslationManager()


# Backward compatibility functions
def translate_from_dict(section: str, key: str, language: str = None) -> str:
    """
    Backward compatibility function for existing translation calls.
    Automatically maps sections to appropriate modules.
    """
    # Module mapping for backward compatibility
    module_mapping = {
        "popup_menu_items": "navigation",
        "air_condition_items": "weather", 
        "precipitation_chart_items": "weather",
        "main_information_items": "weather",
        "weekly_forecast_items": "weather",
        "hourly_forecast_items": "weather",
        "temperature_chart_items": "charts",
        "general_chart_items": "charts",
        "settings_dialog": "settings",
        "unit_systems": "settings",
        "theme_options": "settings",
        "weather_alerts": "alerts",
        "alert_severity": "alerts",
        "notification_types": "alerts",
        "alert_actions": "alerts",
        # Add more mappings as needed
    }
    
    module = module_mapping.get(section, "weather")  # Default to weather module
    return translation_manager.get_translation(module, section, key, language)


def get_air_quality_translation(indicator_type: str, level: str, language: str = None) -> str:
    """Backward compatibility function for air quality indicators."""
    return translation_manager.get_air_quality_indicator(indicator_type, level, language)


# Export main components
__all__ = [
    'TranslationManager',
    'translation_manager', 
    'translate_from_dict',
    'get_air_quality_translation',
    'SUPPORTED_LANGUAGES'
]
