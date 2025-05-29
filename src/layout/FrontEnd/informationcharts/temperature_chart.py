import flet as ft
from typing import List
from config import LIGHT_THEME, DARK_THEME # Import theme configurations

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
        self.text_color = text_color # Initial text color

        # Store references to text elements that need color updates
        self.legend_max_text = ft.Text("Max", color=self.text_color)
        self.legend_min_text = ft.Text("Min", color=self.text_color)
        # Axis labels are more complex as they are generated in build()
        # We will need to re-generate them or update their color in handle_theme_change

        # Register for theme change events
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_change)
    
    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color and chart elements."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]

            # Update legend text colors
            if hasattr(self, 'legend_max_text'):
                self.legend_max_text.color = self.text_color
                if self.legend_max_text.page:
                    self.legend_max_text.update()
            
            if hasattr(self, 'legend_min_text'):
                self.legend_min_text.color = self.text_color
                if self.legend_min_text.page:
                    self.legend_min_text.update()

            # For axis labels, the chart might need to be rebuilt or its components updated directly.
            # This example assumes the parent (WeatherView) will refresh the chart component,
            # which will then call build() again with the new text_color.
            # If more direct control is needed, store and update axis label Text objects.
            if hasattr(self, 'chart_control') and self.chart_control.page:
                 # Update axis label colors directly if possible, or trigger a rebuild
                 self._update_chart_axis_colors() # Implement this method
                 self.chart_control.update()

    def _update_chart_axis_colors(self):
        """Updates the colors of chart axis labels."""
        if hasattr(self, 'chart_control'):
            # Update X-axis labels
            if self.chart_control.bottom_axis and self.chart_control.bottom_axis.labels:
                for label in self.chart_control.bottom_axis.labels:
                    if isinstance(label.label, ft.Container) and isinstance(label.label.content, ft.Text):
                        label.label.content.color = self.text_color
            # Update Y-axis labels
            if self.chart_control.left_axis and self.chart_control.left_axis.labels:
                for label in self.chart_control.left_axis.labels:
                    if isinstance(label.label, ft.Text):
                        label.label.color = self.text_color

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
                        color=self.text_color # Apply text_color
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
                label=ft.Text(str(y), size=12, color=self.text_color) # Apply text_color
            )
            for y in range(min_y, max_y + 1, 5)
        ]
        
        # Chart
        self.chart_control = ft.LineChart( # Store chart for potential direct updates
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
            min_y=min_y,
            max_y=max_y,
            min_x=0,
            max_x=6,
            expand=True,
        )
        
        return ft.Column([
            ft.Row(
                [
                    ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.RED),
                    self.legend_max_text, # Use stored text control
                    ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.BLUE),
                    self.legend_min_text, # Use stored text control
                ], 
            spacing=20
        ),
            self.chart_control # Use stored chart control
        ]
    )
