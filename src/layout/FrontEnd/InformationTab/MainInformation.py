import random
import flet as ft
from layout.BackEnd.APIOperation import APIOperation

class MainInformation:
    def __init__(self, page, city="Milano"):
        self.city = city
        self.api = APIOperation(page)

    def createMainInformation(self):
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(self.city, size=40, weight="bold"),
                        ft.Text(f"Visibility: {self.api.getVisibilityPercentage(self.city)} km", size=20),
                        ft.Text(f"{self.api.getTemperatureByCity(self.city)}°", size=60, weight="bold"),
                    ],
                    expand=True, 
                ),
                ft.Column(
                    controls=[self.api.getImageByWeather(self.city)],
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
