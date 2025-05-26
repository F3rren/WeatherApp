import flet as ft
from typing import Callable, Optional

class LocationToggle:
    """
    A toggle switch for enabling/disabling location tracking.
    """
    
    def __init__(self, on_change: Optional[Callable] = None, value: bool = False):
        self.on_change = on_change
        self._value = value
        self.switch = None
    
    def build(self) -> ft.Row:
        """Build the location toggle"""
        self.switch = ft.Switch(
            label="Usa posizione attuale",
            value=self._value,
            on_change=self.on_change
        )
        
        return ft.Row([self.switch])
    
    @property
    def value(self) -> bool:
        """Get the current value of the switch"""
        if self.switch:
            return self.switch.value
        return self._value
    
