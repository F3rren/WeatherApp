import logging
import flet as ft

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

        self.language_dropdown = None
        self.measurement_dropdown = None
        self.theme_toggle_control = None
        self.dialog = None  # Initialize dialog attribute
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)

    def _init_dropdowns(self):
        # Always use theme_handler for color
        text_color = self.theme_handler.get_text_color() if self.theme_handler else {"TEXT": "#000000"}
        if isinstance(text_color, str):
            text_color = {"TEXT": text_color, "ACCENT": "#3b82f6"}
        self.language_dropdown = DropdownLanguage(
            page=self.page,
            state_manager=self.state_manager,
            text_color=text_color,
            language=self.language,
        )
        self.measurement_dropdown = DropdownMeasurement(
            state_manager=self.state_manager,
            page=self.page, 
            text_color=text_color,
            language=self.language,
        )
        self.language_dropdown.register_child_observer(self.measurement_dropdown)
        self.language_dropdown.register_child_observer(self)

    def on_language_change(self, new_language_code):
        """Called when language changes from the dropdown."""
        logging.info(f"Settings dialog received language change notification: {new_language_code}")
        self.language = new_language_code
        
        # Update UI to reflect the language change
        if self.dialog:
            self._apply_current_styling_and_text()

    def update_ui(self, event_data=None):
        """Update UI based on current state with instant theme application."""
        logging.debug(f"Settings dialog update_ui called with event_data: {event_data}")
        
        # Update language from state manager
        if self.state_manager:
            current_language = self.state_manager.get_state('language')
            if current_language and current_language != self.language:
                self.language = current_language
                logging.info(f"Settings dialog language updated to: {self.language}")
        
        # Force reinitialize dropdowns with new state
        self._init_dropdowns()
        
        # Update theme switch to reflect current theme
        if self.theme_toggle_control:
            current_theme_value = False
            if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
                current_theme_value = self.page.theme_mode == ft.ThemeMode.DARK
            elif self.state_manager:
                theme_mode = self.state_manager.get_state('theme_mode')
                if theme_mode is not None:
                    current_theme_value = theme_mode == 'dark'
            
            self.theme_toggle_control.value = current_theme_value
            
            # Update theme switch colors immediately
            text_color = self.theme_handler.get_text_color() if self.theme_handler else {"TEXT": "#000000"}
            if isinstance(text_color, str):
                text_color = {"TEXT": text_color, "ACCENT": "#3b82f6"}
            if isinstance(text_color, dict):
                self.theme_toggle_control.active_color = text_color.get("ACCENT", "#3b82f6")
                self.theme_toggle_control.active_track_color = ft.Colors.with_opacity(0.5, text_color.get("ACCENT", "#3b82f6"))
            
            try:
                if hasattr(self.theme_toggle_control, 'page') and self.theme_toggle_control.page:
                    self.theme_toggle_control.update()
            except Exception:
                pass
        
        # Apply complete theme and text updates
        if self.dialog:
            self._apply_current_styling_and_text()
            self._force_update_all_components()
            
            # Force update if dialog is open
            if hasattr(self.dialog, 'open') and self.dialog.open:
                try:
                    self.dialog.update()
                    if self.page:
                        self.page.update()
                except Exception as e:
                    logging.debug(f"Error updating dialog: {e}")
        
        logging.debug("Settings dialog update_ui completed")

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
        def get_size(k):
            if k == 'title':
                return 20
            elif k == 'label':
                return 16
            elif k == 'body':
                return 14
            elif k == 'icon':
                return 20
            return 14
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
                        # Language settings row
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LANGUAGE, size=16, color="#ff6b35"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "language", self.language), size=16, weight=ft.FontWeight.W_500, color=text_color["TEXT"]),
                                    ], spacing=10),
                                language_dropdown_control,
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        
                        # Unit measurement row
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.STRAIGHTEN, size=16, color="#22c55e"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "measurement", self.language), size=16, weight=ft.FontWeight.W_500, color=text_color["TEXT"]),
                                    ], spacing=10),
                                measurement_dropdown_control,
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        
                        # Location toggle row
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LOCATION_ON, size=16, color="#ef4444"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "use_current_location", self.language), size=16, weight=ft.FontWeight.W_500, color=text_color["TEXT"]),
                                    ], spacing=10),
                                self._create_location_button_instance(text_color),
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        
                        # Theme toggle row
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.DARK_MODE, size=16, color="#3b82f6"),
                                        ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "dark_theme", self.language), size=16, weight=ft.FontWeight.W_500, color=text_color["TEXT"]),
                                    ], spacing=10),
                                self._create_theme_toggle_instance(),
                            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        
                        # Divider
                        ft.Divider(color=ft.Colors.with_opacity(0.2, text_color["TEXT"])),
                        
                        # App information section
                        self._build_app_info_section(text_color),
                        
                        # Quick actions section
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text=self._get_translation_local("refresh_data"),
                                    icon=ft.Icons.REFRESH,
                                    on_click=self._refresh_weather_data,
                                    bgcolor=ft.Colors.with_opacity(0.1, text_color.get("ACCENT", "#0078d4")),
                                    color=text_color.get("ACCENT", "#0078d4"),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    )
                                ),
                                ft.ElevatedButton(
                                    text=self._get_translation_local("reset_settings"),
                                    icon=ft.Icons.RESTORE,
                                    on_click=self._reset_settings,
                                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE),
                                    color=ft.Colors.ORANGE_700,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    )
                                ),
                                ft.OutlinedButton(
                                    text=self._get_translation_local("about_app"),
                                    icon=ft.Icons.INFO_OUTLINE,
                                    on_click=self._show_about_dialog,
                                    style=ft.ButtonStyle(
                                        color=text_color.get("ACCENT", "#0078d4"),
                                        side=ft.BorderSide(1, text_color.get("ACCENT", "#0078d4")),
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    )
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ],
                    spacing=20,
                ),
                padding=ft.padding.all(20),
            ),
            actions=[                
                ft.TextButton(
                    content=ft.Text(TranslationService.translate_from_dict("settings_alert_dialog_items", "close", self.language), size=14, color=text_color.get("ACCENT", ft.Colors.BLUE)),
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
            
        logging.debug("Applying current styling and text to settings dialog")
            
        # Get current state
        if self.state_manager:
            current_language = self.state_manager.get_state('language')
            if current_language:
                self.language = current_language
            
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
        
        # Update dialog background
        self.dialog.bgcolor = dialog_bg
        if self.dialog.content and hasattr(self.dialog.content, 'bgcolor'):
            self.dialog.content.bgcolor = dialog_bg
        if self.dialog.content and hasattr(self.dialog.content, 'opacity'):
            self.dialog.content.opacity = 1.0
            
        # Update title with current language and theme
        if isinstance(self.dialog.title, ft.Text):
            self.dialog.title.value = TranslationService.translate_from_dict("settings_alert_dialog_items", "settings_alert_dialog_title", self.language)
            self.dialog.title.size = 20
            self.dialog.title.weight = ft.FontWeight.BOLD
            self.dialog.title.color = self.text_color["TEXT"]

        # Update content controls with current language and theme
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
                        icon_control.size = 20
                        icon_control.color = icon_color_val
                    if isinstance(label_control, ft.Text):
                        # Update text with current language
                        label_control.value = TranslationService.translate_from_dict("settings_alert_dialog_items", key, self.language)
                        label_control.size = 16
                        label_control.weight = ft.FontWeight.W_500
                        label_control.color = self.text_color["TEXT"]
                        
        # Update action buttons with current language and theme
        if self.dialog.actions and len(self.dialog.actions) > 0:
            action_button = self.dialog.actions[0]
            if isinstance(action_button, ft.TextButton) and hasattr(action_button, 'content') and isinstance(action_button.content, ft.Text):
                action_button.content.value = TranslationService.translate_from_dict("settings_alert_dialog_items", "close", self.language)
                action_button.content.size = 14
                action_button.content.color = self.text_color.get("ACCENT", ft.Colors.BLUE)
            
            # Update button style with theme colors
            action_button.style = ft.ButtonStyle(
                color=self.text_color.get("ACCENT", "#0078d4"),
                overlay_color=ft.Colors.with_opacity(0.1, self.text_color.get("ACCENT", "#0078d4")),
            )
            
        # Update theme switch colors and value
        if self.theme_toggle_control:
            self.theme_toggle_control.value = is_dark
            self.theme_toggle_control.active_color = self.text_color.get("ACCENT", "#3b82f6")
            self.theme_toggle_control.active_track_color = ft.Colors.with_opacity(0.5, self.text_color.get("ACCENT", "#3b82f6"))
            self.theme_toggle_control.inactive_thumb_color = "#cccccc" if not is_dark else "#666666"
            self.theme_toggle_control.inactive_track_color = "#eeeeee" if not is_dark else "#333333"
            
        # Update dropdown controls with current theme
        if self.language_dropdown:
            try:
                self.language_dropdown.update_text_sizes(self.text_color, self.language)
                self.language_dropdown.update_theme_colors(self.text_color, is_dark)
            except Exception as e:
                logging.debug(f"Error updating language dropdown: {e}")
                
        if self.measurement_dropdown:
            try:
                self.measurement_dropdown.update_text_sizes(self.text_color, self.language)
                self.measurement_dropdown.update_theme_colors(self.text_color, is_dark)
            except Exception as e:
                logging.debug(f"Error updating measurement dropdown: {e}")
        
        # Update app info section with current theme
        self._update_app_info_section_theme()
        
        # Update action buttons in the quick actions section
        self._update_action_buttons_theme()
        
        logging.debug("Styling and text application completed")

    def _force_update_all_components(self):
        """Force update all dialog components."""
        if not self.dialog or not self.page:
            return
            
        try:
            logging.debug("Force updating all dialog components")
            
            # Update individual controls if dialog is open and connected
            if hasattr(self.page, 'dialog') and self.page.dialog == self.dialog and self.dialog.open:
                # Update dropdown controls
                if self.language_dropdown and hasattr(self.language_dropdown, 'dropdown'):
                    try:
                        self.language_dropdown.dropdown.update()
                    except Exception:
                        pass
                        
                if self.measurement_dropdown and hasattr(self.measurement_dropdown, 'dropdown'):
                    try:
                        self.measurement_dropdown.dropdown.update()
                    except Exception:
                        pass
                        
                # Update theme toggle control
                if self.theme_toggle_control:
                    try:
                        self.theme_toggle_control.update()
                    except Exception:
                        pass
                
                # Update all text controls recursively
                self._update_text_controls_recursive(self.dialog.content)
                
                # Update the dialog itself
                self.dialog.update()
                
        except Exception as e:
            logging.debug(f"Error in force update: {e}")

    def _update_text_controls_recursive(self, control):
        """Recursively update all text controls within a container."""
        if not control:
            return
            
        try:
            # Update if it's a text control
            if isinstance(control, ft.Text):
                control.update()
            elif isinstance(control, ft.Icon):
                control.update()
            elif isinstance(control, ft.Button):
                control.update()
            elif isinstance(control, ft.ElevatedButton):
                control.update()
            elif isinstance(control, ft.OutlinedButton):
                control.update()
            elif isinstance(control, ft.TextButton):
                control.update()
            elif isinstance(control, ft.Switch):
                control.update()
            elif isinstance(control, ft.Dropdown):
                control.update()
            
            # Recursively update child controls
            if hasattr(control, 'controls') and control.controls:
                for child in control.controls:
                    self._update_text_controls_recursive(child)
            elif hasattr(control, 'content') and control.content:
                self._update_text_controls_recursive(control.content)
                
        except Exception as e:
            logging.debug(f"Error updating control {type(control)}: {e}")

    def _update_app_info_section_theme(self):
        """Update app info section with current theme colors."""
        if not self.dialog or not hasattr(self.dialog, 'content'):
            return
            
        try:
            # Find the app info section in the dialog content
            if hasattr(self.dialog.content, 'content') and isinstance(self.dialog.content.content, ft.Column):
                rows = self.dialog.content.content.controls
                # App info section is typically the second-to-last control before action buttons
                for row in rows:
                    if isinstance(row, ft.Container) and hasattr(row, 'content'):
                        # This might be the app info section
                        info_color = self.text_color["TEXT"]
                        
                        # Update container background with theme
                        row.bgcolor = ft.Colors.with_opacity(0.05, self.text_color["TEXT"])
                        
                        # Update text colors in the info section
                        if hasattr(row.content, 'controls'):
                            for control in row.content.controls:
                                if isinstance(control, ft.Text):
                                    control.color = info_color
                                elif isinstance(control, ft.Row) and hasattr(control, 'controls'):
                                    for subcontrol in control.controls:
                                        if isinstance(subcontrol, ft.Text):
                                            if "MeteoApp" in str(subcontrol.value):
                                                subcontrol.color = ft.Colors.with_opacity(0.7, info_color)
                                            else:
                                                subcontrol.color = info_color
                        try:
                            row.update()
                        except Exception:
                            pass
                            
        except Exception as e:
            logging.debug(f"Error updating app info section theme: {e}")

    def _update_action_buttons_theme(self):
        """Update quick action buttons with current theme colors."""
        if not self.dialog or not hasattr(self.dialog, 'content'):
            return
            
        try:
            # Find the action buttons row in the dialog content
            if hasattr(self.dialog.content, 'content') and isinstance(self.dialog.content.content, ft.Column):
                rows = self.dialog.content.content.controls
                # Action buttons are typically the last row before dialog actions
                for row in rows:
                    if isinstance(row, ft.Row) and hasattr(row, 'controls'):
                        for control in row.controls:
                            if isinstance(control, (ft.ElevatedButton, ft.OutlinedButton)):
                                # Update button colors based on theme
                                if isinstance(control, ft.ElevatedButton):
                                    if "refresh" in str(control.text).lower():
                                        control.bgcolor = ft.Colors.with_opacity(0.1, self.text_color.get("ACCENT", "#0078d4"))
                                        control.color = self.text_color.get("ACCENT", "#0078d4")
                                    elif "reset" in str(control.text).lower():
                                        control.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.ORANGE)
                                        control.color = ft.Colors.ORANGE_700
                                elif isinstance(control, ft.OutlinedButton):
                                    # About button
                                    control.style = ft.ButtonStyle(
                                        color=self.text_color.get("ACCENT", "#0078d4"),
                                        side=ft.BorderSide(1, self.text_color.get("ACCENT", "#0078d4")),
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    )
                                try:
                                    control.update()
                                except Exception:
                                    pass
                                    
        except Exception as e:
            logging.debug(f"Error updating action buttons theme: {e}")

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
        """Always (re)builds and opens the alert dialog with instant theme application."""
        if not self.page:
            logging.error("Error: Page context not available for SettingsAlertDialog.")
            return
            
        logging.info("Opening settings dialog with instant theme update")
        
        # Build the dialog first
        dialog = self.build()
        
        # Apply immediate theme and language updates
        self.update_ui()
        
        # Ensure the dialog is properly added to the page
        if dialog not in self.page.controls:
            self.page.controls.append(dialog)
        self.page.dialog = dialog
        self.page.dialog.open = True
        
        # Force a complete page update to ensure all theme changes are applied
        self.page.update()
        
        logging.info("Settings dialog opened successfully with current theme")

    def close_dialog(self):
        """Closes the alert dialog."""
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def _create_location_button_instance(self, text_color):
        """Create location button with current state indication and theme awareness."""
        # Get current location state
        using_location = False
        if self.state_manager:
            using_location = self.state_manager.get_state('using_location') or False
        
        # Determine button style based on state and theme
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        if using_location:
            button_text = self._get_translation_local("location_enabled")
            button_icon = ft.Icons.GPS_FIXED
            button_color = ft.Colors.GREEN_700 if not is_dark else ft.Colors.GREEN_400
            button_bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.GREEN)
        else:
            button_text = self._get_translation_local("location_disabled")
            button_icon = ft.Icons.GPS_OFF
            button_color = ft.Colors.GREY_700 if not is_dark else ft.Colors.GREY_400
            button_bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.GREY)
        
        async def on_location_click(e):
            """Handle location button click."""
            try:
                new_state = not using_location
                if self.state_manager:
                    await self.state_manager.set_state('using_location', new_state)
                
                # Call the callback if provided
                if self.handle_location_toggle_callback:
                    # Create a mock event for compatibility
                    mock_event = type('MockEvent', (), {
                        'control': type('MockControl', (), {'value': new_state})()
                    })()
                    await self.handle_location_toggle_callback(mock_event)
                
                # Update the dialog to reflect the new state
                self.update_ui()
                
            except Exception as ex:
                logging.error(f"Error toggling location: {ex}")
        
        return ft.ElevatedButton(
            text=button_text,
            icon=button_icon,
            on_click=on_location_click,
            bgcolor=button_bgcolor,
            color=button_color,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                overlay_color=ft.Colors.with_opacity(0.1, button_color)
            ),
            width=140,
            height=36
        )

    def _create_theme_toggle_instance(self):
        """Create theme toggle switch with improved state management."""
        # Get current theme state - check page first, then state manager
        theme_value = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            theme_value = self.page.theme_mode == ft.ThemeMode.DARK
        elif self.state_manager:
            theme_mode = self.state_manager.get_state('theme_mode')
            if theme_mode is not None:
                theme_value = theme_mode == 'dark'

        async def on_theme_toggle(e):
            # Log the theme toggle action
            logging.info(f"Theme toggle clicked - current value: {e.control.value}")
            
            # Update the switch appearance immediately for instant feedback
            if self.theme_toggle_control:
                current_theme_colors = self.theme_handler.get_text_color() if self.theme_handler else {"ACCENT": "#3b82f6"}
                if isinstance(current_theme_colors, str):
                    current_theme_colors = {"ACCENT": "#3b82f6"}
                self.theme_toggle_control.active_color = current_theme_colors.get("ACCENT", "#3b82f6")
                try:
                    self.theme_toggle_control.update()
                except Exception:
                    pass
            
            # Use the same pattern as weather_alert_dialog for consistency
            if self.handle_theme_toggle_callback:
                # Call the callback which should handle both state and page theme updates
                if hasattr(self.page, 'run_task'):
                    self.page.run_task(self.handle_theme_toggle_callback, e)
                else:
                    await self.handle_theme_toggle_callback(e)

        if self.theme_toggle_control is None:
            # Get current theme colors for initial styling
            current_theme_colors = self.theme_handler.get_text_color() if self.theme_handler else {"ACCENT": "#3b82f6"}
            if isinstance(current_theme_colors, str):
                current_theme_colors = {"ACCENT": "#3b82f6"}
            
            self.theme_toggle_control = ft.Switch(
                value=theme_value,
                on_change=on_theme_toggle,
                active_color=current_theme_colors.get("ACCENT", "#3b82f6"),
                active_track_color=ft.Colors.with_opacity(0.5, current_theme_colors.get("ACCENT", "#3b82f6")),
                inactive_thumb_color="#cccccc" if not theme_value else "#666666",
                inactive_track_color="#eeeeee" if not theme_value else "#333333",
            )
        else:
            # Update existing switch
            self.theme_toggle_control.value = theme_value
            current_theme_colors = self.theme_handler.get_text_color() if self.theme_handler else {"ACCENT": "#3b82f6"}
            if isinstance(current_theme_colors, str):
                current_theme_colors = {"ACCENT": "#3b82f6"}
            self.theme_toggle_control.active_color = current_theme_colors.get("ACCENT", "#3b82f6")
            self.theme_toggle_control.active_track_color = ft.Colors.with_opacity(0.5, current_theme_colors.get("ACCENT", "#3b82f6"))
            self.theme_toggle_control.inactive_thumb_color = "#cccccc" if not theme_value else "#666666"
            self.theme_toggle_control.inactive_track_color = "#eeeeee" if not theme_value else "#333333"
            
        return self.theme_toggle_control

    def _build_app_info_section(self, text_color):
        """Build app information section."""
        try:
            current_city = self.state_manager.get_state('city') if self.state_manager else "Unknown"
            current_language = self.state_manager.get_state('language') if self.state_manager else "en"
            current_unit = self.state_manager.get_state('unit') if self.state_manager else "metric"
            
            info_color = text_color["TEXT"]
            accent_color = text_color.get("ACCENT", "#0078d4")
            
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            self._get_translation_local("app_status"),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=info_color
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.LOCATION_CITY, size=14, color="#f59e0b"),
                                ft.Text(f"{self._get_translation_local('current_city')}: {current_city}", size=12, color=info_color),
                            ],
                            spacing=5
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.LANGUAGE, size=14, color="#ff6b35"),
                                ft.Text(f"{self._get_translation_local('active_language')}: {current_language.upper()}", size=12, color=info_color),
                            ],
                            spacing=5
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.STRAIGHTEN, size=14, color="#22c55e"),
                                ft.Text(f"{self._get_translation_local('unit_system')}: {current_unit.title()}", size=12, color=info_color),
                            ],
                            spacing=5
                        ),
                        # App version info
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.INFO, size=14, color=accent_color),
                                ft.Text("MeteoApp v1.0.0", size=10, color=ft.Colors.with_opacity(0.7, info_color)),
                            ],
                            spacing=5
                        ),
                    ],
                    spacing=5
                ),
                padding=ft.padding.all(8),
                bgcolor=ft.Colors.with_opacity(0.05, text_color["TEXT"]),
                border_radius=8,
            )
        except Exception as e:
            logging.warning(f"Error building app info section: {e}")
            return ft.Container(
                content=ft.Text(
                    self._get_translation_local("app_info_unavailable"),
                    size=12,
                    color=ft.Colors.with_opacity(0.6, text_color["TEXT"])
                ),
                padding=8
            )

    def _get_translation_local(self, key):
        """Get translation using the standard translation service."""
        try:
            return self._get_translation(key, "settings_alert_dialog_items")
        except Exception as e:
            logging.warning(f"Translation error for key '{key}': {e}")
            return key

    def _reset_settings(self, e):
        """Reset all settings to defaults with confirmation."""
        try:
            # Create confirmation dialog
            def confirm_reset(e):
                confirmation_dialog.open = False
                self.page.update()
                
                # Perform the reset
                if self.state_manager:
                    from utils.config import DEFAULT_CITY, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
                    
                    async def do_reset():
                        await self.state_manager.update_state({
                            "city": DEFAULT_CITY,
                            "language": DEFAULT_LANGUAGE,
                            "unit": DEFAULT_UNIT_SYSTEM,
                            "using_location": False
                        })
                    
                    if hasattr(self.page, 'run_task'):
                        self.page.run_task(do_reset)
                    
                    # Show confirmation
                    self.page.show_snack_bar(
                        ft.SnackBar(
                            content=ft.Text(self._get_translation_local("settings_reset")),
                            duration=3000
                        )
                    )
                    
                    # Update the dialog content
                    self.update_ui()

            def cancel_reset(e):
                confirmation_dialog.open = False
                self.page.update()

            confirmation_dialog = ft.AlertDialog(
                title=ft.Text(self._get_translation_local("reset_confirmation")),
                content=ft.Text(self._get_translation_local("confirm_reset")),
                actions=[
                    ft.TextButton(
                        self._get_translation_local("cancel"),
                        on_click=cancel_reset
                    ),
                    ft.ElevatedButton(
                        self._get_translation_local("confirm"),
                        on_click=confirm_reset,
                        bgcolor=ft.Colors.ORANGE,
                        color=ft.Colors.WHITE
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            
            self.page.dialog = confirmation_dialog
            confirmation_dialog.open = True
            self.page.update()
            
        except Exception as ex:
            logging.error(f"Error resetting settings: {ex}")

    def _refresh_weather_data(self, e):
        """Refresh weather data."""
        try:
            main_app = self.page.session.get('main_app') if self.page else None
            if main_app and self.state_manager:
                city = self.state_manager.get_state('city')
                language = self.state_manager.get_state('language')
                unit = self.state_manager.get_state('unit')
                
                if city and language and unit:
                    if hasattr(self.page, 'run_task'):
                        self.page.run_task(main_app.update_weather_with_sidebar, city, language, unit)
                    
                    # Show temporary feedback
                    self.page.show_snack_bar(
                        ft.SnackBar(
                            content=ft.Text(self._get_translation_local("refreshing_data")),
                            duration=2000
                        )
                    )
        except Exception as ex:
            logging.error(f"Error refreshing weather data: {ex}")

    def _show_about_dialog(self, e):
        """Show application information dialog."""
        try:
            def close_about(e):
                about_dialog.open = False
                self.page.update()

            about_content = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.WB_SUNNY, size=32, color="#f59e0b"),
                            ft.Text("MeteoApp", size=24, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    ft.Divider(),
                    ft.Text(
                        self._get_translation_local("about_description"),
                        size=14,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(),
                    ft.Text(f"{self._get_translation_local('version')}: 1.0.0", size=12),
                    ft.Text(f"{self._get_translation_local('developer')}: F3rren", size=12),
                    ft.Divider(),
                    ft.Text(
                        self._get_translation_local("features"),
                        size=14,
                        weight=ft.FontWeight.W_600
                    ),
                    ft.Text(
                        self._get_translation_local("feature_list"),
                        size=12
                    ),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            about_dialog = ft.AlertDialog(
                title=ft.Text(self._get_translation_local("about_title")),
                content=ft.Container(
                    content=about_content,
                    width=400,
                    height=350,
                ),
                actions=[
                    ft.TextButton(
                        self._get_translation("close", "settings_alert_dialog_items"),
                        on_click=close_about
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER
            )
            
            self.page.dialog = about_dialog
            about_dialog.open = True
            self.page.update()
            
        except Exception as ex:
            logging.error(f"Error showing about dialog: {ex}")

    def cleanup(self):
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
            self.state_manager.unregister_observer("theme_event", self.update_ui)
