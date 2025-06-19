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
        
        self._passed_page_ref = page

        # Initialize state variables
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_unit_system = DEFAULT_UNIT_SYSTEM
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)

        # Initialize ResponsiveTextHandler
        # Page will be set properly in did_mount if not available now
        self._text_handler = ResponsiveTextHandler(
            page=self._passed_page_ref,
            base_sizes={
                'city': 36,
                'location': 20,
                'temperature': 40,
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Initial content placeholder
        self.content = ft.Text("Loading Main Info...")
          # To store the original page.on_resize if we decide to use it.
        self._original_page_resize_handler = None
        
    def did_mount(self):
        """Called when the control is added to the page."""
        if self.page and self._text_handler:
            if not self._text_handler.page:
                self._text_handler.page = self.page
                logging.debug(f"MainWeatherInfo ({self._city_data}): Text handler page set in did_mount.")

        self._initialize_state_and_observers()
        self._request_ui_rebuild()

    def _initialize_state_and_observers(self):
        """Initializes state manager and registers observers."""
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._current_language = self._state_manager.get_state('language') or self._current_language
            self._current_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
            self._state_manager.register_observer("language_event", self._handle_language_or_unit_change)
            self._state_manager.register_observer("unit_event", self._handle_language_or_unit_change)
            self._state_manager.register_observer("unit_text_change", self._handle_language_or_unit_change)
            self._state_manager.register_observer("theme_event", self._handle_theme_change)
        
        if self.page:
            self._original_on_resize = self.page.on_resize
            self.page.on_resize = self._combined_resize_handler
            
    def will_unmount(self):
        """Called when the control is removed from the page."""
        if self._state_manager:
            self._state_manager.unregister_observer("language_event", self._handle_language_or_unit_change)
            self._state_manager.unregister_observer("unit_event", self._handle_language_or_unit_change)
            self._state_manager.unregister_observer("unit_text_change", self._handle_language_or_unit_change)            self._state_manager.unregister_observer("theme_event", self._handle_theme_change)
        
        if self.page and hasattr(self, '_original_on_resize'):
            self.page.on_resize = self._original_on_resize

    def _combined_resize_handler(self, e):
        """Handles page resize events for this component."""
        if hasattr(self, '_original_on_resize') and self._original_on_resize:
            self._original_on_resize(e) # Call previously registered handler first

        self._text_handler._handle_resize(e) # Update ResponsiveTextHandler
        self._update_text_and_icon_sizes()   # Update elements within this component

    async def _handle_language_or_unit_change(self, event_data=None):
        """Handles language or unit changes: rebuilds UI if either changes."""
        if self._state_manager:
            new_language = self._state_manager.get_state('language') or self._current_language
            new_unit_system = self._state_manager.get_state('unit') or self._current_unit_system

            language_changed = self._current_language != new_language
            unit_changed = self._current_unit_system != new_unit_system

            self._current_language = new_language
            self._current_unit_system = new_unit_system

            # Rebuild UI if language or unit system changes
            if language_changed or unit_changed:
                await self._fetch_data_and_request_rebuild()

    def _handle_theme_change(self, event_data=None):
        """Handles theme change events by updating the appearance."""
        self._current_text_color = self._determine_text_color_from_theme()
        self._update_text_and_icon_sizes()

    def _determine_text_color_from_theme(self):
        """Determines text color based on the current page theme."""
        if self.page and self.page.theme_mode:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config.get("TEXT", ft.Colors.BLACK)
        return LIGHT_THEME.get("TEXT", ft.Colors.BLACK) # Overall fallback

    def _safe_update(self):
        if getattr(self, "page", None) and getattr(self, "visible", True):
            self.update()    def _request_ui_rebuild(self, event_data=None):
        """Updates state, rebuilds UI, and updates the control - similar to WeeklyForecastDisplay."""
        if not self.page or not self.visible:
            return

        if self._state_manager:
            self._current_language = self._state_manager.get_state('language') or self._current_language
            self._current_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
        
        self._current_text_color = self._determine_text_color_from_theme()
        
        new_content = self._build_ui_elements()
        if self.content != new_content:
            self.content = new_content
            self._safe_update()
        
    def _get_formatted_temperature(self):
        """Formats temperature with the correct unit symbol."""
        unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
        return f"{self._temperature_data}{unit_symbol}"
        
    def _build_ui_elements(self):
        """Constructs the UI elements for the main weather information."""
        try:
            if not self._text_handler:
                logging.error(f"MainWeatherInfo ({self._city_data}): Text handler is None in _build_ui_elements.")
                return ft.Text("Error: Text handler not available.", color=ft.Colors.RED)

            # Use translations for location label if available
            # location_label = TranslationService.translate_from_dict("main_information_items", "current_location", self._current_language)

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
                self._get_formatted_temperature(),
                size=self._text_handler.get_size('temperature'),
                weight="bold",
                color=self._current_text_color,
                data={"category": "temperature"}
            )

            controls=[
                city_text_control,
                # Mostra la posizione solo se la geolocalizzazione è attiva
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

    def handle_resize(self, e=None):
        """
        This method should be called by the parent component when the page resizes.
        It triggers the ResponsiveTextHandler to update sizes, which in turn
        notifies this component (via its observer) to rebuild its UI.
        """
        if self._text_handler:
            # logging.debug(f"MainWeatherInfo ({self._city_data}): handle_resize called, forwarding to text_handler.")
            self._text_handler._handle_resize(e)
        # else:
            # logging.warning(f"MainWeatherInfo ({self._city_data}): handle_resize called, but no text_handler.")

    
    def _update_text_elements(self, event_type=None, data=None):
        """
        Updates specific text elements in the UI.
        - update_temperature: Flag to update the temperature text.
        """
        if not self.content or not isinstance(self.content, ft.Container) or not isinstance(self.content.content, ft.ResponsiveRow):
            return

        responsive_row = self.content.content
        if not responsive_row.controls:
             return
        container = responsive_row.controls[0]
        column = container.content
        
        for control in column.controls:
            if isinstance(control, ft.Text) and hasattr(control, 'data'):
                category = control.data.get("category")
                if event_type and category == "temperature":
                    control.value = self._get_formatted_temperature()
        
        self._safe_update()

    def _handle_unit_change(self, event_data):
        """Handles unit changes from any source (dict from notify_all or str from set_state)."""
        new_unit = None
        if isinstance(event_data, dict) and 'unit' in event_data:
            new_unit = event_data['unit']
        elif isinstance(event_data, str):
            # This handles the direct value from set_state('unit', new_value)
            new_unit = event_data
        
        if new_unit and self._current_unit_system != new_unit:
            logging.info(f"MainWeatherInfo: Unit changed to {new_unit}. Updating temperature display.")
            self._current_unit_system = new_unit
            self._update_text_elements(update_temperature=True)
        elif not new_unit:
            logging.warning(f"MainWeatherInfo: _handle_unit_change received invalid event_data: {event_data}")
