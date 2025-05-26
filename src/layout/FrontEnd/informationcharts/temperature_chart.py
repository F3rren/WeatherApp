import flet as ft
from typing import List

class TemperatureChart:
    """
    Temperature chart display.
    """
    
    def __init__(self, page: ft.Page, days: List[str], temp_min: List[int], 
                 temp_max: List[int], text_color: str):
        self.page = page
        self.days = days
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.text_color = text_color
    
    def build(self) -> ft.Column:
        """Build the temperature chart"""
        # Calculate dynamic range with margin
        min_temp = min(self.temp_min) if self.temp_min else 0
        max_temp = max(self.temp_max) if self.temp_max else 30
        min_y = int((min_temp - 5) // 5 * 5)
        max_y = int((max_temp + 5) // 5 * 5)
        min_y = max(min_y, 0)
        
        # Data series
        data_series = [
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i + 1, t) for i, t in enumerate(self.temp_min)],
                stroke_width=5,
                color=ft.Colors.BLUE,
                curved=True,
                stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i + 1, t) for i, t in enumerate(self.temp_max)],
                stroke_width=5,
                color=ft.Colors.RED,
                curved=True,
                stroke_cap_round=True,
            ),
        ]
        
        # X-axis labels
        x_labels = [
            ft.ChartAxisLabel(
                value=i + 1,
                label=ft.Container(
                    ft.Text(
                        day,
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=self.text_color
                    ),
                    margin=ft.margin.only(top=10),
                )
            )
            for i, day in enumerate(self.days)
        ]
        
        # Y-axis labels
        y_labels = [
            ft.ChartAxisLabel(
                value=y,
                label=ft.Text(str(y), size=12, color=self.text_color)
            )
            for y in range(min_y, max_y + 1, 5)
        ]
        
        # Chart
        chart = ft.LineChart(
            data_series=data_series,
            border=ft.border.all(3, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
                width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
                width=1
            ),
            left_axis=ft.ChartAxis(labels=y_labels, labels_size=40),
            bottom_axis=ft.ChartAxis(labels=x_labels, labels_size=40),
            tooltip_bgcolor=(
                ft.Colors.WHITE if self.text_color == "#000000" else ft.Colors.GREY_800
            ),
            min_y=min_y,
            max_y=max_y,
            min_x=0,
            max_x=6,
            expand=True,
        )
        
        return ft.Column([
            ft.Row([
                ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.RED),
                ft.Text("Max", color=self.text_color),
                ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.BLUE),
                ft.Text("Min", color=self.text_color),
            ], spacing=20),
            chart
        ])
