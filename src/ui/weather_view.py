"""
Weather View for the MeteoApp.
Handles the display of weather information.
"""

import flet as ft
from datetime import datetime
from config import LIGHT_THEME, DARK_THEME

from services.api_service import ApiService

from layout.frontend.weather_card import WeatherCard
from layout.frontend.weeklyweather.hourly_forecast_items import HourlyForecastItems
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

        self.info_container = ft.Container(content=ft.Text("Caricamento...", color=self.text_color), expand=True) # Apply initial text color and expand
        self.weekly_container = ft.Container(expand=True)
        self.chart_container = ft.Container(expand=True)
        self.air_pollution_container = ft.Container(expand=True)
        self.air_pollution_chart_container = ft.Container(expand=True)

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

        # Re-build air pollution components with new theme colors if data is available
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
                print("No coordinates available for air pollution data")
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error getting coordinates for air pollution: {e}")
        self.page.update()

    async def _update_main_info(self, city: str, is_current_location: bool) -> None:
        """Frontend: Updates main weather info UI"""
        # All data comes from backend service
        temperature = self.api_service.get_current_temperature(self.weather_data)
        feels_like = self.api_service.get_feels_like_temperature(self.weather_data)
        humidity = self.api_service.get_humidity(self.weather_data)
        wind_speed = self.api_service.get_wind_speed(self.weather_data)
        pressure = self.api_service.get_pressure(self.weather_data)
        icon_code = self.api_service.get_weather_icon_code(self.weather_data)
        location = ""
        if is_current_location:
            location = "📍 Posizione attuale"
        elif self.city_info and len(self.city_info) > 0:
            location_data = self.city_info[0]
            name = location_data.get("name", "")
            country = location_data.get("country", "")
            state = location_data.get("state", "")
            location = f"{name}, {state}, {country}".strip()
        else:
            location = city
        weather_card = WeatherCard(self.page)


        main_info = MainWeatherInfo(
            city=city,
            location=location,
            temperature=temperature,
            weather_icon=icon_code,
            text_color=self.text_color,
            page=self.page # Pass page for theme observation in MainWeatherInfo
        )
        hourly_data = self.api_service.get_hourly_forecast_data(self.weather_data)
        hourly_items_controls = [] # Renamed to avoid conflict if hourly_items was a list of data
        for i, item_data in enumerate(hourly_data[:6]): # Iterate over data
            time = item_data["dt_txt"]
            dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            hour = dt.strftime("%H:%M")
            # Assuming HourlyForecastItems also needs text_color or handles its own theme
            hourly_item_obj = HourlyForecastItems(
                time=hour,
                icon_code=item_data["weather"][0]["icon"],
                temperature=round(item_data["main"]["temp"]),
                text_color=self.text_color, # Pass text_color
                page=self.page # Pass page for theme observation
            )
            hourly_items_controls.append(hourly_item_obj.build()) # Append built control
            
            if i < 5: # Ensure we only add 5 dividers for 6 items
                divider_color = DARK_THEME.get("BORDER", ft.Colors.WHITE if self.page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLACK)
                hourly_items_controls.append(
                    ft.Container(
                        content=ft.VerticalDivider(width=1, thickness=1, color=divider_color, opacity=0.5),
                        height=120,  # Increased height for better visual separation
                        alignment=ft.alignment.center
                    )
                )

        # Use a container with padding to give the hourly forecast more room
        hourly_forecast_row = ft.Row(
            controls=hourly_items_controls, 
            expand=True, 
            scroll=ft.ScrollMode.ADAPTIVE, # Changed to ADAPTIVE
            alignment=ft.MainAxisAlignment.SPACE_EVENLY, # Changed to SPACE_EVENLY
            vertical_alignment=ft.CrossAxisAlignment.START # Align items to the start vertically
        )

        hourly_forecast_container = ft.Container(
            content=hourly_forecast_row,
            padding=ft.padding.symmetric(vertical=5), # Adjusted padding
            margin=ft.margin.symmetric(vertical=5), # Adjusted margin
            expand=True
        )

        air_condition = AirConditionInfo(
            feels_like=feels_like,
            humidity=humidity,
            wind_speed=wind_speed,
            pressure=pressure,
            text_color=self.text_color,
            page=self.page # Pass page for theme observation
        )
        self.info_container.content = weather_card.build(
            ft.Column(
                controls=[
                    main_info.build(),
                    hourly_forecast_container, # Use the new container
                    air_condition.build(),
                ],
                expand=True, # Ensure this column also expands
                spacing=10 # Add some spacing between sections
            )
        )

    async def _update_weekly_forecast(self) -> None:
        """Frontend: Updates weekly forecast UI"""
        weekly_data = self.api_service.get_weekly_forecast_data(self.weather_data)
        weather_card = WeatherCard(self.page) # Pass page if WeatherCard needs theme context
        forecast_items_controls = [] # Renamed
        self._update_text_color() # Ensure text_color is current
        for i, day_data in enumerate(weekly_data):
            forecast_item_obj = DailyForecastItems( # Create instance
                day=day_data["day_name"],
                icon_code=day_data["icon"],
                description=day_data["description"],
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
            self.weekly_container,
            self.chart_container,
            self.air_pollution_container,
            self.air_pollution_chart_container
        )
