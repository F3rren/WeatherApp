import flet as ft
import math
from services.api_service import ApiService
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE # Added DEFAULT_LANGUAGE
from components.responsive_text_handler import ResponsiveTextHandler
# Removed: from services.translation_service import TranslationService # Not used directly for chart labels yet

class AirPollutionChart:
    """
    Air Pollution chart display.
    """
    def __init__(self, page, lat=None, lon=None, text_color: str = None):
        self.page = page
        self.lat = lat
        self.lon = lon
        self._state_manager = None
        self.chart_control = None # Ensure chart_control is initialized
        self.container_control = None # Ensure container_control is initialized

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

        self.language = DEFAULT_LANGUAGE # Initialize language

        if self.page and hasattr(self.page, 'session'):
            self._state_manager = self.page.session.get('state_manager')
            if self._state_manager:
                self.language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
                # Update text_color based on initial theme from state_manager if possible, or page
                current_theme_mode = self._state_manager.get_state('theme_mode') or self.page.theme_mode
                self.text_color = DARK_THEME["TEXT"] if current_theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"]
                
                self._state_manager.register_observer("theme_event", self._handle_state_change)
                self._state_manager.register_observer("language_event", self._handle_state_change)

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'label': 12,
                'subtitle': 15,
                'icon': 40,
            },
            breakpoints=[600, 900, 1200, 1600]
        )

        self.text_controls = {}
        
        if self.page:
            def combined_resize_handler(e):
                self.text_handler._handle_resize(e)
                if hasattr(self, 'chart_control') and self.chart_control and self.chart_control.page:
                     self._update_chart_text_colors()
                     self.chart_control.update()
                elif hasattr(self, 'container_control') and self.container_control and self.container_control.page:
                    if self.lat is not None and self.lon is not None:
                        new_chart_column = self.createAirPollutionChart(self.lat, self.lon)
                        self.container_control.content = new_chart_column
                        self.container_control.update()

            self.page.on_resize = combined_resize_handler

    def _determine_text_color(self): # Helper to get current theme's text color
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config["TEXT"]
        return LIGHT_THEME["TEXT"] # Fallback

    def _handle_state_change(self, event_data=None): # Renamed from handle_theme_change
        """Handles theme or language change events."""
        if self._state_manager:
            self.language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
            # Potentially update other language-dependent things here if chart labels were translated

        # Update text_color based on the current theme from the page
        self.text_color = self._determine_text_color()
            
        if hasattr(self, 'chart_control') and self.chart_control and self.chart_control.page:
            self._update_chart_text_colors() # This updates colors and calls update_text_controls for sizes
            if hasattr(self.chart_control, 'page') and self.chart_control.page:
                self.chart_control.update()
        elif hasattr(self, 'container_control') and self.container_control and self.container_control.page:
            # Fallback to rebuild if chart_control isn't directly accessible or on page
            if self.lat is not None and self.lon is not None:
                new_chart_column = self.createAirPollutionChart(self.lat, self.lon)
                self.container_control.content = new_chart_column
                if hasattr(self.container_control, 'page') and self.container_control.page:
                    self.container_control.update()
    # ...existing code...
    def _update_chart_text_colors(self):
        """Updates the text colors of the chart's axes, title, and border."""
        if hasattr(self, 'chart_control') and self.chart_control:
            current_text_color = self._determine_text_color() # Get up-to-date text color
            # Update bottom axis labels
            if self.chart_control.bottom_axis and self.chart_control.bottom_axis.labels:
                for label_obj in self.chart_control.bottom_axis.labels:
                    if isinstance(label_obj.label, ft.Container) and isinstance(label_obj.label.content, ft.Text):
                        label_obj.label.content.color = current_text_color
            
            # Update left axis title
            if self.chart_control.left_axis and isinstance(self.chart_control.left_axis.title, ft.Text):
                self.chart_control.left_axis.title.color = current_text_color

            # Update left axis labels style
            if self.chart_control.left_axis:
                if self.chart_control.left_axis.labels_style:
                    self.chart_control.left_axis.labels_style.color = current_text_color
                else:
                    self.chart_control.left_axis.labels_style = ft.TextStyle(color=current_text_color)

            # Update chart border color
            border_color = DARK_THEME.get("BORDER", ft.Colors.GREY_700) if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME.get("BORDER", ft.Colors.GREY_400)
            self.chart_control.border = ft.border.all(1, border_color)
                
            # Re-register and update text controls for size adjustments if necessary
            self._register_chart_text_controls() 
            self.update_text_controls() 

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
        if raw_dynamic_max_y <= 0: 
            final_max_y = 50.0
        elif raw_dynamic_max_y <= 50:
            final_max_y = math.ceil(raw_dynamic_max_y / 10) * 10
        elif raw_dynamic_max_y <= 200:
            final_max_y = math.ceil(raw_dynamic_max_y / 20) * 20
        else:
            final_max_y = math.ceil(raw_dynamic_max_y / 50) * 50
        
        final_max_y = max(final_max_y, 10.0) 

        current_text_color = self._determine_text_color() # Get current text color for initial setup
        border_color = DARK_THEME.get("BORDER", ft.Colors.GREY_700) if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME.get("BORDER", ft.Colors.GREY_400)

        self.chart_control = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=self.co, # Use float value
                            width=40,
                            color=ft.Colors.RED,
                            tooltip=round(self.co), 
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
                            tooltip=round(self.no),
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
                            tooltip=round(self.no2),
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
                            tooltip=round(self.o3),
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
                            tooltip=round(self.so2),
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
                            tooltip=round(self.pm2_5),
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
                            tooltip=round(self.pm10),
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
                            tooltip=round(self.nh3),
                            border_radius=0,
                            
                        ),
                    ],
                ),
            ],
            border=ft.border.all(1, border_color), 
            left_axis=ft.ChartAxis(
                labels_size=40, 
                title=ft.Text("Air Pollution (μg/m³)", size=self.text_handler.get_size('subtitle'), color=current_text_color),
                title_size=20
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0, 
                        label=ft.Container(
                            ft.Text("CO", color=current_text_color, size=self.text_handler.get_size('label')), 
                            padding=20
                        )
                    ),
                    ft.ChartAxisLabel(
                        value=1, label=ft.Container(ft.Text("NO", color=current_text_color, size=self.text_handler.get_size('label')), padding=20)
                    ),
                    ft.ChartAxisLabel(
                        value=2, label=ft.Container(ft.Text("NO2", color=current_text_color, size=self.text_handler.get_size('label')), padding=20)
                    ),
                    ft.ChartAxisLabel(
                        value=3, label=ft.Container(ft.Text("O3", color=current_text_color, size=self.text_handler.get_size('label')), padding=20)
                    ),
                    ft.ChartAxisLabel(
                        value=4, label=ft.Container(ft.Text("SO2", color=current_text_color, size=self.text_handler.get_size('label')), padding=20)
                    ),
                    ft.ChartAxisLabel(
                        value=5, label=ft.Container(ft.Text("PM2.5", color=current_text_color, size=self.text_handler.get_size('label')), padding=20)
                    ),
                    ft.ChartAxisLabel(
                        value=6, label=ft.Container(ft.Text("PM10", color=current_text_color, size=self.text_handler.get_size('label')), padding=20)
                    ),
                    ft.ChartAxisLabel(
                        value=7, label=ft.Container(ft.Text("NH3", color=current_text_color, size=self.text_handler.get_size('label')), padding=20)
                    ),
                ],
                labels_size=40 # Ensure this is applied if not overridden by individual label styles
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=final_max_y / 5,  # Adjust interval based on max_y for better readability
                color=border_color,  # Use theme-based color for grid lines
                width=1
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            max_y=final_max_y,
            interactive=False, # Set to False as per previous requirements
            expand=True,
        )
        self._register_chart_text_controls() # Register controls for size updates
        self.update_text_controls() # Apply initial sizes
        return ft.Column(controls=[self.chart_control], expand=True)

    def _register_chart_text_controls(self):
        """Registers chart text elements for responsive size updates."""
        self.text_controls.clear() # Clear previous controls
        if hasattr(self, 'chart_control') and self.chart_control:
            if self.chart_control.left_axis and isinstance(self.chart_control.left_axis.title, ft.Text):
                self.text_controls[self.chart_control.left_axis.title] = 'subtitle'
            if self.chart_control.bottom_axis and self.chart_control.bottom_axis.labels:
                for label_obj in self.chart_control.bottom_axis.labels:
                    if isinstance(label_obj.label, ft.Container) and isinstance(label_obj.label.content, ft.Text):
                        self.text_controls[label_obj.label.content] = 'label'
        # Note: Left axis numeric labels are styled via labels_style, not individual controls in text_controls

    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati."""
        for control, size_category in self.text_controls.items():
            new_size = self.text_handler.get_size(size_category)
            if hasattr(control, 'size'):
                control.size = new_size
            # No need to update color here as it's handled by _update_chart_text_colors
            if hasattr(control, 'page') and control.page: # Guard update
                control.update()
        # Update left axis labels_size directly if needed, though title_size and labels_style are more common for axes
        if hasattr(self, 'chart_control') and self.chart_control:
            if self.chart_control.left_axis:
                # self.chart_control.left_axis.labels_size = self.text_handler.get_size('label') # Example if needed
                pass
            if self.chart_control.bottom_axis:
                # self.chart_control.bottom_axis.labels_size = self.text_handler.get_size('label') # Example if needed
                pass

    def build(self, lat=None, lon=None):
        # Store the container for potential updates (e.g. gradient)
        self.container_control = ft.Container(
            border_radius=15,
            padding=30,
            # Create chart content. lat, long are used here.
            content=self.createAirPollutionChart(lat, lon), 
        )
        return self.container_control

    def cleanup(self):
        """Unregister observers to prevent memory leaks."""
        if hasattr(self, '_state_manager') and self._state_manager:
            self._state_manager.unregister_observer("theme_event", self._handle_state_change)
            self._state_manager.unregister_observer("language_event", self._handle_state_change)
        # print("AirPollutionChart cleaned up") # For debugging