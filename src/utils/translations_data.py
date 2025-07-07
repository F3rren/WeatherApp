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
            "wind_direction": "Direction",
            "wind_gust": "Wind Gust",
            "pressure": "Pressure",
            "visibility": "Visibility",
            "uv_index": "UV Index",
            "dew_point": "Dew Point",
            "cloud_coverage": "Cloud Coverage",
            "temperature_group": "Temperature",
            "humidity_air_group": "Humidity & Air",
            "wind_group": "Wind",
            "atmospheric_group": "Atmospheric",
            "solar_group": "Solar"
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
        "precipitation_chart_items": {
            "precipitation_chart_title": "Precipitation Forecast",
            "precipitation_mm": "Precipitation (mm)",
            "probability_percent": "Probability (%)",
            "no_data": "No precipitation data available",
            "loading": "Loading precipitation data...",
            "time_hours": "Time (Hours)",
            "total_precipitation": "Total",
            "max_intensity": "Peak",
            "rainy_hours": "Rainy hours",
            # Precipitation intensity descriptions
            "intensity_light": "Light",
            "intensity_moderate": "Moderate", 
            "intensity_heavy": "Heavy",
            "intensity_very_heavy": "Very heavy",
            # Additional labels
            "next_24h": "Next 24 hours",
            "precipitation_type": "Type",
            "rain": "Rain",
            "snow": "Snow",
            "mixed": "Mixed",
            "probability": "Probability",
            "when_expected": "Expected at",
            "duration": "Duration",
            "peak_time": "Peak expected"
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
            "wind_direction": "风向",
            "wind_gust": "阵风",
            "pressure": "气压",
            "visibility": "能见度",
            "uv_index": "紫外线指数",
            "dew_point": "露点",
            "cloud_coverage": "云量",
            "temperature_group": "温度",
            "humidity_air_group": "湿度与空气",
            "wind_group": "风力",
            "atmospheric_group": "大气",
            "solar_group": "太阳能"
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
        "precipitation_chart_items": {
            "precipitation_chart_title": "降水预报",
            "precipitation_mm": "降水量 (毫米)",
            "probability_percent": "概率 (%)",
            "no_data": "无降水数据",
            "loading": "正在加载降水数据...",
            "time_hours": "时间 (小时)",
            "total_precipitation": "总计",
            "max_intensity": "峰值",
            "rainy_hours": "降雨小时",
            # 降水强度描述
            "intensity_light": "小雨",
            "intensity_moderate": "中雨", 
            "intensity_heavy": "大雨",
            "intensity_very_heavy": "暴雨",
            # 额外标签
            "next_24h": "未来24小时",
            "precipitation_type": "类型",
            "rain": "雨",
            "snow": "雪",
            "mixed": "混合",
            "probability": "概率",
            "when_expected": "预期时间",
            "duration": "持续时间",
            "peak_time": "峰值预期"
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
            "wind_direction": "दिशा",
            "wind_gust": "हवा का झोंका",
            "pressure": "दबाव",
            "visibility": "दृश्यता",
            "uv_index": "यूवी इंडेक्स",
            "dew_point": "ओस बिंदु",
            "cloud_coverage": "बादल कवरेज",
            "temperature_group": "तापमान",
            "humidity_air_group": "नमी और हवा",
            "wind_group": "हवा",
            "atmospheric_group": "वायुमंडलीय",
            "solar_group": "सौर"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "वर्षा पूर्वानुमान",
            "precipitation_mm": "वर्षा (मिमी)",
            "probability_percent": "संभावना (%)",
            "no_data": "वर्षा डेटा उपलब्ध नहीं है",
            "loading": "वर्षा डेटा लोड हो रहा है...",
            "time_hours": "समय (घंटे)",
            "total_precipitation": "कुल",
            "max_intensity": "चरम",
            "rainy_hours": "बारिश के घंटे",
            # वर्षा की तीव्रता का विवरण
            "intensity_light": "हल्की",
            "intensity_moderate": "मध्यम", 
            "intensity_heavy": "भारी",
            "intensity_very_heavy": "बहुत भारी",
            # अतिरिक्त लेबल
            "next_24h": "अगले 24 घंटे",
            "precipitation_type": "प्रकार",
            "rain": "बारिश",
            "snow": "बर्फ",
            "mixed": "मिश्रित",
            "probability": "संभावना",
            "when_expected": "अपेक्षित समय",
            "duration": "अवधि",
            "peak_time": "चरम अपेक्षित"
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
            "wind_direction": "Dirección",
            "wind_gust": "Ráfaga de viento",
            "pressure": "Presión",
            "visibility": "Visibilidad",
            "uv_index": "Índice UV",
            "dew_point": "Punto de rocío",
            "cloud_coverage": "Cobertura de nubes",
            "temperature_group": "Temperatura",
            "humidity_air_group": "Humedad y Aire",
            "wind_group": "Viento",
            "atmospheric_group": "Atmosférico",
            "solar_group": "Solar"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "Pronóstico de Precipitaciones",
            "precipitation_mm": "Precipitaciones (mm)",
            "probability_percent": "Probabilidad (%)",
            "no_data": "Datos de precipitaciones no disponibles",
            "loading": "Cargando datos de precipitaciones...",
            "time_hours": "Tiempo (Horas)",
            "total_precipitation": "Total",
            "max_intensity": "Pico",
            "rainy_hours": "Horas de lluvia",
            # Descripciones de intensidad de precipitación
            "intensity_light": "Ligera",
            "intensity_moderate": "Moderada", 
            "intensity_heavy": "Fuerte",
            "intensity_very_heavy": "Muy fuerte",
            # Etiquetas adicionales
            "next_24h": "Próximas 24 horas",
            "precipitation_type": "Tipo",
            "rain": "Lluvia",
            "snow": "Nieve",
            "mixed": "Mixta",
            "probability": "Probabilidad",
            "when_expected": "Esperado a las",
            "duration": "Duración",
            "peak_time": "Pico esperado"
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
            "wind_direction": "الاتجاه",
            "wind_gust": "هبات الرياح",
            "pressure": "الضغط",
            "visibility": "الرؤية",
            "uv_index": "مؤشر الأشعة فوق البنفسجية",
            "dew_point": "نقطة الندى",
            "cloud_coverage": "تغطية السحب",
            "temperature_group": "درجة الحرارة",
            "humidity_air_group": "الرطوبة والهواء",
            "wind_group": "الرياح",
            "atmospheric_group": "الغلاف الجوي",
            "solar_group": "الطاقة الشمسية"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "توقعات الهطول",
            "precipitation_mm": "الهطول (مم)",
            "probability_percent": "الاحتمال (%)",
            "no_data": "لا توجد بيانات هطول متاحة",
            "loading": "جاري تحميل بيانات الهطول...",
            "time_hours": "الوقت (ساعات)",
            "total_precipitation": "المجموع",
            "max_intensity": "الذروة",
            "rainy_hours": "ساعات المطر",
            # وصف شدة الهطول
            "intensity_light": "خفيف",
            "intensity_moderate": "معتدل", 
            "intensity_heavy": "كثيف",
            "intensity_very_heavy": "كثيف جداً",
            # تسميات إضافية
            "next_24h": "الـ 24 ساعة القادمة",
            "precipitation_type": "النوع",
            "rain": "مطر",
            "snow": "ثلج",
            "mixed": "مختلط",
            "probability": "الاحتمال",
            "when_expected": "متوقع في",
            "duration": "المدة",
            "peak_time": "الذروة متوقعة"
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
            "wind_direction": "Arah",
            "wind_gust": "Hembusan Angin",
            "pressure": "Tekanan",
            "visibility": "Visibilitas",
            "uv_index": "Indeks UV",
            "dew_point": "Titik embun",
            "cloud_coverage": "Tutupan awan",
            "temperature_group": "Suhu",
            "humidity_air_group": "Kelembaban & Udara",
            "wind_group": "Angin",
            "atmospheric_group": "Atmosfer",
            "solar_group": "Matahari"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "Prakiraan Curah Hujan",
            "precipitation_mm": "Curah Hujan (mm)",
            "probability_percent": "Probabilitas (%)",
            "no_data": "Data curah hujan tidak tersedia",
            "loading": "Memuat data curah hujan...",
            "time_hours": "Waktu (Jam)",
            "total_precipitation": "Total",
            "max_intensity": "Puncak",
            "rainy_hours": "Jam hujan",
            # Deskripsi intensitas curah hujan
            "intensity_light": "Ringan",
            "intensity_moderate": "Sedang", 
            "intensity_heavy": "Lebat",
            "intensity_very_heavy": "Sangat lebat",
            # Label tambahan
            "next_24h": "24 jam ke depan",
            "precipitation_type": "Jenis",
            "rain": "Hujan",
            "snow": "Salju",
            "mixed": "Campuran",
            "probability": "Probabilitas",
            "when_expected": "Diperkirakan pada",
            "duration": "Durasi",
            "peak_time": "Puncak diperkirakan"
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
            "wind_direction": "風向",
            "wind_gust": "突風",
            "pressure": "気圧",
            "visibility": "視界",
            "uv_index": "UVインデックス",
            "dew_point": "露点",
            "cloud_coverage": "雲量",
            "temperature_group": "気温",
            "humidity_air_group": "湿度と空気",
            "wind_group": "風",
            "atmospheric_group": "大気",
            "solar_group": "太陽"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "降水量予報",
            "precipitation_mm": "降水量 (mm)",
            "probability_percent": "確率 (%)",
            "no_data": "降水量データがありません",
            "loading": "降水量データを読み込み中...",
            "time_hours": "時間 (時)",
            "total_precipitation": "合計",
            "max_intensity": "ピーク",
            "rainy_hours": "雨の時間",
            # 降水強度の説明
            "intensity_light": "弱い",
            "intensity_moderate": "中程度", 
            "intensity_heavy": "強い",
            "intensity_very_heavy": "非常に強い",
            # 追加ラベル
            "next_24h": "今後24時間",
            "precipitation_type": "種類",
            "rain": "雨",
            "snow": "雪",
            "mixed": "混合",
            "probability": "確率",
            "when_expected": "予想時刻",
            "duration": "継続時間",
            "peak_time": "ピーク予想"
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
            "wind_direction": "Angolazione",
            "wind_gust": "Raffica",
            "pressure": "Pressione",
            "visibility": "Visibilità",
            "uv_index": "Indice UV",
            "dew_point": "Punto di rugiada",
            "cloud_coverage": "Copertura nuvolosa",
            "temperature_group": "Temperatura",
            "humidity_air_group": "Umidità e Aria",
            "wind_group": "Vento",
            "atmospheric_group": "Atmosferico",
            "solar_group": "Solare"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "Previsioni Precipitazioni",
            "precipitation_mm": "Precipitazioni (mm)",
            "probability_percent": "Probabilità (%)",
            "no_data": "Dati precipitazioni non disponibili",
            "loading": "Caricamento dati precipitazioni...",
            "time_hours": "Tempo (Ore)",
            "total_precipitation": "Totale",
            "max_intensity": "Picco",
            "rainy_hours": "Ore di pioggia",
            # Descrizioni intensità precipitazioni
            "intensity_light": "Leggera",
            "intensity_moderate": "Moderata", 
            "intensity_heavy": "Intensa",
            "intensity_very_heavy": "Molto intensa",
            # Etichette aggiuntive
            "next_24h": "Prossime 24 ore",
            "precipitation_type": "Tipo",
            "rain": "Pioggia",
            "snow": "Neve",
            "mixed": "Mista",
            "probability": "Probabilità",
            "when_expected": "Prevista alle",
            "duration": "Durata",
            "peak_time": "Picco previsto"
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
            "wind_direction": "Richtung",
            "wind_gust": "Windböe",
            "pressure": "Druck",
            "visibility": "Sichtweite",
            "uv_index": "UV-Index",
            "dew_point": "Taupunkt",
            "cloud_coverage": "Bewölkung",
            "temperature_group": "Temperatur",
            "humidity_air_group": "Feuchtigkeit & Luft",
            "wind_group": "Wind",
            "atmospheric_group": "Atmosphärisch",
            "solar_group": "Solar"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "Niederschlagsvorhersage",
            "precipitation_mm": "Niederschlag (mm)",
            "probability_percent": "Wahrscheinlichkeit (%)",
            "no_data": "Keine Niederschlagsdaten verfügbar",
            "loading": "Lade Niederschlagsdaten...",
            "time_hours": "Zeit (Stunden)",
            "total_precipitation": "Gesamt",
            "max_intensity": "Spitze",
            "rainy_hours": "Regenstunden",
            # Niederschlagsintensität Beschreibungen
            "intensity_light": "Leicht",
            "intensity_moderate": "Mäßig", 
            "intensity_heavy": "Stark",
            "intensity_very_heavy": "Sehr stark",
            # Zusätzliche Etiketten
            "next_24h": "Nächste 24 Stunden",
            "precipitation_type": "Typ",
            "rain": "Regen",
            "snow": "Schnee",
            "mixed": "Gemischt",
            "probability": "Wahrscheinlichkeit",
            "when_expected": "Erwartet um",
            "duration": "Dauer",
            "peak_time": "Spitze erwartet"
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
            "wind_direction": "Direction",
            "wind_gust": "Rafale de vent",
            "pressure": "Pression",
            "visibility": "Visibilité",
            "uv_index": "Indice UV",
            "dew_point": "Point de rosée",
            "cloud_coverage": "Couverture nuageuse",
            "temperature_group": "Température",
            "humidity_air_group": "Humidité & Air",
            "wind_group": "Vent",
            "atmospheric_group": "Atmosphérique",
            "solar_group": "Solaire"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "Prévisions de Précipitations",
            "precipitation_mm": "Précipitations (mm)",
            "probability_percent": "Probabilité (%)",
            "no_data": "Aucune donnée de précipitations disponible",
            "loading": "Chargement des données de précipitations...",
            "time_hours": "Temps (Heures)",
            "total_precipitation": "Total",
            "max_intensity": "Pic",
            "rainy_hours": "Heures pluvieuses",
            # Descriptions d'intensité des précipitations
            "intensity_light": "Légère",
            "intensity_moderate": "Modérée", 
            "intensity_heavy": "Forte",
            "intensity_very_heavy": "Très forte",
            # Étiquettes supplémentaires
            "next_24h": "Prochaines 24 heures",
            "precipitation_type": "Type",
            "rain": "Pluie",
            "snow": "Neige",
            "mixed": "Mixte",
            "probability": "Probabilité",
            "when_expected": "Attendu à",
            "duration": "Durée",
            "peak_time": "Pic attendu"
        }
    },
    "pt": {
        "popup_menu_items": {
            "weather": "Tempo",
            "map": "Mapa",
            "settings": "Configurações"
        },
        "air_condition_items": {
            "air_condition_title": "Condições do Ar",
            "feels_like": "Sensação",
            "humidity": "Umidade",
            "wind": "Vento",
            "wind_direction": "Direção",
            "wind_gust": "Rajada de vento",
            "pressure": "Pressão",
            "visibility": "Visibilidade",
            "uv_index": "Índice UV",
            "dew_point": "Ponto de Orvalho",
            "cloud_coverage": "Cobertura de Nuvens",
            "temperature_group": "Temperatura",
            "humidity_air_group": "Umidade & Ar",
            "wind_group": "Vento",
            "atmospheric_group": "Atmosférico",
            "solar_group": "Solar"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "Previsão de Precipitação",
            "precipitation_mm": "Precipitação (mm)",
            "probability_percent": "Probabilidade (%)",
            "no_data": "Dados de precipitação não disponíveis",
            "loading": "Carregando dados de precipitação...",
            "time_hours": "Tempo (Horas)",
            "total_precipitation": "Total",
            "max_intensity": "Pico",
            "rainy_hours": "Horas chuvosas",
            # Descrições de intensidade de precipitação
            "intensity_light": "Leve",
            "intensity_moderate": "Moderada", 
            "intensity_heavy": "Pesada",
            "intensity_very_heavy": "Muito pesada",
            # Etiquetas adicionais
            "next_24h": "Próximas 24 horas",
            "precipitation_type": "Tipo",
            "rain": "Chuva",
            "snow": "Neve",
            "mixed": "Mista",
            "probability": "Probabilidade",
            "when_expected": "Esperado às",
            "duration": "Duração",
            "peak_time": "Pico esperado"
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
            "wind_direction": "Направление",
            "wind_gust": "Порыв ветра",
            "pressure": "Давление",
            "visibility": "Видимость",
            "uv_index": "УФ-индекс",
            "dew_point": "Точка росы",
            "cloud_coverage": "Облачность",
            "temperature_group": "Температура",
            "humidity_air_group": "Влажность и Воздух",
            "wind_group": "Ветер",
            "atmospheric_group": "Атмосферное",
            "solar_group": "Солнечное"
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
        },
        "precipitation_chart_items": {
            "precipitation_chart_title": "Прогноз Осадков",
            "precipitation_mm": "Осадки (мм)",
            "probability_percent": "Вероятность (%)",
            "no_data": "Данные об осадках недоступны",
            "loading": "Загрузка данных об осадках...",
            "time_hours": "Время (Часы)",
            "total_precipitation": "Всего",
            "max_intensity": "Пик",
            "rainy_hours": "Дождливые часы",
            # Описания интенсивности осадков
            "intensity_light": "Легкие",
            "intensity_moderate": "Умеренные", 
            "intensity_heavy": "Сильные",
            "intensity_very_heavy": "Очень сильные",
            # Дополнительные метки
            "next_24h": "Следующие 24 часа",
            "precipitation_type": "Тип",
            "rain": "Дождь",
            "snow": "Снег",
            "mixed": "Смешанные",
            "probability": "Вероятность",
            "when_expected": "Ожидается в",
            "duration": "Продолжительность",
            "peak_time": "Пик ожидается"
        }
    }
}