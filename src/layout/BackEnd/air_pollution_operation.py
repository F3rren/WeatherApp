import logging
import requests
import os
from dotenv import load_dotenv

class AirPollutionOperation:
    """
    Class for handling air pollution data operations.
    Provides methods to fetch and process air pollution data from OpenWeatherMap API.
    """
    
    # Load environment variables
    load_dotenv()
    
    def __init__(self):
        """Initialize the AirPollutionOperation class"""
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            logging.error("API key not found. Please set the API_KEY environment variable.")
    
    def get_air_pollution(self, lat: float, lon: float) -> dict:
        """
        Get air pollution data for coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing processed air pollution data
        """
        logging.info(f"Fetching air pollution data for coordinates: lat={lat}, lon={lon}")
        try:
            url = "https://api.openweathermap.org/data/2.5/air_pollution"
            params = {"lat": lat, "lon": lon, "appid": self.api_key}
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logging.debug(f"Air pollution API response: {data}")
            
            # Process the data to extract useful information
            if "list" in data and len(data["list"]) > 0:
                # Get the first forecast item (current or nearest time)
                pollution = data["list"][0]
                
                # Extract components and AQI
                components = pollution.get("components", {})
                aqi = pollution.get("main", {}).get("aqi", 0)
                
                # Return processed data
                result = {
                    "aqi": aqi,  # Air Quality Index (1-5)
                    "co": components.get("co", 0),  # Carbon monoxide, μg/m3
                    "no": components.get("no", 0),  # Nitrogen monoxide, μg/m3
                    "no2": components.get("no2", 0),  # Nitrogen dioxide, μg/m3
                    "o3": components.get("o3", 0),  # Ozone, μg/m3
                    "so2": components.get("so2", 0),  # Sulphur dioxide, μg/m3
                    "pm2_5": components.get("pm2_5", 0),  # Fine particles, μg/m3
                    "pm10": components.get("pm10", 0),  # Coarse particles, μg/m3
                    "nh3": components.get("nh3", 0)  # Ammonia, μg/m3
                }
                logging.info("Air pollution data processed successfully")
                return result
            
            logging.warning("No air pollution data found in API response")
            return {}
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching air pollution data: {e}")
            return {}
