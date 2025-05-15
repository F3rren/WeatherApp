import flet as ft

from layout.BackEnd.APIOperation import APIOperation

SIZE_TEXT = 18

class WeeklyWeather:

    def __init__(self, page, city, language, unit):
        self.city = city
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",
        self.api = APIOperation(page, city, language, unit)

    def createWeeklyForecast(self):
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.api.getWeeklyForecast()
                    ]
                ),
            expand=True
            )

    def build(self):
        return ft.Container(
            bgcolor=self.bgcolor,
            border_radius=15,
            padding=20,
            margin=ft.Margin(10, 80, 10, 10),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.createWeeklyForecast()]
                ),
            expand=True
        )
