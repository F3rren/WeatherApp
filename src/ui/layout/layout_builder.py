"""
Layout Builder for the MeteoApp.
Centralizes layout building functions for different UI components.
"""

import flet as ft

class LayoutBuilder:
    """
    Classe utility per costruire elementi di layout per l'applicazione.
    """
 
    @staticmethod
    def build_content_container(content, animation_duration=500, 
                               animation_curve=ft.AnimationCurve.EASE_IN_OUT, 
                               container_type="default") -> ft.Container:
        """
        Crea un container responsive con animazioni e stile moderno ottimizzato per tutti i dispositivi.
        
        Args:
            content: Contenuto del container
            animation_duration: Durata delle animazioni
            animation_curve: Curva di animazione
            container_type: Tipo di container per styling specifico
            
        Returns:
            ft.Container: Container configurato con stile responsive
        """
        # Styling responsive specifico per tipo di container
        if container_type == "main_info":
            # Info principale - ridotto padding su mobile
            border_radius = 20  # Ridotto per mobile
            padding = ft.padding.symmetric(horizontal=16, vertical=16)  # Ridotto padding
            margin = ft.margin.only(bottom=8, left=4, right=4)  # Margini adattivi
            shadow_blur = 16
            shadow_spread = 0
        elif container_type == "sidebar":
            # Sidebar - padding adattivo
            border_radius = 16
            padding = ft.padding.all(12)  # Ridotto per mobile
            margin = ft.margin.all(4)  # Margini ridotti
            shadow_blur = 12
            shadow_spread = 0
        else:
            # Container standard - ottimizzato per mobile
            border_radius = 12  # Ridotto per mobile
            padding = ft.padding.all(12)  # Padding ridotto
            margin = ft.margin.symmetric(horizontal=4, vertical=4)  # Margini ridotti
            shadow_blur = 8
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
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),  # Ombra più leggera
                offset=ft.Offset(0, 2),  # Offset ridotto
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
            expand=True,  # Consente al container di espandersi
        )

    def build_main_layout(sidebar, info, hourly, chart, precipitation_chart, air_pollution) -> ft.Control:
        """
        Costruisce il layout principale responsivo dell'applicazione con design moderno.
        Layout migliorato per telefono, tablet e desktop con breakpoint ottimizzati.
        
        Args:
            sidebar: Container della barra laterale
            info: Container delle informazioni principali meteo
            hourly: Container delle previsioni orarie
            air_pollution: Container delle informazioni sull'inquinamento (air condition)
            chart: Container del grafico temperature
            precipitation_chart: Container del grafico precipitazioni
            
        Returns:
            ft.Column: Layout principale responsive ottimizzato per tutti i dispositivi
        """
        
        # Layout principale con scroll automatico per dispositivi mobili
        main_content = ft.Column([
            # Layout orizzontale principale (sidebar + info)
            ft.ResponsiveRow([
                # Sidebar - layout responsive migliorato
                ft.Container(
                    content=sidebar,
                    col={
                        "xs": 12,    # Mobile: full width, sidebar in alto
                        "sm": 12,    # Tablet portrait: full width 
                        "md": 4,     # Tablet landscape: 33%
                        "lg": 3,     # Desktop: 25% (più spazio per content)
                        "xl": 3      # Large desktop: 25%
                    },
                    # padding=ft.padding.only(left=8, top=8, bottom=8, right=8),
                ),
                
                # Area contenuto principale - responsive migliorato
                ft.Container(
                    content=ft.Column([
                        # Header principale con info meteo
                        ft.ResponsiveRow([
                            ft.Container(
                                content=info,
                                col={"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 12},
                                padding=ft.padding.symmetric(vertical=4, horizontal=4),
                            )
                        ]),
                    ], spacing=8),
                    col={
                        "xs": 12,    # Mobile: full width sotto sidebar
                        "sm": 12,    # Tablet portrait: full width sotto sidebar
                        "md": 8,     # Tablet landscape: 67%
                        "lg": 9,     # Desktop: 75%
                        "xl": 9      # Large desktop: 75%
                    },
                    # padding=ft.padding.only(left=8, top=8, bottom=8, right=8),
                )
            ], spacing=0),
            
            # Previsioni orarie - responsive con scroll orizzontale su mobile
            ft.ResponsiveRow([
                ft.Container(
                    content=hourly,
                    col={"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 12},
                    padding=ft.padding.symmetric(vertical=4, horizontal=8),
                )
            ]),
            
            # Layout per grafici - stack verticale su mobile, grid su desktop
            ft.ResponsiveRow([
                # Grafico temperature
                ft.Container(
                    content=chart,
                    col={
                        "xs": 12,    # Mobile: full width, stack verticale
                        "sm": 12,    # Tablet portrait: full width
                        "md": 6,     # Tablet landscape: 50%
                        "lg": 4,     # Desktop: 33%
                        "xl": 4      # Large desktop: 33%
                    },
                    # padding=ft.padding.symmetric(vertical=4, horizontal=4),
                ),
                
                # Grafico precipitazioni
                ft.Container(
                    content=precipitation_chart,
                    col={
                        "xs": 12,    # Mobile: full width, stack verticale
                        "sm": 12,    # Tablet portrait: full width
                        "md": 6,     # Tablet landscape: 50%
                        "lg": 4,     # Desktop: 33%
                        "xl": 4      # Large desktop: 33%
                    },
                    # padding=ft.padding.symmetric(vertical=4, horizontal=4),
                ),
                
                # Grafico inquinamento aria
                ft.Container(
                    content=air_pollution,
                    col={
                        "xs": 12,    # Mobile: full width, stack verticale
                        "sm": 12,    # Tablet portrait: full width
                        "md": 12,    # Tablet landscape: full width sotto altri grafici
                        "lg": 4,     # Desktop: 33%
                        "xl": 4      # Large desktop: 33%
                    },
                    # padding=ft.padding.symmetric(vertical=4, horizontal=4),
                )
            ])
        ], 
        spacing=8,  # Spacing ridotto per mobile
        scroll=ft.ScrollMode.AUTO,  # Scroll automatico per contenuto che eccede altezza viewport
        )
        
        # Wrapper container con configurazioni responsive
        return ft.Container(
            content=main_content,
            expand=True,
            # padding=ft.padding.symmetric(horizontal=4, vertical=4),  # Padding minimale per mobile
        )