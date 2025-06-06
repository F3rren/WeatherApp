class TranslationService:
    _translations = {
        "en": {
            "feels_like": "Feels like",
            "humidity": "Humidity",
            "wind": "Wind",
            "pressure": "Pressure",
            "air_condition_title": "Air Conditions",
            "settings": "Settings",
            "measurement": "Measurement",
            "use_current_location": "Use current location:",
            "dark_theme": "Dark theme:",
            "language": "Language:",
            "close": "Close",
        },
        "it": {
            "feels_like": "Percepita",
            "humidity": "Umidità",
            "wind": "Vento",
            "pressure": "Pressione",
            "air_condition_title": "Condizioni Atmosferiche",
            "settings": "Impostazioni",
            "measurement": "Unità di misura",
            "use_current_location": "Usa posizione attuale:",
            "dark_theme": "Tema scuro:",
            "language": "Lingua:",
            "close": "Chiudi",
        },
        "fr": {
            "feels_like": "Ressenti",
            "humidity": "Humidité",
            "wind": "Vent",
            "pressure": "Pression",
            "air_condition_title": "Conditions de l'air",
            "settings": "Paramètres",
            "measurement": "Mesure",
            "use_current_location": "Utiliser la position actuelle :",
            "dark_theme": "Thème sombre :",
            "language": "Langue :",
            "close": "Fermer",
        }
        # Puoi aggiungere altre lingue qui
    }

    @classmethod
    def get_text(cls, key, language):
        lang = (language or "en").lower()
        if lang not in cls._translations:
            lang = "en"
        return cls._translations[lang].get(key, cls._translations["en"].get(key, key))
