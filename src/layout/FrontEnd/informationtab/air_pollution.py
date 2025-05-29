import flet as ft
from layout.backend.air_pollution_operation import AirPollutionOperation
from config import LIGHT_THEME, DARK_THEME # Import theme configurations

class AirPollution:
    """
    Air pollution display component.
    Shows detailed air quality information.
    """
    
    def __init__(self, page, lat=None, lon=None, text_color: str = None): # Added text_color
        """
        Initialize the AirPollution component.
        
        Args:
            page: Flet page object
            lat: Latitude (optional)
            lon: Longitude (optional)
            text_color: Initial text color (optional)
        """
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
        
        # Get gradient based on theme mode
        # self.gradient = self._get_gradient() # Gradient seems unused, can be removed or reimplemented if needed

        # Update data if coordinates are provided
        if lat is not None and lon is not None:
            self.update_data(lat, lon)

        # Register for theme change events
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_change)

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color and relevant UI elements."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]
            
            # Update text colors of the dynamically created text controls
            # This requires re-building or having references to the text controls.
            # For simplicity, we'll assume the parent will trigger a rebuild or update.
            # If direct update is needed, store references to text controls during creation.
            if self.page: # Trigger a page update to reflect changes if controls are rebuilt
                # self.page.update() # This might be too broad, ideally update specific controls
                # For now, we rely on WeatherView to refresh this component
                pass 

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


    def update_data(self, lat, lon):
        """
        Update air pollution data with new coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
        """
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
    
    def _get_aqi_description(self) -> str:
        """Get description based on Air Quality Index"""
        descriptions = [
            "N/A",
            "Good",
            "Fair",
            "Moderate",
            "Poor",
            "Very Poor"
        ]
        return descriptions[min(self.aqi, 5)]
    
    def _get_aqi_color(self) -> str:
        """Get color based on Air Quality Index"""
        colors = [
            "#808080",  # Gray for N/A
            "#00E400",  # Green for Good
            "#FFFF00",  # Yellow for Fair
            "#FF7E00",  # Orange for Moderate
            "#FF0000",  # Red for Poor
            "#99004C"   # Purple for Very Poor
        ]
        return colors[min(self.aqi, 5)]
    
    def createAirPollutionTab(self):
        """Create the air pollution tab content"""
        # AQI indicator
        aqi_row = ft.Row([
            ft.Text("Air Quality Index:", size=20, weight="bold", color=self.text_color), # Apply text_color
            ft.Container(
                content=ft.Text(
                    self._get_aqi_description(),
                    size=20,
                    weight="bold",
                    color=self.text_color if self.aqi <= 2 else "#ffffff" # AQI desc color logic
                ),
                bgcolor=self._get_aqi_color(),
                border_radius=10,
                padding=10,
                alignment=ft.alignment.center,
                expand=True
            )
        ])
        
        # Create pollution data rows
        pollution_data = [
            ("CO", self.co, "μg/m³", "Carbon monoxide"),
            ("NO", self.no, "μg/m³", "Nitrogen monoxide"),
            ("NO₂", self.no2, "μg/m³", "Nitrogen dioxide"),
            ("O₃", self.o3, "μg/m³", "Ozone"),
            ("SO₂", self.so2, "μg/m³", "Sulphur dioxide"),
            ("PM2.5", self.pm2_5, "μg/m³", "Fine particles"),
            ("PM10", self.pm10, "μg/m³", "Coarse particles"),
            ("NH₃", self.nh3, "μg/m³", "Ammonia")
        ]
        
        pollution_rows = []
        
        # Create rows with 2 items per row
        for i in range(0, len(pollution_data), 2):
            row_items = []
            
            # Add first item
            name1, value1, unit1, desc1 = pollution_data[i]
            row_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(name1, weight="bold", size=16, color=self.text_color), # Apply text_color
                        ft.Text(f"{value1} {unit1}", size=14, color=self.text_color), # Apply text_color
                        ft.Text(desc1, size=12, color=self.text_color, italic=True), # Apply text_color
                    ]),
                    padding=10,
                    border_radius=10,
                    #bgcolor=ft.colors.with_opacity(0.1, self.txtcolor), # Example: theme aware bg
                    expand=True
                )
            )
            
            # Add second item if exists
            if i + 1 < len(pollution_data):
                name2, value2, unit2, desc2 = pollution_data[i+1]
                row_items.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(name2, weight="bold", size=16, color=self.text_color), # Apply text_color
                            ft.Text(f"{value2} {unit2}", size=14, color=self.text_color), # Apply text_color
                            ft.Text(desc2, size=12, color=self.text_color, italic=True), # Apply text_color
                        ]),
                        padding=10,
                        border_radius=10,
                        #bgcolor=ft.colors.with_opacity(0.1, self.txtcolor),
                        expand=True
                    )
                )
            pollution_rows.append(ft.Row(row_items, spacing=10))

        return ft.Column(
            controls=[
                aqi_row,
                ft.Divider(height=20, color=self.text_color), # Apply text_color to divider
                *pollution_rows
            ],
            spacing=10,
            #expand=True # remove expand true if it causes issues
        )
    
    def build(self):
        """Build the air pollution component"""
        return ft.Container(
            #gradient=self.gradient,
            border_radius=15,
            padding=20,
            content=self.createAirPollutionTab(),
        )
