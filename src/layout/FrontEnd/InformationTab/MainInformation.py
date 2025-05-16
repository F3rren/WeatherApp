import flet as ft
from layout.BackEnd.APIOperation import APIOperation

class MainInformation:
    def __init__(self, page, city, language, unit):
        self.city = city
        self.api = APIOperation(page, city, language, unit)
        self.api.getStateInformation()
    def createMainInformation(self):
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text((self.city).upper(), size=40, weight="bold"),
                        #ft.Text(self.api.getCityLocation(), size=20),
                        ft.Text(f"{self.api.getTemperatureByCity()}°", size=60, weight="bold"),
                    ],
                    expand=True, 
                ),
                ft.Column(
                    controls=[self.api.getImageByWeather()],
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    expand=True 
                )
            ],
            expand=True,
        )


    def build(self):
        return ft.Container(
            expand=True,
            padding=20,
            content=self.createMainInformation(),
        )
