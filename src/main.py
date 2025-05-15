import flet as ft
from layout.FrontEnd.Sidebar.Sidebar import Sidebar
from layout.FrontEnd.InformationTab.InformationTab import InformationTab
from layout.FrontEnd.WeeklyWeather.WeeklyWeather import WeeklyWeather

class Main:

    def main(page: ft.Page):

        page.title = "App Meteo"
        page.theme_mode = ft.ThemeMode.DARK


        city = "Milano"
        language = "sq"
        unit = "metric"

        sidebar = Sidebar(page)
        informationTab = InformationTab(page, city, language, unit)
        weeklyWeather = WeeklyWeather(page, city, language, unit)

        page.add(
            ft.Row(
                controls=[
                    ft.Container(content=sidebar.build()),
                    ft.Container(content=informationTab.build(), expand=4),
                    ft.Container(content=weeklyWeather.build(), expand=2),
                ],
                expand=True
            )
        )

    ft.app(target=main, assets_dir="assets")
