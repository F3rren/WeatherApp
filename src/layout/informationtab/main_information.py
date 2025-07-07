import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
import logging
from services.translation_service import TranslationService
from components.responsive_text_handler import ResponsiveTextHandler
import traceback

class MainWeatherInfo(ft.Container):
    """
    Main weather information display.
    Manages its own UI build and updates based on state changes.
    """

    def __init__(self, city: str, location: str, temperature: int,
                 weather_icon: str, page: ft.Page = None, **kwargs):
        super().__init__(**kwargs)
        self._city_data = city.upper()
        self._location_data = location
        self._temperature_data = temperature
        self._weather_icon_data = weather_icon
        self._weather_description = ""
        self._feels_like = None
        self._temp_min = None
        self._temp_max = None
        self.page = page

        # Initialize state variables
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_unit_system = DEFAULT_UNIT_SYSTEM
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)

        # Initialize ResponsiveTextHandler
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'city': 36,
                'location': 20,
                'temperature': 40,
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        self.content = ft.Text("Loading Main Info...")

        # Setup observers and handlers
        if self.page:
            if self._text_handler and not self._text_handler.page:
                self._text_handler.page = self.page
        # Setup state manager
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
        
        self.content = self.build()

    def update(self):
        """Updates state and rebuilds the UI without fetching new data."""
        if not self.page or not self.visible:
            return

        try:
            # Update state from state_manager
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                new_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
                
                self._current_language = new_language
                self._current_unit_system = new_unit_system

            # Update theme color
            if self.page and self.page.theme_mode:
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
                current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
                self._current_text_color = current_theme_config.get("TEXT", ft.Colors.BLACK)
            else:
                self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)

            # Rebuild and update UI
            self.content = self.build()
            
            # Update the component itself
            try:
                super().update()
            except (AssertionError, AttributeError):
                # Component not yet added to page, skip update
                pass
            
            # Also try to update the parent container if possible
            if hasattr(self, 'parent') and self.parent:
                try:
                    self.parent.update()
                except (AssertionError, AttributeError):
                    pass

        except Exception as e:
            logging.error(f"MainWeatherInfo: Error updating: {e}\n{traceback.format_exc()}")

    def build(self):
        """Costruisce la UI principale con testo tradotto e dati API."""
        try:
            if not self._text_handler:
                logging.error(f"MainWeatherInfo ({self._city_data}): Text handler is None in build.")
                return ft.Text("Error: Text handler not available.", color=ft.Colors.RED)

            # Format temperature unit symbol
            unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)

            # Usa la descrizione già tradotta dalla API
            weather_description = (self._weather_description or "").capitalize()

            # Mostra anche il feels_like se disponibile
            feels_like_str = ""
            if self._feels_like is not None:
                # Get translation service from session for dynamic language updates
                translation_service = None
                if self.page and hasattr(self.page, 'session'):
                    translation_service = self.page.session.get('translation_service')
                
                feels_like_label = "Feels like"  # Default fallback
                if translation_service:
                    feels_like_label = translation_service.translate_from_dict(
                        "air_condition_items", "feels_like", self._current_language
                    ) or "Feels like"
                else:
                    # Fallback to static method
                    feels_like_label = TranslationService.translate_from_dict("air_condition_items", "feels_like", self._current_language)
                
                feels_like_str = f"{feels_like_label} {self._feels_like}{unit_symbol}"

            # Unisce descrizione e feels_like
            description_line = weather_description
            if feels_like_str:
                description_line = f"{weather_description} • {feels_like_str}"

            # Determine weather icon and color based on weather icon code
            weather_icon = ft.Icons.WB_SUNNY
            icon_color = ft.Colors.ORANGE_400
            bg_color = ft.Colors.ORANGE_400
            
            if self._weather_icon_data:
                icon_code = self._weather_icon_data
                is_day = icon_code.endswith('d')
                
                if icon_code.startswith('01'):  # Clear sky
                    weather_icon = ft.Icons.WB_SUNNY if is_day else ft.Icons.NIGHTLIGHT_ROUND
                    icon_color = ft.Colors.ORANGE_400 if is_day else ft.Colors.INDIGO_300
                    bg_color = ft.Colors.ORANGE_400 if is_day else ft.Colors.INDIGO_400
                elif icon_code.startswith(('02', '03', '04')):  # Clouds
                    weather_icon = ft.Icons.CLOUD
                    icon_color = ft.Colors.GREY_600 if is_day else ft.Colors.BLUE_GREY_400
                    bg_color = ft.Colors.GREY_500 if is_day else ft.Colors.BLUE_GREY_600
                elif icon_code.startswith(('09', '10')):  # Rain
                    weather_icon = ft.Icons.WATER_DROP
                    icon_color = ft.Colors.BLUE_500
                    bg_color = ft.Colors.BLUE_500
                elif icon_code.startswith('11'):  # Thunderstorm
                    weather_icon = ft.Icons.FLASH_ON
                    icon_color = ft.Colors.PURPLE_500
                    bg_color = ft.Colors.PURPLE_600
                elif icon_code.startswith('13'):  # Snow
                    weather_icon = ft.Icons.AC_UNIT
                    icon_color = ft.Colors.LIGHT_BLUE_400
                    bg_color = ft.Colors.LIGHT_BLUE_300
                elif icon_code.startswith('50'):  # Mist/Fog
                    weather_icon = ft.Icons.FOGGY
                    icon_color = ft.Colors.BLUE_GREY_400
                    bg_color = ft.Colors.BLUE_GREY_400

            # Create header with location - design moderno
            location_header = ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.MY_LOCATION,
                        size=18, 
                        #color=ft.Colors.with_opacity(0.8, self._current_text_color)
                        color=ft.Colors.RED
                    ),
                    ft.Text(
                        f"{self._city_data.split(', ')[0]}",
                        size=18,
                        color=self._current_text_color,
                        weight="w500"
                    ),
                    ft.Container(
                        content=ft.Text(
                            self._location_data,
                            size=14,
                            color=ft.Colors.with_opacity(0.7, self._current_text_color),
                            weight="w400"
                        ),
                        padding=ft.padding.only(left=8)
                    ),
                ], alignment=ft.MainAxisAlignment.START, spacing=6),
                margin=ft.margin.only(bottom=24)
            )

            # Create main weather section with temperature and icon - design hero migliorato
            weather_main_section = ft.Container(
                content=ft.Column([
                    # Temperature and icon on same row
                    ft.Row([
                        ft.Text(
                            str(self._temperature_data),
                            size=72,
                            weight="w200",
                            color=self._current_text_color,
                        ),
                        ft.Container(
                            content=ft.Text(
                                unit_symbol,
                                size=24,
                                weight="w300",
                                color=ft.Colors.with_opacity(0.8, self._current_text_color),
                            ),
                            padding=ft.padding.only(top=6)
                        ),
                        # Weather icon inline with temperature
                        ft.Container(
                            content=ft.Container(
                                content=ft.Icon(
                                    weather_icon,
                                    size=64,
                                    color=ft.Colors.WHITE,
                                ),
                                width=96,
                                height=96,
                                border_radius=24,
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_left,
                                    end=ft.alignment.bottom_right,
                                    colors=[
                                        ft.Colors.with_opacity(0.9, bg_color),
                                        ft.Colors.with_opacity(0.7, bg_color),
                                    ]
                                ),
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=16,
                                    color=ft.Colors.with_opacity(0.25, bg_color),
                                    offset=ft.Offset(0, 6),
                                ),
                                alignment=ft.alignment.center,
                            ),
                            margin=ft.margin.only(left=24)
                        ),
                    ], alignment=ft.MainAxisAlignment.START, spacing=2),
                    
                    # Weather description con stile moderno
                    ft.Container(
                        content=ft.Text(
                            description_line,
                            size=16,
                            color=ft.Colors.with_opacity(0.85, self._current_text_color),
                            weight="w400"
                        ),
                        margin=ft.margin.only(top=8, bottom=24)
                    ),
                    
                    # High/Low temperatures con design cards migliorato
                    ft.Row([
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(
                                    ft.Icons.KEYBOARD_ARROW_UP,
                                    size=18,
                                    color=ft.Colors.RED_400,
                                ),
                                ft.Column([
                                    ft.Text(
                                        TranslationService.translate_from_dict('main_information_items', 'high', self._current_language).upper(),
                                        size=10,
                                        color=ft.Colors.with_opacity(0.6, self._current_text_color),
                                        weight="w500"
                                    ),
                                    ft.Text(
                                        f"{self._temp_max}{unit_symbol}",
                                        size=15,
                                        color=self._current_text_color,
                                        weight="w600"
                                    ),
                                ], spacing=1, alignment=ft.MainAxisAlignment.CENTER),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                            padding=ft.padding.symmetric(horizontal=14, vertical=10),
                            border_radius=16,
                            bgcolor=ft.Colors.with_opacity(0.08, self._current_text_color),
                            border=ft.border.all(1, ft.Colors.with_opacity(0.12, self._current_text_color)),
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(
                                    ft.Icons.KEYBOARD_ARROW_DOWN,
                                    size=18,
                                    color=ft.Colors.BLUE_400,
                                ),
                                ft.Column([
                                    ft.Text(
                                        TranslationService.translate_from_dict('main_information_items', 'low', self._current_language).upper(),
                                        size=10,
                                        color=ft.Colors.with_opacity(0.6, self._current_text_color),
                                        weight="w500"
                                    ),
                                    ft.Text(
                                        f"{self._temp_min}{unit_symbol}",
                                        size=15,
                                        color=self._current_text_color,
                                        weight="w600"
                                    ),
                                ], spacing=1, alignment=ft.MainAxisAlignment.CENTER),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                            padding=ft.padding.symmetric(horizontal=14, vertical=10),
                            border_radius=16,
                            bgcolor=ft.Colors.with_opacity(0.08, self._current_text_color),
                            border=ft.border.all(1, ft.Colors.with_opacity(0.12, self._current_text_color)),
                            expand=True,
                        ),
                    ], spacing=12),
                ], alignment=ft.MainAxisAlignment.START, spacing=0)
            )

            return ft.Container(
                content=ft.Column([
                    location_header,
                    weather_main_section,
                ], alignment=ft.MainAxisAlignment.START, spacing=0),
                padding=ft.padding.symmetric(horizontal=32, vertical=28),  # Padding più generoso
                expand=True,
                alignment=ft.alignment.center_left,
            )
        except Exception as e:
            logging.error(f"MainWeatherInfo ({self._city_data}): Failed to build UI elements: {e}\nTraceback: {traceback.format_exc()}")
            return ft.Text(f"Error displaying {self._city_data}", color=ft.Colors.RED)
        except Exception as e:
            logging.error(f"MainWeatherInfo ({self._city_data}): Failed to build UI elements: {e}\nTraceback: {traceback.format_exc()}")
            return ft.Text(f"Error displaying {self._city_data}", color=ft.Colors.RED)
