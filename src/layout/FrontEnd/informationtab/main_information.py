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
        logger = logging.getLogger(__name__)
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._current_language = self._state_manager.get_state('language') or self._current_language
            self._current_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
            
            self._state_manager.register_observer("theme_event", self._request_ui_rebuild)
            self._state_manager.register_observer("unit", self._request_ui_rebuild)
            self._state_manager.register_observer("language_event", self._request_ui_rebuild)
            logger.debug(f"MainWeatherInfo ({self._city_data}): State manager observers registered.")
        else:
            logger.warning(f"MainWeatherInfo ({self._city_data}): State manager not found. Using defaults.")

        if self._text_handler and hasattr(self._text_handler, 'add_observer'):
            self._text_handler.add_observer(self._request_ui_rebuild) # Rebuild UI on text size change
            logger.debug(f"MainWeatherInfo ({self._city_data}): ResponsiveTextHandler observer registered.")
        else:
            logger.warning(f"MainWeatherInfo ({self._city_data}): Text handler does not support observers or not available.")

    def will_unmount(self):
        """Called when the control is removed from the page."""
        logger = logging.getLogger(__name__)
        if self._state_manager:
            self._state_manager.unregister_observer("theme_event", self._request_ui_rebuild)
            self._state_manager.unregister_observer("unit", self._request_ui_rebuild)
            self._state_manager.unregister_observer("language_event", self._request_ui_rebuild)
            logger.debug(f"MainWeatherInfo ({self._city_data}): State manager observers unregistered.")
        
        if self._text_handler and hasattr(self._text_handler, 'remove_observer'):
            try:
                self._text_handler.remove_observer(self._request_ui_rebuild)
                logger.debug(f"MainWeatherInfo ({self._city_data}): ResponsiveTextHandler observer unregistered.")
            except Exception as e:
                logger.error(f"MainWeatherInfo ({self._city_data}): Error unregistering from text_handler: {e}")
        
    def _determine_text_color_from_theme(self):
        """Determines text color based on the current page theme."""
        if self.page and self.page.theme_mode:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config.get("TEXT", ft.Colors.BLACK)
        return LIGHT_THEME.get("TEXT", ft.Colors.BLACK) # Overall fallback

    def _safe_update(self):
        if getattr(self, "page", None) and getattr(self, "visible", True):
            self.update()

    def _request_ui_rebuild(self, event_data=None):
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

            city_text_control = ft.Text(
                self._city_data.split(", ")[0],
                size=self._text_handler.get_size('city'),
                weight="bold",
                color=self._current_text_color
            )
            
            location_text_control = ft.Text(
                self._location_data,
                size=self._text_handler.get_size('location'),
                color=self._current_text_color
            )
            
            temperature_text_control = ft.Text(
                self._get_formatted_temperature(),
                size=self._text_handler.get_size('temperature'),
                weight="bold",
                color=self._current_text_color
            )
            
            # Placeholder for weather icon if it needs to be displayed
            # weather_icon_control = ft.Image(
            #     src=f"https://openweathermap.org/img/wn/{self._weather_icon_data}@2x.png", # Example
            #     width=self._text_handler.get_size('icon', 50), # Assuming an 'icon' size in text_handler
            #     height=self._text_handler.get_size('icon', 50),
            #     fit=ft.ImageFit.CONTAIN
            # )

            return ft.Container(
                content=ft.ResponsiveRow(
                    [
                        ft.Container(
                            ft.Column(
                                controls=[
                                    city_text_control,
                                    location_text_control,
                                    temperature_text_control,
                                    # weather_icon_control, # Add if displaying icon
                                ],
                                expand=True, 
                                # horizontal_alignment=ft.CrossAxisAlignment.START, # Default
                                # spacing=5, # Adjust spacing between text elements
                            ),
                            padding=ft.padding.all(5), # Padding for the column container
                        ),
                    ],
                    expand=True, 
                    # alignment=ft.MainAxisAlignment.CENTER, # Center content in ResponsiveRow
                    # vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=self.padding if self.padding is not None else ft.padding.all(20),
                expand=self.expand if self.expand is not None else True, # Usually True if it's a main block
                alignment=ft.alignment.center, # Center the ResponsiveRow within MainWeatherInfo container
                # bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE) # For debugging layout
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

    def handle_theme_change(self, event_data=None):
        """Updates the text color based on the current theme."""
        if not self.page:
            return
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
        self.text_color = current_theme_config["TEXT"]
        controls = {"city_text": self.city_text, "location_text": self.location_text, "temperature_text": self.temperature_text}
        for name, control_obj in controls.items():
            if control_obj is not None:
                if hasattr(control_obj, 'color'):
                    control_obj.color = self.text_color
        # RIMOSSO: self.page.update()
    
    def _update_text_elements(self):
        """Updates only the text elements without rebuilding the entire UI"""
        if not self.content or not isinstance(self.content, ft.Column):
            return
        
        # Find and update text controls
        for container in self.content.controls:
            if isinstance(container, ft.Container) and container.content:
                # First container should be the location/city info
                if isinstance(container.content, ft.Column):
                    for text_control in container.content.controls:
                        if isinstance(text_control, ft.Text):
                            # City or Location text
                            category = getattr(text_control, "data", {}).get("category")
                            if category == "city":
                                text_control.value = self._city_data.split(", ")[0]
                                text_control.update()
                            elif category == "location":
                                text_control.value = self._location_data
                                text_control.update()
                
                # Temperature text
                elif isinstance(container.content, ft.Row):
                    for text_control in container.content.controls:
                        if isinstance(text_control, ft.Text):
                            if getattr(text_control, "data", {}).get("category") == "temperature":
                                text_control.value = self._get_formatted_temperature()
                                text_control.update()
                            elif getattr(text_control, "data", {}).get("category") == "weather_condition":
                                weather_key = getattr(text_control, "data", {}).get("weather_key")
                                if weather_key:
                                    text_control.value = TranslationService.get_text(weather_key, self._current_language)
                                    text_control.update()
        
        self.update()

    def _handle_language_change(self, event_data=None):
        """Handles language changes by updating text elements"""
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_language_change received unexpected event_data type: {type(event_data)}")
            
        if self._state_manager:
            new_language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
            if self._current_language != new_language:
                self._current_language = new_language
                self._update_text_elements()
        
    def _handle_unit_change(self, event_data=None):
        """Handles unit system changes by updating text elements"""
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_unit_change received unexpected event_data type: {type(event_data)}")
            
        if self._state_manager:
            new_unit = self._state_manager.get_state('unit') or "metric"
            if self._current_unit_system != new_unit:
                self._current_unit_system = new_unit
                self._update_text_elements()

# Old methods like __init__ (original), update_text_controls, _update_temperature_display, 
# cleanup, handle_unit_change, handle_language_change, handle_theme_change, and build
# are now effectively replaced or integrated into the new structure.
