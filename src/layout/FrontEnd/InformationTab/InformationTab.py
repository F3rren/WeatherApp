import flet as ft

from layout.FrontEnd.InformationTab.AirCondition import AirCondition
from layout.FrontEnd.InformationTab.DailyForecast import DailyForecast
from layout.FrontEnd.InformationTab.MainInformation import MainInformation


class InformationTab:

    def __init__(self, page, city, language, unit):
        self.page = page
        self.mainInformation = MainInformation(page, city, language, unit)
        self.dailyForecast = DailyForecast(page, city, language, unit)
        self.airCondition = AirCondition(page, city, language, unit)

    def createInformationPage(self):
        return ft.Column(
            controls = [
                ft.Container(content=self.mainInformation.build()),
                ft.Container(content=self.dailyForecast.build()),
                ft.Container(content=self.airCondition.build()),
            ]
        )
        

    def build(self):  
        return ft.Container(
            content=self.createInformationPage()
        )
