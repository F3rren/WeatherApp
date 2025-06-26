"""
API Service for the MeteoApp.
Handles all API calls to the OpenWeatherMap API.
"""

import os
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, List, Optional
from dotenv import load_dotenv
import unicodedata
import asyncio

from utils.config import (
    API_BASE_URL,
    API_WEATHER_ENDPOINT,
    API_GEO_ENDPOINT,
    API_REVERSE_GEO_ENDPOINT,
    API_AIR_POLLUTION_ENDPOINT
)

class ApiService:
    """
    Service for making API calls to the OpenWeatherMap API.
    """
    
    def __init__(self, page=None, city=None, language="en", unit="metric"):
        load_dotenv()
        self._api_key = os.getenv("API_KEY")
        if not self._api_key:
            logging.error("API key not found. Please set the API_KEY environment variable.")
        
        # Supporto per la versione estesa del costruttore
        self.page = page
        self.city = city
        self.language = language
        self.unit = unit

    def _normalize_city_name(self, city: str) -> str:
        if city:
            city = city.replace("’", "'").replace("‘", "'")
            city = unicodedata.normalize("NFKD", city)
        return city
    
    def get_weather_data(self, city: str = None, lat: float = None, lon: float = None, 
                        language: str = "en", unit: str = "metric") -> Dict[str, Any]:
        """
        Get weather forecast data for a city or coordinates.
        Attempts first with coordinates, then with city name if coordinates are not available.
        """
        try:
            url = f"{API_BASE_URL}{API_WEATHER_ENDPOINT}"
            # First attempt with coordinates
            if lat is not None and lon is not None:
                params = {
                    "lat": lat,
                    "lon": lon,
                    "units": unit,
                    "lang": language,
                    "appid": self._api_key
                }
                response = requests.get(url, params=params)
                response.raise_for_status() # Added for consistent error handling
                # if response.status_code == 200: # No longer needed due to raise_for_status
                return response.json()
                # If the request with coordinates fails (e.g. 4xx, 5xx), raise_for_status will throw an exception
                # logging.warning("Coordinate non valide o nessun dato trovato, provo con nome città...") # Commented out, error handled by exception
            
            # Then attempt with city name if lat/lon failed or were not provided
            if city:
                city = self._normalize_city_name(city)
                params = {
                    "q": city,
                    "appid": self._api_key,
                    "units": unit,
                    "lang": language
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                return response.json()
            else:
                # This case should ideally not be reached if called from WeatherView,
                # as WeatherView ensures either city or lat/lon.
                # If coordinate request failed above, and no city was provided, this is an issue.
                # However, the original logic would attempt city if coordinate call returned non-200,
                # but if city is None here, it's an issue.
                # For now, keeping the original error log if no city and no successful coord fetch.
                logging.error("Either city or lat/lon must be provided and result in a successful API call.")
                return {}
        except requests.exceptions.HTTPError as http_err:
            # Specific handling for HTTP errors (4xx, 5xx)
            if lat is not None and lon is not None and city:
                # This block means coordinate call failed, now try city
                #logging.warning(f"Coordinate call failed ({http_err}), trying with city name '{city}'...")
                try:
                    city_normalized = self._normalize_city_name(city)
                    params = {
                        "q": city_normalized,
                        "appid": self._api_key,
                        "units": unit,
                        "lang": language
                    }
                    response = requests.get(url, params=params)
                    response.raise_for_status()
                    return response.json()
                except requests.exceptions.RequestException as e_city:
                    logging.error(f"Error fetching weather data for city '{city}' after coordinate failure: {e_city}")
                    return {}
            else:
                logging.error(f"HTTP error fetching weather data: {http_err}")
                return {}
        except requests.exceptions.RequestException as e:
            # General request exceptions (network issues, etc.)
            logging.error(f"Error fetching weather data: {e}")
            return {}
    
    def get_city_info(self, city: str) -> List[Dict[str, Any]]:
        """
        Get geographic information for a city.
        
        Args:
            city: City name
            
        Returns:
            List of dictionaries containing city information
        """
        try:
            url = f"{API_BASE_URL}{API_GEO_ENDPOINT}"
            params = {"q": city, "limit": 5, "appid": self._api_key}
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching city information: {e}")
            return []
    
    def get_city_by_coordinates(self, lat: float, lon: float) -> str:
        """
        Get city name from coordinates using reverse geocoding.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            City name
        """
        try:
            url = f"{API_BASE_URL}{API_REVERSE_GEO_ENDPOINT}"
            params = {"lat": lat, "lon": lon, "limit": 1, "appid": self._api_key}
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                return data[0].get("name", "Current Location")
            return "Current Location"
        except requests.exceptions.RequestException as e:
            logging.error(f"Error in reverse geocoding: {e}")
            return "Current Location"
    
    def get_current_temperature(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract current temperature from weather data"""
        try:
            return round(data["list"][0]["main"]["temp"])
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting current temperature: {e}")
            return None
    
    def get_feels_like_temperature(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract feels like temperature from weather data"""
        try:
            return round(data["list"][0]["main"]["feels_like"])
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting feels like temperature: {e}")
            return None
    
    def get_min_max_temperature(self, data: Dict[str, Any]) -> Tuple[Optional[int], Optional[int]]:
        """Extract min and max temperature from weather data"""
        try:
            temp_min = round(data["list"][0]["main"]["temp_min"])
            temp_max = round(data["list"][0]["main"]["temp_max"])
            return temp_min, temp_max
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting min/max temperature: {e}")
            return None, None
    
    def get_wind_speed(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract wind speed from weather data"""
        try:
            return round(data["list"][0]["wind"]["speed"])
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting wind speed: {e}")
            return None
    
    def get_humidity(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract humidity from weather data"""
        try:
            return data["list"][0]["main"]["humidity"]
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting humidity: {e}")
            return None
    
    def get_pressure(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract pressure from weather data"""
        try:
            return round(data["list"][0]["main"]["pressure"])
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting pressure: {e}")
            return None
    
    def get_weather_icon_code(self, data: Dict[str, Any]) -> str:
        """Extract weather icon code from weather data"""
        try:
            return data["list"][0]["weather"][0]["icon"]
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting weather icon: {e}")
            return "01d"  # Default clear sky icon
    
    def get_weather_description(self, data: Dict[str, Any]) -> str:
        """Extract weather description from weather data"""
        try:
            return data["list"][0]["weather"][0]["description"]
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting weather description: {e}")
            return "Unknown"
    
    def get_upcoming_days(self, days: int = 5) -> List[str]:
        """Get list of upcoming day name keys (lowercase English full name)."""
        today = datetime.now()
        # Return lowercase English full day name as key for TranslationService
        return [(today + timedelta(days=i)).strftime("%A").lower() for i in range(days)]
    
    def get_daily_forecast_data(self, data: Dict[str, Any], days: int = 5) -> Dict[str, List]:
        """
        Process weather data to get daily min/max temperatures
        
        Returns:
            Dictionary with 'temp_min' and 'temp_max' lists
        """
        try:
            items = data["list"]
            daily_data = {}
            
            # Group items by day
            for item in items:
                dt_txt = item["dt_txt"]
                date_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
                day_key = date_obj.strftime("%Y-%m-%d")
                
                if day_key not in daily_data:
                    daily_data[day_key] = []
                daily_data[day_key].append(item)
            
            # Calculate min/max for each day
            temp_min = []
            temp_max = []
            
            for i, (day_key, items_in_day) in enumerate(sorted(daily_data.items())[:days]):
                # Calculate min and max temperatures for the day
                day_temp_min = min([x["main"]["temp_min"] for x in items_in_day])
                day_temp_max = max([x["main"]["temp_max"] for x in items_in_day])
                
                temp_min.append(day_temp_min)
                temp_max.append(day_temp_max)
            
            return {
                "temp_min": temp_min,
                "temp_max": temp_max
            }
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error processing daily forecast data: {e}")
            return {"temp_min": [], "temp_max": []}
    
    def get_hourly_forecast_data(self, data: Dict[str, Any], hours: int = 6) -> List[Dict[str, Any]]:
        """
        Process weather data to get hourly forecast
        
        Returns:
            List of dictionaries with hourly forecast data
        """
        try:
            items = data["list"]
            return items[:hours]
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error processing hourly forecast data: {e}")
            return []
    
    def get_weekly_forecast_data(self, data: Dict[str, Any], days: int = 5) -> List[Dict[str, Any]]:
        """
        Process weather data to get daily forecast for multiple days
        
        Returns:
            List of dictionaries with daily forecast data, including a 'day_key'
        """
        try:
            items = data["list"]
            daily_data = {}
            
            # Group items by day
            for item in items:
                dt_txt = item["dt_txt"]
                date_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
                day_key_str = date_obj.strftime("%Y-%m-%d") # Internal key for grouping
                
                if day_key_str not in daily_data:
                    daily_data[day_key_str] = []
                daily_data[day_key_str].append(item)
            
            # Process data for each day
            result = []
            for i, (day_key_str, items_in_day) in enumerate(sorted(daily_data.items())[:days]):
                date_obj = datetime.strptime(day_key_str, "%Y-%m-%d")
                
                # Calculate min and max temperatures for the day
                temp_min = min([x["main"]["temp_min"] for x in items_in_day])
                temp_max = max([x["main"]["temp_max"] for x in items_in_day])
                
                # Get icon and description from noon if available, otherwise from first item
                icon_item = next((x for x in items_in_day if "12:00:00" in x["dt_txt"]), items_in_day[0])
                icon = icon_item["weather"][0]["icon"]
                description = icon_item["weather"][0]["description"]
                
                # Calculate additional daily statistics
                avg_humidity = round(sum(x["main"]["humidity"] for x in items_in_day) / len(items_in_day))
                avg_rain_probability = round(sum(x.get("pop", 0) for x in items_in_day) / len(items_in_day) * 100)
                avg_wind_speed = round(sum(x["wind"]["speed"] for x in items_in_day) / len(items_in_day), 1)
                avg_pressure = round(sum(x["main"]["pressure"] for x in items_in_day) / len(items_in_day))
                
                result.append({
                    "date": date_obj,
                    # Use lowercase English full day name as key for TranslationService
                    "day_key": date_obj.strftime("%A").lower(), 
                    "temp_min": round(temp_min),
                    "temp_max": round(temp_max),
                    "icon": icon,
                    "description": description,
                    "humidity": avg_humidity,
                    "rain_probability": avg_rain_probability,
                    "wind_speed": avg_wind_speed,
                    "pressure": avg_pressure
                })
            
            return result
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error processing weekly forecast data: {e}")
            return []


    def get_air_pollution(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get air pollution data for coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing processed air pollution data, or empty dict on error/no data.
        """
        try:
            url = f"{API_BASE_URL}{API_AIR_POLLUTION_ENDPOINT}"
            params = {"lat": lat, "lon": lon, "appid": self._api_key}
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            # Process the data to extract useful information
            if "list" in data and len(data["list"]) > 0:
                # Get the first forecast item (current or nearest time)
                pollution = data["list"][0]
                
                # Extract components and AQI
                components = pollution.get("components", {})
                aqi = pollution.get("main", {}).get("aqi", 0)
                
                # Return processed data
                result_data = { # Renamed to avoid conflict with outer 'result' in other methods
                    "aqi": aqi,  # Air Quality Index (1-5)
                    "co": components.get("co", 0),  # Carbon monoxide, μg/m3
                    "no": components.get("no", 0),  # Nitrogen monoxide, μg/m3
                    "no2": components.get("no2", 0),  # Nitrogen dioxide, μg/m3
                    "o3": components.get("o3", 0),  # Ozone, μg/m3
                    "so2": components.get("so2", 0),  # Sulphur dioxide, μg/m3
                    "pm2_5": components.get("pm2_5", 0),  # Fine particles, μg/m3                    "pm10": components.get("pm10", 0),  # Coarse particles, μg/m3
                    "nh3": components.get("nh3", 0)  # Ammonia, μg/m3
                }
                return result_data
            
            return {} # Return empty dict if no data in list
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching air pollution data: {e}")
            return {}
    
    async def get_air_pollution_async(self, lat: float, lon: float) -> dict:
        """
        Asynchronous version of get_air_pollution using run_in_executor to avoid blocking the event loop.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_air_pollution, lat, lon)
    
    def getDailyForecast(self):
        """
        Returns a flet Control containing the daily forecast.
        This method is specifically added to support DailyForecast component.
        
        Returns:
            A flet Control (Row) with the hourly forecast items.
        """
        import flet as ft
        from layout.frontend.weeklyweather.daily_forecast_items import DailyForecastItems
        from components.responsive_text_handler import ResponsiveTextHandler
        
        try:
            # Get weather data
            weather_data = self.get_weather_data(self.city)
            if not weather_data:
                return ft.Text("No data available")
            
            # Get forecast days
            forecast_days = self.get_weekly_forecast_data(weather_data)
            if not forecast_days:
                return ft.Text("No forecast data available")
                
            # Create items row
            items = []
            self.daily_forecast_items = []  # Store references for cleanup
            
            # Determina il colore del testo in base al tema
            text_color = "#1F1A1A" if self.page and self.page.theme_mode == ft.ThemeMode.LIGHT else "#adadad"
            
            # Use ResponsiveTextHandler for consistent text sizing
            for day_data in forecast_days:
                day_item = DailyForecastItems(
                    day=day_data["day_key"],
                    icon_code=day_data["icon"],
                    temp_min=day_data["temp_min"],
                    temp_max=day_data["temp_max"],
                    text_color=text_color,
                    page=self.page
                )
                self.daily_forecast_items.append(day_item)  # Save reference for cleanup
                items.append(day_item.build())
            
            # Crea la row con le previsioni
            forecast_row = ft.Row(controls=items, scroll=ft.ScrollMode.AUTO)
            
            return forecast_row
        except Exception as e:
            logging.error(f"Error in getDailyForecast: {e}")
            return ft.Text(f"Error loading forecast")
