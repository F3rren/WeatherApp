"""
Weather View for the MeteoApp.
Handles the display of weather information.
"""

import flet as ft
from datetime import datetime

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
        self.api_service = ApiService()
        self.weather_data = {}
        self.city_info = {}
        self.text_color = "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff"
        
        # UI components
        self.info_container = ft.Container(content=ft.Text("Caricamento..."))
        self.weekly_container = ft.Container()
        self.chart_container = ft.Container()
        self.air_pollution_container = ft.Container()
        self.air_pollution_chart_container = ft.Container()

    async def update_by_city(self, city: str, language: str, unit: str) -> None:
        """Update weather information by city name"""
        # Get weather data
        self.weather_data = self.api_service.get_weather_data(
            city=city,
            language=language,
            unit=unit
        )
        
        # Get city information
        self.city_info = self.api_service.get_city_info(city)
        
        # Extract coordinates from city info if available
        lat = None
        lon = None
        if self.city_info and len(self.city_info) > 0:
            lat = self.city_info[0].get("lat")
            lon = self.city_info[0].get("lon")
        
        # Update UI
        await self._update_ui(city, lat=lat, lon=lon)
    
    async def update_by_coordinates(self, lat: float, lon: float, language: str, unit: str) -> None:
        """Update weather information by coordinates"""
        # Get weather data
        self.weather_data = self.api_service.get_weather_data(
            lat=lat,
            lon=lon,
            language=language,
            unit=unit
        )
        
        # Get city name from coordinates
        city = self.api_service.get_city_by_coordinates(lat, lon)
        
        # Update UI
        await self._update_ui(city, is_current_location=True, lat=lat, lon=lon)
    
    async def _update_ui(self, city: str, is_current_location: bool = False, lat: float = None, lon: float = None) -> None:
        """Update UI with weather data"""
        if not self.weather_data:
            return
        
        # Update main information
        await self._update_main_info(city, is_current_location)
        
        # Update weekly forecast
        await self._update_weekly_forecast()
        
        # Update temperature chart
        await self._update_temperature_chart()

        # Use provided coordinates if available, otherwise try to extract from weather data
        try:
            if lat is not None and lon is not None:
                # Use provided coordinates
                await self._update_air_pollution(lat, lon)
                await self._update_air_pollution_chart(lat, lon)
            elif "city" in self.weather_data and "coord" in self.weather_data["city"]:
                # Extract coordinates from weather data
                lat = self.weather_data["city"]["coord"]["lat"]
                lon = self.weather_data["city"]["coord"]["lon"]
                await self._update_air_pollution(lat, lon)
                await self._update_air_pollution_chart(lat, lon)
            else:
                print("No coordinates available for air pollution data")
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error getting coordinates for air pollution: {e}")
        
        # Update page
        self.page.update()
    
    async def _update_main_info(self, city: str, is_current_location: bool) -> None:
        """Update main weather information"""
        # Get weather data
        temperature = self.api_service.get_current_temperature(self.weather_data)
        feels_like = self.api_service.get_feels_like_temperature(self.weather_data)
        humidity = self.api_service.get_humidity(self.weather_data)
        wind_speed = self.api_service.get_wind_speed(self.weather_data)
        pressure = self.api_service.get_pressure(self.weather_data)
        icon_code = self.api_service.get_weather_icon_code(self.weather_data)
        # Air pollution will be updated separately

        # Get location string
        location = ""
        if is_current_location:
            location = "📍 Posizione attuale"
        elif self.city_info and len(self.city_info) > 0:
            location_data = self.city_info[0]
            name = location_data.get("name", "")
            country = location_data.get("country", "")
            state = location_data.get("state", "")
            location = f"{name}, {country} {state}".strip()
        else:
            location = city
        
        # Create components
        weather_card = WeatherCard(self.page)
        
        # Main weather info
        main_info = MainWeatherInfo(
            city=city,
            location=location,
            temperature=temperature,
            weather_icon=icon_code,
            text_color=self.text_color
        )
        
        # Hourly forecast
        hourly_data = self.api_service.get_hourly_forecast_data(self.weather_data)
        hourly_items = []
        
        for i, item in enumerate(hourly_data[:6]):
            time = item["dt_txt"]
            dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            hour = dt.strftime("%H:%M")
            
            hourly_item = HourlyForecastItems(
                time=hour,
                icon_code=item["weather"][0]["icon"],
                temperature=round(item["main"]["temp"])
            )
            
            hourly_items.append(hourly_item.build())
            
            if i < 5:
                hourly_items.append(
                    ft.Container(
                        content=ft.VerticalDivider(width=1, thickness=1, color="white", opacity=0.5),
                        height=100,
                        alignment=ft.alignment.center,
                    )
                )
        
        hourly_forecast = ft.Row(controls=hourly_items, expand=True)
        
        # Air condition
        air_condition = AirConditionInfo(
            feels_like=feels_like,
            humidity=humidity,
            wind_speed=wind_speed,
            pressure=pressure,
            text_color=self.text_color
        )
        
        # Update container
        self.info_container.content = weather_card.build(
            ft.Column([
                main_info.build(),
                hourly_forecast,
                air_condition.build(),
            ])
        )

    async def _update_weekly_forecast(self) -> None:
        """Update weekly forecast"""
        # Get weekly forecast data
        weekly_data = self.api_service.get_weekly_forecast_data(self.weather_data)
        
        # Create components
        weather_card = WeatherCard(self.page)
        forecast_items = []
        
        for i, day_data in enumerate(weekly_data):
            forecast_item = DailyForecastItems(
                day=day_data["day_name"],
                icon_code=day_data["icon"],
                description=day_data["description"],
                temp_min=day_data["temp_min"],
                temp_max=day_data["temp_max"],
                text_color=self.text_color
            )
            
            forecast_items.append(ft.Container(content=forecast_item.build()))
            
            if i < len(weekly_data) - 1:
                forecast_items.append(
                    ft.Container(
                        content=ft.Divider(thickness=0.5, color="white", opacity=1),
                    )
                )
        
        # Update container
        self.weekly_container.content = weather_card.build(
            ft.Column(controls=forecast_items, expand=True)
        )
    
    async def _update_temperature_chart(self) -> None:
        """Update temperature chart"""
        # Get temperature data
        forecast_data = self.api_service.get_daily_forecast_data(self.weather_data)
        days = self.api_service.get_upcoming_days()
        
        # Create components
        weather_card = WeatherCard(self.page)
        
        # Temperature chart
        temp_chart = TemperatureChart(
            page=self.page,
            days=days,
            temp_min=forecast_data["temp_min"],
            temp_max=forecast_data["temp_max"],
            text_color=self.text_color
        )
        
        # Update container
        self.chart_container.content = weather_card.build(temp_chart.build())
    
    async def _update_air_pollution(self, lat: float, lon: float) -> None:
        """Update air pollution container"""
        print(f"Updating air pollution with coordinates: lat={lat}, lon={lon}")
        # Create air pollution component using our new component
        air_pollution = AirPollution(
            page=self.page,
            lat=lat,
            lon=lon
        )
        
        # Update container
        self.air_pollution_container.content = air_pollution.build()
        print("Air pollution container updated")

    async def _update_air_pollution_chart(self, lat: float, lon: float) -> None:
        """Update air pollution chart container"""
        print(f"Updating air pollution chart with coordinates: lat={lat}, lon={lon}")
        # Create air pollution chart component
        air_pollution_chart = AirPollutionChart(
            page=self.page,
            lat=lat,
            lon=lon
        )
        
        # Update container with the chart
        self.air_pollution_chart_container.content = air_pollution_chart.build(lat, lon)
        print("Air pollution chart container updated")

        

    def get_containers(self) -> tuple:
        """Get the containers for the view"""
        return (self.info_container, 
                self.weekly_container, 
                self.chart_container, 
                self.air_pollution_container, 
                self.air_pollution_chart_container)
