import flet as ft
from config import LIGHT_THEME, DARK_THEME

class AirConditionInfo:
    """
    Air condition information display.
    """
    
    def __init__(self, feels_like: int, humidity: int, wind_speed: int, 
                 pressure: int, text_color: str, page: ft.Page = None): # Added page
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.pressure = pressure
        self.text_color = text_color
        self.page = page # Store page

        # Store text controls that need dynamic color updates
        self.title_text = ft.Text("Condizioni Atmosferiche", size=20, weight="bold", color=self.text_color)
        self.divider = ft.Divider(height=1, color=self.text_color)

        self.feels_like_label = ft.Text("Percepita", size=16, color=self.text_color)
        self.feels_like_value = ft.Text(f"{self.feels_like}°", size=20, weight="bold", color=self.text_color)
        self.humidity_label = ft.Text("Umidità", size=16, color=self.text_color)
        self.humidity_value = ft.Text(f"{self.humidity}%", size=20, weight="bold", color=self.text_color)
        
        self.wind_label = ft.Text("Vento", size=16, color=self.text_color)
        self.wind_value = ft.Text(f"{self.wind_speed} km/h", size=20, weight="bold", color=self.text_color)
        self.pressure_label = ft.Text("Pressione", size=16, color=self.text_color)
        self.pressure_value = ft.Text(f"{self.pressure} hPa", size=20, weight="bold", color=self.text_color)

        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                state_manager.register_observer("theme_event", self.handle_theme_change)

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text and divider colors."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]

            # Update colors of all relevant controls
            controls_to_update = [
                self.title_text, self.feels_like_label, self.feels_like_value,
                self.humidity_label, self.humidity_value, self.wind_label,
                self.wind_value, self.pressure_label, self.pressure_value
            ]
            for control in controls_to_update:
                if hasattr(control, 'color'):
                    control.color = self.text_color
                if control.page:
                    control.update()
            
            if hasattr(self.divider, 'color'): # Divider color
                self.divider.color = self.text_color
                if self.divider.page:
                    self.divider.update()

    def build(self) -> ft.Column:
        """Build the air condition information"""
        return ft.Column(
            controls=[
                self.title_text,
                self.divider,
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                self.feels_like_label,
                                self.feels_like_value,
                                self.humidity_label,
                                self.humidity_value,
                            ],
                            expand=True,
                        ),
                        ft.Column(
                            controls=[
                                self.wind_label,
                                self.wind_value,
                                self.pressure_label,
                                self.pressure_value,
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
