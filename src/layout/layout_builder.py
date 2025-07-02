"""
Layout Builder for the MeteoApp.
Centralizes layout building functions for different UI components.
"""

import flet as ft
from components.responsive_text_handler import ResponsiveTextHandler

class LayoutBuilder:
    """
    Classe utility per costruire elementi di layout per l'applicazione.
    """
 
    @staticmethod
    def build_content_container(content, animation_duration=500, 
                               animation_curve=ft.AnimationCurve.EASE_IN_OUT, 
                               container_type="default") -> ft.Container:
        """
        Crea un container responsive con animazioni e stile moderno.
        
        Args:
            content: Contenuto del container
            col_size: Dizionario delle dimensioni colonna per vari breakpoint
            animation_duration: Durata delle animazioni
            animation_curve: Curva di animazione
            container_type: Tipo di container per styling specifico
            
        Returns:
            ft.Container: Container configurato con stile moderno
        """
        # Styling specifico per tipo di container
        if container_type == "main_info":
            border_radius = 24
            padding = ft.padding.symmetric(horizontal=32, vertical=24)
            margin = ft.margin.only(bottom=16)
            shadow_blur = 20
            shadow_spread = 0
        elif container_type == "sidebar":
            border_radius = 16
            padding = ft.padding.all(16)
            margin = ft.margin.all(8)
            shadow_blur = 12
            shadow_spread = 0
        else:
            border_radius = 16
            padding = ft.padding.all(20)
            margin = ft.margin.symmetric(horizontal=8, vertical=6)
            shadow_blur = 12
            shadow_spread = 0

        return ft.Container(
            content=content,
            animate=ft.Animation(animation_duration, animation_curve),
            border_radius=border_radius,
            padding=padding,
            margin=margin,
            shadow=ft.BoxShadow(
                spread_radius=shadow_spread,
                blur_radius=shadow_blur,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
        )

    @staticmethod
    def build_main_layout(sidebar, info, hourly, air_condition, chart, precipitation_chart, air_pollution_chart) -> ft.Control:
        """
        Builds the main responsive layout of the application with a modern design.
        The layout consists of a main horizontal section for sidebar and content,
        followed by full-width sections for hourly forecast and charts.

        Args:
            sidebar: The sidebar container.
            info: The main weather information container.
            hourly: The hourly forecast container.
            air_condition: The air condition information container.
            chart: The temperature chart container.
            precipitation_chart: The precipitation chart container.
            air_pollution_chart: The air pollution chart container.

        Returns:
            ft.Control: The main application layout.
        """

        return ft.Column([
            ft.ResponsiveRow([
                ft.Container(
                    content=sidebar,
                    col={"sm": 12, "md": 5, "lg": 4, "xl": 4},
                    padding=ft.padding.only(left=16, top=16, bottom=48, right=8), # bottom extra
                    expand=False,
                ),
                ft.Container(
                    content=info,
                    col={"sm": 12, "md": 7, "lg": 8, "xl": 8},
                    padding=ft.padding.only(left=8, top=16, bottom=16, right=16),
                    expand=True,
                )
            ], spacing=0),
            ft.ResponsiveRow([
                ft.Container(
                    content=air_condition,
                    col={"xs": 12},
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                )
            ]),
            ft.ResponsiveRow([
                ft.Container(
                    content=hourly,
                    col={"xs": 12},
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                )
            ]),
            ft.ResponsiveRow([
                ft.Container(
                    content=chart,
                    col={"sm": 12, "lg": 4},
                    padding=ft.padding.only(left=16, right=8, top=4, bottom=16),
                ),
                ft.Container(
                    content=precipitation_chart,
                    col={"sm": 12, "lg": 4},
                    padding=ft.padding.only(left=8, right=8, top=4, bottom=16),
                ),
                ft.Container(
                    content=air_pollution_chart,
                    col={"sm": 12, "lg": 4},
                    padding=ft.padding.only(left=8, right=16, top=4, bottom=16),
                ),
            ])
        ], spacing=0)
