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
            "settings_alert_dialog_title": "Settings",
            "language": "Language:", # Used in SettingsAlertDialog
            "measurement": "Measurement", # Used in SettingsAlertDialog
            "use_current_location": "Use current location:", # Used in SettingsAlertDialog
            "dark_theme": "Dark theme:", # Used in SettingsAlertDialog
            "close": "Close" # Used in SettingsAlertDialog
        },
        "weekly_forecast_items": {
            "header": "5-Day Forecast",
            "loading": "Loading weekly forecast...",
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
            "monday": "Mon", # Short day names for charts if needed
            "tuesday": "Tue",
            "wednesday": "Wed",
            "thursday": "Thu",
            "friday": "Fri",
            "saturday": "Sat",
            "sunday": "Sun",
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
            "high": "High",
            "low": "Low",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "Hourly Forecast",
            "loading_forecast": "Loading 24-hour forecast...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Air Pollution (μg/m³)", # For AirPollutionChart y-axis title
        },        "unit_items": {
            "unit_metric": "Metric", # Unit option
            "unit_imperial": "Imperial", # Unit option
            "unit_standard": "Standard", # Unit option
            "measurement": "Measurement", # Used in settings dialog
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "µg/m³", # Y-axis title for AirPollutionChart
            "micrograms_per_cubic_meter_short": "µg/m³",
            "no_air_pollution_data": "No air pollution data available",
            "air_pollution_title": "Air Pollution", # Header title
            # Pollutant names for tooltips
            "co_name": "Carbon Monoxide",
            "no_name": "Nitrogen Monoxide", 
            "no2_name": "Nitrogen Dioxide",
            "o3_name": "Ozone",
            "so2_name": "Sulfur Dioxide",
            "pm2_5_name": "PM2.5 Particles",
            "pm10_name": "PM10 Particles",
            "nh3_name": "Ammonia",
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
            "settings_alert_dialog_title": "设置",
            "language": "语言：",
            "measurement": "测量单位",
            "use_current_location": "使用当前位置：",
            "dark_theme": "深色主题：",
            "close": "关闭"
        },
        "weekly_forecast_items": {
            "header": "5天预报",
            "loading": "加载每周预报...",
            "monday": "星期一",
            "tuesday": "星期二",
            "wednesday": "星期三",
            "thursday": "星期四",
            "friday": "星期五",
            "saturday": "星期六",
            "sunday": "星期日",
            "no_forecast_data": "天气预报数据不可用。"
        },        "temperature_chart_items": {
            "monday": "周一",
            "tuesday": "周二",
            "wednesday": "周三",
            "thursday": "周四",
            "friday": "周五",
            "saturday": "周六",
            "sunday": "周日",
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
            "current_location": "当前位置",
            "high": "最高",
            "low": "最低",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "每小时预报",
            "loading_forecast": "正在加载24小时预报...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "空气污染 (微克/立方米)"
        },        "unit_items": {
            "unit_metric": "公制",
            "unit_imperial": "英制",
            "unit_standard": "标准",
            "measurement": "测量单位"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "微克/立方米",
            "micrograms_per_cubic_meter_short": "微克/立方米",
            "no_air_pollution_data": "无空气污染数据",
            "air_pollution_title": "空气污染", # Header title
            "air_pollution": "空气污染", # Header title
            # Pollutant names for tooltips
            "co_name": "一氧化碳",
            "no_name": "一氧化氮", 
            "no2_name": "二氧化氮",
            "o3_name": "臭氧",
            "so2_name": "二氧化硫",
            "pm2_5_name": "PM2.5颗粒",
            "pm10_name": "PM10颗粒",
            "nh3_name": "氨气",
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
            "settings_alert_dialog_title": "सेटिंग्स",
            "language": "भाषा:",
            "measurement": "मापन इकाई",
            "use_current_location": "वर्तमान स्थान का उपयोग करें:",
            "dark_theme": "डार्क थीम:",
            "close": "बंद करें"
        },
        "weekly_forecast_items": {
            "header": "5 दिन का पूर्वानुमान",
            "loading": "साप्ताहिक पूर्वानुमान लोड हो रहा है...",
            "monday": "सोमवार",
            "tuesday": "मंगलवार",
            "wednesday": "बुधवार",
            "thursday": "गुरुवार",
            "friday": "शुक्रवार",
            "saturday": "शनिवार",
            "sunday": "रविवार",
            "no_forecast_data": "मौसम पूर्वानुमान डेटा उपलब्ध नहीं है।"
        },        "temperature_chart_items": {
            "monday": "सोम",
            "tuesday": "मंगल",
            "wednesday": "बुध",
            "thursday": "गुरु",
            "friday": "शुक्र",
            "saturday": "शनि",
            "sunday": "रवि",
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
                "उपलब्ध नहीं",
                "अच्छा",
                "संतोषजनक",
                "मध्यम",
                "खराब",
                "बहुत खराब"
            ]
        },
        "main_information_items": {
            "current_location": "वर्तमान स्थान",
            "high": "उच्च",
            "low": "निम्न",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "प्रति घंटा पूर्वानुमान",
            "loading_forecast": "24-घंटे का पूर्वानुमान लोड हो रहा है...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "वायु प्रदूषण (माइक्रोग्राम/घन मीटर)"
        },
        "unit_items": {
            "unit_metric": "मीट्रिक",
            "unit_imperial": "इंपीरियल",
            "unit_standard": "मानक",
            "measurement": "मापन इकाई"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "माइक्रोग्राम/घन मीटर",
            "micrograms_per_cubic_meter_short": "माइक्रोग्राम/घन मीटर",
            "no_air_pollution_data": "वायु प्रदूषण डेटा उपलब्ध नहीं है",
            "air_pollution_title": "वायु प्रदूषण", # Header title
            "air_pollution": "वायु प्रदूषण", # Header title
            # Pollutant names for tooltips
            "co_name": "कार्बन मोनोऑक्साइड",
            "no_name": "नाइट्रिक ऑक्साइड", 
            "no2_name": "नाइट्रोजन डाइऑक्साइड",
            "o3_name": "ओजोन",
            "so2_name": "सल्फर डाइऑक्साइड",
            "pm2_5_name": "PM2.5 कण",
            "pm10_name": "PM10 कण",
            "nh3_name": "अमोनिया",
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
            "settings_alert_dialog_title": "Configuración",
            "language": "Idioma:",
            "measurement": "Unidad de medida",
            "use_current_location": "Usar ubicación actual:",
            "dark_theme": "Tema oscuro:",
            "close": "Cerrar"
        },
        "weekly_forecast_items": {
            "header": "Pronóstico 5 Días",
            "loading": "Cargando pronóstico semanal...",
            "monday": "Lunes",
            "tuesday": "Martes",
            "wednesday": "Miércoles",
            "thursday": "Jueves",
            "friday": "Viernes",
            "saturday": "Sábado",
            "sunday": "Domingo",
            "no_forecast_data": "Datos de pronóstico del tiempo no disponibles."
        },        "temperature_chart_items": {
            "monday": "Lun",
            "tuesday": "Mar",
            "wednesday": "Mié",
            "thursday": "Jue",
            "friday": "Vie",
            "saturday": "Sáb",
            "sunday": "Dom",
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
                "N/D",
                "Buena",
                "Aceptable",
                "Moderada",
                "Mala",
                "Muy mala"
            ]
        },
        "main_information_items": {
            "current_location": "Ubicación Actual",
            "high": "Alta",
            "low": "Baja",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "Pronóstico por Horas",
            "loading_forecast": "Cargando pronóstico de 24 horas...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Contaminación del Aire (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Métrico",
            "unit_imperial": "Imperial",
            "unit_standard": "Estándar",
            "measurement": "Medición"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "µg/m³",
            "micrograms_per_cubic_meter_short": "µg/m³",
            "no_air_pollution_data": "No hay datos de contaminación del aire disponibles",
            "air_pollution_title": "Contaminación del Aire", # Header title
            "air_pollution": "Contaminación del Aire", # Header title
            # Pollutant names for tooltips
            "co_name": "Monóxido de Carbono",
            "no_name": "Óxido Nítrico", 
            "no2_name": "Dióxido de Nitrógeno",
            "o3_name": "Ozono",
            "so2_name": "Dióxido de Azufre",
            "pm2_5_name": "Partículas PM2.5",
            "pm10_name": "Partículas PM10",
            "nh3_name": "Amoníaco",
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
            "settings_alert_dialog_title": "الإعدادات",
            "language": "اللغة:",
            "measurement": "القياس",
            "use_current_location": "استخدام الموقع الحالي:",
            "dark_theme": "الوضع الداكن:",
            "close": "إغلاق"
        },
        "weekly_forecast_items": {
            "header": "توقعات 5 أيام",
            "loading": "تحميل التوقعات الأسبوعية...",
            "monday": "الإثنين",
            "tuesday": "الثلاثاء",
            "wednesday": "الأربعاء",
            "thursday": "الخميس",
            "friday": "الجمعة",
            "saturday": "السبت",
            "sunday": "الأحد",
            "no_forecast_data": "بيانات التوقعات الجوية غير متوفرة."
        },        "temperature_chart_items": {
            "monday": "الإثنين",
            "tuesday": "الثلاثاء",
            "wednesday": "الأربعاء",
            "thursday": "الخميس",
            "friday": "الجمعة",
            "saturday": "السبت",
            "sunday": "الأحد",
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
                "غير متوفر",
                "جيد",
                "عادل",
                "معتدل",
                "سيء",
                "سيء جدا"
            ]
        },
        "main_information_items": {
            "current_location": "الموقع الحالي",
            "high": "مرتفع",
            "low": "منخفض",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "التوقعات بالساعة",
            "loading_forecast": "جارٍ تحميل توقعات الـ 24 ساعة...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "تلوث الهواء (ميكروغرام/م³)"
        },
        "unit_items": {
            "unit_metric": "متري",
            "unit_imperial": "إمبراطوري",
            "unit_standard": "قياسي",
            "measurement": "القياس"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "ميكروغرام/م³",
            "micrograms_per_cubic_meter_short": "ميكروغرام/م³",
            "no_air_pollution_data": "لا توجد بيانات تلوث الهواء متاحة",
            "air_pollution": "تلوث الهواء", # Header title
            # Pollutant names for tooltips
            "co_name": "أول أكسيد الكربون",
            "no_name": "أول أكسيد النيتروجين", 
            "no2_name": "ثاني أكسيد النيتروجين",
            "o3_name": "الأوزون",
            "so2_name": "ثاني أكسيد الكبريت",
            "pm2_5_name": "جسيمات PM2.5",
            "pm10_name": "جسيمات PM10",
            "nh3_name": "الأمونيا",
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
            "settings_alert_dialog_title": "Pengaturan",
            "language": "Bahasa:",
            "measurement": "Pengukuran",
            "use_current_location": "Gunakan lokasi saat ini:",
            "dark_theme": "Tema gelap:",
            "close": "Tutup"
        },
        "weekly_forecast_items": {
            "header": "Prakiraan 5 Hari",
            "loading": "Memuat prakiraan mingguan...",
            "monday": "Senin",
            "tuesday": "Selasa",
            "wednesday": "Rabu",
            "thursday": "Kamis",
            "friday": "Jumat",
            "saturday": "Sabtu",
            "sunday": "Minggu",
            "no_forecast_data": "Data prakiraan cuaca tidak tersedia."
        },        "temperature_chart_items": {
            "monday": "Sen",
            "tuesday": "Sel",
            "wednesday": "Rab",
            "thursday": "Kam",
            "friday": "Jum",
            "saturday": "Sab",
            "sunday": "Min",
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
                "T/A",
                "Baik",
                "Cukup",
                "Sedang",
                "Buruk",
                "Sangat Buruk"
            ]
        },
        "main_information_items": {
            "current_location": "Lokasi Saat Ini",
            "high": "Tinggi",
            "low": "Rendah",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "Prakiraan Per Jam",
            "loading_forecast": "Memuat prakiraan 24 jam...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Polusi Udara (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Metrik",
            "unit_imperial": "Imperial",
            "unit_standard": "Standar",
            "measurement": "Pengukuran"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "μg/m³",
            "micrograms_per_cubic_meter_short": "μg/m³",
            "no_air_pollution_data": "Data polusi udara tidak tersedia",
            "air_pollution": "Polusi Udara", # Header title
            # Pollutant names for tooltips
            "co_name": "Karbon Monoksida",
            "no_name": "Nitrogen Monoksida", 
            "no2_name": "Nitrogen Dioksida",
            "o3_name": "Ozon",
            "so2_name": "Sulfur Dioksida",
            "pm2_5_name": "Partikel PM2.5",
            "pm10_name": "Partikel PM10",
            "nh3_name": "Amonia",
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
            "settings_alert_dialog_title": "設定",
            "language": "言語:",
            "measurement": "測定",
            "use_current_location": "現在地を使用:",
            "dark_theme": "ダークテーマ:",
            "close": "閉じる"
        },
        "weekly_forecast_items": {
            "header": "5日間予報",
            "loading": "週間予報を読み込み中...",
            "monday": "月曜日",
            "tuesday": "火曜日",
            "wednesday": "水曜日",
            "thursday": "木曜日",
            "friday": "金曜日",
            "saturday": "土曜日",
            "sunday": "日曜日",
            "no_forecast_data": "天気予報データがありません。"
        },        "temperature_chart_items": {
            "monday": "月",
            "tuesday": "火",
            "wednesday": "水",
            "thursday": "木",
            "friday": "金",
            "saturday": "土",
            "sunday": "日",
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
                "該当なし",
                "良好",
                "まあまあ",
                "普通",
                "悪い",
                "非常に悪い"
            ]
        },
        "main_information_items": {
            "current_location": "現在地",
            "high": "最高",
            "low": "最低",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "時間別予報",
            "loading_forecast": "24時間予報を読み込んでいます...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "大気汚染 (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "メートル法",
            "unit_imperial": "ヤード・ポンド法",
            "unit_standard": "標準",
            "measurement": "測定"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "µg/m³",
            "micrograms_per_cubic_meter_short": "µg/m³",
            "no_air_pollution_data": "大気汚染データが利用できません",
            "air_pollution": "大気汚染", # Header title
            # Pollutant names for tooltips
            "co_name": "一酸化炭素",
            "no_name": "一酸化窒素", 
            "no2_name": "二酸化窒素",
            "o3_name": "オゾン",
            "so2_name": "二酸化硫黄",
            "pm2_5_name": "PM2.5粒子",
            "pm10_name": "PM10粒子",
            "nh3_name": "アンモニア",
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
            "settings_alert_dialog_title": "Impostazioni",
            "language": "Lingua:",
            "measurement": "Misurazione",
            "use_current_location": "Usa posizione corrente:",
            "dark_theme": "Tema scuro:",
            "close": "Chiudi"
        },
        "weekly_forecast_items": {
            "header": "Previsioni 5 Giorni",
            "loading": "Caricamento previsioni settimanali...",
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
            "monday": "Lun",
            "tuesday": "Mar",
            "wednesday": "Mer",
            "thursday": "Gio",
            "friday": "Ven",
            "saturday": "Sab",
            "sunday": "Dom",
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
                "N/D",
                "Buona",
                "Discreta",
                "Moderata",
                "Scarsa",
                "Molto Scarsa"
            ]
        },
        "main_information_items": {
            "current_location": "Posizione Corrente",
            "high": "Massima",
            "low": "Minima",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "Previsioni Orarie",
            "loading_forecast": "Caricamento previsioni 24 ore...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Inquinamento dell'aria (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Metrico",
            "unit_imperial": "Imperiale",
            "unit_standard": "Standard",
            "measurement": "Misurazione"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "µg/m³",
            "micrograms_per_cubic_meter_short": "µg/m³",
            "no_air_pollution_data": "Dati sull'inquinamento atmosferico non disponibili",
            "air_pollution_title": "Inquinamento dell'Aria", # Header title
            "air_pollution": "Inquinamento dell'Aria", # Header title
            # Pollutant names for tooltips
            "co_name": "Monossido di Carbonio",
            "no_name": "Monossido di Azoto", 
            "no2_name": "Biossido di Azoto",
            "o3_name": "Ozono",
            "so2_name": "Biossido di Zolfo",
            "pm2_5_name": "Particelle PM2.5",
            "pm10_name": "Particelle PM10",
            "nh3_name": "Ammoniaca",
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
            "settings_alert_dialog_title": "Einstellungen",
            "language": "Sprache:",
            "measurement": "Messung",
            "use_current_location": "Aktuellen Standort verwenden:",
            "dark_theme": "Dunkles Thema:",
            "close": "Schließen"
        },
        "weekly_forecast_items": {
            "header": "5-Tage-Prognose",
            "loading": "Laden der Wochenprognose...",
            "monday": "Montag",
            "tuesday": "Dienstag",
            "wednesday": "Mittwoch",
            "thursday": "Donnerstag",
            "friday": "Freitag",
            "saturday": "Samstag",
            "sunday": "Sonntag",
            "no_forecast_data": "Wettervorhersagedaten nicht verfügbar."
        },        "temperature_chart_items": {
            "monday": "Mo",
            "tuesday": "Di",
            "wednesday": "Mi",
            "thursday": "Do",
            "friday": "Fr",
            "saturday": "Sa",
            "sunday": "So",
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
                "N/V",
                "Gut",
                "Befriedigend",
                "Mäßig",
                "Schlecht",
                "Sehr schlecht"
            ]
        },
        "main_information_items": {
            "current_location": "Aktueller Standort",
            "high": "Hoch",
            "low": "Niedrig",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "Stündliche Vorhersage",
            "loading_forecast": "Lade 24-Stunden-Vorhersage...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Luftverschmutzung (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Metrisch",
            "unit_imperial": "Imperial",
            "unit_standard": "Standard",
            "measurement": "Messung"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "µg/m³",
            "micrograms_per_cubic_meter_short": "µg/m³",
            "no_air_pollution_data": "Keine Luftverschmutzungsdaten verfügbar",
            "air_pollution": "Luftverschmutzung", # Header title
            # Pollutant names for tooltips
            "co_name": "Kohlenmonoxid",
            "no_name": "Stickstoffmonoxid", 
            "no2_name": "Stickstoffdioxid",
            "o3_name": "Ozon",
            "so2_name": "Schwefeldioxid",
            "pm2_5_name": "PM2.5-Partikel",
            "pm10_name": "PM10-Partikel",
            "nh3_name": "Ammoniak",
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
            "settings_alert_dialog_title": "Paramètres",
            "language": "Langue:",
            "measurement": "Mesure",
            "use_current_location": "Utiliser la position actuelle:",
            "dark_theme": "Thème sombre:",
            "close": "Fermer"
        },
        "weekly_forecast_items": {
            "header": "Prévisions 5 Jours",
            "loading": "Chargement des prévisions hebdomadaires...",
            "monday": "Lundi",
            "tuesday": "Mardi",
            "wednesday": "Mercredi",
            "thursday": "Jeudi",
            "friday": "Vendredi",
            "saturday": "Samedi",
            "sunday": "Dimanche",
            "no_forecast_data": "Données de prévision météo non disponibles."
        },        "temperature_chart_items": {
            "monday": "Lun",
            "tuesday": "Mar",
            "wednesday": "Mer",
            "thursday": "Jeu",
            "friday": "Ven",
            "saturday": "Sam",
            "sunday": "Dim",
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
                "N/D",
                "Bon",
                "Assez bon",
                "Modéré",
                "Mauvais",
                "Très mauvais"
            ]
        },
        "main_information_items": {
            "current_location": "Position actuelle",
            "high": "Haute",
            "low": "Basse",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "Prévisions Horaires",
            "loading_forecast": "Chargement des prévisions 24h...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Pollution de l'air (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Métrique",
            "unit_imperial": "Impérial",
            "unit_standard": "Standard",
            "measurement": "Mesure"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "µg/m³",
            "micrograms_per_cubic_meter_short": "µg/m³",
            "no_air_pollution_data": "Aucune donnée de pollution de l'air disponible",
            "air_pollution": "Pollution de l'Air", # Header title
            # Pollutant names for tooltips
            "co_name": "Monoxyde de Carbone",
            "no_name": "Monoxyde d'Azote", 
            "no2_name": "Dioxyde d'Azote",
            "o3_name": "Ozone",
            "so2_name": "Dioxyde de Soufre",
            "pm2_5_name": "Particules PM2.5",
            "pm10_name": "Particules PM10",
            "nh3_name": "Ammoniac",
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
            "settings_alert_dialog_title": "Configurações",
            "language": "Idioma:",
            "measurement": "Medição",
            "use_current_location": "Usar localização atual:",
            "dark_theme": "Tema escuro:",
            "close": "Fechar"
        },
        "weekly_forecast_items": {
            "header": "Previsão 5 Dias",
            "loading": "Carregando previsão semanal...",
            "monday": "Segunda-feira",
            "tuesday": "Terça-feira",
            "wednesday": "Quarta-feira",
            "thursday": "Quinta-feira",
            "friday": "Sexta-feira",
            "saturday": "Sábado",
            "sunday": "Domingo",
            "no_forecast_data": "Dados de previsão do tempo não disponíveis."
        },        "temperature_chart_items": {
            "monday": "Seg",
            "tuesday": "Ter",
            "wednesday": "Qua",
            "thursday": "Qui",
            "friday": "Sex",
            "saturday": "Sáb",
            "sunday": "Dom",
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
                "N/D",
                "Bom",
                "Razoável",
                "Moderado",
                "Ruim",
                "Muito Ruim"
            ]
        },
        "main_information_items": {
            "current_location": "Localização Atual",
            "high": "Alta",
            "low": "Baixa",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "Previsão Horária",
            "loading_forecast": "Carregando previsão de 24 horas...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Poluição do Ar (μg/m³)"
        },
        "unit_items": {
            "unit_metric": "Métrico",
            "unit_imperial": "Imperial",
            "unit_standard": "Padrão",
            "measurement": "Medição"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "µg/m³",
            "micrograms_per_cubic_meter_short": "µg/m³",
            "no_air_pollution_data": "Nenhum dado de poluição do ar disponível",
            "air_pollution": "Poluição do Ar", # Header title
            # Pollutant names for tooltips
            "co_name": "Monóxido de Carbono",
            "no_name": "Monóxido de Nitrogênio", 
            "no2_name": "Dióxido de Nitrogênio",
            "o3_name": "Ozônio",
            "so2_name": "Dióxido de Enxofre",
            "pm2_5_name": "Partículas PM2.5",
            "pm10_name": "Partículas PM10",
            "nh3_name": "Amônia",
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
            "settings_alert_dialog_title": "Настройки",
            "language": "Язык:",
            "measurement": "Измерение",
            "use_current_location": "Использовать текущее местоположение:",
            "dark_theme": "Темная тема:",
            "close": "Закрыть"
        },
        "weekly_forecast_items": {
            "header": "Прогноз на 5 дней",
            "loading": "Загрузка недельного прогноза...",
            "monday": "Понедельник",
            "tuesday": "Вторник",
            "wednesday": "Среда",
            "thursday": "Четверг",
            "friday": "Пятница",
            "saturday": "Суббота",
            "sunday": "Воскресенье",
            "no_forecast_data": "Данные о прогнозе погоды недоступны."
        },        "temperature_chart_items": {
            "monday": "Пн",
            "tuesday": "Вт",
            "wednesday": "Ср",
            "thursday": "Чт",
            "friday": "Пт",
            "saturday": "Сб",
            "sunday": "Вс",
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
                "Н/Д",
                "Хороший",
                "Приемлемый",
                "Умеренный",
                "Плохой",
                "Очень плохой"
            ]
        },
        "main_information_items": {
            "current_location": "Текущее местоположение",
            "high": "Высокая",
            "low": "Низкая",
        },
        "hourly_forecast_items": {
            "hourly_forecast": "Почасовой прогноз",
            "loading_forecast": "Загрузка 24-часового прогноза...",
        },
        "air_pollution_chart_title_items": {
            "air_pollution_chart_title": "Загрязнение воздуха (μг/м³)"
        },        "unit_items": {
            "unit_metric": "Метрическая",
            "unit_imperial": "Имперская",
            "unit_standard": "Стандартная",
            "measurement": "Измерение"
        },
        "air_pollution_chart_items": {
            "air_pollution_chart_y_axis_title": "мкг/м³",
            "micrograms_per_cubic_meter_short": "мкг/м³",
            "no_air_pollution_data": "Данные о загрязнении воздуха недоступны",
            "air_pollution": "Загрязнение Воздуха", # Header title
            # Pollutant names for tooltips
            "co_name": "Монооксид Углерода",
            "no_name": "Монооксид Азота", 
            "no2_name": "Диоксид Азота",
            "o3_name": "Озон",
            "so2_name": "Диоксид Серы",
            "pm2_5_name": "Частицы PM2.5",
            "pm10_name": "Частицы PM10",
            "nh3_name": "Аммиак",
        }
    }
}