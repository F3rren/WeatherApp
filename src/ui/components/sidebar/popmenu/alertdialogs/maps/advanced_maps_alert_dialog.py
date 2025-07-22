"""
Advanced Maps Alert Dialog for MeteoApp.
Simple dialog for advanced weather maps functionality.
"""

import flet as ft
import webbrowser


class AdvancedMapsAlertDialog:
    """Dialog semplificato per le mappe meteo avanzate."""
    
    def __init__(self, page: ft.Page = None, state_manager=None, language: str = "it", theme_handler=None):
        self.page = page
        self.state_manager = state_manager
        self.language = language
        self.theme_handler = theme_handler
        self.dialog = None
        self.colors = self.update_theme_colors()
        
        # Register for theme and language updates if state_manager is available
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)

    def update_theme_colors(self):
        """Update and return theme colors based on current theme."""
        is_dark = (hasattr(self.page, 'theme_mode') and 
                  self.page.theme_mode == ft.ThemeMode.DARK)
        
        if is_dark:
            return {
                "bg": "#161b22", "surface": "#21262d", "text": "#f0f6fc",
                "text_secondary": "#8b949e", "accent": "#58a6ff", "border": "#30363d"
            }
        else:
            return {
                "bg": "#ffffff", "surface": "#f6f8fa", "text": "#24292f",
                "text_secondary": "#656d76", "accent": "#0969da", "border": "#d1d9e0"
            }

    def update_ui(self, event_data=None):
        """Update UI when theme or language changes."""
        if event_data and 'language' in event_data:
            self.language = event_data['language']
        
        self.colors = self.update_theme_colors()
        
        # If dialog is currently open, refresh it
        if self.dialog and hasattr(self.page, 'dialog') and self.page.dialog and self.page.dialog.open:
            self.show_dialog()

    def show_dialog(self):
        """Show the advanced maps dialog."""
        if not self.page:
            print("ERROR: Page context not available for AdvancedMapsAlertDialog")
            return
        
        try:
            self.colors = self.update_theme_colors()
            dialog = self.create_dialog()
            
            if dialog not in self.page.controls:
                self.page.controls.append(dialog)
            
            self.page.dialog = dialog
            self.page.dialog.open = True
            self.page.update()
            
        except Exception as e:
            print(f"ERROR: Exception in show_dialog: {e}")

    def create_dialog(self) -> ft.AlertDialog:
        """Create the advanced maps alert dialog."""
        texts = self.get_texts()
        
        content = ft.Container(
            content=ft.Column([
                ft.Text(f"{texts['title']}", size=20, weight=ft.FontWeight.BOLD,
                       text_align=ft.TextAlign.CENTER, color=self.colors["text"]),
                ft.Divider(color=ft.Colors.with_opacity(0.3, self.colors["text"])),
                ft.Text(texts['description'], size=14, color=self.colors["text"]),
                ft.Container(height=10),
                ft.Column([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.AIR, color=ft.Colors.BLUE_400, size=20),
                            ft.Text(f"{texts['windy']}", color=self.colors["accent"], weight=ft.FontWeight.W_500)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        on_click=lambda _: self.open_windy(),
                        bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]), 
                        width=300, 
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.MAP_OUTLINED, color=ft.Colors.GREEN_400, size=20),
                            ft.Text(f"{texts['openweather']}", color=self.colors["accent"], weight=ft.FontWeight.W_500)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        on_click=lambda _: self.open_openweather(),
                        bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]), 
                        width=300, 
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.THUNDERSTORM, color=ft.Colors.PURPLE_400, size=20),
                            ft.Text(f"{texts['meteoblue']}", color=self.colors["accent"], weight=ft.FontWeight.W_500)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        on_click=lambda _: self.open_meteoblue(),
                        bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]), 
                        width=300, 
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PUBLIC, color=ft.Colors.CYAN_400, size=20),
                            ft.Text(f"{texts['earth']}", color=self.colors["accent"], weight=ft.FontWeight.W_500)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        on_click=lambda _: self.open_earth(),
                        bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]), 
                        width=300, 
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    )
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, width=min(400, self.page.width * 0.9), bgcolor=self.colors["bg"]
        )
        
        return ft.AlertDialog(
            modal=False, scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.LAYERS_OUTLINED, color=self.colors["accent"], size=24),
                ft.Text(texts['dialog_title'], weight=ft.FontWeight.BOLD, color=self.colors["text"])
            ], spacing=10),
            content=content,
            actions=[ft.FilledButton(
                icon=ft.Icons.CLOSE, text=texts['close'], on_click=self.close_dialog,
                style=ft.ButtonStyle(bgcolor=self.colors["accent"], color=ft.Colors.WHITE,
                                   shape=ft.RoundedRectangleBorder(radius=8))
            )],
            actions_alignment=ft.MainAxisAlignment.END, bgcolor=self.colors["bg"],
            title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
            content_text_style=ft.TextStyle(size=14, color=self.colors["text"]),
            inset_padding=ft.padding.all(20)
        )

    def get_texts(self):
        """Get localized texts based on current language."""
        if self.language == "en":
            return {
                "title": "Advanced Weather Maps", "dialog_title": "Advanced Maps",
                "description": "Access advanced weather maps from different providers:",
                "windy": "Windy - Interactive Maps", "openweather": "OpenWeatherMap",
                "meteoblue": "MeteoBlue", "earth": "Earth Nullschool", "close": "Close"
            }
        else:  # Italian (default)
            return {
                "title": "Mappe Meteo Avanzate", "dialog_title": "Mappe Avanzate", 
                "description": "Accedi a mappe meteo avanzate con diversi fornitori:",
                "windy": "Windy - Mappe Interactive", "openweather": "OpenWeatherMap",
                "meteoblue": "MeteoBlue", "earth": "Earth Nullschool", "close": "Chiudi"
            }

    def open_windy(self):
        """Open Windy weather map."""
        webbrowser.open("https://www.windy.com/?temp,45.4642,9.1900,10")
        
    def open_openweather(self):
        """Open OpenWeatherMap."""
        webbrowser.open("https://openweathermap.org/weathermap")
        
    def open_meteoblue(self):
        """Open MeteoBlue weather maps."""
        webbrowser.open("https://www.meteoblue.com/it/tempo/mappe/como_italia_3176885")
        
    def open_earth(self):
        """Open Earth Nullschool wind map."""
        webbrowser.open("https://earth.nullschool.net/#current/wind/surface/level/orthographic=-347.73,46.87,3000")

    def close_dialog(self, e=None):
        """Close the dialog."""
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def cleanup(self):
        """Cleanup method to unregister observers."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
            self.state_manager.unregister_observer("theme_event", self.update_ui)
