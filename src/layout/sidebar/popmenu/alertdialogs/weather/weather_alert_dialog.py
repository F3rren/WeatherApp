import logging
import flet as ft
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService

class WeatherAlertDialog:

    def __init__(self, page: ft.Page, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_handler=None, language: str = "en"):
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.current_language = language
        self.theme_handler = theme_handler
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
        # Always update theme and language using theme_handler
        if self.theme_handler:
            self.text_color = self.theme_handler.get_text_color()
            if isinstance(self.text_color, str):
                # If theme_handler returns a string, wrap as dict for compatibility
                self.text_color = {"TEXT": self.text_color, "DIALOG_BACKGROUND": "#fff", "ACCENT": "#0078d4"}
        else:
            self.text_color = {"TEXT": "#000000", "DIALOG_BACKGROUND": "#fff", "ACCENT": "#0078d4"}
        # Optionally update language from state_manager
        if self.state_manager:
            self.current_language = self.state_manager.get_state('language') or self.current_language
        self.dialog = self.build()

    def build(self):
        get_size = self._text_handler.get_size
        dialog_text_color = self.text_color["TEXT"]
        accent_color = self.text_color.get("ACCENT", "#0078d4")
        title_size = get_size('title')
        body_size = get_size('body')
        icon_size = get_size('icon')
        # Supporto dark mode per il background del dialog
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        dialog_bg = "#161b22" if is_dark else "#ffffff"
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
        close_button_text_control = ft.Text(self._get_translation("close_button"), color=accent_color, size=body_size)
        dialog = ft.AlertDialog(
            title=title_text_control,
            bgcolor=dialog_bg,
            content=ft.Container(
                width=400,
                bgcolor=dialog_bg,
                opacity=1.0,
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
                        color=accent_color,
                        overlay_color=ft.Colors.with_opacity(0.1, accent_color),
                    ),
                    on_click=lambda e: self.close_dialog()
                ),
            ],
            on_dismiss=lambda e: logging.info("Weather Dialog dismissed"),
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
