"""
Layout Builder for the MeteoApp.
Centralizes layout building functions for different UI components.
"""

import flet as ft
from typing import Dict, Any

class LayoutBuilder:
    """
    Classe utility per costruire elementi di layout per l'applicazione.
    """
    
    @staticmethod
    def build_content_container(content, col_size, animation_duration=500, 
                               animation_curve=ft.AnimationCurve.EASE_IN_OUT) -> ft.Container:
        """
        Crea un container responsive con animazioni.
        
        Args:
            content: Contenuto del container
            col_size: Dizionario delle dimensioni colonna per vari breakpoint
            animation_duration: Durata delle animazioni
            animation_curve: Curva di animazione
            
        Returns:
            ft.Container: Container configurato
        """
        return ft.Container(
            content=content,
            animate=ft.Animation(animation_duration, animation_curve),
            border_radius=15,
            padding=10,
            col=col_size
        )

    @staticmethod
    def build_main_layout(sidebar, info, weekly, air_pollution, chart, air_pollution_chart) -> ft.Control:
        """
        Costruisce il layout principale responsivo dell'applicazione.
        
        Args:
            sidebar: Container della barra laterale
            info: Container delle informazioni principali meteo
            weekly: Container delle previsioni settimanali
            air_pollution: Container delle informazioni sull'inquinamento
            chart: Container del grafico temperature
            air_pollution_chart: Container del grafico inquinamento
            
        Returns:
            ft.ResponsiveRow: Layout principale responsivo
        """
        return ft.Column([
            # Prima riga: sidebar
            ft.ResponsiveRow([
                sidebar
            ]),
            
            # Seconda riga: info
            ft.ResponsiveRow([
                info
            ]),
            
            # Terza riga: previsioni settimanali + inquinamento aria
            ft.ResponsiveRow([
                weekly,
                air_pollution
            ]),
            
            # Quarta riga: grafici
            ft.ResponsiveRow([
                chart,
                air_pollution_chart
            ])
        ])
