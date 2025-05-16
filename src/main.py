import flet as ft

from layout.FrontEnd.Sidebar.Sidebar import Sidebar
from layout.FrontEnd.InformationTab.InformationTab import InformationTab
from layout.FrontEnd.WeeklyWeather.WeeklyWeather import WeeklyWeather

def main(page: ft.Page):

    page.title = "App Meteo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.adaptive = True
    page.scroll = True

    city = "Milano"
    language = "it"
    unit = "metric"

    sidebar = Sidebar(page)
    informationTab = InformationTab(page, city, language, unit)
    weeklyWeather = WeeklyWeather(page, city, language, unit)

    page.add(
        ft.Column(
            controls=[
                # Sidebar in riga sopra
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=sidebar.build(),
                            col={"xs": 12}
                        )
                    ]
                ),
                # RIGA sotto con i due componenti principali
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=informationTab.build(),
                            col={"xs": 12, "md": 7}
                        ),
                        ft.Container(
                            content=weeklyWeather.build(),
                            col={"xs": 12, "md": 5}
                        )
                    ]
                )
            ]
        )
    )



if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
