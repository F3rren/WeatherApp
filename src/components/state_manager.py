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
    
    async def set_state(self, key: str, value: Any) -> None:
        """Set a state value and notify observers"""
        if key in self._state and self._state[key] != value:
            self._state[key] = value
            await self._notify_observers(key, value)
    
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
        if key in self._observers:
            for callback in self._observers[key]:
                try:
                    # Create a task to run the callback asynchronously
                    asyncio.create_task(self._run_callback(callback, value))
                except Exception as e:
                    logging.error(f"Error notifying observer: {e}")

    async def _run_callback(self, callback: Callable, value: Any) -> None:
        """Run a callback, handling both async and sync callbacks."""
        try:
            # Ensure value is of the correct type
            if isinstance(value, dict):
                value = value.get('language', str(value))  # Extract 'language' or convert to string

            # Check if the callback is a bound method of a Flet control
            if hasattr(callback, '__self__') and isinstance(callback.__self__, ft.Control):
                control_instance = callback.__self__
                if control_instance.page is None:
                    logging.warning(
                        f"Skipping callback for {control_instance.__class__.__name__} "
                        f"because its page attribute is None. Callback: {callback.__name__}"
                    )
                    return  # Skip if page is None

            if asyncio.iscoroutinefunction(callback):
                await callback(value)
            else:
                callback(value)
        except Exception as e:
            logging.error(f"Error in observer callback: {e}", exc_info=True)

    async def notify_all(self, event_type: str, data: Any) -> None:
        """
        Notifica tutti gli osservatori di un evento generico.
        Utile per eventi che non sono associati a un cambio di stato specifico.
        
        Args:
            event_type: Tipo di evento
            data: Dati associati all'evento
        """
        if event_type in self._observers:
            for callback in self._observers[event_type]:
                try:
                    # Crea un task per eseguire il callback in modo asincrono
                    asyncio.create_task(self._run_callback(callback, data))
                except Exception as e:
                    logging.error(f"Errore nella notifica dell'evento {event_type}: {e}")
