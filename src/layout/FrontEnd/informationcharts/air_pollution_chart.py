import flet as ft
from layout.backend.air_pollution_operation import AirPollutionOperation

class AirPollutionChart:
    """
    Air Pollution chart display.
    """
    def __init__(self, page, lat=None, lon=None):
        self.page = page
        self.lat = lat
        self.lon = lon
        self.txtcolor = "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff"
        self.api = AirPollutionOperation()
        self.pollution_data = {}
        
        # Initialize with default values
        self.aqi = 0
        self.co = 0
        self.no = 0
        self.no2 = 0
        self.o3 = 0
        self.so2 = 0
        self.pm2_5 = 0
        self.pm10 = 0
        self.nh3 = 0

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


    def createAirPollutionChart(self, lat, lon):

        self.lat = lat
        self.lon = lon
        # Get air pollution data
        self.pollution_data = self.api.get_air_pollution(lat, lon)
        
        # Update component properties
        self.aqi = self.pollution_data.get("aqi", 0)
        self.co = self.pollution_data.get("co", 0)
        self.no = self.pollution_data.get("no", 0)
        self.no2 = self.pollution_data.get("no2", 0)
        self.o3 = self.pollution_data.get("o3", 0)
        self.so2 = self.pollution_data.get("so2", 0)
        self.pm2_5 = self.pollution_data.get("pm2_5", 0)
        self.pm10 = self.pollution_data.get("pm10", 0)
        self.nh3 = self.pollution_data.get("nh3", 0)

        chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=self.co,
                            width=40,
                            color=ft.Colors.RED,
                            tooltip=f"{self.co}",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=1,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=self.no,
                            width=40,
                            color=ft.Colors.ORANGE,
                            tooltip=f"{self.no}",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=2,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=int(self.no2),
                            width=40,
                            color=ft.Colors.YELLOW,
                            tooltip=f"{self.no2}",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=3,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=int(self.o3),
                            width=40,
                            color=ft.Colors.GREEN,
                            tooltip=f"{self.o3}",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=4,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=int(self.so2),
                            width=40,
                            color=ft.Colors.BLUE,
                            tooltip=f"{self.so2}",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=5,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=int(self.pm2_5),
                            width=40,
                            color=ft.Colors.INDIGO,
                            tooltip=f"{self.pm2_5}",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=6,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=int(self.pm10),
                            width=40,
                            color=ft.Colors.PURPLE,
                            tooltip=f"{self.pm10}",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=7,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=int(self.nh3),
                            width=40,
                            color=ft.Colors.BLACK,
                            tooltip=f"{self.nh3}",
                            border_radius=0,
                            
                        ),
                    ],
                ),
            ],
            border=ft.border.all(1, ft.Colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Air Pollution (μg/m³)"), title_size=40
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container(ft.Text("CO"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=1, label=ft.Container(ft.Text("NO"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=2, label=ft.Container(ft.Text("NO₂"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=3, label=ft.Container(ft.Text("O₃"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=4, label=ft.Container(ft.Text("SO₂"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=5, label=ft.Container(ft.Text("PM2.5"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=6, label=ft.Container(ft.Text("PM10"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=7, label=ft.Container(ft.Text("NH₃"), padding=10)
                    ),
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_300, width=1, dash_pattern=[9, 4]
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
            max_y=120,
            interactive=True,
            expand=True,
        )

        return ft.Column([ 
            chart
        ])

    def build(self, lat, long):
        return ft.Container(
            gradient=self.gradient,
            border_radius=15,
            padding=30,
            content=self.createAirPollutionChart(lat, long),
        )