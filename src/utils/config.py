"""
Configuration module for the MeteoApp.
Centralizes all configuration values and settings.
"""
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

