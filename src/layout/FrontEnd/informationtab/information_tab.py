import flet as ft

from layout.frontend.informationtab.daily_forecast import DailyForecast
from layout.frontend.informationtab.main_information import MainWeatherInfo
from layout.frontend.informationtab.air_condition import AirConditionInfo


class InformationTab:

    def __init__(self, page, city, language, unit):
        self.page = page
        self.language = language
        self.unit = unit
        self.city = city
        self.mainInformation = MainWeatherInfo(page, city, language, unit)
        self.dailyForecast = DailyForecast(page, city, language, unit)
        self.airCondition = AirConditionInfo(page, city, language, unit)
        self.location_indicator = ft.Text("", size=14, italic=True, color=ft.Colors.GREEN_400)

    def update_city(self, new_city):
        self.city = new_city
        self.mainInformation.update_city(new_city)
        self.dailyForecast.update_city(new_city)
        self.airCondition.update_city(new_city)
        self.location_indicator.value = ""
        self.page.update()
        
    def update_by_coordinates(self, lat, lon):
        """Aggiorna le informazioni meteo usando le coordinate geografiche"""
        self.mainInformation.update_by_coordinates(lat, lon)
        self.dailyForecast.update_by_coordinates(lat, lon)
        self.airCondition.update_by_coordinates(lat, lon)
        self.location_indicator.value = "📍 Posizione attuale"
        self.page.update()

    def build(self):  
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    self.mainInformation.build(),
                    self.location_indicator
                ]),
                self.dailyForecast.build(),
                self.airCondition.build(),
            ])
        )
