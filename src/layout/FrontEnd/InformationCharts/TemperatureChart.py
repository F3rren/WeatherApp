import flet as ft
from layout.BackEnd.APIOperation import APIOperation

class TemperatureChart:

    def __init__(self, page, city, language, unit):
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626"
        self.txtcolor = "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff"
        self.unit = unit
        self.api = APIOperation(page, city, language, unit)

    def createChart(self):
        # Recupera i dati
        days_list = self.api.getUpcomingDay()[:5]
        temp_min_list, temp_max_list = self.api.getUpcomingMinMaxTemperature()
        
        # Serie di dati: min e max
        data_series = [
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i + 1, t) for i, t in enumerate(temp_min_list)],
                stroke_width=4,
                color=ft.Colors.BLUE,
                curved=True,
                stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i + 1, t) for i, t in enumerate(temp_max_list)],
                stroke_width=4,
                color=ft.Colors.RED,
                curved=True,
                stroke_cap_round=True,
            ),
        ]

        # Etichette X: giorni
        x_labels = [
            ft.ChartAxisLabel(
                value=i + 1,
                label=ft.Container(
                    ft.Text(
                        day,
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=self.txtcolor
                    ),
                    margin=ft.margin.only(top=10),
                )
            )
            for i, day in enumerate(days_list)
        ]

        # Etichette Y dinamiche
        max_temp = max(temp_max_list)
        max_y = int((max_temp + 4) // 5 * 5)

        y_labels = [
            ft.ChartAxisLabel(
                value=y,
                label=ft.Text(str(y), size=12)
            )
            for y in range(0, max_y + 1, 5)
        ]

        # Costruzione grafico
        chart = ft.LineChart(
            data_series=data_series,
            border=ft.border.all(1, ft.Colors.GREY),
            left_axis=ft.ChartAxis(labels=y_labels, labels_size=40),
            bottom_axis=ft.ChartAxis(labels=x_labels, labels_size=40),
            tooltip_bgcolor=ft.Colors.with_opacity(0.0, ft.Colors.TRANSPARENT), 
            min_y=0,
            max_y=max_y,
            min_x=0,
            max_x=6,
            expand=True,
        )

        return chart


    def build(self):  
        return ft.Container(
            bgcolor=self.bgcolor,
            border_radius=15,
            padding=30,
            content=self.createChart()
        )
