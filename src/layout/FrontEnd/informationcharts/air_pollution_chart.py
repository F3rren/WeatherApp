import flet as ft
import math # Added import math
from services.api_service import ApiService # Import ApiService instead of AirPollutionOperation
from config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler # Import theme configurations

class AirPollutionChart:
    """
    Air Pollution chart display.
    """
    def __init__(self, page, lat=None, lon=None, text_color: str = None): # Added text_color
        self.page = page
        self.lat = lat
        self.lon = lon
        # Set initial text_color or derive from theme
        if text_color:
            self.text_color = text_color
        else:
            self.text_color = DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"]
        
        self.api = ApiService()
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

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 40,   # Titolo "Condizioni Atmosferiche" (aumentato da 20 a 40)
                'label': 35,   # Etichette come "Percepita", "Umidità" (aumentato da 15 a 35)
                'value': 35    # Valori come temperature, percentuali (aumentato da 15 a 35)
            }
        )

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
            
            # self.gradient = self._get_gradient() # Update gradient if it were used

            # Update chart axis and title colors
            if hasattr(self, 'chart_control') and self.chart_control.page:
                self._update_chart_text_colors() # Implement this method
                self.chart_control.update()
            elif hasattr(self, 'container_control') and self.container_control.page:
                # If chart is not yet built but container is, trigger rebuild of content
                if self.lat is not None and self.lon is not None:
                    new_chart_column = self.createAirPollutionChart(self.lat, self.lon)
                    self.container_control.content = new_chart_column
                    # self.container_control.gradient = self._get_gradient() # Update gradient if used
                    self.container_control.update()

    def _update_chart_text_colors(self):
        """Updates the text colors of the chart's axes and title."""
        if hasattr(self, 'chart_control'):
            # Update bottom axis labels
            if self.chart_control.bottom_axis and self.chart_control.bottom_axis.labels:
                for label in self.chart_control.bottom_axis.labels:
                    if isinstance(label.label, ft.Container) and isinstance(label.label.content, ft.Text):
                        label.label.content.color = self.text_color
            
            # Update left axis title
            if self.chart_control.left_axis and isinstance(self.chart_control.left_axis.title, ft.Text):
                self.chart_control.left_axis.title.color = self.text_color
            
    def createAirPollutionChart(self, lat, lon):

        self.lat = lat
        self.lon = lon
        # Get air pollution data
        self.pollution_data = self.api.get_air_pollution(lat, lon)
        
        # Update component properties, ensuring they are floats
        self.aqi = float(self.pollution_data.get("aqi", 0.0)) # AQI might not be directly on the bar chart
        self.co = float(self.pollution_data.get("co", 0.0))
        self.no = float(self.pollution_data.get("no", 0.0))
        self.no2 = float(self.pollution_data.get("no2", 0.0))
        self.o3 = float(self.pollution_data.get("o3", 0.0))
        self.so2 = float(self.pollution_data.get("so2", 0.0))
        self.pm2_5 = float(self.pollution_data.get("pm2_5", 0.0))
        self.pm10 = float(self.pollution_data.get("pm10", 0.0))
        self.nh3 = float(self.pollution_data.get("nh3", 0.0))

        # Calculate dynamic max_y for the chart
        all_pollution_metrics = [
            self.co, self.no, self.no2, self.o3,
            self.so2, self.pm2_5, self.pm10, self.nh3
        ]
        
        max_val = 0.0
        numeric_metrics = [m for m in all_pollution_metrics if isinstance(m, (int, float))]
        if numeric_metrics:
            max_val = max(numeric_metrics)

        raw_dynamic_max_y = 0.0 # Renamed from dynamic_max_y to avoid confusion before rounding
        if max_val == 0.0:
            raw_dynamic_max_y = 50.0  # Default max_y if all values are zero
        else:
            # Add a 20% buffer or a fixed 10 units, whichever is larger
            buffered_max_percentage = max_val * 1.2
            buffered_max_fixed = max_val + 10.0
            raw_dynamic_max_y = max(buffered_max_percentage, buffered_max_fixed)
            # Ensure the y-axis isn't too cramped if values are small but non-zero, e.g., min height of 20
            raw_dynamic_max_y = max(raw_dynamic_max_y, 20.0)

        # Round up to the nearest nice number (10, 20, 50)
        if raw_dynamic_max_y <= 0: # Handle edge case of zero or negative before rounding
            final_max_y = 50.0
        elif raw_dynamic_max_y <= 50:
            final_max_y = math.ceil(raw_dynamic_max_y / 10) * 10
        elif raw_dynamic_max_y <= 200:
            final_max_y = math.ceil(raw_dynamic_max_y / 20) * 20
        else:
            final_max_y = math.ceil(raw_dynamic_max_y / 50) * 50
        
        # Ensure final_max_y is at least a small default if all calculations result in very low numbers
        final_max_y = max(final_max_y, 10.0) 

        self.chart_control = ft.BarChart( # Store chart reference
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=self.co, # Use float value
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
                            to_y=self.no, # Use float value
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
                            to_y=self.no2, # Use float value
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
                            to_y=self.o3, # Use float value
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
                            to_y=self.so2, # Use float value
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
                            to_y=self.pm2_5, # Use float value
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
                            to_y=self.pm10, # Use float value
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
                            to_y=self.nh3, # Use float value
                            width=40,
                            color=ft.Colors.BLACK,
                            tooltip=f"{self.nh3}",
                            border_radius=0,
                            
                        ),
                    ],
                ),
            ],
            border=ft.border.all(1, ft.Colors.GREY_400), # Consider theme for border
            left_axis=ft.ChartAxis(
                labels_size=40, 
                title=ft.Text("Air Pollution (μg/m³)", color=self.text_color), # Apply text_color
                title_size=16 # Changed from 40 to 16
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container(ft.Text("CO", color=self.text_color, size=self.text_handler.get_size('label')), padding=10) # Apply text_color and size
                    ),
                    ft.ChartAxisLabel(
                        value=1, label=ft.Container(ft.Text("NO", color=self.text_color, size=self.text_handler.get_size('label')), padding=10) # Apply text_color and size
                    ),
                    ft.ChartAxisLabel(
                        value=2, label=ft.Container(ft.Text("NO₂", color=self.text_color, size=self.text_handler.get_size('label')), padding=10) # Apply text_color and size
                    ),
                    ft.ChartAxisLabel(
                        value=3, label=ft.Container(ft.Text("O₃", color=self.text_color, size=self.text_handler.get_size('label')), padding=10) # Apply text_color and size
                    ),
                    ft.ChartAxisLabel(
                        value=4, label=ft.Container(ft.Text("SO₂", color=self.text_color, size=self.text_handler.get_size('label')), padding=10) # Apply text_color and size
                    ),
                    ft.ChartAxisLabel(
                        value=5, label=ft.Container(ft.Text("PM2.5", color=self.text_color, size=self.text_handler.get_size('label')), padding=10) # Apply text_color and size
                    ),
                    ft.ChartAxisLabel(
                        value=6, label=ft.Container(ft.Text("PM10", color=self.text_color, size=self.text_handler.get_size('label')), padding=10) # Apply text_color and size
                    ),
                    ft.ChartAxisLabel(
                        value=7, label=ft.Container(ft.Text("NH₃", color=self.text_color, size=self.text_handler.get_size('label')), padding=10) # Apply text_color and size
                    ),
                ],
                labels_size=50, # Restored and set to 50 to ensure space for labels
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_300, width=1, dash_pattern=[9, 4]
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
            max_y=final_max_y, # Use calculated and rounded final_max_y
            interactive=True,
            expand=True,
        )

        return ft.Column([ 
            self.chart_control # Return stored chart reference
        ])

    def build(self, lat, long):
        # Store the container for potential updates (e.g. gradient)
        self.container_control = ft.Container(
            border_radius=15,
            padding=30,
            content=self.createAirPollutionChart(lat, long),
        )
        return self.container_control