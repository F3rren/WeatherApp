"""
Weather Alerts Service for MeteoApp.
Handles weather alerts, notifications, and alert management.
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Any
from enum import Enum
import flet as ft

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Severity levels for weather alerts."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    EXTREME = "extreme"

class AlertType(Enum):
    """Types of weather alerts."""
    TEMPERATURE_HIGH = "temperature_high"
    TEMPERATURE_LOW = "temperature_low"
    RAIN_HEAVY = "rain_heavy"
    SNOW_HEAVY = "snow_heavy"
    WIND_STRONG = "wind_strong"
    STORM = "storm"
    FOG = "fog"
    UV_HIGH = "uv_high"
    AIR_QUALITY_POOR = "air_quality_poor"
    HUMIDITY_HIGH = "humidity_high"
    PRESSURE_LOW = "pressure_low"

class WeatherAlert:
    """Represents a weather alert."""
    
    def __init__(self, alert_type: AlertType, severity: AlertSeverity, 
                 title: str, message: str, value: float = None, 
                 threshold: float = None, unit: str = None,
                 expires_at: datetime = None):
        self.alert_type = alert_type
        self.severity = severity
        self.title = title
        self.message = message
        self.value = value
        self.threshold = threshold
        self.unit = unit
        self.created_at = datetime.now()
        self.expires_at = expires_at or (datetime.now() + timedelta(hours=6))
        self.id = f"{alert_type.value}_{int(self.created_at.timestamp())}"
        self.acknowledged = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary."""
        return {
            'id': self.id,
            'type': self.alert_type.value,
            'severity': self.severity.value,
            'title': self.title,
            'message': self.message,
            'value': self.value,
            'threshold': self.threshold,
            'unit': self.unit,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'acknowledged': self.acknowledged
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WeatherAlert':
        """Create alert from dictionary."""
        alert = cls(
            alert_type=AlertType(data['type']),
            severity=AlertSeverity(data['severity']),
            title=data['title'],
            message=data['message'],
            value=data.get('value'),
            threshold=data.get('threshold'),
            unit=data.get('unit'),
            expires_at=datetime.fromisoformat(data['expires_at'])
        )
        alert.id = data['id']
        alert.created_at = datetime.fromisoformat(data['created_at'])
        alert.acknowledged = data.get('acknowledged', False)
        return alert

    def is_active(self) -> bool:
        """Check if alert is still active."""
        return datetime.now() < self.expires_at and not self.acknowledged

class WeatherAlertsService:
    """Service for managing weather alerts and notifications."""
    
    def __init__(self, page: ft.Page, settings_service=None, translation_service=None):
        self.page = page
        self.settings_service = settings_service
        self.translation_service = translation_service
        
        # Alert configuration
        self.alert_thresholds = self._load_default_thresholds()
        self.enabled_alerts = set()
        # Alert storage
        self.active_alerts: Dict[str, WeatherAlert] = {}
        
        # Notification callbacks
        self.notification_callbacks: List[Callable] = []
        
        # Load user preferences
        self._load_alert_preferences()
        
        logger.info("Weather Alerts Service initialized")

    def _load_default_thresholds(self) -> Dict[AlertType, Dict[str, Any]]:
        """Load default alert thresholds."""
        return {
            AlertType.TEMPERATURE_HIGH: {
                'threshold': 25.0,  # °C (lowered for testing)
                'enabled': True,
                'severity': AlertSeverity.MODERATE
            },
            AlertType.TEMPERATURE_LOW: {
                'threshold': 5.0,  # °C (raised for testing)
                'enabled': True,
                'severity': AlertSeverity.MODERATE
            },
            AlertType.RAIN_HEAVY: {
                'threshold': 2.0,  # mm/h (lowered for testing)
                'enabled': True,
                'severity': AlertSeverity.HIGH
            },
            AlertType.WIND_STRONG: {
                'threshold': 20.0,  # km/h (lowered for testing)
                'enabled': True,
                'severity': AlertSeverity.HIGH
            },
            AlertType.UV_HIGH: {
                'threshold': 5.0,  # UV Index (lowered for testing)
                'enabled': True,
                'severity': AlertSeverity.MODERATE
            },
            AlertType.AIR_QUALITY_POOR: {
                'threshold': 50.0,  # AQI (lowered for testing)
                'enabled': True,
                'severity': AlertSeverity.HIGH
            },
            AlertType.STORM: {
                'threshold': 1.0,  # Boolean-like
                'enabled': True,
                'severity': AlertSeverity.EXTREME
            }
        }

    def _load_alert_preferences(self):
        """Load user alert preferences from settings."""
        if self.settings_service:
            # Load enabled alerts - if no settings exist, enable all by default
            enabled_alerts = self.settings_service.get_setting('enabled_alerts', None)
            if enabled_alerts is None:
                # First time - enable all alerts by default
                self.enabled_alerts = set(self.alert_thresholds.keys())
                logger.info("First time loading alerts - enabling all alerts by default")
            else:
                self.enabled_alerts = set(AlertType(alert) for alert in enabled_alerts if alert in [t.value for t in AlertType])
                logger.info(f"Loaded enabled alerts from settings: {[a.value for a in self.enabled_alerts]}")
            
            # Load custom thresholds
            custom_thresholds = self.settings_service.get_setting('alert_thresholds', {})
            for alert_type_str, config in custom_thresholds.items():
                try:
                    alert_type = AlertType(alert_type_str)
                    if alert_type in self.alert_thresholds:
                        self.alert_thresholds[alert_type].update(config)
                except ValueError:
                    continue
        else:
            # Default to all alerts enabled
            self.enabled_alerts = set(self.alert_thresholds.keys())
        
        # Update the enabled status in thresholds config
        for alert_type in self.alert_thresholds:
            self.alert_thresholds[alert_type]['enabled'] = alert_type in self.enabled_alerts
        
        # Save preferences to ensure they persist
        self.save_alert_preferences()

    def save_alert_preferences(self):
        """Save alert preferences to settings."""
        if self.settings_service:
            # Save enabled alerts
            enabled_list = [alert.value for alert in self.enabled_alerts]
            self.settings_service.set_setting('enabled_alerts', enabled_list)
            
            # Save custom thresholds
            threshold_dict = {}
            for alert_type, config in self.alert_thresholds.items():
                threshold_dict[alert_type.value] = config
            self.settings_service.set_setting('alert_thresholds', threshold_dict)

    def register_notification_callback(self, callback: Callable):
        """Register a callback for when alerts are triggered."""
        if callback not in self.notification_callbacks:
            self.notification_callbacks.append(callback)

    def unregister_notification_callback(self, callback: Callable):
        """Unregister a notification callback."""
        if callback in self.notification_callbacks:
            self.notification_callbacks.remove(callback)

    async def check_weather_conditions(self, weather_data: Dict[str, Any], 
                                     forecast_data: Dict[str, Any] = None) -> List[WeatherAlert]:
        """Check weather conditions and generate alerts."""
        new_alerts = []
        
        if not weather_data:
            return new_alerts

        try:
            # Check current conditions
            current_alerts = await self._check_current_conditions(weather_data)
            new_alerts.extend(current_alerts)
            
            # Check forecast conditions if available
            if forecast_data:
                forecast_alerts = await self._check_forecast_conditions(forecast_data)
                new_alerts.extend(forecast_alerts)
            
            # Add new alerts to active list
            for alert in new_alerts:
                if not self._is_duplicate_alert(alert):
                    self.active_alerts[alert.id] = alert
                    await self._trigger_notification(alert)
            
            # Clean expired alerts
            self._clean_expired_alerts()
            
            logger.info(f"Generated {len(new_alerts)} new weather alerts")
            
        except Exception as e:
            logger.error(f"Error checking weather conditions for alerts: {e}")
        
        return new_alerts

    async def _check_current_conditions(self, weather_data: Dict[str, Any]) -> List[WeatherAlert]:
        """Check current weather conditions for alerts."""
        alerts = []
        
        try:
            # Temperature alerts
            if 'temperature' in weather_data:
                temp = weather_data['temperature']
                alerts.extend(self._check_temperature_alerts(temp))
            
            # Wind alerts
            if 'wind_speed' in weather_data:
                wind_speed = weather_data['wind_speed']
                alerts.extend(self._check_wind_alerts(wind_speed))
            
            # UV Index alerts
            if 'uv_index' in weather_data:
                uv = weather_data['uv_index']
                alerts.extend(self._check_uv_alerts(uv))
            
            # Air quality alerts
            if 'air_quality' in weather_data:
                aqi = weather_data['air_quality'].get('aqi', 0)
                alerts.extend(self._check_air_quality_alerts(aqi))
            
            # Precipitation alerts
            if 'precipitation' in weather_data:
                precip = weather_data['precipitation']
                alerts.extend(self._check_precipitation_alerts(precip))
            
        except Exception as e:
            logger.error(f"Error checking current conditions: {e}")
        
        return alerts

    async def _check_forecast_conditions(self, forecast_data: Dict[str, Any]) -> List[WeatherAlert]:
        """Check forecast conditions for upcoming alerts."""
        alerts = []
        
        try:
            # Check next 24 hours for significant weather events
            if 'hourly' in forecast_data:
                hourly_data = forecast_data['hourly'][:24]  # Next 24 hours
                
                for hour_data in hourly_data:
                    # Check for storm conditions
                    if 'weather_condition' in hour_data:
                        condition = hour_data['weather_condition'].lower()
                        if any(word in condition for word in ['storm', 'thunder', 'severe']):
                            alerts.extend(self._check_storm_alerts(hour_data))
                    
                    # Check for heavy precipitation forecast
                    if 'precipitation' in hour_data:
                        precip = hour_data['precipitation']
                        if precip > self.alert_thresholds[AlertType.RAIN_HEAVY]['threshold']:
                            alerts.extend(self._check_precipitation_alerts(precip, is_forecast=True))
                            
        except Exception as e:
            logger.error(f"Error checking forecast conditions: {e}")
        
        return alerts

    def _check_temperature_alerts(self, temperature: float) -> List[WeatherAlert]:
        """Check for temperature-based alerts."""
        alerts = []
        
        # High temperature alert
        if (AlertType.TEMPERATURE_HIGH in self.enabled_alerts and 
            temperature > self.alert_thresholds[AlertType.TEMPERATURE_HIGH]['threshold']):
            
            title = self._get_alert_title(AlertType.TEMPERATURE_HIGH)
            message = self._get_alert_message(AlertType.TEMPERATURE_HIGH, temperature)
            
            alert = WeatherAlert(
                alert_type=AlertType.TEMPERATURE_HIGH,
                severity=self.alert_thresholds[AlertType.TEMPERATURE_HIGH]['severity'],
                title=title,
                message=message,
                value=temperature,
                threshold=self.alert_thresholds[AlertType.TEMPERATURE_HIGH]['threshold'],
                unit="°C"
            )
            alerts.append(alert)
        
        # Low temperature alert
        if (AlertType.TEMPERATURE_LOW in self.enabled_alerts and 
            temperature < self.alert_thresholds[AlertType.TEMPERATURE_LOW]['threshold']):
            
            title = self._get_alert_title(AlertType.TEMPERATURE_LOW)
            message = self._get_alert_message(AlertType.TEMPERATURE_LOW, temperature)
            
            alert = WeatherAlert(
                alert_type=AlertType.TEMPERATURE_LOW,
                severity=self.alert_thresholds[AlertType.TEMPERATURE_LOW]['severity'],
                title=title,
                message=message,
                value=temperature,
                threshold=self.alert_thresholds[AlertType.TEMPERATURE_LOW]['threshold'],
                unit="°C"
            )
            alerts.append(alert)
        
        return alerts

    def _check_wind_alerts(self, wind_speed: float) -> List[WeatherAlert]:
        """Check for wind-based alerts."""
        alerts = []
        
        if (AlertType.WIND_STRONG in self.enabled_alerts and 
            wind_speed > self.alert_thresholds[AlertType.WIND_STRONG]['threshold']):
            
            title = self._get_alert_title(AlertType.WIND_STRONG)
            message = self._get_alert_message(AlertType.WIND_STRONG, wind_speed)
            
            alert = WeatherAlert(
                alert_type=AlertType.WIND_STRONG,
                severity=self.alert_thresholds[AlertType.WIND_STRONG]['severity'],
                title=title,
                message=message,
                value=wind_speed,
                threshold=self.alert_thresholds[AlertType.WIND_STRONG]['threshold'],
                unit="km/h"
            )
            alerts.append(alert)
        
        return alerts

    def _check_uv_alerts(self, uv_index: float) -> List[WeatherAlert]:
        """Check for UV index alerts."""
        alerts = []
        
        if (AlertType.UV_HIGH in self.enabled_alerts and 
            uv_index > self.alert_thresholds[AlertType.UV_HIGH]['threshold']):
            
            title = self._get_alert_title(AlertType.UV_HIGH)
            message = self._get_alert_message(AlertType.UV_HIGH, uv_index)
            
            alert = WeatherAlert(
                alert_type=AlertType.UV_HIGH,
                severity=self.alert_thresholds[AlertType.UV_HIGH]['severity'],
                title=title,
                message=message,
                value=uv_index,
                threshold=self.alert_thresholds[AlertType.UV_HIGH]['threshold'],
                unit="UV"
            )
            alerts.append(alert)
        
        return alerts

    def _check_air_quality_alerts(self, aqi: float) -> List[WeatherAlert]:
        """Check for air quality alerts."""
        alerts = []
        
        if (AlertType.AIR_QUALITY_POOR in self.enabled_alerts and 
            aqi > self.alert_thresholds[AlertType.AIR_QUALITY_POOR]['threshold']):
            
            title = self._get_alert_title(AlertType.AIR_QUALITY_POOR)
            message = self._get_alert_message(AlertType.AIR_QUALITY_POOR, aqi)
            
            alert = WeatherAlert(
                alert_type=AlertType.AIR_QUALITY_POOR,
                severity=self.alert_thresholds[AlertType.AIR_QUALITY_POOR]['severity'],
                title=title,
                message=message,
                value=aqi,
                threshold=self.alert_thresholds[AlertType.AIR_QUALITY_POOR]['threshold'],
                unit="AQI"
            )
            alerts.append(alert)
        
        return alerts

    def _check_precipitation_alerts(self, precipitation: float, is_forecast: bool = False) -> List[WeatherAlert]:
        """Check for precipitation alerts."""
        alerts = []
        
        if (AlertType.RAIN_HEAVY in self.enabled_alerts and 
            precipitation > self.alert_thresholds[AlertType.RAIN_HEAVY]['threshold']):
            
            title = self._get_alert_title(AlertType.RAIN_HEAVY, is_forecast)
            message = self._get_alert_message(AlertType.RAIN_HEAVY, precipitation, is_forecast)
            
            alert = WeatherAlert(
                alert_type=AlertType.RAIN_HEAVY,
                severity=self.alert_thresholds[AlertType.RAIN_HEAVY]['severity'],
                title=title,
                message=message,
                value=precipitation,
                threshold=self.alert_thresholds[AlertType.RAIN_HEAVY]['threshold'],
                unit="mm"
            )
            alerts.append(alert)
        
        return alerts

    def _check_storm_alerts(self, weather_data: Dict[str, Any]) -> List[WeatherAlert]:
        """Check for storm alerts."""
        alerts = []
        
        if AlertType.STORM in self.enabled_alerts:
            title = self._get_alert_title(AlertType.STORM, True)
            message = self._get_alert_message(AlertType.STORM, 1.0, True)
            
            alert = WeatherAlert(
                alert_type=AlertType.STORM,
                severity=AlertSeverity.EXTREME,
                title=title,
                message=message,
                expires_at=datetime.now() + timedelta(hours=12)
            )
            alerts.append(alert)
        
        return alerts

    def _get_alert_title(self, alert_type: AlertType, is_forecast: bool = False) -> str:
        """Get localized alert title."""
        if self.translation_service:
            key = f"alert_{alert_type.value}_title"
            if is_forecast:
                key = f"alert_{alert_type.value}_forecast_title"
            return self.translation_service.translate(key)
        
        # Fallback titles
        titles = {
            AlertType.TEMPERATURE_HIGH: "High Temperature Alert" if not is_forecast else "High Temperature Forecast",
            AlertType.TEMPERATURE_LOW: "Low Temperature Alert" if not is_forecast else "Low Temperature Forecast",
            AlertType.RAIN_HEAVY: "Heavy Rain Alert" if not is_forecast else "Heavy Rain Expected",
            AlertType.WIND_STRONG: "Strong Wind Alert" if not is_forecast else "Strong Wind Expected",
            AlertType.UV_HIGH: "High UV Index Alert",
            AlertType.AIR_QUALITY_POOR: "Poor Air Quality Alert",
            AlertType.STORM: "Storm Alert" if not is_forecast else "Storm Warning"
        }
        return titles.get(alert_type, "Weather Alert")

    def _get_alert_message(self, alert_type: AlertType, value: float, is_forecast: bool = False) -> str:
        """Get localized alert message."""
        if self.translation_service:
            key = f"alert_{alert_type.value}_message"
            return self.translation_service.translate(key, value=value)
        
        # Fallback messages
        if alert_type == AlertType.TEMPERATURE_HIGH:
            return f"Temperature has reached {value:.1f}°C. Stay hydrated and avoid prolonged sun exposure."
        elif alert_type == AlertType.TEMPERATURE_LOW:
            return f"Temperature has dropped to {value:.1f}°C. Dress warmly and be careful of icy conditions."
        elif alert_type == AlertType.RAIN_HEAVY:
            prefix = "Heavy rain expected" if is_forecast else "Heavy rain detected"
            return f"{prefix}: {value:.1f}mm. Avoid driving if possible and stay indoors."
        elif alert_type == AlertType.WIND_STRONG:
            return f"Strong winds detected: {value:.1f}km/h. Secure loose objects and avoid outdoor activities."
        elif alert_type == AlertType.UV_HIGH:
            return f"UV Index is high: {value:.1f}. Use sunscreen and limit sun exposure."
        elif alert_type == AlertType.AIR_QUALITY_POOR:
            return f"Air quality is poor (AQI: {value:.0f}). Limit outdoor activities."
        elif alert_type == AlertType.STORM:
            return "Severe weather conditions expected. Stay indoors and avoid travel."
        
        return f"Weather alert: {alert_type.value}"

    def _is_duplicate_alert(self, new_alert: WeatherAlert) -> bool:
        """Check if this alert is a duplicate of an existing active alert."""
        for existing_alert in self.active_alerts.values():
            if (existing_alert.alert_type == new_alert.alert_type and 
                existing_alert.is_active() and
                (datetime.now() - existing_alert.created_at).total_seconds() < 3600):  # Within 1 hour
                return True
        return False

    def _clean_expired_alerts(self):
        """Remove expired alerts from active list."""
        expired_ids = [alert_id for alert_id, alert in self.active_alerts.items() if not alert.is_active()]
        for alert_id in expired_ids:
            del self.active_alerts[alert_id]

    async def _trigger_notification(self, alert: WeatherAlert):
        """Trigger notification for an alert."""
        try:
            # Call registered callbacks
            for callback in self.notification_callbacks:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(alert)
                    else:
                        callback(alert)
                except Exception as e:
                    logger.error(f"Error in notification callback: {e}")
            
            # Show system notification if page is available
            if self.page:
                await self._show_page_notification(alert)
                
        except Exception as e:
            logger.error(f"Error triggering notification: {e}")

    async def _show_page_notification(self, alert: WeatherAlert):
        """Show notification in the page."""
        try:
            if hasattr(self.page, 'show_snack_bar'):
                # Get severity color
                color_map = {
                    AlertSeverity.LOW: ft.Colors.BLUE,
                    AlertSeverity.MODERATE: ft.Colors.ORANGE,
                    AlertSeverity.HIGH: ft.Colors.RED,
                    AlertSeverity.EXTREME: ft.Colors.PURPLE
                }
                
                snack_bar = ft.SnackBar(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.WARNING_ROUNDED,
                                color=color_map.get(alert.severity, ft.Colors.ORANGE),
                                size=20
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        alert.title,
                                        weight=ft.FontWeight.BOLD,
                                        size=14
                                    ),
                                    ft.Text(
                                        alert.message,
                                        size=12
                                    )
                                ],
                                spacing=2,
                                expand=True
                            )
                        ],
                        spacing=10
                    ),
                    bgcolor=ft.Colors.with_opacity(0.9, color_map.get(alert.severity, ft.Colors.ORANGE)),
                    duration=8000 if alert.severity in [AlertSeverity.HIGH, AlertSeverity.EXTREME] else 5000
                )
                
                self.page.show_snack_bar(snack_bar)
                
        except Exception as e:
            logger.error(f"Error showing page notification: {e}")

    def get_active_alerts(self) -> List[WeatherAlert]:
        """Get all currently active alerts."""
        self._clean_expired_alerts()
        return list(self.active_alerts.values())

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert by ID."""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].acknowledged = True
            logger.info(f"Alert acknowledged: {alert_id}")
            return True
        return False

    def update_alert_threshold(self, alert_type: AlertType, threshold: float, enabled: bool = None):
        """Update threshold for a specific alert type."""
        if alert_type in self.alert_thresholds:
            self.alert_thresholds[alert_type]['threshold'] = threshold
            if enabled is not None:
                self.alert_thresholds[alert_type]['enabled'] = enabled
                if enabled:
                    self.enabled_alerts.add(alert_type)
                else:
                    self.enabled_alerts.discard(alert_type)
            
            self.save_alert_preferences()
            logger.info(f"Updated threshold for {alert_type.value}: {threshold}")

    def toggle_alert_type(self, alert_type: AlertType, enabled: bool):
        """Enable or disable a specific alert type."""
        if enabled:
            self.enabled_alerts.add(alert_type)
        else:
            self.enabled_alerts.discard(alert_type)
        
        if alert_type in self.alert_thresholds:
            self.alert_thresholds[alert_type]['enabled'] = enabled
        
        self.save_alert_preferences()
        logger.info(f"Alert type {alert_type.value} {'enabled' if enabled else 'disabled'}")

    def get_alert_settings(self) -> Dict[str, Any]:
        """Get current alert settings."""
        return {
            'enabled_alerts': [alert.value for alert in self.enabled_alerts],
            'thresholds': {alert.value: config for alert, config in self.alert_thresholds.items()}
        }

    def cleanup(self):
        """Cleanup service resources."""
        self.notification_callbacks.clear()
        self.active_alerts.clear()
        logger.info("Weather Alerts Service cleaned up")

    async def check_real_weather_conditions(self, weather_data: Dict[str, Any], api_service=None) -> List[WeatherAlert]:
        """
        Check real weather data from API and generate alerts.
        
        Args:
            weather_data: Weather data from OpenWeatherMap API
            api_service: API service instance for extracting data
            
        Returns:
            List of generated alerts
        """
        if not weather_data or not api_service:
            logger.warning("No weather data or API service provided")
            return []
        
        new_alerts = []
        
        try:
            # Extract real weather values using API service methods
            current_temp = api_service.get_current_temperature(weather_data)
            wind_speed = api_service.get_wind_speed(weather_data)
            humidity = api_service.get_humidity(weather_data)
            pressure = api_service.get_pressure(weather_data)
            visibility = api_service.get_visibility(weather_data)
            
            # Extract precipitation data
            precipitation = 0.0
            try:
                if 'list' in weather_data and len(weather_data['list']) > 0:
                    first_item = weather_data['list'][0]
                    if 'rain' in first_item and '3h' in first_item['rain']:
                        precipitation = first_item['rain']['3h']
                    elif 'snow' in first_item and '3h' in first_item['snow']:
                        precipitation = first_item['snow']['3h']
            except (KeyError, TypeError):
                pass
            
            logger.info(f"Real weather data - Temp: {current_temp}°C, Wind: {wind_speed} km/h, "
                       f"Humidity: {humidity}%, Pressure: {pressure} hPa, "
                       f"Visibility: {visibility}m, Precipitation: {precipitation}mm")
            
            # Debug: Show thresholds and enabled alerts
            logger.info(f"Enabled alerts: {[alert.value for alert in self.enabled_alerts]}")
            for alert_type in [AlertType.TEMPERATURE_HIGH, AlertType.TEMPERATURE_LOW, AlertType.WIND_STRONG, AlertType.RAIN_HEAVY]:
                if alert_type in self.alert_thresholds:
                    threshold = self.alert_thresholds[alert_type]['threshold']
                    enabled = alert_type in self.enabled_alerts
                    logger.info(f"{alert_type.value}: threshold={threshold}, enabled={enabled}")
            
            # Check temperature alerts
            if current_temp is not None:
                logger.info(f"Checking temperature alerts for {current_temp}°C")
                
                if AlertType.TEMPERATURE_HIGH in self.enabled_alerts:
                    threshold = self.alert_thresholds[AlertType.TEMPERATURE_HIGH]['threshold']
                    logger.info(f"Temperature HIGH check: {current_temp} > {threshold} = {current_temp > threshold}")
                    if current_temp > threshold:
                        severity = self._get_temperature_severity(current_temp, threshold)
                        alert = WeatherAlert(
                            alert_type=AlertType.TEMPERATURE_HIGH,
                            severity=severity,
                            title="Temperatura Elevata Rilevata",
                            message=f"La temperatura attuale di {current_temp}°C supera la soglia di {threshold}°C. Prestare attenzione agli sforzi fisici all'aperto.",
                            value=current_temp,
                            threshold=threshold,
                            unit="°C"
                        )
                        new_alerts.append(alert)
                        logger.info(f"Generated HIGH temperature alert: {current_temp}°C > {threshold}°C")
                
                if AlertType.TEMPERATURE_LOW in self.enabled_alerts:
                    threshold = self.alert_thresholds[AlertType.TEMPERATURE_LOW]['threshold']
                    logger.info(f"Temperature LOW check: {current_temp} < {threshold} = {current_temp < threshold}")
                    if current_temp < threshold:
                        severity = self._get_cold_severity(current_temp, threshold)
                        alert = WeatherAlert(
                            alert_type=AlertType.TEMPERATURE_LOW,
                            severity=severity,
                            title="Temperatura Bassa Rilevata",
                            message=f"La temperatura attuale di {current_temp}°C è scesa sotto la soglia di {threshold}°C. Vestirsi adeguatamente.",
                            value=current_temp,
                            threshold=threshold,
                            unit="°C"
                        )
                        new_alerts.append(alert)
                        logger.info(f"Generated LOW temperature alert: {current_temp}°C < {threshold}°C")
            
            # Check wind alerts
            if wind_speed is not None and AlertType.WIND_STRONG in self.enabled_alerts:
                threshold = self.alert_thresholds[AlertType.WIND_STRONG]['threshold']
                logger.info(f"Wind check: {wind_speed} > {threshold} = {wind_speed > threshold}")
                if wind_speed > threshold:
                    severity = self._get_wind_severity(wind_speed, threshold)
                    alert = WeatherAlert(
                        alert_type=AlertType.WIND_STRONG,
                        severity=severity,
                        title="Vento Forte Rilevato",
                        message=f"Velocità del vento attuale: {wind_speed} km/h (soglia: {threshold} km/h). Prestare attenzione negli spostamenti.",
                        value=wind_speed,
                        threshold=threshold,
                        unit="km/h"
                    )
                    new_alerts.append(alert)
                    logger.info(f"Generated wind alert: {wind_speed} km/h > {threshold} km/h")
            
            # Check precipitation alerts
            if precipitation > 0 and AlertType.RAIN_HEAVY in self.enabled_alerts:
                threshold = self.alert_thresholds[AlertType.RAIN_HEAVY]['threshold']
                logger.info(f"Precipitation check: {precipitation} > {threshold} = {precipitation > threshold}")
                if precipitation > threshold:
                    severity = self._get_precipitation_severity(precipitation, threshold)
                    alert = WeatherAlert(
                        alert_type=AlertType.RAIN_HEAVY,
                        severity=severity,
                        title="Precipitazioni Intense",
                        message=f"Precipitazioni rilevate: {precipitation:.1f}mm (soglia: {threshold}mm). Guidare con prudenza.",
                        value=precipitation,
                        threshold=threshold,
                        unit="mm"
                    )
                    new_alerts.append(alert)
                    logger.info(f"Generated precipitation alert: {precipitation}mm > {threshold}mm")
            
            # Check visibility alerts (poor air quality approximation)
            if visibility is not None and AlertType.AIR_QUALITY_POOR in self.enabled_alerts:
                # Convert visibility to a pseudo AQI (lower visibility = higher AQI)
                pseudo_aqi = max(0, 200 - (visibility / 50))  # Rough approximation
                threshold = self.alert_thresholds[AlertType.AIR_QUALITY_POOR]['threshold']
                
                logger.info(f"Visibility check: visibility={visibility}m, pseudo_aqi={pseudo_aqi}, threshold={threshold}")
                logger.info(f"Visibility conditions: pseudo_aqi > threshold = {pseudo_aqi > threshold}, visibility < 1000 = {visibility < 1000}")
                
                if pseudo_aqi > threshold or visibility < 1000:  # Less than 1km visibility
                    severity = AlertSeverity.MODERATE if visibility > 500 else AlertSeverity.HIGH
                    alert = WeatherAlert(
                        alert_type=AlertType.AIR_QUALITY_POOR,
                        severity=severity,
                        title="Visibilità Ridotta",
                        message=f"Visibilità limitata: {visibility}m. Potrebbero esserci condizioni di scarsa qualità dell'aria.",
                        value=visibility,
                        threshold=1000,
                        unit="m"
                    )
                    new_alerts.append(alert)
                    logger.info(f"Generated visibility/air quality alert: visibility={visibility}m")
            
            # Add alerts to active alerts
            logger.info(f"Total new alerts generated: {len(new_alerts)}")
            for alert in new_alerts:
                if not self._is_duplicate_alert(alert):
                    self.active_alerts[alert.id] = alert
                    await self._trigger_notification(alert)
            
            # Clean expired alerts
            self._clean_expired_alerts()
            
            logger.info(f"Generated {len(new_alerts)} alerts from real weather data")
            return new_alerts
            
        except Exception as e:
            logger.error(f"Error checking real weather conditions: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def _get_temperature_severity(self, temp: float, threshold: float) -> AlertSeverity:
        """Determine severity based on how much temperature exceeds threshold."""
        excess = temp - threshold
        if excess < 5:
            return AlertSeverity.LOW
        elif excess < 10:
            return AlertSeverity.MODERATE
        elif excess < 15:
            return AlertSeverity.HIGH
        else:
            return AlertSeverity.EXTREME
    
    def _get_cold_severity(self, temp: float, threshold: float) -> AlertSeverity:
        """Determine severity based on how much temperature is below threshold."""
        deficit = threshold - temp
        if deficit < 5:
            return AlertSeverity.LOW
        elif deficit < 10:
            return AlertSeverity.MODERATE
        elif deficit < 15:
            return AlertSeverity.HIGH
        else:
            return AlertSeverity.EXTREME
    
    def _get_wind_severity(self, wind: float, threshold: float) -> AlertSeverity:
        """Determine severity based on wind speed."""
        excess = wind - threshold
        if excess < 10:
            return AlertSeverity.LOW
        elif excess < 20:
            return AlertSeverity.MODERATE
        elif excess < 40:
            return AlertSeverity.HIGH
        else:
            return AlertSeverity.EXTREME
    
    def _get_precipitation_severity(self, precip: float, threshold: float) -> AlertSeverity:
        """Determine severity based on precipitation amount."""
        excess = precip - threshold
        if excess < 5:
            return AlertSeverity.LOW
        elif excess < 15:
            return AlertSeverity.MODERATE
        elif excess < 30:
            return AlertSeverity.HIGH
        else:
            return AlertSeverity.EXTREME


