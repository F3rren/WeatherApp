import flet as ft
from layout.backend.api_operation import APIOperation

class DailyForecast:

    def __init__(self, page, city, language, unit):
        self.txtcolor= "#1F1A1A" if page.theme_mode == ft.ThemeMode.LIGHT else "#adadad" #"#262626",
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
        page.update()
        
        self.city = city
        self.language = language
        self.unit = unit
        self.api = APIOperation(page, city, language, unit)

    def update_city(self, new_city):
        self.city = new_city
        # Update the API instance with the new city
        self.api.update_data(new_city, self.language, self.unit)
        
    def update_by_coordinates(self, lat, lon):
        """Aggiorna le informazioni meteo usando le coordinate geografiche"""
        self.api.update_coordinates(lat, lon, self.language, self.unit)
        self.city = self.api.city  # Aggiorna il nome della città dal geocoding inverso
        
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
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH, # <--- MODIFICATO QUI
                controls=[
                    ft.Row(
                        controls=[self.api.getDailyForecast()],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
            ),
            expand=True
        )



    def build(self):
        return ft.Container(
            gradient=self.gradient,
            border_radius=15,
            padding=20,
            content=self.createHourlyForecast(),
        )
