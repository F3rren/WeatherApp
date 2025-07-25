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
        
        Returns:
            Dict containing weather data or error information with structure:
            {
                'success': bool,
                'data': dict (if success=True),
                'error': {
                    'type': str ('city_not_found', 'network_error', 'api_error', etc.),
                    'message': str,
                    'code': int (HTTP status code if applicable)
                } (if success=False)
            }
        """
        try:
            #logging.info(f"get_weather_data called with: city='{city}', lat={lat}, lon={lon}, language='{language}', unit='{unit}'")
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
                #logging.info(f"Making API call with coordinates. URL: {url}, params: {params}")
                response = requests.get(url, params=params)
                response.raise_for_status()
                return {
                    'success': True,
                    'data': response.json()
                }
            
            # Then attempt with city name if lat/lon failed or were not provided
            if city:
                city = self._normalize_city_name(city)
                params = {
                    "q": city,
                    "appid": self._api_key,
                    "units": unit,
                    "lang": language
                }
                #logging.info(f"Making API call with city. URL: {url}, params: {params}")
                response = requests.get(url, params=params)
                response.raise_for_status()
                result = response.json()
                
                # Check if city was found (OpenWeatherMap returns cod=200 but empty list for invalid cities)
                if result.get('cod') == '404' or (result.get('list') and len(result.get('list', [])) == 0):
                    return {
                        'success': False,
                        'error': {
                            'type': 'city_not_found',
                            'message': f"City '{city}' not found. Please check the spelling and try again.",
                            'code': 404
                        }
                    }
                
                #logging.info(f"API call successful. Response contains {len(result.get('list', []))} forecast items")
                return {
                    'success': True,
                    'data': result
                }
            else:
                logging.error("Either city or lat/lon must be provided and result in a successful API call.")
                return {
                    'success': False,
                    'error': {
                        'type': 'invalid_input',
                        'message': 'Either city name or coordinates must be provided.',
                        'code': 400
                    }
                }
        except requests.exceptions.HTTPError as http_err:
            # Specific handling for HTTP errors (4xx, 5xx)
            status_code = http_err.response.status_code if http_err.response else 0
            
            if status_code == 404:
                error_type = 'city_not_found'
                error_message = f"City '{city or 'Unknown'}' not found. Please check the spelling and try again."
            elif status_code == 401:
                error_type = 'api_key_error'
                error_message = "Invalid API key. Please check your API configuration."
            elif status_code >= 500:
                error_type = 'server_error'
                error_message = "Weather service is temporarily unavailable. Please try again later."
            else:
                error_type = 'api_error'
                error_message = f"Weather service error: {str(http_err)}"
            
            if lat is not None and lon is not None and city:
                # This block means coordinate call failed, now try city
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
                    result = response.json()
                    
                    # Check for city not found
                    if result.get('cod') == '404' or (result.get('list') and len(result.get('list', [])) == 0):
                        return {
                            'success': False,
                            'error': {
                                'type': 'city_not_found',
                                'message': f"City '{city}' not found. Please check the spelling and try again.",
                                'code': 404
                            }
                        }
                    
                    return {
                        'success': True,
                        'data': result
                    }
                except requests.exceptions.RequestException as e_city:
                    logging.error(f"Error fetching weather data for city '{city}' after coordinate failure: {e_city}")
                    return {
                        'success': False,
                        'error': {
                            'type': 'city_not_found',
                            'message': f"City '{city}' not found. Please check the spelling and try again.",
                            'code': 404
                        }
                    }
            else:
                logging.error(f"HTTP error fetching weather data: {http_err}")
                return {
                    'success': False,
                    'error': {
                        'type': error_type,
                        'message': error_message,
                        'code': status_code
                    }
                }
        except requests.exceptions.RequestException as e:
            # General request exceptions (network issues, etc.)
            logging.error(f"Error fetching weather data: {e}")
            return {
                'success': False,
                'error': {
                    'type': 'network_error',
                    'message': 'Network error. Please check your internet connection and try again.',
                    'code': 0
                }
            }
    
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
    
    def get_city_by_coordinates(self, lat: float, lon: float, language: str = "en") -> str:
        """
        Get city name from coordinates using reverse geocoding.
        
        Args:
            lat: Latitude
            lon: Longitude
            language: Language code for localization
            
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
    
    def get_location_by_coordinates(self, lat: float, lon: float, language: str = "en") -> dict:
        """
        Get complete location information from coordinates using reverse geocoding.
        
        Args:
            lat: Latitude
            lon: Longitude
            language: Language code for localization
            
        Returns:
            Dictionary with location information
        """
        try:
            url = f"{API_BASE_URL}{API_REVERSE_GEO_ENDPOINT}"
            params = {"lat": lat, "lon": lon, "limit": 1, "appid": self._api_key}
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                location_data = data[0]
                return {
                    "name": location_data.get("name", "Unknown"),
                    "state": location_data.get("state", ""),
                    "country": location_data.get("country", ""),
                    "lat": location_data.get("lat", lat),
                    "lon": location_data.get("lon", lon)
                }
            return {
                "name": "Current Location",
                "state": "",
                "country": "",
                "lat": lat,
                "lon": lon
            }
        except requests.exceptions.RequestException as e:
            logging.error(f"Error in reverse geocoding: {e}")
            return {
                "name": "Current Location",
                "state": "",
                "country": "",
                "lat": lat,
                "lon": lon
            }
    
    def get_current_temperature(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract current temperature from weather data"""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                return round(data["list"][0]["main"]["temp"])
            elif "main" in data and "temp" in data["main"]:
                return round(data["main"]["temp"])
            else:
                logging.warning("Temperature data not found in expected format")
                return None
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting current temperature: {e}")
            return None
    
    def get_feels_like_temperature(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract feels like temperature from weather data"""
        try:
            # Handle None or empty data gracefully
            if not data:
                return None
                
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                first_item = data["list"][0]
                if "main" in first_item and "feels_like" in first_item["main"]:
                    return round(first_item["main"]["feels_like"])
                else:
                    # Only log warning if we have actual data but it's in wrong format
                    if first_item:  # Don't warn for empty data
                        logging.warning(f"Feels like temperature missing in forecast item main: {first_item.get('main', {}).keys() if 'main' in first_item else 'main key missing'}")
                    return None
            elif "main" in data and "feels_like" in data["main"]:
                return round(data["main"]["feels_like"])
            else:
                # Only warn if we have substantial data but can't parse it
                if data and len(data.keys()) > 1:  # More than just basic keys
                    logging.warning("Feels like temperature data not found in expected format")
                return None
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting feels like temperature: {e}")
            return None
    
    def get_min_max_temperature(self, data: Dict[str, Any]) -> Tuple[Optional[int], Optional[int]]:
        """Extract min and max temperature from weather data"""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                temp_min = round(data["list"][0]["main"]["temp_min"])
                temp_max = round(data["list"][0]["main"]["temp_max"])
                return temp_min, temp_max
            elif "main" in data:
                temp_min = round(data["main"].get("temp_min", data["main"]["temp"]))
                temp_max = round(data["main"].get("temp_max", data["main"]["temp"]))
                return temp_min, temp_max
            else:
                logging.warning("Min/max temperature data not found in expected format")
                return None, None
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting min/max temperature: {e}")
            return None, None
    
    def get_wind_speed(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract wind speed from weather data"""
        try:
            # Handle None or empty data gracefully
            if not data:
                return None
                
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                first_item = data["list"][0]
                if "wind" in first_item and "speed" in first_item["wind"]:
                    return round(first_item["wind"]["speed"])
                else:
                    # Only log warning if we have actual data but it's in wrong format
                    if first_item:  # Don't warn for empty data
                        logging.warning(f"Wind speed missing in forecast item: {first_item.get('wind', {}).keys() if 'wind' in first_item else 'wind key missing'}")
                    return None
            elif "wind" in data and "speed" in data["wind"]:
                return round(data["wind"]["speed"])
            else:
                # Only warn if we have substantial data but can't parse it
                if data and len(data.keys()) > 1:
                    logging.warning("Wind speed data not found in expected format")
                return None
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting wind speed: {e}")
            return None
    
    def get_wind_direction(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract wind direction from weather data"""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                return data["list"][0]["wind"].get("deg", None)
            elif "wind" in data:
                return data["wind"].get("deg", None)
            else:
                return None
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting wind direction: {e}")
            return None
    
    def get_wind_gust(self, data: Dict[str, Any]) -> Optional[float]:
        """Extract wind gust speed from weather data"""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                return data["list"][0]["wind"].get("gust", None)
            elif "wind" in data:
                return data["wind"].get("gust", None)
            else:
                return None
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting wind gust: {e}")
            return None
    
    def get_humidity(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract humidity from weather data"""
        try:
            # Handle None or empty data gracefully
            if not data:
                return None
                
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                first_item = data["list"][0]
                if "main" in first_item and "humidity" in first_item["main"]:
                    return first_item["main"]["humidity"]
                else:
                    # Only log warning if we have actual data but it's in wrong format
                    if first_item:  # Don't warn for empty data
                        logging.warning(f"Humidity missing in forecast item main: {first_item.get('main', {}).keys() if 'main' in first_item else 'main key missing'}")
                    return None
            elif "main" in data and "humidity" in data["main"]:
                return data["main"]["humidity"]
            else:
                # Only warn if we have substantial data but can't parse it
                if data and len(data.keys()) > 1:
                    logging.warning("Humidity data not found in expected format")
                return None
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting humidity: {e}")
            return None
    
    def get_pressure(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract pressure from weather data"""
        try:
            # Handle None or empty data gracefully
            if not data:
                return None
                
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                first_item = data["list"][0]
                if "main" in first_item and "pressure" in first_item["main"]:
                    return round(first_item["main"]["pressure"])
                else:
                    # Only log warning if we have actual data but it's in wrong format
                    if first_item:  # Don't warn for empty data
                        logging.warning(f"Pressure missing in forecast item main: {first_item.get('main', {}).keys() if 'main' in first_item else 'main key missing'}")
                    return None
            elif "main" in data and "pressure" in data["main"]:
                return round(data["main"]["pressure"])
            else:
                # Only warn if we have substantial data but can't parse it
                if data and len(data.keys()) > 1:
                    logging.warning("Pressure data not found in expected format")
                return None
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting pressure: {e}")
            return None
    
    def get_weather_icon_code(self, data: Dict[str, Any]) -> str:
        """Extract weather icon code from weather data"""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                return data["list"][0]["weather"][0]["icon"]
            elif "weather" in data and isinstance(data["weather"], list) and len(data["weather"]) > 0:
                return data["weather"][0]["icon"]
            else:
                logging.warning("Weather icon data not found in expected format")
                return "01d"  # Default clear sky icon
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting weather icon: {e}")
            return "01d"  # Default clear sky icon
    
    def get_weather_description(self, data: Dict[str, Any]) -> str:
        """Extract weather description from weather data"""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                return data["list"][0]["weather"][0]["description"]
            elif "weather" in data and isinstance(data["weather"], list) and len(data["weather"]) > 0:
                return data["weather"][0]["description"]
            else:
                logging.warning("Weather description data not found in expected format")
                return "Unknown"
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
        from ui.layout.sections.informationtab.daily_forecast import DailyForecast

        
        try:
            # Get weather data
            weather_response = self.get_weather_data(self.city)
            if not weather_response.get('success', False):
                error_info = weather_response.get('error', {})
                error_message = error_info.get('message', 'No data available')
                return ft.Text(error_message)
            
            weather_data = weather_response.get('data', {})
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
            
            for day_data in forecast_days:
                day_item = DailyForecast(
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
            return ft.Text("Error loading forecast")

    def get_visibility(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract visibility data from weather data (in meters)."""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                return data["list"][0].get("visibility", None)
            elif "visibility" in data:
                return data["visibility"]
            else:
                return None
        except (KeyError, IndexError, TypeError):
            return None

    def get_dew_point(self, data: Dict[str, Any]) -> Optional[int]:
        """Calculate dew point from temperature and humidity."""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                main_data = data["list"][0].get("main", {})
            elif "main" in data:
                main_data = data["main"]
            else:
                return None
                
            temp = main_data.get("temp")
            humidity = main_data.get("humidity")
            
            if temp is not None and humidity is not None:
                # Magnus formula for dew point calculation
                import math
                a = 17.27
                b = 237.7
                alpha = ((a * temp) / (b + temp)) + math.log(humidity / 100.0)
                dew_point = (b * alpha) / (a - alpha)
                return round(dew_point)
            return None
        except (KeyError, IndexError, TypeError, ValueError):
            return None

    def get_uv_index(self, data: Dict[str, Any]) -> Optional[float]:
        """Extract UV index from weather data (if available)."""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                weather_data = data["list"][0].get("weather", [])
            elif "weather" in data and isinstance(data["weather"], list):
                weather_data = data["weather"]
            else:
                return None
                
            if weather_data:
                weather_id = weather_data[0].get("id", 800)
                # Estimate UV based on weather conditions (this is a simulation)
                if weather_id < 300:  # Thunderstorm
                    return 2.0
                elif weather_id < 400:  # Drizzle
                    return 3.0
                elif weather_id < 600:  # Rain
                    return 3.0
                elif weather_id < 700:  # Snow
                    return 2.0
                elif weather_id < 800:  # Atmosphere (fog, etc.)
                    return 4.0
                elif weather_id == 800:  # Clear sky
                    return 8.0
                else:  # Cloudy
                    return 6.0
            return None
        except (KeyError, IndexError, TypeError):
            return None

    def get_cloud_coverage(self, data: Dict[str, Any]) -> Optional[int]:
        """Extract cloud coverage percentage from weather data."""
        try:
            # Handle both forecast format (list) and current weather format (direct)
            if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
                clouds_data = data["list"][0].get("clouds", {})
                return clouds_data.get("all", None)
            elif "clouds" in data:
                return data["clouds"].get("all", None)
            else:
                return None
        except (KeyError, IndexError, TypeError):
            return None
