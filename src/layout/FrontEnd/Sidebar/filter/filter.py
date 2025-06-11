import logging
import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME # Import theme configurations
from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog
from components.responsive_text_handler import ResponsiveTextHandler

class Filter:
    def __init__(self, page: ft.Page = None, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, 
                theme_toggle_value=False, location_toggle_value=False, text_color: str = None):
        self.page = page
        self.state_manager = state_manager
        self.translation_service = page.session.get('translation_service') if page else None
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.location_toggle_value = location_toggle_value
        
        if text_color:
            self.text_color = text_color        
        elif self.page:
            self.text_color = DARK_THEME["TEXT"] if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"]
        else:
            self.text_color = LIGHT_THEME["TEXT"] # Default if no page context
        
        # Initialize ResponsiveTextHandler
        if self.page:
            self.text_handler = ResponsiveTextHandler(
                page=self.page,
                base_sizes={
                    'button': 14,  # Button text size
                    'icon': 20,    # Icon size
                },
                breakpoints=[600, 900, 1200, 1600]
            )
            
            # Dictionary to track text controls
            self.text_controls = {}
            
            # Register as observer for responsive updates
            self.text_handler.add_observer(self.update_text_controls)

        self.weather_alert = WeatherAlertDialog(
            page=self.page, # Pass page to SettingsAlertDialog
            state_manager=state_manager, 
            translation_service=self.translation_service,
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color # Pass text_color
        )

        self.map_alert = MapsAlertDialog(
            page=self.page, # Pass page to MapsAlertDialog
            state_manager=state_manager,
            translation_service=self.translation_service,
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color
        )

        self.setting_alert = SettingsAlertDialog(
            page=self.page, # Pass page to SettingsAlertDialog
            state_manager=state_manager, 
            translation_service=self.translation_service,
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color # Pass text_color
        )

        # Store PopupMenuItems for color updates
        self.meteo_item_text = ft.Text(self._get_translation("weather"), size=20, color=self.text_color)
        self.map_item_text = ft.Text(self._get_translation("map"), size=20, color=self.text_color)
        self.settings_item_text = ft.Text(self._get_translation("settings"), size=20, color=self.text_color) # Added for settings
        self.popup_menu_button_icon = ft.Icon(ft.Icons.FILTER_ALT_OUTLINED, size=40, color=self.text_color) # Apply text_color to icon

        if self.page and self.state_manager:
            self.state_manager.register_observer("theme_event", self.handle_theme_change)

    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        for control, size_category in self.text_controls.items():
            if size_category == 'icon':
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
            else:
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
        
        # Request page update
        if self.page:
            self.page.update()

    def _get_translation(self, key):
        """Helper method to get translation with fallback"""
        if self.translation_service and hasattr(self.translation_service, 'get_text'):
            current_language = self.state_manager.get_state("language") if self.state_manager else "en"
            return self.translation_service.get_text(key, current_language)
        return key  # Fallback to key if no translation service
        
    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text and icon colors."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]

            if hasattr(self, 'meteo_item_text'):
                self.meteo_item_text.color = self.text_color
                if self.meteo_item_text.page:
                    self.meteo_item_text.update()
            
            if hasattr(self, 'map_item_text'):
                self.map_item_text.color = self.text_color
                if self.map_item_text.page:
                    self.map_item_text.update()

            if hasattr(self, 'settings_item_text'): # Added for settings
                self.settings_item_text.color = self.text_color
                if self.settings_item_text.page:
                    self.settings_item_text.update()
            
            if hasattr(self, 'popup_menu_button_icon'):
                self.popup_menu_button_icon.color = self.text_color
                # The icon is part of PopupMenuButton, which might need its own update
                if hasattr(self, 'popup_menu_button') and self.popup_menu_button.page:
                    self.popup_menu_button.update() 
            
            # Propagate theme change to Alert Dialogs
            if hasattr(self, 'setting_alert') and hasattr(self.setting_alert, 'handle_theme_change'):
                self.setting_alert.handle_theme_change(event_data)

            if hasattr(self, 'weather_alert') and hasattr(self.weather_alert, 'handle_theme_change'):
                self.weather_alert.handle_theme_change(event_data)
            
            if hasattr(self, 'map_alert') and hasattr(self.map_alert, 'handle_theme_change'):
                self.map_alert.handle_theme_change(event_data)

    def _open_alert_dialog(self, alert_instance):
        """Helper method to create (if needed) and open an alert dialog."""
        if not self.page:
            logging.error("Error: Page context not available for opening dialog.")
            return
        if not hasattr(alert_instance, 'dialog') or not alert_instance.dialog:
            alert_instance.createAlertDialog(self.page)
          # Ensure dialog was created and is available
        if hasattr(alert_instance, 'dialog') and alert_instance.dialog:
            self.page.open(alert_instance.dialog)
        else:
            logging.error(f"Error: Dialog for {type(alert_instance).__name__} could not be created or found for opening.")

    def createPopMenu(self, page=None):# page arg can be removed if self.page is always set
        if page is None: 
            page = self.page # Use self.page if available
        
        if not page: # Ensure we have a page context
            logging.error("Error: Page context is required to create PopMenu and its dialogs.")
            return ft.Container(ft.Text(self._get_translation("error_page_context_missing")))

        # Create text controls with responsive sizes
        self.popup_menu_button_icon = ft.Icon(
            ft.Icons.MORE_VERT, 
            color=self.text_color,
            size=self.text_handler.get_size('icon') if hasattr(self, 'text_handler') else 20
        )
        
        self.meteo_item_text = ft.Text(
            self._get_translation("weather"), 
            color=self.text_color,
            size=self.text_handler.get_size('button') if hasattr(self, 'text_handler') else 14
        )
        
        self.map_item_text = ft.Text(
            self._get_translation("maps"), 
            color=self.text_color,
            size=self.text_handler.get_size('button') if hasattr(self, 'text_handler') else 14
        )
        
        self.settings_item_text = ft.Text(
            self._get_translation("settings"), 
            color=self.text_color,
            size=self.text_handler.get_size('button') if hasattr(self, 'text_handler') else 14
        )
        
        # Register controls if text_handler is available
        if hasattr(self, 'text_handler'):
            self.text_controls[self.popup_menu_button_icon] = 'icon'
            self.text_controls[self.meteo_item_text] = 'button'
            self.text_controls[self.map_item_text] = 'button'
            self.text_controls[self.settings_item_text] = 'button'

        # Crea il menu popup con tutte le opzioni
        self.popup_menu_button = ft.PopupMenuButton( # Store button for updates
            icon=None, # Icon will be set by content to allow dynamic color
            content=self.popup_menu_button_icon, # Use the stored icon
            icon_size=self.text_handler.get_size('icon') if hasattr(self, 'text_handler') else 50,
            items=[
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SUNNY, color="#FF8C00"), # Custom color DarkOrange
                        self.meteo_item_text,
                    ]),
                    on_click=lambda _, al=self.weather_alert: self._open_alert_dialog(al),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.MAP_OUTLINED, color="#0000FF"), # Custom color Blue
                        self.map_item_text,
                    ]),
                    on_click=lambda _, al=self.map_alert: self._open_alert_dialog(al),
                ),
                ft.PopupMenuItem(
                     content=ft.Row([
                         ft.Icon(ft.Icons.SETTINGS, color="#808080"), # Custom color Gray
                         self.settings_item_text, # Use dedicated text control
                     ]),
                    on_click=lambda _, al=self.setting_alert: self._open_alert_dialog(al),
                ),
            ]
        )
        
        return self.popup_menu_button
    
    def update_location_toggle_value(self, value):
        """
        Aggiorna il valore interno dello stato del toggle della localizzazione.
        Da chiamare quando lo stato cambia esternamente.
        """
        if hasattr(self, 'setting_alert'):
            self.setting_alert.update_location_toggle(value)
            
    def update_theme_toggle_value(self, value):
        """
        Aggiorna il valore interno dello stato del toggle del tema.
        Da chiamare quando lo stato cambia esternamente.
        """
        if hasattr(self, 'setting_alert'):
            self.setting_alert.update_theme_toggle(value)
        
    def cleanup(self):
        """Cleanup method to remove observers"""
        if hasattr(self, 'text_handler') and self.text_handler:
            self.text_handler.remove_observer(self.update_text_controls)
    
    def build(self, page=None):
        return ft.Container(
            content=ft.Column([
                self.createPopMenu(page)
            ])
        )