"""
Main application file for the MeteoApp.
"""

import flet as ft # MODIFIED: Use standard alias 'ft'
import logging


from utils.config import (DARK_THEME, DEFAULT_CITY, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM, DEFAULT_THEME_MODE, LIGHT_THEME)
from layout.layout_manager import LayoutManager
from layout.sidebar.sidebar_manager import SidebarManager
from services.api_service import ApiService
from state_manager import StateManager
from services.geolocation_service import GeolocationService
from services.location_toggle_service import LocationToggleService
from services.theme_toggle_service import ThemeToggleService
from services.translation_service import TranslationService # Add this import
from ui.weather_view import WeatherView
from ui.charts_view import ChartsView # Add import for ChartsView

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class MeteoApp:

    def __init__(self):
        self.page = None
        self.api_service = ApiService()
        self.geolocation_service = GeolocationService()
        self.state_manager = None
        self.location_toggle_service = None
        self.theme_toggle_service = None
        self.sidebar_container = None
        self.info_container_wrapper = None
        self.hourly_container_wrapper = None
        self.chart_container_wrapper = None
        self.air_pollution_chart_container_wrapper = None # Add air pollution chart container wrapper
        self.precipitation_chart_container_wrapper = None # For precipitation chart
        self.air_pollution_container_wrapper = None
        self.layout_manager = None
        self.weather_view_instance = None # Add to store WeatherView instance
        self.charts_view_instance = None # Add to store ChartsView instance
        self.translation_service = None # Add to store TranslationService instance

    def _update_container_colors(self, event_data=None):
        """Aggiorna solo i colori dei container principali e dei testi senza ricostruire i container."""
        if not self.page:
            return
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME
        
        # Helper function to safely update container
        def safe_update_container(container, color_key):
            if container:
                try:
                    container.bgcolor = theme.get(color_key)
                    container.update()
                except AssertionError:
                    # Container not yet properly connected to page
                    pass
        
        # Aggiorna colori specifici per ogni container
        safe_update_container(self.sidebar_container, "SIDEBAR")
        
        if self.info_container_wrapper:
            try:
                # Applica gradiente se definito nel tema
                if "INFO_GRADIENT" in theme:
                    gradient_start = theme["INFO_GRADIENT"]["start"]
                    gradient_end = theme["INFO_GRADIENT"]["end"]
                    self.info_container_wrapper.gradient = ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=[gradient_start, gradient_end]
                    )
                    self.info_container_wrapper.bgcolor = None
                else:
                    self.info_container_wrapper.bgcolor = theme.get("CARD_BACKGROUND")
                    self.info_container_wrapper.gradient = None
                self.info_container_wrapper.update()
            except AssertionError:
                # Container not yet properly connected to page
                pass
        
        safe_update_container(self.hourly_container_wrapper, "HOURLY")
        safe_update_container(self.chart_container_wrapper, "CHART")
        safe_update_container(self.precipitation_chart_container_wrapper, "CHART") # For precipitation chart
        safe_update_container(self.air_pollution_chart_container_wrapper, "CHART") # For air pollution chart
        safe_update_container(self.air_pollution_container_wrapper, "CARD_BACKGROUND")
        safe_update_container(self.air_condition_container_wrapper, "CARD_BACKGROUND")
        
        # Aggiorna il colore di sfondo della pagina
        self.page.bgcolor = theme.get("BACKGROUND")
        try:
            self.page.update()
        except Exception:
            # Page not ready for update
            pass

    async def main(self, page: ft.Page) -> None: # MODIFIED: ft.Page
        """
        Main entry point for the application.
        
        Args:
            page: Flet page object
        """
        self.page = page # Store page reference
        # Set page properties
        page.title = "MeteoOGGI - Il tuo meteo giornaliero"
        page.theme_mode = (ft.ThemeMode.LIGHT if DEFAULT_THEME_MODE == "light" else ft.ThemeMode.DARK) # MODIFIED: ft.ThemeMode
        page.adaptive = True
        page.scroll = ft.ScrollMode.AUTO # MODIFIED: ft.ScrollMode
        page.animation_duration = 500 # Add animation duration for page-level animations

        self.state_manager = StateManager(page)
        # Salva lo state_manager nella sessione per accedervi da altre parti dell'app
        page.session.set('state_manager', self.state_manager)
        
        # Initialize TranslationService
        self.translation_service = TranslationService()
        page.session.set('translation_service', self.translation_service) # Optionally store in session

        # Register theme update handler for containers
        self.state_manager.register_observer("theme_event", self._update_container_colors)

        self.weather_view_instance = WeatherView(page, self.api_service) # Store instance
        
        info_container, hourly_container, chart_container, air_pollution_container, air_pollution_chart_container, precipitation_chart_container = self.weather_view_instance.get_containers() # Get all containers including both charts
        
        # Create a method to get air condition components once weather data is loaded
        def get_air_condition_components():
            return self.weather_view_instance.get_air_condition_components()
        
        # Store the getter function for later use
        self.get_air_condition_components = get_air_condition_components
        
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
            api_service=self.api_service,
            state_manager=self.state_manager,
            location_toggle_service=self.location_toggle_service,
            theme_toggle_service=self.theme_toggle_service,
            update_weather_callback=self.update_weather_with_sidebar # Use unified callback
        )
        
        # Ottieni l'istanza della sidebar dal gestore
        # sidebar = self.sidebar_manager.initialize_sidebar() # Vecchio modo
        # Ora SidebarManager è esso stesso il componente sidebar da aggiungere al layout
        sidebar_control = self.sidebar_manager # SidebarManager è ora un ft.Container

        
        # Le funzioni di gestione della posizione e del cambio città sono state spostate nei rispettivi servizi
          # Inizializza il layout manager
        self.layout_manager = LayoutManager(page)
        
        # Crea i contenitori del layout
        self.layout_manager.create_containers(
            sidebar_content=sidebar_control, # Usa l'istanza di SidebarManager
            info_content=info_container,
            hourly_content=hourly_container,
            chart_content=chart_container,
            precipitation_chart_content=precipitation_chart_container, # For precipitation chart
            air_pollution_chart_content=air_pollution_chart_container, # For air pollution chart
            air_pollution_content=air_pollution_container
        )
        
        # Memorizza riferimenti ai contenitori per la loro gestione
        containers = self.layout_manager.get_all_containers()
        self.sidebar_container = containers['sidebar']
        self.info_container_wrapper = containers['info']
        self.hourly_container_wrapper = containers['hourly']
        self.chart_container_wrapper = containers['chart']
        self.precipitation_chart_container_wrapper = containers['precipitation_chart'] # For precipitation chart
        self.air_pollution_chart_container_wrapper = containers['air_pollution_chart'] # For air pollution chart
        self.air_pollution_container_wrapper = containers['air_pollution']
        self.air_condition_container_wrapper = containers.get('air_condition')  # New air condition container
        
        # Costruisce e aggiunge il layout alla pagina
        page.add(self.layout_manager.build_layout())
        
        # Assicuriamoci che lo StateManager sia correttamente inizializzato
        await self.state_manager.set_state("language", DEFAULT_LANGUAGE)
        await self.state_manager.set_state("unit", DEFAULT_UNIT_SYSTEM)
        await self.state_manager.set_state("city", DEFAULT_CITY)


        await self.update_weather_with_sidebar( # Use unified method
            city=self.state_manager.get_state("city") or DEFAULT_CITY,
            language= self.state_manager.get_state("language") or DEFAULT_LANGUAGE,
            unit= self.state_manager.get_state("unit") or DEFAULT_UNIT_SYSTEM
        )

        # Initial update of container colors (after everything is loaded)
        self._update_container_colors()

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
        if page.platform == ft.PagePlatform.WINDOWS or page.platform == ft.PagePlatform.LINUX or page.platform == ft.PagePlatform.MACOS: # MODIFIED: ft.PagePlatform
            async def window_event_handler(e):
                if e.data == "close": # Or other relevant events like 'destroy'
                    await on_disconnect_or_close(e)
            page.on_window_event = window_event_handler


    async def update_weather_with_sidebar(self, city: str, language: str, unit: str):
        """Update both main weather view and sidebar weekly forecast."""
        print(f"DEBUG: update_weather_with_sidebar called with city: {city}, language: {language}, unit: {unit}")
        
        # Update main weather view
        result = await self.weather_view_instance.update_by_city(city, language, unit)
        print(f"DEBUG: Main weather view updated for city: {city}")
        
        # Update charts view if it exists
        if self.charts_view_instance:
            await self.charts_view_instance.update_by_city(city, language, unit)
            print(f"DEBUG: Charts view updated for city: {city}")
        
        # Update layout with separated air condition components after weather data is updated
        air_condition_components = self.get_air_condition_components()
        if air_condition_components and self.layout_manager:
            self.layout_manager.update_air_condition_layout(air_condition_components)
            print("DEBUG: Air condition layout updated with separated components")
        else:
            # Schedule an update for after the first render
            def delayed_update():
                air_condition_components = self.get_air_condition_components()
                if air_condition_components and self.layout_manager:
                    self.layout_manager.update_air_condition_layout(air_condition_components)
                    print("DEBUG: Air condition layout updated with separated components (delayed)")
            
            # Schedule the delayed update
            if self.page:
                self.page.run_task(lambda: delayed_update())
        
        # Update sidebar weekly forecast
        if self.sidebar_manager:
            self.sidebar_manager.update_weekly_forecast(city)
            print(f"DEBUG: Sidebar weekly forecast updated for city: {city}")
        
        return result

def main():
    """Entry point for the application"""
    app = MeteoApp()
    ft.app( # MODIFIED: ft.app
        target=app.main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER # MODIFIED: ft.AppView
    )


if __name__ == "__main__":
    main()
