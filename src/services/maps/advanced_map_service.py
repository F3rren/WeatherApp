"""
Advanced Map Service for MeteoApp.
Handles multiple map providers, layers, and animations.
"""

import logging
import webbrowser
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

import flet as ft

# Map provider configurations
class MapProvider(Enum):
    WINDY = "windy"
    OPENWEATHERMAP = "openweathermap"
    METEOBLUE = "meteoblue"
    VENTUSKY = "ventusky"
    NULLSCHOOL = "nullschool"
    RAINVIEWER = "rainviewer"

class WeatherLayer(Enum):
    TEMPERATURE = "temp"
    PRECIPITATION = "rain"
    WIND = "wind"
    PRESSURE = "pressure"
    CLOUDS = "clouds"
    HUMIDITY = "humidity"
    RADAR = "radar"
    SATELLITE = "satellite"
    SATELLITE_VISIBLE = "satellite_visible"
    SATELLITE_INFRARED = "satellite_infrared"
    SATELLITE_WATER_VAPOR = "satellite_water_vapor"
    LIGHTNING = "lightning"
    UV_INDEX = "uvi"
    SNOW = "snow"
    WAVES = "waves"

@dataclass
class MapConfig:
    """Configuration for map display"""
    provider: MapProvider
    layer: WeatherLayer
    zoom: int = 10
    animation: bool = False
    time_range: int = 24  # hours
    auto_refresh: bool = False
    refresh_interval: int = 300  # seconds

class AdvancedMapService:
    """
    Advanced service for weather map functionality with multiple providers and layers.
    """
    
    def __init__(self, page: ft.Page, state_manager=None, translation_service=None):
        self.page = page
        self.state_manager = state_manager
        self.translation_service = translation_service
        self.logger = logging.getLogger(__name__)
        
        # Map providers and their capabilities
        self.provider_configs = {
            MapProvider.WINDY: {
                "base_url": "https://www.windy.com",
                "layers": {
                    WeatherLayer.TEMPERATURE: "temp",
                    WeatherLayer.PRECIPITATION: "rain",
                    WeatherLayer.WIND: "wind",
                    WeatherLayer.PRESSURE: "pressure",
                    WeatherLayer.CLOUDS: "clouds",
                    WeatherLayer.HUMIDITY: "rh",
                    WeatherLayer.RADAR: "radar",
                    WeatherLayer.SATELLITE: "satellite",
                    WeatherLayer.SATELLITE_VISIBLE: "satellite",
                    WeatherLayer.SATELLITE_INFRARED: "satellite",
                    WeatherLayer.SATELLITE_WATER_VAPOR: "satellite",
                    WeatherLayer.LIGHTNING: "lightning",
                    WeatherLayer.UV_INDEX: "uvi",
                    WeatherLayer.SNOW: "snow",
                    WeatherLayer.WAVES: "waves"
                },
                "supports_animation": True,
                "supports_forecast": True
            },
            MapProvider.OPENWEATHERMAP: {
                "base_url": "https://openweathermap.org/weathermap",
                "layers": {
                    WeatherLayer.TEMPERATURE: "temp_new",
                    WeatherLayer.PRECIPITATION: "precipitation_new",
                    WeatherLayer.WIND: "wind_new",
                    WeatherLayer.PRESSURE: "pressure_new",
                    WeatherLayer.CLOUDS: "clouds_new"
                },
                "supports_animation": False,
                "supports_forecast": True
            },
            MapProvider.METEOBLUE: {
                "base_url": "https://www.meteoblue.com/en/weather/maps",
                "layers": {
                    WeatherLayer.TEMPERATURE: "temperature",
                    WeatherLayer.PRECIPITATION: "precipitation",
                    WeatherLayer.WIND: "wind",
                    WeatherLayer.PRESSURE: "pressure"
                },
                "supports_animation": True,
                "supports_forecast": True
            },
            MapProvider.VENTUSKY: {
                "base_url": "https://www.ventusky.com",
                "layers": {
                    WeatherLayer.TEMPERATURE: "temperature",
                    WeatherLayer.PRECIPITATION: "rain",
                    WeatherLayer.WIND: "wind",
                    WeatherLayer.PRESSURE: "pressure",
                    WeatherLayer.CLOUDS: "clouds"
                },
                "supports_animation": True,
                "supports_forecast": True
            },
            MapProvider.NULLSCHOOL: {
                "base_url": "https://earth.nullschool.net",
                "layers": {
                    WeatherLayer.WIND: "wind",
                    WeatherLayer.TEMPERATURE: "temp",
                    WeatherLayer.HUMIDITY: "rh"
                },
                "supports_animation": True,
                "supports_forecast": False
            },
            MapProvider.RAINVIEWER: {
                "base_url": "https://www.rainviewer.com/map.html",
                "layers": {
                    WeatherLayer.PRECIPITATION: "rain",
                    WeatherLayer.RADAR: "radar"
                },
                "supports_animation": True,
                "supports_forecast": True
            }
        }
        
        # Current map configuration
        self.current_config = MapConfig(
            provider=MapProvider.WINDY,
            layer=WeatherLayer.TEMPERATURE
        )
        
        # Animation state
        self.animation_active = False
        self.animation_timer = None
        
    def get_available_layers(self, provider: MapProvider) -> List[WeatherLayer]:
        """Get available layers for a specific provider"""
        if provider in self.provider_configs:
            return list(self.provider_configs[provider]["layers"].keys())
        return []
    
    def get_available_providers(self) -> List[MapProvider]:
        """Get all available map providers"""
        return list(self.provider_configs.keys())
    
    def build_map_url(self, lat: float, lon: float, config: MapConfig) -> str:
        """Build URL for specific map configuration"""
        provider_config = self.provider_configs.get(config.provider)
        if not provider_config:
            return self._build_fallback_url(lat, lon)
        
        base_url = provider_config["base_url"]
        
        if config.provider == MapProvider.WINDY:
            layer_param = provider_config["layers"].get(config.layer, "temp")
            url = f"{base_url}/?{layer_param},{lat},{lon},{config.zoom}"
            if config.animation and provider_config["supports_animation"]:
                url += "&animate=true"
            return url
            
        elif config.provider == MapProvider.OPENWEATHERMAP:
            layer_param = provider_config["layers"].get(config.layer, "temp_new")
            return f"{base_url}?lat={lat}&lon={lon}&zoom={config.zoom}&layer={layer_param}"
            
        elif config.provider == MapProvider.METEOBLUE:
            layer_param = provider_config["layers"].get(config.layer, "temperature")
            return f"{base_url}/{layer_param}#{config.zoom}/{lat}/{lon}"
            
        elif config.provider == MapProvider.VENTUSKY:
            layer_param = provider_config["layers"].get(config.layer, "temperature")
            return f"{base_url}?p={lat};{lon};{config.zoom}&l={layer_param}"
            
        elif config.provider == MapProvider.NULLSCHOOL:
            layer_param = provider_config["layers"].get(config.layer, "wind")
            return f"{base_url}/#{config.zoom}/{lat}/{lon}/{layer_param}"
            
        elif config.provider == MapProvider.RAINVIEWER:
            return f"{base_url}?lat={lat}&lng={lon}&zoom={config.zoom}"
        
        return self._build_fallback_url(lat, lon)
    
    def _build_fallback_url(self, lat: float, lon: float) -> str:
        """Build fallback URL when provider is not supported"""
        return f"https://www.windy.com/?temp,{lat},{lon},10"
    
    def open_map(self, lat: float, lon: float, config: Optional[MapConfig] = None) -> bool:
        """Open map with specified configuration"""
        try:
            if config:
                self.current_config = config
            
            url = self.build_map_url(lat, lon, self.current_config)
            self.logger.info(f"Opening map: {url}")
            
            webbrowser.open(url)
            return True
            
        except Exception as e:
            self.logger.error(f"Error opening map: {e}")
            return False
    
    def get_provider_name(self, provider: MapProvider) -> str:
        """Get human-readable provider name"""
        provider_names = {
            MapProvider.WINDY: "Windy",
            MapProvider.OPENWEATHERMAP: "OpenWeatherMap",
            MapProvider.METEOBLUE: "MeteoBlue",
            MapProvider.VENTUSKY: "Ventusky",
            MapProvider.NULLSCHOOL: "Earth Nullschool",
            MapProvider.RAINVIEWER: "RainViewer"
        }
        return provider_names.get(provider, provider.value.title())
    
    def get_layer_name(self, layer: WeatherLayer) -> str:
        """Get human-readable layer name"""
        # This should use translation service in real implementation
        layer_names = {
            WeatherLayer.TEMPERATURE: "Temperature",
            WeatherLayer.PRECIPITATION: "Precipitation",
            WeatherLayer.WIND: "Wind",
            WeatherLayer.PRESSURE: "Pressure",
            WeatherLayer.CLOUDS: "Clouds",
            WeatherLayer.HUMIDITY: "Humidity",
            WeatherLayer.RADAR: "Radar",
            WeatherLayer.SATELLITE: "Satellite",
            WeatherLayer.LIGHTNING: "Lightning",
            WeatherLayer.UV_INDEX: "UV Index",
            WeatherLayer.SNOW: "Snow",
            WeatherLayer.WAVES: "Waves"
        }
        return layer_names.get(layer, layer.value.title())
    
    def supports_animation(self, provider: MapProvider) -> bool:
        """Check if provider supports animation"""
        return self.provider_configs.get(provider, {}).get("supports_animation", False)
    
    def supports_forecast(self, provider: MapProvider) -> bool:
        """Check if provider supports forecast data"""
        return self.provider_configs.get(provider, {}).get("supports_forecast", False)
    
    async def start_animation_cycle(self, lat: float, lon: float, duration_hours: int = 24):
        """Start animated weather cycle (for demo purposes)"""
        if self.animation_active:
            return
        
        self.animation_active = True
        try:
            # This is a simplified animation - in reality you'd cycle through time periods
            providers = [MapProvider.WINDY, MapProvider.VENTUSKY, MapProvider.METEOBLUE]
            layers = [WeatherLayer.TEMPERATURE, WeatherLayer.PRECIPITATION, WeatherLayer.WIND]
            
            for i in range(duration_hours):
                if not self.animation_active:
                    break
                
                # Cycle through different configurations
                provider = providers[i % len(providers)]
                layer = layers[i % len(layers)]
                
                config = MapConfig(
                    provider=provider,
                    layer=layer,
                    animation=True
                )
                
                self.open_map(lat, lon, config)
                await asyncio.sleep(2)  # Wait 2 seconds between changes
                
        finally:
            self.animation_active = False
    
    def stop_animation_cycle(self):
        """Stop the animation cycle"""
        self.animation_active = False
        if self.animation_timer:
            self.animation_timer.cancel()
            self.animation_timer = None
    
    def get_comparison_urls(self, lat: float, lon: float, layer: WeatherLayer) -> Dict[str, str]:
        """Get URLs for the same layer across different providers for comparison"""
        urls = {}
        
        for provider in self.get_available_providers():
            if layer in self.get_available_layers(provider):
                config = MapConfig(provider=provider, layer=layer)
                urls[self.get_provider_name(provider)] = self.build_map_url(lat, lon, config)
        
        return urls
    
    def open_comparison_view(self, lat: float, lon: float, layer: WeatherLayer):
        """Open multiple maps for comparison"""
        comparison_urls = self.get_comparison_urls(lat, lon, layer)
        
        for provider_name, url in comparison_urls.items():
            self.logger.info(f"Opening {provider_name}: {url}")
            webbrowser.open(url)
            asyncio.sleep(0.5)  # Small delay between opening tabs
