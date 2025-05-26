import flet as ft

class MainWeatherInfo:
    """
    Main weather information display.
    """
    
    def __init__(self, city: str, location: str, temperature: int, 
                 weather_icon: str, text_color: str):
        self.city = city
        self.location = location
        self.temperature = temperature
        self.weather_icon = weather_icon
        self.text_color = text_color
    
    def build(self) -> ft.Row:
        """Build the main weather information"""
        return ft.Container(
            content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(self.city.upper(), size=40, weight="bold"),
                        ft.Text(self.location, size=20),
                        ft.Text(f"{self.temperature}°", size=60, weight="bold"),
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