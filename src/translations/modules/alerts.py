"""
Alerts and notifications translations for MeteoApp.
Contains all text related to weather alerts, warnings, and notification systems.
"""

ALERTS_TRANSLATIONS = {
    "weather_alerts": {
        "alerts_title": {
            "en": "Weather Alerts", "it": "Avvisi meteo", "fr": "Alertes météo", "de": "Wetterwarnungen", 
            "es": "Alertas meteorológicas", "pt": "Alertas meteorológicos", "ru": "Метеооповещения", "zh_cn": "天气警报", 
            "hi": "मौसम अलर्ट", "ja": "天気警報", "ar": "تنبيهات الطقس", "id": "Peringatan Cuaca"
        },
        "severe_weather": {
            "en": "Severe Weather", "it": "Maltempo severo", "fr": "Temps sévère", "de": "Unwetter", 
            "es": "Tiempo severo", "pt": "Tempo severo", "ru": "Суровая погода", "zh_cn": "恶劣天气", 
            "hi": "कठोर मौसम", "ja": "悪天候", "ar": "طقس قاس", "id": "Cuaca Buruk"
        },
        "storm_warning": {
            "en": "Storm Warning", "it": "Avviso di tempesta", "fr": "Avertissement de tempête", "de": "Sturmwarnung", 
            "es": "Aviso de tormenta", "pt": "Aviso de tempestade", "ru": "Штормовое предупреждение", "zh_cn": "风暴警告", 
            "hi": "तूफान चेतावनी", "ja": "嵐警報", "ar": "تحذير من العاصفة", "id": "Peringatan Badai"
        },
        "heavy_rain": {
            "en": "Heavy Rain", "it": "Pioggia intensa", "fr": "Pluie forte", "de": "Starkregen", 
            "es": "Lluvia intensa", "pt": "Chuva forte", "ru": "Сильный дождь", "zh_cn": "大雨", 
            "hi": "भारी बारिश", "ja": "大雨", "ar": "أمطار غزيرة", "id": "Hujan Deras"
        },
        "snow_alert": {
            "en": "Snow Alert", "it": "Allerta neve", "fr": "Alerte neige", "de": "Schneewarnung", 
            "es": "Alerta de nieve", "pt": "Alerta de neve", "ru": "Снежное предупреждение", "zh_cn": "雪警", 
            "hi": "बर्फ चेतावनी", "ja": "雪警報", "ar": "تنبيه ثلج", "id": "Peringatan Salju"
        },
        "heat_wave": {
            "en": "Heat Wave", "it": "Ondata di calore", "fr": "Vague de chaleur", "de": "Hitzewelle", 
            "es": "Ola de calor", "pt": "Onda de calor", "ru": "Волна жары", "zh_cn": "热浪", 
            "hi": "गर्मी की लहर", "ja": "熱波", "ar": "موجة حر", "id": "Gelombang Panas"
        },
        "cold_snap": {
            "en": "Cold Snap", "it": "Ondata di freddo", "fr": "Vague de froid", "de": "Kältewelle", 
            "es": "Ola de frío", "pt": "Onda de frio", "ru": "Волна холода", "zh_cn": "寒潮", 
            "hi": "ठंड की लहर", "ja": "寒波", "ar": "موجة برد", "id": "Gelombang Dingin"
        },
        "high_winds": {
            "en": "High Winds", "it": "Venti forti", "fr": "Vents forts", "de": "Starke Winde", 
            "es": "Vientos fuertes", "pt": "Ventos fortes", "ru": "Сильные ветры", "zh_cn": "大风", 
            "hi": "तेज़ हवाएं", "ja": "強風", "ar": "رياح قوية", "id": "Angin Kencang"
        },
        "fog_advisory": {
            "en": "Fog Advisory", "it": "Avviso nebbia", "fr": "Avis de brouillard", "de": "Nebelwarnung", 
            "es": "Aviso de niebla", "pt": "Aviso de neblina", "ru": "Предупреждение о тумане", "zh_cn": "雾警", 
            "hi": "कोहरा चेतावनी", "ja": "霧注意報", "ar": "تنبيه ضباب", "id": "Peringatan Kabut"
        }
    },
    
    "alert_severity": {
        "minor": {
            "en": "Minor", "it": "Minore", "fr": "Mineur", "de": "Gering", 
            "es": "Menor", "pt": "Menor", "ru": "Незначительная", "zh_cn": "轻微", 
            "hi": "मामूली", "ja": "軽微", "ar": "طفيف", "id": "Ringan"
        },
        "moderate": {
            "en": "Moderate", "it": "Moderata", "fr": "Modérée", "de": "Mäßig", 
            "es": "Moderada", "pt": "Moderada", "ru": "Умеренная", "zh_cn": "中等", 
            "hi": "मध्यम", "ja": "中程度", "ar": "معتدل", "id": "Sedang"
        },
        "severe": {
            "en": "Severe", "it": "Severa", "fr": "Sévère", "de": "Schwer", 
            "es": "Severa", "pt": "Severa", "ru": "Серьёзная", "zh_cn": "严重", 
            "hi": "गंभीर", "ja": "深刻", "ar": "شديد", "id": "Parah"
        },
        "extreme": {
            "en": "Extreme", "it": "Estrema", "fr": "Extrême", "de": "Extrem", 
            "es": "Extrema", "pt": "Extrema", "ru": "Экстремальная", "zh_cn": "极端", 
            "hi": "चरम", "ja": "極端", "ar": "متطرف", "id": "Ekstrem"
        }
    },
    
    "notification_types": {
        "push_notification": {
            "en": "Push Notification", "it": "Notifica push", "fr": "Notification push", "de": "Push-Benachrichtigung", 
            "es": "Notificación push", "pt": "Notificação push", "ru": "Push-уведомление", "zh_cn": "推送通知", 
            "hi": "पुश नोटिफिकेशन", "ja": "プッシュ通知", "ar": "إشعار فوري", "id": "Notifikasi Push"
        },
        "email_alert": {
            "en": "Email Alert", "it": "Avviso email", "fr": "Alerte email", "de": "E-Mail-Warnung", 
            "es": "Alerta por email", "pt": "Alerta por email", "ru": "Email-оповещение", "zh_cn": "邮件警报", 
            "hi": "ईमेल अलर्ट", "ja": "メール警報", "ar": "تنبيه بريد إلكتروني", "id": "Peringatan Email"
        },
        "sms_alert": {
            "en": "SMS Alert", "it": "Avviso SMS", "fr": "Alerte SMS", "de": "SMS-Warnung", 
            "es": "Alerta SMS", "pt": "Alerta SMS", "ru": "SMS-оповещение", "zh_cn": "短信警报", 
            "hi": "एसएमएस अलर्ट", "ja": "SMS警報", "ar": "تنبيه رسالة نصية", "id": "Peringatan SMS"
        },
        "in_app_notification": {
            "en": "In-App Notification", "it": "Notifica in-app", "fr": "Notification dans l'app", "de": "In-App-Benachrichtigung", 
            "es": "Notificación en la app", "pt": "Notificação no app", "ru": "Уведомление в приложении", "zh_cn": "应用内通知", 
            "hi": "ऐप में नोटिफिकेशन", "ja": "アプリ内通知", "ar": "إشعار داخل التطبيق", "id": "Notifikasi Dalam Aplikasi"
        }
    },
    
    "alert_actions": {
        "acknowledge": {
            "en": "Acknowledge", "it": "Conferma", "fr": "Acquitter", "de": "Bestätigen", 
            "es": "Confirmar", "pt": "Confirmar", "ru": "Подтвердить", "zh_cn": "确认", 
            "hi": "स्वीकार करें", "ja": "確認", "ar": "إقرار", "id": "Akui"
        },
        "dismiss": {
            "en": "Dismiss", "it": "Ignora", "fr": "Ignorer", "de": "Verwerfen", 
            "es": "Descartar", "pt": "Dispensar", "ru": "Отклонить", "zh_cn": "忽略", 
            "hi": "खारिज करें", "ja": "却下", "ar": "رفض", "id": "Abaikan"
        },
        "view_details": {
            "en": "View Details", "it": "Visualizza dettagli", "fr": "Voir les détails", "de": "Details anzeigen", 
            "es": "Ver detalles", "pt": "Ver detalhes", "ru": "Показать детали", "zh_cn": "查看详情", 
            "hi": "विवरण देखें", "ja": "詳細を見る", "ar": "عرض التفاصيل", "id": "Lihat Detail"
        },
        "share_alert": {
            "en": "Share Alert", "it": "Condividi avviso", "fr": "Partager l'alerte", "de": "Warnung teilen", 
            "es": "Compartir alerta", "pt": "Compartilhar alerta", "ru": "Поделиться оповещением", "zh_cn": "分享警报", 
            "hi": "अलर्ट साझा करें", "ja": "警報を共有", "ar": "مشاركة التنبيه", "id": "Bagikan Peringatan"
        }
    }
}
