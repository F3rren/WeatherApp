import flet as ft
from layout.backend.air_pollution_operation import AirPollutionOperation
from config import LIGHT_THEME, DARK_THEME # Import theme configurations

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

        # self.gradient = self._get_gradient() # Gradient seems unused, can be removed or updated

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
            
            # Update left axis labels (if they are simple text, not implemented here yet)
            # If Y labels also need dynamic color, their creation should store ft.Text and be updated here.

    # def _get_gradient(self) -> ft.LinearGradient: # Gradient seems unused
    #     """Get the gradient based on the current theme"""
    #     if self.page.theme_mode == ft.ThemeMode.DARK:
    #         return ft.LinearGradient(
    #             begin=ft.alignment.top_left,
    #             end=ft.alignment.bottom_right,
    #             colors=[ft.Colors.BLUE, ft.Colors.YELLOW]
    #         )
    #     else:
    #         return ft.LinearGradient(
    #             begin=ft.alignment.top_left,
    #             end=ft.alignment.bottom_right,
    #             colors=["#1a1a1a", "#333333"],
    #         )

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

        self.chart_control = ft.BarChart( # Store chart reference
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
            border=ft.border.all(1, ft.Colors.GREY_400), # Consider theme for border
            left_axis=ft.ChartAxis(
                labels_size=40, 
                title=ft.Text("Air Pollution (μg/m³)", color=self.text_color), # Apply text_color
                title_size=40
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container(ft.Text("CO", color=self.text_color), padding=10) # Apply text_color
                    ),
                    ft.ChartAxisLabel(
                        value=1, label=ft.Container(ft.Text("NO", color=self.text_color), padding=10) # Apply text_color
                    ),
                    ft.ChartAxisLabel(
                        value=2, label=ft.Container(ft.Text("NO₂", color=self.text_color), padding=10) # Apply text_color
                    ),
                    ft.ChartAxisLabel(
                        value=3, label=ft.Container(ft.Text("O₃", color=self.text_color), padding=10) # Apply text_color
                    ),
                    ft.ChartAxisLabel(
                        value=4, label=ft.Container(ft.Text("SO₂", color=self.text_color), padding=10) # Apply text_color
                    ),
                    ft.ChartAxisLabel(
                        value=5, label=ft.Container(ft.Text("PM2.5", color=self.text_color), padding=10) # Apply text_color
                    ),
                    ft.ChartAxisLabel(
                        value=6, label=ft.Container(ft.Text("PM10", color=self.text_color), padding=10) # Apply text_color
                    ),
                    ft.ChartAxisLabel(
                        value=7, label=ft.Container(ft.Text("NH₃", color=self.text_color), padding=10) # Apply text_color
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
            self.chart_control # Return stored chart reference
        ])

    def build(self, lat, long):
        # Store the container for potential updates (e.g. gradient)
        self.container_control = ft.Container(
            # gradient=self.gradient, # Gradient is currently unused
            border_radius=15,
            padding=30,
            content=self.createAirPollutionChart(lat, long),
        )
        return self.container_control