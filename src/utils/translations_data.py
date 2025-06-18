LANGUAGES = [
    {"code": "ar", "name": "العربية", "flag": "ar.png"},
    {"code": "id", "name": "Bahasa Indonesia", "flag": "id.png"},
    {"code": "de", "name": "Deutsch", "flag": "de.png"},
    {"code": "en", "name": "English", "flag": "gb.png"},
    {"code": "fr", "name": "Français", "flag": "fr.png"},
    {"code": "hi", "name": "हिन्दी", "flag": "in.png"},
    {"code": "it", "name": "Italiano", "flag": "it.png"},
    {"code": "ja", "name": "日本語", "flag": "jp.png"},
    {"code": "pt", "name": "Português", "flag": "pt.png"},
    {"code": "ru", "name": "Русский", "flag": "ru.png"},
    {"code": "es", "name": "Español", "flag": "es.png"},
    {"code": "zh_cn", "name": "简体中文", "flag": "cn.png"},
]


TRANSLATIONS = {
    "en": {
        "popup_menu_items": {
            "weather" : "Weather",
            "map" : "Map",
            "settings" : "Settings"
        },
        "air_condition_items": {
            "air_condition_title": "Air Conditions",
            "feels_like": "Feels like",
            "humidity": "Humidity",
            "wind": "Wind",
            "pressure": "Pressure"
        },
        "settings_alert_dialog_items": {
            "language": "Language:", # Used in SettingsAlertDialog
            "measurement": "Measurement", # Used in SettingsAlertDialog
            "use_current_location": "Use current location:", # Used in SettingsAlertDialog
            "dark_theme": "Dark theme:", # Used in SettingsAlertDialog
            "close": "Close" # Used in SettingsAlertDialog
        },
        "weekly_forecast_items": {
            "monday": "Monday",
            "tuesday": "Tuesday",
            "wednesday": "Wednesday",
            "thursday": "Thursday",
            "friday": "Friday",
            "saturday": "Saturday",
            "sunday": "Sunday",
            "no_forecast_data": "Weather forecast data not available.",
        },
        "temperature_chart_items": {
            "mon": "Mon", # Short day names for charts if needed
            "tue": "Tue",
            "wed": "Wed",
            "thu": "Thu",
            "fri": "Fri",
            "sat": "Sat",
            "sun": "Sun",
            "max": "Max",
            "min": "Min",
            "temperature": "Temperature", # Used for chart titles, labels
        },
        "air_pollution_items": {
            "air_quality_index": "Air Quality Index", # Used in AirQualityIndexCard
            "CO": "Carbon Monoxide",
            "NO": "Nitrogen Monoxide",
            "NO2": "Nitrogen Dioxide",
            "O3": "Ozone",
            "SO2": "Sulphur Dioxide",
            "PM2.5": "Fine Particulate Matter",
            "PM10": "Coarse Particulate Matter",
            "NH3": "Ammonia",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "Current Location",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Air Pollution (μg/m³)", # For AirPollutionChart y-axis title
        },
        "unit_items": {
            "unit_metric": "Metric", # Unit option
            "unit_imperial": "Imperial", # Unit option
            "unit_standard": "Standard", # Unit option
        },  
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "Concentration (µg/m³)", # Y-axis title for AirPollutionChart
        },
    },
    
    "zh_cn": {
        "popup_menu_items": {
            "weather": "天气",
            "map": "地图",
            "settings": "设置"
        },
        "air_condition_items": {
            "air_condition_title": "空气状况",
            "feels_like": "体感温度",
            "humidity": "湿度",
            "wind": "风速",
            "pressure": "气压"
        },
        "settings_alert_dialog_items": {
            "language": "语言：",
            "measurement": "测量单位",
            "use_current_location": "使用当前位置：",
            "dark_theme": "深色主题：",
            "close": "关闭"
        },
        "weekly_forecast_items": {
            "monday": "星期一",
            "tuesday": "星期二",
            "wednesday": "星期三",
            "thursday": "星期四",
            "friday": "星期五",
            "saturday": "星期六",
            "sunday": "星期日",
            "no_forecast_data": "天气预报数据不可用。"
        },
        "temperature_chart_items": {
            "mon": "周一",
            "tue": "周二",
            "wed": "周三",
            "thu": "周四",
            "fri": "周五",
            "sat": "周六",
            "sun": "周日",
            "max": "最大值",
            "min": "最小值",
            "temperature": "温度"
        },
        "air_pollution_items": {
            "air_quality_index": "空气质量指数",
            "CO": "一氧化碳",
            "NO": "一氧化氮",
            "NO2": "二氧化氮",
            "O3": "臭氧",
            "SO2": "二氧化硫",
            "PM2.5": "细颗粒物",
            "PM10": "粗颗粒物",
            "NH3": "氨",
            "aqi_descriptions": [
                "无数据",
                "优",
                "良",
                "中等",
                "差",
                "非常差"
            ]
        },
        "main_information_items": {
            "current_location": "当前位置"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "空气污染 (微克/立方米)"
        },
        "unit_items": {
            "unit_metric": "公制",
            "unit_imperial": "英制",
            "unit_standard": "标准"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "浓度 (微克/立方米)"
        },
        "other": {
            "weather_card_title": "天气详情",
            "settings_title": "设置",
            "loading": "加载中...",
            "search_city": "搜索城市...",
            "filter_options": "筛选选项",
            "select_language": "选择语言",
            "theme_light": "浅色主题",
            "theme_dark": "深色主题",
            "theme_system": "系统主题",
            "language_setting": "语言",
            "measurement_setting": "测量单位",
            "use_current_location_setting": "使用当前位置",
            "dark_theme_setting": "深色主题",
            "close_button": "关闭",
            "aqi_descriptions": [
                "无数据",
                "优",
                "良",
                "中等",
                "差",
                "非常差"
            ]
        }
    },

    "hi": {
        "popup_menu_items": {
            "weather": "मौसम",
            "map": "नक्शा",
            "settings": "सेटिंग्स"
        },
        "air_condition_items": {
            "air_condition_title": "वायु की स्थिति",
            "feels_like": "अनुभूत तापमान",
            "humidity": "नमी",
            "wind": "हवा",
            "pressure": "दबाव"
        },
        "settings_alert_dialog_items": {
            "language": "भाषा:",
            "measurement": "मापन इकाई",
            "use_current_location": "वर्तमान स्थान का उपयोग करें:",
            "dark_theme": "डार्क थीम:",
            "close": "बंद करें"
        },
        "weekly_forecast_items": {
            "monday": "सोमवार",
            "tuesday": "मंगलवार",
            "wednesday": "बुधवार",
            "thursday": "गुरुवार",
            "friday": "शुक्रवार",
            "saturday": "शनिवार",
            "sunday": "रविवार",
            "no_forecast_data": "मौसम पूर्वानुमान डेटा उपलब्ध नहीं है।"
        },
        "temperature_chart_items": {
            "mon": "सोम",
            "tue": "मंगल",
            "wed": "बुध",
            "thu": "गुरु",
            "fri": "शुक्र",
            "sat": "शनि",
            "sun": "रवि",
            "max": "अधिकतम",
            "min": "न्यूनतम",
            "temperature": "तापमान"
        },
        "air_pollution_items": {
            "air_quality_index": "वायु गुणवत्ता सूचकांक",
            "CO": "कार्बन मोनोऑक्साइड",
            "NO": "नाइट्रोजन मोनोऑक्साइड",
            "NO2": "नाइट्रोजन डाइऑक्साइड",
            "O3": "ओजोन",
            "SO2": "सल्फर डाइऑक्साइड",
            "PM2.5": " महीन कण पदार्थ",
            "PM10": "मोटे कण पदार्थ",
            "NH3": "अमोनिया",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "वर्तमान स्थान"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "वायु प्रदूषण (माइक्रोग्राम/घन मीटर)"
        },
        "unit_items": {
            "unit_metric": "मीट्रिक",
            "unit_imperial": "इंपीरियल",
            "unit_standard": "मानक"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "सांद्रता (माइक्रोग्राम/घन मीटर)"
        }
    },
    "es": {
        "popup_menu_items": {
            "weather": "Clima",
            "map": "Mapa",
            "settings": "Configuración"
        },
        "air_condition_items": {
            "air_condition_title": "Condiciones del aire",
            "feels_like": "Sensación térmica",
            "humidity": "Humedad",
            "wind": "Viento",
            "pressure": "Presión"
        },
        "settings_alert_dialog_items": {
            "language": "Idioma:",
            "measurement": "Unidad de medida",
            "use_current_location": "Usar ubicación actual:",
            "dark_theme": "Tema oscuro:",
            "close": "Cerrar"
        },
        "weekly_forecast_items": {
            "monday": "Lunes",
            "tuesday": "Martes",
            "wednesday": "Miércoles",
            "thursday": "Jueves",
            "friday": "Viernes",
            "saturday": "Sábado",
            "sunday": "Domingo",
            "no_forecast_data": "Datos de pronóstico del tiempo no disponibles."
        },
        "temperature_chart_items": {
            "mon": "Lun",
            "tue": "Mar",
            "wed": "Mié",
            "thu": "Jue",
            "fri": "Vie",
            "sat": "Sáb",
            "sun": "Dom",
            "max": "Máx",
            "min": "Mín",
            "temperature": "Temperatura"
        },
        "air_pollution_items": {
            "air_quality_index": "Índice de calidad del aire",
            "CO": "Monóxido de carbono",
            "NO": "Monóxido de nitrógeno",
            "NO2": "Dióxido de nitrógeno",
            "O3": "Ozono",
            "SO2": "Dióxido de azufre",
            "PM2.5": "Partículas finas PM2.5",
            "PM10": "Partículas gruesas PM10",
            "NH3": "Amoníaco",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "Ubicación Actual"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Contaminación del Aire (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Métrico",
            "unit_imperial": "Imperial",
            "unit_standard": "Estándar"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "Concentración (µg/m³)"
        }
    },
    "ar": {
        "popup_menu_items": {
            "weather": "الطقس",
            "map": "الخريطة",
            "settings": "الإعدادات"
        },
        "air_condition_items": {
            "air_condition_title": "حالة الهواء",
            "feels_like": "يشعر وكأنه",
            "humidity": "الرطوبة",
            "wind": "الرياح",
            "pressure": "الضغط"
        },
        "settings_alert_dialog_items": {
            "language": "اللغة:",
            "measurement": "القياس",
            "use_current_location": "استخدام الموقع الحالي:",
            "dark_theme": "الوضع الداكن:",
            "close": "إغلاق"
        },
        "weekly_forecast_items": {
            "monday": "الإثنين",
            "tuesday": "الثلاثاء",
            "wednesday": "الأربعاء",
            "thursday": "الخميس",
            "friday": "الجمعة",
            "saturday": "السبت",
            "sunday": "الأحد",
            "no_forecast_data": "بيانات التوقعات الجوية غير متوفرة."
        },
        "temperature_chart_items": {
            "mon": "الإثنين",
            "tue": "الثلاثاء",
            "wed": "الأربعاء",
            "thu": "الخميس",
            "fri": "الجمعة",
            "sat": "السبت",
            "sun": "الأحد",
            "max": "الحد الأقصى",
            "min": "الحد الأدنى",
            "temperature": "درجة الحرارة"
        },
        "air_pollution_items": {
            "air_quality_index": "إندكس جودة الهواء",
            "CO": "أول أكسيد الكربون",
            "NO": "أول أكسيد النيتروجين",
            "NO2": "ثاني أكسيد النيتروجين",
            "O3": "الأوزون",
            "SO2": "ثاني أكسيد الكبريت",
            "PM2.5": "الجسيمات الدقيقة",
            "PM10": "الجسيمات الخشنة",
            "NH3": "الأمونيا",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "الموقع الحالي"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "تلوث الهواء (ميكروغرام/م³)"
        },
        "unit_items": {
            "unit_metric": "متري",
            "unit_imperial": "إمبراطوري",
            "unit_standard": "قياسي"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "التركيز (ميكروغرام/م³)"
        }
    },
    "id": {
        "popup_menu_items": {
            "weather": "Cuaca",
            "map": "Peta",
            "settings": "Pengaturan"
        },
        "air_condition_items": {
            "air_condition_title": "Kondisi Udara",
            "feels_like": "Terasa seperti",
            "humidity": "Kelembaban",
            "wind": "Angin",
            "pressure": "Tekanan"
        },
        "settings_alert_dialog_items": {
            "language": "Bahasa:",
            "measurement": "Pengukuran",
            "use_current_location": "Gunakan lokasi saat ini:",
            "dark_theme": "Tema gelap:",
            "close": "Tutup"
        },
        "weekly_forecast_items": {
            "monday": "Senin",
            "tuesday": "Selasa",
            "wednesday": "Rabu",
            "thursday": "Kamis",
            "friday": "Jumat",
            "saturday": "Sabtu",
            "sunday": "Minggu",
            "no_forecast_data": "Data prakiraan cuaca tidak tersedia."
        },
        "temperature_chart_items": {
            "mon": "Sen",
            "tue": "Sel",
            "wed": "Rab",
            "thu": "Kam",
            "fri": "Jum",
            "sat": "Sab",
            "sun": "Min",
            "max": "Maks",
            "min": "Min",
            "temperature": "Suhu"
        },
        "air_pollution_items": {
            "air_quality_index": "Indeks Kualitas Udara",
            "CO": "Karbon Monoksida",
            "NO": "Nitrogen Monoksida",
            "NO2": "Nitrogen Dioksida",
            "O3": "Ozon",
            "SO2": "Sulfur Dioksida",
            "PM2.5": "Partikel Halus",
            "PM10": "Partikel Kasar",
            "NH3": "Amonia",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "Lokasi Saat Ini"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Polusi Udara (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Metrik",
            "unit_imperial": "Imperial",
            "unit_standard": "Standar"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "Konsentrasi (μg/m³)"
        }
    },
    "ja": {
        "popup_menu_items": {
            "weather": "天気",
            "map": "地図",
            "settings": "設定"
        },
        "air_condition_items": {
            "air_condition_title": "空気の状態",
            "feels_like": "体感温度",
            "humidity": "湿度",
            "wind": "風",
            "pressure": "気圧"
        },
        "settings_alert_dialog_items": {
            "language": "言語:",
            "measurement": "測定",
            "use_current_location": "現在地を使用:",
            "dark_theme": "ダークテーマ:",
            "close": "閉じる"
        },
        "weekly_forecast_items": {
            "monday": "月曜日",
            "tuesday": "火曜日",
            "wednesday": "水曜日",
            "thursday": "木曜日",
            "friday": "金曜日",
            "saturday": "土曜日",
            "sunday": "日曜日",
            "no_forecast_data": "天気予報データがありません。"
        },
        "temperature_chart_items": {
            "mon": "月",
            "tue": "火",
            "wed": "水",
            "thu": "木",
            "fri": "金",
            "sat": "土",
            "sun": "日",
            "max": "最大",
            "min": "最小",
            "temperature": "気温"
        },
        "air_pollution_items": {
            "air_quality_index": "大気質指数",
            "CO": "一酸化炭素",
            "NO": "一酸化窒素",
            "NO2": "二酸化窒素",
            "O3": "オゾン",
            "SO2": "二酸化硫黄",
            "PM2.5": "微小粒子状物質 PM2.5",
            "PM10": "粗大粒子状物質 PM10",
            "NH3": "アンモニア",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "現在地"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "大気汚染 (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "メートル法",
            "unit_imperial": "ヤード・ポンド法",
            "unit_standard": "標準"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "濃度 (µg/m³)"
        }
    },
    "it": {
        "popup_menu_items": {
            "weather": "Meteo",
            "map": "Mappa",
            "settings": "Impostazioni"
        },
        "air_condition_items": {
            "air_condition_title": "Condizioni dell'aria",
            "feels_like": "Percepito",
            "humidity": "Umidità",
            "wind": "Vento",
            "pressure": "Pressione"
        },
        "settings_alert_dialog_items": {
            "language": "Lingua:",
            "measurement": "Misurazione",
            "use_current_location": "Usa posizione corrente:",
            "dark_theme": "Tema scuro:",
            "close": "Chiudi"
        },
        "weekly_forecast_items": {
            "monday": "Lunedì",
            "tuesday": "Martedì",
            "wednesday": "Mercoledì",
            "thursday": "Giovedì",
            "friday": "Venerdì",
            "saturday": "Sabato",
            "sunday": "Domenica",
            "no_forecast_data": "Dati previsione meteo non disponibili."
        },
        "temperature_chart_items": {
            "mon": "Lun",
            "tue": "Mar",
            "wed": "Mer",
            "thu": "Gio",
            "fri": "Ven",
            "sat": "Sab",
            "sun": "Dom",
            "max": "Max",
            "min": "Min",
            "temperature": "Temperatura"
        },
        "air_pollution_items": {
            "air_quality_index": "Indice di qualità dell'aria",
            "CO": "Monossido di carbonio",
            "NO": "Monossido di azoto",
            "NO2": "Biossido di azoto",
            "O3": "Ozono",
            "SO2": "Biossido di zolfo",
            "PM2.5": "Particolato fine PM2.5",
            "PM10": "Particolato grossolano PM10",
            "NH3": "Ammoniaca",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "Posizione Corrente"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Inquinamento dell'aria (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Metrico",
            "unit_imperial": "Imperiale",
            "unit_standard": "Standard"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "Concentrazione (µg/m³)"
        }
    },
    "de": {
        "popup_menu_items": {
            "weather": "Wetter",
            "map": "Karte",
            "settings": "Einstellungen"
        },
        "air_condition_items": {
            "air_condition_title": "Luftbedingungen",
            "feels_like": "Gefühlt",
            "humidity": "Luftfeuchtigkeit",
            "wind": "Wind",
            "pressure": "Druck"
        },
        "settings_alert_dialog_items": {
            "language": "Sprache:",
            "measurement": "Messung",
            "use_current_location": "Aktuellen Standort verwenden:",
            "dark_theme": "Dunkles Thema:",
            "close": "Schließen"
        },
        "weekly_forecast_items": {
            "monday": "Montag",
            "tuesday": "Dienstag",
            "wednesday": "Mittwoch",
            "thursday": "Donnerstag",
            "friday": "Freitag",
            "saturday": "Samstag",
            "sunday": "Sonntag",
            "no_forecast_data": "Wettervorhersagedaten nicht verfügbar."
        },
        "temperature_chart_items": {
            "mon": "Mo",
            "tue": "Di",
            "wed": "Mi",
            "thu": "Do",
            "fri": "Fr",
            "sat": "Sa",
            "sun": "So",
            "max": "Max",
            "min": "Min",
            "temperature": "Temperatur"
        },
        "air_pollution_items": {
            "air_quality_index": "Luftqualitätsindex",
            "CO": "Kohlenmonoxid",
            "NO": "Stickstoffmonoxid",
            "NO2": "Stickstoffdioxid",
            "O3": "Ozon",
            "SO2": "Schwefeldioxid",
            "PM2.5": "Feinstaub PM2.5",
            "PM10": "Grobstaub PM10",
            "NH3": "Ammoniak",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "Aktueller Standort"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Luftverschmutzung (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Metrisch",
            "unit_imperial": "Imperial",
            "unit_standard": "Standard"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "Konzentration (µg/m³)"
        }
    },
    "fr": {
        "popup_menu_items": {
            "weather": "Météo",
            "map": "Carte",
            "settings": "Paramètres"
        },
        "air_condition_items": {
            "air_condition_title": "Conditions de l'air",
            "feels_like": "Ressenti",
            "humidity": "Humidité",
            "wind": "Vent",
            "pressure": "Pression"
        },
        "settings_alert_dialog_items": {
            "language": "Langue:",
            "measurement": "Mesure",
            "use_current_location": "Utiliser la position actuelle:",
            "dark_theme": "Thème sombre:",
            "close": "Fermer"
        },
        "weekly_forecast_items": {
            "monday": "Lundi",
            "tuesday": "Mardi",
            "wednesday": "Mercredi",
            "thursday": "Jeudi",
            "friday": "Vendredi",
            "saturday": "Samedi",
            "sunday": "Dimanche",
            "no_forecast_data": "Données de prévision météo non disponibles."
        },
        "temperature_chart_items": {
            "mon": "Lun",
            "tue": "Mar",
            "wed": "Mer",
            "thu": "Jeu",
            "fri": "Ven",
            "sat": "Sam",
            "sun": "Dim",
            "max": "Max",
            "min": "Min",
            "temperature": "Température"
        },
        "air_pollution_items": {
            "air_quality_index": "Qualité de l'air",
            "CO": "Monoxyde de carbone",
            "NO": "Monoxyde d'azote",
            "NO2": "Dioxyde d'azote",
            "O3": "Ozone",
            "SO2": "Dioxyde de soufre",
            "PM2.5": "Particules fines PM2.5",
            "PM10": "Particules grossières PM10",
            "NH3": "Ammoniac",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "Position actuelle"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Pollution de l'air (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Métrique",
            "unit_imperial": "Impérial",
            "unit_standard": "Standard"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "Concentration (µg/m³)"
        }
    },
    "pt": {
        "popup_menu_items": {
            "weather": "Tempo",
            "map": "Mapa",
            "settings": "Configurações"
        },
        "air_condition_items": {
            "air_condition_title": "Condições do ar",
            "feels_like": "Sensação térmica",
            "humidity": "Umidade",
            "wind": "Vento",
            "pressure": "Pressão"
        },
        "settings_alert_dialog_items": {
            "language": "Idioma:",
            "measurement": "Medição",
            "use_current_location": "Usar localização atual:",
            "dark_theme": "Tema escuro:",
            "close": "Fechar"
        },
        "weekly_forecast_items": {
            "monday": "Segunda-feira",
            "tuesday": "Terça-feira",
            "wednesday": "Quarta-feira",
            "thursday": "Quinta-feira",
            "friday": "Sexta-feira",
            "saturday": "Sábado",
            "sunday": "Domingo",
            "no_forecast_data": "Dados de previsão do tempo não disponíveis."
        },
        "temperature_chart_items": {
            "mon": "Seg",
            "tue": "Ter",
            "wed": "Qua",
            "thu": "Qui",
            "fri": "Sex",
            "sat": "Sáb",
            "sun": "Dom",
            "max": "Máx",
            "min": "Mín",
            "temperature": "Temperatura"
        },
        "air_pollution_items": {
            "air_quality_index": "Índice de qualidade do ar",
            "CO": "Monóxido de carbono",
            "NO": "Monóxido de nitrogênio",
            "NO2": "Dióxido de nitrogênio",
            "O3": "Ozônio",
            "SO2": "Dióxido de enxofre",
            "PM2.5": "Material particulado fino PM2.5",
            "PM10": "Material particulado grosso PM10",
            "NH3": "Amônia",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "Localização Atual"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Poluição do Ar (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Métrico",
            "unit_imperial": "Imperial",
            "unit_standard": "Padrão"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "Concentração (µg/m³)"
        }
    },
    "ru": {
        "popup_menu_items": {
            "weather": "Погода",
            "map": "Карта",
            "settings": "Настройки"
        },
        "air_condition_items": {
            "air_condition_title": "Состояние воздуха",
            "feels_like": "Ощущается как",
            "humidity": "Влажность",
            "wind": "Ветер",
            "pressure": "Давление"
        },
        "settings_alert_dialog_items": {
            "language": "Язык:",
            "measurement": "Измерение",
            "use_current_location": "Использовать текущее местоположение:",
            "dark_theme": "Темная тема:",
            "close": "Закрыть"
        },
        "weekly_forecast_items": {
            "monday": "Понедельник",
            "tuesday": "Вторник",
            "wednesday": "Среда",
            "thursday": "Четверг",
            "friday": "Пятница",
            "saturday": "Суббота",
            "sunday": "Воскресенье",
            "no_forecast_data": "Данные о прогнозе погоды недоступны."
        },
        "temperature_chart_items": {
            "mon": "Пн",
            "tue": "Вт",
            "wed": "Ср",
            "thu": "Чт",
            "fri": "Пт",
            "sat": "Сб",
            "sun": "Вс",
            "max": "Макс",
            "min": "Мин",
            "temperature": "Температура"
        },
        "air_pollution_items": {
            "air_quality_index": "Индекс качества воздуха",
            "CO": "Угарный газ",
            "NO": "Оксид азота",
            "NO2": "Диоксид азота",
            "O3": "Озон",
            "SO2": "Диоксид серы",
            "PM2.5": "Мелкие твердые частицы PM2.5",
            "PM10": "Крупные твердые частицы PM10",
            "NH3": "Аммиак",
            "aqi_descriptions": [
                "N/A",
                "Good",
                "Fair",
                "Moderate",
                "Poor",
                "Very Poor"
            ]
        },
        "main_information_items": {
            "current_location": "Текущее местоположение"
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Загрязнение воздуха (μг/м³)"
        },
        "unit_items": {
            "unit_metric": "Метрическая",
            "unit_imperial": "Имперская",
            "unit_standard": "Стандартная"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "Концентрация (мкг/м³)"
        }
    }
}