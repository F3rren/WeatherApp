import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
import logging
from services.translation_service import TranslationService
from components.responsive_text_handler import ResponsiveTextHandler
import traceback
import asyncio

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
            
            if hasattr(self.page, 'session') and self.page.session.get('state_manager'):
                self._state_manager = self.page.session.get('state_manager')
                # NOTE: Without a dedicated cleanup method (like will_unmount),
                # these observers are never unregistered.
                self._state_manager.register_observer("language_event", self.update_ui)
                self._state_manager.register_observer("unit_event", self.update_ui)
                self._state_manager.register_observer("theme_event", self.update_ui)
            
            original_on_resize = self.page.on_resize
            def resize_handler(e):
                if original_on_resize:
                    original_on_resize(e)
                if self._text_handler:
                    self._text_handler._handle_resize(e)
                if self.page:
                    self.page.run_task(self.update_ui)
            self.page.on_resize = resize_handler

            # Initial update
            self.page.run_task(self.update_ui)

    async def update_ui(self, event_data=None):
        """Fetches data, updates state, and rebuilds the UI."""
        if not self.page or not self.visible:
            return

        try:
            # Update state from state_manager
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                new_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
                
                language_changed = self._current_language != new_language
                unit_changed = self._current_unit_system != new_unit_system

                self._current_language = new_language
                self._current_unit_system = new_unit_system

                # Fetch data if language or unit changed
                if language_changed or unit_changed:
                    from services.api_service import ApiService
                    api = ApiService()
                    weather_data = await asyncio.to_thread(
                        api.get_weather_data,
                        city=self._city_data,
                        language=self._current_language,
                        unit=self._current_unit_system
                    )
                    temp = api.get_current_temperature(weather_data)
                    if temp is not None:
                        self._temperature_data = temp
                    # Aggiorna anche descrizione, feels_like, min/max
                    self._weather_description = api.get_weather_description(weather_data)
                    self._feels_like = api.get_feels_like_temperature(weather_data)
                    tmin, tmax = api.get_min_max_temperature(weather_data)
                    self._temp_min = tmin
                    self._temp_max = tmax

            # Update theme color
            if self.page and self.page.theme_mode:
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
                current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
                self._current_text_color = current_theme_config.get("TEXT", ft.Colors.BLACK)
            else:
                self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)

            # Rebuild and update UI
            self.content = self.build()
            if self.page:
                self.page.update()

        except Exception as e:
            logging.error(f"MainWeatherInfo: Error updating UI: {e}\n{traceback.format_exc()}")

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

            # Create header with location
            location_header = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON, size=16, color=self._current_text_color),
                    ft.Text(
                        f"{self._city_data.split(', ')[0]} - {self._location_data}",
                        size=14,
                        color=self._current_text_color,
                        weight="w400"
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                padding=ft.padding.only(bottom=10)
            )

            # Create main weather section with temperature and large icon on same line
            weather_main_section = ft.Container(
                content=ft.Column([
                    # Temperature and large icon on same row
                    ft.Row([
                        # Left side: Temperature
                        ft.Row([
                            ft.Text(
                                str(self._temperature_data),
                                size=72,  # Very large temperature
                                weight="w300",  # Light weight for modern look
                                color=self._current_text_color,
                            ),
                            ft.Text(
                                unit_symbol,
                                size=24,
                                weight="w300",
                                color=self._current_text_color,
                            ),
                        ], alignment=ft.MainAxisAlignment.START, spacing=5),
                        
                        # Right side: Large weather icon
                        ft.Container(
                            content=ft.Icon(
                                weather_icon,
                                size=64,  # Large icon but not too big for same line
                                color=ft.Colors.WHITE,
                            ),
                            width=80,
                            height=80,
                            border_radius=40,
                            bgcolor=ft.Colors.with_opacity(0.8, bg_color),
                            shadow=ft.BoxShadow(
                                spread_radius=2,
                                blur_radius=12,
                                color=ft.Colors.with_opacity(0.3, bg_color),
                                offset=ft.Offset(0, 4),
                            ),
                            alignment=ft.alignment.center,
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
                    
                    # Weather description
                    ft.Container(
                        content=ft.Text(
                            description_line,
                            size=16,
                            color=self._current_text_color,
                            weight="w400"
                        ),
                        padding=ft.padding.only(top=15, bottom=15)
                    ),
                    
                    # Today's additional info (high/low temperatures)
                    ft.Row([
                        ft.Text(
                            f"{TranslationService.translate_from_dict('main_information_items', 'high', self._current_language).capitalize()}: {self._temp_max}{unit_symbol}",
                            size=14, color=self._current_text_color),
                        ft.Text(
                            f"{TranslationService.translate_from_dict('main_information_items', 'low', self._current_language).capitalize()}: {self._temp_min}{unit_symbol}",
                            size=14, color=self._current_text_color),
                       ], spacing=20),
                ], alignment=ft.MainAxisAlignment.START, spacing=0),
                padding=ft.padding.only(bottom=10)
            )

            return ft.Container(
                content=ft.Column([
                    location_header,
                    weather_main_section,
                ], alignment=ft.MainAxisAlignment.START, spacing=0),
                padding=ft.padding.all(30),
                expand=True,
                alignment=ft.alignment.center_left,  # Align to left like in the design
            )
        except Exception as e:
            logging.error(f"MainWeatherInfo ({self._city_data}): Failed to build UI elements: {e}\nTraceback: {traceback.format_exc()}")
            return ft.Text(f"Error displaying {self._city_data}", color=ft.Colors.RED)
        except Exception as e:
            logging.error(f"MainWeatherInfo ({self._city_data}): Failed to build UI elements: {e}\nTraceback: {traceback.format_exc()}")
            return ft.Text(f"Error displaying {self._city_data}", color=ft.Colors.RED)
