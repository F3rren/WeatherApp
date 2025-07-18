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
            "measurement": "Measurement:", # Used in SettingsAlertDialog
            "use_current_location": "Use current location:", # Used in SettingsAlertDialog
            "dark_theme": "Dark theme:", # Used in SettingsAlertDialog
            "close": "Close", # Used in SettingsAlertDialog
            "location_enabled": "GPS Active",
            "location_disabled": "GPS Inactive",
            "refresh_data": "Refresh",
            "refreshing_data": "Refreshing weather data...",
            "reset_settings": "Reset Settings",
            "about_app": "About",
            "app_status": "App Status",
            "current_city": "City",
            "active_language": "Language",
            "unit_system": "Units",
            "app_info_unavailable": "App info unavailable",
            "settings_reset": "Settings have been reset to defaults",
            "confirm_reset": "Reset all settings to default values?",
            "reset_confirmation": "Confirm Reset",
            "confirm": "Confirm",
            "cancel": "Cancel",
            "about_title": "About MeteoApp",
            "about_description": "A modern weather application built with Flet and Python. Get real-time weather data, forecasts, and interactive maps.",
            "version": "Version",
            "developer": "Developer",
            "features": "Features",
            "feature_list": "• Real-time weather data\n• 5-day forecasts\n• Interactive maps\n• Multi-language support\n• Dark/Light themes\n• GPS location support"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "Weather Map",
            "fullscreen": "Fullscreen",
            "close": "Close",
            "loading": "Loading map...",
            "error": "Error loading map"
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
        },        
        "unit_items": {
            "unit_metric": "Metric (°C)", # Unit option
            "unit_imperial": "Imperial (°F)", # Unit option
            "unit_standard": "Standard (K)", # Unit option
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
        "error_messages": {
            "network_error": "Network connection failed",
            "api_error": "Weather service temporarily unavailable",
            "location_error": "Unable to access location services",
            "data_error": "Error processing weather data",
            "retry": "Retry",
            "offline_mode": "Offline Mode",
            "cached_data": "Showing cached data",
            "last_updated": "Last updated",
            "connection_restored": "Connection restored"
        },
        "performance": {
            "loading": "Loading...",
            "updating": "Updating...",
            "optimizing": "Optimizing performance...",
            "cache_cleared": "Cache cleared successfully"
        },
        "accessibility": {
            "weather_icon": "Weather condition icon",
            "temperature_reading": "Current temperature",
            "humidity_level": "Humidity level",
            "wind_speed": "Wind speed",
            "pressure_reading": "Atmospheric pressure",
            "high_contrast": "High contrast mode",
            "large_text": "Large text mode",
            "screen_reader": "Screen reader compatible"
        },
        "personalization": {
            "favorites": "Favorite Locations",
            "add_favorite": "Add to Favorites",
            "remove_favorite": "Remove from Favorites",
            "custom_alerts": "Weather Alerts",
            "alert_temperature": "Temperature Alert",
            "alert_rain": "Rain Alert",
            "alert_wind": "Wind Alert",
            "notification_settings": "Notification Settings",
            "widget_customization": "Customize Widgets"
        },
        "advanced_features": {
            "radar": "Weather Radar",
            "satellite": "Satellite View",
            "historical_data": "Historical Weather",
            "comparison": "Compare Locations",
            "export_data": "Export Data",
            "share_weather": "Share Weather"
        },
        "weather_alerts": {
            "alerts_title": "Weather Alerts",
            "no_alerts": "No active alerts",
            "alert_settings": "Alert Settings",
            "enable_alerts": "Enable Alerts",
            "alert_thresholds": "Alert Thresholds",
            "acknowledge": "Acknowledge",
            "acknowledge_all": "Acknowledge All",
            "alert_temperature_high_title": "High Temperature Alert",
            "alert_temperature_high_forecast_title": "High Temperature Expected",
            "alert_temperature_high_message": "Temperature has reached {value}°C. Stay hydrated and avoid prolonged sun exposure.",
            "alert_temperature_low_title": "Low Temperature Alert",
            "alert_temperature_low_forecast_title": "Low Temperature Expected",
            "alert_temperature_low_message": "Temperature has dropped to {value}°C. Dress warmly and be careful of icy conditions.",
            "alert_rain_heavy_title": "Heavy Rain Alert",
            "alert_rain_heavy_forecast_title": "Heavy Rain Expected",
            "alert_rain_heavy_message": "Heavy rain detected: {value}mm. Avoid driving if possible and stay indoors.",
            "alert_wind_strong_title": "Strong Wind Alert",
            "alert_wind_strong_forecast_title": "Strong Wind Expected",
            "alert_wind_strong_message": "Strong winds detected: {value}km/h. Secure loose objects and avoid outdoor activities.",
            "alert_uv_high_title": "High UV Index Alert",
            "alert_uv_high_message": "UV Index is high: {value}. Use sunscreen and limit sun exposure.",
            "alert_air_quality_poor_title": "Poor Air Quality Alert",
            "alert_air_quality_poor_message": "Air quality is poor (AQI: {value}). Limit outdoor activities.",
            "alert_storm_title": "Storm Alert",
            "alert_storm_forecast_title": "Storm Warning",
            "alert_storm_message": "Severe weather conditions expected. Stay indoors and avoid travel.",
            "severity_low": "Low",
            "severity_moderate": "Moderate", 
            "severity_high": "High",
            "severity_extreme": "Extreme",
            "alert_type_temperature_high": "High Temperature",
            "alert_type_temperature_low": "Low Temperature",
            "alert_type_rain_heavy": "Heavy Rain",
            "alert_type_wind_strong": "Strong Wind",
            "alert_type_uv_high": "High UV Index",
            "alert_type_air_quality_poor": "Poor Air Quality",
            "alert_type_storm": "Storm Warning"
        }
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
            "measurement": "测量单位:",
            "use_current_location": "使用当前位置：",
            "dark_theme": "深色主题：",
            "close": "关闭"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "天气地图",
            "fullscreen": "全屏",
            "close": "关闭",
            "loading": "地图加载中...",
            "error": "地图加载错误"
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
        },        
        "unit_items": {
            "unit_metric": "公制 (°C)",
            "unit_imperial": "英制 (°F)",
            "unit_standard": "标准 (K)",
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
        "error_messages": {
            "network_error": "网络连接失败",
            "api_error": "天气服务暂时不可用",
            "location_error": "无法访问定位服务",
            "data_error": "处理天气数据时出错",
            "retry": "重试",
            "offline_mode": "离线模式",
            "cached_data": "显示缓存数据",
            "last_updated": "最后更新",
            "connection_restored": "连接已恢复"
        },
        "performance": {
            "loading": "加载中...",
            "updating": "更新中...",
            "optimizing": "优化性能中...",
            "cache_cleared": "缓存成功清除"
        },
        "accessibility": {
            "weather_icon": "天气状况图标",
            "temperature_reading": "当前温度",
            "humidity_level": "湿度水平",
            "wind_speed": "风速",
            "pressure_reading": "大气压力",
            "high_contrast": "高对比度模式",
            "large_text": "大文本模式",
            "screen_reader": "屏幕阅读器兼容"
        },
        "personalization": {
            "favorites": "收藏地点",
            "add_favorite": "添加到收藏",
            "remove_favorite": "从收藏中移除",
            "custom_alerts": "天气警报",
            "alert_temperature": "温度警报",
            "alert_rain": "降雨警报",
            "alert_wind": "风警报",
            "notification_settings": "通知设置",
            "widget_customization": "自定义小部件"
        },
        "advanced_features": {
            "radar": "天气雷达",
            "satellite": "卫星视图",
            "historical_data": "历史天气",
            "comparison": "比较地点",
            "export_data": "导出数据",
            "share_weather": "分享天气"
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
            "measurement": "मापन इकाई:",
            "use_current_location": "वर्तमान स्थान का उपयोग करें:",
            "dark_theme": "डार्क थीम:",
            "close": "बंद करें"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "मौसम मानचित्र",
            "fullscreen": "पूर्ण स्क्रीन",
            "close": "बंद करें",
            "loading": "मानचित्र लोड हो रहा है...",
            "error": "मानचित्र लोड करने में त्रुटि"
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
            "unit_metric": "मीट्रिक (°C)",
            "unit_imperial": "इंपीरियल (°F)",
            "unit_standard": "मानक (K)",
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
        },
        "error_messages": {
            "network_error": "नेटवर्क कनेक्शन विफल",
            "api_error": "मौसम सेवा अस्थायी रूप से अनुपलब्ध",
            "location_error": "स्थान सेवाओं तक पहुंच असंभव",
            "data_error": "मौसम डेटा संसाधित करते समय त्रुटि",
            "retry": "पुनः प्रयास करें",
            "offline_mode": "ऑफलाइन मोड",
            "cached_data": "कैश किए गए डेटा को दिखा रहा है",
            "last_updated": "अंतिम अपडेट",
            "connection_restored": "कनेक्शन बहाल"
        },
        "performance": {
            "loading": "लोड हो रहा है...",
            "updating": "अपडेट हो रहा है...",
            "optimizing": "प्रदर्शन का अनुकूलन कर रहा है...",
            "cache_cleared": "कैश सफलतापूर्वक साफ़ किया गया"
        },
        "accessibility": {
            "weather_icon": "मौसम स्थिति आइकन",
            "temperature_reading": "वर्तमान तापमान",
            "humidity_level": "नमी स्तर",
            "wind_speed": "हवा की गति",
            "pressure_reading": "वायुमंडलीय दबाव",
            "high_contrast": "उच्च विपरीत मोड",
            "large_text": "बड़ा पाठ मोड",
            "screen_reader": "स्क्रीन रीडर संगत"
        },
        "personalization": {
            "favorites": "पसंदीदा स्थान",
            "add_favorite": "पसंदीदा में जोड़ें",
            "remove_favorite": "पसंदीदा से हटाएँ",
            "custom_alerts": "मौसम अलर्ट",
            "alert_temperature": "तापमान अलर्ट",
            "alert_rain": "बारिश अलर्ट",
            "alert_wind": "हवा अलर्ट",
            "notification_settings": "सूचना सेटिंग्स",
            "widget_customization": "विजेट अनुकूलन करें"
        },
        "advanced_features": {
            "radar": "मौसम रडार",
            "satellite": "उपग्रह दृश्य",
            "historical_data": "ऐतिहासिक मौसम",
            "comparison": "स्थान की तुलना करें",
            "export_data": "डेटा निर्यात करें",
            "share_weather": "मौसम साझा करें"
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
            "measurement": "Unidad de medida:",
            "use_current_location": "Usar ubicación actual:",
            "dark_theme": "Tema oscuro:",
            "close": "Cerrar",
            "location_enabled": "GPS Activo",
            "location_disabled": "GPS Inactivo",
            "refresh_data": "Actualizar",
            "refreshing_data": "Actualizando datos...",
            "reset_settings": "Restablecer",
            "about_app": "Acerca de",
            "app_status": "Estado App",
            "current_city": "Ciudad",
            "active_language": "Idioma",
            "unit_system": "Unidades",
            "app_info_unavailable": "Info app no disponible",
            "settings_reset": "Configuración restablecida a valores predeterminados",
            "confirm_reset": "¿Restablecer toda la configuración a valores predeterminados?",
            "reset_confirmation": "Confirmar Restablecimiento",
            "confirm": "Confirmar",
            "cancel": "Cancelar",
            "about_title": "Acerca de MeteoApp",
            "about_description": "Una aplicación meteorológica moderna construida con Flet y Python. Obtén datos meteorológicos en tiempo real, pronósticos y mapas interactivos.",
            "version": "Versión",
            "developer": "Desarrollador",
            "features": "Características",
            "feature_list": "• Datos meteorológicos en tiempo real\n• Pronósticos de 5 días\n• Mapas interactivos\n• Soporte multiidioma\n• Temas oscuro/claro\n• Soporte GPS"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "Mapa del Tiempo",
            "fullscreen": "Pantalla Completa",
            "close": "Cerrar",
            "loading": "Cargando mapa...",
            "error": "Error al cargar el mapa"
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
            "unit_metric": "Métrico (°C)",
            "unit_imperial": "Imperial (°F)",
            "unit_standard": "Estándar (K)",
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
        },
        "error_messages": {
            "network_error": "Error de conexión de red",
            "api_error": "Servicio meteorológico temporalmente no disponible",
            "location_error": "No se puede acceder a los servicios de ubicación",
            "data_error": "Error al procesar los datos meteorológicos",
            "retry": "Reintentar",
            "offline_mode": "Modo sin conexión",
            "cached_data": "Mostrando datos en caché",
            "last_updated": "Última actualización",
            "connection_restored": "Conexión restaurada"
        },
        "performance": {
            "loading": "Cargando...",
            "updating": "Actualizando...",
            "optimizing": "Optimizando rendimiento...",
            "cache_cleared": "Caché borrada con éxito"
        },
        "accessibility": {
            "weather_icon": "Ícono de condición meteorológica",
            "temperature_reading": "Temperatura actual",
            "humidity_level": "Nivel de humedad",
            "wind_speed": "Velocidad del viento",
            "pressure_reading": "Presión atmosférica",
            "high_contrast": "Modo de alto contraste",
            "large_text": "Modo de texto grande",
            "screen_reader": "Compatible con lectores de pantalla"
        },
        "personalization": {
            "favorites": "Ubicaciones favoritas",
            "add_favorite": "Agregar a favoritos",
            "remove_favorite": "Eliminar de favoritos",
            "custom_alerts": "Alertas meteorológicas",
            "alert_temperature": "Alerta de temperatura",
            "alert_rain": "Alerta de lluvia",
            "alert_wind": "Alerta de viento",
            "notification_settings": "Configuración de notificaciones",
            "widget_customization": "Personalizar widgets"
        },
        "advanced_features": {
            "radar": "Radar meteorológico",
            "satellite": "Vista satelital",
            "historical_data": "Datos meteorológicos históricos",
            "comparison": "Comparar ubicaciones",
            "export_data": "Exportar datos",
            "share_weather": "Compartir clima"
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
            "measurement": "القياس:",
            "use_current_location": "استخدام الموقع الحالي:",
            "dark_theme": "الوضع الداكن:",
            "close": "إغلاق"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "خريطة الطقس",
            "fullscreen": "ملء الشاشة",
            "close": "إغلاق",
            "loading": "تحميل الخريطة...",
            "error": "خطأ في تحميل الخريطة"
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
            "unit_metric": "متري (°C)",
            "unit_imperial": "إمبراطوري (°F)",
            "unit_standard": "قياسي (K)",
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
        },
        "error_messages": {
            "network_error": "فشل اتصال الشبكة",
            "api_error": "خدمة الطقس غير متاحة مؤقتًا",
            "location_error": "غير قادر على الوصول إلى خدمات الموقع",
            "data_error": "خطأ في معالجة بيانات الطقس",
            "retry": "إعادة المحاولة",
            "offline_mode": "وضع عدم الاتصال",
            "cached_data": "عرض البيانات المخزنة",
            "last_updated": "آخر تحديث",
            "connection_restored": "تم استعادة الاتصال"
        },
        "performance": {
            "loading": "جارٍ التحميل...",
            "updating": "جارٍ التحديث...",
            "optimizing": "جارٍ تحسين الأداء...",
            "cache_cleared": "تم مسح الذاكرة المؤقتة بنجاح"
        },
        "accessibility": {
            "weather_icon": "رمز حالة الطقس",
            "temperature_reading": "درجة الحرارة الحالية",
            "humidity_level": "مستوى الرطوبة",
            "wind_speed": "سرعة الرياح",
            "pressure_reading": "ضغط الهواء",
            "high_contrast": "وضع التباين العالي",
            "large_text": "وضع النص الكبير",
            "screen_reader": "متوافق مع قارئات الشاشة"
        },
        "personalization": {
            "favorites": "المواقع المفضلة",
            "add_favorite": "أضف إلى المفضلة",
            "remove_favorite": "إزالة من المفضلة",
            "custom_alerts": "تنبيهات الطقس",
            "alert_temperature": "تنبيه درجة الحرارة",
            "alert_rain": "تنبيه المطر",
            "alert_wind": "تنبيه الرياح",
            "notification_settings": "إعدادات الإشعارات",
            "widget_customization": "تخصيص الأدوات"
        },
        "advanced_features": {
            "radar": "رادار الطقس",
            "satellite": "عرض القمر الصناعي",
            "historical_data": "الطقس التاريخي",
            "comparison": "قارن المواقع",
            "export_data": "تصدير البيانات",
            "share_weather": "مشاركة الطقس"
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
            "measurement": "Pengukuran:",
            "use_current_location": "Gunakan lokasi saat ini:",
            "dark_theme": "Tema gelap:",
            "close": "Tutup"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "Peta Cuaca",
            "fullscreen": "Layar Penuh",
            "close": "Tutup",
            "loading": "Memuat peta...",
            "error": "Kesalahan memuat peta"
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
            "unit_metric": "Metrik (°C)",
            "unit_imperial": "Imperial (°F)",
            "unit_standard": "Standar (K)",
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
        },
        "error_messages": {
            "network_error": "Kesalahan koneksi jaringan",
            "api_error": "Layanan cuaca tidak tersedia sementara",
            "location_error": "Tidak dapat mengakses layanan lokasi",
            "data_error": "Kesalahan saat memproses data cuaca",
            "retry": "Coba lagi",
            "offline_mode": "Mode Offline",
            "cached_data": "Menampilkan data yang disimpan",
            "last_updated": "Terakhir diperbarui",
            "connection_restored": "Koneksi dipulihkan"
        },
        "performance": {
            "loading": "Memuat...",
            "updating": "Memperbarui...",
            "optimizing": "Mengoptimalkan kinerja...",
            "cache_cleared": "Cache berhasil dibersihkan"
        },
        "accessibility": {
            "weather_icon": "Ikon kondisi cuaca",
            "temperature_reading": "Suhu saat ini",
            "humidity_level": "Tingkat kelembaban",
            "wind_speed": "Kecepatan angin",
            "pressure_reading": "Tekanan atmosfer",
            "high_contrast": "Mode kontras tinggi",
            "large_text": "Mode teks besar",
            "screen_reader": "Kompatibel dengan pembaca layar"
        },
        "personalization": {
            "favorites": "Lokasi Favorit",
            "add_favorite": "Tambahkan ke Favorit",
            "remove_favorite": "Hapus dari Favorit",
            "custom_alerts": "Peringatan Cuaca",
            "alert_temperature": "Peringatan Suhu",
            "alert_rain": "Peringatan Hujan",
            "alert_wind": "Peringatan Angin",
            "notification_settings": "Pengaturan Notifikasi",
            "widget_customization": "Sesuaikan Widget"
        },
        "advanced_features": {
            "radar": "Radar Cuaca",
            "satellite": "Tampilan Satelit",
            "historical_data": "Cuaca Historis",
            "comparison": "Bandingkan Lokasi",
            "export_data": "Ekspor Data",
            "share_weather": "Bagikan Cuaca"
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
            "measurement": "測定:",
            "use_current_location": "現在地を使用:",
            "dark_theme": "ダークテーマ:",
            "close": "閉じる"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "天気マップ",
            "fullscreen": "全画面",
            "close": "閉じる",
            "loading": "マップを読み込み中...",
            "error": "マップ読み込みエラー"
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
            "unit_metric": "メートル法 (°C)",
            "unit_imperial": "ヤード・ポンド法 (°F)",
            "unit_standard": "標準 (K)",
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
        },
        "error_messages": {
            "network_error": "ネットワーク接続に失敗しました",
            "api_error": "天気サービスは一時的に利用できません",
            "location_error": "位置情報サービスにアクセスできません",
            "data_error": "天気データの処理中にエラーが発生しました",
            "retry": "再試行",
            "offline_mode": "オフラインモード",
            "cached_data": "キャッシュデータを表示中",
            "last_updated": "最終更新",
            "connection_restored": "接続が回復しました"
        },
        "performance": {
            "loading": "読み込み中...",
            "updating": "更新中...",
            "optimizing": "パフォーマンスを最適化中...",
            "cache_cleared": "キャッシュが正常にクリアされました"
        },
        "accessibility": {
            "weather_icon": "天気状態アイコン",
            "temperature_reading": "現在の気温",
            "humidity_level": "湿度レベル",
            "wind_speed": "風速",
            "pressure_reading": "大気圧",
            "high_contrast": "高コントラストモード",
            "large_text": "大文字モード",
            "screen_reader": "スクリーンリーダー対応"
        },
        "personalization": {
            "favorites": "お気に入りの場所",
            "add_favorite": "お気に入りに追加",
            "remove_favorite": "お気に入りから削除",
            "custom_alerts": "天気アラート",
            "alert_temperature": "温度アラート",
            "alert_rain": "雨アラート",
            "alert_wind": "風アラート",
            "notification_settings": "通知設定",
            "widget_customization": "ウィジェットをカスタマイズ"
        },
        "advanced_features": {
            "radar": "天気レーダー",
            "satellite": "衛星ビュー",
            "historical_data": "過去の天気",
            "comparison": "場所を比較",
            "export_data": "データをエクスポート",
            "share_weather": "天気を共有"
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
            "measurement": "Misurazione:",
            "use_current_location": "Usa posizione corrente:",
            "dark_theme": "Tema scuro:",
            "close": "Chiudi",
            "location_enabled": "GPS Attivo",
            "location_disabled": "GPS Inattivo",
            "refresh_data": "Aggiorna",
            "refreshing_data": "Aggiornamento dati meteo...",
            "reset_settings": "Ripristina",
            "about_app": "Info",
            "app_status": "Stato App",
            "current_city": "Città",
            "active_language": "Lingua",
            "unit_system": "Unità",
            "app_info_unavailable": "Info app non disponibili",
            "settings_reset": "Impostazioni ripristinate ai valori predefiniti",
            "confirm_reset": "Ripristinare tutte le impostazioni ai valori predefiniti?",
            "reset_confirmation": "Conferma Ripristino",
            "confirm": "Conferma",
            "cancel": "Annulla",
            "about_title": "Info su MeteoApp",
            "about_description": "Un'applicazione meteo moderna costruita con Flet e Python. Ottieni dati meteo in tempo reale, previsioni e mappe interattive.",
            "version": "Versione",
            "developer": "Sviluppatore",
            "features": "Funzionalità",
            "feature_list": "• Dati meteo in tempo reale\n• Previsioni a 5 giorni\n• Mappe interattive\n• Supporto multilingua\n• Temi scuro/chiaro\n• Supporto GPS"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "Mappa Meteo",
            "fullscreen": "Schermo Intero",
            "close": "Chiudi",
            "loading": "Caricamento mappa...",
            "error": "Errore nel caricamento della mappa"
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
            "air_quality_index": "Indice qualità aria",
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
            "unit_metric": "Metrico (°C)",
            "unit_imperial": "Imperiale (°F)",
            "unit_standard": "Standard (K)",
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
            "intensity_light": "Leggera",
            "intensity_moderate": "Moderata", 
            "intensity_heavy": "Intensa",
            "intensity_very_heavy": "Molto intensa",
            "next_24h": "Prossime 24 ore",
            "precipitation_type": "Tipo",
            "rain": "Pioggia",
            "snow": "Neve",
            "mixed": "Mista",
            "probability": "Probabilità",
            "when_expected": "Prevista alle",
            "duration": "Durata",
            "peak_time": "Picco previsto"
        },
        "error_messages": {
            "network_error": "Errore di connessione di rete",
            "api_error": "Servizio meteorologico temporaneamente non disponibile",
            "location_error": "Impossibile accedere ai servizi di posizione",
            "data_error": "Errore nell'elaborazione dei dati meteo",
            "retry": "Riprova",
            "offline_mode": "Modalità Offline",
            "cached_data": "Mostrando dati memorizzati",
            "last_updated": "Ultimo aggiornamento",
            "connection_restored": "Connessione ripristinata"
        },
        "performance": {
            "loading": "Caricamento...",
            "updating": "Aggiornamento...",
            "optimizing": "Ottimizzazione prestazioni...",
            "cache_cleared": "Cache svuotata con successo"
        },
        "accessibility": {
            "weather_icon": "Icona condizione meteo",
            "temperature_reading": "Temperatura attuale",
            "humidity_level": "Livello umidità",
            "wind_speed": "Velocità vento",
            "pressure_reading": "Pressione atmosferica",
            "high_contrast": "Modalità alto contrasto",
            "large_text": "Modalità testo grande",
            "screen_reader": "Compatibile screen reader"
        },
        "personalization": {
            "favorites": "Località Preferite",
            "add_favorite": "Aggiungi ai Preferiti",
            "remove_favorite": "Rimuovi dai Preferiti",
            "custom_alerts": "Avvisi Meteo",
            "alert_temperature": "Avviso Temperatura",
            "alert_rain": "Avviso Pioggia",
            "alert_wind": "Avviso Vento",
            "notification_settings": "Impostazioni Notifiche",
            "widget_customization": "Personalizza Widget"
        },
        "advanced_features": {
            "radar": "Radar Meteo",
            "satellite": "Vista Satellite",
            "historical_data": "Dati Storici Meteo",
            "comparison": "Confronta Località",
            "export_data": "Esporta Dati",
            "share_weather": "Condividi Meteo"
        },
        "weather_alerts": {
            "alerts_title": "Allerte Meteo",
            "no_alerts": "Nessuna allerta attiva",
            "alert_settings": "Impostazioni Allerte",
            "enable_alerts": "Abilita Allerte",
            "alert_thresholds": "Soglie di Allerta",
            "acknowledge": "Prendi Nota",
            "acknowledge_all": "Prendi Nota di Tutte",
            "alert_temperature_high_title": "Allerta Temperatura Alta",
            "alert_temperature_high_forecast_title": "Temperatura Alta Prevista",
            "alert_temperature_high_message": "La temperatura ha raggiunto {value}°C. Rimani idratato ed evita l'esposizione prolungata al sole.",
            "alert_temperature_low_title": "Allerta Temperatura Bassa",
            "alert_temperature_low_forecast_title": "Temperatura Bassa Prevista",
            "alert_temperature_low_message": "La temperatura è scesa a {value}°C. Vestiti pesante e attenzione alle condizioni di ghiaccio.",
            "alert_rain_heavy_title": "Allerta Pioggia Intensa",
            "alert_rain_heavy_forecast_title": "Pioggia Intensa Prevista",
            "alert_rain_heavy_message": "Rilevata pioggia intensa: {value}mm. Evita di guidare se possibile e resta al coperto.",
            "alert_wind_strong_title": "Allerta Vento Forte",
            "alert_wind_strong_forecast_title": "Vento Forte Previsto",
            "alert_wind_strong_message": "Rilevato vento forte: {value}km/h. Metti in sicurezza oggetti liberi ed evita attività all'aperto.",
            "alert_uv_high_title": "Allerta Indice UV Alto",
            "alert_uv_high_message": "Indice UV alto: {value}. Usa la protezione solare e limita l'esposizione al sole.",
            "alert_air_quality_poor_title": "Allerta Qualità dell'Aria Scarsa",
            "alert_air_quality_poor_message": "La qualità dell'aria è scarsa (AQI: {value}). Limita le attività all'aperto.",
            "alert_storm_title": "Allerta Tempesta",
            "alert_storm_forecast_title": "Avviso di Tempesta",
            "alert_storm_message": "Previste condizioni meteorologiche severe. Resta al coperto ed evita di viaggiare.",
            "severity_low": "Bassa",
            "severity_moderate": "Moderata",
            "severity_high": "Alta",
            "severity_extreme": "Estrema",
            "alert_type_temperature_high": "Temperatura Alta",
            "alert_type_temperature_low": "Temperatura Bassa",
            "alert_type_rain_heavy": "Pioggia Intensa",
            "alert_type_wind_strong": "Vento Forte",
            "alert_type_uv_high": "Indice UV Alto",
            "alert_type_air_quality_poor": "Qualità dell'Aria Scarsa",
            "alert_type_storm": "Avviso di Tempesta"
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
            "measurement": "Messung:",
            "use_current_location": "Aktuellen Standort verwenden:",
            "dark_theme": "Dunkles Thema:",
            "close": "Schließen",
            "location_enabled": "GPS Aktiv",
            "location_disabled": "GPS Inaktiv",
            "refresh_data": "Aktualisieren",
            "refreshing_data": "Daten werden aktualisiert...",
            "reset_settings": "Zurücksetzen",
            "about_app": "Über",
            "app_status": "App-Status",
            "current_city": "Stadt",
            "active_language": "Sprache",
            "unit_system": "Einheiten",
            "app_info_unavailable": "App-Info nicht verfügbar",
            "settings_reset": "Einstellungen auf Standardwerte zurückgesetzt",
            "confirm_reset": "Alle Einstellungen auf Standardwerte zurücksetzen?",
            "reset_confirmation": "Zurücksetzen bestätigen",
            "confirm": "Bestätigen",
            "cancel": "Abbrechen",
            "about_title": "Über MeteoApp",
            "about_description": "Eine moderne Wetter-App, erstellt mit Flet und Python. Erhalten Sie Echtzeit-Wetterdaten, Vorhersagen und interaktive Karten.",
            "version": "Version",
            "developer": "Entwickler",
            "features": "Funktionen",
            "feature_list": "• Echtzeit-Wetterdaten\n• 5-Tage-Vorhersagen\n• Interaktive Karten\n• Mehrsprachiger Support\n• Dunkle/Helle Themes\n• GPS-Support"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "Wetterkarte",
            "fullscreen": "Vollbild",
            "close": "Schließen",
            "loading": "Karte wird geladen...",
            "error": "Fehler beim Laden der Karte"
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
            "unit_metric": "Metrisch (°C)",
            "unit_imperial": "Imperial (°F)",
            "unit_standard": "Standard (K)",
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
        },
        "error_messages": {
            "network_error": "Netzwerkverbindung fehlgeschlagen",
            "api_error": "Wetterdienst vorübergehend nicht verfügbar",
            "location_error": "Standortdienste können nicht zugegriffen werden",
            "data_error": "Fehler bei der Verarbeitung der Wetterdaten",
            "retry": "Erneut versuchen",
            "offline_mode": "Offline-Modus",
            "cached_data": "Zeige zwischengespeicherte Daten",
            "last_updated": "Zuletzt aktualisiert",
            "connection_restored": "Verbindung wiederhergestellt"
        },
        "performance": {
            "loading": "Laden...",
            "updating": "Aktualisieren...",
            "optimizing": "Leistung optimieren...",
            "cache_cleared": "Cache erfolgreich geleert"
        },
        "accessibility": {
            "weather_icon": "Wetterzustandsymbol",
            "temperature_reading": "Aktuelle Temperatur",
            "humidity_level": "Luftfeuchtigkeitslevel",
            "wind_speed": "Windgeschwindigkeit",
            "pressure_reading": "Luftdruck",
            "high_contrast": "Hochkontrastmodus",
            "large_text": "Großer Textmodus",
            "screen_reader": "Bildschirmlesegerät kompatibel"
        },
        "personalization": {
            "favorites": "Lieblingsstandorte",
            "add_favorite": "Zu Favoriten hinzufügen",
            "remove_favorite": "Von Favoriten entfernen",
            "custom_alerts": "Wetterwarnungen",
            "alert_temperature": "Temperaturwarnung",
            "alert_rain": "Regenwarnung",
            "alert_wind": "Windwarnung",
            "notification_settings": "Benachrichtigungseinstellungen",
            "widget_customization": "Widgets anpassen"
        },
        "advanced_features": {
            "radar": "Wetterradar",
            "satellite": "Satellitenansicht",
            "historical_data": "Historische Wetterdaten",
            "comparison": "Standorte vergleichen",
            "export_data": "Daten exportieren",
            "share_weather": "Wetter teilen"
        },
        "weather_alerts": {
            "alerts_title": "Wetterwarnungen",
            "no_alerts": "Keine aktiven Warnungen",
            "alert_settings": "Warnung Einstellungen",
            "enable_alerts": "Warnungen aktivieren",
            "alert_thresholds": "Warnschwellen",
            "acknowledge": "Bestätigen",
            "acknowledge_all": "Alle bestätigen",
            "alert_temperature_high_title": "Hohe Temperatur Warnung",
            "alert_temperature_high_forecast_title": "Hohe Temperatur erwartet",
            "alert_temperature_high_message": "Temperatur hat {value}°C erreicht. Viel trinken und längere Sonnenexposition vermeiden.",
            "alert_temperature_low_title": "Niedrige Temperatur Warnung",
            "alert_temperature_low_forecast_title": "Niedrige Temperatur erwartet",
            "alert_temperature_low_message": "Temperatur ist auf {value}°C gefallen. Warm anziehen und auf Eis achten.",
            "alert_rain_heavy_title": "Starkregen Warnung",
            "alert_rain_heavy_forecast_title": "Starkregen erwartet",
            "alert_rain_heavy_message": "Starkregen erkannt: {value}mm. Wenn möglich nicht fahren und drinnen bleiben.",
            "alert_wind_strong_title": "Starker Wind Warnung",
            "alert_wind_strong_forecast_title": "Starker Wind erwartet",
            "alert_wind_strong_message": "Starker Wind erkannt: {value}km/h. Lose Gegenstände sichern und Outdoor-Aktivitäten vermeiden.",
            "alert_uv_high_title": "Hoher UV-Index Warnung",
            "alert_uv_high_message": "UV-Index ist hoch: {value}. Sonnencreme verwenden und Sonnenexposition begrenzen.",
            "alert_air_quality_poor_title": "Schlechte Luftqualität Warnung",
            "alert_air_quality_poor_message": "Luftqualität ist schlecht (AQI: {value}). Outdoor-Aktivitäten begrenzen.",
            "alert_storm_title": "Sturm Warnung",
            "alert_storm_forecast_title": "Sturm Warnung",
            "alert_storm_message": "Schwere Wetterbedingungen erwartet. Drinnen bleiben und Reisen vermeiden.",
            "severity_low": "Niedrig",
            "severity_moderate": "Mäßig",
            "severity_high": "Hoch",
            "severity_extreme": "Extrem",
            "alert_type_temperature_high": "Hohe Temperatur",
            "alert_type_temperature_low": "Niedrige Temperatur",
            "alert_type_rain_heavy": "Starkregen",
            "alert_type_wind_strong": "Starker Wind",
            "alert_type_uv_high": "Hoher UV-Index",
            "alert_type_air_quality_poor": "Schlechte Luftqualität",
            "alert_type_storm": "Sturm Warnung"
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
            "measurement": "Mesure:",
            "use_current_location": "Utiliser la position actuelle:",
            "dark_theme": "Thème sombre:",
            "close": "Fermer",
            "location_enabled": "GPS Actif",
            "location_disabled": "GPS Inactif",
            "refresh_data": "Actualiser",
            "refreshing_data": "Actualisation des données...",
            "reset_settings": "Réinitialiser",
            "about_app": "À propos",
            "app_status": "État App",
            "current_city": "Ville",
            "active_language": "Langue",
            "unit_system": "Unités",
            "app_info_unavailable": "Info app indisponible",
            "settings_reset": "Paramètres réinitialisés aux valeurs par défaut",
            "confirm_reset": "Réinitialiser tous les paramètres aux valeurs par défaut?",
            "reset_confirmation": "Confirmer la Réinitialisation",
            "confirm": "Confirmer",
            "cancel": "Annuler",
            "about_title": "À propos de MeteoApp",
            "about_description": "Une application météo moderne construite avec Flet et Python. Obtenez des données météo en temps réel, des prévisions et des cartes interactives.",
            "version": "Version",
            "developer": "Développeur",
            "features": "Fonctionnalités",
            "feature_list": "• Données météo en temps réel\n• Prévisions 5 jours\n• Cartes interactives\n• Support multilingue\n• Thèmes sombre/clair\n• Support GPS"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "Carte Météo",
            "fullscreen": "Plein Écran",
            "close": "Fermer",
            "loading": "Chargement de la carte...",
            "error": "Erreur lors du chargement de la carte"
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
            "unit_metric": "Métrique (°C)",
            "unit_imperial": "Impérial (°F)",
            "unit_standard": "Standard (K)",
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
        },
        "error_messages": {
            "network_error": "Échec de la connexion réseau",
            "api_error": "Service météorologique temporairement indisponible",
            "location_error": "Impossible d'accéder aux services de localisation",
            "data_error": "Erreur lors du traitement des données météorologiques",
            "retry": "Réessayer",
            "offline_mode": "Mode hors ligne",
            "cached_data": "Affichage des données mises en cache",
            "last_updated": "Dernière mise à jour",
            "connection_restored": "Connexion restaurée"
        },
        "performance": {
            "loading": "Chargement...",
            "updating": "Mise à jour...",
            "optimizing": "Optimisation des performances...",
            "cache_cleared": "Cache vidé avec succès"
        },
        "accessibility": {
            "weather_icon": "Icône de condition météorologique",
            "temperature_reading": "Température actuelle",
            "humidity_level": "Niveau d'humidité",
            "wind_speed": "Vitesse du vent",
            "pressure_reading": "Pression atmosphérique",
            "high_contrast": "Mode haute contraste",
            "large_text": "Mode texte large",
            "screen_reader": "Compatible avec les lecteurs d'écran"
        },
        "personalization": {
            "favorites": "Lieux favoris",
            "add_favorite": "Ajouter aux favoris",
            "remove_favorite": "Retirer des favoris",
            "custom_alerts": "Alertes météo",
            "alert_temperature": "Alerte de température",
            "alert_rain": "Alerte de pluie",
            "alert_wind": "Alerte de vent",
            "notification_settings": "Paramètres de notification",
            "widget_customization": "Personnaliser les widgets"
        },
        "advanced_features": {
            "radar": "Radar météo",
            "satellite": "Vue satellite",
            "historical_data": "Données météorologiques historiques",
            "comparison": "Comparer les emplacements",
            "export_data": "Exporter les données",
            "share_weather": "Partager la météo"
        },
        "weather_alerts": {
            "alerts_title": "Alertes Météo",
            "no_alerts": "Aucune alerte active",
            "alert_settings": "Paramètres d'Alerte",
            "enable_alerts": "Activer les Alertes",
            "alert_thresholds": "Seuils d'Alerte",
            "acknowledge": "Confirmer",
            "acknowledge_all": "Confirmer Toutes",
            "alert_temperature_high_title": "Alerte Température Élevée",
            "alert_temperature_high_forecast_title": "Température Élevée Prévue",
            "alert_temperature_high_message": "La température a atteint {value}°C. Restez hydraté et évitez l'exposition prolongée au soleil.",
            "alert_temperature_low_title": "Alerte Température Basse",
            "alert_temperature_low_forecast_title": "Température Basse Prévue",
            "alert_temperature_low_message": "La température est tombée à {value}°C. Habillez-vous chaudement et attention aux conditions glaciales.",
            "alert_rain_heavy_title": "Alerte Pluie Intense",
            "alert_rain_heavy_forecast_title": "Pluie Intense Prévue",
            "alert_rain_heavy_message": "Pluie intense détectée: {value}mm. Évitez de conduire si possible et restez à l'intérieur.",
            "alert_wind_strong_title": "Alerte Vent Fort",
            "alert_wind_strong_forecast_title": "Vent Fort Prévu",
            "alert_wind_strong_message": "Vent fort détecté: {value}km/h. Sécurisez les objets libres et évitez les activités extérieures.",
            "alert_uv_high_title": "Alerte Indice UV Élevé",
            "alert_uv_high_message": "L'indice UV est élevé: {value}. Utilisez de la crème solaire et limitez l'exposition au soleil.",
            "alert_air_quality_poor_title": "Alerte Qualité de l'Air Médiocre",
            "alert_air_quality_poor_message": "La qualité de l'air est médiocre (AQI: {value}). Limitez les activités extérieures.",
            "alert_storm_title": "Alerte Tempête",
            "alert_storm_forecast_title": "Avertissement de Tempête",
            "alert_storm_message": "Conditions météorologiques sévères attendues. Restez à l'intérieur et évitez de voyager.",
            "severity_low": "Faible",
            "severity_moderate": "Modérée",
            "severity_high": "Élevée",
            "severity_extreme": "Extrême",
            "alert_type_temperature_high": "Température Élevée",
            "alert_type_temperature_low": "Température Basse",
            "alert_type_rain_heavy": "Pluie Intense",
            "alert_type_wind_strong": "Vent Fort",
            "alert_type_uv_high": "Indice UV Élevé",
            "alert_type_air_quality_poor": "Qualité de l'Air Médiocre",
            "alert_type_storm": "Avertissement de Tempête"
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
            "measurement": "Medição:",
            "use_current_location": "Usar localização atual:",
            "dark_theme": "Tema escuro:",
            "close": "Fechar"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "Mapa do Tempo",
            "fullscreen": "Tela Cheia",
            "close": "Fechar",
            "loading": "Carregando mapa...",
            "error": "Erro ao carregar mapa"
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
            "unit_metric": "Métrico (°C)",
            "unit_imperial": "Imperial (°F)",
            "unit_standard": "Padrão (K)",
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
        },
        "error_messages": {
            "network_error": "Erro de conexão de rede",
            "api_error": "Serviço meteorológico temporariamente não disponível",
            "location_error": "Não é possível acessar os serviços de localização",
            "data_error": "Erro ao processar os dados meteorológicos",
            "retry": "Tentar novamente",
            "offline_mode": "Modo offline",
            "cached_data": "Exibindo dados em cache",
            "last_updated": "Última atualização",
            "connection_restored": "Conexão restaurada"
        },
        "performance": {
            "loading": "Carregando...",
            "updating": "Atualizando...",
            "optimizing": "Otimizando desempenho...",
            "cache_cleared": "Cache limpa com sucesso"
        },
        "accessibility": {
            "weather_icon": "Ícone de condição meteorológica",
            "temperature_reading": "Temperatura atual",
            "humidity_level": "Nível de umidade",
            "wind_speed": "Velocidade do vento",
            "pressure_reading": "Pressão atmosférica",
            "high_contrast": "Modo de alto contraste",
            "large_text": "Modo de texto grande",
            "screen_reader": "Compatível com leitores de tela"
        },
        "personalization": {
            "favorites": "Locais Favoritos",
            "add_favorite": "Adicionar aos Favoritos",
            "remove_favorite": "Remover dos Favoritos",
            "custom_alerts": "Alertas Meteorológicos",
            "alert_temperature": "Alerta de Temperatura",
            "alert_rain": "Alerta de Chuva",
            "alert_wind": "Alerta de Vento",
            "notification_settings": "Configurações de Notificação",
            "widget_customization": "Personalizar Widgets"
        },
        "advanced_features": {
            "radar": "Radar do Tempo",
            "satellite": "Visão por Satélite",
            "historical_data": "Dados Meteorológicos Históricos",
            "comparison": "Comparar Localizações",
            "export_data": "Exportar Dados",
            "share_weather": "Compartilhar Clima"
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
            "measurement": "Измерение:",
            "use_current_location": "Использовать текущее местоположение:",
            "dark_theme": "Темная тема:",
            "close": "Закрыть"
        },
        "maps_alert_dialog_items": {
            "weather_map_title": "Карта Погоды",
            "fullscreen": "Полный Экран",
            "close": "Закрыть",
            "loading": "Загрузка карты...",
            "error": "Ошибка загрузки карты"
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
        },        
        "unit_items": {
            "unit_metric": "Метрическая (°C)",
            "unit_imperial": "Имперская (°F)",
            "unit_standard": "Стандартная (K)",
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
        },
        "error_messages": {
            "network_error": "Ошибка сетевого подключения",
            "api_error": "Служба погоды временно недоступна",
            "location_error": "Не удается получить доступ к службам местоположения",
            "data_error": "Ошибка обработки данных о погоде",
            "retry": "Повторить",
            "offline_mode": "Оффлайн режим",
            "cached_data": "Показать кэшированные данные",
            "last_updated": "Последнее обновление",
            "connection_restored": "Соединение восстановлено"
        },
        "performance": {
            "loading": "Загрузка...",
            "updating": "Обновление...",
            "optimizing": "Оптимизация производительности...",
            "cache_cleared": "Кэш успешно очищен"
        },
        "accessibility": {
            "weather_icon": "Иконка состояния погоды",
            "temperature_reading": "Текущая температура",
            "humidity_level": "Уровень влажности",
            "wind_speed": "Скорость ветра",
            "pressure_reading": "Атмосферное давление",
            "high_contrast": "Режим высокого контраста",
            "large_text": "Режим большого текста",
            "screen_reader": "Совместимо с экранными считывателями"
        },
        "personalization": {
            "favorites": "Избранные места",
            "add_favorite": "Добавить в Избранное",
            "remove_favorite": "Удалить из Избранного",
            "custom_alerts": "Метео-оповещения",
            "alert_temperature": "Предупреждение о температуре",
            "alert_rain": "Предупреждение о дожде",
            "alert_wind": "Предупреждение о ветре",
            "notification_settings": "Настройки уведомлений",
            "widget_customization": "Настроить виджеты"
        },
        "advanced_features": {
            "radar": "Метеорадар",
            "satellite": "Спутниковый вид",
            "historical_data": "Исторические данные погоды",
            "comparison": "Сравнить местоположения",
            "export_data": "Экспорт данных",
            "share_weather": "Поделиться погодой"
        }
    }
}

# Dizionari centralizzati per air_quality_indicators in tutte le lingue
AIR_QUALITY_INDICATORS = {
    "humidity": {
        "excellent": {"en": "Excellent", "it": "Ottima", "fr": "Excellente", "de": "Ausgezeichnet", "es": "Excelente", "pt": "Excelente", "ru": "Отличная", "zh_cn": "优秀", "hi": "उत्कृष्ट", "ja": "優秀", "ar": "ممتاز", "id": "Sangat Baik"},
        "good": {"en": "Good", "it": "Buona", "fr": "Bonne", "de": "Gut", "es": "Buena", "pt": "Boa", "ru": "Хорошая", "zh_cn": "良好", "hi": "अच्छा", "ja": "良い", "ar": "جيد", "id": "Baik"},
        "moderate": {"en": "Moderate", "it": "Moderata", "fr": "Modérée", "de": "Mäßig", "es": "Moderada", "pt": "Moderada", "ru": "Умеренная", "zh_cn": "适中", "hi": "मध्यम", "ja": "普通", "ar": "معتدل", "id": "Sedang"},
        "poor": {"en": "Poor", "it": "Scarsa", "fr": "Médiocre", "de": "Schlecht", "es": "Mala", "pt": "Ruim", "ru": "Плохая", "zh_cn": "差", "hi": "खराब", "ja": "悪い", "ar": "سيء", "id": "Buruk"},
        "very_poor": {"en": "Very Poor", "it": "Molto scarsa", "fr": "Très médiocre", "de": "Sehr schlecht", "es": "Muy mala", "pt": "Muito ruim", "ru": "Очень плохая", "zh_cn": "很差", "hi": "बहुत खराब", "ja": "とても悪い", "ar": "سيء جداً", "id": "Sangat Buruk"}
    },
    "uv_index": {
        "low": {"en": "Low", "it": "Basso", "fr": "Faible", "de": "Niedrig", "es": "Bajo", "pt": "Baixo", "ru": "Низкий", "zh_cn": "低", "hi": "कम", "ja": "低い", "ar": "منخفض", "id": "Rendah"},
        "moderate": {"en": "Moderate", "it": "Moderato", "fr": "Modéré", "de": "Mäßig", "es": "Moderado", "pt": "Moderado", "ru": "Умеренный", "zh_cn": "适中", "hi": "मध्यम", "ja": "普通", "ar": "معتدل", "id": "Sedang"},
        "high": {"en": "High", "it": "Alto", "fr": "Élevé", "de": "Hoch", "es": "Alto", "pt": "Alto", "ru": "Высокий", "zh_cn": "高", "hi": "उच्च", "ja": "高い", "ar": "عالي", "id": "Tinggi"},
        "very_high": {"en": "Very High", "it": "Molto alto", "fr": "Très élevé", "de": "Sehr hoch", "es": "Muy alto", "pt": "Muito alto", "ru": "Очень высокий", "zh_cn": "很高", "hi": "बहुत उच्च", "ja": "とても高い", "ar": "عالي جداً", "id": "Sangat Tinggi"},
        "extreme": {"en": "Extreme", "it": "Estremo", "fr": "Extrême", "de": "Extrem", "es": "Extremo", "pt": "Extremo", "ru": "Экстремальный", "zh_cn": "极端", "hi": "चरम", "ja": "極端", "ar": "متطرف", "id": "Ekstrem"}
    },
    "pressure": {
        "normal": {"en": "Normal", "it": "Normale", "fr": "Normale", "de": "Normal", "es": "Normal", "pt": "Normal", "ru": "Нормальное", "zh_cn": "正常", "hi": "सामान्य", "ja": "正常", "ar": "طبيعي", "id": "Normal"},
        "low": {"en": "Low", "it": "Bassa", "fr": "Basse", "de": "Niedrig", "es": "Baja", "pt": "Baixa", "ru": "Низкое", "zh_cn": "低", "hi": "कम", "ja": "低い", "ar": "منخفض", "id": "Rendah"},
        "high": {"en": "High", "it": "Alta", "fr": "Élevée", "de": "Hoch", "es": "Alta", "pt": "Alta", "ru": "Высокое", "zh_cn": "高", "hi": "उच्च", "ja": "高い", "ar": "عالي", "id": "Tinggi"},
        "very_low": {"en": "Very Low", "it": "Molto bassa", "fr": "Très basse", "de": "Sehr niedrig", "es": "Muy baja", "pt": "Muito baixa", "ru": "Очень низкое", "zh_cn": "很低", "hi": "बहुत कम", "ja": "とても低い", "ar": "منخفض جداً", "id": "Sangat Rendah"},
        "very_high": {"en": "Very High", "it": "Molto alta", "fr": "Très élevée", "de": "Sehr hoch", "es": "Muy alta", "pt": "Muito alta", "ru": "Очень высокое", "zh_cn": "很高", "hi": "बहुत उच्च", "ja": "とても高い", "ar": "عالي جداً", "id": "Sangat Tinggi"}
    },
    "visibility": {
        "excellent": {"en": "Excellent", "it": "Ottima", "fr": "Excellente", "de": "Ausgezeichnet", "es": "Excelente", "pt": "Excelente", "ru": "Отличная", "zh_cn": "优秀", "hi": "उत्कृष्ट", "ja": "優秀", "ar": "ممتاز", "id": "Sangat Baik"},
        "good": {"en": "Good", "it": "Buona", "fr": "Bonne", "de": "Gut", "es": "Buena", "pt": "Boa", "ru": "Хорошая", "zh_cn": "良好", "hi": "अच्छा", "ja": "良い", "ar": "جيد", "id": "Baik"},
        "moderate": {"en": "Moderate", "it": "Moderata", "fr": "Modérée", "de": "Mäßig", "es": "Moderada", "pt": "Moderada", "ru": "Умеренная", "zh_cn": "适中", "hi": "मध्यम", "ja": "普通", "ar": "معتدل", "id": "Sedang"},
        "poor": {"en": "Poor", "it": "Scarsa", "fr": "Médiocre", "de": "Schlecht", "es": "Mala", "pt": "Ruim", "ru": "Плохая", "zh_cn": "差", "hi": "खराब", "ja": "悪い", "ar": "سيء", "id": "Buruk"},
        "very_poor": {"en": "Very Poor", "it": "Molto scarsa", "fr": "Très médiocre", "de": "Sehr schlecht", "es": "Muy mala", "pt": "Muito ruim", "ru": "Очень плохая", "zh_cn": "很差", "hi": "बहुत खराब", "ja": "とても悪い", "ar": "سيء جداً", "id": "Sangat Buruk"}
    },
    "feels_like": {
        "ideal": {"en": "Ideal", "it": "Ideale", "fr": "Idéale", "de": "Ideal", "es": "Ideal", "pt": "Ideal", "ru": "Идеальная", "zh_cn": "理想", "hi": "आदर्श", "ja": "理想的", "ar": "مثالي", "id": "Ideal"},
        "comfortable": {"en": "Comfortable", "it": "Confortevole", "fr": "Confortable", "de": "Komfortabel", "es": "Cómoda", "pt": "Confortável", "ru": "Комфортная", "zh_cn": "舒适", "hi": "आरामदायक", "ja": "快適", "ar": "مريح", "id": "Nyaman"},
        "acceptable": {"en": "Acceptable", "it": "Accettabile", "fr": "Acceptable", "de": "Akzeptabel", "es": "Aceptable", "pt": "Aceitável", "ru": "Приемлемая", "zh_cn": "可接受", "hi": "स्वीकार्य", "ja": "許容範囲", "ar": "مقبول", "id": "Dapat Diterima"},
        "uncomfortable": {"en": "Uncomfortable", "it": "Scomodo", "fr": "Inconfortable", "de": "Unkomfortabel", "es": "Incómoda", "pt": "Desconfortável", "ru": "Некомфортная", "zh_cn": "不舒适", "hi": "असहज", "ja": "不快", "ar": "غير مريح", "id": "Tidak Nyaman"},
        "extreme": {"en": "Extreme", "it": "Estremo", "fr": "Extrême", "de": "Extrem", "es": "Extrema", "pt": "Extrema", "ru": "Экстремальная", "zh_cn": "极端", "hi": "चरम", "ja": "極端", "ar": "متطرف", "id": "Ekstrem"}
    },
    "wind": {
        "calm": {"en": "Calm", "it": "Calmo", "fr": "Calme", "de": "Windstill", "es": "Calmado", "pt": "Calmo", "ru": "Штиль", "zh_cn": "无风", "hi": "शांत", "ja": "無風", "ar": "هدوء", "id": "Tenang"},
        "light": {"en": "Light", "it": "Leggero", "fr": "Léger", "de": "Schwach", "es": "Ligero", "pt": "Leve", "ru": "Слабый", "zh_cn": "微风", "hi": "हल्की", "ja": "軽風", "ar": "خفيف", "id": "Ringan"},
        "moderate": {"en": "Moderate", "it": "Moderato", "fr": "Modéré", "de": "Mäßig", "es": "Moderado", "pt": "Moderado", "ru": "Умеренный", "zh_cn": "和风", "hi": "मध्यम", "ja": "中風", "ar": "معتدل", "id": "Sedang"},
        "strong": {"en": "Strong", "it": "Forte", "fr": "Fort", "de": "Stark", "es": "Fuerte", "pt": "Forte", "ru": "Сильный", "zh_cn": "强风", "hi": "तेज़", "ja": "強風", "ar": "قوي", "id": "Kuat"},
        "very_strong": {"en": "Very Strong", "it": "Molto forte", "fr": "Très fort", "de": "Sehr stark", "es": "Muy fuerte", "pt": "Muito forte", "ru": "Очень сильный", "zh_cn": "大风", "hi": "बहुत तेज़", "ja": "非常に強い", "ar": "قوي جداً", "id": "Sangat Kuat"}
    },
    "dew_point": {
        "dry": {"en": "Dry", "it": "Secco", "fr": "Sec", "de": "Trocken", "es": "Seco", "pt": "Seco", "ru": "Сухо", "zh_cn": "干燥", "hi": "सूखा", "ja": "乾燥", "ar": "جاف", "id": "Kering"},
        "comfortable": {"en": "Comfortable", "it": "Confortevole", "fr": "Confortable", "de": "Komfortabel", "es": "Cómodo", "pt": "Confortável", "ru": "Комфортно", "zh_cn": "舒适", "hi": "आरामदायक", "ja": "快適", "ar": "مريح", "id": "Nyaman"},
        "humid": {"en": "Humid", "it": "Umido", "fr": "Humide", "de": "Feucht", "es": "Húmedo", "pt": "Úmido", "ru": "Влажно", "zh_cn": "潮湿", "hi": "नम", "ja": "湿気", "ar": "رطب", "id": "Lembap"},
        "unpleasant": {"en": "Unpleasant", "it": "Sgradevole", "fr": "Désagréable", "de": "Unangenehm", "es": "Desagradable", "pt": "Desagradável", "ru": "Неприятно", "zh_cn": "不舒服", "hi": "अप्रिय", "ja": "不快", "ar": "غير مريح", "id": "Tidak Menyenangkan"},
        "oppressive": {"en": "Oppressive", "it": "Oppressivo", "fr": "Oppressant", "de": "Drückend", "es": "Opresivo", "pt": "Opressivo", "ru": "Удушливо", "zh_cn": "闷热", "hi": "दमघोंटू", "ja": "圧迫的", "ar": "خانق", "id": "Menekan"}
    },
    "cloud_coverage": {
        "clear": {"en": "Clear", "it": "Sereno", "fr": "Dégagé", "de": "Klar", "es": "Despejado", "pt": "Limpo", "ru": "Ясно", "zh_cn": "晴朗", "hi": "साफ", "ja": "晴れ", "ar": "صافي", "id": "Cerah"},
        "partly_cloudy": {"en": "Partly Cloudy", "it": "Poco nuvoloso", "fr": "Partiellement nuageux", "de": "Teilweise bewölkt", "es": "Parcialmente nublado", "pt": "Parcialmente nublado", "ru": "Переменная облачность", "zh_cn": "部分多云", "hi": "आंशिक रूप से बादल", "ja": "一部曇り", "ar": "غائم جزئياً", "id": "Sebagian Berawan"},
        "partly_cloudy_moderate": {"en": "Partly Cloudy", "it": "Parzialmente nuvoloso", "fr": "Partiellement nuageux", "de": "Mäßig bewölkt", "es": "Parcialmente nublado", "pt": "Parcialmente nublado", "ru": "Умеренная облачность", "zh_cn": "部分多云", "hi": "मध्यम बादल", "ja": "部分的に曇り", "ar": "غائم معتدل", "id": "Berawan Sedang"},
        "mostly_cloudy": {"en": "Mostly Cloudy", "it": "Molto nuvoloso", "fr": "Très nuageux", "de": "Stark bewölkt", "es": "Muy nublado", "pt": "Muito nublado", "ru": "Пасмурно", "zh_cn": "多云", "hi": "अधिकतर बादल", "ja": "ほぼ曇り", "ar": "غائم في الغالب", "id": "Kebanyakan Berawan"},
        "overcast": {"en": "Overcast", "it": "Coperto", "fr": "Couvert", "de": "Bedeckt", "es": "Nublado", "pt": "Encoberto", "ru": "Сплошная облачность", "zh_cn": "阴天", "hi": "बादलों से ढका", "ja": "曇天", "ar": "غائم تماماً", "id": "Mendung"}
    }
}