import flet as ft
from config import LIGHT_THEME, DARK_THEME

class HourlyForecastItems:
    """
    An item displaying hourly forecast information.
    """
    
    def __init__(self, time: str, icon_code: str, temperature: int, text_color: str, page: ft.Page = None):
        self.time = time
        self.icon_code = icon_code
        self.temperature = temperature
        self.text_color = text_color
        self.page = page

        self.time_text = ft.Text(self.time, size=20, weight=ft.FontWeight.BOLD, color=self.text_color)
        self.temp_text = ft.Text(f"{self.temperature}°", size=20, weight=ft.FontWeight.BOLD, color=self.text_color)

        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                state_manager.register_observer("theme_event", self.handle_theme_change)
    
    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color."""
        if self.page: # Ensure page context is available
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]
            
            if hasattr(self, 'time_text'):
                self.time_text.color = self.text_color
                if self.time_text.page:
                    self.time_text.update()
            
            if hasattr(self, 'temp_text'):
                self.temp_text.color = self.text_color
                if self.temp_text.page:
                    self.temp_text.update()

    def build(self) -> ft.Container:
        """Build the hourly forecast item"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.time_text,
                    ft.Image(
                        src=f"https://openweathermap.org/img/wn/{self.icon_code}@2x.png",
                        width=100,  # Restored image size
                        height=100, # Restored image size
                    ),
                    self.temp_text
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True  # Inner column expands to fill this container
            ),
            expand=True, # Crucial: Allow this container to expand within the parent Row
            alignment=ft.alignment.center, # Aligns the Column within this Container
            padding=10, # Restored padding
            border_radius=10
        )
