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

from layout.frontend.sidebar.sidebar import Sidebar  
from state_manager import StateManager
from services.geolocation_service import GeolocationService
from services.location_toggle_service import LocationToggleService
from services.theme_toggle_service import ThemeToggleService
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
        self.location_toggle_service = None
        self.theme_toggle_service = None

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
        # Salva lo state_manager nella sessione per accedervi da altre parti dell'app
        page.session.set('state_manager', self.state_manager)
        weather_view = WeatherView(page)
        info_container, weekly_container, chart_container, air_pollution_container, air_pollution_chart_container = weather_view.get_containers()
        
        # Inizializza il servizio di location toggle
        self.location_toggle_service = LocationToggleService(
            page=page,
            geolocation_service=self.geolocation_service,
            state_manager=self.state_manager,
            update_weather_callback=weather_view.update_by_coordinates
        )
        
        # Inizializza il servizio di theme toggle
        self.theme_toggle_service = ThemeToggleService(
            page=page,
            state_manager=self.state_manager
        )

        async def handle_city_change(city: str):
            """Callback per il cambio città."""
            try:
                # Aggiorna lo stato: quando si seleziona una città, disabilita la localizzazione
                await self.state_manager.update_state({
                    "city": city,
                    "using_location": False
                })
                
                # Aggiorna la UI: se esiste l'istanza della sidebar, aggiorna il toggle
                if hasattr(sidebar, 'update_location_toggle'):
                    sidebar.update_location_toggle(False)
                
                # Aggiorna la visualizzazione del meteo con la città selezionata
                await weather_view.update_by_city(
                    city=city,
                    language=self.state_manager.get_state("language"),
                    unit=self.state_manager.get_state("unit")
                )
                
                logging.info(f"Città cambiata: {city}, localizzazione disattivata")
            except Exception as e:
                logging.error(f"Errore nel cambio città: {e}")

        # Le funzioni di gestione della posizione sono state spostate nel LocationToggleService

        sidebar = Sidebar(
            page=page, 
            on_city_selected=handle_city_change,
            handle_location_toggle=self.location_toggle_service.handle_location_toggle,
            location_toggle_value=self.state_manager.get_state("using_location") or False,
            handle_theme_toggle=self.theme_toggle_service.handle_theme_toggle,
            theme_toggle_value=self.state_manager.get_state("using_theme") or False
        )

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

        # Inizializza il tracking della posizione
        await self.location_toggle_service.initialize_tracking()
        
        # Inizializza il tema dell'applicazione
        await self.theme_toggle_service.initialize_theme()


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
