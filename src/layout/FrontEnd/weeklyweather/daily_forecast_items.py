import flet as ft

class DailyForecastItems:
    """
    An item displaying daily forecast information.
    """
    
    def __init__(self, day: str, icon_code: str, description: str, 
                 temp_min: int, temp_max: int, text_color: str):
        self.day = day
        self.icon_code = icon_code
        self.description = description
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.text_color = text_color
    
    def build(self) -> ft.Row:
        """Build the daily forecast item"""
        return ft.Row(
            controls=[
                ft.Text(
                    self.day, 
                    size=20, 
                    color=self.text_color, 
                    weight="bold", 
                    width=100,
                    text_align=ft.TextAlign.START
                ),
                ft.Container(
                    content=ft.Image(
                        src=f"https://openweathermap.org/img/wn/{self.icon_code}@4x.png",
                        width=80,
                        height=80,
                    ),
                    expand=True,
                    alignment=ft.alignment.center
                ),
                ft.Text(
                    self.description.upper(), 
                    size=20, 
                    color=self.text_color, 
                    weight="bold", 
                    text_align=ft.TextAlign.START
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            f"{self.temp_min}°",
                            ft.TextStyle(
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE,
                            )
                        ),
                        ft.TextSpan(" / ",
                            ft.TextStyle(
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            )),
                        ft.TextSpan(
                            f"{self.temp_max}°",
                            ft.TextStyle(
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.RED,
                            )
                        ),
                    ],
                    expand=True,
                    text_align=ft.TextAlign.END
                )
            ],
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
