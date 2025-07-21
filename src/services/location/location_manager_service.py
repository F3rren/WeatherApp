#!/usr/bin/env python3

import json
import os
from typing import List, Dict, Optional


class LocationManagerService:
    """Servizio per gestire le località salvate dall'utente."""
    
    def __init__(self, storage_path: str = "storage/data/saved_locations.json"):
        self.storage_path = storage_path
        self.locations = []
        self._ensure_storage_directory()
        self.load_locations()
    
    def _ensure_storage_directory(self):
        """Assicura che la directory di storage esista."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
    
    def load_locations(self) -> List[Dict]:
        """Carica le località salvate dal file."""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.locations = json.load(f)
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
                        "added_date": "2025-01-01"
                    },
                    {
                        "id": "milano_it", 
                        "name": "Milano, Italia",
                        "country": "IT",
                        "lat": 45.4642,
                        "lon": 9.1900,
                        "favorite": False,
                        "added_date": "2025-01-01"
                    }
                ]
                self.save_locations()
        except Exception as e:
            print(f"Errore nel caricamento delle località: {e}")
            self.locations = []
        
        return self.locations
    
    def save_locations(self) -> bool:
        """Salva le località nel file."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.locations, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Errore nel salvataggio delle località: {e}")
            return False
    
    def add_location(self, name: str, lat: float, lon: float, country: str = "") -> bool:
        """Aggiunge una nuova località."""
        try:
            from datetime import datetime
            
            # Genera un ID unico
            location_id = f"{name.lower().replace(' ', '_').replace(',', '')}"
            
            # Controlla se esiste già
            if any(loc['id'] == location_id for loc in self.locations):
                return False
            
            new_location = {
                "id": location_id,
                "name": name,
                "country": country,
                "lat": float(lat),
                "lon": float(lon),
                "favorite": False,
                "added_date": datetime.now().strftime("%Y-%m-%d")
            }
            
            self.locations.append(new_location)
            return self.save_locations()
            
        except Exception as e:
            print(f"Errore nell'aggiunta della località: {e}")
            return False
    
    def remove_location(self, location_id: str) -> bool:
        """Rimuove una località."""
        try:
            self.locations = [loc for loc in self.locations if loc['id'] != location_id]
            return self.save_locations()
        except Exception as e:
            print(f"Errore nella rimozione della località: {e}")
            return False
    
    def toggle_favorite(self, location_id: str) -> bool:
        """Alterna lo stato di preferito di una località."""
        try:
            for location in self.locations:
                if location['id'] == location_id:
                    location['favorite'] = not location.get('favorite', False)
                    return self.save_locations()
            return False
        except Exception as e:
            print(f"Errore nel toggle favorite: {e}")
            return False
    
    def get_location_by_id(self, location_id: str) -> Optional[Dict]:
        """Ottiene una località per ID."""
        for location in self.locations:
            if location['id'] == location_id:
                return location
        return None
    
    def get_favorite_locations(self) -> List[Dict]:
        """Ottiene solo le località preferite."""
        return [loc for loc in self.locations if loc.get('favorite', False)]
    
    def search_locations(self, query: str) -> List[Dict]:
        """Cerca località per nome."""
        query_lower = query.lower()
        return [
            loc for loc in self.locations 
            if query_lower in loc['name'].lower()
        ]
    
    def get_all_locations(self) -> List[Dict]:
        """Ottiene tutte le località."""
        return self.locations.copy()
    
    def clear_all_locations(self) -> bool:
        """Rimuove tutte le località."""
        try:
            self.locations = []
            return self.save_locations()
        except Exception as e:
            print(f"Errore nella pulizia delle località: {e}")
            return False
