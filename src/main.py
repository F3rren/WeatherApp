"""
Main application file for the MeteoApp.
"""

import flet as ft
import logging

from utils.config import (DEFAULT_CITY, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM, DEFAULT_THEME_MODE)

from layout.frontend.layout_manager import LayoutManager
from layout.frontend.sidebar.sidebar_manager import SidebarManager
from state_manager import StateManager
from services.geolocation_service import GeolocationService
from services.location_toggle_service import LocationToggleService
from services.theme_toggle_service import ThemeToggleService
from services.translation_service import TranslationService # Add this import
from ui.weather_view import WeatherView

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class MeteoApp:

    def __init__(self):
        self.geolocation_service = GeolocationService()
        self.state_manager = None
        self.location_toggle_service = None
        self.theme_toggle_service = None
        self.sidebar_container = None
        self.info_container_wrapper = None
        self.weekly_container_wrapper = None
        self.chart_container_wrapper = None
        self.air_pollution_chart_container_wrapper = None
        self.air_pollution_container_wrapper = None
        self.page = None
        self.layout_manager = None
        self.weather_view_instance = None # Add to store WeatherView instance
        self.translation_service = None # Add to store TranslationService instance

    async def _update_container_colors(self, event_data=None):
        """Updates the background colors of main containers based on the theme."""
        if not self.page or not hasattr(self, 'layout_manager'):
            return
        # Delega l'aggiornamento dei colori al layout manager
        self.layout_manager.update_container_colors(self.page.theme_mode)

    async def main(self, page: ft.Page) -> None:
        """
        Main entry point for the application.
        
        Args:
            page: Flet page object
        """
        self.page = page # Store page reference
        # Set page properties
        page.title = "MeteoApp"
        page.theme_mode = (ft.ThemeMode.LIGHT if DEFAULT_THEME_MODE == "light" else ft.ThemeMode.DARK)
        page.adaptive = True
        page.scroll = ft.ScrollMode.AUTO
        page.animation_duration = 500 # Add animation duration for page-level animations

        self.state_manager = StateManager(page)
        # Salva lo state_manager nella sessione per accedervi da altre parti dell'app
        page.session.set('state_manager', self.state_manager)
        
        # Initialize TranslationService
        self.translation_service = TranslationService()
        page.session.set('translation_service', self.translation_service) # Optionally store in session

        # Register theme update handler for containers
        self.state_manager.register_observer("theme_event", self._update_container_colors)

        self.weather_view_instance = WeatherView(page) # Store instance
        info_container, weekly_container, chart_container, air_pollution_container, air_pollution_chart_container = self.weather_view_instance.get_containers()
        
        # Inizializza il servizio di location toggle
        self.location_toggle_service = LocationToggleService(
            page=page,
            geolocation_service=self.geolocation_service,
            state_manager=self.state_manager,
            update_weather_callback=self.weather_view_instance.update_by_coordinates # Use instance
        )
        
        # Inizializza il servizio di theme toggle
        self.theme_toggle_service = ThemeToggleService(
            page=page, state_manager=self.state_manager
        )
        # Inizializzazione del gestore della sidebar
        self.sidebar_manager = SidebarManager(
            page=page,
            state_manager=self.state_manager,
            location_toggle_service=self.location_toggle_service,
            theme_toggle_service=self.theme_toggle_service,
            update_weather_callback=self.weather_view_instance.update_by_city # Use instance
        )
        
        # Ottieni l'istanza della sidebar dal gestore
        sidebar = self.sidebar_manager.initialize_sidebar()
        
        # Le funzioni di gestione della posizione e del cambio città sono state spostate nei rispettivi servizi
          # Inizializza il layout manager
        self.layout_manager = LayoutManager(page)
        
        # Crea i contenitori del layout
        self.layout_manager.create_containers(
            sidebar_content=sidebar,
            info_content=info_container,
            weekly_content=weekly_container,
            chart_content=chart_container,
            air_pollution_chart_content=air_pollution_chart_container,
            air_pollution_content=air_pollution_container
        )
        
        # Memorizza riferimenti ai contenitori per la loro gestione
        containers = self.layout_manager.get_all_containers()
        self.sidebar_container = containers['sidebar']
        self.info_container_wrapper = containers['info']
        self.weekly_container_wrapper = containers['weekly']
        self.chart_container_wrapper = containers['chart']
        self.air_pollution_chart_container_wrapper = containers['air_pollution_chart']
        self.air_pollution_container_wrapper = containers['air_pollution']
        
        # Costruisce e aggiunge il layout alla pagina
        page.add(self.layout_manager.build_layout())
        
        # Initial update of container colors
        await self._update_container_colors()

        await self.weather_view_instance.update_by_city( # Use instance
            city=DEFAULT_CITY,
            language=DEFAULT_LANGUAGE,
            unit=DEFAULT_UNIT_SYSTEM
        )

        # Inizializza il tracking della posizione
        await self.location_toggle_service.initialize_tracking()
        
        # Inizializza il tema dell'applicazione
        await self.theme_toggle_service.initialize_theme()

        # Register cleanup function for page disconnect or window close
        async def on_disconnect_or_close(e):
            logging.info("Page disconnected or window closed, performing cleanup...")
            if self.weather_view_instance:
                self.weather_view_instance.cleanup()
            if self.state_manager:
                # Potentially unregister other global observers if any were set directly on state_manager here
                pass # No other global observers to unregister from MeteoApp directly for now
            logging.info("Cleanup complete.")

        page.on_disconnect = on_disconnect_or_close
        # For desktop, on_window_event might be more reliable for cleanup before exit
        if page.platform == ft.PagePlatform.WINDOWS or page.platform == ft.PagePlatform.LINUX or page.platform == ft.PagePlatform.MACOS:
            async def window_event_handler(e):
                if e.data == "close": # Or other relevant events like 'destroy'
                    await on_disconnect_or_close(e)
            page.on_window_event = window_event_handler


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
