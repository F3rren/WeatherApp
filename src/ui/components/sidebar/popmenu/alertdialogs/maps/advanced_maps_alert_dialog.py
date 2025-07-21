"""
Advanced Maps Alert Dialog for MeteoApp.
Simple dialog for advanced weather maps functionality.
"""

import flet as ft
import webbrowser


class AdvancedMapsAlertDialog:
    """Simple alert dialog for advanced weather maps."""
    
    def __init__(self, page: ft.Page = None, state_manager=None, language: str = "it", theme_handler=None):
        self.page = page
        self.state_manager = state_manager
        self.language = language
        self.theme_handler = theme_handler
        self.dialog = None
        
        # Register for theme and language updates if state_manager is available
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)

    def update_ui(self, event_data=None):
        """Update UI when theme or language changes."""
        if event_data:
            if 'language' in event_data:
                self.language = event_data['language']
            
        # If dialog is currently open, refresh it
        if self.dialog and hasattr(self.page, 'dialog') and self.page.dialog and self.page.dialog.open:
            self.open_dialog()

    def open_dialog(self):
        """Open the advanced maps dialog following the same pattern as SettingsAlertDialog."""
        if not self.page:
            print("ERROR: Page context not available for AdvancedMapsAlertDialog")
            return
        
        try:
            # Build the dialog first (like SettingsAlertDialog)
            dialog = self._create_dialog()
            
            # Ensure the dialog is properly added to the page (like SettingsAlertDialog)
            if dialog not in self.page.controls:
                self.page.controls.append(dialog)
            
            # Set the page dialog and open it (like SettingsAlertDialog)
            self.page.dialog = dialog
            self.page.dialog.open = True
            
            # Force a complete page update (like SettingsAlertDialog)
            self.page.update()
            
        except Exception as e:
            print(f"ERROR: Exception in open_dialog: {e}")
            import traceback
            traceback.print_exc()

    def show_dialog(self):
        """Alias for open_dialog to maintain compatibility."""
        return self.open_dialog()

    def _create_dialog(self) -> ft.AlertDialog:
        """Create the advanced maps alert dialog with theme and language support."""
        # Get theme colors following the same pattern as SettingsAlertDialog
        theme_colors = self.theme_handler.get_text_color() if self.theme_handler else {"TEXT": "#000000"}
        if isinstance(theme_colors, str):
            theme_colors = {"TEXT": theme_colors, "DIALOG_BACKGROUND": "#fff", "ACCENT": "#0078d4"}
        
        # Support dark mode for dialog background
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        dialog_bg = "#161b22" if is_dark else "#ffffff"
        text_color = theme_colors["TEXT"]
        accent_color = theme_colors.get("ACCENT", "#0078d4")
        
        # Define texts based on language
        texts = self._get_texts()
        
        content = ft.Container(
            content=ft.Column([
                ft.Text(
                    f"🗺️ {texts['title']}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=text_color
                ),
                ft.Divider(color=ft.Colors.with_opacity(0.3, text_color)),
                ft.Text(
                    texts['description'],
                    size=14,
                    color=text_color
                ),
                ft.Container(height=10),
                ft.Column([
                    ft.ElevatedButton(
                        f"🌀 {texts['windy']}",
                        on_click=lambda _: self._open_windy(),
                        bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                        color=accent_color,
                        width=300,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    ft.ElevatedButton(
                        f"🗺️ {texts['openweather']}", 
                        on_click=lambda _: self._open_openweather(),
                        bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                        color=accent_color,
                        width=300,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    ft.ElevatedButton(
                        f"⛈️ {texts['meteoblue']}",
                        on_click=lambda _: self._open_meteoblue(),
                        bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                        color=accent_color,
                        width=300,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    ft.ElevatedButton(
                        f"🌍 {texts['earth']}",
                        on_click=lambda _: self._open_earth(),
                        bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                        color=accent_color,
                        width=300,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    )
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            width=400,
            height=350,
            bgcolor=dialog_bg
        )
        
        return ft.AlertDialog(
            modal=False,  # Allow clicking outside to close
            scrollable=True,  # Make dialog scrollable
            title=ft.Row([
                ft.Icon(ft.Icons.LAYERS_OUTLINED, color=accent_color, size=24),
                ft.Text(texts['dialog_title'], weight=ft.FontWeight.BOLD, color=text_color)
            ], spacing=10),
            content=content,
            actions=[
                ft.TextButton(texts['close'], on_click=self._close_dialog, style=ft.ButtonStyle(color=accent_color))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=dialog_bg,
            title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=text_color),
            content_text_style=ft.TextStyle(size=14, color=text_color),
            inset_padding=ft.padding.all(20)
        )

    def _get_texts(self):
        """Get localized texts based on current language."""
        if self.language == "en":
            return {
                "title": "Advanced Weather Maps",
                "dialog_title": "Advanced Maps",
                "description": "Access advanced weather maps from different providers:",
                "windy": "Windy - Interactive Maps",
                "openweather": "OpenWeatherMap",
                "meteoblue": "MeteoBlue",
                "earth": "Earth Nullschool",
                "close": "Close"
            }
        else:  # Italian (default)
            return {
                "title": "Mappe Meteo Avanzate",
                "dialog_title": "Mappe Avanzate", 
                "description": "Accedi a mappe meteo avanzate con diversi fornitori:",
                "windy": "Windy - Mappe Interactive",
                "openweather": "OpenWeatherMap",
                "meteoblue": "MeteoBlue", 
                "earth": "Earth Nullschool",
                "close": "Chiudi"
            }

    def _open_windy(self):
        """Open Windy weather map."""
        webbrowser.open("https://www.windy.com/?temp,45.4642,9.1900,10")
        
    def _open_openweather(self):
        """Open OpenWeatherMap."""
        webbrowser.open("https://openweathermap.org/weathermap")
        
    def _open_meteoblue(self):
        """Open MeteoBlue weather maps."""
        webbrowser.open("https://www.meteoblue.com/it/tempo/mappe/como_italia_3176885")
        
    def _open_earth(self):
        """Open Earth Nullschool wind map."""
        webbrowser.open("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-347.73,46.87,3000")

    def _close_dialog(self, e):
        """Close the dialog following SettingsAlertDialog pattern."""
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def cleanup(self):
        """Cleanup method to unregister observers."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
            self.state_manager.unregister_observer("theme_event", self.update_ui)
