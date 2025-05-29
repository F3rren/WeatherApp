import flet as ft
from config import LIGHT_THEME, DARK_THEME # Import theme configurations
from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog


class PopMenu:

    def __init__(self, page: ft.Page = None, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, 
                theme_toggle_value=False, location_toggle_value=False, text_color: str = None):
        self.page = page
        self.state_manager = state_manager
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
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color # Pass text_color
        )

        self.map_alert = MapsAlertDialog(
            page=self.page, # Pass page to MapsAlertDialog
            state_manager=state_manager,
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color
        )

        self.setting_alert = SettingsAlertDialog(
            page=self.page, # Pass page to SettingsAlertDialog
            state_manager=state_manager, 
            handle_location_toggle=handle_location_toggle,
            handle_theme_toggle=handle_theme_toggle,
            text_color=self.text_color # Pass text_color
        )

        # Store PopupMenuItems for color updates
        self.meteo_item_text = ft.Text("Meteo", size=20, color=self.text_color)
        self.map_item_text = ft.Text("Mappa", size=20, color=self.text_color)
        self.popup_menu_button_icon = ft.Icon(ft.Icons.MENU, color=self.text_color) # Icon color

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
            
            if hasattr(self, 'popup_menu_button_icon'):
                self.popup_menu_button_icon.color = self.text_color
                # The icon is part of PopupMenuButton, which might need its own update
                if hasattr(self, 'popup_menu_button') and self.popup_menu_button.page:
                    self.popup_menu_button.update() 
            
            # Propagate theme change to SettingsAlertDialog
            if hasattr(self, 'setting_alert'):
                self.setting_alert.handle_theme_change(event_data) # Pass event_data

    def createPopMenu(self, page=None): # page arg can be removed if self.page is always set
        if page is None: 
            page = self.page # Use self.page if available

        # Crea il menu popup con tutte le opzioni
        self.popup_menu_button = ft.PopupMenuButton( # Store button for updates
            icon=None, # Icon will be set by content to allow dynamic color
            content=self.popup_menu_button_icon, # Use the stored icon
            icon_size=50,
            items=[
                self.weather_alert.createAlertDialog(page), # Pass page if needed by createAlertDialog
                
                #unico funzionale
                self.setting_alert.createAlertDialog(page),
                
                # Altre opzioni
                # ft.PopupMenuItem(
                #     content=ft.Row([
                #         ft.Icon(ft.Icons.SUNNY, color=self.text_color), # Changed ft.Colors.YELLOW to self.text_color
                #         self.meteo_item_text, # Use stored text control
                #     ]),
                #     # Use a default color if needed
                #     on_click=lambda e: print("Meteo clicked")
                # ),
                # ft.PopupMenuItem(
                #     content=ft.Row([
                #         ft.Icon(ft.Icons.MAP_OUTLINED, color=self.text_color), # Changed ft.Colors.GREEN to self.text_color
                #         self.map_item_text, # Use stored text control
                #     ]),
                #     on_click=lambda e: print("Map clicked")
                # )
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