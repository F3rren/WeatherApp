import logging
import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME
from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.frontend.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog


class Filter:
    def __init__(self, page: ft.Page = None, state_manager=None,
                 handle_location_toggle=None, handle_theme_toggle=None,
                 theme_toggle_value=False, location_toggle_value=False,
                 text_color: dict = None, language: str = None, text_handler_get_size=None):
        self.page = page
        self.state_manager = state_manager
        self.translation_service = page.session.get('translation_service') if page else None
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.location_toggle_value = location_toggle_value
        self.text_color = text_color if text_color else (DARK_THEME if self.page and self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME)
        self.language = language if language else "en"
        self.text_handler_get_size = text_handler_get_size

        self.weather_alert = WeatherAlertDialog(
            page=self.page,
            state_manager=state_manager,
            text_color=self.text_color,
            language=self.language,
        )
        self.map_alert = MapsAlertDialog(
            page=self.page,
            state_manager=state_manager,
            text_color=self.text_color,
            language=self.language,
        )
        self.setting_alert = SettingsAlertDialog(
            page=self.page,
            state_manager=state_manager,
            handle_location_toggle=self.handle_location_toggle,
            handle_theme_toggle=self.handle_theme_toggle,
            text_color=self.text_color,
            language=self.language,
        )

    def update_text_sizes(self, text_handler_get_size, text_color: dict, language: str):
        self.text_handler_get_size = text_handler_get_size
        self.text_color = text_color
        self.language = language
        if hasattr(self.weather_alert, 'update_text_sizes'):
            self.weather_alert.update_text_sizes(self.text_handler_get_size, self.text_color, self.language)
        if hasattr(self.map_alert, 'update_text_sizes'):
            self.map_alert.update_text_sizes(self.text_handler_get_size, self.text_color, self.language)
        if hasattr(self.setting_alert, 'update_text_sizes'):
            self.setting_alert.update_text_sizes(self.text_handler_get_size, self.text_color, self.language)
        if self.page:
            self.page.update()

    def _get_translation(self, key):
        if self.translation_service and hasattr(self.translation_service, 'translate'):
            return self.translation_service.translate(key, self.language)
        return key

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
        if hasattr(self, 'setting_alert'):
            self.setting_alert.update_location_toggle(value)

    def update_theme_toggle_value(self, value):
        if hasattr(self, 'setting_alert'):
            self.setting_alert.update_theme_toggle(value)

    def cleanup(self):
        pass

    def build(self):
        return ft.PopupMenuButton(
            content=ft.Icon(
                ft.Icons.MENU,
                size=self.text_handler_get_size('icon')
            ),
            items=self._build_popup_menu_items(),
        )