"""
Weather View for the MeteoApp.
Handles the display of weather information.
"""

import flet as ft
import logging
import asyncio # Add asyncio import
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE

from services.api_service import ApiService
from services.translation_service import TranslationService

from layout.frontend.weather_card import WeatherCard
from layout.frontend.informationtab.hourly_forecast import HourlyForecastDisplay # Importa la nuova classe
from layout.frontend.weeklyweather.daily_forecast_items import DailyForecastItems
from layout.frontend.informationtab.main_information import MainWeatherInfo
from layout.frontend.informationtab.air_condition import AirConditionInfo
from layout.frontend.informationtab.air_pollution import AirPollution
from layout.frontend.informationcharts.temperature_chart import TemperatureChart
from layout.frontend.informationcharts.air_pollution_chart import AirPollutionChart

class WeatherView:
    """
    View for displaying weather information.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.api_service = ApiService()
        self.weather_data = {}
        self.city_info = {}
        self.current_lat = None
        self.current_lon = None
        self.current_city = None
        self._update_text_color()
        self._pending_tasks = [] # Initialize pending tasks list

        # Initialize child component instances to None
        self.main_weather_info_instance = None
        self.air_condition_info_instance = None
        self.hourly_forecast_instance = None # For HourlyForecastDisplay
        self.weekly_forecast_items = [] # For DailyForecastItems
        self.temperature_chart_instance = None
        self.air_pollution_instance = None
        self.air_pollution_chart_instance = None
        
        # Register for theme change events
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_change)
            state_manager.register_observer("language_event", self.handle_language_change)
            state_manager.register_observer("unit_event", self.handle_unit_change) # Add observer for unit changes

        # Get current language
        if page and hasattr(page, 'session') and page.session.get('state_manager'):
            state_manager = page.session.get('state_manager')
            self.language = state_manager.get_state('language') or DEFAULT_LANGUAGE
        else:
            self.language = DEFAULT_LANGUAGE

        self.info_container = ft.Container(content=ft.Text(TranslationService.get_text("loading", self.language), color=self.text_color)) # Apply initial text color
        self.weekly_container = ft.Container()
        self.chart_container = ft.Container()
        self.air_pollution_container = ft.Container()
        self.air_pollution_chart_container = ft.Container()

    def _update_text_color(self):
        """Updates text_color based on the current page theme."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        self.text_color = DARK_THEME["TEXT"] if is_dark else LIGHT_THEME["TEXT"]

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color and relevant UI parts."""
        self._update_text_color()
        
        if self.info_container.content and isinstance(self.info_container.content, ft.Text):
            self.info_container.content.color = self.text_color
            # self.info_container.update() # Usually page.update() is enough

        # Re-build air pollution components with new theme Colors if data is available
        if self.current_lat is not None and self.current_lon is not None:
            # Update air pollution component with new text color
            air_pollution = AirPollution(
                page=self.page,
                lat=self.current_lat,
                lon=self.current_lon,
                text_color=self.text_color,
            )
            self.air_pollution_container.content = air_pollution.build()
            
            # Update air pollution chart component with new text color
            air_pollution_chart = AirPollutionChart(
                page=self.page,
                lat=self.current_lat,
                lon=self.current_lon,
                text_color=self.text_color
            )
            self.air_pollution_chart_container.content = air_pollution_chart.build(self.current_lat, self.current_lon)
        
        self.page.update()

    async def handle_unit_change(self, event_data=None):
        """Handles unit change events by re-fetching and updating UI."""
        state_manager = self.page.session.get('state_manager')
        if not state_manager:
            return

        current_unit = state_manager.get_state('unit')
        current_language = state_manager.get_state('language')
        # current_city is already stored in self.current_city
        # current_lat and self.current_lon are also stored

        if state_manager.get_state('using_location') and self.current_lat is not None and self.current_lon is not None:
            await self.update_by_coordinates(self.current_lat, self.current_lon, current_language, current_unit) # await here
        elif self.current_city:
            await self.update_by_city(self.current_city, current_language, current_unit) # await here
        else:
            logging.warning("Unit changed, but no current city or coordinates to update.")

    async def handle_language_change(self, event_data=None): # Make async
        """Aggiorna i contenuti della UI quando cambia la lingua."""
        state_manager = self.page.session.get('state_manager')
        if not state_manager:
            return

        language = state_manager.get_state('language') or DEFAULT_LANGUAGE
        unit = state_manager.get_state('unit') or 'metric'
        
        # Determine if updating by city or coordinates based on current state
        if state_manager.get_state('using_location') and self.current_lat is not None and self.current_lon is not None:
            await self.update_by_coordinates(self.current_lat, self.current_lon, language, unit)
        elif self.current_city:
            await self.update_by_city(self.current_city, language, unit)
        else:
            logging.warning("Language changed, but no current city or coordinates to update.")

    async def update_by_city(self, city: str, language: str, unit: str) -> None:
        """Frontend: Triggers backend to fetch weather by city, then updates UI"""
        # Backend call
        self.weather_data = self.api_service.get_weather_data(
            city=city,
            language=language,
            unit=unit
        )
        self.city_info = self.api_service.get_city_info(city)
        lat = None
        lon = None
        if self.city_info and len(self.city_info) > 0:
            lat = self.city_info[0].get("lat")
            lon = self.city_info[0].get("lon")
        await self._update_ui(city, lat=lat, lon=lon)

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
        
        # Store current coordinates and city for theme change rebuilds
        self.current_city = city
        self.current_lat = lat
        self.current_lon = lon
        
        # Ensure text_color is up-to-date before updating sub-components
        self._update_text_color() 
        await self._update_main_info(city, is_current_location)
        await self._update_weekly_forecast()
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
                logging.error("No coordinates available for air pollution data")
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error getting coordinates for air pollution: {e}")
        self.page.update()

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
        if is_current_location:
            # Use TranslationService for "Current Location"
            location = f"📍 {TranslationService.get_text('current_location', self.language)}"
        elif self.city_info:
            data = self.city_info[0]
            location = ", ".join(filter(None, [data.get("name"), data.get("state"), data.get("country")]))
        else:
            location = city

        # Costruisce la riga di previsioni orarie (massimo 6)
        hourly_data = self.api_service.get_hourly_forecast_data(self.weather_data)[:6]
        
        # Cleanup old hourly forecast instance if exists
        if self.hourly_forecast_instance and hasattr(self.hourly_forecast_instance, 'cleanup'):
            self.hourly_forecast_instance.cleanup()

        # Utilizza la nuova classe per costruire la sezione delle previsioni orarie
        self.hourly_forecast_instance = HourlyForecastDisplay( # Store new instance
            hourly_data=hourly_data,
            text_color=self.text_color,
            page=self.page
        )
        hourly_forecast_control = self.hourly_forecast_instance.build()

        # Costruisce le sezioni dell'interfaccia
        if self.main_weather_info_instance and hasattr(self.main_weather_info_instance, 'cleanup'):
            self.main_weather_info_instance.cleanup() 

        self.main_weather_info_instance = MainWeatherInfo(city, location, temperature, icon_code, self.text_color, self.page)
        main_info_control = self.main_weather_info_instance.build()

        if self.air_condition_info_instance and hasattr(self.air_condition_info_instance, 'cleanup'):
            self.air_condition_info_instance.cleanup()

        self.air_condition_info_instance = AirConditionInfo(feels_like, humidity, wind_speed, pressure, self.text_color, self.page)
        air_condition_control = self.air_condition_info_instance.build()

        # Cleanup old air pollution instance if exists - MOVED to _update_air_pollution
        # Cleanup old air pollution chart instance if exists - MOVED to _update_air_pollution_chart

        # Assembla il contenuto e aggiorna il contenitore
        self.info_container.content = WeatherCard(self.page).build(
            ft.Column(
                controls=[main_info_control, hourly_forecast_control, air_condition_control],
                expand=True,
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH  # Assicura che i figli si estendano
            )
        )
        self.info_container.expand = True

    async def _update_weekly_forecast(self) -> None:
        """Frontend: Updates weekly forecast UI"""
        # Cleanup old weekly forecast items
        if self.weekly_forecast_items:
            for item in self.weekly_forecast_items:
                if hasattr(item, 'cleanup') and callable(item.cleanup):
                    item.cleanup()
            self.weekly_forecast_items.clear()

        weekly_data = self.api_service.get_weekly_forecast_data(self.weather_data)
        weather_card = WeatherCard(self.page) 
        forecast_items_controls = [] 
        self._update_text_color() 
        for i, day_data in enumerate(weekly_data):
            forecast_item_obj = DailyForecastItems( 
                day=day_data["day_key"], 
                icon_code=day_data["icon"],
                temp_min=day_data["temp_min"],
                temp_max=day_data["temp_max"],
                text_color=self.text_color,
                page=self.page 
            )
            self.weekly_forecast_items.append(forecast_item_obj) # Store instance
            forecast_items_controls.append(ft.Container(content=forecast_item_obj.build()))
            if i < len(weekly_data) - 1:
                divider_color = DARK_THEME.get("BORDER", ft.Colors.WHITE if self.page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLACK)
                forecast_items_controls.append(
                    ft.Container(
                        content=ft.Divider(thickness=0.5, color=divider_color, opacity=1),
                    )
                )
        self.weekly_container.content = weather_card.build(
            ft.Column(controls=forecast_items_controls, expand=True)
        )
        # self.weekly_container.update() # Covered by page.update()

    async def _update_temperature_chart(self) -> None:
        """Frontend: Updates temperature chart UI"""
        if self.temperature_chart_instance and hasattr(self.temperature_chart_instance, 'cleanup'):
            self.temperature_chart_instance.cleanup()

        forecast_data = self.api_service.get_daily_forecast_data(self.weather_data)
        days = self.api_service.get_upcoming_days()
        weather_card = WeatherCard(self.page) # Pass page if WeatherCard needs theme context
        self._update_text_color() # Ensure text_color is current
        
        self.temperature_chart_instance = TemperatureChart( # Store new instance
            page=self.page,
            days=days,
            temp_min=forecast_data["temp_min"],
            temp_max=forecast_data["temp_max"],
            text_color=self.text_color
        )
        self.chart_container.content = weather_card.build(self.temperature_chart_instance.build())

    async def _update_air_pollution(self, lat: float, lon: float) -> None:
        """Frontend: Updates air pollution UI"""
        # Cleanup old air pollution instance if exists
        if self.air_pollution_instance and hasattr(self.air_pollution_instance, 'cleanup'):
            self.air_pollution_instance.cleanup()

        self._update_text_color() 
        self.air_pollution_instance = AirPollution( # Store new instance
            page=self.page,
            lat=lat,
            lon=lon,
            text_color=self.text_color, 
        )
        self.air_pollution_container.content = self.air_pollution_instance.build()

    async def _update_air_pollution_chart(self, lat: float, lon: float) -> None:
        """Frontend: Updates air pollution chart UI"""
        # Cleanup old air pollution chart instance if exists
        if self.air_pollution_chart_instance and hasattr(self.air_pollution_chart_instance, 'cleanup'):
            self.air_pollution_chart_instance.cleanup()

        self._update_text_color() 
        self.air_pollution_chart_instance = AirPollutionChart( # Store new instance
            page=self.page,
            lat=lat,
            lon=lon,
            text_color=self.text_color 
        )
        self.air_pollution_chart_container.content = self.air_pollution_chart_instance.build(lat, lon)

    def get_containers(self) -> tuple:
        """Frontend: Returns UI containers for display"""
        return (
            self.info_container,
            self.weekly_container,
            self.chart_container,
            self.air_pollution_container,
            self.air_pollution_chart_container
        )

    def cleanup(self):
        """Cleans up resources and observers used by WeatherView."""
        logging.info("Cleaning up WeatherView...")
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            state_manager.unregister_observer("theme_event", self.handle_theme_change)
            state_manager.unregister_observer("language_event", self.handle_language_change)
            state_manager.unregister_observer("unit_event", self.handle_unit_change)

        # Cancel any pending asyncio tasks
        for task in self._pending_tasks:
            if not task.done():
                task.cancel()
        self._pending_tasks.clear()

        # Cleanup child components
        if self.main_weather_info_instance and hasattr(self.main_weather_info_instance, 'cleanup'):
            self.main_weather_info_instance.cleanup()
        if self.air_condition_info_instance and hasattr(self.air_condition_info_instance, 'cleanup'):
            self.air_condition_info_instance.cleanup()
        if self.hourly_forecast_instance and hasattr(self.hourly_forecast_instance, 'cleanup'):
            self.hourly_forecast_instance.cleanup()
        if self.temperature_chart_instance and hasattr(self.temperature_chart_instance, 'cleanup'):
            self.temperature_chart_instance.cleanup()
        if self.air_pollution_instance and hasattr(self.air_pollution_instance, 'cleanup'):
            self.air_pollution_instance.cleanup()
        if self.air_pollution_chart_instance and hasattr(self.air_pollution_chart_instance, 'cleanup'):
            self.air_pollution_chart_instance.cleanup()
        
        if self.weekly_forecast_items:
            for item in self.weekly_forecast_items:
                if hasattr(item, 'cleanup') and callable(item.cleanup):
                    item.cleanup()
            self.weekly_forecast_items.clear()
        
        logging.info("WeatherView cleanup complete.")
