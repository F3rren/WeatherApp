"""
Geolocation Service for the MeteoApp.
Handles all geolocation functionality.
"""

import flet as ft
import threading
import time
import logging
from typing import Callable, Optional, Tuple

from config import GEO_ACCURACY, GEO_DISTANCE_FILTER, GEO_UPDATE_INTERVAL

class GeolocationService:
    """
    Service for handling geolocation functionality.
    """
    
    def __init__(self):
        self._geolocator = None
        self._location_callback = None
        self._is_tracking = False
        self._current_lat = None
        self._current_lon = None
        self._update_thread = None
        self._stop_thread = False
    
    @property
    def is_tracking(self) -> bool:
        """Check if location tracking is active"""
        return self._is_tracking
    
    @property
    def current_coordinates(self) -> Tuple[Optional[float], Optional[float]]:
        """Get current coordinates"""
        return self._current_lat, self._current_lon
    
    @property
    def has_coordinates(self) -> bool:
        """Check if coordinates are available"""
        return self._current_lat is not None and self._current_lon is not None
    
    async def get_current_location(self, page: ft.Page) -> Tuple[Optional[float], Optional[float]]:
        """
        Get the current location once.
        
        Args:
            page: Flet page object
            
        Returns:
            Tuple of (latitude, longitude) or (None, None) if location not available
        """
        try:
            # Create geolocator if not already created
            if not self._geolocator:
                self._geolocator = ft.Geolocator(
                    location_settings=ft.GeolocatorSettings(
                        accuracy=ft.GeolocatorPositionAccuracy.HIGH
                    ),
                    on_error=lambda e: logging.error(f"Geolocation error: {e.data}"),
                )
                
                # Add to page overlay
                page.overlay.append(self._geolocator)
                page.update()
            
            # Request permission
            permission = await self._geolocator.request_permission_async()
            if permission != "granted":
                logging.warning("Location permission not granted")
                return None, None
            
            # Get current position
            position = await self._geolocator.get_current_position_async()
            
            # Update stored coordinates
            self._current_lat = position.latitude
            self._current_lon = position.longitude
            
            return position.latitude, position.longitude
        except Exception as e:
            logging.error(f"Error getting current location: {e}")
            return None, None
    
    async def start_tracking(self, page: ft.Page, on_location_change: Optional[Callable] = None) -> bool:
        """
        Start tracking the user's location.
        
        Args:
            page: Flet page object
            on_location_change: Callback function to call when location changes
            
        Returns:
            True if tracking started successfully, False otherwise
        """
        try:
            self._location_callback = on_location_change
            
            # Define position change handler
            def handle_position_change(e):
                if e.latitude and e.longitude:
                    # Store coordinates
                    self._current_lat = e.latitude
                    self._current_lon = e.longitude
                    
                    # Update UI
                    try:
                        page.update()
                    except Exception as e:
                        logging.error(f"Error updating UI: {e}")
            
            # Create geolocator
            self._geolocator = ft.Geolocator(
                location_settings=ft.GeolocatorSettings(
                    accuracy=(
                        ft.GeolocatorPositionAccuracy.HIGH 
                        if GEO_ACCURACY == "high" 
                        else ft.GeolocatorPositionAccuracy.REDUCED
                    ),
                    distance_filter=GEO_DISTANCE_FILTER
                ),
                on_position_change=handle_position_change,
                on_error=lambda e: logging.error(f"Geolocation error: {e.data}"),
            )
            
            # Add to page overlay
            page.overlay.append(self._geolocator)
            page.update()
            
            # Request permission
            permission = await self._geolocator.request_permission_async()
            if permission != "granted":
                logging.warning("Location permission not granted")
                return False
            
            # Start tracking
            await self._geolocator.start_position_watcher_async()
            self._is_tracking = True
            
            # Start update thread
            self._stop_thread = False
            self._update_thread = threading.Thread(target=self._update_ui_thread, args=(page,))
            self._update_thread.daemon = True
            self._update_thread.start()
            
            return True
        except Exception as e:
            logging.error(f"Error starting location tracking: {e}")
            return False
    
    async def stop_tracking(self) -> None:
        """Stop tracking the user's location"""
        try:
            if self._geolocator and self._is_tracking:
                await self._geolocator.stop_position_watcher_async()
                self._is_tracking = False
            
            # Stop update thread
            self._stop_thread = True
            if self._update_thread and self._update_thread.is_alive():
                self._update_thread.join(1)  # Wait max 1 second
        except Exception as e:
            logging.error(f"Error stopping location tracking: {e}")
    
    def set_location_callback(self, callback: Optional[Callable]) -> None:
        """Set or clear the location change callback"""
        self._location_callback = callback
    
    def _update_ui_thread(self, page: ft.Page) -> None:
        """Thread that periodically updates the UI with new coordinates"""
        while not self._stop_thread:
            if self._current_lat and self._current_lon and self._location_callback:
                try:
                    # Get current coordinates
                    lat, lon = self._current_lat, self._current_lon
                    
                    # Update UI asynchronously
                    page.invoke_async(lambda: self._location_callback(lat, lon))
                except Exception as e:
                    logging.error(f"Error updating UI from thread: {e}")
            
            # Wait before next check
            time.sleep(GEO_UPDATE_INTERVAL)
