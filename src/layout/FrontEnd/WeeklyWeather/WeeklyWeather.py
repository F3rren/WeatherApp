import flet as ft

from layout.BackEnd.APIOperation import APIOperation
from layout.FrontEnd.InformationTab.AirCondition import AirCondition
from layout.FrontEnd.InformationTab.DailyForecast import DailyForecast
from layout.FrontEnd.InformationTab.MainInformation import MainInformation

SIZE_TEXT = 18

class WeeklyWeather:

    def __init__(self, page, city, language, unit):
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",
        self.page = page
        self.language = language
        self.unit = unit
        self.city = city
        self.mainInformation = MainInformation(page, city, language, unit)
        self.dailyForecast = DailyForecast(page, city, language, unit)
        self.airCondition = AirCondition(page, city, language, unit)
        self.api = APIOperation(page, city, language, unit)

    def update_city(self, new_city):
        self.city = new_city
        self.mainInformation.update_city(new_city)
        self.dailyForecast.update_city(new_city)
        self.airCondition.update_city(new_city)


    def createWeeklyForecast(self):
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.api.getWeeklyForecast()
                    ]
                )
            )

    def build(self):
        return ft.Container(
            bgcolor=self.bgcolor,
            border_radius=15,
            padding=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.createWeeklyForecast()]
                ),
        )
