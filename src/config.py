"""
Configuration module for the MeteoApp.
Centralizes all configuration values and settings.
"""

# Default application settings
DEFAULT_CITY = "Milan"
DEFAULT_LANGUAGE = "en"
DEFAULT_UNIT = "metric"  # "metric", "imperial", or "standard"
DEFAULT_THEME_MODE = "light"  # "light" or "dark"

# Theme colors
# Colori per il tema chiaro
LIGHT_THEME = {
    "BACKGROUND": "#f5f5f5",
    "TEXT": "#000000",
    "SECONDARY_TEXT": "#555555",
    "ACCENT": "#0078d4",
    "CARD_BACKGROUND": "#ffffff",
    "BORDER": "#e0e0e0",
    "ICON": "#333333",
    "BUTTON_TEXT": "#ffffff",
    "BUTTON_BACKGROUND": "#0078d4",
    "DIALOG_BACKGROUND": "#ffffff",
    "DIALOG_TEXT": "#000000",
    "GRADIENT": {
        "LINEAR": {
            "BEGIN": "#ffffff",
            "END": "#f0f0f0"
        },
        "RADIAL": {
            "CENTER": "#ffffff",
            "RADIUS": "#f0f0f0"
        }
    }
}

# Colori per il tema scuro
DARK_THEME = {
    "BACKGROUND": "#1a1a1a",
    "TEXT": "#ffffff",
    "SECONDARY_TEXT": "#cccccc",
    "ACCENT": "#0078d4",
    "CARD_BACKGROUND": "#262626",
    "BORDER": "#444444",
    "ICON": "#ffffff",
    "BUTTON_TEXT": "#ffffff",
    "BUTTON_BACKGROUND": "#0078d4",
    "DIALOG_BACKGROUND": "#262626",
    "DIALOG_TEXT": "#ffffff",
    "GRADIENT": {
        "LINEAR": {
            "BEGIN": "#333333",
            "END": "#1a1a1a"
        },
        "RADIAL": {
            "CENTER": "#262626",
            "RADIUS": "#1a1a1a"
        }
    }
}




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
    {"code": "AL", "name": "Shqip", "flag": "al.png"},
    {"code": "ZA", "name": "Afrikaans", "flag": "za.png"},
    {"code": "SA", "name": "العربية", "flag": "sa.png"},
    {"code": "AZ", "name": "Azərbaycan dili", "flag": "az.png"},
    {"code": "ES", "name": "Español", "flag": "es.png"},
    {"code": "BY", "name": "Беларуская", "flag": "by.png"},
    {"code": "BG", "name": "Български", "flag": "bg.png"},
    {"code": "CN", "name": "简体中文", "flag": "cn.png"},
    {"code": "TW", "name": "繁體中文", "flag": "tw.png"},
    {"code": "HR", "name": "Hrvatski", "flag": "hr.png"},
    {"code": "CZ", "name": "Čeština", "flag": "cz.png"},
    {"code": "DK", "name": "Dansk", "flag": "dk.png"},
    {"code": "NL", "name": "Nederlands", "flag": "nl.png"},
    {"code": "GB", "name": "English", "flag": "gb.png"},
    {"code": "FI", "name": "Suomi", "flag": "fi.png"},
    {"code": "FR", "name": "Français", "flag": "fr.png"},
    {"code": "DE", "name": "Deutsch", "flag": "de.png"},
    {"code": "GR", "name": "Ελληνικά", "flag": "gr.png"},
    {"code": "IL", "name": "עברית", "flag": "il.png"},
    {"code": "IN", "name": "हिन्दी", "flag": "in.png"},
    {"code": "HU", "name": "Magyar", "flag": "hu.png"},
    {"code": "IS", "name": "Íslenska", "flag": "is.png"},
    {"code": "ID", "name": "Bahasa Indonesia", "flag": "id.png"},
    {"code": "IT", "name": "Italiano", "flag": "it.png"},
    {"code": "JP", "name": "日本語", "flag": "jp.png"},
    {"code": "KR", "name": "한국어", "flag": "kr.png"},
    {"code": "TR", "name": "Türkçe", "flag": "tr.png"},
    {"code": "LV", "name": "Latviešu", "flag": "lv.png"},
    {"code": "LT", "name": "Lietuvių", "flag": "lt.png"},
    {"code": "MK", "name": "Македонски", "flag": "mk.png"},
    {"code": "NO", "name": "Norsk", "flag": "no.png"},
    {"code": "IR", "name": "فارسی", "flag": "ir.png"},
    {"code": "PL", "name": "Polski", "flag": "pl.png"},
    {"code": "PT", "name": "Português", "flag": "pt.png"},
    {"code": "BR", "name": "Português (Brasil)", "flag": "br.png"},
    {"code": "RO", "name": "Română", "flag": "ro.png"},
    {"code": "RU", "name": "Русский", "flag": "ru.png"},
    {"code": "RS", "name": "Српски", "flag": "rs.png"},
    {"code": "SK", "name": "Slovenčina", "flag": "sk.png"},
    {"code": "SI", "name": "Slovenščina", "flag": "si.png"},
    {"code": "SE", "name": "Svenska", "flag": "se.png"},
    {"code": "TH", "name": "ไทย", "flag": "th.png"},
    {"code": "UA", "name": "Українська", "flag": "ua.png"},
    {"code": "VN", "name": "Tiếng Việt", "flag": "vn.png"}
]

