"""
Satellite Service for MeteoApp.
Gestisce i diversi provider di immagini satellitari e le loro funzionalità.
"""

import logging
import webbrowser
import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

import flet as ft


class SatelliteProvider(Enum):
    """Provider di immagini satellitari"""
    WINDY = "windy"
    ZOOM_EARTH = "zoom_earth"
    GOOGLE_EARTH = "google_earth"
    METEOBLUE = "meteoblue"
    WORLDVIEW = "worldview"
    SENTINEL_HUB = "sentinel_hub"
    EARTH_NULLSCHOOL = "earth_nullschool"


class SatelliteLayer(Enum):
    """Tipi di layer satellitari"""
    VISIBLE = "visible"              # Luce visibile
    INFRARED = "infrared"            # Infrarosso
    WATER_VAPOR = "water_vapor"      # Vapore acqueo
    ENHANCED_INFRARED = "enhanced_ir" # Infrarosso migliorato
    TRUE_COLOR = "true_color"        # Colori reali
    NATURAL_COLOR = "natural_color"  # Colori naturali
    NIGHT_MICROPHYSICS = "night_micro" # Microfisica notturna


@dataclass
class SatelliteConfig:
    """Configurazione per la vista satellitare"""
    provider: SatelliteProvider
    layer: SatelliteLayer = SatelliteLayer.VISIBLE
    zoom_level: int = 8
    animation: bool = False
    time_range_hours: int = 24
    auto_refresh: bool = False
    refresh_interval_minutes: int = 15


class SatelliteService:
    """
    Servizio avanzato per la gestione delle immagini satellitari meteorologiche.
    """
    
    def __init__(self, page: ft.Page, state_manager=None, translation_service=None):
        self.page = page
        self.state_manager = state_manager
        self.translation_service = translation_service
        self.logger = logging.getLogger(__name__)
        
        # Configurazioni dei provider satellitari
        self.provider_configs = {
            SatelliteProvider.WINDY: {
                "name": "Windy Satellite",
                "base_url": "https://www.windy.com",
                "layers": {
                    SatelliteLayer.VISIBLE: "satellite",
                    SatelliteLayer.INFRARED: "satellite",
                    SatelliteLayer.WATER_VAPOR: "satellite"
                },
                "supports_animation": True,
                "supports_time_control": True,
                "max_zoom": 12,
                "description": "Immagini satellitari in tempo reale con animazioni"
            },
            SatelliteProvider.ZOOM_EARTH: {
                "name": "Zoom Earth",
                "base_url": "https://zoom.earth",
                "layers": {
                    SatelliteLayer.VISIBLE: "/live",
                    SatelliteLayer.INFRARED: "/storms"
                },
                "supports_animation": True,
                "supports_time_control": False,
                "max_zoom": 10,
                "description": "Vista satellitare ad altissima risoluzione"
            },
            SatelliteProvider.GOOGLE_EARTH: {
                "name": "Google Earth",
                "base_url": "https://earth.google.com/web",
                "layers": {
                    SatelliteLayer.VISIBLE: "",
                    SatelliteLayer.TRUE_COLOR: ""
                },
                "supports_animation": False,
                "supports_time_control": True,
                "max_zoom": 20,
                "description": "Vista satellitare Google con vista 3D"
            },
            SatelliteProvider.METEOBLUE: {
                "name": "MeteoBlue Satellite",
                "base_url": "https://www.meteoblue.com/en/weather/maps",
                "layers": {
                    SatelliteLayer.VISIBLE: "satellite",
                    SatelliteLayer.INFRARED: "satellite_infrared",
                    SatelliteLayer.WATER_VAPOR: "satellite_water_vapor"
                },
                "supports_animation": True,
                "supports_time_control": True,
                "max_zoom": 10,
                "description": "Immagini satellitari meteorologiche professionali"
            },
            SatelliteProvider.WORLDVIEW: {
                "name": "NASA Worldview",
                "base_url": "https://worldview.earthdata.nasa.gov",
                "layers": {
                    SatelliteLayer.VISIBLE: "MODIS_Terra_CorrectedReflectance_TrueColor",
                    SatelliteLayer.INFRARED: "MODIS_Terra_CorrectedReflectance_Bands721",
                    SatelliteLayer.NATURAL_COLOR: "VIIRS_SNPP_CorrectedReflectance_TrueColor"
                },
                "supports_animation": True,
                "supports_time_control": True,
                "max_zoom": 12,
                "description": "Immagini satellitari NASA scientifiche"
            },
            SatelliteProvider.SENTINEL_HUB: {
                "name": "Sentinel Hub",
                "base_url": "https://apps.sentinel-hub.com/eo-browser",
                "layers": {
                    SatelliteProvider.VISIBLE: "1_TRUE_COLOR",
                    SatelliteLayer.INFRARED: "2_FALSE_COLOR",
                    SatelliteLayer.NATURAL_COLOR: "4_FALSE_COLOR"
                },
                "supports_animation": False,
                "supports_time_control": True,
                "max_zoom": 14,
                "description": "Immagini Sentinel ad alta risoluzione"
            },
            SatelliteProvider.EARTH_NULLSCHOOL: {
                "name": "Earth Nullschool",
                "base_url": "https://earth.nullschool.net",
                "layers": {
                    SatelliteLayer.VISIBLE: "overlay=satellite",
                    SatelliteLayer.WATER_VAPOR: "overlay=rh"
                },
                "supports_animation": True,
                "supports_time_control": False,
                "max_zoom": 8,
                "description": "Vista globale animata con dati meteorologici"
            }
        }
        
        # Configurazione corrente
        self.current_config = SatelliteConfig(
            provider=SatelliteProvider.WINDY,
            layer=SatelliteLayer.VISIBLE
        )
    
    def get_available_layers(self, provider: SatelliteProvider) -> List[SatelliteLayer]:
        """Ottiene i layer disponibili per un provider specifico"""
        if provider in self.provider_configs:
            return list(self.provider_configs[provider]["layers"].keys())
        return []
    
    def get_available_providers(self) -> List[SatelliteProvider]:
        """Ottiene tutti i provider disponibili"""
        return list(self.provider_configs.keys())
    
    def build_satellite_url(self, lat: float, lon: float, config: SatelliteConfig) -> str:
        """Costruisce l'URL per la configurazione satellitare specificata"""
        provider_config = self.provider_configs.get(config.provider)
        if not provider_config:
            return self._build_fallback_url(lat, lon)
        
        base_url = provider_config["base_url"]
        
        if config.provider == SatelliteProvider.WINDY:
            layer_param = provider_config["layers"].get(config.layer, "satellite")
            url = f"{base_url}/?{layer_param},{lat},{lon},{config.zoom_level}"
            if config.animation and provider_config["supports_animation"]:
                url += "&animate=true"
            return url
        
        elif config.provider == SatelliteProvider.ZOOM_EARTH:
            layer_path = provider_config["layers"].get(config.layer, "/live")
            return f"{base_url}{layer_path}/@{lat},{lon},{config.zoom_level}z/sat"
        
        elif config.provider == SatelliteProvider.GOOGLE_EARTH:
            # Google Earth usa un sistema di coordinate diverso
            altitude = 8000 * (11 - config.zoom_level)  # Calcola altitudine approssimativa
            return f"{base_url}/@{lat},{lon},{altitude}a,35y,0h,0t,0r"
        
        elif config.provider == SatelliteProvider.METEOBLUE:
            layer_param = provider_config["layers"].get(config.layer, "satellite")
            return f"{base_url}/{layer_param}#{config.zoom_level}/{lat}/{lon}"
        
        elif config.provider == SatelliteProvider.WORLDVIEW:
            # NASA Worldview richiede una bounding box
            offset = 2.0 / config.zoom_level  # Offset basato sullo zoom
            west, south = lon - offset, lat - offset
            east, north = lon + offset, lat + offset
            
            layer_param = provider_config["layers"].get(config.layer, "MODIS_Terra_CorrectedReflectance_TrueColor")
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            return f"{base_url}/?v={west},{south},{east},{north}&t={current_date}&l={layer_param}"
        
        elif config.provider == SatelliteProvider.SENTINEL_HUB:
            return f"{base_url}/?zoom={config.zoom_level}&lat={lat}&lng={lon}&themeId=DEFAULT-THEME"
        
        elif config.provider == SatelliteProvider.EARTH_NULLSCHOOL:
            layer_param = provider_config["layers"].get(config.layer, "overlay=satellite")
            return f"{base_url}/#{config.zoom_level}/{lat}/{lon}/{layer_param}"
        
        return self._build_fallback_url(lat, lon)
    
    def _build_fallback_url(self, lat: float, lon: float) -> str:
        """URL di fallback quando il provider non è supportato"""
        return f"https://www.windy.com/?satellite,{lat},{lon},8"
    
    def open_satellite_view(self, lat: float, lon: float, config: Optional[SatelliteConfig] = None) -> bool:
        """Apre la vista satellitare con la configurazione specificata"""
        try:
            if config:
                self.current_config = config
            
            url = self.build_satellite_url(lat, lon, self.current_config)
            self.logger.info(f"Opening satellite view: {url}")
            
            webbrowser.open(url)
            return True
            
        except Exception as e:
            self.logger.error(f"Error opening satellite view: {e}")
            return False
    
    def get_provider_info(self, provider: SatelliteProvider) -> Dict:
        """Ottiene informazioni dettagliate su un provider"""
        return self.provider_configs.get(provider, {})
    
    def get_layer_name(self, layer: SatelliteLayer) -> str:
        """Ottiene il nome leggibile di un layer"""
        layer_names = {
            SatelliteLayer.VISIBLE: "Luce visibile",
            SatelliteLayer.INFRARED: "Infrarosso",
            SatelliteLayer.WATER_VAPOR: "Vapore acqueo",
            SatelliteLayer.ENHANCED_INFRARED: "Infrarosso migliorato",
            SatelliteLayer.TRUE_COLOR: "Colori reali",
            SatelliteLayer.NATURAL_COLOR: "Colori naturali",
            SatelliteLayer.NIGHT_MICROPHYSICS: "Microfisica notturna"
        }
        return layer_names.get(layer, layer.value.replace("_", " ").title())
    
    def supports_animation(self, provider: SatelliteProvider) -> bool:
        """Verifica se il provider supporta l'animazione"""
        return self.provider_configs.get(provider, {}).get("supports_animation", False)
    
    def supports_time_control(self, provider: SatelliteProvider) -> bool:
        """Verifica se il provider supporta il controllo temporale"""
        return self.provider_configs.get(provider, {}).get("supports_time_control", False)
    
    def get_comparison_urls(self, lat: float, lon: float, layer: SatelliteLayer) -> Dict[str, str]:
        """Ottiene URL per confrontare lo stesso layer su provider diversi"""
        urls = {}
        
        for provider in self.get_available_providers():
            if layer in self.get_available_layers(provider):
                config = SatelliteConfig(provider=provider, layer=layer)
                provider_name = self.provider_configs[provider]["name"]
                urls[provider_name] = self.build_satellite_url(lat, lon, config)
        
        return urls
    
    def open_comparison_view(self, lat: float, lon: float, layer: SatelliteLayer):
        """Apre viste multiple per confronto"""
        comparison_urls = self.get_comparison_urls(lat, lon, layer)
        
        for provider_name, url in comparison_urls.items():
            self.logger.info(f"Opening {provider_name}: {url}")
            webbrowser.open(url)
            # Piccolo delay tra le aperture per evitare sovraccarico
            asyncio.create_task(asyncio.sleep(0.5))
    
    async def create_satellite_animation(self, lat: float, lon: float, 
                                       provider: SatelliteProvider = SatelliteProvider.WINDY,
                                       duration_hours: int = 12) -> bool:
        """Crea un'animazione satellitare (aprendo URL in sequenza)"""
        if not self.supports_animation(provider):
            self.logger.warning(f"Provider {provider} does not support animation")
            return False
        
        try:
            # Per ora, apriamo semplicemente la vista animata del provider
            config = SatelliteConfig(
                provider=provider,
                layer=SatelliteLayer.VISIBLE,
                animation=True
            )
            
            return self.open_satellite_view(lat, lon, config)
            
        except Exception as e:
            self.logger.error(f"Error creating satellite animation: {e}")
            return False
    
    def get_best_provider_for_location(self, lat: float, lon: float) -> SatelliteProvider:
        """Suggerisce il miglior provider basato sulla posizione"""
        # Logica semplice - può essere estesa con regioni specifiche
        if abs(lat) > 60:  # Regioni polari
            return SatelliteProvider.WORLDVIEW  # NASA ha buona copertura polare
        elif abs(lat) < 30:  # Regioni tropicali
            return SatelliteProvider.ZOOM_EARTH  # Buona risoluzione per tropici
        else:  # Regioni temperate
            return SatelliteProvider.WINDY  # Buon compromesso generale
    
    def get_recommended_layer_for_time(self, hour: int) -> SatelliteLayer:
        """Suggerisce il miglior layer basato sull'ora del giorno"""
        if 6 <= hour <= 18:  # Giorno
            return SatelliteLayer.VISIBLE
        else:  # Notte
            return SatelliteLayer.INFRARED
    
    def create_location_optimized_config(self, lat: float, lon: float) -> SatelliteConfig:
        """Crea una configurazione ottimizzata per la posizione"""
        current_hour = datetime.now().hour
        
        return SatelliteConfig(
            provider=self.get_best_provider_for_location(lat, lon),
            layer=self.get_recommended_layer_for_time(current_hour),
            zoom_level=8,
            animation=True
        )
