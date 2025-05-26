"""
Main application file for the MeteoApp.
"""

import flet as ft
import logging

from config import (
    DEFAULT_CITY,
    DEFAULT_LANGUAGE,
    DEFAULT_UNIT,
    DEFAULT_THEME_MODE
)
from ui.components import LocationToggle
from state_manager import StateManager
from services.geolocation_service import GeolocationService
from layout.backEnd.sidebar.sidebar import Sidebar
from ui.weather_view import WeatherView

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class MeteoApp:
    """
    Main application class for the MeteoApp.
    """
    
    def __init__(self):
        self.geolocation_service = GeolocationService()
    
    async def main(self, page: ft.Page):
        """
        Main entry point for the application.
        
        Args:
            page: Flet page object
        """
        # Set page properties
        page.title = "MeteoApp"
        page.theme_mode = (
            ft.ThemeMode.LIGHT if DEFAULT_THEME_MODE == "light" else ft.ThemeMode.DARK
        )
        page.adaptive = True
        page.scroll = ft.ScrollMode.AUTO
        
        # Create state manager
        self.state_manager = StateManager(page)
        
        # Create weather view
        weather_view = WeatherView(page)
        info_container, weekly_container, chart_container, air_pollution_container, air_pollution_chart_container = weather_view.get_containers()
        
        # Handle city change
        async def handle_city_change(city):
            # Update state
            await self.state_manager.update_state({
                "city": city,
                "using_location": False
            })
            
            # Update weather view
            await weather_view.update_by_city(
                city=city,
                language=self.state_manager.get_state("language"),
                unit=self.state_manager.get_state("unit")
            )
            
            # Update location toggle
            if location_toggle.value:
                location_toggle.value = False
                page.update()
        
        # Handle location change
        async def handle_location_change(lat_lon):
            lat, lon = lat_lon
            
            # Update state
            await self.state_manager.update_state({
                "current_lat": lat,
                "current_lon": lon
            })
            
            # Update weather view if using location
            if self.state_manager.get_state("using_location"):
                await weather_view.update_by_coordinates(
                    lat=lat,
                    lon=lon,
                    language=self.state_manager.get_state("language"),
                    unit=self.state_manager.get_state("unit")
                )
        
        # Handle location toggle
        async def handle_location_toggle(e):
            using_location = e.control.value
            
            # Update state
            await self.state_manager.set_state("using_location", using_location)
            
            if using_location:
                # If we have coordinates, use them
                if self.geolocation_service.has_coordinates:
                    lat, lon = self.geolocation_service.current_coordinates
                    
                    # Update weather view
                    await weather_view.update_by_coordinates(
                        lat=lat,
                        lon=lon,
                        language=self.state_manager.get_state("language"),
                        unit=self.state_manager.get_state("unit")
                    )
                    
                    # Set location callback
                    self.geolocation_service.set_location_callback(handle_location_change)
                else:
                    # Start tracking location
                    success = await self.geolocation_service.start_tracking(
                        page=page,
                        on_location_change=handle_location_change
                    )
                    
                    if not success:
                        # If tracking failed, reset toggle
                        e.control.value = False
                        page.update()
            else:
                # Remove location callback
                self.geolocation_service.set_location_callback(None)
        
        # Create sidebar
        sidebar = Sidebar(page, on_city_selected=handle_city_change)
        
        # Create location toggle
        location_toggle = LocationToggle(
            on_change=handle_location_toggle,
            value=False
        )
        #location_toggle_row = location_toggle.build()
        
        # Create layout
        page.add(
            ft.ListView(
                expand=True,
                spacing=10,
                #padding=20,
                auto_scroll=True,
                controls=[
                    # Header row with sidebar and location toggle
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=ft.Column([
                                    sidebar.build(),
                                    location_toggle.build()
                                ]), 
                                col={"xs": 12},
                                margin=10,
                                padding=10,
                                border_radius=15,
                                #bgcolor=ft.Colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.PURPLE_100
                            )
                        ],
                        #spacing=20
                    ),
                    # Main content row
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=info_container, 
                                col={"xs": 12},
                                margin=10,
                                padding=10,
                                border_radius=15,
                                #bgcolor=ft.Colors.BLUE_GREY_900 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_100
                            ),
                        ],
                        #spacing=20
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=weekly_container, 
                                col={"xs": 8},
                                margin=10,
                                padding=10,
                                border_radius=15,
                                #bgcolor=ft.Colors.INDIGO_900 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.INDIGO_100
                            ),
                            ft.Container(
                                content=chart_container, 
                                col={"xs": 4},
                                margin=10,
                                padding=10,
                                border_radius=15,
                                #bgcolor=ft.Colors.TEAL_900 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.TEAL_100
                            ),  
                        ],
                        #spacing=20
                    ),
                    # Chart row
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=air_pollution_chart_container, 
                                col={"xs": 7},
                                margin=10,
                                padding=10,
                                border_radius=15,
                                #bgcolor=ft.Colors.TEAL_900 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.TEAL_100
                            ),                      
                            ft.Container(
                                content=air_pollution_container, 
                                col={"xs": 5},
                                margin=10,
                                padding=10,
                                border_radius=15,
                                #bgcolor=ft.Colors.TEAL_900 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.TEAL_100
                            ),    
                        ],
                        #spacing=20
                    ),
                           
                ]
            )
        )
        
        # Load default city
        await weather_view.update_by_city(
            city=DEFAULT_CITY,
            language=DEFAULT_LANGUAGE,
            unit=DEFAULT_UNIT
        )
        
        # Start location tracking in background
        try:
            # Start tracking but without UI updates
            success = await self.geolocation_service.start_tracking(
                page=page,
                on_location_change=None
            )
            
            if success:
                # Get initial coordinates
                lat, lon = await self.geolocation_service.get_current_location(page)
                if lat and lon:
                    # Store coordinates in state
                    await self.state_manager.update_state({
                        "current_lat": lat,
                        "current_lon": lon
                    })
            else:
                logging.warning("Failed to start location tracking")
        except Exception as e:
            logging.error(f"Error initializing geolocation: {e}")


def main():
    """Entry point for the application"""
    app = MeteoApp()
    ft.app(
        target=app.main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER
    )


if __name__ == "__main__":
    main()
