import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME # Import theme configurations
from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog


class PopMenu:

    def __init__(self, page: ft.Page = None, state_manager=None, translation_service=None, handle_location_toggle=None, handle_theme_toggle=None, 
                theme_toggle_value=False, location_toggle_value=False, text_color: str = None):
        self.page = page
        self.state_manager = state_manager
        self.translation_service = translation_service # Initialize translation_service
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

        self.weather_alert = WeatherAlertDialog(
            page=self.page, # Pass page to SettingsAlertDialog
            state_manager=state_manager, 
            translation_service=self.translation_service, # Pass translation_service
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color # Pass text_color
        )

        self.map_alert = MapsAlertDialog(
            page=self.page, # Pass page to MapsAlertDialog
            state_manager=state_manager,
            translation_service=self.translation_service, # Pass translation_service
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color
        )

        self.setting_alert = SettingsAlertDialog(
            page=self.page, # Pass page to SettingsAlertDialog
            state_manager=state_manager, 
            translation_service=self.translation_service, # Pass translation_service
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color # Pass text_color
        )

        # Store PopupMenuItems for color updates with language-aware fallbacks
        current_language = self.state_manager.get_state("language") if self.state_manager else "en"
        
        # Define fallback translations
        translations = {
            "en": {"weather": "Weather", "map": "Map", "settings": "Settings"},
            "it": {"weather": "Meteo", "map": "Mappa", "settings": "Impostazioni"},
            "fr": {"weather": "Météo", "map": "Carte", "settings": "Paramètres"},
            "es": {"weather": "Clima", "map": "Mapa", "settings": "Configuración"},
            "de": {"weather": "Wetter", "map": "Karte", "settings": "Einstellungen"}
        }
        
        # Get translations with fallbacks
        lang_translations = translations.get(current_language, translations["en"])
        weather_text = lang_translations["weather"]
        map_text = lang_translations["map"]
        settings_text = lang_translations["settings"]
        
        self.meteo_item_text = ft.Text(weather_text, size=20, color=self.text_color)
        self.map_item_text = ft.Text(map_text, size=20, color=self.text_color)
        self.settings_item_text = ft.Text(settings_text, size=20, color=self.text_color)
        self.popup_menu_button_icon = ft.Icon(ft.Icons.MENU, size=50, color=self.text_color) # Apply text_color to icon

        if self.page and self.state_manager:
            self.state_manager.register_observer("theme_event", self.handle_theme_change)
        
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
            
            # Propagate theme change to SettingsAlertDialog
            if hasattr(self, 'setting_alert'):
                self.setting_alert.handle_theme_change(event_data) # Pass event_data

    def _open_alert_dialog(self, alert_instance):
        """Helper method to create (if needed) and open an alert dialog."""
        if not self.page:
            print("Error: Page context not available for opening dialog.")
            return
        if not hasattr(alert_instance, 'dialog') or not alert_instance.dialog:
            alert_instance.createAlertDialog(self.page)
        
        # Ensure dialog was created and is available
        if hasattr(alert_instance, 'dialog') and alert_instance.dialog:
            self.page.open(alert_instance.dialog)
        else:
            print(f"Error: Dialog for {type(alert_instance).__name__} could not be created or found for opening.")

    def createPopMenu(self, page=None): # page arg can be removed if self.page is always set
        if page is None: 
            page = self.page # Use self.page if available
        
        if not page: # Ensure we have a page context
            print("Error: Page context is required to create PopMenu and its dialogs.")
            return ft.Container(ft.Text("Error: Page context missing"))

        # Crea il menu popup con tutte le opzioni
        self.popup_menu_button = ft.PopupMenuButton( # Store button for updates
            icon=None, # Icon will be set by content to allow dynamic color
            content=self.popup_menu_button_icon, # Use the stored icon
            icon_size=50,
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
        
    def build(self, page=None):
        return ft.Container(
            content=ft.Column([
                self.createPopMenu(page)
            ])
        )
