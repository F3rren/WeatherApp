"""
Sidebar Manager for the MeteoApp.
Handles the initialization and management of the sidebar.
Refactored for better robustness and consistency.
"""

import logging
import os
from dotenv import load_dotenv
import flet as ft
from typing import Callable, Optional

from .popmenu.pop_menu import PopMenu
from .searchbar.search_bar import SearchBar
from ui.layout.sections.weeklyweather.weekly_weather import WeeklyForecastDisplay
from core.state_manager import StateManager
from services.location.location_toggle_service import LocationToggleService
from services.ui.theme_toggle_service import ThemeToggleService
from services.ui.theme_handler import ThemeHandler

# Configure logging
logger = logging.getLogger(__name__)

class SidebarManager(ft.Container):
    """
    Manager per la sidebar dell'applicazione.
    Gestisce l'inizializzazione e il comportamento della sidebar.
    Refactored per robustezza e consistenza.
    """
    
    def __init__(self, 
                 page: ft.Page, 
                 api_service, 
                 state_manager: StateManager, 
                 location_toggle_service: LocationToggleService,
                 theme_toggle_service: ThemeToggleService,
                 update_weather_callback: Optional[Callable] = None,
                 language=None, unit=None,
                 **kwargs):
        load_dotenv()
        super().__init__(**kwargs)
        # Core references
        self.page = page
        self.api_service = api_service
        self.state_manager = state_manager
        self.location_toggle_service = location_toggle_service
        self.theme_toggle_service = theme_toggle_service
        self.update_weather_callback = update_weather_callback
        # Theme handler must be initialized before components
        self.theme_handler = ThemeHandler(self.page)
        # Component state
        self.current_city = None
        self.cities = []
        # Child components
        self.pop_menu = None
        self.search_bar = None
        self.weekly_forecast_display = None

        self.current_language = language or os.getenv("DEFAULT_LANGUAGE")
        self.current_unit_system = unit or os.getenv("DEFAULT_UNIT_SYSTEM")
        self.current_text_color = self.theme_handler.get_text_color()


        # Initialize components and styling
        self._initialize_styling()
        self._initialize_components()
        # Build initial content
        self.content = self.build()

    def _initialize_styling(self) -> None:
        """Initialize container styling properties."""
        self.border_radius = 22
        self.shadow = ft.BoxShadow(blur_radius=18, color="#00000033")

    def _initialize_components(self) -> None:
        """Initialize all child components of the sidebar."""
        logger.info("Initializing sidebar components")
        
        # Get current language
        language = self.current_language

        # Define city selection handler
        async def handle_city_selected(city):
            logger.info(f"City selected in sidebar: {city}")
            unit = self.state_manager.get_state("unit") or "metric"
            if self.update_weather_callback is not None:
                try:
                    result = await self.update_weather_callback(city, language, unit)
                    logger.info(f"Weather update completed for city: {city}")
                    return result
                except Exception as e:
                    logger.error(f"Error updating weather for city {city}: {e}")
                    return False
            else:
                logger.error("No weather update callback available")
                return False

        # Initialize popup menu with theme_handler
        self.pop_menu = PopMenu(
            page=self.page,
            state_manager=self.state_manager,
            handle_location_toggle=self.location_toggle_service.handle_location_toggle,
            handle_theme_toggle=self.theme_toggle_service.handle_theme_toggle,
            theme_toggle_value=(self.page.theme_mode == ft.ThemeMode.DARK),
            location_toggle_value=self.state_manager.get_state("using_location") or False,
            language=language,
            theme_handler=self.theme_handler,
            update_weather_callback=self.update_weather_callback
        )

        # Initialize search bar with theme_handler
        self.search_bar = SearchBar(
            page=self.page,
            cities=self.cities,
            on_city_selected=handle_city_selected,
            language=language,
            theme_handler=self.theme_handler
        )

        self.border_radius = 22
        self.shadow = ft.BoxShadow(blur_radius=18, color="#00000033")
        self.content = self.build()
        # self.update()  # <-- RIMOSSO: Non chiamare update() finché il controllo non è aggiunto alla pagina

        # Register event handlers for robust updates
        self._register_event_handlers()

    def _register_event_handlers(self) -> None:
        """Register event handlers for sidebar updates."""
        logger.info("Registering SidebarManager event handlers")
        
        try:
            # Register theme, language and unit change handlers
            self.state_manager.register_observer("theme_event", self.handle_theme_change)
            self.state_manager.register_observer("language_event", self.handle_language_change)
            self.state_manager.register_observer("unit", self.handle_unit_change)
            logger.debug("SidebarManager event handlers registered successfully")
        except Exception as e:
            logger.warning(f"Error registering SidebarManager event handlers: {e}")

    def handle_theme_change(self, event_data=None) -> None:
        """
        Handle theme change events for sidebar components.
        
        Args:
            event_data: Theme change event data
        """
        logger.info("SidebarManager handling theme change")
        
        try:
            # STEP 1: Update theme handler and text color
            self.theme_handler = ThemeHandler(self.page)
            self.current_text_color = self.theme_handler.get_text_color()
            logger.debug(f"Updated theme handler and text color: {self.current_text_color}")
            
            # STEP 2: Reinitialize components with new theme (SIDEBAR PATTERN)
            language = self.state_manager.get_state("language") or "en"

            # Reinitialize popup menu with new theme_handler
            self.pop_menu = PopMenu(
                page=self.page,
                state_manager=self.state_manager,
                handle_location_toggle=self.location_toggle_service.handle_location_toggle,
                handle_theme_toggle=self.theme_toggle_service.handle_theme_toggle,
                theme_toggle_value=(self.page.theme_mode == ft.ThemeMode.DARK),
                location_toggle_value=self.state_manager.get_state("using_location") or False,
                language=language,
                theme_handler=self.theme_handler,
                update_weather_callback=self.update_weather_callback
            )

            # Reinitialize search bar with new theme_handler
            async def handle_city_selected(city):
                logger.info(f"City selected in sidebar: {city}")
                language = self.state_manager.get_state("language") or "en"
                unit = self.state_manager.get_state("unit") or "metric"
                if self.update_weather_callback is not None:
                    try:
                        result = await self.update_weather_callback(city, language, unit)
                        logger.info(f"Weather update completed for city: {city}")
                        return result
                    except Exception as e:
                        logger.error(f"Error updating weather for city {city}: {e}")
                        return False
                else:
                    logger.error("No weather update callback available")
                    return False

            self.search_bar = SearchBar(
                page=self.page,
                cities=self.cities,
                on_city_selected=handle_city_selected,
                language=language,
                theme_handler=self.theme_handler
            )

            # STEP 3: Reinitialize WeeklyForecastDisplay if it exists to apply new theme
            if self.weekly_forecast_display and self.current_city:
                logger.debug(f"Reinitializing WeeklyForecastDisplay for theme change: {self.current_city}")
                self.weekly_forecast_display = WeeklyForecastDisplay(
                    page=self.page,
                    city=self.current_city
                )

            # STEP 4: Update existing WeeklyForecastDisplay with new theme
            if self.weekly_forecast_display and hasattr(self.weekly_forecast_display, 'update'):
                try:
                    self.weekly_forecast_display.update()
                    logger.debug("Triggered WeeklyForecastDisplay theme update using MainWeatherInfo pattern")
                except Exception as e:
                    logger.warning(f"Error updating WeeklyForecastDisplay theme: {e}")

            # STEP 4: Rebuild sidebar content with new theme (SIDEBAR PATTERN)
            self.content = self.build()

            # STEP 5: Update sidebar container if attached to page
            try:
                self.update()
                logger.info("SidebarManager theme change handled successfully")
            except (AssertionError, AttributeError) as e:
                logger.debug(f"SidebarManager not ready for update: {e}")

        except Exception as e:
            logger.error(f"Error handling SidebarManager theme change: {e}")

    def handle_language_change(self, event_data=None) -> None:
        """
        Handle language change events for sidebar components.
        
        Args:
            event_data: Language change event data
        """
        logger.info("SidebarManager handling language change")
        
        try:
            # STEP 1: Get new language
            language = self.state_manager.get_state("language") or "en"

            # STEP 2: Reinitialize components with new language (SIDEBAR PATTERN)

            # Reinitialize popup menu with new language and theme_handler
            self.pop_menu = PopMenu(
                page=self.page,
                state_manager=self.state_manager,
                handle_location_toggle=self.location_toggle_service.handle_location_toggle,
                handle_theme_toggle=self.theme_toggle_service.handle_theme_toggle,
                theme_toggle_value=(self.page.theme_mode == ft.ThemeMode.DARK),
                location_toggle_value=self.state_manager.get_state("using_location") or False,
                language=language,
                theme_handler=self.theme_handler,
                update_weather_callback=self.update_weather_callback
            )

            # Reinitialize search bar with new language and theme_handler
            async def handle_city_selected(city):
                logger.info(f"City selected in sidebar: {city}")
                language = self.state_manager.get_state("language") or "en"
                unit = self.state_manager.get_state("unit") or "metric"
                if self.update_weather_callback is not None:
                    try:
                        result = await self.update_weather_callback(city, language, unit)
                        logger.info(f"Weather update completed for city: {city}")
                        return result
                    except Exception as e:
                        logger.error(f"Error updating weather for city {city}: {e}")
                        return False
                else:
                    logger.error("No weather update callback available")
                    return False

            self.search_bar = SearchBar(
                page=self.page,
                cities=self.cities,
                on_city_selected=handle_city_selected,
                language=language,
                theme_handler=self.theme_handler
            )

            # STEP 3: Update existing WeeklyForecastDisplay with new language
            if self.weekly_forecast_display and hasattr(self.weekly_forecast_display, 'update'):
                try:
                    self.weekly_forecast_display.update()
                    logger.debug("Triggered WeeklyForecastDisplay language update using MainWeatherInfo pattern")
                except Exception as e:
                    logger.warning(f"Error updating WeeklyForecastDisplay language: {e}")

            # STEP 4: Rebuild sidebar content with new language (SIDEBAR PATTERN)
            self.content = self.build()

            # STEP 5: Update sidebar container if attached to page
            try:
                self.update()
                logger.info("SidebarManager language change handled successfully")
            except (AssertionError, AttributeError) as e:
                logger.debug(f"SidebarManager not ready for update: {e}")

        except Exception as e:
            logger.error(f"Error handling SidebarManager language change: {e}")

    def handle_unit_change(self, event_data=None) -> None:
        """
        Handle unit change events for sidebar components.
        
        Args:
            event_data: Unit change event data
        """
        logger.info("SidebarManager handling unit change")
        
        try:
            # Get current state to refresh the weekly forecast with new units
            unit = self.current_unit_system
            city = self.current_city or self.state_manager.get_state("city")
            
            if city:
                # Update weekly forecast with new unit system
                logger.debug(f"Updating weekly forecast for unit change: {unit}")
                self.update_weekly_forecast(city)
                logger.info("SidebarManager unit change handled successfully")
            else:
                logger.warning("No city available for unit change update")
                
        except Exception as e:
            logger.error(f"Error handling SidebarManager unit change: {e}")

    def update_weekly_forecast(self, city: str) -> bool:
        """
        Update the weekly forecast display with new city data.
        This is the core pattern that makes the sidebar work correctly.
        
        Args:
            city: City name to update forecast for
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Updating sidebar weekly forecast for city: {city}")
        
        try:
            self.current_city = city
            
            if not city:
                logger.warning("No city provided for weekly forecast update")
                return False
            
            # STEP 1: Create/update the child component
            logger.debug(f"Creating WeeklyForecastDisplay for city: {city}")
            self.weekly_forecast_display = WeeklyForecastDisplay(
                page=self.page,
                city=city
            )
            
            # STEP 2: ALWAYS rebuild the entire content (KEY PATTERN)
            logger.debug("Rebuilding sidebar content")
            self.content = self.build()
            
            # STEP 3: ALWAYS update the container if attached to page (KEY PATTERN)
            if self.page and hasattr(self, 'page'):
                try:
                    self.update()
                    logger.info(f"Sidebar successfully updated for city: {city}")
                    return True
                except (AssertionError, AttributeError) as e:
                    logger.debug(f"Sidebar not ready for update (not attached to page): {e}")
                    return False
            else:
                logger.debug("Sidebar page reference not available")
                return False
                
        except Exception as e:
            logger.error(f"Error updating sidebar weekly forecast for {city}: {e}")
            return False
        
    def get_weekly_forecast_content(self):
        """Get the weekly forecast content for the sidebar."""
        if self.weekly_forecast_display:
            return self.weekly_forecast_display
        else:
            # Placeholder when no city is selected
            return ft.Container(
                content=ft.Text(
                    "Select a city to view weekly forecast",
                    size=14,
                    color=self.current_text_color,
                    text_align=ft.TextAlign.CENTER
                ),
                padding=ft.padding.all(20),
                alignment=ft.alignment.center
            )

    def build(self):
        """
        Costruisce una moderna sidebar con previsioni giornaliere simile al design mostrato.
        """
        # Header della sidebar con controlli in riga
        header_section = ft.Container(
            content=ft.Row([
                # PopMenu a sinistra
                ft.Container(
                    content=self.pop_menu,
                    margin=ft.margin.only(right=8),  # Spazio tra PopMenu e SearchBar
                ),
                # SearchBar allargata a destra
                ft.Container(
                    content=self.search_bar.build(
                        popmenu_widget=None,  # Non più necessario
                        clear_icon_size=25,
                    ),
                    expand=True,  # Prende tutto lo spazio rimanente
                ),
            ], 
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0),
            padding=ft.padding.all(15),
            margin=ft.margin.only(bottom=10)
        )

        # Sezione previsioni giornaliere - usa il WeeklyForecastDisplay completo
        weekly_forecast_content = self.get_weekly_forecast_content()
        
        return ft.Column([
            header_section,
            weekly_forecast_content,
        ], spacing=0, expand=True)



    def _on_day_selected(self, day_data):
        """Gestisce la selezione di un giorno specifico."""
        logging.info(f"Selected day: {day_data['day']}")
        
        # Notifica il cambio di giorno attraverso lo state manager
        if self.state_manager:
            # Salva i dati del giorno selezionato
            self.state_manager.set_state('selected_day', day_data)
            
            # Notifica l'evento per aggiornare l'UI
            self.page.run_task(
                self.state_manager._notify_observers, 
                'day_selected_event', 
                day_data
            )

    def set_switch_view_callback(self, callback: Callable):
        """
        Set the callback function for switching view modes.
        
        Args:
            callback: Function to call when switching between weather and charts views
        """
        self.switch_view_callback = callback

    def cleanup(self) -> None:
        """
        Cleanup the SidebarManager component.
        Unregister event handlers and cleanup child components.
        """
        logger.info("Cleaning up SidebarManager")
        
        try:
            # Unregister event handlers
            self.state_manager.unregister_observer("theme_event", self.handle_theme_change)
            self.state_manager.unregister_observer("language_event", self.handle_language_change)
            self.state_manager.unregister_observer("unit", self.handle_unit_change)
            
            # Cleanup child components
            if self.search_bar:
                self.search_bar.cleanup()
            
            if self.pop_menu:
                self.pop_menu.cleanup()
            
            # Clear references
            self.search_bar = None
            self.pop_menu = None
            self.weekly_forecast_display = None
            
            logger.info("SidebarManager cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Error during SidebarManager cleanup: {e}")
