import flet as ft

from layout.FrontEnd.InformationCharts.TemperatureChart import TemperatureChart
from layout.FrontEnd.Sidebar.Sidebar import Sidebar
from layout.FrontEnd.InformationTab.InformationTab import InformationTab
from layout.FrontEnd.WeeklyWeather.WeeklyWeather import WeeklyWeather


class Main:

    def main(page: ft.Page):

        page.title = "App Meteo"
        page.theme_mode = ft.ThemeMode.DARK
        page.adaptive = True

        language = "it"
        unit = "metric"
        default_city = "Milano"

        # Contenitori dinamici
        info_container = ft.Container()
        weekly_container = ft.Container()
        chart_component = ft.Container()

        def update_city(new_city):
            info_tab = InformationTab(page, new_city, language, unit)
            weekly_weather = WeeklyWeather(page, new_city, language, unit)
            temperature_chart = TemperatureChart(page, new_city, language, unit)

            info_container.content = info_tab.build()
            weekly_container.content = weekly_weather.build()
            chart_component.content = temperature_chart.build()

            page.update()

        def handle_city_change(city):
            update_city(city)

        # Sidebar con callback corretta
        sidebar = Sidebar(page, on_city_selected=handle_city_change)

        # Layout principale
        page.add(
            ft.Column(
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=sidebar.build(),
                                col={"xs": 12, "lg": 7},
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=info_container,
                                col={"xs": 12, "md": 3, "lg": 7},
                            ),
                            ft.Container(
                                content=weekly_container,
                                col={"xs": 12, "md": 3, "lg": 5},
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=chart_component,
                                col={"xs": 12, "md": 6, "lg": 12}
                            )
                        ]
                    )
                ]
            )
        )

        update_city(default_city)


if __name__ == "__main__":
    ft.app(target=Main.main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
