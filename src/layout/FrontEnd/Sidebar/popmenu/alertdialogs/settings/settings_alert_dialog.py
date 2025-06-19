import flet as ft
from components.responsive_text_handler import ResponsiveTextHandler
import logging
from services.translation_service import TranslationService

from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_language import DropdownLanguage
from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_measurement import DropdownMeasurement

DEFAULT_LANGUAGE = "en"  # Define a default language

class SettingsAlertDialog:
    """
    Versione semplificata per test dell'alert dialog delle impostazioni.
    """    
    def __init__(self, page, text_color, language, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None):
        self.page = page
        self.text_color = text_color
        self.language = language
        self.state_manager = state_manager
        if self.state_manager:
            self.state_manager.register_observer("language_event", self._handle_language_change)
        
        # Store callbacks for toggles
        self.handle_location_toggle_callback = handle_location_toggle
        self.handle_theme_toggle_callback = handle_theme_toggle

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

        # Initialize child dropdowns, passing new props (assuming they are refactored)
        self.language_dropdown = DropdownLanguage(
            page=self.page, # Add if DropdownLanguage needs it
            state_manager=self.state_manager,
            text_color=self.text_color,
            language=self.language,
            text_handler_get_size=self._text_handler.get_size
        )
        self.measurement_dropdown = DropdownMeasurement(
            state_manager=self.state_manager,
            page=self.page, 
            text_color=self.text_color,
            language=self.language,
            text_handler_get_size=self._text_handler.get_size
        )
        # --- Observer pattern: collega measurement_dropdown come child observer ---
        self.language_dropdown.register_child_observer(self.measurement_dropdown)
        self.language_dropdown.register_child_observer(self)  # Registra se stesso come child observer
        # Collegamento degli altri figli observer:
        if hasattr(self, 'weekly_weather'):
            self.language_dropdown.register_child_observer(self.weekly_weather)
        if hasattr(self, 'air_pollution'):
            self.language_dropdown.register_child_observer(self.air_pollution)
        if hasattr(self, 'temperature_chart'):
            self.language_dropdown.register_child_observer(self.temperature_chart)
        if hasattr(self, 'air_pollution_chart'):
            self.language_dropdown.register_child_observer(self.air_pollution_chart)

        self.location_toggle_control = None # Will hold the ft.Switch control
        self.theme_toggle_control = None    # Will hold the ft.Switch control
        self.dialog = None

    def _handle_language_change(self, new_language_code):
        self.language = new_language_code
        # If dialog is built, update its components
        if self.dialog:
            self._apply_current_styling_and_text()

        # Also ensure child dropdowns get the new language for their internal texts (e.g., hints)
        # Need to pass the current text_color and text_handler.get_size
        current_text_color = self.text_color # Or re-fetch if it could change
        current_text_handler_get_size = self._text_handler.get_size

        if hasattr(self.language_dropdown, 'update_text_sizes'):
            self.language_dropdown.update_text_sizes(current_text_handler_get_size, current_text_color, new_language_code)
        if hasattr(self.measurement_dropdown, 'update_text_sizes'):
            self.measurement_dropdown.update_text_sizes(current_text_handler_get_size, current_text_color, new_language_code)

    def _get_translation(self, key, dict_key=None):
        if dict_key:
            return TranslationService.translate_from_dict(dict_key, key, str(self.language))
        return TranslationService.translate(key, str(self.language))

    def _apply_current_styling_and_text(self):
        """Applies current text sizes, colors, language, and theme styles to the dialog."""
        if not self.dialog:
            return

        self.dialog.bgcolor = self.text_color.get("DIALOG_BACKGROUND", ft.Colors.WHITE)
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

    def createAlertDialog(self, page):
        language_dropdown_control = self.language_dropdown.build()
        measurement_dropdown_control = self.measurement_dropdown.build()
        get_size = self._text_handler.get_size
        self.dialog = ft.AlertDialog(
            title=ft.Text(
                TranslationService.translate_from_dict("settings_alert_dialog_items", "settings_alert_dialog_title", self.language),
                size=get_size('title'),
                weight=ft.FontWeight.BOLD,
                color=self.text_color["TEXT"]
            ),
            scrollable=True,
            bgcolor=self.text_color.get("DIALOG_BACKGROUND"),
            content=ft.Container(
                width=500,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LANGUAGE, size=get_size('label'), color="#ff6b35"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "language", self.language), size=get_size('label'), weight=ft.FontWeight.W_500, color=self.text_color["TEXT"]),
                                    ], spacing=10),
                                language_dropdown_control,
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.STRAIGHTEN, size=get_size('label'), color="#22c55e"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "measurement", self.language), size=get_size('label'), weight=ft.FontWeight.W_500, color=self.text_color["TEXT"]),
                                    ], spacing=10),
                                measurement_dropdown_control,
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LOCATION_ON, size=get_size('label'), color="#ef4444"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "use_current_location", self.language), size=get_size('label'), weight=ft.FontWeight.W_500, color=self.text_color["TEXT"]),
                                    ], spacing=10),
                                self._create_location_toggle_instance(),
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.DARK_MODE, size=get_size('label'), color="#3b82f6"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "dark_theme", self.language), size=get_size('label'), weight=ft.FontWeight.W_500, color=self.text_color["TEXT"]),
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
                    content=ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "close", self.language), size=get_size('body'), color=self.text_color.get("ACCENT", ft.Colors.BLUE)),
                    on_click=lambda e: self._close_dialog(e)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            open=False,
        )
        return self.dialog

    def _close_dialog(self, e=None):
        """Close the dialog when close button is clicked"""
        if self.dialog and hasattr(self.dialog, 'open'):
            self.dialog.open = False
            self.page.update()

    def open_dialog(self):
        """Creates (if necessary) and opens the alert dialog in the correct Flet sequence."""
        if not self.page:
            print("Error: Page context not available for SettingsAlertDialog.")
            return
        if self.dialog is None:
            self.createAlertDialog(self.page)
        self._apply_current_styling_and_text()
        if self.dialog not in self.page.controls:
            self.page.controls.append(self.dialog)
        self.page.dialog = self.dialog
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self):
        """Closes the alert dialog."""
        if self.dialog and self.page:
            self.dialog.open = False
            self.page.update()

    def build(self):
        """
        Builds the initial dialog structure.
        The dialog is not shown until open_dialog() is called.
        """
        if self.dialog is None:
            self.createAlertDialog(self.page)
        return self.dialog

    def did_mount(self):
        """
        Called when the control is added to the page.
        """
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self.state_manager = self.page.session.get('state_manager')
            self.language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            self.state_manager.register_observer("language_event", self.handle_language_change)

    def will_unmount(self):
        """
        Called when the control is removed from the page.
        """
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.handle_language_change)
            
    def _update_text_elements(self):
        """
        Update text elements without rebuilding the entire UI.
        """
        if not self.dialog:
            return
            
        logging.debug(f"SettingsAlertDialog._update_text_elements chiamato, language={self.language}")
        
        # Aggiorna il titolo
        if self.dialog.title and isinstance(self.dialog.title, ft.Text):
            self.dialog.title.value = TranslationService.translate_from_dict("settings_alert_dialog_items", "settings_alert_dialog_title", self.language)
            self.dialog.title.update()
            
        # Aggiorna i testi delle sezioni
        if self.dialog.content and hasattr(self.dialog.content, 'content') and isinstance(self.dialog.content.content, ft.Column):
            rows = self.dialog.content.content.controls
            
            sections_config = [
                ("language_setting", ft.Icons.LANGUAGE, "#ff6b35"), 
                ("measurement_setting", ft.Icons.STRAIGHTEN, "#22c55e"),
                ("use_current_location_setting", ft.Icons.LOCATION_ON, "#ef4444"),
                ("dark_theme_setting", ft.Icons.DARK_MODE, "#3b82f6"),
            ]
            
            for i, config in enumerate(sections_config):
                key, _, _ = config
                if len(rows) > i and isinstance(rows[i], ft.Row) and \
                   len(rows[i].controls) > 0 and isinstance(rows[i].controls[0], ft.Row) and \
                   len(rows[i].controls[0].controls) > 1:
                    
                    label_control = rows[i].controls[0].controls[1]
                    if isinstance(label_control, ft.Text):
                        label_control.value = self._get_translation(key)
                        label_control.update()
                    
        # Aggiorna button di chiusura
        if self.dialog.actions and len(self.dialog.actions) > 0:
            action_button = self.dialog.actions[0]
            if isinstance(action_button, ft.TextButton) and hasattr(action_button, 'content') and isinstance(action_button.content, ft.Text):
                action_button.content.value = self._get_translation("close_button")
                action_button.content.update()
                
        # Aggiorna i dropdown
        if self.language_dropdown and hasattr(self.language_dropdown, 'update_text_sizes'):
            self.language_dropdown.update_text_sizes(self._text_handler.get_size, self.text_color, self.language)
            
        if self.measurement_dropdown and hasattr(self.measurement_dropdown, 'update_text_sizes'):
            self.measurement_dropdown.update_text_sizes(self._text_handler.get_size, self.text_color, self.language)
            
        # Aggiorna il dialogo se è aperto
        if self.dialog and hasattr(self.dialog, 'open') and self.dialog.open:
            self.dialog.update()

    def handle_language_change(self, event_data=None):
        """
        Handle language change event.
        """
        new_language = None
        
        # Handle different formats of event_data
        if event_data is None:
            if self.state_manager:
                new_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            else:
                new_language = DEFAULT_LANGUAGE
        elif isinstance(event_data, dict):
            new_language = event_data.get('language', DEFAULT_LANGUAGE)
        elif isinstance(event_data, str):
            new_language = event_data
        else:
            logging.warning(f"handle_language_change received unexpected event_data type: {type(event_data)}")
            if self.state_manager:
                new_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            else:
                new_language = DEFAULT_LANGUAGE
        
        if self.language != new_language:
            logging.info(f"SettingsAlertDialog: Updating language from {self.language} to {new_language}")
            self.language = new_language
            self._update_text_elements()
            # Verifica se il dialog è attualmente visualizzato
            if self.dialog and hasattr(self.dialog, 'open') and self.dialog.open:
                self._apply_current_styling_and_text()
    def cleanup(self):
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self._handle_language_change)
        # Add other cleanup if necessary, e.g., for self._text_handler if it uses observers

    def on_language_change(self, new_language_code):
        """Metodo chiamato dal parent observer per aggiornare la lingua e i testi delle label."""
        self.language = new_language_code
        # Aggiorna le label/dialoghi/testi
        if self.dialog:
            self._apply_current_styling_and_text()
        # Aggiorna anche i dropdown se necessario
        if hasattr(self.language_dropdown, 'update_text_sizes'):
            self.language_dropdown.update_text_sizes(self._text_handler.get_size, self.text_color, new_language_code)
        if hasattr(self.measurement_dropdown, 'update_text_sizes'):
            self.measurement_dropdown.update_text_sizes(self._text_handler.get_size, self.text_color, new_language_code)

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
