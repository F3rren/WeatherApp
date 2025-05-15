import flet as ft

from layout.FrontEnd.InformationTab.AirCondition import AirCondition
from layout.FrontEnd.InformationTab.DailyForecast import DailyForecast
from layout.FrontEnd.InformationTab.MainInformation import MainInformation
from layout.FrontEnd.InformationTab.Searchbar import Searchbar

class InformationTab:

    def __init__(self, page):
        self.page = page
        self.searchbar = Searchbar()
        self.mainInformation = MainInformation(page)
        self.dailyForecast = DailyForecast(page)
        self.airCondition = AirCondition(page)

    def createInformationPage(self):
        return ft.Column(
            controls = [
                ft.Container(content=self.searchbar.build()),
                ft.Container(content=self.mainInformation.build()),
                ft.Container(content=self.dailyForecast.build()),
                ft.Container(content=self.airCondition.build()),
            ],
            expand=True
        )
        

    def build(self):  
        return ft.Container(
            content=self.createInformationPage()
        )
