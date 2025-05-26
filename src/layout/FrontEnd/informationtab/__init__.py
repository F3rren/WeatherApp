import flet as ft
from layout.frontend.informationtab.air_condition import AirConditionInfo
from layout.frontend.informationtab.daily_forecast import DailyForecast
from layout.frontend.informationtab.main_information import MainWeatherInfo

class InformationTab:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        return ft.Column(
            [
                AirConditionInfo(),
                DailyForecast(),
                MainWeatherInfo(),
            ]
        )