import logging
import flet as ft
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
from layout.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_language import DropdownLanguage
from layout.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_measurement import DropdownMeasurement


class SettingsAlertDialog:
    """
    Versione semplificata per test dell'alert dialog delle impostazioni.
    Refactored: exposes only __init__, update_ui, build as public methods.
    """    
    def __init__(self, page, theme_handler, language, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None):
        self.page = page
        self.theme_handler = theme_handler
        self.language = language
        self.state_manager = state_manager
        self.handle_location_toggle_callback = handle_location_toggle
        self.handle_theme_toggle_callback = handle_theme_toggle
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20,
                'body': 14,
                'icon': 20,
                'label': 15,
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        self.language_dropdown = None
        self.measurement_dropdown = None
        self.location_toggle_control = None
        self.theme_toggle_control = None
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)

    def _init_dropdowns(self):
        # Always use theme_handler for color
        text_color = self.theme_handler.get_text_color() if self.theme_handler else {"TEXT": "#000000"}
        self.language_dropdown = DropdownLanguage(
            page=self.page,
            state_manager=self.state_manager,
            text_color=text_color,
            language=self.language,
            text_handler_get_size=self._text_handler.get_size
        )
        self.measurement_dropdown = DropdownMeasurement(
            state_manager=self.state_manager,
            page=self.page, 
            text_color=text_color,
            language=self.language,
            text_handler_get_size=self._text_handler.get_size
        )
        self.language_dropdown.register_child_observer(self.measurement_dropdown)
        self.language_dropdown.register_child_observer(self)

    def update_ui(self, event_data=None):
        self.language = self.state_manager.get_state('language') if self.state_manager else self.language
        self._init_dropdowns()
        if self.dialog:
            self._apply_current_styling_and_text()

    def build(self):
        self._init_dropdowns()
        return self.createAlertDialog(self.page)

    # --- Internal helpers and dialog logic remain private ---
    def createAlertDialog(self, page):
        # Always use theme_handler for all color logic
        text_color = self.theme_handler.get_text_color() if self.theme_handler else {"TEXT": "#000000"}
        if isinstance(text_color, str):
            text_color = {"TEXT": text_color, "DIALOG_BACKGROUND": "#fff", "ACCENT": "#0078d4"}
        # Support dark mode for dialog background
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        dialog_bg = "#161b22" if is_dark else "#ffffff"
        # (Stateless: do not check or update self.dialog here)

        language_dropdown_control = self.language_dropdown.build()
        measurement_dropdown_control = self.measurement_dropdown.build()
        get_size = self._text_handler.get_size
        self.dialog = ft.AlertDialog(
            title=ft.Text(
                TranslationService.translate_from_dict("settings_alert_dialog_items", "settings_alert_dialog_title", self.language),
                size=get_size('title'),
                weight=ft.FontWeight.BOLD,
                color=text_color["TEXT"]
            ),
            scrollable=True,
            bgcolor=dialog_bg,
            content=ft.Container(
                width=500,
                bgcolor=dialog_bg,  # Usa il colore dinamico in base al tema
                opacity=1.0,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LANGUAGE, size=get_size('label'), color="#ff6b35"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "language", self.language), size=get_size('label'), weight=ft.FontWeight.W_500, color=text_color["TEXT"]),
                                    ], spacing=10),
                                language_dropdown_control,
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.STRAIGHTEN, size=get_size('label'), color="#22c55e"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "measurement", self.language), size=get_size('label'), weight=ft.FontWeight.W_500, color=text_color["TEXT"]),
                                    ], spacing=10),
                                measurement_dropdown_control,
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LOCATION_ON, size=get_size('label'), color="#ef4444"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "use_current_location", self.language), size=get_size('label'), weight=ft.FontWeight.W_500, color=text_color["TEXT"]),
                                    ], spacing=10),
                                self._create_location_toggle_instance(),
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.DARK_MODE, size=get_size('label'), color="#3b82f6"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "dark_theme", self.language), size=get_size('label'), weight=ft.FontWeight.W_500, color=text_color["TEXT"]),
                                    ], spacing=10),
                                self._create_theme_toggle_instance(),
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ],
                    spacing=20,
                ),
                padding=ft.padding.all(20),
            ),
            actions=[                
                ft.TextButton(
                    content=ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "close", self.language), size=get_size('body'), color=text_color.get("ACCENT", ft.Colors.BLUE)),
                    on_click=lambda e: self._close_dialog(e)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            open=False,
        )
        return self.dialog

    def _apply_current_styling_and_text(self):
        """Applies current text sizes, colors, language, and theme styles to the dialog."""
        if not self.dialog:
            return
        # Always get the latest theme colors
        text_color = self.theme_handler.get_text_color() if self.theme_handler else {"TEXT": "#000000"}
        if isinstance(text_color, str):
            text_color = {"TEXT": text_color, "DIALOG_BACKGROUND": "#fff", "ACCENT": "#0078d4"}
        self.text_color = text_color

        # Support dark mode for dialog background also on update
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        dialog_bg = "#161b22" if is_dark else "#ffffff"
        self.dialog.bgcolor = dialog_bg
        if self.dialog.content and hasattr(self.dialog.content, 'bgcolor'):
            self.dialog.content.bgcolor = dialog_bg
        if self.dialog.content and hasattr(self.dialog.content, 'opacity'):
            self.dialog.content.opacity = 1.0
        self.dialog.bgcolor = self.text_color.get("DIALOG_BACKGROUND", "#ffffff")
        if isinstance(self.dialog.title, ft.Text):
            self.dialog.title.value = TranslationService.translate_from_dict("settings_alert_dialog_items", "settings_alert_dialog_title", self.language)
            self.dialog.title.size = self._text_handler.get_size('title')
            self.dialog.title.color = self.text_color["TEXT"]

        if self.dialog.content and hasattr(self.dialog.content, 'content') and isinstance(self.dialog.content.content, ft.Column):
            rows = self.dialog.content.content.controls
            sections_config = [
                ("language", ft.Icons.LANGUAGE, "#ff6b35"),
                ("measurement", ft.Icons.STRAIGHTEN, "#22c55e"),
                ("use_current_location", ft.Icons.LOCATION_ON, "#ef4444"),
                ("dark_theme", ft.Icons.DARK_MODE, "#3b82f6"),
            ]
            for i, config in enumerate(sections_config):
                key, icon_name, icon_color_val = config
                if len(rows) > i and isinstance(rows[i], ft.Row) and \
                   len(rows[i].controls) > 0 and isinstance(rows[i].controls[0], ft.Row) and \
                   len(rows[i].controls[0].controls) > 1:
                    icon_control = rows[i].controls[0].controls[0]
                    label_control = rows[i].controls[0].controls[1]
                    if isinstance(icon_control, ft.Icon):
                        icon_control.size = self._text_handler.get_size('icon')
                        icon_control.color = icon_color_val
                    if isinstance(label_control, ft.Text):
                        label_control.value = self._get_translation(key, "settings_alert_dialog_items")
                        label_control.size = self._text_handler.get_size('body')
                        label_control.color = self.text_color["TEXT"]
        if self.dialog.actions and len(self.dialog.actions) > 0:
            action_button = self.dialog.actions[0]
            if isinstance(action_button, ft.TextButton) and hasattr(action_button, 'content') and isinstance(action_button.content, ft.Text):
                action_button.content.value = self._get_translation("close", "settings_alert_dialog_items")
                action_button.content.size = self._text_handler.get_size('body')
                action_button.content.color = self.text_color.get("ACCENT", ft.Colors.BLUE)
            action_button.style = ft.ButtonStyle(
                color=self.text_color.get("ACCENT"),
                overlay_color=ft.Colors.with_opacity(0.1, self.text_color.get("ACCENT")),
            )
        if self.location_toggle_control:
            self.location_toggle_control.active_color = self.text_color.get("ACCENT")
            self.location_toggle_control.active_track_color = ft.Colors.with_opacity(0.5, self.text_color.get("ACCENT"))
        if self.theme_toggle_control:
            self.theme_toggle_control.value = self.page.theme_mode == ft.ThemeMode.DARK
            self.theme_toggle_control.active_color = self.text_color.get("ACCENT")
            self.theme_toggle_control.active_track_color = ft.Colors.with_opacity(0.5, self.text_color.get("ACCENT"))
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog == self.dialog and self.dialog.open:
            self.dialog.update()

    def _get_translation(self, key, dict_key=None):
        if dict_key:
            return TranslationService.translate_from_dict(dict_key, key, str(self.language))
        return TranslationService.translate(key, str(self.language))

    def _close_dialog(self, e=None):
        """Close the dialog when close button is clicked"""
        if self.dialog and hasattr(self.dialog, 'open'):
            self.dialog.open = False
            self.page.update()

    def open_dialog(self):
        """Always (re)builds and opens the alert dialog in the correct Flet sequence."""
        if not self.page:
            logging.error("Error: Page context not available for SettingsAlertDialog.")
            return
        dialog = self.build()
        if dialog not in self.page.controls:
            self.page.controls.append(dialog)
        self.page.dialog = dialog
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self):
        """Closes the alert dialog."""
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def _create_location_toggle_instance(self):
        if self.location_toggle_control is None:
            self.location_toggle_control = ft.Switch(
                value=False,  # Puoi collegare qui lo stato reale se disponibile
                on_change=self.handle_location_toggle_callback,
                active_color="#ef4444",
                inactive_thumb_color="#cccccc",
                inactive_track_color="#eeeeee",
            )
        return self.location_toggle_control

    def _create_theme_toggle_instance(self):
        if self.theme_toggle_control is None:
            self.theme_toggle_control = ft.Switch(
                value=False,  # Puoi collegare qui lo stato reale se disponibile
                on_change=self.handle_theme_toggle_callback,
                active_color="#3b82f6",
                inactive_thumb_color="#cccccc",
                inactive_track_color="#eeeeee",
            )
        return self.theme_toggle_control

    def cleanup(self):
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
