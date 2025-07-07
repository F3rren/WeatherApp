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
        
        try:
            is_dark = False
            if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            
            # Helper function to safely update container
            def safe_update_container(container, color_key):
                if container and hasattr(container, 'bgcolor'):
                    try:
                        # More robust checking for container readiness
                        is_ready = False
                        
                        # Check if container is properly connected to page
                        if hasattr(container, 'page') and container.page is not None:
                            is_ready = True
                        # Alternative check - try to traverse up the widget tree
                        elif hasattr(container, 'parent'):
                            current = container
                            while current and hasattr(current, 'parent') and current.parent:
                                current = current.parent
                                if hasattr(current, 'page') and current.page is not None:
                                    is_ready = True
                                    break
                        
                        if is_ready:
                            container.bgcolor = theme.get(color_key)
                            container.update()
                        else:
                            # Reduce log noise - only log occasionally
                            if not hasattr(safe_update_container, '_not_ready_count'):
                                safe_update_container._not_ready_count = {}
                            safe_update_container._not_ready_count[color_key] = safe_update_container._not_ready_count.get(color_key, 0) + 1
                            if safe_update_container._not_ready_count[color_key] % 20 == 1:  # Log every 20th occurrence
                                logging.debug(f"Container ({color_key}) not ready for color update - not connected to page")
                    except (AssertionError, AttributeError) as e:
                        # Reduce log noise - only log once every 10 attempts
                        if not hasattr(safe_update_container, '_error_count'):
                            safe_update_container._error_count = {}
                        safe_update_container._error_count[color_key] = safe_update_container._error_count.get(color_key, 0) + 1
                        if safe_update_container._error_count[color_key] % 10 == 1:  # Log first error and every 10th
                            logging.debug(f"Container ({color_key}) not ready for color update: {e}")
                    except Exception as e:
                        logging.error(f"Error updating container color for {color_key}: {e}")
            
            # Aggiorna colori specifici per ogni container
            safe_update_container(self.sidebar_container, "SIDEBAR")
            
            if self.info_container_wrapper:
                try:
                    # More robust checking for info container
                    is_ready = False
                    if hasattr(self.info_container_wrapper, 'page') and self.info_container_wrapper.page is not None:
                        is_ready = True
                    elif hasattr(self.info_container_wrapper, 'parent'):
                        current = self.info_container_wrapper
                        while current and hasattr(current, 'parent') and current.parent:
                            current = current.parent
                            if hasattr(current, 'page') and current.page is not None:
                                is_ready = True
                                break
                    
                    if is_ready:
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
                    else:
                        logging.debug("Info container not ready for update - not connected to page")
                except (AssertionError, AttributeError) as e:
                    logging.debug(f"Info container not ready for update: {e}")
                except Exception as e:
                    logging.error(f"Error updating info container: {e}")
            
            safe_update_container(self.hourly_container_wrapper, "HOURLY")
            safe_update_container(self.chart_container_wrapper, "CHART")
            safe_update_container(self.precipitation_chart_container_wrapper, "CHART") # For precipitation chart
            safe_update_container(self.air_pollution_container_wrapper, "CARD_BACKGROUND")
            
            # Aggiorna il colore di sfondo della pagina
            try:
                if self.page and hasattr(self.page, 'bgcolor'):
                    self.page.bgcolor = theme.get("BACKGROUND")
                    self.page.update()
            except (AssertionError, AttributeError) as e:
                logging.debug(f"Page not ready for background update: {e}")
            except Exception as e:
                logging.error(f"Error updating page background: {e}")
                
        except Exception as e:
            logging.error(f"Error in _update_container_colors: {e}")

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
        
        # Register language change handler for main app
        self.state_manager.register_observer("language_event", self._handle_language_change)

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
        
        # Initialize location service with timeout handling
        try:
            await self.location_toggle_service.initialize_tracking()
        except Exception as e:
            logging.warning(f"Failed to initialize location tracking: {e}")
            # Continue without location tracking if it fails
        
        # Initialize theme service
        try:
            await self.theme_toggle_service.initialize_theme()
        except Exception as e:
            logging.warning(f"Failed to initialize theme service: {e}")
            # Continue with default theme if it fails

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
        
        # Aggiorna lo stato con la nuova città - BATCH UPDATE per evitare multiple notifiche
        await self.state_manager.update_state({
            "city": city,
            "language": language,
            "unit": unit
        })
        
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
                
                # Helper function to safely update wrapper containers
                def safe_update_wrapper(wrapper, content, wrapper_name):
                    if wrapper and content:
                        try:
                            # Check if wrapper is properly connected to page
                            if hasattr(wrapper, 'page') and wrapper.page is not None:
                                wrapper.content = content.content
                                wrapper.update()
                                logging.info(f"DEBUG: {wrapper_name} wrapper updated")
                            else:
                                # Reduce log noise - only log occasionally
                                if not hasattr(safe_update_wrapper, '_not_ready_count'):
                                    safe_update_wrapper._not_ready_count = {}
                                safe_update_wrapper._not_ready_count[wrapper_name] = safe_update_wrapper._not_ready_count.get(wrapper_name, 0) + 1
                                if safe_update_wrapper._not_ready_count[wrapper_name] % 5 == 1:  # Log every 5th occurrence
                                    logging.debug(f"DEBUG: {wrapper_name} wrapper not ready for update")
                        except (AssertionError, AttributeError) as e:
                            # Reduce log noise
                            if not hasattr(safe_update_wrapper, '_error_count'):
                                safe_update_wrapper._error_count = {}
                            safe_update_wrapper._error_count[wrapper_name] = safe_update_wrapper._error_count.get(wrapper_name, 0) + 1
                            if safe_update_wrapper._error_count[wrapper_name] % 10 == 1:  # Log every 10th error
                                logging.debug(f"DEBUG: {wrapper_name} wrapper not ready for update: {e}")
                        except Exception as e:
                            logging.error(f"DEBUG: Error updating {wrapper_name} wrapper: {e}")
                
                # IMPORTANTE: Forza l'aggiornamento dei wrapper container con controlli robusti
                safe_update_wrapper(self.info_container_wrapper, info_container, "Info")
                safe_update_wrapper(self.air_condition_container_wrapper, air_condition_container, "Air condition")
                safe_update_wrapper(self.hourly_container_wrapper, hourly_container, "Hourly")
                safe_update_wrapper(self.chart_container_wrapper, chart_container, "Chart")
                safe_update_wrapper(self.precipitation_chart_container_wrapper, precipitation_chart_container, "Precipitation chart")
                safe_update_wrapper(self.air_pollution_container_wrapper, air_pollution_container, "Air pollution")
                
                logging.info(f"DEBUG: UI containers updated successfully for city: {city}")
                
            except Exception as e:
                logging.error(f"DEBUG: Error updating UI containers: {e}")
                import traceback
                traceback.print_exc()

        # Debug: Verifica che i container siano ora popolati
        if hasattr(self, 'weather_view_instance'):
            info_container, air_condition_container, hourly_container, _, _, _ = self.weather_view_instance.get_containers()
            logging.info(f"DEBUG: [update_weather_with_sidebar] Dopo aggiornamento - Container info popolato: {info_container.content is not None}")
            logging.info(f"DEBUG: [update_weather_with_sidebar] Dopo aggiornamento - Container air_condition popolato: {air_condition_container.content is not None}")
        
        return result

    def _handle_language_change(self, event_data=None):
        """Handle language change events at the main app level."""
        try:
            logging.info(f"Main app: handling language change event with data: {event_data}")
            
            # Get current state
            state_manager = self.state_manager
            if not state_manager:
                logging.warning("No state manager available for language change")
                return
                
            # Get current location context
            language = state_manager.get_state('language') or DEFAULT_LANGUAGE
            unit = state_manager.get_state('unit') or DEFAULT_UNIT_SYSTEM
            using_location = state_manager.get_state('using_location')
            current_lat = state_manager.get_state('current_lat')
            current_lon = state_manager.get_state('current_lon')
            city = state_manager.get_state('city')
            
            # Trigger weather update with new language
            if using_location and current_lat is not None and current_lon is not None:
                # Use coordinates to get location name in new language
                logging.info("Language change: updating weather by coordinates")
                if self.page and hasattr(self.page, 'run_task'):
                    self.page.run_task(self.update_weather_with_coordinates, current_lat, current_lon, language, unit)
            elif city:
                # Use city name to get translated data
                logging.info(f"Language change: updating weather by city ({city})")
                if self.page and hasattr(self.page, 'run_task'):
                    self.page.run_task(self.update_weather_with_sidebar, city, language, unit)
            else:
                logging.warning("Language change: no location context available for update")
                
        except Exception as e:
            logging.error(f"Error handling language change: {e}")
    
    async def update_weather_with_coordinates(self, lat: float, lon: float, language: str, unit: str):
        """Update weather data using coordinates."""
        logging.info(f"Updating weather with coordinates: lat={lat}, lon={lon}, language={language}, unit={unit}")
        
        # Update state - BATCH UPDATE per evitare multiple notifiche
        await self.state_manager.update_state({
            "language": language,
            "unit": unit,
            "current_lat": lat,
            "current_lon": lon,
            "using_location": True
        })
        
        # Update weather view
        await self.weather_view_instance.update_by_coordinates(lat, lon, language, unit)
        
        # Update sidebar if needed
        if self.sidebar_manager:
            # Get city name from coordinates for sidebar with correct language
            city = self.api_service.get_city_by_coordinates(lat, lon, language)
            if city:
                await self.state_manager.set_state("city", city)
                self.sidebar_manager.update_weekly_forecast(city)
        
        logging.info("Weather updated successfully with coordinates")

    # ...existing code...
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
