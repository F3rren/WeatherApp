import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME
import logging # Added import for logging

class MainWeatherInfo:
    """
    Main weather information display.
    """

    def __init__(self, city: str, location: str, temperature: int,
                 weather_icon: str, text_color: str, page: ft.Page = None):  # Added page for state_manager access
        self.city = city.upper()  # Changed to accept city name as string
        self.location = location
        self.temperature = temperature
        self.weather_icon = weather_icon
        self.text_color = text_color
        self.page = page # Store page to access state_manager if needed for observing theme
        self.language = None
        self._state_manager_ref_for_cleanup = None # To store state_manager if observer is registered

        # Text controls that need dynamic color updates
        self.city_text = ft.Text(
            self.city.split(", ")[0], 
            size=36, 
            weight="bold", 
            color=self.text_color
        ) 
        
        self.location_text = ft.Text(
            self.location, 
            size=20,
            color=self.text_color
        )
        
        self.temperature_text = ft.Text(
            f"{self.temperature}°", 
            size=40,
            weight="bold", 
            color=self.text_color
        )

        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                state_manager.register_observer("theme_event", self.handle_theme_change)
                self._state_manager_ref_for_cleanup = state_manager # Store for cleanup

    def cleanup(self):
        logger = logging.getLogger(__name__)
        if self._state_manager_ref_for_cleanup and hasattr(self._state_manager_ref_for_cleanup, 'unregister_observer'):
            city_name = self.city_text.value if self.city_text and hasattr(self.city_text, 'value') else "N/A"
            logger.info(f"MainWeatherInfo ({city_name}): Attempting to unregister theme_event observer.")
            try:
                self._state_manager_ref_for_cleanup.unregister_observer("theme_event", self.handle_theme_change)
                logger.info(f"MainWeatherInfo ({city_name}): Successfully unregistered theme_event observer.")
            except Exception as e:
                logger.warning(f"MainWeatherInfo ({city_name}): Could not unregister theme_event observer (may not have been registered or already removed): {e}")
        self._state_manager_ref_for_cleanup = None # Clear the reference
        # Optionally, clear references to controls if it helps, though Python's GC should handle it.
        # self.page = None # Avoid potential cycles if page references this instance elsewhere

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color."""
        logger = logging.getLogger(__name__)
        logger.info("MainWeatherInfo: handle_theme_change called.")

        if self.page:
            logger.info(f"MainWeatherInfo: Current page theme_mode: {self.page.theme_mode}")
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]
            logger.info(f"MainWeatherInfo: Calculated text_color: {self.text_color}")

            controls_to_update = {
                "city_text": getattr(self, 'city_text', None),
                "location_text": getattr(self, 'location_text', None),
                "temperature_text": getattr(self, 'temperature_text', None)
            }

            for name, control_obj in controls_to_update.items(): # Renamed variable for clarity
                logger.info(f"MainWeatherInfo: Processing control '{name}'. Object: {control_obj}, Type: {type(control_obj)}")
                if control_obj is not None:
                    if hasattr(control_obj, 'color'):
                        logger.info(f"MainWeatherInfo: Attempting to set color for '{name}'. Current color: {getattr(control_obj, 'color', 'N/A')}, New color: {self.text_color}")
                        try:
                            control_obj.color = self.text_color # THE CRITICAL LINE
                        except Exception as e:
                            logger.error(f"MainWeatherInfo: ERROR during color assignment for '{name}': {e}", exc_info=True)
                            continue # Skip update if color setting failed

                        if getattr(control_obj, 'page', None):
                            try:
                                control_obj.update()
                                logger.info(f"MainWeatherInfo: {name}.update() successfully called.")
                            except Exception as e:
                                logger.error(f"MainWeatherInfo: ERROR during {name}.update(): {e}", exc_info=True)
                        else:
                            logger.warning(f"MainWeatherInfo: {name} is not on page, {name}.update() skipped.")
                    else:
                        # This case should ideally not be reached if control_obj is a standard ft.Text
                        logger.error(f"MainWeatherInfo: Control '{name}' (Object: {control_obj}, Type: {type(control_obj)}) is not None but lacks 'color' attribute.")
                else:
                    logger.warning(f"MainWeatherInfo: Control '{name}' is None. Skipping operations for this control.")

            if getattr(self.page, 'update', None):
                self.page.update()
                logger.info("MainWeatherInfo: self.page.update() called.")
            else:
                logger.warning("MainWeatherInfo: self.page.update is not available or self.page is None.")
        else:
            logger.warning("MainWeatherInfo: self.page is None in handle_theme_change.")

    def build(self) -> ft.Container:
        """Build the main weather information"""
        return ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Container(
                        ft.Column(
                            controls=[
                                self.city_text,
                                self.location_text,
                                self.temperature_text,
                            ],
                            expand=True, 
                        ),
                        padding=5,
                        #col={"xs": 12, "md": 6, "lg": 11},
                    ),
                ],
                expand=True,
            ),
            padding=20
        )
