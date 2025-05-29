import flet as ft
from config import LIGHT_THEME, DARK_THEME # Ensure these are imported

class MainWeatherInfo:
    """
    Main weather information display.
    """
    
    def __init__(self, city: str, location: str, temperature: int, 
                 weather_icon: str, text_color: str, page: ft.Page = None): # Added page for state_manager access
        self.city = city
        self.location = location
        self.temperature = temperature
        self.weather_icon = weather_icon
        self.text_color = text_color
        self.page = page # Store page to access state_manager if needed for observing theme

        # Text controls that need dynamic color updates
        self.city_text = ft.Text(self.city.upper(), size=40, weight="bold", color=self.text_color)
        self.location_text = ft.Text(self.location, size=20, color=self.text_color)
        self.temperature_text = ft.Text(f"{self.temperature}°", size=60, weight="bold", color=self.text_color)
        
        # Register for theme change events if page and state_manager are available
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
            
            # Update text colors of the controls
            if hasattr(self, 'city_text'): # Check if attribute exists
                self.city_text.color = self.text_color
                if self.city_text.page:
                    self.city_text.update()
            if hasattr(self, 'location_text'):
                self.location_text.color = self.text_color
                if self.location_text.page:
                    self.location_text.update()
            if hasattr(self, 'temperature_text'):
                self.temperature_text.color = self.text_color
                if self.temperature_text.page:
                    self.temperature_text.update()

    def build(self) -> ft.Container:
        """Build the main weather information"""
        return ft.Container(
            content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self.city_text,
                        self.location_text,
                        self.temperature_text,
                    ],
                    expand=True, 
                ),
                ft.Column(
                    controls=[
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{self.weather_icon}@4x.png",
                            width=150,
                            height=150,
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    expand=True 
                )
            ],
            expand=True,
        ),
        padding=20
    )