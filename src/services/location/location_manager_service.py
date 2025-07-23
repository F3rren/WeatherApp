#!/usr/bin/env python3

from typing import List, Dict, Optional
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from services.data.local_storage_service import LocalStorageService
import logging

logger = logging.getLogger(__name__)


class LocationManagerService:
    """Servizio per gestire le località salvate dall'utente."""
    
    def __init__(self):
        self.storage_service = LocalStorageService()
        self.storage_path = self.storage_service.get_data_path("saved_locations.json")
        self.locations = []
        self.last_selected_location = None
        self.load_locations()
        
        logger.info(f"LocationManagerService inizializzato - File: {self.storage_path}")
    
    def load_locations(self) -> List[Dict]:
        """Carica le località salvate dal file."""
        try:
            data = self.storage_service.load_json(self.storage_path, {})
            
            if "locations" in data:
                self.locations = data["locations"]
                self.last_selected_location = data.get("last_selected_location")
            else:
                # Inizializza con alcune località di esempio
                self.locations = [
                    {
                        "id": "roma_it",
                        "name": "Roma, Italia",
                        "country": "IT",
                        "lat": 41.9028,
                        "lon": 12.4964,
                        "favorite": True,
                        "added_date": datetime.now().isoformat(),
                        "custom_layout": {
                            "show_hourly": True,
                            "show_charts": True,
                            "show_alerts": True,
                            "show_air_quality": True
                        }
                    },
                    {
                        "id": "milano_it", 
                        "name": "Milano, Italia",
                        "country": "IT",
                        "lat": 45.4642,
                        "lon": 9.1900,
                        "favorite": False,
                        "added_date": datetime.now().isoformat(),
                        "custom_layout": {
                            "show_hourly": True,
                            "show_charts": False,
                            "show_alerts": True,
                            "show_air_quality": False
                        }
                    }
                ]
                self.last_selected_location = "roma_it"
                self.save_locations()
                
            logger.info(f"Caricate {len(self.locations)} località")
            return self.locations
            
        except Exception as e:
            logger.error(f"Errore nel caricare le località: {e}")
            self.locations = []
            return []
    
    def save_locations(self) -> bool:
        """Salva le località nel file."""
        try:
            data = {
                "locations": self.locations,
                "last_selected_location": self.last_selected_location,
                "updated": datetime.now().isoformat()
            }
            
            return self.storage_service.save_json(data, self.storage_path)
            
        except Exception as e:
            logger.error(f"Errore nel salvataggio delle località: {e}")
            return False
    
    def add_location(self, name: str, lat: float, lon: float, country: str = "", 
                    custom_layout: Dict = None) -> bool:
        """Aggiunge una nuova località."""
        try:
            # Genera un ID unico
            location_id = f"{name.lower().replace(' ', '_').replace(',', '').replace('.', '')}"
            
            # Controlla se esiste già
            if any(loc['id'] == location_id for loc in self.locations):
                logger.warning(f"Località {name} già esistente")
                return False
            
            # Layout di default se non specificato
            if custom_layout is None:
                custom_layout = {
                    "show_hourly": True,
                    "show_charts": True,
                    "show_alerts": True,
                    "show_air_quality": True
                }
            
            new_location = {
                "id": location_id,
                "name": name,
                "country": country,
                "lat": float(lat),
                "lon": float(lon),
                "favorite": False,
                "added_date": datetime.now().isoformat(),
                "custom_layout": custom_layout
            }
            
            self.locations.append(new_location)
            logger.info(f"Aggiunta località: {name}")
            return self.save_locations()
            
        except Exception as e:
            logger.error(f"Errore nell'aggiunta della località: {e}")
            return False
    
    def remove_location(self, location_id: str) -> bool:
        """Rimuove una località."""
        try:
            initial_count = len(self.locations)
            self.locations = [loc for loc in self.locations if loc['id'] != location_id]
            
            # Se la località rimossa era l'ultima selezionata, seleziona la prima disponibile
            if self.last_selected_location == location_id:
                self.last_selected_location = self.locations[0]["id"] if self.locations else None
            
            if len(self.locations) < initial_count:
                logger.info(f"Rimossa località: {location_id}")
                return self.save_locations()
            return False
            
        except Exception as e:
            logger.error(f"Errore nella rimozione della località: {e}")
            return False
    
    def toggle_favorite(self, location_id: str) -> bool:
        """Alterna lo stato di preferito di una località."""
        try:
            for location in self.locations:
                if location['id'] == location_id:
                    location['favorite'] = not location.get('favorite', False)
                    logger.info(f"Toggle favorite per {location_id}: {location['favorite']}")
                    return self.save_locations()
            return False
        except Exception as e:
            logger.error(f"Errore nel toggle favorite: {e}")
            return False
    
    def select_location(self, location_id: str) -> bool:
        """Seleziona una località come attiva (ultima selezionata)."""
        try:
            if any(loc['id'] == location_id for loc in self.locations):
                self.last_selected_location = location_id
                logger.info(f"Selezionata località: {location_id}")
                return self.save_locations()
            return False
        except Exception as e:
            logger.error(f"Errore nella selezione della località: {e}")
            return False
    
    def update_location_layout(self, location_id: str, layout_config: Dict) -> bool:
        """Aggiorna il layout personalizzato di una località."""
        try:
            for location in self.locations:
                if location['id'] == location_id:
                    location['custom_layout'] = layout_config
                    logger.info(f"Aggiornato layout per {location_id}")
                    return self.save_locations()
            return False
        except Exception as e:
            logger.error(f"Errore nell'aggiornamento layout: {e}")
            return False
    
    def get_location_by_id(self, location_id: str) -> Optional[Dict]:
        """Ottiene una località per ID."""
        for location in self.locations:
            if location['id'] == location_id:
                return location
        return None
    
    def get_selected_location(self) -> Optional[Dict]:
        """Ottiene l'ultima località selezionata."""
        if self.last_selected_location:
            return self.get_location_by_id(self.last_selected_location)
        elif self.locations:
            return self.locations[0]  # Prima disponibile se nessuna selezionata
        return None
    
    def get_favorite_locations(self) -> List[Dict]:
        """Ottiene tutte le località marcate come preferite."""
        return [loc for loc in self.locations if loc.get('favorite', False)]
    
    def get_all_locations(self) -> List[Dict]:
        """Ottiene tutte le località."""
        return self.locations.copy()
    
    def search_locations(self, query: str) -> List[Dict]:
        """Cerca località per nome."""
        query_lower = query.lower()
        return [
            loc for loc in self.locations 
            if query_lower in loc['name'].lower() or query_lower in loc.get('country', '').lower()
        ]
    
    def get_storage_info(self) -> Dict:
        """Ottiene informazioni sui file di storage."""
        storage_info = self.storage_service.get_storage_info()
        storage_info.update({
            "locations_file": str(self.storage_path),
            "locations_count": len(self.locations),
            "last_selected": self.last_selected_location,
            "file_exists": self.storage_path.exists()
        })
        return storage_info
    
    def clear_all_locations(self) -> bool:
        """Rimuove tutte le località."""
        try:
            self.locations = []
            self.last_selected_location = None
            logger.info("Tutte le località sono state rimosse")
            return self.save_locations()
        except Exception as e:
            logger.error(f"Errore nella pulizia delle località: {e}")
            return False
