
from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE
from services.theme_handler import ThemeHandler
from layout.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog
import flet as ft



class PopMenu(ft.Container):
    def __init__(self, page: ft.Page = None, state_manager=None, 
                 handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_toggle_value=False, location_toggle_value=False, 
                 language: str = None, theme_handler: ThemeHandler = None, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.location_toggle_value = location_toggle_value
        self.theme_handler = theme_handler or ThemeHandler(page)
        self.language = language if language else DEFAULT_LANGUAGE
        self.weather_alert = None
        self.map_alert = None
        self.setting_alert = None
        self.pop_menu_items = None
        self.popup_menu_button_icon = None
        self.popup_menu_button_control = None
        self.update_ui()
        self.content = self.build()
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)


    def update_ui(self, event_data=None):
        """Update theme, language, text sizes, and rebuild UI."""
        self._current_text_color = self.theme_handler.get_text_color() if self.theme_handler else "black"
        self.language = self.state_manager.get_state('language') if self.state_manager else DEFAULT_LANGUAGE

        # Update child dialogs, passing theme_handler for color logic
        self.weather_alert = WeatherAlertDialog(page=self.page, state_manager=self.state_manager, theme_handler=self.theme_handler, language=self.language)
        
        self.map_alert = MapsAlertDialog(page=self.page, state_manager=self.state_manager)
        
        self.setting_alert = SettingsAlertDialog(
            page=self.page, state_manager=self.state_manager,
            handle_location_toggle=self.handle_location_toggle,
            handle_theme_toggle=self.handle_theme_toggle,
            theme_handler=self.theme_handler, language=self.language)

        # Update popup menu items using translation keys from TRANSLATIONS
        self.pop_menu_items = {
            "weather": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "weather", self.language), color=self._current_text_color),
            "map": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "map", self.language), color=self._current_text_color),
            "settings": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "settings", self.language), color=self._current_text_color)
        }
        self.popup_menu_button_icon = ft.Icon(ft.Icons.FILTER_ALT_OUTLINED, color=self._current_text_color)

    def build(self):
        """Build the frontend component."""
        def build_popup_menu_items():
            return [
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SUNNY, color="#FF8C00", size=20),
                        self.pop_menu_items["weather"]
                    ]),
                    on_click=lambda _, al=self.weather_alert: self.weather_alert.open_dialog(),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.MAP_OUTLINED, color="#0000FF", size=20),
                        self.pop_menu_items["map"]
                    ]),
                    on_click=lambda _, al=self.map_alert: self.map_alert.open_dialog(),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SETTINGS, color="#808080", size=20),
                        self.pop_menu_items["settings"]
                    ]),
                    on_click=lambda _, al=self.setting_alert: self.setting_alert.open_dialog(),
                ),
            ]
        self.popup_menu_button_control = ft.PopupMenuButton(
            content=ft.Icon(ft.Icons.MENU, color=self._current_text_color, size=20),
            items=build_popup_menu_items(),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )
        return self.popup_menu_button_control

    def cleanup(self):
        """Cleanup observers and resources."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
            self.state_manager.unregister_observer("theme_event", self.update_ui)

    def _determine_text_color_from_theme(self):
        """Returns the full theme dictionary based on the current page theme."""
        
