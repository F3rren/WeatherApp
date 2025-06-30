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
            ),
            col=col_size
        )

    @staticmethod
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
            air_pollution_chart: Container del grafico inquinamento aria
            
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
                                col={"xs": 12},
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
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                )
            ]),
            
            # Layout orizzontale per grafici - full width
            ft.ResponsiveRow([
                # Grafico temperature
                ft.Container(
                    content=chart,
                    col={"sm": 12, "md": 12, "lg": 4, "xl": 4},
                    padding=ft.padding.only(left=16, right=8, top=4, bottom=16),
                ),
                
                # Grafico precipitazioni
                ft.Container(
                    content=precipitation_chart,
                    col={"sm": 12, "md": 12, "lg": 4, "xl": 4},
                    padding=ft.padding.only(left=8, right=8, top=4, bottom=16),
                ),
                
                # Grafico inquinamento aria
                ft.Container(
                    content=air_pollution_chart,
                    col={"sm": 12, "md": 12, "lg": 4, "xl": 4},
                    padding=ft.padding.only(left=8, right=16, top=4, bottom=16),
                )
            ])
        ], spacing=0)

    @staticmethod
    def build_air_condition_grid(air_condition_components, page: ft.Page = None) -> ft.Container:
        """
        Build a responsive grid layout for separated air condition components.
        
        Args:
            air_condition_components: Dictionary with component keys and ft.Container values
            page: Flet page object for theme detection and translation
            
        Returns:
            ft.Container: Grid container with air condition components and title
        """
        if not air_condition_components:
            return ft.Container(
                content=ft.Text("Loading air conditions...", size=14),
                height=200,
                alignment=ft.alignment.center
            )

        # Get translation service for title
        translation_service = None
        if page and hasattr(page, 'session'):
            translation_service = page.session.get('translation_service')
        
        # Get current language from state manager
        current_language = "en"  # Default fallback
        if page and hasattr(page, 'session') and page.session.get('state_manager'):
            state_manager = page.session.get('state_manager')
            current_language = state_manager.get_state('language') or current_language
        
        # Get translated title
        title_text = "Air Conditions"  # Default fallback
        if translation_service:
            title_text = translation_service.translate_from_dict(
                "air_condition_items", 
                "air_condition_title", 
                current_language
            ) or title_text

        # Initialize text handler for title sizing
        text_handler = LayoutBuilder.init_text_handler(page)
        title_size = 22  # Default size (axis_title + 2)
        if text_handler:
            title_size = text_handler.get_size('axis_title') + 2 or 22

        # Get theme colors
        is_dark = page.theme_mode == ft.ThemeMode.DARK if page else False
        
        # Get correct text color from theme (same as other components)
        from utils.config import LIGHT_THEME, DARK_THEME
        theme = DARK_THEME if is_dark else LIGHT_THEME
        title_color = theme.get("TEXT", ft.Colors.BLACK)

        # Get components in preferred order (now grouped)
        components_order = [
            "temperature", "humidity_air", "wind", "atmospheric", "solar"  # Group names
        ]
        
        responsive_components = []
        
        for comp_key in components_order:
            if comp_key in air_condition_components:
                responsive_components.append(ft.Container(
                    content=air_condition_components[comp_key],
                    col={"sm": 12, "md": 6, "lg": 4, "xl": 3},  # Mobile: 1 col, Tablet: 2 cols, Desktop: 3 cols, Large: 4 cols
                    padding=4,
                ))
        
        # Create the main title with icon (same style as other components)
        title_container = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.AIR_OUTLINED,
                    color=ft.Colors.BLUE_400 if not is_dark else ft.Colors.BLUE_300,
                    size=24
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    title_text,
                    size=title_size,
                    weight=ft.FontWeight.BOLD,
                    color=title_color,
                    font_family="system-ui",
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=16, bottom=12)
        )

        # Create responsive grid layout with title
        return ft.Container(
            content=ft.Column([
                title_container,
                ft.ResponsiveRow(responsive_components, spacing=8)
            ], spacing=0),
            padding=8,
        )
