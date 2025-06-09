from utils.translations_data import TRANSLATIONS
from deep_translator import GoogleTranslator

class TranslationService:
    TRANSLATIONS = TRANSLATIONS
    CHEMICAL_ELEMENTS = [
        ("CO", "Carbon monoxide"),
        ("NO", "Nitrogen monoxide"),
        ("NO₂", "Nitrogen dioxide"),
        ("O₃", "Ozone"),
        ("SO₂", "Sulphur dioxide"),
        ("PM2.5", "Fine particles (PM2.5)"),
        ("PM10", "Coarse particles (PM10)"),
        ("NH₃", "Ammonia"),
    ]

    # Mapping of app language codes to GoogleTranslator supported codes
    GOOGLE_TRANSLATOR_LANG_CODES = {
        'af': 'af', 'sq': 'sq', 'am': 'am', 'ar': 'ar', 'hy': 'hy', 'as': 'as', 'ay': 'ay', 'az': 'az', 'bm': 'bm',
        'eu': 'eu', 'be': 'be', 'bn': 'bn', 'bho': 'bho', 'bs': 'bs', 'bg': 'bg', 'ca': 'ca', 'ceb': 'ceb', 'ny': 'ny',
        'zh': 'zh-CN', 'zh_cn': 'zh-CN', 'zh-cn': 'zh-CN', 'zh_tw': 'zh-TW', 'zh-tw': 'zh-TW', 'co': 'co', 'hr': 'hr',
        'cs': 'cs', 'da': 'da', 'dv': 'dv', 'doi': 'doi', 'nl': 'nl', 'en': 'en', 'eo': 'eo', 'et': 'et', 'ee': 'ee',
        'tl': 'tl', 'fi': 'fi', 'fr': 'fr', 'fy': 'fy', 'gl': 'gl', 'ka': 'ka', 'de': 'de', 'el': 'el', 'gn': 'gn',
        'gu': 'gu', 'ht': 'ht', 'ha': 'ha', 'haw': 'haw', 'iw': 'iw', 'he': 'iw', 'hi': 'hi', 'hmn': 'hmn', 'hu': 'hu',
        'is': 'is', 'ig': 'ig', 'ilo': 'ilo', 'id': 'id', 'ga': 'ga', 'it': 'it', 'ja': 'ja', 'jw': 'jw', 'kn': 'kn',
        'kk': 'kk', 'km': 'km', 'rw': 'rw', 'gom': 'gom', 'ko': 'ko', 'kri': 'kri', 'ku': 'ku', 'ckb': 'ckb', 'ky': 'ky',
        'lo': 'lo', 'la': 'la', 'lv': 'lv', 'ln': 'ln', 'lt': 'lt', 'lg': 'lg', 'lb': 'lb', 'mk': 'mk', 'mai': 'mai',
        'mg': 'mg', 'ms': 'ms', 'ml': 'ml', 'mt': 'mt', 'mi': 'mi', 'mr': 'mr', 'mni-mtei': 'mni-Mtei', 'lus': 'lus',
        'mn': 'mn', 'my': 'my', 'ne': 'ne', 'no': 'no', 'or': 'or', 'om': 'om', 'ps': 'ps', 'fa': 'fa', 'pl': 'pl',
        'pt': 'pt', 'pt_br': 'pt', 'pt-pt': 'pt', 'pa': 'pa', 'qu': 'qu', 'ro': 'ro', 'ru': 'ru', 'sm': 'sm', 'sa': 'sa',
        'gd': 'gd', 'nso': 'nso', 'sr': 'sr', 'st': 'st', 'sn': 'sn', 'sd': 'sd', 'si': 'si', 'sk': 'sk', 'sl': 'sl',
        'so': 'so', 'es': 'es', 'su': 'su', 'sw': 'sw', 'sv': 'sv', 'tg': 'tg', 'ta': 'ta', 'tt': 'tt', 'te': 'te',
        'th': 'th', 'ti': 'ti', 'ts': 'ts', 'tr': 'tr', 'tk': 'tk', 'ak': 'ak', 'uk': 'uk', 'ur': 'ur', 'ug': 'ug',
        'uz': 'uz', 'vi': 'vi', 'cy': 'cy', 'xh': 'xh', 'yi': 'yi', 'yo': 'yo', 'zu': 'zu'
    }

    _translation_cache = {}

    @staticmethod
    def normalize_lang_code(code):
        """
        Normalizza il codice lingua per l'accesso al dizionario delle traduzioni.
        Esempi:
        - 'it-IT', 'it_IT', 'IT' -> 'it'
        - 'zh-cn', 'zh_CN', 'zh-hans' -> 'zh_CN'
        - 'en' -> 'en'
        """
        if not code:
            return 'en'
        code = code.replace('-', '_').lower()
        # Gestione speciale per cinese semplificato
        if code in ("zh_cn", "zh-hans", "zh_sg"):
            return "zh-CN"
        # Gestione speciale per cinese tradizionale (se aggiungi zh_TW)
        if code in ("zh_tw", "zh-hant"):
            return "zh-TW"
        # Altri codici: usa solo la parte principale (es: 'it', 'fr')
        base = code.split('_')[0]
        if base in TranslationService.TRANSLATIONS:
            return base
        # Fallback su inglese
        return 'en'

    @staticmethod
    def map_language_code_for_google(code: str) -> str:
        """
        Map app language code to GoogleTranslator supported code.
        Handles region codes and falls back to English if not supported.
        """
        if not code:
            return 'en'
        code = code.replace('-', '_').lower()
        # Direct match
        if code in TranslationService.GOOGLE_TRANSLATOR_LANG_CODES:
            return TranslationService.GOOGLE_TRANSLATOR_LANG_CODES[code]
        # Try base language (e.g., 'pt_br' -> 'pt')
        base = code.split('_')[0]
        if base in TranslationService.GOOGLE_TRANSLATOR_LANG_CODES:
            return TranslationService.GOOGLE_TRANSLATOR_LANG_CODES[base]
        # Try with dash
        code_dash = code.replace('_', '-')
        if code_dash in TranslationService.GOOGLE_TRANSLATOR_LANG_CODES:
            return TranslationService.GOOGLE_TRANSLATOR_LANG_CODES[code_dash]
        # Fallback to English
        return 'en'

    @classmethod
    def get_text(cls, key, language):
        """
        Restituisce la traduzione per la chiave e la lingua specificata.
        Se non trovata, ritorna la chiave stessa.
        """
        lang_code = cls.normalize_lang_code(language)
        return cls.TRANSLATIONS.get(lang_code, cls.TRANSLATIONS['en']).get(key, key)

    @classmethod
    def get_pollution_elements(cls, language):
        """
        Restituisce la lista degli elementi di inquinamento tradotti per la lingua.
        """
        lang_code = cls.normalize_lang_code(language)
        return cls.TRANSLATIONS.get(lang_code, cls.TRANSLATIONS['en']).get('pollution_elements', [])

    @classmethod
    def get_aqi_descriptions(cls, language):
        """
        Restituisce la lista delle descrizioni AQI tradotte per la lingua.
        """
        lang_code = cls.normalize_lang_code(language)
        return cls.TRANSLATIONS.get(lang_code, cls.TRANSLATIONS['en']).get('aqi_descriptions', [])

    @classmethod
    def clear_cache(cls):
        cls._translation_cache.clear()

    @classmethod
    def get_chemical_elements(cls, language):
        """
        Restituisce la lista degli elementi chimici tradotti per la lingua.
        Usa una cache per evitare chiamate ripetute eccessive.
        Ottimizzato: usa batch translation se possibile, fallback su traduzione singola se necessario.
        """
        google_code = cls.map_language_code_for_google(language)
        cache_key = f"chem_elements_{google_code}"
        if cache_key in cls._translation_cache:
            return cls._translation_cache[cache_key]
        elements = []
        descriptions = [desc for _, desc in cls.CHEMICAL_ELEMENTS]
        if google_code in ('en', 'en-us', 'en-gb'):
            elements = [(symbol, desc) for symbol, desc in cls.CHEMICAL_ELEMENTS]
        else:
            try:
                # Batch translation: GoogleTranslator accetta una lista (ma non per tutte le lingue)
                translated_list = GoogleTranslator(source='en', target=google_code).translate(descriptions)
                if not isinstance(translated_list, list):
                    raise ValueError('Batch translation did not return a list')
            except Exception:
                translated_list = []
                for desc in descriptions:
                    try:
                        translated = GoogleTranslator(source='en', target=google_code).translate(desc)
                    except Exception:
                        translated = desc
                    translated_list.append(translated)
            elements = [(symbol, translated) for (symbol, _), translated in zip(cls.CHEMICAL_ELEMENTS, translated_list)]
        cls._translation_cache[cache_key] = elements
        return elements

    @staticmethod
    def translate_weekday(day_key, language):
        """
        Restituisce la traduzione del giorno della settimana (accetta sia abbreviazioni che nomi estesi).
        """
        day_map = {
            "Mon": "Monday",
            "Tue": "Tuesday",
            "Wed": "Wednesday", 
            "Thu": "Thursday", 
            "Fri": "Friday",
            "Sat": "Saturday",
            "Sun": "Sunday",
        }

        
        key = day_map.get(day_key, day_key) #giorni
        # Normalizza la chiave per il lookup (es: Monday -> monday)
        return TranslationService.get_text(key.lower(), language)
