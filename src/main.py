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
        self.precipitation_chart_container_wrapper = None
        self.air_pollution_container_wrapper = None
        self.air_condition_container_wrapper = None
        self.layout_manager = None
        self.weather_view_instance = None 
        self.charts_view_instance = None 
        self.translation_service = None 

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
        safe_update_container(self.air_pollution_container_wrapper, "CARD_BACKGROUND")
        # Rimosso air_condition_container_wrapper perché ora è incluso nel info_container
        
        # Aggiorna il colore di sfondo della pagina
        self.page.bgcolor = theme.get("BACKGROUND")
        try:
            self.page.update()
        except Exception:

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
        # Salva anche il riferimento all'app principale per permettere l'accesso al layout manager
        page.session.set('main_app', self)
        
        # Initialize TranslationService
        self.translation_service = TranslationService()
        page.session.set('translation_service', self.translation_service) # Optionally store in session

        # Register theme update handler for containers
        self.state_manager.register_observer("theme_event", self._update_container_colors)

        self.weather_view_instance = WeatherView(page, self.api_service) # Store instance
        
        self.location_toggle_service = LocationToggleService(
            page=page,
            geolocation_service=self.geolocation_service,
            state_manager=self.state_manager,
            update_weather_callback=self.update_weather_with_sidebar # Imposta il callback
        )
        self.theme_toggle_service = ThemeToggleService(
            page=page, 
            state_manager=self.state_manager
        )
        self.sidebar_manager = SidebarManager(
            page=page,
            api_service=self.api_service,
            state_manager=self.state_manager,
            location_toggle_service=self.location_toggle_service,
            theme_toggle_service=self.theme_toggle_service,
            update_weather_callback=self.update_weather_with_sidebar # Imposta il callback
        )
        
        self.layout_manager = LayoutManager(page)
        
        await self.build_layout()

    async def build_layout(self):
        """Costruisce e aggiunge il layout alla pagina, inizializza stato e servizi."""
        # FASE 1: Inizializza stato e carica i dati meteo PRIMA di costruire il layout
        await self.state_manager.set_state("language", DEFAULT_LANGUAGE)
        await self.state_manager.set_state("unit", DEFAULT_UNIT_SYSTEM)
        await self.state_manager.set_state("city", DEFAULT_CITY)
        
        logging.info("DEBUG: [build_layout] Caricamento dati meteo PRIMA della costruzione del layout...")
        await self.update_weather_with_sidebar(
            city=self.state_manager.get_state("city") or DEFAULT_CITY,
            language=self.state_manager.get_state("language") or DEFAULT_LANGUAGE,
            unit=self.state_manager.get_state("unit") or DEFAULT_UNIT_SYSTEM
        )
        logging.info("DEBUG: [build_layout] Dati meteo caricati, ora costruisco il layout con container popolati...")

        # FASE 2: Ora recupera i container popolati dal WeatherView
        # Nota: air_condition è ora incluso nel info_container, quindi air_condition_container sarà vuoto
        info_container, air_condition_container, hourly_container, chart_container, precipitation_chart_container, air_pollution_container = self.weather_view_instance.get_containers()
        sidebar_control = self.sidebar_manager

        # Debug: Verifica che i container siano popolati
        logging.info(f"DEBUG: [build_layout] Container info popolato: {info_container.content is not None}")
        logging.info(f"DEBUG: [build_layout] Container air_condition popolato: {air_condition_container.content is not None}")
        logging.info(f"DEBUG: [build_layout] Container hourly popolato: {hourly_container.content is not None}")

        # FASE 3: Crea i container nel layout manager con i container già popolati
        self.layout_manager.create_containers(
            sidebar_content=sidebar_control,
            info_content=info_container,
            #air_condition_content=air_condition_container,
            hourly_content=hourly_container,
            chart_content=chart_container,
            precipitation_chart_content=precipitation_chart_container,
            air_pollution_content=air_pollution_container
        )

        # FASE 4: Recupera tutti i wrapper/container dal layout manager
        containers = self.layout_manager.get_all_containers()
        self.sidebar_container = containers.get('sidebar')
        self.info_container_wrapper = containers.get('info')
        # Rimosso air_condition_container_wrapper perché ora è incluso nel info_container
        self.hourly_container_wrapper = containers.get('hourly')
        self.chart_container_wrapper = containers.get('chart')
        self.precipitation_chart_container_wrapper = containers.get('precipitation_chart')
        self.air_pollution_container_wrapper = containers.get('air_pollution')

        # FASE 5: Costruisce e aggiunge il layout alla pagina
        self.page.controls.clear()
        layout = self.layout_manager.build_layout()
        self.page.add(layout)

        # FASE 6: Applica tema e inizializza servizi
        self._update_container_colors()
        await self.location_toggle_service.initialize_tracking()
        await self.theme_toggle_service.initialize_theme()

        # Debug finale: Verifica che il layout finale contenga dati
        logging.info("DEBUG: [build_layout] Layout costruito e aggiunto alla pagina")

        # Gestione eventi di chiusura/disconnessione
        async def on_disconnect_or_close(e):
            logging.info("Page disconnected or window closed, performing cleanup...")
            if self.weather_view_instance:
                self.weather_view_instance.cleanup()
            if self.state_manager:
                pass
            logging.info("Cleanup complete.")
        self.page.on_disconnect = on_disconnect_or_close
        if self.page.platform in [ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS]:
            async def window_event_handler(e):
                if e.data == "close":
                    await on_disconnect_or_close(e)
            self.page.on_window_event = window_event_handler


    async def update_weather_with_sidebar(self, city: str, language: str, unit: str):
        """Update both main weather view and sidebar weekly forecast."""
        logging.info(f"DEBUG: update_weather_with_sidebar called with city: {city}, language: {language}, unit: {unit}")
        
        # Aggiorna lo stato con la nuova città
        await self.state_manager.set_state("city", city)
        await self.state_manager.set_state("language", language)
        await self.state_manager.set_state("unit", unit)
        
        # Update main weather view
        result = await self.weather_view_instance.update_by_city(city, language, unit)
        logging.info(f"DEBUG: Main weather view updated for city: {city}")
        
        # Update charts view if it exists
        if self.charts_view_instance:
            await self.charts_view_instance.update_by_city(city, language, unit)
            logging.info(f"DEBUG: Charts view updated for city: {city}")

        # Update sidebar weekly forecast
        if self.sidebar_manager:
            self.sidebar_manager.update_weekly_forecast(city)
            logging.info(f"DEBUG: Sidebar weekly forecast updated for city: {city}")

        # AGGIORNAMENTO UI: I container del WeatherView si aggiornano automaticamente
        # Ora basta aggiornare i riferimenti nei wrapper del layout manager
        if hasattr(self, 'layout_manager') and self.layout_manager:
            try:
                # Recupera i container aggiornati dal WeatherView
                info_container, air_condition_container, hourly_container, chart_container, precipitation_chart_container, air_pollution_container = self.weather_view_instance.get_containers()
                
                # Aggiorna i riferimenti nei wrapper del layout manager
                if hasattr(self.layout_manager, 'update_containers'):
                    self.layout_manager.update_containers(
                        info_content=info_container,
                        air_condition_content=air_condition_container,
                        hourly_content=hourly_container,
                        chart_content=chart_container,
                        precipitation_chart_content=precipitation_chart_container,
                        air_pollution_content=air_pollution_container
                    )
                    logging.info("DEBUG: Layout manager containers updated")
                
                # IMPORTANTE: Forza l'aggiornamento dei wrapper container
                if self.info_container_wrapper:
                    self.info_container_wrapper.content = info_container.content
                    try:
                        self.info_container_wrapper.update()
                        logging.info("DEBUG: Info wrapper updated")
                    except (AssertionError, AttributeError):
                        pass
                
                if self.air_condition_container_wrapper:
                    self.air_condition_container_wrapper.content = air_condition_container.content
                    try:
                        self.air_condition_container_wrapper.update()
                        logging.info("DEBUG: Air condition wrapper updated")
                    except (AssertionError, AttributeError):
                        pass
                
                if self.hourly_container_wrapper:
                    self.hourly_container_wrapper.content = hourly_container.content
                    try:
                        self.hourly_container_wrapper.update()
                        logging.info("DEBUG: Hourly wrapper updated")
                    except (AssertionError, AttributeError):
                        pass
                
                if self.chart_container_wrapper:
                    self.chart_container_wrapper.content = chart_container.content
                    try:
                        self.chart_container_wrapper.update()
                        logging.info("DEBUG: Chart wrapper updated")
                    except (AssertionError, AttributeError):
                        pass
                
                if self.precipitation_chart_container_wrapper:
                    self.precipitation_chart_container_wrapper.content = precipitation_chart_container.content
                    try:
                        self.precipitation_chart_container_wrapper.update()
                        logging.info("DEBUG: Precipitation chart wrapper updated")
                    except (AssertionError, AttributeError):
                        pass
                
                if self.air_pollution_container_wrapper:
                    self.air_pollution_container_wrapper.content = air_pollution_container.content
                    try:
                        self.air_pollution_container_wrapper.update()
                        logging.info("DEBUG: Air pollution wrapper updated")
                    except (AssertionError, AttributeError):
                        pass
                
                logging.info(f"DEBUG: UI containers updated successfully for city: {city}")
                
            except Exception as e:
                logging.info(f"DEBUG: Error updating UI containers: {e}")
                import traceback
                traceback.logging.info_exc()

        # Debug: Verifica che i container siano ora popolati
        if hasattr(self, 'weather_view_instance'):
            info_container, air_condition_container, hourly_container, _, _, _ = self.weather_view_instance.get_containers()
            logging.info(f"DEBUG: [update_weather_with_sidebar] Dopo aggiornamento - Container info popolato: {info_container.content is not None}")
            logging.info(f"DEBUG: [update_weather_with_sidebar] Dopo aggiornamento - Container air_condition popolato: {air_condition_container.content is not None}")
        
        return result

def run():
    """Entry point for the application"""
    app = MeteoApp()
    ft.app( # MODIFIED: ft.app
        target=app.main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER # MODIFIED: ft.AppView
    )


if __name__ == "__main__":
    run()
