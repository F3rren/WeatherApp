import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService

class WeatherAlertDialog:
    def __init__(self, page: ft.Page, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, 
                 text_color: dict = None, language: str = "en"):
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.current_language = language
        # Always use full theme dict
        if self.page and hasattr(self.page, 'theme_mode'):
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            self.text_color = DARK_THEME if is_dark else LIGHT_THEME
        else:
            self.text_color = text_color if text_color else LIGHT_THEME
        self.dialog = None
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20,
                'body': 14,
                'icon': 20,
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        self.update_ui()

    def update_ui(self, event_data=None):
        # Always update theme and language
        if self.page and hasattr(self.page, 'theme_mode'):
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            self.text_color = DARK_THEME if is_dark else LIGHT_THEME
        # Optionally update language from state_manager
        if self.state_manager:
            self.current_language = self.state_manager.get_state('language') or self.current_language
        self.dialog = self.build()

    def build(self):
        get_size = self._text_handler.get_size
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK if self.page and hasattr(self.page, 'theme_mode') else False
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        dialog_text_color = self.text_color["TEXT"]
        bg_color = current_theme["DIALOG_BACKGROUND"]
        title_size = get_size('title')
        body_size = get_size('body')
        icon_size = get_size('icon')
        title_text_control = ft.Text(
            self._get_translation("weather"), 
            size=title_size, 
            weight=ft.FontWeight.BOLD, 
            color=dialog_text_color
        )
        language_icon_control = ft.Icon(ft.Icons.LANGUAGE, size=icon_size, color="#ff6b35")
        measurement_icon_control = ft.Icon(ft.Icons.STRAIGHTEN, size=icon_size, color="#22c55e")
        location_icon_control = ft.Icon(ft.Icons.LOCATION_ON, size=icon_size, color="#ef4444")
        theme_icon_control = ft.Icon(ft.Icons.DARK_MODE, size=icon_size, color="#3b82f6")
        language_text_control = ft.Text(self._get_translation("language_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        measurement_text_control = ft.Text(self._get_translation("measurement_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        location_text_control = ft.Text(self._get_translation("use_current_location_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        theme_text_control = ft.Text(self._get_translation("dark_theme_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        close_button_text_control = ft.Text(self._get_translation("close_button"), color=current_theme["ACCENT"], size=body_size)
        dialog = ft.AlertDialog(
            title=title_text_control,
            bgcolor=bg_color,
            content=ft.Container(
                width=400,
                content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(controls=[language_icon_control, language_text_control], spacing=10),
                        ],
                        spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Row(controls=[measurement_icon_control, measurement_text_control], spacing=10),
                        ],
                        spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Row(controls=[location_icon_control, location_text_control], spacing=10),
                        ],
                        spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Row(controls=[theme_icon_control, theme_text_control], spacing=10),
                        ],
                        spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                height=280,
                spacing=20,
            ),
            ),
            actions=[
                ft.TextButton(
                    content=close_button_text_control,
                    style=ft.ButtonStyle(
                        color=current_theme["ACCENT"], 
                        overlay_color=ft.Colors.with_opacity(0.1, current_theme["ACCENT"]),
                    ),
                    on_click=lambda e: self.close_dialog()
                ),
            ],
            on_dismiss=lambda e: print("Weather Dialog dismissed"),
            modal=True
        )
        return dialog

    def _get_translation(self, key):
        return TranslationService.translate(key, str(self.current_language))

    def open_dialog(self):
        if not self.dialog:
            self.dialog = self.build()
        if self.page and self.dialog:
            if self.dialog not in self.page.controls:
                self.page.controls.append(self.dialog)
            self.page.dialog = self.dialog
            self.page.dialog.open = True
            self.page.update()

    def close_dialog(self):
        if self.dialog:
            self.dialog.open = False
            if self.page:
                 self.page.update()

    def cleanup(self):
        pass