import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME
import logging # Added import for logging
from services.translation_service import TranslationService # Added import
from components.responsive_text_handler import ResponsiveTextHandler

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
        self._state_manager_ref_for_cleanup = None # To store state_manager if observer is registered

        # Initialize ResponsiveTextHandler
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'city': 36,
                'location': 20,
                'temperature': 40,
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Dictionary to track text controls for responsive sizing
        self.text_controls = {}
        
        # Text controls that need dynamic color updates
        self.city_text = ft.Text(
            self.city.split(", ")[0], 
            size=self.text_handler.get_size('city'), 
            weight="bold", 
            color=self.text_color
        ) 
        
        self.location_text = ft.Text(
            self.location, 
            size=self.text_handler.get_size('location'),
            color=self.text_color
        )
        
        self.temperature_text = ft.Text(
            size=self.text_handler.get_size('temperature'),
            weight="bold", 
            color=self.text_color
        )

        # Register text controls for responsive sizing
        self.text_controls[self.city_text] = 'city'
        self.text_controls[self.location_text] = 'location'
        self.text_controls[self.temperature_text] = 'temperature'
        
        # Register observer for responsive text changes
        if self.text_handler:
            self.text_handler.add_observer(self.update_text_controls)
            
        # Sovrascrivi il gestore di ridimensionamento della pagina per questo componente
        if self.page:
            # Salva l'handler originale se presente
            self._original_resize_handler = self.page.on_resize
            
            def combined_resize_handler(e):
                # Aggiorna le dimensioni del testo
                self.text_handler._handle_resize(e)
                # Aggiorna i controlli di testo
                self.update_text_controls()
                # Chiama anche l'handler originale se esiste
                if hasattr(self, '_original_resize_handler') and self._original_resize_handler:
                    self._original_resize_handler(e)
            
            self.page.on_resize = combined_resize_handler

        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                # Register for theme_event to update text colors
                state_manager.register_observer("theme_event", self.handle_theme_change)
                # Register for unit_event to update temperature unit symbol
                state_manager.register_observer("unit_event", self.handle_unit_change)
                # Register for language_event to update temperature unit symbol (as language can affect symbol)
                state_manager.register_observer("language_event", self.handle_language_change)
                self._state_manager_ref_for_cleanup = state_manager # Store for cleanup
    
    def update_text_controls(self):
        """Update text controls with current responsive sizes."""
        if self.text_handler and self.text_controls:
            self.text_handler.update_text_controls(self.text_controls)
    
    def _update_temperature_display(self):
        """Updates the temperature text with the correct unit symbol."""
        if not self.page:
            self.temperature_text.value = f"{self.temperature}°" # Fallback
            return

        state_manager = self.page.session.get('state_manager')
        if not state_manager:
            self.temperature_text.value = f"{self.temperature}°" # Fallback
            return

        current_unit = state_manager.get_state('unit')
        current_language = state_manager.get_state('language')
        
        unit_symbol = TranslationService.get_unit_symbol("temperature", current_unit, current_language)
        self.temperature_text.value = f"{self.temperature}{unit_symbol}"
        if hasattr(self.temperature_text, 'update') and self.temperature_text.page:
            self.temperature_text.update()

    def cleanup(self):
        logger = logging.getLogger(__name__)
        
        # Remove responsive text handler observer
        if hasattr(self, 'text_handler') and self.text_handler:
            self.text_handler.remove_observer(self.update_text_controls)
        
        # Ripristina l'handler originale di resize se esiste
        if hasattr(self, '_original_resize_handler') and self.page:
            self.page.on_resize = self._original_resize_handler
        
        if self._state_manager_ref_for_cleanup and hasattr(self._state_manager_ref_for_cleanup, 'unregister_observer'):
            city_name = self.city_text.value if self.city_text and hasattr(self.city_text, 'value') else "N/A"
            logger.debug(f"MainWeatherInfo: Unregistering theme_event observer for city {city_name}")
            self._state_manager_ref_for_cleanup.unregister_observer("theme_event", self.handle_theme_change)
            self._state_manager_ref_for_cleanup.unregister_observer("unit_event", self.handle_unit_change)
            self._state_manager_ref_for_cleanup.unregister_observer("language_event", self.handle_language_change)

    def handle_unit_change(self, event_data=None):
        """Updates the temperature display when the unit system changes."""
        self._update_temperature_display()

    def handle_language_change(self, event_data=None):
        """Updates the temperature display when the language changes (as it could affect unit symbols)."""
        self._update_temperature_display()

    def handle_theme_change(self, event_data=None):
        """Updates the text color based on the current theme."""
        logger = logging.getLogger(__name__)
        
        if not self.page:
            logger.warning("MainWeatherInfo: self.page is None in handle_theme_change.")
            return
        
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
        self.text_color = current_theme_config["TEXT"]
        logger.info(f"MainWeatherInfo: Theme changed to {'DARK' if is_dark else 'LIGHT'}, new text_color: {self.text_color}")
        
        # Update color of all controls
        controls = {"city_text": self.city_text, "location_text": self.location_text, "temperature_text": self.temperature_text}
        
        for name, control_obj in controls.items():
            if control_obj is not None:
                if hasattr(control_obj, 'color'):
                    control_obj.color = self.text_color
                    logger.info(f"MainWeatherInfo: Updated {name}.color to {self.text_color}")
                else:
                    # This case should ideally not be reached if control_obj is a standard ft.Text
                    logger.error(f"MainWeatherInfo: Control '{name}' (Object: {control_obj}, Type: {type(control_obj)}) is not None but lacks 'color' attribute.")
            else:
                logger.warning(f"MainWeatherInfo: Control '{name}' is None. Skipping operations for this control.")
        
        # Update temperature display as well, as text_color might affect it if not handled by control.color
        self._update_temperature_display()

        if getattr(self.page, 'update', None):
            self.page.update()
            logger.info("MainWeatherInfo: self.page.update() called.")
        else:
            logger.warning("MainWeatherInfo: self.page.update is not available or self.page is None.")

    def build(self) -> ft.Container:
        """Build the main weather information"""
        self._update_temperature_display() # Update temperature text when building
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
