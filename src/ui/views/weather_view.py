"""
Weather View for the MeteoApp.
Handles the display of weather information.
"""

import os
import asyncio
import flet as ft
import logging # Add logging import
from ui.themes.themes import LIGHT_THEME, DARK_THEME
from services.api.api_service import ApiService, load_dotenv
from services.ui.translation_service import TranslationService # Import TranslationService
from services.ui.theme_handler import ThemeHandler
from utils.responsive_utils import ResponsiveTextFactory

from ui.components.cards.weather_card import WeatherCard
from ui.layout.sections.informationtab.hourly_forecast import HourlyForecastDisplay # Importa la nuova classe
from ui.layout.sections.weeklyweather.weekly_weather import WeeklyForecastDisplay # CHANGED: Import WeeklyForecastDisplay
from ui.layout.sections.informationtab.main_information import MainWeatherInfo
from ui.layout.sections.informationtab.air_condition import AirConditionInfo
from ui.layout.sections.informationtab.air_pollution import AirPollutionDisplay # CHANGED: Import AirPollutionDisplay
from ui.layout.sections.informationcharts.temperature_chart import TemperatureChartDisplay # CHANGED: Import TemperatureChartDisplay
from ui.layout.sections.informationcharts.precipitation_chart import PrecipitationChartDisplay # CHANGED: Import PrecipitationChartDisplay instead of AirPollutionChartDisplay

class WeatherView:
    """
    View for displaying weather information.
    """
    
    def __init__(self, page: ft.Page, api_service: ApiService):
        load_dotenv()
        self.page = page
        self.api_service = api_service
        self.state_manager = self.page.session.get('state_manager')
        self.weather_data = None
        self.current_weather_data = None  # For weather alerts service
        self.city_info = None
        self.current_lat = None
        self.current_lon = None
        self.current_city = None
        self._update_text_color()

        # ThemeHandler centralizzato
        self.theme_handler = ThemeHandler(self.page)

        # Main containers for different sections of the view
        self.info_container = ft.Container(expand=True)
        self.hourly_container = ft.Container(expand=True)
        self.weekly_container = ft.Container(expand=True)
        self.chart_container = ft.Container(expand=True)
        self.precipitation_chart_container = ft.Container(expand=True)
        self.air_pollution_container = ft.Container(expand=True)

        self.loading = ft.Column(
            [ft.ProgressRing(width=32, height=32)],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            visible=False
        )

        self._register_observers()

    def _register_observers(self):
        if self.state_manager:
            self.state_manager.register_observer("theme_event", self.handle_theme_change)
            self.state_manager.register_observer("language_event", self.handle_language_or_unit_change)
            self.state_manager.register_observer("unit", self.handle_language_or_unit_change)
            logging.info("WeatherView observers registered.")

    def _unregister_observers(self):
        if self.state_manager:
            self.state_manager.unregister_observer("theme_event", self.handle_theme_change)
            self.state_manager.unregister_observer("language_event", self.handle_language_or_unit_change)
            self.state_manager.unregister_observer("unit", self.handle_language_or_unit_change)
            logging.info("WeatherView observers unregistered.")

    def cleanup(self):
        self._unregister_observers()
        logging.info("WeatherView cleanup complete.")

    def _handle_page_resize(self, e=None):
        """Handles page resize events for WeatherView and propagates to children."""
        # Call original page resize handler FIRST if it existed
        if hasattr(self, '_original_page_resize_handler') and self._original_page_resize_handler:
            self._original_page_resize_handler(e)

        # Child components (MainWeatherInfo, HourlyForecastDisplay, 
        # WeeklyForecastDisplay, AirPollutionDisplay, TemperatureChartDisplay, AirPollutionChartDisplay)
        # now manage their own page.on_resize.
        # No direct calls to their _combined_resize_handler needed here.

        # It's generally good practice for the top-level resize handler to call page.update()
        # if sub-components don't reliably do it or if there are direct changes in WeatherView itself.
        if self.page: 
            self.page.update()

    def _cleanup_child_components(self):
        """Clears all child containers' content to remove old components and calls cleanup on observer components."""
        # Cleanup observer components if they exist
        if hasattr(self, 'main_weather_info_instance') and self.main_weather_info_instance:
            try:
                self.main_weather_info_instance.cleanup()
            except Exception:
                pass
            self.main_weather_info_instance = None
        if hasattr(self, 'air_condition_instance') and self.air_condition_instance:
            try:
                self.air_condition_instance.cleanup()
            except Exception:
                pass
            self.air_condition_instance = None
        # Add similar cleanup for other observer-based components if needed
        self.info_container.content = None
        self.hourly_container.content = None
        self.weekly_container.content = None
        self.chart_container.content = None
        self.precipitation_chart_container.content = None
        self.air_pollution_container.content = None

    def _update_text_color(self):
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        self.text_color = DARK_THEME["TEXT"] if is_dark else LIGHT_THEME["TEXT"]

    def _safe_update(self):
        if self.page:
            self.page.update()

    def handle_theme_change(self, event_data=None):
        logging.info("WeatherView: Handling theme change.")
        self._update_text_color()
        # Trigger a full UI update so all child components are rebuilt with the new theme
        self.handle_language_or_unit_change(event_data)

    def handle_language_or_unit_change(self, event_data=None):
        logging.info(f"WeatherView: Handling language/unit change. Event: {event_data}")
        # Always get the latest state from state_manager
        language = self.state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE")
        unit = self.state_manager.get_state('unit') or os.getenv("DEFAULT_UNIT_SYSTEM")
        using_location = self.state_manager.get_state('using_location')
        current_lat = self.state_manager.get_state('current_lat')
        current_lon = self.state_manager.get_state('current_lon')
        city = self.state_manager.get_state('city') or self.current_city

        # Always force a full data refetch and UI rebuild
        if using_location and current_lat is not None and current_lon is not None:
            self.page.run_task(self.update_by_coordinates, current_lat, current_lon, language, unit)
        elif city:
            self.page.run_task(self.update_by_city, city, language, unit)
        else:
            logging.warning("Language/unit change handler: No location context available for update.")

    def _update_component_texts(self, event_type=None, data=None):
        """Update text elements in child components that support selective updates"""
        logging.debug(f"WeatherView: _update_component_texts called with event_type={event_type}, data={data}")
        
        # For unit changes, we need to update components directly since they don't have _update_text_elements
        if event_type == "unit_text_change":
            components_to_update = [
                self.main_weather_info_instance,
                self.temperature_chart_instance,
                self.air_condition_instance,
                self.hourly_forecast_instance,
                self.weekly_forecast_display_instance,
                self.air_pollution_display_instance,
                self.air_pollution_chart_instance
            ]
            
            for component in components_to_update:
                if component and hasattr(component, 'update'):
                    try:
                        logging.debug(f"WeatherView: Updating component {type(component).__name__} for unit change")
                        # Check if the update method is async
                        if hasattr(component, '__class__') and component.__class__.__name__ in ['AirConditionInfo', 'HourlyForecastDisplay', 'AirPollutionDisplay', 'WeeklyForecastDisplay']:
                            # Async components
                            if self.page:
                                self.page.run_task(component.update)
                        else:
                            # Sync components
                            component.update()
                    except Exception as e:
                        logging.error(f"WeatherView: Error updating component {type(component).__name__}: {e}")
            return
        
        # Check for components with _update_text_elements method (for other events)
        # Rimosso air_condition_container perché ora è incluso nel info_container
        for container in [self.info_container, self.hourly_container, self.weekly_container, self.chart_container, self.air_pollution_container]:
            if container and container.content:
                # If the component itself has the method
                if hasattr(container.content, '_update_text_elements'):
                    container.content._update_text_elements(event_type=event_type, data=data)
                # Or if it's a container with items that have the method
                elif hasattr(container.content, 'controls'):
                    for item in container.content.controls:
                        if hasattr(item, '_update_text_elements'):
                            item._update_text_elements(event_type=event_type, data=data)

    def handle_language_change(self, event_data=None):
        """Aggiorna i contenuti della UI quando cambia la lingua."""
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"handle_language_change received unexpected event_data type: {type(event_data)}")
        
        # First update any text elements that can be updated without rebuilding
        self._update_component_texts(event_type="language_change", data=event_data)
        
        # Then handle data re-fetching for a full update if needed
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            language = state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE")
            unit = state_manager.get_state('unit') or os.getenv("DEFAULT_UNIT_SYSTEM")

            # Check if we're using current location
            using_location = state_manager.get_state('using_location')
            
            if using_location and self.current_lat is not None and self.current_lon is not None:
                # If using current location, update by coordinates to get translated location name
                self.page.run_task(self.update_by_coordinates, self.current_lat, self.current_lon, language, unit)
                logging.info(f"Language change: updating by coordinates (lat={self.current_lat}, lon={self.current_lon})")
            if self.current_city:
                # If using city search, use the original city name to get translated data
                original_city = state_manager.get_state('city') or self.current_city
                
                # Clear city_info to force fresh location data
                self.city_info = None
                
                self.page.run_task(self.update_by_city, original_city, language, unit)
                logging.info(f"Language change: updating by city ({original_city})")
            else:
                logging.warning("Language change: no location data available for update")

    async def handle_unit_system_change(self, new_unit_system: str):
        """Handles unit system change events by re-fetching data and updating the UI."""
        state_manager = self.page.session.get('state_manager')
        if not state_manager:
            return

        language = state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE")
        # Get current location context from state_manager if possible, otherwise use WeatherView's last known
        using_location = state_manager.get_state('using_location')
        current_lat_from_state = state_manager.get_state('current_lat')
        current_lon_from_state = state_manager.get_state('current_lon')
        current_city_from_state = state_manager.get_state('city')

        # import asyncio # No longer needed here
        if using_location and current_lat_from_state is not None and current_lon_from_state is not None:
            await self.update_by_coordinates(current_lat_from_state, current_lon_from_state, language, new_unit_system)
        elif current_city_from_state:
            await self.update_by_city(current_city_from_state, language, new_unit_system)
        # Fallback to WeatherView's internally stored context if state manager doesn't have fresh info
        elif self.current_city:
            await self.update_by_city(self.current_city, language, new_unit_system)
        elif self.current_lat is not None and self.current_lon is not None:
            await self.update_by_coordinates(self.current_lat, self.current_lon, language, new_unit_system)
        else:
            # If no location context at all, we might not be able to update.
            # This could happen if unit is changed before any location is set.
            # Consider fetching with a default city if this case is problematic.
            logging.warning("Unit system changed, but no location context (city/coords) available in WeatherView or StateManager to refresh data.")


    async def update_by_city(self, city: str, language: str, unit: str) -> bool:
        """
        Update weather data by city name.
        
        Returns:
            bool: True if successful, False if city not found or error occurred
        """
        logging.info(f"update_by_city called with: city='{city}', language='{language}', unit='{unit}'")
        self._set_loading(True)
        import asyncio
        try:
            try:
                # Recupera i dati in thread separato
                weather_response, city_info = await asyncio.gather(
                    asyncio.to_thread(self.api_service.get_weather_data, city=city, lat=None, lon=None, language=language, unit=unit),
                    asyncio.to_thread(self.api_service.get_city_info, city)
                )
                
                # Controlla se la chiamata API è riuscita
                if not weather_response.get('success', False):
                    error_info = weather_response.get('error', {})
                    error_type = error_info.get('type', 'unknown')
                    error_message = error_info.get('message', 'Unknown error occurred')
                    
                    logging.warning(f"Weather API error: {error_type} - {error_message}")
                    
                    # Mostra popup di errore specifico
                    if error_type == 'city_not_found':
                        self._show_city_not_found_popup(city, error_message)
                    elif error_type == 'network_error':
                        self._show_network_error_popup(error_message)
                    elif error_type == 'api_key_error':
                        self._show_api_error_popup(error_message)
                    else:
                        self._show_generic_error_popup(error_message)
                    
                    return False
                
                weather_data = weather_response.get('data', {})
                
                # Verifica se la città è stata trovata
                if not weather_data or not city_info:
                    logging.warning(f"City '{city}' not found or no weather data available")
                    self._show_city_not_found_error(city)
                    return False
                    
                self.weather_data = weather_data
                self.current_weather_data = weather_data  # For weather alerts service
                self.city_info = city_info
                logging.info(f"Weather data keys: {list(weather_data.keys()) if weather_data else 'None'}")
                
                
                # Debug: Log della struttura city nel weather_data
                if weather_data and "city" in weather_data:
                    city_data = weather_data["city"]
                    logging.info(f"Weather data city: {city_data}")
                    logging.info(f"Weather data city name: {city_data.get('name', 'Not found')}")
                else:
                    logging.warning("No 'city' field found in weather_data")
            except Exception as e:
                logging.error(f"Errore durante il recupero dati: {e}")
                return

            lat = self.city_info[0].get("lat") if self.city_info and len(self.city_info) > 0 else None
            lon = self.city_info[0].get("lon") if self.city_info and len(self.city_info) > 0 else None
            await self._update_ui(city, lat=lat, lon=lon)
            # Aggiorna la UI dopo aver cambiato i dati
            if hasattr(self, 'page') and self.page:
                self.page.update()
            return True
        finally:
            self._set_loading(False)

    async def update_by_coordinates(self, lat: float, lon: float, language: str, unit: str) -> None:
        """Frontend: Triggers backend to fetch weather by coordinates, then updates UI"""
        weather_response = self.api_service.get_weather_data(
            lat=lat,
            lon=lon,
            language=language,
            unit=unit
        )
        
        # Controlla se la chiamata API è riuscita
        if not weather_response.get('success', False):
            error_info = weather_response.get('error', {})
            error_message = error_info.get('message', 'Unknown error occurred')
            logging.error(f"Error fetching weather by coordinates: {error_message}")
            self._show_generic_error_popup(error_message)
            return
        
        self.weather_data = weather_response.get('data', {})
        self.current_weather_data = self.weather_data  # For weather alerts service
        city = self.api_service.get_city_by_coordinates(lat, lon)
        await self._update_ui(city, is_current_location=True, lat=lat, lon=lon)

    async def _update_ui(self, city: str, is_current_location: bool = False, lat: float = None, lon: float = None) -> None:
        """Frontend: Updates UI containers with backend data"""
        if not self.weather_data:
            return
        
        # Cleanup old component instances before creating new ones
        self._cleanup_child_components() # ADDED

        # Capitalize city name
        city = city.capitalize() if city else city

        # Store current coordinates and city for theme change rebuilds
        self.current_city = city
        self.current_lat = lat
        self.current_lon = lon
        
        # Aggiorna la posizione nello state manager
        await self._update_location_in_state(city, lat, lon)

        # Ensure text_color is up-to-date before updating sub-components
        self._update_text_color()
        # Ora aggiorna main info che includerà air condition
        await self._update_main_info(city, is_current_location)
        await self._update_weekly_forecast()
        await self._update_hourly_container()
        await self._update_temperature_chart()
        try:
            if lat is not None and lon is not None:
                self.current_lat = lat
                self.current_lon = lon
                await self._update_air_pollution(lat, lon)
                await self._update_air_pollution_chart(lat, lon) # Add air pollution chart update
                await self._update_precipitation_chart(self.weather_data) # CHANGED: Use precipitation chart with weather data
            elif "city" in self.weather_data and "coord" in self.weather_data["city"]:
                lat = self.weather_data["city"]["coord"]["lat"]
                lon = self.weather_data["city"]["coord"]["lon"]
                self.current_lat = lat
                self.current_lon = lon
                await self._update_air_pollution(lat, lon)
                await self._update_air_pollution_chart(lat, lon) # Add air pollution chart update
                await self._update_precipitation_chart(self.weather_data) # CHANGED: Use precipitation chart with weather data
            else:
                logging.error("No coordinates available for air pollution data")
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error getting coordinates for air pollution: {e}")
        self._safe_update()

    async def _update_location_in_state(self, city: str, lat: float, lon: float):
        """Aggiorna i dettagli della posizione corrente nello state manager centrale."""
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            await state_manager.update_state({
                "city": city,
                "current_lat": lat,
                "current_lon": lon
            })
            logging.info(f"Posizione aggiornata nello stato: City={city}, Lat={lat}, Lon={lon}")

    async def _update_main_info(self, city: str, is_current_location: bool) -> None:
        """Frontend: Updates main weather info UI (robust, always creates new instance)."""
        # Determine display location and translated city name
        if is_current_location:
            location_str = TranslationService.translate_from_dict('main_information_items', 'current_location', self.state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE"))
            location = f"{location_str}"
            translated_city = location_str
        elif self.weather_data and self.weather_data.get("city"):
            city_data = self.weather_data["city"]
            city_name = city_data.get("name", city)
            country = city_data.get("country", "")
            location = f"{city_name}, {country}" if country else city_name
            translated_city = city_name
        elif self.city_info:
            data = self.city_info[0]
            location = ", ".join(filter(None, [data.get("name"), data.get("state"), data.get("country")]))
            translated_city = data.get("name", city)
        else:
            location = city
            translated_city = city

        # Cleanup previous instance if exists
        if hasattr(self, 'main_weather_info_instance') and self.main_weather_info_instance:
            try:
                self.main_weather_info_instance.cleanup()
            except Exception:
                pass

        temp_min, temp_max = self.api_service.get_min_max_temperature(self.weather_data)

        self.main_weather_info_instance = MainWeatherInfo(
            city=translated_city,
            location=location,
            temp_min=temp_min,
            temp_max=temp_max,
            temperature=self.api_service.get_current_temperature(self.weather_data),
            weather_icon=self.api_service.get_weather_icon_code(self.weather_data),
            language=self.state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE"),
            unit=self.state_manager.get_state('unit') or os.getenv("DEFAULT_UNIT_SYSTEM"),
            weather_description=self.api_service.get_weather_description(self.weather_data),
            feels_like=self.api_service.get_feels_like_temperature(self.weather_data),
            page=self.page,
            theme_handler=self.theme_handler,
            expand=True
        )

        # Always create a new AirConditionInfo instance and cleanup previous
        if hasattr(self, 'air_condition_instance') and self.air_condition_instance:
            try:
                self.air_condition_instance.cleanup()
            except Exception:
                pass
        self.air_condition_instance = await self._build_air_condition()

        self.info_container.content = ft.Column(
            controls=[self.main_weather_info_instance, self.air_condition_instance],
            spacing=5,
            expand=True
        )
        self._update_layout_manager_containers()


    async def _update_weekly_forecast(self) -> None:
        """Frontend: Updates weekly forecast UI using WeeklyForecastDisplay."""
        weather_card = WeatherCard(self.page) 
        self._update_text_color() # Ensure text_color is current for components not self-managing it

        if not self.current_city:
            logging.warning("Weekly forecast update skipped: current_city is not set.")
            self.weekly_container.content = ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text="City not selected for weekly forecast.",
                text_type="body_primary",
                color=self.text_color
            )
            return

        # Always create a new instance to guarantee a full rebuild and color update
        self.weekly_forecast_display_instance = WeeklyForecastDisplay(
            page=self.page,
            city=self.current_city,
            theme_handler=self.theme_handler
        )
        self.weekly_container.content = weather_card.build(self.weekly_forecast_display_instance)

    async def _update_temperature_chart(self) -> None:
        """Frontend: Updates temperature chart UI using TemperatureChartDisplay."""
        forecast_data = self.api_service.get_daily_forecast_data(self.weather_data)
        days = self.api_service.get_upcoming_days()
        weather_card = WeatherCard(self.page)
        # Cleanup previous instance if exists
        if hasattr(self, 'temperature_chart_instance') and self.temperature_chart_instance:
            try:
                self.temperature_chart_instance.cleanup()
            except Exception:
                pass
        self.temperature_chart_instance = TemperatureChartDisplay(
            page=self.page,
            days=days,
            temp_min=forecast_data["temp_min"],
            temp_max=forecast_data["temp_max"],
            language=self.state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE"),
            unit=self.state_manager.get_state('unit') or os.getenv("DEFAULT_UNIT_SYSTEM"),
            theme_handler=self.theme_handler
        )
        try:
            self.temperature_chart_instance.update()
        except Exception as e:
            logging.error(f"Error updating temperature chart: {e}")
        self.chart_container.content = weather_card.build(self.temperature_chart_instance)
        try:
            self.chart_container.update()
        except (AssertionError, AttributeError):
            pass

    async def _update_hourly_container(self) -> None:
        """Frontend: Updates hourly forecast UI"""
        weather_card = WeatherCard(self.page)
        self._update_text_color()
        # Cleanup previous instance if exists
        if hasattr(self, 'hourly_forecast_instance') and self.hourly_forecast_instance:
            try:
                self.hourly_forecast_instance.cleanup()
            except Exception:
                pass
        self.hourly_forecast_instance = HourlyForecastDisplay(
            page=self.page,
            city=self.current_city,
            language=self.state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE"),
            unit=self.state_manager.get_state('unit') or os.getenv("DEFAULT_UNIT_SYSTEM"),
            theme_handler=self.theme_handler
        )

        await self.hourly_forecast_instance.update()
        self.hourly_container.content = weather_card.build(self.hourly_forecast_instance)
        try:
            self.hourly_container.update()
        except (AssertionError, AttributeError):
            pass
    
    async def _update_air_pollution(self, lat: float, lon: float) -> None:
        """Frontend: Updates air pollution UI using AirPollutionDisplay."""
        weather_card = WeatherCard(self.page)
        # Cleanup previous instance if exists
        if hasattr(self, 'air_pollution_display_instance') and self.air_pollution_display_instance:
            try:
                self.air_pollution_display_instance.cleanup()
            except Exception:
                pass
        self.air_pollution_display_instance = AirPollutionDisplay(
            page=self.page,
            lat=lat,
            lon=lon,
            theme_handler=self.theme_handler
        )
        await self.air_pollution_display_instance.update()
        self.air_pollution_container.content = weather_card.build(self.air_pollution_display_instance)
        try:
            self.air_pollution_container.update()
        except (AssertionError, AttributeError):
            pass
    
    async def _update_precipitation_chart(self, forecast_data: dict) -> None:
        """Frontend: Updates precipitation chart UI using PrecipitationChartDisplay."""
        logging.info(f"DEBUG: _update_precipitation_chart called with forecast_data keys: {list(forecast_data.keys()) if forecast_data else 'None'}")

        # Get hourly forecast data specifically for precipitation
        try:
            # Fetch forecast data if we don't have the right structure
            if forecast_data and 'list' not in forecast_data:
                logging.info("DEBUG: Current weather data doesn't have forecast list, fetching forecast data...")
                language = self.state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE") 
                unit = self.state_manager.get_state('unit') or os.getenv("DEFAULT_UNIT_SYSTEM")
                
                # Use the city to get forecast data
                if self.current_city:
                    forecast_response = await asyncio.to_thread(
                        self.api_service.get_forecast_data,
                        city=self.current_city,
                        language=language,
                        unit=unit
                    )
                    if forecast_response and forecast_response.get('success'):
                        forecast_data = forecast_response.get('data', {})
                        logging.info(f"DEBUG: Fetched forecast data with keys: {list(forecast_data.keys())}")
                else:
                    logging.warning("DEBUG: No current city available for forecast data")
        except Exception as e:
            logging.error(f"DEBUG: Error fetching forecast data: {e}")

        # Always create a new instance to ensure proper updates
        self.precipitation_chart_instance = PrecipitationChartDisplay(
            page=self.page,
            language=self.state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE"),
            unit=self.state_manager.get_state('unit') or os.getenv("DEFAULT_UNIT_SYSTEM"),
            theme_handler=self.theme_handler
        )
        logging.info("DEBUG: Created new PrecipitationChartDisplay instance")
        
        # Update the chart with forecast data
        self.precipitation_chart_instance.update_data(forecast_data)
        logging.info("DEBUG: Updated precipitation chart with data")

        # Set the chart directly as content (no wrapper needed)
        self.precipitation_chart_container.content = self.precipitation_chart_instance
        logging.info("DEBUG: Set precipitation chart container content")
        
        # Force container update
        try:
            self.precipitation_chart_container.update()
            logging.info("DEBUG: Updated precipitation chart container")
        except AssertionError:
            logging.error("Container not ready for update")
            pass

    async def _update_air_pollution_chart(self, lat: float, lon: float) -> None:
        """Frontend: Updates air pollution chart UI using AirPollutionChartDisplay."""
        # This method seems to be a duplicate of _update_air_pollution and is using
        # AirPollutionDisplay instead of a chart. This is likely a bug.
        # For now, let's assume it should have been using PrecipitationChartDisplay as well,
        # or a non-existent AirPollutionChartDisplay. Since PrecipitationChartDisplay
        # takes forecast_data, we will call that instead.
        # This avoids the linting error and aligns with available components.
        await self._update_precipitation_chart(self.weather_data)

    async def _build_air_condition(self):
        if not self.weather_data:
            return None

        return AirConditionInfo(
            city=self.current_city or "Unknown",
            feels_like=self.api_service.get_feels_like_temperature(self.weather_data) or 0,
            humidity=self.api_service.get_humidity(self.weather_data) or 0,
            wind_speed=self.api_service.get_wind_speed(self.weather_data) or 0,
            pressure=self.api_service.get_pressure(self.weather_data) or 0,
            wind_direction=self.api_service.get_wind_direction(self.weather_data),
            wind_gust=self.api_service.get_wind_gust(self.weather_data),
            visibility=self.api_service.get_visibility(self.weather_data),
            uv_index=self.api_service.get_uv_index(self.weather_data),
            dew_point=self.api_service.get_dew_point(self.weather_data),
            cloud_coverage=self.api_service.get_cloud_coverage(self.weather_data),
            page=self.page,
            theme_handler=self.theme_handler,
            language=self.state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE"),
            unit=self.state_manager.get_state('unit') or os.getenv("DEFAULT_UNIT_SYSTEM")
        )

    def _set_loading(self, value: bool):
        self.loading = value
        self.info_container.visible = not value
        self.hourly_container.visible = not value
        self.weekly_container.visible = not value
        self.chart_container.visible = not value
        self.air_pollution_container.visible = not value
        self.precipitation_chart_container.visible = not value
        self._safe_update()

    def get_containers(self) -> tuple:
        """Frontend: Returns UI containers for display"""
        # Non restituire più loading_container e weekly_container (ora nella sidebar)
        # Non restituire più air_condition_container perché ora è incluso nel info_container
        return (
            self.info_container,
            ft.Container(),  # Container vuoto al posto di air_condition_container
            self.hourly_container,
            self.chart_container,
            self.precipitation_chart_container,
            self.air_pollution_container           
        )

    # cleanup is now defined at the top of the class, no need for a duplicate here.

    def _update_layout_manager_containers(self):
        """
        Aggiorna i riferimenti nei container wrapper del layout manager 
        dopo che i container logici sono stati popolati con i dati meteo.
        """
        # Ottieni il riferimento al main app e al layout manager
        try:
            # Trova l'istanza dell'app tramite la sessione della page
            main_app = None
            for control in self.page.controls:
                if hasattr(control, 'data') and hasattr(control.data, 'layout_manager'):
                    main_app = control.data
                    break
            
            # Alternativa: cerca direttamente nell'app runner se disponibile
            if not main_app and hasattr(self.page, 'session'):
                # Prova a ottenere l'istanza dell'app dalla sessione se disponibile
                main_app = self.page.session.get('main_app')
            
            # Se non troviamo l'istanza, non possiamo aggiornare
            if not main_app or not hasattr(main_app, 'layout_manager'):
                logging.error("DEBUG: Non è possibile ottenere il riferimento al layout manager per aggiornare i container")
                return
            
            # Aggiorna il contenuto dei container wrapper nel layout manager
            # Il wrapper 'info' dovrebbe già puntare al container corretto
            if hasattr(main_app, 'info_container_wrapper') and main_app.info_container_wrapper:
                main_app.info_container_wrapper.content = self.info_container
                logging.info("DEBUG: Container wrapper 'info' aggiornato")
                
            # Aggiorna anche gli altri container se necessario
            if hasattr(main_app, 'hourly_container_wrapper') and main_app.hourly_container_wrapper:
                main_app.hourly_container_wrapper.content = self.hourly_container
                logging.info("DEBUG: Container wrapper 'hourly' aggiornato")
                
            if hasattr(main_app, 'chart_container_wrapper') and main_app.chart_container_wrapper:
                main_app.chart_container_wrapper.content = self.chart_container
                logging.info("DEBUG: Container wrapper 'chart' aggiornato")
                
            if hasattr(main_app, 'precipitation_chart_container_wrapper') and main_app.precipitation_chart_container_wrapper:
                main_app.precipitation_chart_container_wrapper.content = self.precipitation_chart_container
                logging.info("DEBUG: Container wrapper 'precipitation_chart' aggiornato")
                
            if hasattr(main_app, 'air_pollution_container_wrapper') and main_app.air_pollution_container_wrapper:
                main_app.air_pollution_container_wrapper.content = self.air_pollution_container
                logging.info("DEBUG: Container wrapper 'air_pollution' aggiornato")
                
        except Exception as e:
            logging.error(f"DEBUG: Errore durante l'aggiornamento dei container wrapper: {e}")

    def _show_city_not_found_popup(self, city: str, error_message: str) -> None:
        """Show popup when city is not found"""
        import flet as ft
        
        def close_popup(e):
            error_dialog.open = False
            if hasattr(self, 'page') and self.page:
                self.page.update()
        
        # Get translations
        current_language = self.state_manager.get_language()
        translations = self.translation_service.translate_from_dict({
            'error_title': {
                'en': 'City Not Found',
                'it': 'Città non trovata', 
                'es': 'Ciudad no encontrada',
                'fr': 'Ville non trouvée',
                'de': 'Stadt nicht gefunden',
                'pt': 'Cidade não encontrada',
                'ru': 'Город не найден',
                'zh': '未找到城市',
                'ja': '都市が見つかりません',
                'ar': 'لم يتم العثور على المدينة',
                'hi': 'शहर नहीं मिला',
                'ko': '도시를 찾을 수 없습니다'
            },
            'city_error_message': {
                'en': f"The city '{city}' was not found. Please check the spelling and try again.",
                'it': f"La città '{city}' non è stata trovata. Controlla l'ortografia e riprova.",
                'es': f"La ciudad '{city}' no fue encontrada. Por favor verifica la ortografía e inténtalo de nuevo.",
                'fr': f"La ville '{city}' n'a pas été trouvée. Veuillez vérifier l'orthographe et réessayer.",
                'de': f"Die Stadt '{city}' wurde nicht gefunden. Bitte überprüfen Sie die Schreibweise und versuchen Sie es erneut.",
                'pt': f"A cidade '{city}' não foi encontrada. Por favor, verifique a ortografia e tente novamente.",
                'ru': f"Город '{city}' не найден. Пожалуйста, проверьте правописание и попробуйте снова.",
                'zh': f"未找到城市 '{city}'。请检查拼写后重试。",
                'ja': f"都市 '{city}' が見つかりませんでした。スペルを確認してもう一度お試しください。",
                'ar': f"لم يتم العثور على المدينة '{city}'. يرجى التحقق من الإملاء والمحاولة مرة أخرى.",
                'hi': f"शहर '{city}' नहीं मिला। कृपया वर्तनी जांचें और फिर से प्रयास करें।",
                'ko': f"도시 '{city}'를 찾을 수 없습니다. 철자를 확인하고 다시 시도해주세요."
            },
            'ok_button': {
                'en': 'OK',
                'it': 'OK',
                'es': 'Aceptar',
                'fr': 'OK',
                'de': 'OK',
                'pt': 'OK',
                'ru': 'OK',
                'zh': '确定',
                'ja': 'OK',
                'ar': 'حسناً',
                'hi': 'ठीक',
                'ko': '확인'
            }
        }, current_language)
        
        error_dialog = ft.AlertDialog(
            modal=True,
            scrollable=True,  # Make dialog scrollable
            title=ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=translations.get('error_title', 'Error'),
                text_type="title_secondary",
                weight=ft.FontWeight.BOLD,
                color=ft.colors.RED_400
            ),
            content=ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=translations.get('city_error_message', error_message),
                text_type="body_primary"
            ),
            actions=[
                ft.TextButton(
                    translations.get('ok_button', 'OK'),
                    on_click=close_popup,
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_400
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        if hasattr(self, 'page') and self.page:
            self.page.dialog = error_dialog
            error_dialog.open = True
            self.page.update()

    def _show_network_error_popup(self, error_message: str) -> None:
        """Show popup for network errors"""
        import flet as ft
        
        def close_popup(e):
            error_dialog.open = False
            if hasattr(self, 'page') and self.page:
                self.page.update()
        
        # Get translations
        current_language = self.state_manager.get_language()
        translations = self.translation_service.translate_from_dict({
            'network_error_title': {
                'en': 'Network Error',
                'it': 'Errore di rete',
                'es': 'Error de red',
                'fr': 'Erreur réseau',
                'de': 'Netzwerkfehler',
                'pt': 'Erro de rede',
                'ru': 'Ошибка сети',
                'zh': '网络错误',
                'ja': 'ネットワークエラー',
                'ar': 'خطأ في الشبكة',
                'hi': 'नेटवर्क त्रुटि',
                'ko': '네트워크 오류'
            },
            'network_error_message': {
                'en': 'Unable to connect to weather service. Please check your internet connection and try again.',
                'it': 'Impossibile connettersi al servizio meteo. Controlla la connessione internet e riprova.',
                'es': 'No se puede conectar al servicio meteorológico. Por favor verifica tu conexión a internet e inténtalo de nuevo.',
                'fr': 'Impossible de se connecter au service météo. Veuillez vérifier votre connexion internet et réessayer.',
                'de': 'Verbindung zum Wetterdienst nicht möglich. Bitte überprüfen Sie Ihre Internetverbindung und versuchen Sie es erneut.',
                'pt': 'Não é possível conectar ao serviço meteorológico. Por favor, verifique sua conexão com a internet e tente novamente.',
                'ru': 'Невозможно подключиться к службе погоды. Пожалуйста, проверьте подключение к интернету и попробуйте снова.',
                'zh': '无法连接到天气服务。请检查您的互联网连接并重试。',
                'ja': '天気サービスに接続できません。インターネット接続を確認して、もう一度お試しください。',
                'ar': 'تعذر الاتصال بخدمة الطقس. يرجى التحقق من اتصالك بالإنترنت والمحاولة مرة أخرى.',
                'hi': 'मौसम सेवा से कनेक्ट नहीं हो सका। कृपया अपना इंटरनेट कनेक्शन जांचें और फिर से प्रयास करें।',
                'ko': '날씨 서비스에 연결할 수 없습니다. 인터넷 연결을 확인하고 다시 시도해주세요.'
            },
            'ok_button': {
                'en': 'OK',
                'it': 'OK',
                'es': 'Aceptar',
                'fr': 'OK',
                'de': 'OK',
                'pt': 'OK',
                'ru': 'OK',
                'zh': '确定',
                'ja': 'OK',
                'ar': 'حسناً',
                'hi': 'ठीक',
                'ko': '확인'
            }
        }, current_language)
        
        error_dialog = ft.AlertDialog(
            modal=True,
            scrollable=True,  # Make dialog scrollable
            title=ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=translations.get('network_error_title', 'Network Error'),
                text_type="title_secondary",
                weight=ft.FontWeight.BOLD,
                color=ft.colors.ORANGE_400
            ),
            content=ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=translations.get('network_error_message', error_message),
                text_type="body_primary"
            ),
            actions=[
                ft.TextButton(
                    translations.get('ok_button', 'OK'),
                    on_click=close_popup,
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_400
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        if hasattr(self, 'page') and self.page:
            self.page.dialog = error_dialog
            error_dialog.open = True
            self.page.update()

    def _show_api_error_popup(self, error_message: str) -> None:
        """Show popup for API key errors"""
        import flet as ft
        
        def close_popup(e):
            error_dialog.open = False
            if hasattr(self, 'page') and self.page:
                self.page.update()
        
        # Get translations
        current_language = self.state_manager.get_language()
        translations = self.translation_service.translate_from_dict({
            'api_error_title': {
                'en': 'API Error',
                'it': 'Errore API',
                'es': 'Error de API',
                'fr': 'Erreur API',
                'de': 'API-Fehler',
                'pt': 'Erro de API',
                'ru': 'Ошибка API',
                'zh': 'API错误',
                'ja': 'APIエラー',
                'ar': 'خطأ في واجهة برمجة التطبيقات',
                'hi': 'API त्रुटि',
                'ko': 'API 오류'
            },
            'api_error_message': {
                'en': 'There was an issue with the weather service. Please try again later.',
                'it': 'Si è verificato un problema con il servizio meteo. Riprova più tardi.',
                'es': 'Hubo un problema con el servicio meteorológico. Por favor inténtalo más tarde.',
                'fr': 'Il y a eu un problème avec le service météo. Veuillez réessayer plus tard.',
                'de': 'Es gab ein Problem mit dem Wetterdienst. Bitte versuchen Sie es später erneut.',
                'pt': 'Houve um problema com o serviço meteorológico. Por favor, tente novamente mais tarde.',
                'ru': 'Возникла проблема со службой погоды. Пожалуйста, попробуйте позже.',
                'zh': '天气服务出现问题。请稍后再试。',
                'ja': '天気サービスに問題が発生しました。後でもう一度お試しください。',
                'ar': 'حدثت مشكلة في خدمة الطقس. يرجى المحاولة مرة أخرى لاحقاً.',
                'hi': 'मौसम सेवा में समस्या थी। कृपया बाद में फिर से प्रयास करें।',
                'ko': '날씨 서비스에 문제가 발생했습니다. 나중에 다시 시도해주세요.'
            },
            'ok_button': {
                'en': 'OK',
                'it': 'OK',
                'es': 'Aceptar',
                'fr': 'OK',
                'de': 'OK',
                'pt': 'OK',
                'ru': 'OK',
                'zh': '确定',
                'ja': 'OK',
                'ar': 'حسناً',
                'hi': 'ठीक',
                'ko': '확인'
            }
        }, current_language)
        
        error_dialog = ft.AlertDialog(
            modal=True,
            scrollable=True,  # Make dialog scrollable
            title=ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=translations.get('api_error_title', 'API Error'),
                text_type="title_secondary",
                weight=ft.FontWeight.BOLD,
                color=ft.colors.RED_600
            ),
            content=ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=translations.get('api_error_message', error_message),
                text_type="body_primary"
            ),
            actions=[
                ft.TextButton(
                    translations.get('ok_button', 'OK'),
                    on_click=close_popup,
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_400
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        if hasattr(self, 'page') and self.page:
            self.page.dialog = error_dialog
            error_dialog.open = True
            self.page.update()

    def _show_generic_error_popup(self, error_message: str) -> None:
        """Show popup for generic errors"""
        import flet as ft
        
        def close_popup(e):
            error_dialog.open = False
            if hasattr(self, 'page') and self.page:
                self.page.update()
        
        # Get translations
        current_language = self.state_manager.get_language()
        translations = self.translation_service.translate_from_dict({
            'generic_error_title': {
                'en': 'Error',
                'it': 'Errore',
                'es': 'Error',
                'fr': 'Erreur',
                'de': 'Fehler',
                'pt': 'Erro',
                'ru': 'Ошибка',
                'zh': '错误',
                'ja': 'エラー',
                'ar': 'خطأ',
                'hi': 'त्रुटि',
                'ko': '오류'
            },
            'ok_button': {
                'en': 'OK',
                'it': 'OK',
                'es': 'Aceptar',
                'fr': 'OK',
                'de': 'OK',
                'pt': 'OK',
                'ru': 'OK',
                'zh': '确定',
                'ja': 'OK',
                'ar': 'حسناً',
                'hi': 'ठीक',
                'ko': '확인'
            }
        }, current_language)
        
        error_dialog = ft.AlertDialog(
            modal=True,
            scrollable=True,  # Make dialog scrollable
            title=ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=translations.get('generic_error_title', 'Error'),
                text_type="title_secondary",
                weight=ft.FontWeight.BOLD,
                color=ft.colors.RED_500
            ),
            content=ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=error_message,
                text_type="body_primary"
            ),
            actions=[
                ft.TextButton(
                    translations.get('ok_button', 'OK'),
                    on_click=close_popup,
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_400
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        if hasattr(self, 'page') and self.page:
            self.page.dialog = error_dialog
            error_dialog.open = True
            self.page.update()
