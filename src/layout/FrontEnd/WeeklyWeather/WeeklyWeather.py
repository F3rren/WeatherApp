from datetime import datetime, timedelta
import flet as ft

from layout.BackEnd.APIOperation import APIOperation

SIZE_TEXT = 18

class WeeklyWeather:

    def __init__(self, page, city = "Milano"):
        self.city = city
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",
        self.api = APIOperation()

    def get_upcoming_days(self, n):
        today = datetime.now()
        return [(today + timedelta(days=i)).strftime("%a") for i in range(n)]

    def generate_forecast(self):
        blocks = []
        days = self.get_upcoming_days(7)
        today_abbrev = datetime.now().strftime("%a")
        self.api.getWeeklyForecast(self.city)
        for idx, abbrev in enumerate(days):
            min_temp, max_temp = self.api.getMinMaxTemperatureByCity(self.city)
            is_today = abbrev == today_abbrev
            label = "Today" if is_today else abbrev

            row = ft.Row(
                controls=[
                    ft.Text(
                        label,
                        size=SIZE_TEXT,
                        color=self.txtcolor,
                        weight="bold" if is_today else "normal",
                    ),
                    ft.Text(f"{min_temp}°/{max_temp}°", size=SIZE_TEXT, color=self.txtcolor),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

            # ⬇️ Ogni blocco contiene riga + divider
            row_block = ft.Column(
                controls=[
                    row,
                    ft.Divider(thickness=1, color="gray") if idx < len(days) - 1 else ft.Container(),
                ],
                expand=True,
                spacing=0,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )

            blocks.append(row_block)

        return blocks


    def build(self):
        return ft.Container(
            bgcolor=self.bgcolor,
            border_radius=15,
            padding=20,
            margin=ft.Margin(10, 80, 10, 10),
            content=ft.Column(
                controls=[
                    ft.Text("7-DAY FORECAST", size=SIZE_TEXT + 6, weight="bold", color=ft.colors.WHITE),
                    ft.Column(
                        controls=self.generate_forecast(),
                        expand=True,
                        spacing=0,
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    )
                ],
                expand=True,
                spacing=15,
            )
        )
