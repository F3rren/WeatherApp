"""
Layout Builder for the MeteoApp.
Centralizes layout building functions for different UI components.
"""

import flet as ft
from typing import Dict, Any
from components.responsive_text_handler import ResponsiveTextHandler

class LayoutBuilder:
    """
    Classe utility per costruire elementi di layout per l'applicazione.
    """
    
    _text_handler = None
    _debug_initialized = False
    
    @classmethod
    def init_text_handler(cls, page: ft.Page):
        """Initialize ResponsiveTextHandler if not already initialized"""
        if cls._text_handler is None and page is not None:
            cls._text_handler = ResponsiveTextHandler(
                page=page,
                base_sizes={
                    'title': 22,        # Titoli principali
                    'subtitle': 18,     # Sottotitoli
                    'body': 14,         # Testo normale
                    'small': 12,        # Testo piccolo
                },
                breakpoints=[600, 900, 1200, 1600]
            )
            if not cls._debug_initialized:
                print("DEBUG: LayoutBuilder initialized with ResponsiveTextHandler")
                cls._debug_initialized = True
        return cls._text_handler
    
    @classmethod
    def get_text_size(cls, category, page=None):
        """Get text size for the given category"""
        if cls._text_handler is None:
            cls.init_text_handler(page)
        
        if cls._text_handler:
            return cls._text_handler.get_size(category)
        return None
    
    @staticmethod
    def build_content_container(content, col_size, animation_duration=500, 
                               animation_curve=ft.AnimationCurve.EASE_IN_OUT) -> ft.Container:
        """
        Crea un container responsive con animazioni e stile moderno.
        
        Args:
            content: Contenuto del container
            col_size: Dizionario delle dimensioni colonna per vari breakpoint
            animation_duration: Durata delle animazioni
            animation_curve: Curva di animazione
            
        Returns:
            ft.Container: Container configurato con stile moderno
        """
        return ft.Container(
            content=content,
            animate=ft.Animation(animation_duration, animation_curve),
            border_radius=20,  # Angoli più arrotondati
            padding=ft.padding.all(20),  # Padding più generoso
            margin=ft.margin.all(5),  # Piccolo margine per spaziatura
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
            col=col_size
        )

    @staticmethod
    def build_main_layout(sidebar, info, hourly, weekly, air_pollution, chart, air_pollution_chart) -> ft.Control:
        """
        Costruisce il layout principale responsivo dell'applicazione con design moderno.
        Layout orizzontale: sidebar sinistra + contenuto principale a destra.
        
        Args:
            sidebar: Container della barra laterale
            info: Container delle informazioni principali meteo
            hourly: Container delle previsioni orarie
            weekly: Container delle previsioni settimanali
            air_pollution: Container delle informazioni sull'inquinamento
            chart: Container del grafico temperature
            air_pollution_chart: Container del grafico inquinamento
            
        Returns:
            ft.ResponsiveRow: Layout principale responsivo
        """
        # Layout principale orizzontale
        return ft.ResponsiveRow([
            # Sidebar sinistra (25% larghezza)
            ft.Container(
                content=sidebar,
                col={"sm": 12, "md": 4, "lg": 3, "xl": 3},
                padding=ft.padding.all(10),
            ),
            
            # Area contenuto principale (75% larghezza)
            ft.Container(
                content=ft.Column([
                    # Header principale con info meteo
                    ft.ResponsiveRow([
                        info
                    ]),
                    
                    # Previsioni orarie
                    ft.ResponsiveRow([
                        hourly
                    ]),
                    
                    # Riga con condizioni attuali e dettagli
                    ft.ResponsiveRow([
                        # Condizioni attuali (sinistra)
                        ft.Container(
                            content=ft.Column([
                                weekly,
                                air_pollution
                            ], spacing=10),
                            col={"sm": 12, "md": 6, "lg": 6},
                            padding=ft.padding.all(5),
                        ),
                        
                        # Dettagli e grafici (destra)
                        ft.Container(
                            content=ft.Column([
                                chart,
                                air_pollution_chart
                            ], spacing=10),
                            col={"sm": 12, "md": 6, "lg": 6},
                            padding=ft.padding.all(5),
                        )
                    ])
                ], spacing=15),
                col={"sm": 12, "md": 8, "lg": 9, "xl": 9},
                padding=ft.padding.all(10),
            )
        ], spacing=0)
