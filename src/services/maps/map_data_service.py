"""
Map Data Service for MeteoApp.
Handles weather map data fetching and processing.
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional
from datetime import datetime


class MapDataService:
    """Service for fetching and processing weather map data."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "demo_key"  # Replace with actual API key
        self.base_urls = {
            'openweather': 'https://api.openweathermap.org/data/2.5',
            'tiles': 'https://tile.openweathermap.org/map'
        }
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    async def get_weather_tiles(self, layer: str, zoom: int, x: int, y: int) -> Optional[bytes]:
        """Get weather map tiles for a specific layer."""
        url = f"{self.base_urls['tiles']}/{layer}/{zoom}/{x}/{y}.png"
        params = {'appid': self.api_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.read()
        except Exception as e:
            print(f"Error fetching tile: {e}")
        
        return None
    
    async def get_current_weather_data(self, lat: float, lon: float) -> Optional[Dict]:
        """Get current weather data for map overlay."""
        cache_key = f"weather_{lat}_{lon}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_duration:
                return cached_data
        
        url = f"{self.base_urls['openweather']}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Cache the result
                        self.cache[cache_key] = (data, datetime.now())
                        return data
        except Exception as e:
            print(f"Error fetching weather data: {e}")
        
        return None
    
    def get_layer_config(self, layer_type: str) -> Dict:
        """Get configuration for a specific map layer."""
        configs = {
            'precipitation': {
                'name': 'Precipitazioni',
                'color_scale': ['#00000000', '#0000FF', '#00FF00', '#FFFF00', '#FF0000'],
                'units': 'mm/h',
                'opacity': 0.8
            },
            'clouds': {
                'name': 'Nuvole',
                'color_scale': ['#00000000', '#FFFFFF'],
                'units': '%',
                'opacity': 0.6
            },
            'temperature': {
                'name': 'Temperatura',
                'color_scale': ['#0000FF', '#00FF00', '#FFFF00', '#FF0000'],
                'units': '°C',
                'opacity': 0.7
            },
            'wind': {
                'name': 'Vento',
                'color_scale': ['#00000000', '#0000FF', '#00FF00', '#FFFF00', '#FF0000'],
                'units': 'm/s',
                'opacity': 0.8
            },
            'pressure': {
                'name': 'Pressione',
                'color_scale': ['#0000FF', '#00FF00', '#FFFF00', '#FF0000'],
                'units': 'hPa',
                'opacity': 0.7
            }
        }
        
        return configs.get(layer_type, {})
    
    def clear_cache(self):
        """Clear the data cache."""
        self.cache.clear()
    
    def set_api_key(self, api_key: str):
        """Set the API key for weather data services."""
        self.api_key = api_key
