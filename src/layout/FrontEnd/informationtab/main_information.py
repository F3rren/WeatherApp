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
        """Constructs the UI elements for the main weather information."""
        try:
            if not self._text_handler:
                logging.error(f"MainWeatherInfo ({self._city_data}): Text handler is None in build.")
                return ft.Text("Error: Text handler not available.", color=ft.Colors.RED)

            # Format temperature
            unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
            formatted_temp = f"{self._temperature_data}{unit_symbol}"

            city_text_control = ft.Text(
                self._city_data.split(", ")[0],
                size=self._text_handler.get_size('city'),
                weight="bold",
                color=self._current_text_color,
                data={"category": "city"}
            )

            location_text_control = ft.Text(
                f"{self._location_data}",
                size=self._text_handler.get_size('location'),
                color=self._current_text_color,
                data={"category": "location"}
            )

            temperature_text_control = ft.Text(
                formatted_temp,
                size=self._text_handler.get_size('temperature'),
                weight="bold",
                color=self._current_text_color,
                data={"category": "temperature"}
            )

            controls = [
                city_text_control,
                location_text_control if self._location_data else None,
                temperature_text_control,
            ]
            controls = [c for c in controls if c is not None]

            return ft.Container(
                content=ft.ResponsiveRow(
                    [
                        ft.Container(
                            ft.Column(
                                controls=controls,
                                expand=True,
                            ),
                            padding=ft.padding.all(5),
                        ),
                    ],
                    expand=True,
                ),
                padding=self.padding if self.padding is not None else ft.padding.all(20),
                expand=self.expand if self.expand is not None else True,
                alignment=ft.alignment.center,
            )
        except Exception as e:
            logging.error(f"MainWeatherInfo ({self._city_data}): Failed to build UI elements: {e}\nTraceback: {traceback.format_exc()}")
            return ft.Text(f"Error displaying {self._city_data}", color=ft.Colors.RED)
