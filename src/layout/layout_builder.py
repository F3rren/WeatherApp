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

    def build_main_layout(sidebar, info, hourly, air_pollution, chart, precipitation_chart, air_pollution_chart) -> ft.Control:
        """
        Costruisce il layout principale responsivo dell'applicazione con design moderno.
        Layout: sidebar + info + air condition in alto, previsioni orarie full-width sotto, grafici in basso.
        
        Args:
            sidebar: Container della barra laterale
            info: Container delle informazioni principali meteo
            hourly: Container delle previsioni orarie
            air_pollution: Container delle informazioni sull'inquinamento (air condition)
            chart: Container del grafico temperature
            precipitation_chart: Container del grafico precipitazioni
            
        Returns:
            ft.Column: Layout principale con previsioni orarie full-width
        """
        return ft.Column([
            # Layout orizzontale principale (sidebar + info + air condition)
            ft.ResponsiveRow([
                # Sidebar sinistra più ampia (33% larghezza desktop)
                ft.Container(
                    content=sidebar,
                    col={"sm": 12, "md": 5, "lg": 4, "xl": 4},
                    padding=ft.padding.only(left=16, top=16, bottom=16, right=12),
                ),
                
                # Area contenuto principale (67% larghezza desktop)
                ft.Container(
                    content=ft.Column([
                        # Header principale con info meteo - hero section
                        ft.ResponsiveRow([
                            ft.Container(
                                content=info,
                                #col={"sm": 12, "md": 7, "lg": 8, "xl": 8},
                                padding=ft.padding.symmetric(vertical=4),
                            )
                        ]),
                        
                        # Air Condition (ora posizionato dopo le info principali)
                        ft.ResponsiveRow([
                            ft.Container(
                                content=air_pollution,  # Questo è il container Air Condition
                                col={"xs": 12},
                                padding=ft.padding.symmetric(vertical=4),
                            )
                        ]),
                    ], spacing=16),
                    col={"sm": 12, "md": 7, "lg": 8, "xl": 8},
                    padding=ft.padding.only(left=12, top=16, bottom=16, right=16),
                )
            ], spacing=0),
            
            # Previsioni orarie - full width (occupa tutta la larghezza della finestra)
            ft.ResponsiveRow([
                ft.Container(
                    content=hourly,
                    col={"xs": 12},  # Sempre 100% della larghezza
                    padding=ft.padding.symmetric(vertical=4),
                )
            ]),
            
            # Layout orizzontale per grafici - full width
            ft.ResponsiveRow([
                # Grafico temperature
                ft.Container(
                    content=chart,
                    col={"sm": 12, "md": 12, "lg": 4, "xl": 4},
                    padding=ft.padding.symmetric(vertical=4),
                ),
                
                # Grafico precipitazioni
                ft.Container(
                    content=precipitation_chart,
                    col={"sm": 12, "md": 12, "lg": 4, "xl": 4},
                    padding=ft.padding.symmetric(vertical=4),
                ),
                
                # Grafico inquinamento aria
                ft.Container(
                    content=air_pollution_chart,
                    col={"sm": 12, "md": 12, "lg": 4, "xl": 4},
                    padding=ft.padding.only(left=8, right=16, top=4, bottom=16),
                )
            ])
        ], spacing=0)