import flet as ft
from services.translation_service import TranslationService # Keep for type hinting or if static methods are used elsewhere
from utils.config import LIGHT_THEME, DARK_THEME # Import theme configurations
from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog


class PopMenu:

    def __init__(self, page: ft.Page = None, state_manager=None, translation_service: TranslationService = None, 
                 handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_toggle_value=False, location_toggle_value=False, text_color: str = None, 
                 language: str = "en", text_handler_get_size=None):
        self.page = page
        self.state_manager = state_manager
        self.translation_service = translation_service
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.location_toggle_value = location_toggle_value
        self.text_handler_get_size = text_handler_get_size # Store the passed function
        self.current_language = language # Store the passed language

        if text_color:
            self.text_color = text_color
        elif self.page:
            self.text_color = DARK_THEME["TEXT"] if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"]
        else:
            self.text_color = LIGHT_THEME["TEXT"] # Default if no page context

        # Pass text_color, language, and text_handler_get_size to child dialogs
        # Assuming child dialogs' __init__ methods are updated to accept these
        self.weather_alert = WeatherAlertDialog(
            page=self.page,
            state_manager=state_manager, 
            translation_service=self.translation_service,
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color,
            language=self.current_language,
            text_handler_get_size=self.text_handler_get_size
        )

        self.map_alert = MapsAlertDialog(
            page=self.page,
            state_manager=state_manager,
            translation_service=self.translation_service,
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color,
            language=self.current_language,
            text_handler_get_size=self.text_handler_get_size
        )

        self.setting_alert = SettingsAlertDialog(
            page=self.page,
            state_manager=state_manager, 
            translation_service=self.translation_service,
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color,
            language=self.current_language,
            text_handler_get_size=self.text_handler_get_size
        )
        
        # Initialize text elements that will be created in createPopMenu
        self.meteo_item_text = None
        self.map_item_text = None
        self.settings_item_text = None
        self.popup_menu_button_icon = None
        self.popup_menu_button = None # Will hold the ft.PopupMenuButton

        if self.page and self.state_manager:
            self.state_manager.register_observer("theme_event", self.handle_theme_change)
        
        # Initial call to set sizes and text based on current props
        self._update_internal_elements()


    def _update_internal_elements(self):
        """Helper to update or create text elements based on current props."""
        if not self.translation_service or not self.text_handler_get_size:
            # Not fully initialized yet, or called too early
            return

        button_size = self.text_handler_get_size('button')
        icon_menu_size = self.text_handler_get_size('icon') 
        
        weather_text_val = self.translation_service.get_text("weather", target_language=self.current_language)
        map_text_val = self.translation_service.get_text("map", target_language=self.current_language)
        settings_text_val = self.translation_service.get_text("settings", target_language=self.current_language)

        if self.meteo_item_text:
            self.meteo_item_text.value = weather_text_val
            self.meteo_item_text.size = button_size
            self.meteo_item_text.color = self.text_color
        else:
            self.meteo_item_text = ft.Text(weather_text_val, size=button_size, color=self.text_color)

        if self.map_item_text:
            self.map_item_text.value = map_text_val
            self.map_item_text.size = button_size
            self.map_item_text.color = self.text_color
        else:
            self.map_item_text = ft.Text(map_text_val, size=button_size, color=self.text_color)

        if self.settings_item_text:
            self.settings_item_text.value = settings_text_val
            self.settings_item_text.size = button_size
            self.settings_item_text.color = self.text_color
        else:
            self.settings_item_text = ft.Text(settings_text_val, size=button_size, color=self.text_color)
        
        if self.popup_menu_button_icon:
            self.popup_menu_button_icon.size = icon_menu_size
            self.popup_menu_button_icon.color = self.text_color
        else:
            self.popup_menu_button_icon = ft.Icon(ft.Icons.MENU, size=icon_menu_size, color=self.text_color)

        # Update elements if they are already on the page
        if self.page:
            for ctrl in [self.meteo_item_text, self.map_item_text, self.settings_item_text, self.popup_menu_button_icon]:
                if ctrl and ctrl.page:
                    ctrl.update()
            if self.popup_menu_button and self.popup_menu_button.page:
                self.popup_menu_button.update()


    def update_text_sizes(self, get_size_func, text_color, language):
        """Updates text sizes, colors, and translations based on provided parameters."""
        self.text_handler_get_size = get_size_func
        self.text_color = text_color
        self.current_language = language

        self._update_internal_elements()

        # Propagate updates to child dialogs
        # Assuming child dialogs have an 'update_text_sizes' method
        if hasattr(self, 'weather_alert') and hasattr(self.weather_alert, 'update_text_sizes'):
            self.weather_alert.update_text_sizes(self.text_handler_get_size, self.text_color, self.current_language)
        if hasattr(self, 'map_alert') and hasattr(self.map_alert, 'update_text_sizes'):
            self.map_alert.update_text_sizes(self.text_handler_get_size, self.text_color, self.current_language)
        if hasattr(self, 'setting_alert') and hasattr(self.setting_alert, 'update_text_sizes'):
            self.setting_alert.update_text_sizes(self.text_handler_get_size, self.text_color, self.current_language)
            

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
            if hasattr(self, 'settings_item_text'):
                self.settings_item_text.color = self.text_color
                if self.settings_item_text.page:
                    self.settings_item_text.update()
            if hasattr(self, 'popup_menu_button_icon'):
                self.popup_menu_button_icon.color = self.text_color
                # ...


    def _open_alert_dialog(self, alert_instance):
        """Helper method to open an alert dialog using its open_dialog method only."""
        if not self.page:
            print("Error: Page context not available for opening dialog.")
            return
        if hasattr(alert_instance, 'open_dialog') and callable(alert_instance.open_dialog):
            alert_instance.open_dialog()
        else:
            print(f"Error: Dialog for {type(alert_instance).__name__} could not be opened (no open_dialog method).")

    def createPopMenu(self, page=None, icon_size=None, text_size=None):
        if page is None: 
            page = self.page
        if not page:
            print("Error: Page context is required to create PopMenu.")
            return ft.Container(ft.Text("Error: Page context missing"))

        if not self.text_handler_get_size or not self.translation_service:
             print("Error: PopMenu not fully initialized (text_handler or translation_service missing).")
             return ft.Container(ft.Text("Error: PopMenu init incomplete"))

        if not all([self.meteo_item_text, self.map_item_text, self.settings_item_text, self.popup_menu_button_icon]):
            self._update_internal_elements()

        # Usa i parametri se forniti, altrimenti fallback
        icon_item_size = icon_size if icon_size else (self.text_handler_get_size('icon_small') if self.text_handler_get_size else 18)
        # Usa la stessa logica di Filter per la grandezza del testo
        current_get_size_func = self.text_handler_get_size if self.text_handler_get_size else (lambda x: 14)
        text_item_size = text_size if text_size else current_get_size_func('button')

        # Aggiorna la dimensione dei testi delle scelte
        if hasattr(self.meteo_item_text, 'size'):
            self.meteo_item_text.size = text_item_size
        if hasattr(self.map_item_text, 'size'):
            self.map_item_text.size = text_item_size
        if hasattr(self.settings_item_text, 'size'):
            self.settings_item_text.size = text_item_size

        self.popup_menu_button = ft.PopupMenuButton(
            content=self.popup_menu_button_icon, # Use the stored icon instance
            items=[
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SUNNY, color="#FF8C00", size=icon_item_size), 
                        ft.Text(self.meteo_item_text.value, size=text_item_size, color=self.meteo_item_text.color),
                    ]),
                    on_click=lambda _, al=self.weather_alert: self._open_alert_dialog(al),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.MAP_OUTLINED, color="#0000FF", size=icon_item_size), 
                        ft.Text(self.map_item_text.value, size=text_item_size, color=self.map_item_text.color),
                    ]),
                    on_click=lambda _, al=self.map_alert: self._open_alert_dialog(al),
                ),
                ft.PopupMenuItem(
                     content=ft.Row([
                         ft.Icon(ft.Icons.SETTINGS, color="#808080", size=icon_item_size), 
                         ft.Text(self.settings_item_text.value, size=text_item_size, color=self.settings_item_text.color),
                     ]),
                     on_click=lambda _, al=self.setting_alert: self._open_alert_dialog(al),
                ),
            ]
        )
        
        return self.popup_menu_button
    
    def update_location_toggle_value(self, value):
        if hasattr(self, 'setting_alert'):
            # Assuming setting_alert has a method to update its internal toggle state
            if hasattr(self.setting_alert, 'update_location_toggle_value'):
                 self.setting_alert.update_location_toggle_value(value)
            elif hasattr(self.setting_alert, 'update_location_toggle'): # old name
                 self.setting_alert.update_location_toggle(value)


    def update_theme_toggle_value(self, value):
        if hasattr(self, 'setting_alert'):
            # Assuming setting_alert has a method to update its internal toggle state
            if hasattr(self.setting_alert, 'update_theme_toggle_value'):
                self.setting_alert.update_theme_toggle_value(value)
            elif hasattr(self.setting_alert, 'update_theme_toggle'): # old name
                self.setting_alert.update_theme_toggle(value)

    def cleanup(self):
        """Cleanup method to remove observers"""
        if self.state_manager and hasattr(self, 'handle_theme_change'):
            self.state_manager.unregister_observer("theme_event", self.handle_theme_change)
        
        # If child dialogs have cleanup methods, call them
        if hasattr(self, 'weather_alert') and hasattr(self.weather_alert, 'cleanup'):
            self.weather_alert.cleanup()
        if hasattr(self, 'map_alert') and hasattr(self.map_alert, 'cleanup'):
            self.map_alert.cleanup()
        if hasattr(self, 'setting_alert') and hasattr(self.setting_alert, 'cleanup'):
            self.setting_alert.cleanup()

    def build(self, page=None, icon_size=None, text_size=None): # build is not standard Flet for a non-Control class
        # This class is not a Flet Control. It provides a Flet control via createPopMenu.
        # If it were to be used as a control directly, it should inherit ft.UserControl.
        # For now, Sidebar will call createPopMenu.
        # If build() is intended to be called, it should return the main control.
        if not self.popup_menu_button:
            self.createPopMenu(page if page else self.page, icon_size=icon_size, text_size=text_size)
        else:
            # Aggiorna la dimensione del testo delle scelte anche se già creato
            if text_size:
                if hasattr(self.meteo_item_text, 'size'):
                    self.meteo_item_text.size = text_size
                if hasattr(self.map_item_text, 'size'):
                    self.map_item_text.size = text_size
                if hasattr(self.settings_item_text, 'size'):
                    self.settings_item_text.size = text_size
        return self.popup_menu_button
