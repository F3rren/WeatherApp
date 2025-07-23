"""
Satellite Widget for MeteoApp.
Widget compatto per accesso rapido alla vista satellitare.
"""

import flet as ft
import logging
from typing import Optional
from services.maps.satellite_service import SatelliteService, SatelliteProvider, SatelliteLayer, SatelliteConfig


class SatelliteWidget:
    """Widget compatto per accesso rapido alla vista satellitare"""
    
    def __init__(self, page: ft.Page, state_manager=None, translation_service=None):
        self.page = page
        self.state_manager = state_manager
        self.translation_service = translation_service
        self.logger = logging.getLogger(__name__)
        
        # Servizio satellitare
        self.satellite_service = SatelliteService(page, state_manager, translation_service)
        
        # Coordinate correnti
        self.current_lat = 45.4642  # Default Milano
        self.current_lon = 9.1900
        
        # Aggiorna coordinate se disponibili
        self._update_coordinates()
        
        # Register for state changes
        if self.state_manager:
            self.state_manager.register_observer("current_lat", self._on_coordinates_change)
            self.state_manager.register_observer("current_lon", self._on_coordinates_change)
    
    def _update_coordinates(self):
        """Aggiorna le coordinate dal state manager"""
        if self.state_manager:
            lat = self.state_manager.get_state('current_lat')
            lon = self.state_manager.get_state('current_lon')
            
            if lat is not None and lon is not None:
                self.current_lat = float(lat)
                self.current_lon = float(lon)
                self.logger.info(f"Updated satellite widget coordinates: {self.current_lat}, {self.current_lon}")
    
    def _on_coordinates_change(self, event_data=None):
        """Callback per cambiamenti di coordinate"""
        self._update_coordinates()
    
    def _get_theme_colors(self) -> dict:
        """Ottiene i colori del tema corrente"""
        is_dark = (hasattr(self.page, 'theme_mode') and 
                  self.page.theme_mode == ft.ThemeMode.DARK)
        
        if is_dark:
            return {
                "bg": "#161b22", "surface": "#21262d", "text": "#f0f6fc",
                "text_secondary": "#8b949e", "accent": "#58a6ff", "border": "#30363d"
            }
        else:
            return {
                "bg": "#ffffff", "surface": "#f6f8fa", "text": "#24292f",
                "text_secondary": "#656d76", "accent": "#0969da", "border": "#d1d9e0"
            }
    
    def build_compact_widget(self) -> ft.Container:
        """Crea un widget compatto per la vista satellitare"""
        colors = self._get_theme_colors()
        
        # Quick access buttons per provider principali
        quick_buttons = ft.Row([
            ft.IconButton(
                icon=ft.Icons.CLOUD,
                tooltip="Windy Satellite",
                on_click=lambda _: self._open_provider(SatelliteProvider.WINDY),
                icon_color="#2196F3",
                icon_size=20
            ),
            ft.IconButton(
                icon=ft.Icons.PUBLIC,
                tooltip="Zoom Earth",
                on_click=lambda _: self._open_provider(SatelliteProvider.ZOOM_EARTH),
                icon_color="#4CAF50",
                icon_size=20
            ),
            ft.IconButton(
                icon=ft.Icons.LANGUAGE,
                tooltip="Google Earth",
                on_click=lambda _: self._open_provider(SatelliteProvider.GOOGLE_EARTH),
                icon_color="#FF9800",
                icon_size=20
            ),
            ft.IconButton(
                icon=ft.Icons.ROCKET_LAUNCH,
                tooltip="NASA Worldview",
                on_click=lambda _: self._open_provider(SatelliteProvider.WORLDVIEW),
                icon_color="#F44336",
                icon_size=20
            )
        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SATELLITE_ALT, color=colors["accent"], size=16),
                    ft.Text(
                        "Vista Satellitare", 
                        size=12, 
                        weight=ft.FontWeight.W_500,
                        color=colors["text"]
                    )
                ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                
                quick_buttons,
                
                ft.Text(
                    f"📍 {self.current_lat:.2f}, {self.current_lon:.2f}",
                    size=10,
                    color=colors["text_secondary"],
                    text_align=ft.TextAlign.CENTER
                )
            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            
            padding=8,
            bgcolor=ft.Colors.with_opacity(0.05, colors["surface"]),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, colors["border"])),
            border_radius=8,
            width=200
        )
    
    def build_full_widget(self) -> ft.Container:
        """Crea un widget completo per la vista satellitare"""
        colors = self._get_theme_colors()
        
        # Layer selector
        layer_chips = ft.Row([
            ft.Chip(
                label=ft.Text("Visibile", size=10),
                selected=True,
                on_select=lambda e: self._set_layer(SatelliteLayer.VISIBLE),
                bgcolor=colors["accent"],
                height=28
            ),
            ft.Chip(
                label=ft.Text("IR", size=10),
                on_select=lambda e: self._set_layer(SatelliteLayer.INFRARED),
                bgcolor=colors["surface"],
                height=28
            ),
            ft.Chip(
                label=ft.Text("Vapore", size=10),
                on_select=lambda e: self._set_layer(SatelliteLayer.WATER_VAPOR),
                bgcolor=colors["surface"],
                height=28
            )
        ], spacing=4, wrap=True)
        
        # Provider grid
        provider_grid = ft.Column([
            ft.Row([
                self._create_provider_button("Windy", ft.Icons.CLOUD, "#2196F3", SatelliteProvider.WINDY),
                self._create_provider_button("Zoom Earth", ft.Icons.PUBLIC, "#4CAF50", SatelliteProvider.ZOOM_EARTH)
            ], spacing=8),
            ft.Row([
                self._create_provider_button("Google", ft.Icons.LANGUAGE, "#FF9800", SatelliteProvider.GOOGLE_EARTH),
                self._create_provider_button("NASA", ft.Icons.ROCKET_LAUNCH, "#F44336", SatelliteProvider.WORLDVIEW)
            ], spacing=8)
        ], spacing=8)
        
        # Quick action button
        quick_action = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.OPEN_IN_NEW, size=16),
                ft.Text("Vista Rapida", size=12)
            ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
            on_click=lambda _: self._open_best_provider(),
            bgcolor=colors["accent"],
            color=ft.Colors.WHITE,
            height=32,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )
        
        return ft.Container(
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Icon(ft.Icons.SATELLITE_ALT, color=colors["accent"], size=20),
                    ft.Text(
                        "Vista Satellitare", 
                        size=14, 
                        weight=ft.FontWeight.W_500,
                        color=colors["text"]
                    )
                ], spacing=6, alignment=ft.MainAxisAlignment.CENTER),
                
                # Coordinate info
                ft.Container(
                    content=ft.Text(
                        f"📍 Lat: {self.current_lat:.4f}, Lon: {self.current_lon:.4f}",
                        size=11,
                        color=colors["text_secondary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=4,
                    bgcolor=ft.Colors.with_opacity(0.1, colors["surface"]),
                    border_radius=4
                ),
                
                # Layer selector
                ft.Text("Layer:", size=12, weight=ft.FontWeight.W_500, color=colors["text"]),
                layer_chips,
                
                # Provider grid
                ft.Text("Provider:", size=12, weight=ft.FontWeight.W_500, color=colors["text"]),
                provider_grid,
                
                # Quick action
                quick_action
                
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            
            padding=12,
            bgcolor=ft.Colors.with_opacity(0.05, colors["surface"]),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, colors["border"])),
            border_radius=10,
            width=280
        )
    
    def _create_provider_button(self, name: str, icon: ft.Icons, color: str, provider: SatelliteProvider) -> ft.Container:
        """Crea un bottone per un provider"""
        colors = self._get_theme_colors()
        
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=color, size=20),
                ft.Text(name, size=10, color=colors["text"], text_align=ft.TextAlign.CENTER)
            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=8,
            width=60,
            height=50,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, colors["border"])),
            border_radius=6,
            bgcolor=ft.Colors.with_opacity(0.05, colors["surface"]),
            on_click=lambda _: self._open_provider(provider),
            ink=True
        )
    
    def _open_provider(self, provider: SatelliteProvider):
        """Apre un provider specifico"""
        config = SatelliteConfig(
            provider=provider,
            layer=getattr(self, 'current_layer', SatelliteLayer.VISIBLE),
            zoom_level=8
        )
        
        success = self.satellite_service.open_satellite_view(
            self.current_lat, 
            self.current_lon, 
            config
        )
        
        if success:
            self.logger.info(f"Opened satellite view with {provider.value}")
    
    def _open_best_provider(self):
        """Apre il miglior provider per la posizione corrente"""
        best_provider = self.satellite_service.get_best_provider_for_location(
            self.current_lat, 
            self.current_lon
        )
        
        config = self.satellite_service.create_location_optimized_config(
            self.current_lat, 
            self.current_lon
        )
        
        success = self.satellite_service.open_satellite_view(
            self.current_lat, 
            self.current_lon, 
            config
        )
        
        if success:
            self.logger.info(f"Opened optimized satellite view with {best_provider.value}")
    
    def _set_layer(self, layer: SatelliteLayer):
        """Imposta il layer corrente"""
        self.current_layer = layer
        self.logger.info(f"Selected satellite layer: {layer.value}")
    
    def cleanup(self):
        """Cleanup observers"""
        if self.state_manager:
            self.state_manager.unregister_observer("current_lat", self._on_coordinates_change)
            self.state_manager.unregister_observer("current_lon", self._on_coordinates_change)
