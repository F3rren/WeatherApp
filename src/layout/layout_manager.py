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
        precipitation_chart_content, air_pollution_chart_content, air_pollution_content, animation_duration=500, animation_curve=ft.AnimationCurve.EASE_IN_OUT) -> None:
        """
        Crea tutti i contenitori per il layout dell'applicazione con design moderno.
        
        Args:
            sidebar_content: Oggetto Sidebar da inserire nel container
            info_content: Contenuto del container info meteo
            hourly_content: Contenuto del container previsioni orarie
            chart_content: Contenuto del container grafico temperature
            precipitation_chart_content: Contenuto del container grafico precipitazioni
            air_pollution_chart_content: Contenuto del container grafico inquinamento
            air_pollution_content: Contenuto del container informazioni inquinamento
            animation_duration: Durata delle animazioni in millisecondi
            animation_curve: Curva di animazione
        """
        # Sidebar con stile moderno e larghezza aumentata
        self.containers['sidebar'] = LayoutBuilder.build_content_container(
            sidebar_content, 
            {"sm": 12, "md": 5, "lg": 4, "xl": 4}, # Aumentata da 3 a 4 per più spazio
            animation_duration,
            animation_curve,
            "sidebar"
        )
        
        # Container principale info meteo - stile hero section
        self.containers['info'] = LayoutBuilder.build_content_container(
            info_content,
            {"xs": 12},
            animation_duration,
            animation_curve,
            "main_info"
        )
        
        # Previsioni orarie - stile elegante
        self.containers['hourly'] = LayoutBuilder.build_content_container(
            hourly_content, 
            {"xs": 12}, 
            animation_duration,
            animation_curve
        )
        
        # Informazioni inquinamento (temporaneamente vuoto per ora)
        self.containers['air_pollution'] = LayoutBuilder.build_content_container(
            air_pollution_content,
            {"xs": 12},
            animation_duration,
            animation_curve
        )
        
        # Air condition components (initially empty, will be populated after weather data loads)
        self.containers['air_condition'] = LayoutBuilder.build_content_container(
            ft.Container(
                content=ft.Text(
                    "Loading air conditions...", 
                    size=14,
                    color=ft.Colors.GREY_600
                ),
                height=150,
                alignment=ft.alignment.center
            ),
            {"xs": 12},
            animation_duration,
            animation_curve
        )

        # Grafico temperature
        self.containers['chart'] = LayoutBuilder.build_content_container(
            chart_content,
            {"xs": 12},
            animation_duration,
            animation_curve
        )

        # Grafico precipitazioni
        self.containers['precipitation_chart'] = LayoutBuilder.build_content_container(
            precipitation_chart_content,
            {"xs": 12},
            animation_duration,
            animation_curve
        )

        # Grafico inquinamento aria
        self.containers['air_pollution_chart'] = LayoutBuilder.build_content_container(
            air_pollution_chart_content,
            {"xs": 12},
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
            self.containers.get('air_condition', ft.Container()),  # Use air_condition instead of air_pollution
            self.containers['chart'],
            self.containers['precipitation_chart'],
            self.containers['air_pollution_chart']
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
    
    def update_air_condition_layout(self, air_condition_components) -> None:
        """
        Updates the layout to use separated air condition components.
        
        Args:
            air_condition_components: Dictionary with individual air condition components
        """
        if not air_condition_components:
            return
            
        # Create air condition grid layout
        air_condition_grid = LayoutBuilder.build_air_condition_grid(
            air_condition_components, 
            self.page
        )
        
        # Update the existing air_condition container content instead of recreating everything
        if 'air_condition' in self.containers and self.containers['air_condition']:
            self.containers['air_condition'].content = air_condition_grid
            try:
                self.containers['air_condition'].update()
            except AssertionError:
                # Container not yet added to page, this is okay
                pass

