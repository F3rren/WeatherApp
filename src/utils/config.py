"""
Configuration module for the MeteoApp.
Centralizes all configuration values and settings.
"""

# Default application settings
DEFAULT_CITY = "Milano"
DEFAULT_LANGUAGE = "it"
DEFAULT_UNIT_SYSTEM = "metric"  # "metric", "imperial", or "standard"
DEFAULT_THEME_MODE = "light"  # "light" or "dark"

# Theme colors
# Colori per il tema chiaro
LIGHT_THEME = {
    "BACKGROUND": "#f0f8ff",  # Azzurro molto chiaro come sfondo principale
    "TEXT": "#2c3e50",
    "SECONDARY_TEXT": "#7f8c8d",
    "ACCENT": "#3498db",  # Blu accento
    "CARD_BACKGROUND": "#ffffff",
    "SIDEBAR": "#ffffff",  # Sidebar bianca
    # Gradiente per il container info principale (come nell'immagine)
    "INFO_GRADIENT": {
        "start": "#87ceeb",  # Sky blue
        "end": "#e6f3ff"     # Azzurro molto chiaro
    },
    "HOURLY": "#ffffff",  # Container previsioni orarie bianco
    "WEEKLY": "#ffffff",  # Container settimanale bianco
    "CHART": "#ffffff",   # Container grafici bianco
    "AIR_POLLUTION": "#ffffff",  # Container inquinamento bianco
    "AIR_POLLUTION_CHART": "#ffffff",  # Container grafico inquinamento bianco
    "BORDER": "#e1e8ed",
    "ICON": "#2c3e50",
    "BUTTON_TEXT": "#ffffff",
    "BUTTON_BACKGROUND": "#3498db",
    "DIALOG_BACKGROUND": "#7f8c8d",
    "DIALOG_TEXT": "#2c3e50",
    # Colori aggiuntivi per elementi specifici
    "TEMPERATURE_MAIN": "#2c3e50",  # Colore temperatura principale
    "WEATHER_DESCRIPTION": "#7f8c8d",  # Descrizione meteo
    "CARD_SHADOW": "#00000010",  # Ombra delle card
}

# Colori per il tema scuro
DARK_THEME = {
    "BACKGROUND": "#0d1117",  # Sfondo scuro moderno
    "TEXT": "#f0f6fc",
    "SECONDARY_TEXT": "#8b949e",
    "ACCENT": "#58a6ff",  # Blu accento per tema scuro
    "CARD_BACKGROUND": "#161b22",
    "SIDEBAR": "#161b22",  # Sidebar scura
    # Gradiente per il container info nel tema scuro
    "INFO_GRADIENT": {
        "start": "#1f2937",  # Grigio scuro
        "end": "#0d1117"     # Nero
    },
    "HOURLY": "#161b22",  # Container previsioni orarie scuro
    "WEEKLY": "#161b22",  # Container settimanale scuro
    "CHART": "#161b22",   # Container grafici scuro
    "AIR_POLLUTION": "#161b22",  # Container inquinamento scuro
    "AIR_POLLUTION_CHART": "#161b22",  # Container grafico inquinamento scuro
    "BORDER": "#30363d",
    "ICON": "#f0f6fc",
    "BUTTON_TEXT": "#ffffff",
    "BUTTON_BACKGROUND": "#58a6ff",
    "DIALOG_BACKGROUND": "#161b22",
    "DIALOG_TEXT": "#f0f6fc",
    # Colori aggiuntivi per elementi specifici
    "TEMPERATURE_MAIN": "#f0f6fc",  # Colore temperatura principale
    "WEATHER_DESCRIPTION": "#8b949e",  # Descrizione meteo
    "CARD_SHADOW": "#00000030",  # Ombra delle card
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

# Defines the available unit systems and their specific units.
# 'name_key' is used for fetching the translated name of the unit system.
UNIT_SYSTEMS = {
    "metric": {
        "name_key": "unit_metric",
        "temperature": "°C",
        "wind": "m/s",
        "pressure": "hPa"
    },
    "imperial": {
        "name_key": "unit_imperial",
        "temperature": "°F",
        "wind": "mph",
        "pressure": "hPa"  # OpenWeatherMap typically provides pressure in hPa for all systems
    },
    "standard": {
        "name_key": "unit_standard",
        "temperature": "°K",
        "wind": "m/s",      # API provides wind speed in m/s for the standard system
        "pressure": "hPa"
    }
}

