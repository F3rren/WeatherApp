import flet as ft
from components.responsive_text_handler import ResponsiveTextHandler

from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_language import DropdownLanguage
from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_measurement import DropdownMeasurement

class SettingsAlertDialog:
    """
    Versione semplificata per test dell'alert dialog delle impostazioni.
    """    
    def __init__(self, page, text_color, language, state_manager=None, translation_service=None, handle_location_toggle=None, handle_theme_toggle=None):
        self.page = page
        self.text_color = text_color
        self.language = language
        self.state_manager = state_manager
        self.translation_service = translation_service or (page.session.get('translation_service') if page else None)
        
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
        
        self.location_toggle_control = None # Will hold the ft.Switch control
        self.theme_toggle_control = None    # Will hold the ft.Switch control
        self.dialog = None

    def _get_translation(self, key):
        """Helper method to get translation with fallback"""
        if self.translation_service and hasattr(self.translation_service, 'get_text'):
            # Use self.language which is passed in and updated
            return self.translation_service.get_text(key, self.language)
        return key  # Fallback to key if no translation service

    def _create_location_toggle_instance(self):
        using_location = self.state_manager.get_state('using_location') if self.state_manager else False
        self.location_toggle_control = ft.Switch(
            value=using_location,
            on_change=self.handle_location_toggle_callback 
        )
        # Styling will be applied by _apply_current_styling_and_text
        return self.location_toggle_control
    
    def _create_theme_toggle_instance(self):
        is_dark_mode_active = self.page.theme_mode == ft.ThemeMode.DARK
        self.theme_toggle_control = ft.Switch(
            value=is_dark_mode_active,
            on_change=self.handle_theme_toggle_callback
        )
        # Styling will be applied by _apply_current_styling_and_text
        return self.theme_toggle_control

    def update_text_sizes(self, text_color, language):
        self.text_color = text_color
        self.language = language
        if hasattr(self.language_dropdown, 'update_text_sizes'):
            self.language_dropdown.update_text_sizes(self._text_handler.get_size, text_color, language)
        if hasattr(self.measurement_dropdown, 'update_text_sizes'):
            self.measurement_dropdown.update_text_sizes(self._text_handler.get_size, text_color, language)
        if self.dialog:
            self._apply_current_styling_and_text()

    def _apply_current_styling_and_text(self):
        """Applies current text sizes, colors, language, and theme styles to the dialog."""
        if not self.dialog:
            return

        # Update dialog properties
        self.dialog.bgcolor = self.text_color.get("DIALOG_BACKGROUND", ft.Colors.WHITE)
        if isinstance(self.dialog.title, ft.Text):
            self.dialog.title.value = self._get_translation("settings")
            self.dialog.title.size = self._text_handler.get_size('title')
            self.dialog.title.color = self.text_color["TEXT"] 
        
        # Update content: labels, icons, etc.
        if self.dialog.content and hasattr(self.dialog.content, 'content') and isinstance(self.dialog.content.content, ft.Column):
            rows = self.dialog.content.content.controls
            
            sections_config = [
                ("language_setting", ft.Icons.LANGUAGE, "#ff6b35"), 
                ("measurement_setting", ft.Icons.STRAIGHTEN, "#22c55e"),
                ("use_current_location_setting", ft.Icons.LOCATION_ON, "#ef4444"),
                ("dark_theme_setting", ft.Icons.DARK_MODE, "#3b82f6"),
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
                        label_control.value = self._get_translation(key)
                        label_control.size = self._text_handler.get_size('body')
                        label_control.color = self.text_color["TEXT"] 
            
        # Update actions (close button)
        if self.dialog.actions and len(self.dialog.actions) > 0:
            action_button = self.dialog.actions[0]
            if isinstance(action_button, ft.TextButton) and hasattr(action_button, 'content') and isinstance(action_button.content, ft.Text):
                action_button.content.value = self._get_translation("close_button")
                action_button.content.size = self._text_handler.get_size('body')
                action_button.content.color = self.text_color.get("ACCENT", ft.Colors.BLUE)
            action_button.style = ft.ButtonStyle(
                color=self.text_color.get("ACCENT"), 
                overlay_color=ft.Colors.with_opacity(0.1, self.text_color.get("ACCENT")), 
            )

        # Update toggles appearance
        if self.location_toggle_control:
            self.location_toggle_control.active_color = self.text_color.get("ACCENT") 
            self.location_toggle_control.active_track_color = ft.Colors.with_opacity(0.5, self.text_color.get("ACCENT")) 

        if self.theme_toggle_control:
            self.theme_toggle_control.value = self.page.theme_mode == ft.ThemeMode.DARK 
            self.theme_toggle_control.active_color = self.text_color.get("ACCENT") 
            self.theme_toggle_control.active_track_color = ft.Colors.with_opacity(0.5, self.text_color.get("ACCENT")) 

        # Only call update on the dialog if it's already the page's dialog and is open
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog == self.dialog and self.dialog.open:
            self.dialog.update()

    def createAlertDialog(self, page): # page parameter is kept for consistency, uses self.page
        language_dropdown_control = self.language_dropdown.build()
        measurement_dropdown_control = self.measurement_dropdown.build()
        get_size = self._text_handler.get_size
        self.dialog = ft.AlertDialog(
            title=ft.Text(
                self._get_translation("settings"), 
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
                        # Language Section
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LANGUAGE, size=get_size('label'), color="#ff6b35"),
                                        ft.Text(self._get_translation("language_setting"), size=get_size('label'), weight=ft.FontWeight.W_500, color=self.text_color["TEXT"]),
                                    ], spacing=10),
                                language_dropdown_control,
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        # Measurement Section
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.STRAIGHTEN, size=get_size('label'), color="#22c55e"),
                                        ft.Text(self._get_translation("measurement_setting"), size=get_size('label'), weight=ft.FontWeight.W_500, color=self.text_color["TEXT"]),
                                    ], spacing=10),
                                measurement_dropdown_control,
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        # Location Section
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LOCATION_ON, size=get_size('label'), color="#ef4444"),
                                        ft.Text(self._get_translation("use_current_location_setting"), size=get_size('label'), weight=ft.FontWeight.W_500, color=self.text_color["TEXT"]),
                                    ], spacing=10),
                                self._create_location_toggle_instance(), 
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        # Theme Section
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.DARK_MODE, size=get_size('label'), color="#3b82f6"),
                                        ft.Text(self._get_translation("dark_theme_setting"), size=get_size('label'), weight=ft.FontWeight.W_500, color=self.text_color["TEXT"]),
                                    ], spacing=10),
                                self._create_theme_toggle_instance(), 
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ],
                    expand=True, 
                    spacing=20,
                ),
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text(
                        self._get_translation("close_button"), 
                        size=get_size('body'), 
                        color=self.text_color.get("ACCENT") 
                    ),
                    style=ft.ButtonStyle( 
                        color=self.text_color.get("ACCENT"), 
                        overlay_color=ft.Colors.with_opacity(0.1, self.text_color.get("ACCENT")), 
                    ),
                    on_click=lambda e: self.close_dialog()
                ),
            ],
        )

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