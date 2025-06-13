import logging
import flet as ft
# LIGHT_THEME, DARK_THEME imports will be removed if text_color dict is used directly
from utils.config import LIGHT_THEME, DARK_THEME 
from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog
# ResponsiveTextHandler will eventually be removed from here
from components.responsive_text_handler import ResponsiveTextHandler

class Filter:
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
        self.language = language if language else "en" # Default if not provided
        self.passed_text_handler_get_size = text_handler_get_size # Store passed function
        
        # Initialize ResponsiveTextHandler (This will be removed in a future refactor)
        if self.page:
            self.text_handler = ResponsiveTextHandler(
                page=self.page,
                base_sizes={
                    'button': 14,  # Button text size
                    'icon': 20,    # Icon size
                },
                breakpoints=[600, 900, 1200, 1600]
            )
            self.text_controls = {}
            self.text_handler.add_observer(self.update_text_controls)
        else:
            self.text_handler = None # Ensure it's None if no page

        # Determine the get_size function to use for children for now
        # Eventually, Filter will use passed_text_handler_get_size directly
        current_get_size_func = self.passed_text_handler_get_size if self.passed_text_handler_get_size else (self.text_handler.get_size if self.text_handler else lambda x: 14) 

        self.weather_alert = WeatherAlertDialog(
            page=self.page, 
            state_manager=state_manager, 
            # translation_service=self.translation_service, # translation_service is usually fetched from page session by dialogs
            # handle_location_toggle=handle_location_toggle, # These seem specific to SettingsAlertDialog
            # handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color, # Pass the text_color dictionary
            language=self.language, # Pass language
            text_handler_get_size=current_get_size_func # Pass get_size function
        )

        self.map_alert = MapsAlertDialog(
            page=self.page, 
            state_manager=state_manager,
            # translation_service=self.translation_service,
            # handle_location_toggle=handle_location_toggle,
            # handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color, # Pass the text_color dictionary
            language=self.language, # Pass language
            text_handler_get_size=current_get_size_func # Pass get_size function
        )

        self.setting_alert = SettingsAlertDialog(
            page=self.page, 
            state_manager=state_manager, 
            # translation_service=self.translation_service, # SettingsAlertDialog fetches its own
            handle_location_toggle=self.handle_location_toggle, # Pass the specific callbacks
            handle_theme_toggle=self.handle_theme_toggle,
            text_color=self.text_color, # Pass the text_color dictionary
            language=self.language, # Pass language
            text_handler_get_size=current_get_size_func # Pass get_size function
        )

        # Store PopupMenuItems for color updates
        self.meteo_item_text = ft.Text(self._get_translation("weather"), size=20, color=self.text_color)
        self.map_item_text = ft.Text(self._get_translation("map"), size=20, color=self.text_color)
        self.settings_item_text = ft.Text(self._get_translation("settings"), size=20, color=self.text_color) # Added for settings
        self.popup_menu_button_icon = ft.Icon(ft.Icons.FILTER_ALT_OUTLINED, size=40, color=self.text_color) # Apply text_color to icon

    def update_text_sizes(self, text_handler_get_size, text_color: dict, language: str):
        """Updates text sizes, color, and language for the Filter and its children."""
        self.passed_text_handler_get_size = text_handler_get_size
        self.text_color = text_color
        self.language = language

        # Update own elements if they were more complex or directly managed text sizes
        # For now, PopMenu items are recreated in createPopMenu, which will use new props.
        # If PopMenu itself needs an update, it would be called here.
        if hasattr(self, 'popup_menu_button') and self.popup_menu_button:
            # Re-create or update PopMenu parts if necessary
            # This might involve updating icon sizes/colors directly if not done in createPopMenu
            if self.popup_menu_button_icon:
                self.popup_menu_button_icon.size = self.passed_text_handler_get_size('icon')
                self.popup_menu_button_icon.color = self.text_color
            # Update text items (they are recreated in createPopMenu, but if held, update here)
            if self.meteo_item_text: 
                self.meteo_item_text.value = self._get_translation("weather")
                self.meteo_item_text.size = self.passed_text_handler_get_size('button')
                self.meteo_item_text.color = self.text_color
            if self.map_item_text: 
                self.map_item_text.value = self._get_translation("maps") # "map" or "maps"
                self.map_item_text.size = self.passed_text_handler_get_size('button')
                self.map_item_text.color = self.text_color
            if self.settings_item_text: 
                self.settings_item_text.value = self._get_translation("settings")
                self.settings_item_text.size = self.passed_text_handler_get_size('button')
                self.settings_item_text.color = self.text_color
            
            # If the popup_menu_button itself needs an update due to content changes:
            self.popup_menu_button.items = self._build_popup_menu_items() # Rebuild items
            self.popup_menu_button.update()

        # Propagate to child dialogs
        if hasattr(self.weather_alert, 'update_text_sizes'):
            self.weather_alert.update_text_sizes(self.passed_text_handler_get_size, self.text_color, self.language)
        if hasattr(self.map_alert, 'update_text_sizes'):
            self.map_alert.update_text_sizes(self.passed_text_handler_get_size, self.text_color, self.language)
        if hasattr(self.setting_alert, 'update_text_sizes'):
            self.setting_alert.update_text_sizes(self.passed_text_handler_get_size, self.text_color, self.language)
        
        if self.page:
            self.page.update() # Trigger a page update to reflect changes

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
        """Helper method to create (if needed) and open an alert dialog."""
        if not self.page:
            logging.error("Error: Page context not available for opening dialog.")
            return
        
        # Ensure the dialog instance has the latest props before creating/opening
        # This is important if dialogs are created lazily
        if hasattr(alert_instance, 'text_color'): # Check if it has these attributes
            alert_instance.text_color = self.text_color
            alert_instance.language = self.language
            alert_instance.text_handler_get_size = self.passed_text_handler_get_size 
            # If the dialog is already created, call its update_text_sizes
            if alert_instance.dialog and hasattr(alert_instance, 'update_text_sizes'):
                alert_instance.update_text_sizes(self.passed_text_handler_get_size, self.text_color, self.language)
            elif not alert_instance.dialog and hasattr(alert_instance, 'createAlertDialog'):
                alert_instance.createAlertDialog(self.page) # It will use its updated props
        elif hasattr(alert_instance, 'createAlertDialog'): # Fallback for older dialogs not yet fully refactored
             alert_instance.createAlertDialog(self.page)

        if hasattr(alert_instance, 'dialog') and alert_instance.dialog:
            # self.page.open(alert_instance.dialog) # Flet V1 uses page.dialog = instance; instance.open = True
            self.page.dialog = alert_instance.dialog
            alert_instance.dialog.open = True
            self.page.update()
        else:
            logging.error(f"Error: Dialog for {type(alert_instance).__name__} could not be created or shown.")

    def createPopMenu(self, page=None, icon_size=None, text_size=None):
        if page is None: 
            page = self.page # Use self.page if available
        if not page: # Ensure we have a page context
            logging.error("Error: Page context is required to create PopMenu and its dialogs.")
            return ft.Container(ft.Text(self._get_translation("error_page_context_missing")))

        current_get_size_func = self.passed_text_handler_get_size if self.passed_text_handler_get_size else (self.text_handler.get_size if self.text_handler else lambda x: 14)
        icon_size_val = icon_size if icon_size else current_get_size_func('icon')
        button_size_val = text_size if text_size else current_get_size_func('button')

        self.popup_menu_button_icon = ft.Icon(
            ft.Icons.MORE_VERT, 
            color=self.text_color, 
            size=icon_size_val
        )

        self.popup_menu_button = ft.PopupMenuButton(
            content=self.popup_menu_button_icon, 
            icon_size=icon_size_val, 
            items=self._build_popup_menu_items(button_size_val)
        )
        return self.popup_menu_button

    def _build_popup_menu_items(self, button_size_val):
        """Helper to build/rebuild PopupMenuItem list with current translations and styles."""
        current_get_size_func = self.passed_text_handler_get_size if self.passed_text_handler_get_size else (self.text_handler.get_size if self.text_handler else lambda x: 14)
        button_size_val = current_get_size_func('button')

        # Re-create text controls for items to ensure they have latest language and color
        self.meteo_item_text = ft.Text(
            self._get_translation("weather"), 
            color=self.text_color, 
            size=button_size_val
        )
        self.map_item_text = ft.Text(
            self._get_translation("maps"), # Ensure key is correct ("map" or "maps")
            color=self.text_color, 
            size=button_size_val
        )
        self.settings_item_text = ft.Text(
            self._get_translation("settings"), 
            color=self.text_color, 
            size=button_size_val
        )

        return [
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.SUNNY, color="#FF8C00"),
                    self.meteo_item_text,
                ]),
                on_click=lambda _, al=self.weather_alert: self._open_alert_dialog(al),
            ),
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.MAP_OUTLINED, color="#0000FF"),
                    self.map_item_text,
                ]),
                on_click=lambda _, al=self.map_alert: self._open_alert_dialog(al),
            ),
            ft.PopupMenuItem(
                 content=ft.Row([
                     ft.Icon(ft.Icons.SETTINGS, color="#808080"),
                     self.settings_item_text,
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
    
    def build(self, page=None, icon_size=None, text_size=None):
        return ft.Container(
            content=ft.Column([
                self.createPopMenu(page, icon_size=icon_size, text_size=text_size)
            ])
        )