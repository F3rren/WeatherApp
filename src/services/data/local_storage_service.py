#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class LocalStorageService:
    """Servizio per gestire la persistenza dei dati in cartelle locali del progetto."""
    
    def __init__(self, project_root: str = None):
        # Usa la directory del progetto corrente se non specificata
        if project_root is None:
            # Trova la root del progetto (dove si trova src/)
            current_file = Path(__file__)
            src_dir = current_file.parent.parent.parent  # risale da services/data/ a src/
            self.project_root = src_dir.parent  # risale da src/ alla root del progetto
        else:
            self.project_root = Path(project_root)
        
        # Directory per i dati persistenti
        self.data_dir = self.project_root / "storage" / "data"
        self.cache_dir = self.project_root / "storage" / "cache" 
        self.settings_dir = self.project_root / "storage" / "settings"
        
        # Crea le directory se non esistono
        self._ensure_directories()
        
        logger.info(f"LocalStorageService inizializzato - Root: {self.project_root}")
    
    def _ensure_directories(self):
        """Assicura che tutte le directory necessarie esistano."""
        directories = [self.data_dir, self.cache_dir, self.settings_dir]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory assicurata: {directory}")
    
    def get_data_path(self, filename: str) -> Path:
        """Restituisce il percorso completo per un file di dati."""
        return self.data_dir / filename
    
    def get_cache_path(self, filename: str) -> Path:
        """Restituisce il percorso completo per un file di cache."""
        return self.cache_dir / filename
    
    def get_settings_path(self, filename: str) -> Path:
        """Restituisce il percorso completo per un file di impostazioni."""
        return self.settings_dir / filename
    
    def save_json(self, data: Dict[str, Any], filepath: Path) -> bool:
        """Salva dati in formato JSON."""
        try:
            # Assicura che la directory esista
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"Dati JSON salvati in: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Errore nel salvare JSON in {filepath}: {e}")
            return False
    
    def load_json(self, filepath: Path, default: Dict[str, Any] = None) -> Dict[str, Any]:
        """Carica dati da un file JSON."""
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.debug(f"Dati JSON caricati da: {filepath}")
                return data
            else:
                logger.debug(f"File JSON non trovato: {filepath}, usando default")
                return default or {}
                
        except Exception as e:
            logger.error(f"Errore nel caricare JSON da {filepath}: {e}")
            return default or {}
    
    def delete_file(self, filepath: Path) -> bool:
        """Elimina un file."""
        try:
            if filepath.exists():
                filepath.unlink()
                logger.debug(f"File eliminato: {filepath}")
                return True
            return False
        except Exception as e:
            logger.error(f"Errore nell'eliminare file {filepath}: {e}")
            return False
    
    def list_files(self, directory: Path, pattern: str = "*") -> List[Path]:
        """Lista i file in una directory con un pattern specifico."""
        try:
            if directory.exists():
                return list(directory.glob(pattern))
            return []
        except Exception as e:
            logger.error(f"Errore nel listare file in {directory}: {e}")
            return []
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Restituisce informazioni sui percorsi di storage."""
        return {
            "project_root": str(self.project_root),
            "data_dir": str(self.data_dir),
            "cache_dir": str(self.cache_dir),
            "settings_dir": str(self.settings_dir),
            "data_exists": self.data_dir.exists(),
            "cache_exists": self.cache_dir.exists(),
            "settings_exists": self.settings_dir.exists()
        }
