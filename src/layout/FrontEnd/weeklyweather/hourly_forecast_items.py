import flet as ft
from datetime import datetime
from config import LIGHT_THEME, DARK_THEME

class HourlyForecastDisplay:
    """
    Manages the display of the entire hourly forecast section, 
    including generating each item and arranging them in a scrollable row.
    """
    def __init__(self, hourly_data: list, text_color: str, page: ft.Page):
        self.hourly_data_list = hourly_data
        self.text_color = text_color
        self.page = page
        self.built_item_containers = [] # To store references to individual item containers
        self.main_container_ref = None # To store reference to the main container

        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                state_manager.register_observer("theme_event", self.handle_theme_change)

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color and item backgrounds."""
        if not self.page:
            return

        if event_data and "is_dark" in event_data:
            is_dark = event_data["is_dark"]
        else:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            
        current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
        
        self.text_color = current_theme_config["TEXT"]
        new_item_bgcolor = current_theme_config["HOURLY_FORECAST_CARD"] # Use config color for both themes

        if hasattr(self, 'built_item_containers') and self.built_item_containers:
            for item_container in self.built_item_containers:
                item_container.bgcolor = new_item_bgcolor
                
                # item_container.content is the ft.Column
                if isinstance(item_container.content, ft.Column) and item_container.content.controls:
                    column_controls = item_container.content.controls
                    # Update text color for ft.Text elements
                    if len(column_controls) > 0 and isinstance(column_controls[0], ft.Text): # Time text
                        column_controls[0].color = self.text_color
                    if len(column_controls) > 2 and isinstance(column_controls[2], ft.Text): # Temperature text
                        column_controls[2].color = self.text_color
                
                item_container.update()
        
        # Update the main HourlyForecastDisplay container's background
        if hasattr(self, 'built_item_containers') and self.built_item_containers:
            self.built_item_containers.bgcolor = current_theme_config.get("HOURLY_FORECAST_CARD",) 
            self.built_item_containers.update()

    def _create_item_column(self, item_data: dict) -> ft.Container:
        """Helper method to create a single forecast item's visual representation."""
        time_str = datetime.strptime(item_data["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
        icon = item_data["weather"][0]["icon"]
        temp = round(item_data["main"]["temp"])
        
        item_bgcolor = DARK_THEME["HOURLY_FORECAST_CARD"] if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["HOURLY_FORECAST_CARD"]

        return ft.Container(
            bgcolor=item_bgcolor,
            content=ft.Column(
                controls=[
                    ft.Text(time_str, size=20, weight=ft.FontWeight.BOLD, color=self.text_color),
                    ft.Image(
                        src=f"https://openweathermap.org/img/wn/{icon}@2x.png",
                        width=100,
                        height=100,
                    ),
                    ft.Text(f"{temp}°", size=20, weight=ft.FontWeight.BOLD, color=self.text_color)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border_radius=20,
            expand=True,
        )

    def build(self) -> ft.Container:
        """Builds the hourly forecast container with a scrollable row of items."""
        self.built_item_containers.clear() # Clear previous items if any (e.g., on a rebuild)
        
        if self.hourly_data_list:
            for item_data in self.hourly_data_list:
                item_container = self._create_item_column(item_data)
                self.built_item_containers.append(item_container)
        
        self.main_container_ref = ft.Container(
            content=ft.Row(
                controls=self.built_item_containers, # Use the stored list
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Keep items spaced out
            ),
            expand=True,
            padding=ft.padding.symmetric(vertical=10), # Restore padding
            
        )
        return self.main_container_ref
