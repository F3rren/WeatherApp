import flet as ft
from layout.BackEnd.APIOperation import APIOperation

class AirCondition:

    def __init__(self, page, city, language, unit):
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",
        page.scroll = True
        
        self.city = city
        self.api = APIOperation(page, city, language, unit)
        
    def update_data(self, city, language, unit):
        self.city = city
        self.language = language
        self.unit = unit
        self.fetch_data_again()  # un metodo che rifà la chiamata API e aggiorna i controlli

    def createAirConditionTab(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Prima riga: Real feel + Wind
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.Icons.THERMOSTAT, size=30),
                                        ft.Text(
                                            f"Real feel: {self.api.getRealFeelByCity()}°",
                                            size=20,
                                            weight="bold",
                                            color=self.txtcolor,
                                        )
                                    ]
                                ),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.Icons.AIR, size=30),
                                        ft.Text(
                                            f"Wind: {self.api.getWindInformation()} km/h",
                                            size=20,
                                            weight="bold",
                                            color=self.txtcolor,
                                        )
                                    ]
                                ),
                                expand=True
                            )
                        ]
                    ),

                    # Seconda riga: Humidity + Pressure
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.Icons.WATER_DROP, size=30),
                                        ft.Text(
                                            f"Humidity: {self.api.getHumidityInformation()}%",
                                            size=20,
                                            weight="bold",
                                            color=self.txtcolor,
                                        )
                                    ]
                                ),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.Icons.SPEED, size=30),
                                        ft.Text(
                                            f"Pressure: {self.api.getPressureInformation()} hPa",
                                            size=20,
                                            weight="bold",
                                            color=self.txtcolor,
                                        )
                                    ],
                                ),
                                expand=True
                            )
                        ]
                    )
                ]
            )
        )


    def build(self):
        return ft.Container(
            bgcolor=self.bgcolor,
            border_radius=15,
            padding=20,      
            content=self.createAirConditionTab(),
        )
        
