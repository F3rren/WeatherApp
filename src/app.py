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

from layout.backend.sidebar.sidebar import Sidebar
from layout.frontend.sidebar.location_toggle import LocationToggle
from state_manager import StateManager
from services.geolocation_service import GeolocationService
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
        self.state_manager = None

    async def main(self, page: ft.Page) -> None:
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

        self.state_manager = StateManager(page)
        weather_view = WeatherView(page)
        info_container, weekly_container, chart_container, air_pollution_container, air_pollution_chart_container = weather_view.get_containers()

        # Create location toggle first so it's available in callbacks
        location_toggle = LocationToggle(
            on_change=None,  # Temporarily None, will set after definition
            value=False
        )

        async def handle_city_change(city: str):
            """Callback per il cambio città."""
            try:
                await self.state_manager.update_state({
                    "city": city,
                    "using_location": False
                })
                await weather_view.update_by_city(
                    city=city,
                    language=self.state_manager.get_state("language"),
                    unit=self.state_manager.get_state("unit")
                )
                if location_toggle.value:
                    location_toggle.value = False
                    page.update()
            except Exception as e:
                logging.error(f"Errore nel cambio città: {e}")

        async def handle_location_change(lat_lon):
            """Callback per il cambio posizione."""
            try:
                lat, lon = lat_lon
                await self.state_manager.update_state({
                    "current_lat": lat,
                    "current_lon": lon
                })
                if self.state_manager.get_state("using_location"):
                    await weather_view.update_by_coordinates(
                        lat=lat,
                        lon=lon,
                        language=self.state_manager.get_state("language"),
                        unit=self.state_manager.get_state("unit")
                    )
            except Exception as e:
                logging.error(f"Errore nel cambio posizione: {e}")

        async def handle_location_toggle(e: ft.ControlEvent):
            """Callback per il toggle della posizione."""
            try:
                using_location = e.control.value
                await self.state_manager.set_state("using_location", using_location)
                if using_location:
                    if self.geolocation_service.has_coordinates:
                        lat, lon = self.geolocation_service.current_coordinates
                        await weather_view.update_by_coordinates(
                            lat=lat,
                            lon=lon,
                            language=self.state_manager.get_state("language"),
                            unit=self.state_manager.get_state("unit")
                        )
                        self.geolocation_service.set_location_callback(handle_location_change)
                    else:
                        success = await self.geolocation_service.start_tracking(
                            page=page,
                            on_location_change=handle_location_change
                        )
                        if not success:
                            e.control.value = False
                            page.update()
                else:
                    self.geolocation_service.set_location_callback(None)
            except Exception as ex:
                logging.error(f"Errore nel toggle posizione: {ex}")

        # Set the callback now that it's defined
        location_toggle.on_change = handle_location_toggle

        sidebar = Sidebar(page, on_city_selected=handle_city_change)

        def build_layout():
            return ft.ListView(
                expand=True,
                spacing=10,
                auto_scroll=True,
                controls=[
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
                                border_radius=15
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=info_container,
                                col={"xs": 12},
                                margin=10,
                                padding=10,
                                border_radius=15
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=weekly_container,
                                col={"xs": 8},
                                margin=10,
                                padding=10,
                                border_radius=15
                            ),
                            ft.Container(
                                content=chart_container,
                                col={"xs": 4},
                                margin=10,
                                padding=10,
                                border_radius=15
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=air_pollution_chart_container,
                                col={"xs": 7},
                                margin=10,
                                padding=10,
                                border_radius=15
                            ),
                            ft.Container(
                                content=air_pollution_container,
                                col={"xs": 5},
                                margin=10,
                                padding=10,
                                border_radius=15
                            )
                        ]
                    )
                ]
            )

        page.add(build_layout())

        await weather_view.update_by_city(
            city=DEFAULT_CITY,
            language=DEFAULT_LANGUAGE,
            unit=DEFAULT_UNIT
        )

        try:
            success = await self.geolocation_service.start_tracking(
                page=page,
                on_location_change=None
            )
            if success:
                lat, lon = await self.geolocation_service.get_current_location(page)
                if lat and lon:
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
