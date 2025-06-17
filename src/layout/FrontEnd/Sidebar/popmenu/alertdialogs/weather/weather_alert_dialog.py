import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class WeatherAlertDialog:
        
    def __init__(self, page: ft.Page, state_manager=None, translation_service=None, 
                 handle_location_toggle=None, handle_theme_toggle=None, 
                 text_color: str = None, language: str = "en"):
        self.page = page
        self.state_manager = state_manager
        self.translation_service = translation_service or (page.session.get('translation_service') if page else None)
        self.handle_location_toggle = handle_location_toggle # Will be used for toggles if re-added
        self.handle_theme_toggle = handle_theme_toggle # Will be used for toggles if re-added
        
        self.current_language = language

        self.text_color = text_color if text_color else (DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"])
        self.dialog = None

        # ResponsiveTextHandler locale come in main_information
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20,
                'body': 14,
                'icon': 20,
            },
            breakpoints=[600, 900, 1200, 1600]
        )

        # Controls will be initialized in createAlertDialog
        self.title_text_control = None
        self.language_text_control = None
        self.measurement_text_control = None
        self.location_text_control = None
        self.theme_text_control = None
        self.close_button_text_control = None
        self.language_icon_control = None
        self.measurement_icon_control = None
        self.location_icon_control = None
        self.theme_icon_control = None
        
        self.createAlertDialog()

    def update_text_sizes(self, text_color, language):
        self.text_color = text_color
        self.current_language = language
        if not self.dialog or not self._text_handler:
            return
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        self.dialog.bgcolor = current_theme["DIALOG_BACKGROUND"]
        title_size = self._text_handler.get_size('title')
        body_size = self._text_handler.get_size('body')
        icon_size = self._text_handler.get_size('icon')

        if self.title_text_control:
            self.title_text_control.value = self._get_translation("weather")
            self.title_text_control.size = title_size
            self.title_text_control.color = self.text_color
        
        if self.language_text_control:
            self.language_text_control.value = self._get_translation("language_setting")
            self.language_text_control.size = body_size
            self.language_text_control.color = self.text_color

        if self.measurement_text_control:
            self.measurement_text_control.value = self._get_translation("measurement_setting")
            self.measurement_text_control.size = body_size
            self.measurement_text_control.color = self.text_color

        if self.location_text_control:
            self.location_text_control.value = self._get_translation("use_current_location_setting")
            self.location_text_control.size = body_size
            self.location_text_control.color = self.text_color
            
        if self.theme_text_control:
            self.theme_text_control.value = self._get_translation("dark_theme_setting")
            self.theme_text_control.size = body_size
            self.theme_text_control.color = self.text_color

        if self.close_button_text_control:
            self.close_button_text_control.value = self._get_translation("close_button")
            self.close_button_text_control.color = current_theme["ACCENT"]
            self.close_button_text_control.size = body_size
            if self.dialog.actions and isinstance(self.dialog.actions[0], ft.TextButton):
                self.dialog.actions[0].style.color = current_theme["ACCENT"]
                self.dialog.actions[0].style.overlay_color = ft.Colors.with_opacity(0.1, current_theme["ACCENT"])

        if self.language_icon_control:
            self.language_icon_control.size = icon_size
        if self.measurement_icon_control:
            self.measurement_icon_control.size = icon_size
        if self.location_icon_control:
            self.location_icon_control.size = icon_size
        if self.theme_icon_control:
            self.theme_icon_control.size = icon_size
        
        if self.dialog.page: # Check if dialog is on page before updating
            self.dialog.update()
        elif self.page: 
            self.page.update() # Fallback, though dialog should ideally be on page to update

    def _get_translation(self, key):
        if self.translation_service and hasattr(self.translation_service, 'get_text'):
            return self.translation_service.get_text(key, self.current_language)
        return key 

    def createAlertDialog(self):
        current_get_size = self._text_handler.get_size
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        dialog_text_color = self.text_color
        bg_color = current_theme["DIALOG_BACKGROUND"]
        title_size = current_get_size('title')
        body_size = current_get_size('body')
        icon_size = current_get_size('icon')

        self.title_text_control = ft.Text(
            self._get_translation("weather"), 
            size=title_size, 
            weight=ft.FontWeight.BOLD, 
            color=dialog_text_color
        )
        
        self.language_icon_control = ft.Icon(ft.Icons.LANGUAGE, size=icon_size, color="#ff6b35")
        self.measurement_icon_control = ft.Icon(ft.Icons.STRAIGHTEN, size=icon_size, color="#22c55e")
        self.location_icon_control = ft.Icon(ft.Icons.LOCATION_ON, size=icon_size, color="#ef4444")
        self.theme_icon_control = ft.Icon(ft.Icons.DARK_MODE, size=icon_size, color="#3b82f6")
        
        self.language_text_control = ft.Text(self._get_translation("language_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        self.measurement_text_control = ft.Text(self._get_translation("measurement_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        self.location_text_control = ft.Text(self._get_translation("use_current_location_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        self.theme_text_control = ft.Text(self._get_translation("dark_theme_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        
        self.close_button_text_control = ft.Text(self._get_translation("close_button"), color=current_theme["ACCENT"], size=body_size)

        self.dialog = ft.AlertDialog(
            title=self.title_text_control,
            bgcolor=bg_color,
            content=ft.Container(
                width=400,
                content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(controls=[self.language_icon_control, self.language_text_control], spacing=10),
                            # Placeholder for language_dropdown (e.g., self.language_dropdown.build())
                        ],
                        spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Row(controls=[self.measurement_icon_control, self.measurement_text_control], spacing=10),
                            # Placeholder for measurement_dropdown (e.g., self.measurement_dropdown.build())
                        ],
                        spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Row(controls=[self.location_icon_control, self.location_text_control], spacing=10),
                            # Placeholder for location_toggle (e.g., self.create_location_toggle())
                        ],
                        spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Row(controls=[self.theme_icon_control, self.theme_text_control], spacing=10),
                            # Placeholder for theme_toggle (e.g., self.create_theme_toggle())
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
                    content=self.close_button_text_control,
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

    def open_dialog(self):
        if not self.dialog:
            self.createAlertDialog()
        if self.page and self.dialog:
            if self.dialog not in self.page.controls:
                self.page.controls.append(self.dialog)
            self.page.dialog = self.dialog
            self.page.dialog.open = True
            self.update_text_sizes(self.text_color, self.current_language)
            self.page.update()

    def close_dialog(self):
        if self.dialog:
            self.dialog.open = False
            if self.page:
                 self.page.update()

    def cleanup(self):
        print(f"Cleaning up WeatherAlertDialog for page: {self.page}")
        # No specific observers to unregister in this version
        pass