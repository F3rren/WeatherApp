"""
Configuration module for the MeteoApp.
Centralizes all configuration values and settings.
"""

# Default application settings
DEFAULT_CITY = "Milan"
DEFAULT_LANGUAGE = "en"
DEFAULT_UNIT = "metric"
DEFAULT_THEME_MODE = "light"  # "light" or "dark"

# API settings
API_BASE_URL = "https://api.openweathermap.org"
API_WEATHER_ENDPOINT = "/data/2.5/forecast"
API_GEO_ENDPOINT = "/geo/1.0/direct"
API_REVERSE_GEO_ENDPOINT = "/geo/1.0/reverse"
API_AIR_POLLUTION_ENDPOINT= "/data/2.5/air_pollution"

# Geolocation settings
GEO_ACCURACY = "high"  # "high" or "low"
GEO_DISTANCE_FILTER = 500  # meters
GEO_UPDATE_INTERVAL = 5  # seconds

# UI settings
UI_REFRESH_RATE = 5  # seconds

MEASUREMENT_UNITS = [
    {"code": "metric", "name": "Metric (°C, m/s)"},
    {"code": "imperial", "name": "Imperial (°F, mph)"},
    {"code": "standard", "name": "Standard (K, knt/h)"}
]

LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "af", "name": "Afrikaans"},
    {"code": "ar", "name": "العربية"},
    {"code": "az", "name": "Azərbaycan dili"},
    {"code": "be", "name": "Беларуская"},
    {"code": "bg", "name": "Български"},
    {"code": "ca", "name": "Català"},
    {"code": "cs", "name": "Čeština"},
    {"code": "da", "name": "Dansk"},
    {"code": "nl", "name": "Nederlands"},
    {"code": "fi", "name": "Suomi"},
    {"code": "fr", "name": "Français"},
    {"code": "gl", "name": "Galego"},
    {"code": "de", "name": "Deutsch"},
    {"code": "el", "name": "Ελληνικά"},
    {"code": "he", "name": "עברית"},
    {"code": "hi", "name": "हिन्दी"},
    {"code": "hr", "name": "Hrvatski"},
    {"code": "hu", "name": "Magyar"},
    {"code": "id", "name": "Bahasa Indonesia"},
    {"code": "is", "name": "Íslenska"},
    {"code": "it", "name": "Italiano"},
    {"code": "ja", "name": "日本語"},
    {"code": "kr", "name": "한국어"},
    {"code": "ku", "name": "Kurmancî"},
    {"code": "la", "name": "Latviešu"},
    {"code": "lt", "name": "Lietuvių"},
    {"code": "mk", "name": "Македонски"},
    {"code": "no", "name": "Norsk"},
    {"code": "fa", "name": "فارسی"},
    {"code": "pl", "name": "Polski"},
    {"code": "pt", "name": "Português"},
    {"code": "pt_br", "name": "Português (Brasil)"},
    {"code": "ro", "name": "Română"},
    {"code": "ru", "name": "Русский"},
    {"code": "sr", "name": "Српски"},
    {"code": "sk", "name": "Slovenčina"},
    {"code": "sl", "name": "Slovenščina"},
    {"code": "es", "name": "Español"},
    {"code": "sq", "name": "Shqip"},
    {"code": "sv", "name": "Svenska"},
    {"code": "th", "name": "ไทย"},
    {"code": "tr", "name": "Türkçe"},
    {"code": "uk", "name": "Українська"},
    {"code": "eu", "name": "Euskara"},
    {"code": "vi", "name": "Tiếng Việt"},
    {"code": "zh_cn", "name": "简体中文"},
    {"code": "zh_tw", "name": "繁體中文"},
    {"code": "zu", "name": "isiZulu"}
]
