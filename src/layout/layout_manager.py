"""
Layout Manager per MeteoApp.
Centralizza la gestione del layout dell'applicazione.
"""

import flet as ft
import logging
from typing import Dict

from layout.layout_builder import LayoutBuilder
from utils.config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class LayoutManager:
    """
    Layout manager class for the MeteoApp.
    Handles the construction and management of UI layout components.
    """
    
    def __init__(self, page: ft.Page):
        """
        Inizializza il gestore del layout.
        
        Args:
            page: Flet page object
        """
        self.page = page
        self.containers = {}
        self.layout = None
        
        # Initialize ResponsiveTextHandler
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 22,        # Titoli principali
                'subtitle': 18,     # Sottotitoli
                'body': 14,         # Testo normale
                'small': 12,        # Testo piccolo
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Dictionary to track text controls
        self.text_controls = {}
        
        # Register as observer for responsive updates
        self.text_handler.add_observer(self.update_text_controls)
    
    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        for control, size_category in self.text_controls.items():
            if hasattr(control, 'size'):
                control.size = self.text_handler.get_size(size_category)
        
        # Request page update
        if self.page:
            self.page.update()
    
    def create_containers(self, sidebar_content, info_content, hourly_content, chart_content,
        precipitation_chart_content, air_pollution_content, animation_duration=500, animation_curve=ft.AnimationCurve.EASE_IN_OUT) -> None:
        """
        Crea tutti i contenitori per il layout dell'applicazione con design moderno.
        
        Args:
            sidebar_content: Oggetto Sidebar da inserire nel container
            info_content: Contenuto del container info meteo
            hourly_content: Contenuto del container previsioni orarie
            chart_content: Contenuto del container grafico temperature
            precipitation_chart_content: Contenuto del container grafico precipitazioni
            air_condition_content: Contenuto del container condizioni dell'aria
            air_pollution_content: Contenuto del container informazioni inquinamento
            animation_duration: Durata delle animazioni in millisecondi
            animation_curve: Curva di animazione
        """
        # Sidebar con stile moderno e larghezza aumentata
        self.containers['sidebar'] = LayoutBuilder.build_content_container(
            sidebar_content, 
            animation_duration,
            animation_curve,
            "sidebar"
        )
        
        # Container principale info meteo - stile hero section
        self.containers['info'] = LayoutBuilder.build_content_container(
            info_content,
            animation_duration,
            animation_curve,
            "main_info"
        )


        # Previsioni orarie - stile elegante
        self.containers['hourly'] = LayoutBuilder.build_content_container(
            hourly_content, 
            #{"xs": 12}, 
            animation_duration,
            animation_curve
        )
        
        # Grafico temperature
        self.containers['chart'] = LayoutBuilder.build_content_container(
            chart_content,
            #{"xs": 12},
            animation_duration,
            animation_curve
        )

        # Grafico precipitazioni
        self.containers['precipitation_chart'] = LayoutBuilder.build_content_container(
            precipitation_chart_content,
            #{"xs": 12},
            animation_duration,
            animation_curve
        )

        # Informazioni inquinamento (temporaneamente vuoto per ora)
        self.containers['air_pollution'] = LayoutBuilder.build_content_container(
            air_pollution_content,
            #{"xs": 12},
            animation_duration,
            animation_curve
        )
    def build_layout(self) -> ft.Control:
        """
        Costruisce il layout principale dell'applicazione.
        
        Returns:
            ft.Control: Il layout principale
        """
        self.layout = LayoutBuilder.build_main_layout(
            self.containers['sidebar'],
            self.containers['info'],
            self.containers['hourly'], 
            self.containers['chart'],
            self.containers['precipitation_chart'],
            self.containers['air_pollution']
        )
        return self.layout
    
    def get_all_containers(self) -> Dict[str, ft.Container]:
        """
        Restituisce tutti i contenitori del layout.
        
        Returns:
            Dict[str, ft.Container]: Dizionario dei contenitori
        """
        return self.containers
    
    def update_container_colors(self, theme_mode: ft.ThemeMode) -> None:
        """
        Aggiorna i colori dei contenitori in base al tema.
        
        Args:
            theme_mode: Modalità tema (chiaro/scuro)
        """
        if not self.containers:
            logging.warning("Containers not initialized. Cannot update colors.")
            return

        # Determina lo schema di colori basato sul tema
        theme = LIGHT_THEME if theme_mode == ft.ThemeMode.LIGHT else DARK_THEME
        
        # Applica il colore di sfondo a tutti i container
        card_background = theme.get("CARD_BACKGROUND", "#ffffff" if theme_mode == ft.ThemeMode.LIGHT else "#262626")
        
        # Aggiorna tutti i container con lo stesso colore di sfondo
        for name, container in self.containers.items():
            if container:  # Check if container is not None
                # Il container 'info' avrà un gradiente speciale
                if name == 'info' and 'INFO_GRADIENT' in theme:
                    gradient_start = theme["INFO_GRADIENT"]["start"]
                    gradient_end = theme["INFO_GRADIENT"]["end"]
                    
                    # Applica il gradiente al container info
                    container.gradient = ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=[gradient_start, gradient_end]
                    )
                    
                    # Rimuovi il background solido quando si applica il gradiente
                    container.bgcolor = None
                else:
                    # Tutti gli altri container hanno un colore solido
                    container.bgcolor = card_background
                    # Assicurati che non ci sia alcun gradiente residuo
                    container.gradient = None
                
                # Only update if the container is attached to the page
                if getattr(container, 'page', None):
                    container.update()
            else:
                logging.warning(f"Container '{name}' is None, skipping color update.")
    
        # Aggiorna anche il colore di sfondo della pagina
        if self.page:
            self.page.bgcolor = theme.get("BACKGROUND", "#f5f5f5" if theme_mode == ft.ThemeMode.LIGHT else "#1a1a1a")
            if getattr(self.page, 'update', None):
                self.page.update()
    
    def switch_main_content(self, new_content):
        """
        Switch the main content area to display new content (e.g., charts view).
        
        Args:
            new_content: The new content to display in the main area
        """
        if not self.layout:
            logging.warning("Layout not initialized, cannot switch content")
            return
            
        try:
            # Find the main content area in the layout and replace it
            # Assuming the layout is a Row with sidebar and main content
            if hasattr(self.layout, 'controls') and len(self.layout.controls) > 1:
                # Replace the main content (assuming it's the second control)
                self.layout.controls[1] = new_content
                self.layout.update()
                logging.info("Successfully switched to new main content")
            else:
                logging.warning("Cannot find main content area to switch")
        except Exception as e:
            logging.error(f"Error switching main content: {e}")
    
    def switch_to_weather_content(self, info_container, hourly_container, chart_container, 
                                 air_pollution_container, air_pollution_chart_container, 
                                 precipitation_chart_container):
        """
        Switch back to the original weather view layout.
        
        Args:
            info_container: Weather info container
            hourly_container: Hourly forecast container
            chart_container: Chart container
            air_pollution_container: Air pollution container
            air_pollution_chart_container: Air pollution chart container
            precipitation_chart_container: Precipitation chart container
        """
        if not self.layout:
            logging.warning("Layout not initialized, cannot switch to weather content")
            return
            
        try:
            # Rebuild the original weather layout using the main layout structure
            # Get the sidebar from the current layout
            sidebar_container = None
            if hasattr(self.layout, 'controls') and len(self.layout.controls) > 0:
                # Extract sidebar from the first row
                first_row = self.layout.controls[0]
                if hasattr(first_row, 'controls') and len(first_row.controls) > 0:
                    sidebar_container = first_row.controls[0].content
            
            if sidebar_container:
                # Rebuild the complete weather layout
                weather_layout = LayoutBuilder.build_main_layout(
                    sidebar=sidebar_container,
                    info=info_container,
                    hourly=hourly_container,
                    chart=chart_container,
                    precipitation_chart=precipitation_chart_container,
                    air_pollution_chart=air_pollution_chart_container
                )
                
                # Replace the entire layout
                if hasattr(self.page, 'controls') and len(self.page.controls) > 0:
                    self.page.controls[0] = weather_layout
                    self.layout = weather_layout
                    self.page.update()
                    logging.info("Successfully switched back to weather content")
                else:
                    logging.warning("Cannot find page controls to update")
            else:
                logging.warning("Cannot find sidebar to rebuild weather layout")
        except Exception as e:
            logging.error(f"Error switching to weather content: {e}")

