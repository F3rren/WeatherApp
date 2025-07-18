"""
Settings persistence service for MeteoApp.
Handles loading and saving user preferences (theme, language, units, etc.)
"""

import json
import os
import logging
import time
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class SettingsService:
    """Service for managing persistent user settings."""
    
    def __init__(self, app_name: str = "MeteoApp"):
        """Initialize the settings service.
        
        Args:
            app_name: Name of the application for settings folder
        """
        self.app_name = app_name
        self.settings_file = self._get_settings_file_path()
        self._settings: Dict[str, Any] = {}
        self._default_settings = {
            'theme_mode': 'light',
            'language': 'it',
            'unit_system': 'metric',
            'last_city': 'Milano, IT',
            'using_location': False,
            'auto_refresh': True,
            'refresh_interval': 30,  # minutes
            'notifications_enabled': True,
            'show_hourly_forecast': True,
            'show_charts': True,
            'temperature_unit': 'celsius',
            'wind_unit': 'km/h',
            'pressure_unit': 'hPa',
            'visibility_unit': 'km'
        }
        self.load_settings()
    
    def _get_settings_file_path(self) -> Path:
        """Get the path for the settings file based on the operating system."""
        if os.name == 'nt':  # Windows
            settings_dir = Path(os.environ.get('APPDATA', Path.home())) / self.app_name
        elif os.name == 'posix':  # macOS and Linux
            if 'darwin' in os.uname().sysname.lower():  # macOS
                settings_dir = Path.home() / 'Library' / 'Application Support' / self.app_name
            else:  # Linux
                settings_dir = Path.home() / '.config' / self.app_name
        else:
            # Fallback to home directory
            settings_dir = Path.home() / f'.{self.app_name.lower()}'
        
        # Create directory if it doesn't exist
        settings_dir.mkdir(parents=True, exist_ok=True)
        
        return settings_dir / 'settings.json'
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create default settings."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                
                # Merge with defaults to ensure all required keys exist
                self._settings = {**self._default_settings, **loaded_settings}
                
                logger.info(f"Settings loaded from {self.settings_file}")
            else:
                self._settings = self._default_settings.copy()
                self.save_settings()  # Create initial settings file
                logger.info("Created default settings file")
                
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            self._settings = self._default_settings.copy()
        
        return self._settings
    
    def save_settings(self) -> bool:
        """Save current settings to file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Settings saved to {self.settings_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting value.
        
        Args:
            key: Setting key
            default: Default value if key doesn't exist
            
        Returns:
            Setting value or default
        """
        return self._settings.get(key, default)
    
    def set_setting(self, key: str, value: Any, auto_save: bool = True) -> None:
        """Set a specific setting value.
        
        Args:
            key: Setting key
            value: Setting value
            auto_save: Whether to automatically save to file
        """
        self._settings[key] = value
        
        if auto_save:
            self.save_settings()
        
        logger.debug(f"Setting updated: {key} = {value}")
    
    def update_settings(self, updates: Dict[str, Any], auto_save: bool = True) -> None:
        """Update multiple settings at once.
        
        Args:
            updates: Dictionary of setting updates
            auto_save: Whether to automatically save to file
        """
        self._settings.update(updates)
        
        if auto_save:
            self.save_settings()
        
        logger.debug(f"Settings updated: {list(updates.keys())}")
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all current settings.
        
        Returns:
            Dictionary of all settings
        """
        return self._settings.copy()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self._settings = self._default_settings.copy()
        self.save_settings()
        logger.info("Settings reset to defaults")
    
    def export_settings(self, file_path: str) -> bool:
        """Export settings to a specific file.
        
        Args:
            file_path: Path to export file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Settings exported to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """Import settings from a specific file.
        
        Args:
            file_path: Path to import file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            # Validate and merge with current settings
            valid_settings = {}
            for key, value in imported_settings.items():
                if key in self._default_settings:
                    valid_settings[key] = value
            
            self._settings.update(valid_settings)
            self.save_settings()
            
            logger.info(f"Settings imported from {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error importing settings: {e}")
            return False
    
    def backup_settings(self) -> str:
        """Create a backup of current settings.
        
        Returns:
            str: Path to backup file
        """
        try:
            backup_path = self.settings_file.parent / f"settings_backup_{int(time.time())}.json"
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Settings backed up to {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Error creating settings backup: {e}")
            return ""
