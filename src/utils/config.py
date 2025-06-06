"""
Configuration module for the MeteoApp.
Centralizes all configuration values and settings.
"""

# Default application settings
DEFAULT_CITY = "Milano"
DEFAULT_LANGUAGE = "en"
DEFAULT_UNIT = "metric"  # "metric", "imperial", or "standard"
DEFAULT_THEME_MODE = "light"  # "light" or "dark"

# Theme colors
# Colori per il tema chiaro
LIGHT_THEME = {
    "BACKGROUND": "#f5f5f5",
    "TEXT": "#000000",
    "SECONDARY_TEXT": "#555555",
    "ACCENT": "#6b46c1",  # Cambiato da azzurro a viola
    "CARD_BACKGROUND": "#ffffff",
    # Aggiungo il gradiente per il container info (main meteo container)
    "INFO_GRADIENT": {
        "start": "#78bff1",  # Azzurro chiaro
        "end": "#ffffff"     # Bianco
    },
    "BORDER": "#e0e0e0",
    "ICON": "#333333",
    "BUTTON_TEXT": "#ffffff",
    "BUTTON_BACKGROUND": "#6b46c1",  # Cambiato da azzurro a viola
    "DIALOG_BACKGROUND": "#ffffff",
    "DIALOG_TEXT": "#000000",
}

# Colori per il tema scuro
DARK_THEME = {
    "BACKGROUND": "#1a1a1a",
    "TEXT": "#ffffff",
    "SECONDARY_TEXT": "#cccccc",
    "ACCENT": "#8b5cf6",  # Cambiato da azzurro a viola più chiaro per il tema scuro
    "CARD_BACKGROUND": "#262626",
    # Aggiungo il gradiente per il container info (main meteo container) nel tema scuro
    "INFO_GRADIENT": {
        "start": "#78bff1",  # Blu scuro
        "end": "#262626"     # Nero
    },
    "BORDER": "#444444",
    "ICON": "#ffffff",
    "BUTTON_TEXT": "#ffffff",
    "BUTTON_BACKGROUND": "#8b5cf6",  # Cambiato da azzurro a viola più chiaro
    "DIALOG_BACKGROUND": "#262626",
    "DIALOG_TEXT": "#ffffff",
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

