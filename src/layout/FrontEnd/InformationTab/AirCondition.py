import flet as ft
from layout.BackEnd.APIOperation import APIOperation

class AirCondition:

    def __init__(self, page, city = "Milano"):
        self.city = city
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",
        self.api = APIOperation(page)

    def createAirConditionTab(self):
        informationTag = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Icon(name=ft.icons.THERMOSTAT, size=30),
                        ft.Text(
                            f"Real feel: {self.api.getRealFeelByCity(self.city)}°",
                            size=20,
                            weight="bold",
                            color=self.txtcolor,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        ft.Icon(name=ft.icons.AIR, size=30),
                        ft.Text(
                            f"Wind: {self.api.getWindInformation(self.city)} km/h",
                            size=20,
                            weight="bold",
                            color=self.txtcolor,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        ft.Icon(name=ft.icons.WATER_DROP, size=30),
                        ft.Text(
                            f"Humidity: {self.api.getHumidityInformation(self.city)}%",
                            size=20,
                            weight="bold",
                            color=self.txtcolor,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        ft.Icon(name=ft.icons.SPEED, size=30),
                        ft.Text(
                            f"Pressure: {self.api.getPressureInformation(self.city)} hPa",
                            size=20,
                            weight="bold",
                            color=self.txtcolor,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,  # Distribuisce in modo uniforme
            spacing=20
        )

        return informationTag


    def build(self):
        return ft.Container(
            bgcolor=self.bgcolor,
            border_radius=15,
            padding=25,       
            expand=True,           
            content=self.createAirConditionTab() 
        )
