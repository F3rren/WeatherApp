import flet as ft

from layout.FrontEnd.InformationTab.AirCondition import AirCondition
from layout.FrontEnd.InformationTab.DailyForecast import DailyForecast
from layout.FrontEnd.InformationTab.MainInformation import MainInformation
from layout.FrontEnd.InformationTab.Searchbar import Searchbar

class InformationTab:

    def __init__(self, page):
        self.page = page
        self.searchbar = Searchbar()
        self.mainInformation = MainInformation()
        self.dailyForecast = DailyForecast(page)
        self.airCondition = AirCondition(page)

    def createInformationPage(self):
        controls = [
            ft.Container(content=self.searchbar.build()),
            ft.Container(content=self.mainInformation.build()),
            ft.Container(content=self.dailyForecast.build(self.page)),
            ft.Container(content=self.airCondition.build()),
        ]
        return ft.Column(controls=controls, expand=True)

    def build(self):  
        return ft.Container(
            content=self.createInformationPage()
        )
