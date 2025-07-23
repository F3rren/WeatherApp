"""
State Manager for the MeteoApp.
Centralizes all application state and provides methods to update it.
"""

import logging
import flet as ft
from typing import Callable, Dict, Any, List
import asyncio

from utils.config import DEFAULT_CITY, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM

class StateManager:
    """
    Manages the application state and provides methods to update it.
    Uses the observer pattern to notify components of state changes.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        
        # Application state
        self._state = {
            "city": DEFAULT_CITY,
            "language": DEFAULT_LANGUAGE,
            "unit": DEFAULT_UNIT_SYSTEM,
            "using_location": False,
            "current_lat": None,
            "current_lon": None,
            "theme_mode": page.theme_mode,
            "using_theme": page.theme_mode == ft.ThemeMode.DARK,
        }
        
        # Observers for state changes
        self._observers: Dict[str, List[Callable]] = {}
        
    def get_state(self, key: str) -> Any:
        """Get a state value by key"""
        return self._state.get(key)
    
    async def set_state(self, key: str, value: Any, notify: bool = True) -> None:
        """Set a state value and optionally notify observers.
        
        Args:
            key: State key
            value: State value
            notify: Whether to notify observers (default: True)
        """
        old_value = self._state.get(key)
        self._state[key] = value
        
        if notify and old_value != value:
            await self._notify_observers(key, {"old_value": old_value, "new_value": value})
    
    def set_state_sync(self, key: str, value: Any) -> None:
        """Set a state value synchronously without notifying observers.
        
        Use this method when you need to update state from non-async contexts
        and don't need immediate observer notification.
        
        Args:
            key: State key
            value: State value
        """
        self._state[key] = value
    
    async def update_state(self, updates: Dict[str, Any]) -> None:
        """Update multiple state values at once"""
        changed_keys = []
        
        for key, value in updates.items():
            if key in self._state and self._state[key] != value:
                self._state[key] = value
                changed_keys.append(key)
        
        for key in changed_keys:
            await self._notify_observers(key, self._state[key])
    
    def register_observer(self, key: str, callback: Callable) -> None:
        """Register an observer for a specific state key"""
        if key not in self._observers:
            self._observers[key] = []
        
        if callback not in self._observers[key]:
            self._observers[key].append(callback)
    
    def unregister_observer(self, key: str, callback: Callable) -> None:
        """Unregister an observer for a specific state key"""
        if key in self._observers and callback in self._observers[key]:
            self._observers[key].remove(callback)
    
    async def _notify_observers(self, key: str, value: Any) -> None:
        """Notify all observers of a state change"""
        logging.debug(f"Notifying observers for key: {key} with value: {value}")
        if key in self._observers:
            for callback in self._observers[key]:
                try:
                    # Create a task to run the callback asynchronously
                    asyncio.create_task(self._run_callback(callback, value))
                except Exception as e:
                    logging.error(f"Error notifying observer: {e}")

    async def _run_callback(self, callback: Callable, value: Any) -> None:
        """Run a callback, handling both async and sync callbacks"""
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(value)
            else:
                callback(value)
        except Exception as e:
            logging.error(f"Error in observer callback {getattr(callback, '__name__', 'N/A')}: {e}")

    async def notify_all(self, event_type: str, data: Any) -> None:
        """
        Notifies all observers of a generic event.
        Passes only the data payload to the callback.
        """
        logging.debug(f"Notifying all observers for event: {event_type} with data: {data}")
        if event_type in self._observers:
            for callback in self._observers[event_type]:
                try:
                    # Ensure the callback is called only with the data payload.
                    if asyncio.iscoroutinefunction(callback):
                        await callback(data)
                    else:
                        callback(data)
                except Exception as e:
                    logging.error(f"Error in observer callback {getattr(callback, '__name__', 'N/A')} for event {event_type}: {e}")
