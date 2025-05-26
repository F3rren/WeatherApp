import flet as ft

class AirConditionInfo:
    """
    Air condition information display.
    """
    
    def __init__(self, feels_like: int, humidity: int, wind_speed: int, 
                 pressure: int, text_color: str):
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.pressure = pressure
        self.text_color = text_color
    
    def build(self) -> ft.Column:
        """Build the air condition information"""
        return ft.Column(
            controls=[
                ft.Text("Condizioni Atmosferiche", size=20, weight="bold"),
                ft.Divider(height=1, color=self.text_color),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Percepita", size=16),
                                ft.Text(f"{self.feels_like}°", size=20, weight="bold"),
                                ft.Text("Umidità", size=16),
                                ft.Text(f"{self.humidity}%", size=20, weight="bold"),
                            ],
                            expand=True,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Vento", size=16),
                                ft.Text(f"{self.wind_speed} km/h", size=20, weight="bold"),
                                ft.Text("Pressione", size=16),
                                ft.Text(f"{self.pressure} hPa", size=20, weight="bold"),
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
