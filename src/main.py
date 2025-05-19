import flet as ft

from layout.FrontEnd.Sidebar.Sidebar import Sidebar
from layout.FrontEnd.InformationTab.InformationTab import InformationTab
from layout.FrontEnd.WeeklyWeather.WeeklyWeather import WeeklyWeather

def main(page: ft.Page):

    page.title = "App Meteo"
    page.theme_mode = ft.ThemeMode.DARK
    page.adaptive = True

    language = "it"
    unit = "metric"
    default_city = "Milano"

    # Containers vuoti che conterranno le UI aggiornabili
    info_container = ft.Container()
    weekly_container = ft.Container()

    # Funzione che aggiorna le view
    def update_city(new_city):
        info_tab = InformationTab(page, new_city, language, unit)
        weekly_weather = WeeklyWeather(page, new_city, language, unit)
        info_container.content = info_tab.build()
        weekly_container.content = weekly_weather.build()
        page.update()

        # Passa la callback alla Sidebar
    sidebar = Sidebar(page, on_city_selected=update_city)

    # Inizializza con Milano
    update_city(default_city)

    page.add(
        ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=sidebar.build(),  # usa .build() sulla sidebar
                            col={"xs": 12},
                            padding=10
                        )
                    ]
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=info_container,
                            col={"xs": 12, "md": 7}
                        ),
                        ft.Container(
                            content=weekly_container,
                            col={"xs": 12, "md": 5}
                        )
                    ]
                )
            ]
        )
    )


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
