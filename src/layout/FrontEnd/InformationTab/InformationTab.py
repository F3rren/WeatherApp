import flet as ft

from layout.FrontEnd.InformationTab.DailyForecast import DailyForecast
from layout.FrontEnd.InformationTab.MainInformation import MainInformation
from layout.FrontEnd.InformationTab.AirCondition import AirCondition


class InformationTab:

    def __init__(self, page, city, language, unit):
        self.page = page
        self.language = language
        self.unit = unit
        self.city = city
        self.mainInformation = MainInformation(page, city, language, unit)
        self.dailyForecast = DailyForecast(page, city, language, unit)
        self.airCondition = AirCondition(page, city, language, unit)

    def update_city(self, new_city):
        self.city = new_city
        self.mainInformation.update_city(new_city)
        self.dailyForecast.update_city(new_city)
        self.airCondition.update_city(new_city)

    def build(self):  
        return ft.Container(
            padding=10,
            content=ft.Column([
                self.mainInformation.build(),
                self.dailyForecast.build(),
                self.airCondition.build(),
            ])
        )

