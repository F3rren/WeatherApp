from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME
from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog
import flet as ft


class PopMenu:

    def __init__(self, page: ft.Page = None, state_manager=None, 
                 handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_toggle_value=False, location_toggle_value=False, 
                 text_color: dict = None, language: str = None, text_handler_get_size=None):
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.location_toggle_value = location_toggle_value
        self.text_color = text_color if text_color else (DARK_THEME if self.page and self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME)
        self.language = language if language else DEFAULT_LANGUAGE
        self.text_handler_get_size = text_handler_get_size

        # Initialize child dialogs
        self.weather_alert = WeatherAlertDialog(page=self.page, state_manager=state_manager, text_color=self.text_color, language=self.language)
        self.map_alert = MapsAlertDialog(page=self.page, state_manager=state_manager, text_color=self.text_color, language=self.language)
        self.setting_alert = SettingsAlertDialog(page=self.page, state_manager=state_manager, handle_location_toggle=self.handle_location_toggle, handle_theme_toggle=self.handle_theme_toggle, text_color=self.text_color, language=self.language)

        # Initialize popup menu items dictionary
        self.pop_menu_items = {
            "weather": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "weather", self.language), color=self.text_color),
            "map": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "map", self.language), color=self.text_color),
            "settings": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "settings", self.language), color=self.text_color)
        }
        self.popup_menu_button_icon = ft.Icon(ft.Icons.FILTER_ALT_OUTLINED, color=self.text_color)

        # Register observers
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_component)
            self.state_manager.register_observer("theme_event", self.update_component)

    def update_component(self):
        """Update theme, language, text sizes, and rebuild UI."""
        self.text_color = self._determine_text_color_from_theme()
        self.language = self.state_manager.get_state('language') if self.state_manager else DEFAULT_LANGUAGE

        # Update popup menu items using translation keys from TRANSLATIONS
        for key in self.pop_menu_items.keys():
            if key in self.pop_menu_items:
                self.pop_menu_items[key].value = TranslationService.translate_from_dict("popup_menu_items", key, self.language)
                self.pop_menu_items[key].color = self.text_color
                if self.text_handler_get_size:
                    self.pop_menu_items[key].size = self.text_handler_get_size('button')

        # Update sizes
        if self.text_handler_get_size:
            self.popup_menu_button_icon.size = self.text_handler_get_size('icon')

        # Update child dialogs
        for alert in [self.weather_alert, self.map_alert, self.setting_alert]:
            if hasattr(alert, 'update_text_sizes'):
                alert.update_text_sizes(self.text_handler_get_size, self.text_color, self.language)

        # Rebuild UI
        self.popup_menu_button_control.items = self._build_popup_menu_items()
        if self.page:
            self.page.update()

    def build_component(self):
        """Build the frontend component."""
        self.popup_menu_button_control = ft.PopupMenuButton(
            content=ft.Icon(ft.Icons.MENU, color=self.text_color, size=self.text_handler_get_size('icon')),
            items=self._build_popup_menu_items(),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )
        return self.popup_menu_button_control

    def cleanup(self):
        """Cleanup observers and resources."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_component)
            self.state_manager.unregister_observer("theme_event", self.update_component)

    def _determine_text_color_from_theme(self):
        """Determines text color based on the current page theme."""
        if self.page and self.page.theme_mode:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config.get("TEXT", LIGHT_THEME["TEXT"]) # Fallback to light theme text
        return LIGHT_THEME["TEXT"] # Default if page or theme_mode not set

    def _build_popup_menu_items(self):
        """Build popup menu items using the dictionary."""
        return [
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.SUNNY, color="#FF8C00", size=self.text_handler_get_size('popup_menu_button_icon')),
                    self.pop_menu_items["weather"]
                ]),
                on_click=lambda _, al=self.weather_alert: self.weather_alert.open_dialog(),
            ),
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.MAP_OUTLINED, color="#0000FF", size=self.text_handler_get_size('popup_menu_button_icon')),
                    self.pop_menu_items["map"]
                ]),
                on_click=lambda _, al=self.map_alert: self.map_alert.open_dialog(),
            ),
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.SETTINGS, color="#808080", size=self.text_handler_get_size('popup_menu_button_icon')),
                    self.pop_menu_items["settings"]
                ]),
                on_click=lambda _, al=self.setting_alert: self.setting_alert.open_dialog(),
            ),
        ]
