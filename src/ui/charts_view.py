"""
Charts view module for the MeteoApp.
Provides comprehensive chart visualizations for weather data.
"""

import flet as ft
import logging
from services.api_service import ApiService
from utils.config import DARK_THEME, LIGHT_THEME

class ChartsView:
    """Advanced charts view for weather data visualization."""
    
    def __init__(self, page: ft.Page):
        """Initialize the charts view."""
        self.page = page
        self.api_service = ApiService()
        self.current_city = None
        self.current_language = "it"
        self.current_unit = "metric"
        self.weather_data = None
        
        # Main container for charts
        self.main_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Grafici Meteo Avanzati",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Visualizzazioni dettagliate dei dati meteorologici",
                    size=14,
                    opacity=0.8,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(height=20),
                self._create_charts_content()
            ], 
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            margin=10,
            border_radius=12,
            expand=True
        )
        
        self._update_theme()
    
    def _create_charts_content(self) -> ft.Container:
        """Create the main charts content area."""
        return ft.Container(
            content=ft.Column([
                # Temperature trend chart placeholder
                ft.Container(
                    content=ft.Column([
                        ft.Text("Andamento Temperature", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Text(
                                "Grafico temperature 7 giorni\n(In sviluppo)",
                                text_align=ft.TextAlign.CENTER,
                                size=14,
                                opacity=0.6
                            ),
                            height=200,
                            alignment=ft.alignment.center,
                            border=ft.border.all(1, ft.colors.OUTLINE),
                            border_radius=8,
                            padding=20
                        )
                    ], spacing=10),
                    padding=15,
                    border_radius=8,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    margin=ft.margin.only(bottom=15)
                ),
                
                # Precipitation chart placeholder
                ft.Container(
                    content=ft.Column([
                        ft.Text("Precipitazioni", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Text(
                                "Grafico precipitazioni\n(In sviluppo)",
                                text_align=ft.TextAlign.CENTER,
                                size=14,
                                opacity=0.6
                            ),
                            height=200,
                            alignment=ft.alignment.center,
                            border=ft.border.all(1, ft.colors.OUTLINE),
                            border_radius=8,
                            padding=20
                        )
                    ], spacing=10),
                    padding=15,
                    border_radius=8,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    margin=ft.margin.only(bottom=15)
                ),
                
                # Wind chart placeholder
                ft.Container(
                    content=ft.Column([
                        ft.Text("Vento", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Text(
                                "Grafico vento\n(In sviluppo)",
                                text_align=ft.TextAlign.CENTER,
                                size=14,
                                opacity=0.6
                            ),
                            height=200,
                            alignment=ft.alignment.center,
                            border=ft.border.all(1, ft.colors.OUTLINE),
                            border_radius=8,
                            padding=20
                        )
                    ], spacing=10),
                    padding=15,
                    border_radius=8,
                    bgcolor=ft.colors.SURFACE_VARIANT
                )
            ], 
            spacing=10,
            scroll=ft.ScrollMode.AUTO
            ),
            expand=True
        )
    
    def _update_theme(self):
        """Update the theme of the charts view."""
        if not self.page:
            return
            
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME
        
        if self.main_container:
            self.main_container.bgcolor = theme.get("CARD_BACKGROUND", ft.colors.SURFACE)
            try:
                self.main_container.update()
            except Exception:
                pass
    
    async def update_by_city(self, city: str, language: str = "it", unit: str = "metric"):
        """Update charts with data for the specified city."""
        try:
            self.current_city = city
            self.current_language = language
            self.current_unit = unit
            
            # Fetch weather data
            self.weather_data = await self.api_service.get_weather_data(city, language, unit)
            
            if self.weather_data:
                self._update_charts_with_data()
                logging.info(f"Charts updated for city: {city}")
                return True
            else:
                logging.warning(f"No weather data received for city: {city}")
                return False
                
        except Exception as e:
            logging.error(f"Error updating charts for city {city}: {e}")
            return False
    
    def _update_charts_with_data(self):
        """Update chart content with actual weather data."""
        if not self.weather_data:
            return
        
        # Update the main container title with current city
        if self.main_container and self.main_container.content:
            title_text = self.main_container.content.controls[0]
            if isinstance(title_text, ft.Text):
                title_text.value = f"Grafici Meteo - {self.current_city}"
        
        # Here you would implement actual chart updates with real data
        # For now, just update the placeholders to show we have data
        try:
            self.main_container.update()
        except Exception:
            pass
    
    def get_container(self) -> ft.Container:
        """Get the main container for the charts view."""
        return self.main_container
    
    def cleanup(self):
        """Clean up resources when the view is destroyed."""
        self.weather_data = None
        self.current_city = None
        logging.info("ChartsView cleanup completed")
