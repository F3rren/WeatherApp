import flet as ft

from layout.backend.api_operation import APIOperation
from layout.frontend.informationtab.air_condition import AirConditionInfo
from layout.frontend.informationtab.daily_forecast import DailyForecast
from layout.frontend.informationtab.main_information import MainWeatherInfo

class WeeklyWeather:

    def __init__(self, page, city, language, unit):
        #self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",
        self.gradient = (
            ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.BLUE, ft.Colors.YELLOW],
            )
            if page.theme_mode == ft.ThemeMode.LIGHT else
            ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
                    ft.Colors.GREY_900,
                ],
            )
        )
        
        self.page = page
        self.language = language
        self.unit = unit
        self.city = city
        self.mainInformation = MainWeatherInfo(page, city, language, unit)
        self.dailyForecast = DailyForecast(page, city, language, unit)
        self.airCondition = AirConditionInfo(page, city, language, unit)
        self.api = APIOperation(page, city, language, unit)

    def update_city(self, new_city):
        self.city = new_city
        self.mainInformation.update_city(new_city)
        self.dailyForecast.update_city(new_city)
        self.airCondition.update_city(new_city)
        self.api.update_data(new_city, self.language, self.unit)
        
    def update_by_coordinates(self, lat, lon):
        """Aggiorna le informazioni meteo usando le coordinate geografiche"""
        self.api.update_coordinates(lat, lon, self.language, self.unit)
        self.city = self.api.city  # Aggiorna il nome della città dal geocoding inverso
        self.mainInformation.update_by_coordinates(lat, lon)
        self.dailyForecast.update_by_coordinates(lat, lon)
        self.airCondition.update_by_coordinates(lat, lon)

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
            #bgcolor=self.bgcolor,
            gradient=self.gradient,
            border_radius=15,
            padding=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.createWeeklyForecast()]
                ),
        )
