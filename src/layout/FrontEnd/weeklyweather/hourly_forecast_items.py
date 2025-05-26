import flet as ft

class HourlyForecastItems:
    """
    An item displaying hourly forecast information.
    """
    
    def __init__(self, time: str, icon_code: str, temperature: int):
        self.time = time
        self.icon_code = icon_code
        self.temperature = temperature
    
    def build(self) -> ft.Column:
        """Build the hourly forecast item"""
        return ft.Column(
            controls=[
                ft.Text(self.time, size=20, weight=ft.FontWeight.BOLD),
                ft.Image(
                    src=f"https://openweathermap.org/img/wn/{self.icon_code}@2x.png",
                    width=100,
                    height=100,
                ),
                ft.Text(f"{self.temperature}°", size=20, weight=ft.FontWeight.BOLD)
            ],
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
