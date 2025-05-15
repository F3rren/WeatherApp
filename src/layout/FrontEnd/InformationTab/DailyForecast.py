import flet as ft
from layout.BackEnd.APIOperation import APIOperation

class DailyForecast:

    def __init__(self, page, city="Milano"):
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",
        self.city = city
        self.api = APIOperation(page)

    def createHourlyForecast(self):
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.api.getDailyForecast(self.city)]
                ),
            expand=True
            )

    def build(self, page):
        return ft.Container(
            bgcolor=self.bgcolor,
            border_radius=15,
            padding=20,
            content=self.createHourlyForecast(),
        )
