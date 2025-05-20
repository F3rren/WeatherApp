import flet as ft
from layout.BackEnd.APIOperation import APIOperation

class DailyForecast:

    def __init__(self, page, city, language, unit):
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",
        self.page = page
        page.update()
        
        self.city = city
        self.language = language
        self.unit = unit
        self.api = APIOperation(page, city, language, unit)

    def update_city(self, new_city):
        self.city = new_city
        # Update the API instance with the new city
        self.api = APIOperation(self.page, new_city, self.language, self.unit)
        
    def update_data(self, city, language, unit):
        self.city = city
        self.language = language
        self.unit = unit
        # Update the API instance with the new parameters
        self.api = APIOperation(self.page, city, language, unit)
        

    def createHourlyForecast(self):
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        controls=[self.api.getDailyForecast()],
                        scroll=ft.ScrollMode.AUTO,  # Scroll orizzontale qui
                    ),
                ],
            ),
            expand=True
        )



    def build(self):
        return ft.Container(
            bgcolor=self.bgcolor,
            border_radius=15,
            padding=20,
            content=self.createHourlyForecast(),
        )
