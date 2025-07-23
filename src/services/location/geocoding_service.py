#!/usr/bin/env python3

import os
from typing import List, Dict, Optional
import logging
import aiohttp
from dataclasses import dataclass
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class LocationCandidate:
    """Rappresenta un candidato per una località."""
    name: str
    country: str
    country_code: str
    state: str = ""
    lat: float = 0.0
    lon: float = 0.0
    population: int = 0
    relevance_score: float = 0.0
    full_name: str = ""
    
    def __post_init__(self):
        if not self.full_name:
            parts = [self.name]
            if self.state:
                parts.append(self.state)
            parts.append(self.country)
            self.full_name = ", ".join(parts)


class GeocodingService:
    """Servizio di geocoding professionale con API esterne."""
    
    def __init__(self, api_key: str = None):
        # Trova il file .env nella cartella src
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(current_dir, '..', '..')
        env_path = os.path.join(src_dir, '.env')
        
        # Carica le variabili d'ambiente
        load_dotenv(env_path)
        
        # Prova entrambi i nomi di variabile
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY") or os.getenv("API_KEY")
        self.base_url = "https://api.openweathermap.org/geo/1.0"
        logger.info(f"GeocodingService inizializzato con API OpenWeatherMap - API Key: {'✅ Presente' if self.api_key else '❌ Mancante'}")
        logger.info(f"File .env caricato da: {env_path}")
        if not self.api_key:
            logger.error("ATTENZIONE: Chiave API OpenWeatherMap non trovata nelle variabili d'ambiente!")
    
    async def search_by_structured_input(self, city: str, state: str = "", country: str = "") -> List[LocationCandidate]:
        """Cerca località usando input strutturato (città, stato, paese)."""
        if not city.strip():
            return []
        
        # Costruisci la query strutturata
        query_parts = [city.strip()]
        if state.strip():
            query_parts.append(state.strip())
        if country.strip():
            query_parts.append(country.strip())
        
        query = ",".join(query_parts)
        
        try:
            return await self._geocode_query(query)
        except Exception as ex:
            logger.error(f"Errore nella ricerca strutturata: {ex}")
            return []
    
    async def _geocode_query(self, query: str, limit: int = 5) -> List[LocationCandidate]:
        """Esegue geocoding tramite API OpenWeatherMap."""
        url = f"{self.base_url}/direct"
        params = {
            "q": query,
            "limit": limit,
            "appid": self.api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_geocoding_response(data)
                    else:
                        logger.error(f"API Error: {response.status}")
                        return []
        except Exception as ex:
            logger.error(f"Errore nell'API geocoding: {ex}")
            return []
    
    def _parse_geocoding_response(self, data: List[Dict]) -> List[LocationCandidate]:
        """Converte la risposta API in LocationCandidate."""
        candidates = []
        
        for item in data:
            try:
                # Estrai informazioni dalla risposta API
                name = item.get("name", "")
                lat = float(item.get("lat", 0))
                lon = float(item.get("lon", 0))
                country = item.get("country", "")
                state = item.get("state", "")
                
                # Ottieni nome paese completo
                country_name = self._get_country_name(country)
                
                candidate = LocationCandidate(
                    name=name,
                    country=country_name,
                    country_code=country,
                    state=state,
                    lat=lat,
                    lon=lon
                )
                
                candidates.append(candidate)
                
            except Exception as ex:
                logger.warning(f"Errore nel parsing risultato geocoding: {ex}")
                continue
        
        return candidates
    
    def _get_country_name(self, country_code: str) -> str:
        """Converte codice paese in nome completo."""
        country_names = {
            "IT": "Italia", "FR": "Francia", "ES": "Spagna", "DE": "Germania",
            "GB": "Regno Unito", "US": "Stati Uniti", "CH": "Svizzera",
            "AT": "Austria", "NL": "Paesi Bassi", "BE": "Belgio", "PT": "Portogallo",
            "GR": "Grecia", "PL": "Polonia", "CZ": "Repubblica Ceca", "HU": "Ungheria",
            "RO": "Romania", "BG": "Bulgaria", "HR": "Croazia", "SI": "Slovenia",
            "SK": "Slovacchia", "LT": "Lituania", "LV": "Lettonia", "EE": "Estonia",
            "FI": "Finlandia", "SE": "Svezia", "NO": "Norvegia", "DK": "Danimarca",
            "IE": "Irlanda", "LU": "Lussemburgo", "MT": "Malta", "CY": "Cipro"
        }
        return country_names.get(country_code.upper(), country_code)
    
    async def validate_location(self, city: str, state: str = "", country: str = "") -> Optional[LocationCandidate]:
        """Valida e ottiene coordinate precise per una località."""
        candidates = await self.search_by_structured_input(city, state, country)
        
        if candidates:
            # Restituisci il primo risultato (più rilevante)
            return candidates[0]
        
        return None
    
    def validate_coordinates(self, lat: float, lon: float) -> bool:
        """Valida se le coordinate sono plausibili."""
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    async def reverse_geocode(self, lat: float, lon: float) -> Optional[LocationCandidate]:
        """Geocoding inverso: da coordinate a località."""
        url = f"{self.base_url}/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "limit": 1,
            "appid": self.api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        candidates = self._parse_geocoding_response(data)
                        return candidates[0] if candidates else None
                    else:
                        logger.error(f"Reverse geocoding error: {response.status}")
                        return None
        except Exception as ex:
            logger.error(f"Errore nel reverse geocoding: {ex}")
            return None
