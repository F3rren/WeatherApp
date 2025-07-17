"""
Main application file for the MeteoApp.
Refactored for better structure, modularity and robustness.
"""

# Standard library imports
import logging
import asyncio

# Third-party imports
import flet as ft

# Local imports - Config
from services.theme_handler import ThemeHandler

from utils.config import (
    DARK_THEME, 
    LIGHT_THEME,
    DEFAULT_CITY, 
    DEFAULT_LANGUAGE, 
    DEFAULT_UNIT_SYSTEM, 
    DEFAULT_THEME_MODE
)

# Local imports - Core services
from services.api_service import ApiService
from services.geolocation_service import GeolocationService
from services.location_toggle_service import LocationToggleService
from services.theme_toggle_service import ThemeToggleService
from services.translation_service import TranslationService

# Local imports - State and Layout
from state_manager import StateManager
from layout.layout_manager import LayoutManager
from layout.sidebar.sidebar_manager import SidebarManager
from ui.weather_view import WeatherView

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MeteoApp:
    """
    Main application class for the MeteoApp.
    Handles the initialization and orchestration of all components.
    """

    def __init__(self):
        """Initialize the MeteoApp with default values."""
        # Core references
        self.page: ft.Page = None
        self.theme_handler = ThemeHandler(self.page)
        self.language= DEFAULT_LANGUAGE
        self.unit_system = DEFAULT_UNIT_SYSTEM
        self.text_color = self.theme_handler.get_text_color()
        
        # Core services (initialized early)
        self.api_service = ApiService()
        self.geolocation_service = GeolocationService()
        
        # Services (initialized in main method)
        self.state_manager: StateManager = None
        self.location_toggle_service: LocationToggleService = None
        self.theme_toggle_service: ThemeToggleService = None
        self.translation_service: TranslationService = None
        
        # UI Components
        self.weather_view_instance: WeatherView = None
        self.sidebar_manager: SidebarManager = None
        self.layout_manager: LayoutManager = None
        
        # Container references (for theme updates)
        self.sidebar_container: ft.Container = None
        self.info_container_wrapper: ft.Container = None
        self.hourly_container_wrapper: ft.Container = None
        self.chart_container_wrapper: ft.Container = None
        self.precipitation_chart_container_wrapper: ft.Container = None
        self.air_pollution_container_wrapper: ft.Container = None
        self.air_condition_container_wrapper: ft.Container = None
        
        # Additional instances
        self.charts_view_instance = None 

    def _setup_page_properties(self) -> None:
        """Configure initial page properties."""
        if not self.page:
            return
            
        logger.info("Setting up page properties")
        self.page.title = "MeteoOGGI - Il tuo meteo giornaliero"
        self.page.theme_mode = (
            ft.ThemeMode.LIGHT if DEFAULT_THEME_MODE == "light" 
            else ft.ThemeMode.DARK
        )
        self.page.adaptive = True
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.animation_duration = 500

    def _initialize_services(self) -> None:
        """Initialize all core services."""
        logger.info("Initializing core services")
        
        # Initialize state manager
        self.state_manager = StateManager(self.page)
        
        # Store references in session for global access
        self.page.session.set('state_manager', self.state_manager)
        self.page.session.set('main_app', self)
        
        # Initialize translation service
        self.translation_service = TranslationService()
        self.page.session.set('translation_service', self.translation_service)
        
        # Initialize weather view
        self.weather_view_instance = WeatherView(self.page, self.api_service)
        
        # Initialize toggle services
        self.location_toggle_service = LocationToggleService(
            page=self.page,
            geolocation_service=self.geolocation_service,
            state_manager=self.state_manager,
            update_weather_callback=self.update_weather_with_coordinates
        )
        
        self.theme_toggle_service = ThemeToggleService(
            page=self.page, 
            state_manager=self.state_manager
        )
        
        # Initialize sidebar manager
        self.sidebar_manager = SidebarManager(
            page=self.page,
            api_service=self.api_service,
            state_manager=self.state_manager,
            location_toggle_service=self.location_toggle_service,
            theme_toggle_service=self.theme_toggle_service,
            update_weather_callback=self.update_weather_with_sidebar,
            language=self.language, unit= self.unit_system
        )
        
        # Initialize layout manager
        self.layout_manager = LayoutManager(self.page)

    def _register_event_handlers(self) -> None:
        """Register all event handlers."""
        logger.info("Registering event handlers")
        
        # Register theme update handler
        self.state_manager.register_observer("theme_event", self._update_container_colors)
        
        # Register language change handler
        self.state_manager.register_observer("language_event", self._handle_language_change)
        
        # Register unit change handler
        self.state_manager.register_observer("unit", self._handle_unit_change)
        
        # Register cleanup handlers
        self._register_cleanup_handlers()

    def _register_cleanup_handlers(self) -> None:
        """Register cleanup handlers for page disconnect/close events."""
        async def on_disconnect_or_close(e):
            logger.info("Page disconnected or window closed, performing cleanup...")
            try:
                if self.weather_view_instance:
                    self.weather_view_instance.cleanup()
                logger.info("Cleanup completed successfully")
            except Exception as cleanup_error:
                logger.error(f"Error during cleanup: {cleanup_error}")
        
        self.page.on_disconnect = on_disconnect_or_close
        
        # Desktop platform specific window event handler
        if self.page.platform in [ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS]:
            async def window_event_handler(e):
                if e.data == "close":
                    await on_disconnect_or_close(e)
            self.page.on_window_event = window_event_handler

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
            
            # Apply specific theme for precipitation chart
            if self.precipitation_chart_container_wrapper and hasattr(self.precipitation_chart_container_wrapper, 'bgcolor'):
                try:
                    is_ready = False
                    if hasattr(self.precipitation_chart_container_wrapper, 'page') and self.precipitation_chart_container_wrapper.page is not None:
                        is_ready = True
                    elif hasattr(self.precipitation_chart_container_wrapper, 'parent'):
                        current = self.precipitation_chart_container_wrapper
                        while current and hasattr(current, 'parent') and current.parent:
                            current = current.parent
                            if hasattr(current, 'page') and current.page is not None:
                                is_ready = True
                                break
                    
                    if is_ready:
                        # Apply specific styling for precipitation chart to match the chart itself
                        bg_color = theme.get("CARD_BACKGROUND", "#ffffff" if not is_dark else "#161b22")
                        self.precipitation_chart_container_wrapper.bgcolor = bg_color
                        
                        # Apply border for better visibility with custom color for precipitation chart
                        border_color = ft.Colors.with_opacity(0.1, theme.get("BORDER", "#e1e8ed"))
                        self.precipitation_chart_container_wrapper.border = ft.border.all(
                            width=1, 
                            color=border_color
                        )
                        
                        # Apply shadow for better depth
                        shadow_color = ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
                        self.precipitation_chart_container_wrapper.shadow = ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=4,
                            color=shadow_color,
                            offset=ft.Offset(0, 2)
                        )
                        
                        # Notify any precipitation chart instances that theme changed
                        # This helps ensure inner content also gets updated
                        try:
                            if self.weather_view_instance and hasattr(self.weather_view_instance, 'precipitation_chart'):
                                precipitation_chart = self.weather_view_instance.precipitation_chart
                                if precipitation_chart and hasattr(precipitation_chart, '_safe_theme_update'):
                                    precipitation_chart._safe_theme_update({'is_dark': is_dark})
                                    logging.debug("Triggered theme update on precipitation chart instance")
                        except Exception as e:
                            logging.debug(f"Note: Could not trigger theme update on precipitation chart: {e}")
                        
                        self.precipitation_chart_container_wrapper.update()
                        logging.debug("Precipitation chart container updated with specific theme")
                    else:
                        logging.debug("Precipitation chart container not ready for theme update")
                except Exception as e:
                    logging.error(f"Error updating precipitation chart container: {e}")
            
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

    async def main(self, page: ft.Page) -> None:
        """
        Main entry point for the application.
        
        Args:
            page: Flet page object
        """
        logger.info("Starting MeteoApp initialization")
        
        try:
            # Store page reference
            self.page = page
            
            # Phase 1: Setup page properties
            self._setup_page_properties()
            
            # Phase 2: Initialize services
            self._initialize_services()
            
            # Phase 3: Register event handlers
            self._register_event_handlers()
            
            # Phase 4: Build and display the layout
            await self.build_layout()
            
            logger.info("MeteoApp initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize MeteoApp: {e}")
            # Show error to user
            self.page.add(
                ft.Container(
                    content=ft.Text(
                        f"Errore nell'inizializzazione dell'app: {e}",
                        color=ft.Colors.RED,
                        size=16
                    ),
                    padding=20,
                    alignment=ft.alignment.center
                )
            )
            raise

    async def _initialize_default_state(self) -> None:
        """Initialize default application state."""
        logger.info("Initializing default application state")
        
        await self.state_manager.set_state("language", DEFAULT_LANGUAGE)
        await self.state_manager.set_state("unit", DEFAULT_UNIT_SYSTEM)
        await self.state_manager.set_state("city", DEFAULT_CITY)

    async def _load_initial_weather_data(self) -> bool:
        """Load initial weather data before building the UI."""
        logger.info("Loading initial weather data")
        
        try:
            success = await self.update_weather_with_sidebar(
                city=self.state_manager.get_state("city") or DEFAULT_CITY,
                language=self.state_manager.get_state("language") or DEFAULT_LANGUAGE,
                unit=self.state_manager.get_state("unit") or DEFAULT_UNIT_SYSTEM
            )
            
            if success:
                logger.info("Initial weather data loaded successfully")
            else:
                logger.warning("Failed to load initial weather data")
                
            return success
            
        except Exception as e:
            logger.error(f"Error loading initial weather data: {e}")
            return False

    async def _initialize_background_services(self) -> None:
        """Initialize background services with timeout handling."""
        logger.info("Initializing background services")
        
        # Initialize location service
        try:
            await asyncio.wait_for(
                self.location_toggle_service.initialize_tracking(), 
                timeout=5.0
            )
            logger.info("Location service initialized successfully")
        except asyncio.TimeoutError:
            logger.warning("Location service initialization timed out")
        except Exception as e:
            logger.warning(f"Failed to initialize location tracking: {e}")
        
        # Initialize theme service
        try:
            await self.theme_toggle_service.initialize_theme()
            logger.info("Theme service initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize theme service: {e}")

    async def build_layout(self) -> None:
        """Build and display the application layout."""
        logger.info("Building application layout")
        
        try:
            # Phase 1: Initialize default state
            await self._initialize_default_state()
            
            # Phase 2: Load initial weather data
            await self._load_initial_weather_data()
            
            # Phase 3: Get populated containers from WeatherView
            logger.info("Retrieving containers from WeatherView")
            containers = self.weather_view_instance.get_containers()
            info_container, air_condition_container, hourly_container, chart_container, precipitation_chart_container, air_pollution_container = containers
            
            # Phase 4: Create layout manager containers
            logger.info("Creating layout manager containers")
            self.layout_manager.create_containers(
                sidebar_content=self.sidebar_manager,
                info_content=info_container,
                hourly_content=hourly_container,
                chart_content=chart_container,
                precipitation_chart_content=precipitation_chart_container,
                air_pollution_content=air_pollution_container
            )
            
            # Phase 5: Store container references for theme updates
            self._store_container_references()
            
            # Phase 6: Build and add layout to page
            logger.info("Adding layout to page")
            self.page.controls.clear()
            layout = self.layout_manager.build_layout()
            self.page.add(layout)
            
            # Phase 7: Apply initial theme
            self._update_container_colors()
            
            # Phase 8: Initialize background services
            await self._initialize_background_services()
            
            logger.info("Layout building completed successfully")
            
        except Exception as e:
            logger.error(f"Error building layout: {e}")
            raise

    def _store_container_references(self) -> None:
        """Store container references for theme updates."""
        logger.info("Storing container references")
        
        containers = self.layout_manager.get_all_containers()
        self.sidebar_container = containers.get('sidebar')
        self.info_container_wrapper = containers.get('info')
        self.hourly_container_wrapper = containers.get('hourly')
        self.chart_container_wrapper = containers.get('chart')
        self.precipitation_chart_container_wrapper = containers.get('precipitation_chart')
        self.air_pollution_container_wrapper = containers.get('air_pollution')


    async def update_weather_with_sidebar(self, city: str, language: str, unit: str) -> bool:
        """
        Update both main weather view and sidebar weekly forecast.
        
        Args:
            city: City name
            language: Language code
            unit: Unit system
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Updating weather data for city: {city}, language: {language}, unit: {unit}")
        
        try:
            # Update state with batch update to avoid multiple notifications
            await self.state_manager.update_state({
                "city": city,
                "language": language,
                "unit": unit
            })
            
            # Update main weather view
            result = await self.weather_view_instance.update_by_city(city, language, unit)
            if not result:
                logger.warning(f"Failed to update weather view for city: {city}")
                return False
                
            logger.info(f"Weather view updated successfully for city: {city}")
            
            # Update charts view if it exists
            if self.charts_view_instance:
                try:
                    await self.charts_view_instance.update_by_city(city, language, unit)
                    logger.info(f"Charts view updated for city: {city}")
                except Exception as e:
                    logger.warning(f"Failed to update charts view: {e}")
            
            # Update sidebar weekly forecast
            if self.sidebar_manager:
                try:
                    self.sidebar_manager.update_weekly_forecast(city)
                    logger.info(f"Sidebar weekly forecast updated for city: {city}")
                except Exception as e:
                    logger.warning(f"Failed to update sidebar: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating weather data for {city}: {e}")
            return False

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
    
    def _handle_unit_change(self, event_data=None):
        """Handle unit change events at the main app level."""
        try:
            logging.info(f"Main app: handling unit change event with data: {event_data}")
            
            # Get current state
            state_manager = self.state_manager
            if not state_manager:
                logging.warning("No state manager available for unit change")
                return
                
            # Get current location context
            language = state_manager.get_state('language') or DEFAULT_LANGUAGE
            unit = state_manager.get_state('unit') or DEFAULT_UNIT_SYSTEM
            using_location = state_manager.get_state('using_location')
            current_lat = state_manager.get_state('current_lat')
            current_lon = state_manager.get_state('current_lon')
            city = state_manager.get_state('city')
            
            # Trigger weather update with new unit
            if using_location and current_lat is not None and current_lon is not None:
                # Use coordinates to refresh with new unit
                logging.info("Unit change: updating weather by coordinates")
                if self.page and hasattr(self.page, 'run_task'):
                    self.page.run_task(self.update_weather_with_coordinates, current_lat, current_lon, language, unit)
            elif city:
                # Use city name to get data with new unit
                logging.info(f"Unit change: updating weather by city ({city})")
                if self.page and hasattr(self.page, 'run_task'):
                    self.page.run_task(self.update_weather_with_sidebar, city, language, unit)
            else:
                logging.warning("Unit change: no location context available for update")
                
        except Exception as e:
            logging.error(f"Error handling unit change: {e}")
    
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
def run() -> None:
    """Entry point for the MeteoApp application."""
    try:
        logger.info("Starting MeteoApp")
        app = MeteoApp()
        ft.app(
            target=app.main,
            assets_dir="assets",
            view=ft.AppView.FLET_APP
        )
    except Exception as e:
        logger.error(f"Failed to start MeteoApp: {e}")
        raise


if __name__ == "__main__":
    run()
