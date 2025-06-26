"""
Weather View for the MeteoApp.
Handles the display of weather information.
"""

import flet as ft
import logging # Add logging import
from utils.config import LIGHT_THEME, DARK_THEME
from services.api_service import ApiService
from services.translation_service import TranslationService # Import TranslationService

from layout.weather_card import WeatherCard
from layout.informationtab.hourly_forecast import HourlyForecastDisplay # Importa la nuova classe
from layout.weeklyweather.weekly_weather import WeeklyForecastDisplay # CHANGED: Import WeeklyForecastDisplay
from layout.informationtab.main_information import MainWeatherInfo
from layout.informationtab.air_condition import AirConditionInfo
from layout.informationtab.air_pollution import AirPollutionDisplay # CHANGED: Import AirPollutionDisplay
from layout.informationcharts.temperature_chart import TemperatureChartDisplay # CHANGED: Import TemperatureChartDisplay
from layout.informationcharts.air_pollution_chart import AirPollutionChartDisplay # CHANGED: Import AirPollutionChartDisplay

class WeatherView:
    """
    View for displaying weather information.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        # Backend service for all data fetching/processing
        self.api_service = ApiService()
        self.weather_data = {}
        self.city_info = {}
        # Store current coordinates for theme change rebuilds
        self.current_lat = None
        self.current_lon = None
        self.current_city = None
        self._update_text_color() 
        
        self.main_weather_info_instance = None
        self.air_condition_instance = None # ADDED
        self.weekly_forecast_display_instance = None # CHANGED: Renamed from weekly_weather_instance
        self.hourly_forecast_instance = None # ADDED
        self.temperature_chart_instance = None # ADDED
        self.air_pollution_display_instance = None # CHANGED: Renamed from air_pollution_instance
        self.air_pollution_chart_instance = None

        # Register for theme change events
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_change)
            state_manager.register_observer("language_event", self.handle_language_change)
            state_manager.register_observer("unit", self.handle_unit_system_change) # Register observer for unit changes
            state_manager.register_observer("unit_text_change", self.handle_unit_text_change)

        self.info_container = ft.Container(content=ft.Text("Caricamento...", color=self.text_color)) # Apply initial text color
        self.hourly_container = ft.Container()
        self.weekly_container = ft.Container()
        self.chart_container = ft.Container()
        self.air_pollution_container = ft.Container()
        self.air_pollution_chart_container = ft.Container()
        self.loading = False
        # RIMOSSO: self._loading_dialog e ProgressRing modale

        # Add the main on_resize handler for WeatherView
        if self.page:
            # It's important that WeatherView's on_resize is set up to call the
            # original handler if one existed, and then propagate to its children.
            # The children (like HourlyForecastDisplay) will then replace page.on_resize
            # with their own combined handler.
            self._original_page_resize_handler = self.page.on_resized # Corrected: store page.on_resize not on_resized
            self.page.on_resize = self._handle_page_resize

    def _handle_page_resize(self, e=None):
        """Handles page resize events for WeatherView and propagates to children."""
        # Call original page resize handler FIRST if it existed
        if hasattr(self, '_original_page_resize_handler') and self._original_page_resize_handler:
            self._original_page_resize_handler(e)

        # Child components (MainWeatherInfo, AirConditionInfo, HourlyForecastDisplay, 
        # WeeklyForecastDisplay, AirPollutionDisplay, TemperatureChartDisplay, AirPollutionChartDisplay)
        # now manage their own page.on_resize.
        # No direct calls to their _combined_resize_handler needed here.

        # It's generally good practice for the top-level resize handler to call page.update()
        # if sub-components don't reliably do it or if there are direct changes in WeatherView itself.
        if self.page: 
            self.page.update()

    def _cleanup_child_components(self): 
        """Calls cleanup on all child component instances."""
        children_to_cleanup = [
            self.main_weather_info_instance,
            self.air_condition_instance, 
            self.weekly_forecast_display_instance, 
            self.hourly_forecast_instance,
            self.temperature_chart_instance,
            self.air_pollution_display_instance, # CHANGED: Renamed
            self.air_pollution_chart_instance
        ]
        for child in children_to_cleanup:
            if child and hasattr(child, 'will_unmount'): # Use will_unmount for ft.Control based components
                child.will_unmount()
            elif child and hasattr(child, 'cleanup'): # Fallback for older components
                child.cleanup()
        
        self.main_weather_info_instance = None
        self.air_condition_instance = None 
        self.weekly_forecast_display_instance = None # CHANGED: Renamed
        self.hourly_forecast_instance = None
        self.temperature_chart_instance = None
        self.air_pollution_display_instance = None # CHANGED: Renamed
        self.air_pollution_chart_instance = None

    def _update_text_color(self):
        """Updates text_color based on the current page theme."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        self.text_color = DARK_THEME["TEXT"] if is_dark else LIGHT_THEME["TEXT"]

    def _safe_update(self):
        if getattr(self, "page", None):
            self.page.update()

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color and relevant UI parts."""
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"handle_theme_change received unexpected event_data type: {type(event_data)}")
        self._update_text_color()
        if self.info_container.content and isinstance(self.info_container.content, ft.Text):
            self.info_container.content.color = self.text_color
        self._safe_update()

    def handle_unit_text_change(self, event_data=None):
        """Handles unit text change events by updating relevant UI text parts without a full rebuild."""
        logging.debug(f"WeatherView: Handling unit_text_change with data: {event_data}")
        self._update_component_texts(event_type="unit_text_change", data=event_data)

    def _update_component_texts(self, event_type=None, data=None):
        """Update text elements in child components that support selective updates"""
        # Check for components with _update_text_elements method
        for container in [self.info_container, self.hourly_container, self.weekly_container, self.chart_container,
                         self.air_pollution_chart_container, self.air_pollution_container]:
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
        if self.current_city or (self.current_lat is not None and self.current_lon is not None):
            state_manager = self.page.session.get('state_manager')
            language = state_manager.get_state('language') if state_manager else 'en'
            unit = state_manager.get_state('unit') if state_manager else 'metric'
            if self.current_city:
                self.page.run_task(self.update_by_city, self.current_city, language, unit)
            elif self.current_lat is not None and self.current_lon is not None:
                self.page.run_task(self.update_by_coordinates, self.current_lat, self.current_lon, language, unit)

    async def handle_unit_system_change(self, new_unit_system: str):
        """Handles unit system change events by re-fetching data and updating the UI."""
        state_manager = self.page.session.get('state_manager')
        if not state_manager:
            return

        language = state_manager.get_state('language') or 'en'
        # Get current location context from state_manager if possible, otherwise use WeatherView's last known
        using_location = state_manager.get_state('using_location')
        current_lat_from_state = state_manager.get_state('current_lat')
        current_lon_from_state = state_manager.get_state('current_lon')
        current_city_from_state = state_manager.get_state('city')

        # import asyncio # No longer needed here
        if using_location and current_lat_from_state is not None and current_lon_from_state is not None:
            self.page.run_task(self.update_by_coordinates, current_lat_from_state, current_lon_from_state, language, new_unit_system)
        elif current_city_from_state:
            self.page.run_task(self.update_by_city, current_city_from_state, language, new_unit_system)
        # Fallback to WeatherView's internally stored context if state manager doesn't have fresh info
        elif self.current_city:
            self.page.run_task(self.update_by_city, self.current_city, language, new_unit_system)
        elif self.current_lat is not None and self.current_lon is not None:
            self.page.run_task(self.update_by_coordinates, self.current_lat, self.current_lon, language, new_unit_system)
        else:
            # If no location context at all, we might not be able to update.
            # This could happen if unit is changed before any location is set.
            # Consider fetching with a default city if this case is problematic.
            logging.warning("Unit system changed, but no location context (city/coords) available in WeatherView or StateManager to refresh data.")


    async def update_by_city(self, city: str, language: str, unit: str) -> None:
        self._set_loading(True)
        import asyncio
        try:
            try:
                # Recupera i dati in thread separato
                weather_data, city_info = await asyncio.gather(
                    asyncio.to_thread(self.api_service.get_weather_data, city, None, language, unit),
                    asyncio.to_thread(self.api_service.get_city_info, city)
                )
                self.weather_data = weather_data
                self.city_info = city_info
            except Exception as e:
                print(f"Errore durante il recupero dati: {e}")
                return

            lat = lon = None
            if self.city_info and len(self.city_info) > 0:
                lat = self.city_info[0].get("lat")
                lon = self.city_info[0].get("lon")
                await self._update_ui(city, lat=lat, lon=lon)
            # Aggiorna la UI dopo aver cambiato i dati
            if hasattr(self, 'page') and self.page:
                self.page.update()
        finally:
            self._set_loading(False)

    async def update_by_coordinates(self, lat: float, lon: float, language: str, unit: str) -> None:
        """Frontend: Triggers backend to fetch weather by coordinates, then updates UI"""
        self.weather_data = self.api_service.get_weather_data(
            lat=lat,
            lon=lon,
            language=language,
            unit=unit
        )
        city = self.api_service.get_city_by_coordinates(lat, lon)
        await self._update_ui(city, is_current_location=True, lat=lat, lon=lon)

    async def _update_ui(self, city: str, is_current_location: bool = False, lat: float = None, lon: float = None) -> None:
        """Frontend: Updates UI containers with backend data"""
        if not self.weather_data:
            return
        
        # Cleanup old component instances before creating new ones
        self._cleanup_child_components() # ADDED

        # Store current coordinates and city for theme change rebuilds
        self.current_city = city
        self.current_lat = lat
        self.current_lon = lon
        
        # Ensure text_color is up-to-date before updating sub-components
        self._update_text_color() 
        await self._update_main_info(city, is_current_location)
        await self._update_weekly_forecast()
        await self._update_hourly_container()
        await self._update_temperature_chart()
        try:
            if lat is not None and lon is not None:
                self.current_lat = lat
                self.current_lon = lon
                await self._update_air_pollution(lat, lon)
                await self._update_air_pollution_chart(lat, lon)
            elif "city" in self.weather_data and "coord" in self.weather_data["city"]:
                lat = self.weather_data["city"]["coord"]["lat"]
                lon = self.weather_data["city"]["coord"]["lon"]
                self.current_lat = lat
                self.current_lon = lon
                await self._update_air_pollution(lat, lon)
                await self._update_air_pollution_chart(lat, lon)
            else:
                print("No coordinates available for air pollution data")
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error getting coordinates for air pollution: {e}")
        self._safe_update()

    async def _update_main_info(self, city: str, is_current_location: bool) -> None:
        """Frontend: Updates main weather info UI"""
        # Dati meteo correnti dal servizio API
        temperature = self.api_service.get_current_temperature(self.weather_data)
        feels_like = self.api_service.get_feels_like_temperature(self.weather_data)
        humidity = self.api_service.get_humidity(self.weather_data)
        wind_speed = self.api_service.get_wind_speed(self.weather_data)
        pressure = self.api_service.get_pressure(self.weather_data)
        icon_code = self.api_service.get_weather_icon_code(self.weather_data)

        # Determina la posizione da mostrare
        location_data = self.weather_data.get('location_data', {})
        if is_current_location:
            location = f"📍 {TranslationService.translate_from_dict('main_information_items', 'current_location', self.page.session.get('state_manager').get_state('language'))}"
        elif self.city_info:
            data = self.city_info[0]
            location = ", ".join(filter(None, [data.get("name"), data.get("state"), data.get("country")]))
        else:
            location = ", ".join(filter(None, [location_data.get('city', 'Unknown'), location_data.get('region', 'Unknown'), location_data.get('country', 'Unknown')]))
        
        # Create and store the MainWeatherInfo instance
        self.main_weather_info_instance = MainWeatherInfo(
            city=city,
            location=location,
            temperature=temperature,
            weather_icon=icon_code,
            page=self.page,
            expand=True # Ensure it expands if needed within the column
        )

        # Create and store the AirConditionInfo instance
        self.air_condition_instance = AirConditionInfo(
            feels_like=feels_like,
            humidity=humidity,
            wind_speed=wind_speed,
            pressure=pressure,
            page=self.page,
            city=city,
            expand=True # Ensure it expands if needed within the column
        )
        
        # Combine MainWeatherInfo and AirConditionInfo in a Column
        self.info_container.content = ft.Column(
            controls=[
                self.main_weather_info_instance,
                self.air_condition_instance
            ],
            spacing=10, # Add some spacing between the two components
            expand=True
        )
        # self.info_container.update() # Covered by page.update() later in _update_ui


    async def _update_weekly_forecast(self) -> None:
        """Frontend: Updates weekly forecast UI using WeeklyForecastDisplay."""
        weather_card = WeatherCard(self.page) 
        self._update_text_color() # Ensure text_color is current for components not self-managing it

        # state_manager = self.page.session.get(\'state_manager\')
        # language = state_manager.get_state(\'language\') if state_manager else \'en\'
        # unit = state_manager.get_state(\'unit\') if state_manager else \'metric\'
        # The WeeklyForecastDisplay will get lang/unit from state_manager itself.

        if not self.current_city:
            # Handle case where city is not yet set, perhaps show a placeholder or log
            logging.warning("Weekly forecast update skipped: current_city is not set.")
            self.weekly_container.content = ft.Text("City not selected for weekly forecast.", color=self.text_color)
            # self.weekly_container.update() # Covered by page.update()
            return

        # Instantiate or update the WeeklyForecastDisplay instance
        if not hasattr(self, 'weekly_forecast_display_instance') or not self.weekly_forecast_display_instance:
            self.weekly_forecast_display_instance = WeeklyForecastDisplay(
                page=self.page, 
                city=self.current_city
                # expand=True # WeeklyForecastDisplay sets its own expand
            )
        else:
            # If the city has changed, update the component
            if self.weekly_forecast_display_instance._city != self.current_city:
                self.weekly_forecast_display_instance.update_city(self.current_city)
            # Language and unit changes are handled internally by WeeklyForecastDisplay via observers

        # The WeatherCard is a generic wrapper, WeeklyForecastDisplay is the actual content.
        self.weekly_container.content = weather_card.build(self.weekly_forecast_display_instance)
        # self.weekly_container.update() # Covered by page.update() in _update_ui

    async def _update_temperature_chart(self) -> None:
        """Frontend: Updates temperature chart UI using TemperatureChartDisplay."""
        forecast_data = self.api_service.get_daily_forecast_data(self.weather_data)
        days = self.api_service.get_upcoming_days()
        weather_card = WeatherCard(self.page)
        # self._update_text_color() # TemperatureChartDisplay manages its own text color

        # Instantiate or update the TemperatureChartDisplay instance
        if not hasattr(self, 'temperature_chart_instance') or not self.temperature_chart_instance:
            self.temperature_chart_instance = TemperatureChartDisplay(
                page=self.page,
                days=days,
                temp_min=forecast_data["temp_min"],
                temp_max=forecast_data["temp_max"]
                # expand=True # TemperatureChartDisplay sets its own expand if needed
            )
        else:
            # If data needs to be updated (e.g., city change, unit change affecting data)
            self.temperature_chart_instance.update_data(
                days=days,
                temp_min=forecast_data["temp_min"],
                temp_max=forecast_data["temp_max"]
            )
            # Language and theme changes are handled internally by TemperatureChartDisplay

        # The WeatherCard is a generic wrapper, TemperatureChartDisplay is the actual content.
        self.chart_container.content = weather_card.build(self.temperature_chart_instance)
        # self.chart_container.update() # Covered by page.update() in _update_ui

    async def _update_hourly_container(self) -> None:
        """Frontend: Updates hourly forecast UI"""
        weather_card = WeatherCard(self.page) 
        self._update_text_color() # Ensure text_color is current for components not self-managing it

        # Instantiate the refactored HourlyForecastDisplay
        self.hourly_forecast_instance = HourlyForecastDisplay(
            page=self.page,
            city=self.current_city,
            # expand=True # HourlyForecastDisplay sets its own expand property if needed
        )
        # The WeatherCard is a generic wrapper, the HourlyForecastDisplay is the actual content.
        self.hourly_container.content = weather_card.build(self.hourly_forecast_instance)
        # self.hourly_container.update() # Covered by page.update() in _update_ui
    
    async def _update_air_pollution(self, lat: float, lon: float) -> None:
        """Frontend: Updates air pollution UI using AirPollutionDisplay."""
        weather_card = WeatherCard(self.page)

        if not hasattr(self, 'air_pollution_display_instance') or not self.air_pollution_display_instance:
            self.air_pollution_display_instance = AirPollutionDisplay(
                page=self.page,
                lat=lat,
                lon=lon
            )
        else:
            if self.air_pollution_display_instance._lat != lat or self.air_pollution_display_instance._lon != lon:
                self.air_pollution_display_instance.update_location(lat, lon)
            # Language and theme changes are handled internally by AirPollutionDisplay

        # --- FIX: Aggiorna sempre la lingua e l'unità prima del refresh ---
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            self.air_pollution_display_instance._current_language = state_manager.get_state('language') or self.air_pollution_display_instance._current_language
            self.air_pollution_display_instance._current_unit = state_manager.get_state('unit') or getattr(self.air_pollution_display_instance, '_current_unit', 'metric')


        self.air_pollution_container.content = weather_card.build(self.air_pollution_display_instance)
        # self.air_pollution_container.update() # Covered by page.update() in _update_ui
    
    async def _update_air_pollution_chart(self, lat: float, lon: float) -> None:
        """Frontend: Updates air pollution chart UI using AirPollutionChartDisplay."""
        weather_card = WeatherCard(self.page) # Assuming WeatherCard is still used as a wrapper
        # self._update_text_color() # AirPollutionChartDisplay manages its own text color

        # Instantiate or update the AirPollutionChartDisplay instance
        if not hasattr(self, 'air_pollution_chart_instance') or not self.air_pollution_chart_instance:
            self.air_pollution_chart_instance = AirPollutionChartDisplay(
                page=self.page,
                lat=lat,
                lon=lon
                # expand=True # AirPollutionChartDisplay sets its own expand if needed
            )
        else:
            # If location has changed, update the component
            if self.air_pollution_chart_instance._lat != lat or self.air_pollution_chart_instance._lon != lon:
                self.air_pollution_chart_instance.update_location(lat, lon)
            # Language and theme changes are handled internally by AirPollutionChartDisplay

        # The WeatherCard is a generic wrapper, AirPollutionChartDisplay is the actual content.
        self.air_pollution_chart_container.content = weather_card.build(self.air_pollution_chart_instance)
        # self.air_pollution_chart_container.update() # Covered by page.update() in _update_ui

    def _set_loading(self, value: bool):
        self.loading = value
        # RIMOSSO: logica AlertDialog e print di debug
        # Nascondi/mostra i container principali
        self.info_container.visible = not value
        self.hourly_container.visible = not value
        self.weekly_container.visible = not value
        self.chart_container.visible = not value
        self.air_pollution_container.visible = not value
        self.air_pollution_chart_container.visible = not value
        self._safe_update()

    def get_containers(self) -> tuple:
        """Frontend: Returns UI containers for display"""
        # Non restituire più loading_container
        return (
            self.info_container,
            self.hourly_container,
            self.weekly_container,
            self.chart_container,
            self.air_pollution_container,
            self.air_pollution_chart_container
        )

    def cleanup(self):
        """Cleanup method to release resources and child components."""
        self._cleanup_child_components()
