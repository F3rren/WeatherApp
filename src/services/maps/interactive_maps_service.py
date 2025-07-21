"""
Interactive Maps Service for MeteoApp.
Handles interactive weather map functionality with layers and real-time data.
"""

import flet as ft
import webbrowser
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json


class MapLayer:
    """Represents a weather map layer."""
    
    def __init__(self, layer_id: str, name: str, description: str, 
                 provider: str, base_url: str, enabled: bool = True):
        self.layer_id = layer_id
        self.name = name
        self.description = description
        self.provider = provider
        self.base_url = base_url
        self.enabled = enabled
        self.opacity = 0.8
        self.animation_speed = 1.0


class InteractiveMapService:
    """Service for managing interactive weather maps with multiple layers."""
    
    def __init__(self, page: ft.Page = None, state_manager=None):
        self.page = page
        self.state_manager = state_manager
        self.current_location = None
        self.zoom_level = 10
        self.available_layers = self._initialize_layers()
        self.active_layers = []
        self.animation_enabled = True
        self.auto_refresh = True
        self.refresh_interval = 10  # minutes
        
    def _initialize_layers(self) -> Dict[str, MapLayer]:
        """Initialize available weather map layers."""
        layers = {
            'precipitation': MapLayer(
                'precipitation',
                'Precipitazioni',
                'Radar precipitazioni in tempo reale',
                'OpenWeatherMap',
                'https://tile.openweathermap.org/map/precipitation_new'
            ),
            'clouds': MapLayer(
                'clouds',
                'Nuvole',
                'Copertura nuvolosa',
                'OpenWeatherMap', 
                'https://tile.openweathermap.org/map/clouds_new'
            ),
            'temperature': MapLayer(
                'temperature',
                'Temperatura',
                'Temperatura superficiale',
                'OpenWeatherMap',
                'https://tile.openweathermap.org/map/temp_new'
            ),
            'wind': MapLayer(
                'wind',
                'Vento',
                'Velocità e direzione del vento',
                'OpenWeatherMap',
                'https://tile.openweathermap.org/map/wind_new'
            ),
            'pressure': MapLayer(
                'pressure',
                'Pressione',
                'Pressione atmosferica',
                'OpenWeatherMap',
                'https://tile.openweathermap.org/map/pressure_new'
            )
        }
        return layers
    
    def get_available_layers(self) -> List[MapLayer]:
        """Get list of available map layers."""
        return list(self.available_layers.values())
    
    def toggle_layer(self, layer_id: str) -> bool:
        """Toggle a map layer on/off."""
        if layer_id in self.available_layers:
            layer = self.available_layers[layer_id]
            layer.enabled = not layer.enabled
            
            if layer.enabled and layer not in self.active_layers:
                self.active_layers.append(layer)
            elif not layer.enabled and layer in self.active_layers:
                self.active_layers.remove(layer)
                
            return layer.enabled
        return False
    
    def set_layer_opacity(self, layer_id: str, opacity: float):
        """Set opacity for a specific layer."""
        if layer_id in self.available_layers:
            self.available_layers[layer_id].opacity = max(0.0, min(1.0, opacity))
    
    def set_location(self, lat: float, lon: float):
        """Set the current map location."""
        self.current_location = (lat, lon)
    
    def set_zoom(self, zoom: int):
        """Set the map zoom level."""
        self.zoom_level = max(1, min(18, zoom))
    
    def get_current_view_config(self) -> Dict:
        """Get current map view configuration."""
        return {
            'location': self.current_location,
            'zoom': self.zoom_level,
            'active_layers': [layer.layer_id for layer in self.active_layers],
            'animation_enabled': self.animation_enabled,
            'auto_refresh': self.auto_refresh
        }
    
    def open_interactive_map(self, layer_ids: List[str] = None):
        """Open interactive map with specified layers."""
        if not self.current_location:
            # Default to a central location if none set
            self.current_location = (45.4642, 9.1900)  # Milan
        
        lat, lon = self.current_location
        
        # Use Windy as the primary interactive map platform
        windy_url = f"https://www.windy.com/?{lat},{lon},{self.zoom_level}"
        
        # Add layer parameters if specified
        if layer_ids:
            layer_params = []
            for layer_id in layer_ids:
                if layer_id == 'precipitation':
                    layer_params.append('rain')
                elif layer_id == 'clouds':
                    layer_params.append('clouds')
                elif layer_id == 'temperature':
                    layer_params.append('temp')
                elif layer_id == 'wind':
                    layer_params.append('wind')
                elif layer_id == 'pressure':
                    layer_params.append('pressure')
            
            if layer_params:
                windy_url = f"https://www.windy.com/?{','.join(layer_params)},{lat},{lon},{self.zoom_level}"
        
        webbrowser.open(windy_url)
    
    def open_radar_map(self):
        """Open dedicated precipitation radar map."""
        if not self.current_location:
            self.current_location = (45.4642, 9.1900)
        
        lat, lon = self.current_location
        # Use RainViewer for detailed precipitation radar
        radar_url = f"https://www.rainviewer.com/map.html?loc={lat},{lon},{self.zoom_level}&oFa=0&oC=0&oU=0&oCS=1&oF=0&oAP=0&rmt=4&c=1&o=83&lm=0&th=1"
        webbrowser.open(radar_url)
    
    def open_satellite_map(self):
        """Open satellite weather map."""
        if not self.current_location:
            self.current_location = (45.4642, 9.1900)
        
        lat, lon = self.current_location
        # Use Zoom Earth for satellite imagery
        satellite_url = f"https://zoom.earth/#view={lat},{lon},{self.zoom_level}z"
        webbrowser.open(satellite_url)
    
    def get_layer_info(self, layer_id: str) -> Optional[Dict]:
        """Get detailed information about a specific layer."""
        if layer_id in self.available_layers:
            layer = self.available_layers[layer_id]
            return {
                'id': layer.layer_id,
                'name': layer.name,
                'description': layer.description,
                'provider': layer.provider,
                'enabled': layer.enabled,
                'opacity': layer.opacity,
                'animation_speed': layer.animation_speed
            }
        return None
    
    def save_preferences(self):
        """Save map preferences to storage."""
        if self.state_manager:
            preferences = {
                'active_layers': [layer.layer_id for layer in self.active_layers],
                'zoom_level': self.zoom_level,
                'animation_enabled': self.animation_enabled,
                'auto_refresh': self.auto_refresh,
                'layer_settings': {
                    layer_id: {
                        'opacity': layer.opacity,
                        'enabled': layer.enabled
                    } for layer_id, layer in self.available_layers.items()
                }
            }
            self.state_manager.set_state('map_preferences', preferences)
    
    def load_preferences(self):
        """Load map preferences from storage."""
        if self.state_manager:
            preferences = self.state_manager.get_state('map_preferences')
            if preferences:
                self.zoom_level = preferences.get('zoom_level', self.zoom_level)
                self.animation_enabled = preferences.get('animation_enabled', self.animation_enabled)
                self.auto_refresh = preferences.get('auto_refresh', self.auto_refresh)
                
                # Restore layer settings
                layer_settings = preferences.get('layer_settings', {})
                for layer_id, settings in layer_settings.items():
                    if layer_id in self.available_layers:
                        self.available_layers[layer_id].opacity = settings.get('opacity', 0.8)
                        self.available_layers[layer_id].enabled = settings.get('enabled', True)
                
                # Restore active layers
                active_layer_ids = preferences.get('active_layers', [])
                self.active_layers = [
                    self.available_layers[layer_id] 
                    for layer_id in active_layer_ids 
                    if layer_id in self.available_layers and self.available_layers[layer_id].enabled
                ]
    
    def get_quick_map_options(self) -> List[Dict]:
        """Get quick access map options for UI."""
        return [
            {
                'name': 'Radar Precipitazioni',
                'description': 'Mostra precipitazioni in tempo reale',
                'icon': '🌧️',
                'action': lambda: self.open_radar_map(),
                'layers': ['precipitation']
            },
            {
                'name': 'Mappa Satellitare',
                'description': 'Vista satellitare con nuvole',
                'icon': '🛰️',
                'action': lambda: self.open_satellite_map(),
                'layers': ['clouds', 'temperature']
            },
            {
                'name': 'Vento e Pressione',
                'description': 'Analisi del vento e pressione atmosferica',
                'icon': '💨',
                'action': lambda: self.open_interactive_map(['wind', 'pressure']),
                'layers': ['wind', 'pressure']
            },
            {
                'name': 'Vista Completa',
                'description': 'Tutti i layer meteo combinati',
                'icon': '🗺️',
                'action': lambda: self.open_interactive_map(['precipitation', 'clouds', 'temperature', 'wind']),
                'layers': ['precipitation', 'clouds', 'temperature', 'wind']
            }
        ]
