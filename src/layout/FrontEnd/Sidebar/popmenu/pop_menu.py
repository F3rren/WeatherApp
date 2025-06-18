import flet as ft
import logging

from components.responsive_text_handler import ResponsiveTextHandler
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME
from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog


class PopMenu:

    def __init__(self, page: ft.Page = None, state_manager=None, 
                 handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_toggle_value=False, location_toggle_value=False, 
                 text_color: dict = None, language: str = None, text_handler_get_size = None):
        self.page = page
        self.state_manager = state_manager
        self.popup_menu_button_control = None
        if self.state_manager:
            self.state_manager.register_observer("language_event", self._handle_language_change)
        self.translation_service = page.session.get('translation_service') if page else None
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.location_toggle_value = location_toggle_value
        
        self.text_color = text_color if text_color else (DARK_THEME if self.page and self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME)
        self.language = language if language else DEFAULT_LANGUAGE
        self.text_handler_get_size = text_handler_get_size  
 
        self.weather_alert = WeatherAlertDialog(
            page=self.page, 
            state_manager=state_manager, 
            text_color=self.text_color, # Pass the text_color dictionary
            language=self.language, # Pass language
        )

        self.map_alert = MapsAlertDialog(
            page=self.page, 
            state_manager=state_manager,
            text_color=self.text_color, # Pass the text_color dictionary
            language=self.language, # Pass language
            )

        self.setting_alert = SettingsAlertDialog(
            page=self.page, 
            state_manager=state_manager, 
            handle_location_toggle=self.handle_location_toggle, # Pass the specific callbacks
            handle_theme_toggle=self.handle_theme_toggle,
            text_color=self.text_color, # Pass the text_color dictionary
            language=self.language, # Pass language
            )

        # Store PopupMenuItems for color updates
        self.meteo_item_text = ft.Text(self._get_translation("weather"), color=self.text_color)
        self.map_item_text = ft.Text(self._get_translation("map"), color=self.text_color)
        self.settings_item_text = ft.Text(self._get_translation("settings"), color=self.text_color) # Added for settings
        self.popup_menu_button_icon = ft.Icon(ft.Icons.FILTER_ALT_OUTLINED, color=self.text_color) # Apply text_color to icon

    def _handle_language_change(self, new_language_code):
        import flet as ft # Ensure ft is imported if not already at module level
        self.language = new_language_code
        if self.popup_menu_button_control: # Check if the button control exists
            # Re-build items with new language
            self.popup_menu_button_control.items = self._build_popup_menu_items()
            # Update the text of ft.Text controls that were stored if any (self.meteo_item_text etc. are not directly part of items after build)
            # The _build_popup_menu_items method creates new Text controls with updated translations.
            if self.page:
                self.popup_menu_button_control.update() # Update the button to reflect new items

        # Propagate to SettingsAlertDialog if it's already created
        if hasattr(self, 'setting_alert') and self.setting_alert:
            # Call a method on setting_alert to handle its own language update
            if hasattr(self.setting_alert, '_handle_language_change'): # Check if method exists
                self.setting_alert._handle_language_change(new_language_code)
            elif hasattr(self.setting_alert, 'update_text_sizes'): # Fallback to update_text_sizes
                 # We need to pass the current text_color and text_handler_get_size
                 # This assumes text_color and text_handler_get_size are up-to-date or don't change with language alone
                 current_text_color = self.text_color # Or re-fetch theme based color if necessary
                 current_text_handler_get_size = self.text_handler_get_size
                 self.setting_alert.update_text_sizes(current_text_handler_get_size, current_text_color, new_language_code)

        # Update other direct child alerts if they also need language updates
        if hasattr(self, 'weather_alert') and self.weather_alert and hasattr(self.weather_alert, 'update_text_sizes'):
            current_text_color = self.text_color
            current_text_handler_get_size = self.text_handler_get_size
            self.weather_alert.update_text_sizes(current_text_handler_get_size, current_text_color, new_language_code)

        if hasattr(self, 'map_alert') and self.map_alert and hasattr(self.map_alert, 'update_text_sizes'):
            current_text_color = self.text_color
            current_text_handler_get_size = self.text_handler_get_size
            self.map_alert.update_text_sizes(current_text_handler_get_size, current_text_color, new_language_code)

        # It might be necessary to update the page if PopMenu itself has direct text that changed.
        # For now, focus on items and child dialogs.

    def update_text_sizes(self, text_handler_get_size, text_color: dict, language: str):
        """Aggiorna dinamicamente le dimensioni del testo e i colori in base alla finestra."""
        self.passed_text_handler_get_size = text_handler_get_size
        self.text_color = text_color
        self.language = language
        # Aggiorna icone e testi se presenti
        if hasattr(self, 'popup_menu_button_icon') and self.popup_menu_button_icon:
            self.popup_menu_button_icon.size = self.passed_text_handler_get_size('icon')
            self.popup_menu_button_icon.color = self.text_color
        if hasattr(self, 'meteo_item_text'):
            self.meteo_item_text.size = self.passed_text_handler_get_size('button')
            self.meteo_item_text.color = self.text_color
        if hasattr(self, 'map_item_text'):
            self.map_item_text.size = self.passed_text_handler_get_size('button')
            self.map_item_text.color = self.text_color
        if hasattr(self, 'settings_item_text'):
            self.settings_item_text.size = self.passed_text_handler_get_size('button')
            self.settings_item_text.color = self.text_color
        # Aggiorna eventuali child dialogs
        if hasattr(self.weather_alert, 'update_text_sizes'):
            self.weather_alert.update_text_sizes(self.passed_text_handler_get_size, self.text_color, self.language)
        if hasattr(self.map_alert, 'update_text_sizes'):
            self.map_alert.update_text_sizes(self.passed_text_handler_get_size, self.text_color, self.language)
        if hasattr(self.setting_alert, 'update_text_sizes'):
            self.setting_alert.update_text_sizes(self.passed_text_handler_get_size, self.text_color, self.language)
        if self.page:
            self.page.update()

    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        # This method will be removed when internal text_handler is removed
        if not self.text_handler:
            return
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
            # Use self.language (passed prop) instead of fetching from state_manager here
            # as this component should reflect the language it was given.
            current_language = self.language 
            return self.translation_service.get_text(key, current_language)
        return key  # Fallback to key if no translation service

    def _open_alert_dialog(self, alert_instance):
        if not self.page:
            print("Error: Page context not available for opening dialog.")
            return
        if hasattr(alert_instance, 'open_dialog') and callable(alert_instance.open_dialog):
            alert_instance.open_dialog()
        else:
            print(f"Error: Dialog for {type(alert_instance).__name__} could not be opened (no open_dialog method).")

    def _build_popup_menu_items(self):
        return [
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.SUNNY, 
                            color="#FF8C00", 
                            size=self.text_handler_get_size('popup_menu_button_icon')),
                    ft.Text(
                        self._get_translation("weather"), 
                        color=self.text_color, 
                        size=self.text_handler_get_size('alert_dialog_text') 
                    )
                ]),
                on_click=lambda _, al=self.weather_alert: self._open_alert_dialog(al),
            ),
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.MAP_OUTLINED, 
                            color="#0000FF", 
                            size=self.text_handler_get_size('popup_menu_button_icon')),
                    ft.Text(
                        self._get_translation("map"), # Ensure key is correct ("map" or "maps")
                        color=self.text_color, 
                        size=self.text_handler_get_size('alert_dialog_text') 
                    )
                ]),
                on_click=lambda _, al=self.map_alert: self._open_alert_dialog(al),
            ),
            ft.PopupMenuItem(
                 content=ft.Row([
                    ft.Icon(
                        ft.Icons.SETTINGS, 
                        color="#808080", 
                        size=self.text_handler_get_size('popup_menu_button_icon')),
                    ft.Text(
                        self._get_translation("settings"), 
                        color=self.text_color,
                        size=self.text_handler_get_size('alert_dialog_text')
                    )
                ]),
                on_click=lambda _, al=self.setting_alert: self._open_alert_dialog(al),
            ),
        ]

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
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self._handle_language_change)
        # Keep existing cleanup for text_handler if present
        if hasattr(self, 'text_handler') and self.text_handler and hasattr(self.text_handler, 'remove_observer'):
             try: # Add try-except if text_handler might not have this observer
                self.text_handler.remove_observer(self.update_text_controls)
             except ValueError: # Observer not found
                pass
    
    def build(self):
        self.popup_menu_button_control = ft.PopupMenuButton(
                content=ft.Icon(
                    ft.Icons.MENU, 
                        color=self.text_color, 
                        size=self.text_handler_get_size('icon')
                    ), 
                items=self._build_popup_menu_items(),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
            )
        return self.popup_menu_button_control