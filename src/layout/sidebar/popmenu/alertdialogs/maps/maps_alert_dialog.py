import flet as ft
from utils.config import DARK_THEME, LIGHT_THEME
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService

class MapsAlertDialog:
    def __init__(self, page: ft.Page, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, 
                 text_color: str = None, language: str = "en"):
        self.page = page
        self.state_manager = state_manager
        self.current_language = language
        self.text_color = text_color if text_color else (DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"])
        self.dialog = None
        # ResponsiveTextHandler locale
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20,
                'body': 14,
                'icon': 20,
            },
            breakpoints=[600, 900, 1200, 1600]
        )

        # Controls to be initialized in createAlertDialog
        self.title_text_control = None
        self.content_text_control = None
        self.close_button_text_control = None
        
        if state_manager:
            # Only register for theme_event if it's handled by this class directly
            # The new pattern is that parent calls update_text_sizes, which handles theme indirectly
            # However, if direct theme updates are needed for bgcolor etc., this can be kept.
            # For now, relying on update_text_sizes to be called by parent.
            # state_manager.register_observer("theme_event", self.handle_theme_event) # Re-evaluate if needed
            pass # No direct observers needed if parent manages updates

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

        if self.title_text_control:
            self.title_text_control.value = self._get_translation("maps")
            self.title_text_control.size = title_size
            self.title_text_control.color = self.text_color

        if self.content_text_control:
            # Assuming a generic content text for now
            self.content_text_control.value = self._get_translation("maps_content_placeholder") # Example key
            self.content_text_control.size = body_size
            self.content_text_control.color = self.text_color

        if self.close_button_text_control:
            self.close_button_text_control.value = self._get_translation("close_button")
            self.close_button_text_control.color = current_theme["ACCENT"]
            self.close_button_text_control.size = body_size # Assuming body size for button text
            if self.dialog.actions and isinstance(self.dialog.actions[0], ft.TextButton):
                self.dialog.actions[0].style.color = current_theme["ACCENT"]
                self.dialog.actions[0].style.overlay_color = ft.Colors.with_opacity(0.1, current_theme["ACCENT"])
        
        if self.dialog.page:
            self.dialog.update()
        elif self.page:
            self.page.update()

    def _get_translation(self, key):
        return TranslationService.translate(key, str(self.current_language))

    def createAlertDialog(self):
        get_size = self._text_handler.get_size
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        dialog_text_color = self.text_color
        bg_color = current_theme["DIALOG_BACKGROUND"]

        title_size = get_size('title')
        body_size = get_size('body')

        self.title_text_control = ft.Text(
            self._get_translation("maps"),
            size=title_size,
            weight=ft.FontWeight.BOLD, 
            color=dialog_text_color
        )
        
        self.content_text_control = ft.Text(
            self._get_translation("maps_content_placeholder"), # Example key
            size=body_size, 
            color=dialog_text_color
        )
        
        self.close_button_text_control = ft.Text(
            self._get_translation("close_button"), 
            color=current_theme["ACCENT"], 
            size=body_size
        )

        self.dialog = ft.AlertDialog(
            title=self.title_text_control,
            bgcolor=bg_color,
            content=ft.Container(
                width=400,
                content=ft.Column(
                    controls=[
                        self.content_text_control,
                    ],
                    spacing=20,
                    height=200, # Adjust as needed
                ),
            ),
            actions=[
                ft.TextButton(
                    content=self.close_button_text_control,
                    style=ft.ButtonStyle(
                        color=current_theme["ACCENT"],
                        overlay_color=ft.Colors.with_opacity(0.1, current_theme["ACCENT"])
                    ),
                    on_click=lambda e: self.close_dialog()
                ),
            ],
            on_dismiss=lambda e: print("Maps dialog dismissed"), # Or self.close_dialog()
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
        # If any observers were registered with state_manager by this instance, unregister them here.
        # Example: if self.state_manager and hasattr(self, 'handle_theme_event'):
        # self.state_manager.unregister_observer("theme_event", self.handle_theme_event)
        print(f"Cleaning up MapsAlertDialog for page: {self.page}")
        pass
