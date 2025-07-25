"""
Language configuration for MeteoApp.
Contains all supported languages and their metadata.
"""

SUPPORTED_LANGUAGES = [
    {"code": "ar", "name": "العربية", "flag": "ar.png", "rtl": True},
    {"code": "id", "name": "Bahasa Indonesia", "flag": "id.png", "rtl": False},
    {"code": "de", "name": "Deutsch", "flag": "de.png", "rtl": False},
    {"code": "en", "name": "English", "flag": "gb.png", "rtl": False},
    {"code": "fr", "name": "Français", "flag": "fr.png", "rtl": False},
    {"code": "hi", "name": "हिन्दी", "flag": "in.png", "rtl": False},
    {"code": "it", "name": "Italiano", "flag": "it.png", "rtl": False},
    {"code": "ja", "name": "日本語", "flag": "jp.png", "rtl": False},
    {"code": "pt", "name": "Português", "flag": "pt.png", "rtl": False},
    {"code": "ru", "name": "Русский", "flag": "ru.png", "rtl": False},
    {"code": "es", "name": "Español", "flag": "es.png", "rtl": False},
    {"code": "zh_cn", "name": "简体中文", "flag": "cn.png", "rtl": False},
]

# Utility functions
def get_language_by_code(code: str) -> dict:
    """Get language metadata by language code."""
    return next((lang for lang in SUPPORTED_LANGUAGES if lang["code"] == code), None)

def get_all_language_codes() -> list:
    """Get list of all supported language codes."""
    return [lang["code"] for lang in SUPPORTED_LANGUAGES]

def is_rtl_language(code: str) -> bool:
    """Check if a language is right-to-left."""
    lang = get_language_by_code(code)
    return lang["rtl"] if lang else False
