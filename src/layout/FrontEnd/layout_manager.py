"""
Layout Manager per MeteoApp.
Centralizza la gestione del layout dell'applicazione.
"""

import flet as ft
import logging
from typing import Dict

from layout.frontend.layout_builder import LayoutBuilder
from config import LIGHT_THEME, DARK_THEME

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
    
    def create_containers(self,                         
                         sidebar_content,
                         info_content,
                         weekly_content,
                         chart_content,
                         air_pollution_chart_content,
                         air_pollution_content,
                         animation_duration=500,
                         animation_curve=ft.AnimationCurve.EASE_IN_OUT) -> None:
        """
        Crea tutti i contenitori per il layout dell'applicazione.
        
        Args:
            sidebar_content: Oggetto Sidebar da inserire nel container
            info_content: Contenuto del container info meteo
            weekly_content: Contenuto del container previsioni settimanali
            chart_content: Contenuto del container grafico
            air_pollution_chart_content: Contenuto del container grafico inquinamento
            air_pollution_content: Contenuto del container informazioni inquinamento
            animation_duration: Durata delle animazioni in millisecondi
            animation_curve: Curva di animazione
        """
        self.containers['sidebar'] = LayoutBuilder.build_content_container(
            sidebar_content, 
            {"xs": 12},
            animation_duration,
            animation_curve
        )
        
        self.containers['info'] = LayoutBuilder.build_content_container(
            info_content,
            {"xs": 12, "md": 12, "lg": 12},
            animation_duration,
            animation_curve
        )
        
        self.containers['weekly'] = LayoutBuilder.build_content_container(
            weekly_content,
            {"xs": 12, "md": 8, "lg": 7},
            animation_duration,
            animation_curve
        )
        
        self.containers['air_pollution'] = LayoutBuilder.build_content_container(
            air_pollution_content,
            {"xs": 12, "md": 4, "lg": 5},
            animation_duration,
            animation_curve
        )

        self.containers['air_pollution_chart'] = LayoutBuilder.build_content_container(
            air_pollution_chart_content,
            {"xs": 12, "sm": 6, "md": 12, "lg": 6},
            animation_duration,
            animation_curve
        )

        self.containers['chart'] = LayoutBuilder.build_content_container(
            chart_content,
            {"xs": 12, "sm": 6, "md": 6, "lg": 6},
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
            self.containers['weekly'],
            self.containers['air_pollution'],
            self.containers['chart'],
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

        # Aggiorna i container con i gradienti
        #self.update_container_gradients(theme_mode)
        
        # Aggiorna anche il colore di sfondo della pagina
        theme = LIGHT_THEME if theme_mode == ft.ThemeMode.LIGHT else DARK_THEME
        self.page.bgcolor = theme.get("BACKGROUND", "#f5f5f5" if theme_mode == ft.ThemeMode.LIGHT else "#1a1a1a")
        self.page.update()

