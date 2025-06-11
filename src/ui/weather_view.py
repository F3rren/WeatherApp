"""
Weather View for the MeteoApp.
Handles the display of weather information.
"""

import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME

from services.api_service import ApiService

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
        # Backend service for all data fetching/processing
        self.api_service = ApiService()
        self.weather_data = {}
        self.city_info = {}
        # Store current coordinates for theme change rebuilds
        self.current_lat = None
        self.current_lon = None
        self.current_city = None
        # Initialize text_color based on the current theme
        self._update_text_color() 
        
        # Register for theme change events
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_change)
            state_manager.register_observer("language_event", self.handle_language_change)

        self.info_container = ft.Container(content=ft.Text("Caricamento...", color=self.text_color)) # Apply initial text color
        self.hourly_container = ft.Container()
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

    def handle_language_change(self, event_data=None):
        """Aggiorna i contenuti della UI quando cambia la lingua."""
        # Forza il rebuild dei componenti principali con la nuova lingua
        if self.current_city:
            # Recupera la lingua e l'unità correnti dallo state_manager
            state_manager = self.page.session.get('state_manager')
            language = state_manager.get_state('language') if state_manager else 'en'
            unit = state_manager.get_state('unit') if state_manager else 'metric'
            # Aggiorna la UI principale
            import asyncio
            asyncio.create_task(self.update_by_city(self.current_city, language, unit))

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
            location = "📍 Posizione attuale"
        elif self.city_info:
            data = self.city_info[0]
            location = ", ".join(filter(None, [data.get("name"), data.get("state"), data.get("country")]))
        else:
            location = city

        # Costruisce le sezioni dell'interfaccia
        main_info = MainWeatherInfo(city, location, temperature, icon_code, self.text_color, self.page).build()

        air_condition = AirConditionInfo(feels_like, humidity, wind_speed, pressure, self.text_color, self.page).build()        # Assembla il contenuto e aggiorna il contenitore
        self.info_container.content = WeatherCard(self.page).build(
            ft.Column(
                controls=[main_info, air_condition],
                expand=True,
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH  # Assicura che i figli si estendano
            )
        )
        self.info_container.expand = True
        
    async def _update_weekly_forecast(self) -> None:
        """Frontend: Updates weekly forecast UI"""
        weekly_data = self.api_service.get_weekly_forecast_data(self.weather_data)
        weather_card = WeatherCard(self.page) # Pass page if WeatherCard needs theme context
        forecast_items_controls = [] # Renamed
        self._update_text_color() # Ensure text_color is current
        for i, day_data in enumerate(weekly_data):            
            forecast_item_obj = DailyForecastItems( # Create instance
                day=day_data["day_key"],
                icon_code=day_data["icon"],
                temp_min=day_data["temp_min"],
                temp_max=day_data["temp_max"],
                text_color=self.text_color,
                page=self.page # Pass page for theme observation
            )
            forecast_items_controls.append(ft.Container(content=forecast_item_obj.build())) # Append built control
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
        forecast_data = self.api_service.get_daily_forecast_data(self.weather_data)
        days = self.api_service.get_upcoming_days()
        weather_card = WeatherCard(self.page) # Pass page if WeatherCard needs theme context
        self._update_text_color() # Ensure text_color is current
        temp_chart = TemperatureChart(
            page=self.page,
            days=days,
            temp_min=forecast_data["temp_min"],
            temp_max=forecast_data["temp_max"],
            text_color=self.text_color
        )
        self.chart_container.content = weather_card.build(temp_chart.build())
        
    async def _update_hourly_container(self) -> None:
        """Frontend: Updates air pollution chart UI"""
        weather_card = WeatherCard(self.page) # Pass page if WeatherCard needs theme context
        self._update_text_color() # Ensure text_color is current

        # Costruisce la riga di previsioni orarie (massimo 6)
        hourly_data = self.api_service.get_hourly_forecast_data(self.weather_data)[:6]
        # Utilizza la nuova classe per costruire la sezione delle previsioni orarie
        hourly_forecast = HourlyForecastDisplay(
            hourly_data=hourly_data,
            text_color=self.text_color,
            page=self.page
        )

        self.hourly_container.content = weather_card.build(hourly_forecast.build())
    
    async def _update_air_pollution(self, lat: float, lon: float) -> None:
        """Frontend: Updates air pollution UI"""
        self._update_text_color() # Ensure text_color is current
        air_pollution = AirPollution( # Assuming AirPollution is a class
            page=self.page,
            lat=lat,
            lon=lon,
            text_color=self.text_color, # Pass text_color
        )
        self.air_pollution_container.content = air_pollution.build()
        
    async def _update_air_pollution_chart(self, lat: float, lon: float) -> None:
        """Frontend: Updates air pollution chart UI"""
        self._update_text_color() # Ensure text_color is current
        air_pollution_chart = AirPollutionChart( # Assuming AirPollutionChart is a class
            page=self.page,
            lat=lat,
            lon=lon,
            text_color=self.text_color # Pass text_color
        )
        self.air_pollution_chart_container.content = air_pollution_chart.build(lat, lon)

    def get_containers(self) -> tuple:
        """Frontend: Returns UI containers for display"""
        return (
            self.info_container,
            self.hourly_container,
            self.weekly_container,
            self.chart_container,
            self.air_pollution_container,
            self.air_pollution_chart_container
        )
