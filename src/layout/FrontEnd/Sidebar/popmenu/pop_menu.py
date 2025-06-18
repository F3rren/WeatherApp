import flet as ft
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME
from utils.translations_data import TRANSLATIONS
from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog
import logging


class PopMenu:

    def __init__(self, page: ft.Page = None, state_manager=None, 
                 handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_toggle_value=False, location_toggle_value=False, 
                 text_color: dict = None, language: str = None, text_handler_get_size = None):
        self.page = page
        self.state_manager = state_manager
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

    def did_mount(self):
        """
        Called when the control is added to the page.
        """
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self.state_manager = self.page.session.get('state_manager')
            self.language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            self.state_manager.register_observer("language_event", self.handle_language_change)
            logging.debug(f"PopMenu did_mount called. Language: {self.language}")
            logging.debug("PopMenu registered observer for language_event.")

    def will_unmount(self):
        """
        Called when the control is removed from the page.
        """        
        if self.state_manager:
            logging.debug("PopMenu will_unmount called. Unregistering observer for language_event.")
            self.state_manager.unregister_observer("language_event", self.handle_language_change)
            
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
            self.setting_alert.update_text_sizes(self.text_color, self.language)
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
            return self.translation_service.get_text(key, self.language)
        return TRANSLATIONS.get(self.language, {}).get(key, key)  # Fallback to key if no translation found

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
        """Cleanup method to remove observers"""
        if hasattr(self, 'text_handler') and self.text_handler:
            self.text_handler.remove_observer(self.update_text_controls)
    
    def build(self):
        return ft.PopupMenuButton(
                content=ft.Icon(
                    ft.Icons.MENU, 
                        color=self.text_color, 
                        size=self.text_handler_get_size('icon')
                    ), 
                items=self._build_popup_menu_items(),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
            )

    def _update_text_elements(self):
        """
        Update text elements without rebuilding the entire UI.
        """
        self.meteo_item_text.value = self._get_translation("weather")
        self.map_item_text.value = self._get_translation("map")
        self.settings_item_text.value = self._get_translation("settings")
        if self.page:
            self.meteo_item_text.update()            
            self.map_item_text.update()
            self.settings_item_text.update()
            
    def handle_language_change(self, event_data=None):
        """
        Handle language change event.
        """
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"handle_language_change received unexpected event_data type: {type(event_data)}")
            return
        new_language = event_data.get('language', DEFAULT_LANGUAGE)
        if self.language != new_language:
            self.language = new_language
            # Aggiorna i testi del menu popup
            self._update_text_elements()
            
            # Aggiorna esplicitamente i testi nei dialog
            if hasattr(self.setting_alert, '_update_text_elements'):
                self.setting_alert._update_text_elements()
            if hasattr(self.map_alert, '_update_text_elements'):
                self.map_alert._update_text_elements()
            if hasattr(self.weather_alert, '_update_text_elements'):
                self.weather_alert._update_text_elements()