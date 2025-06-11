import flet as ft
from typing import Callable, Optional
import inspect
import asyncio
from components.responsive_text_handler import ResponsiveTextHandler

class LocationToggle:
    """
    A toggle switch for enabling/disabling location tracking.
    """
    
    def __init__(self, on_change: Optional[Callable] = None, value: bool = False, page: ft.Page = None):
        self.on_change = on_change
        self._value = value
        self.page = page
        self.switch = None
        
        # Initialize ResponsiveTextHandler
        if self.page:
            self.text_handler = ResponsiveTextHandler(
                page=self.page,
                base_sizes={
                    'toggle_label': 14,  # Toggle label size
                },
                breakpoints=[600, 900, 1200, 1600]
            )
            
            # Dictionary to track text controls
            self.text_controls = {}
            
            # Register as observer for responsive updates
            self.text_handler.add_observer(self.update_text_controls)
    
    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        if self.switch and hasattr(self.switch, 'label_style'):
            if self.switch.label_style is None:
                self.switch.label_style = ft.TextStyle()
            self.switch.label_style.size = self.text_handler.get_size('toggle_label')
        
        # Request page update
        if self.page:
            self.page.update()
    
    def build(self) -> ft.Row:
        """Build the location toggle"""
        
        def handle_toggle_change(e):
            if self.on_change:
                # Usando una funzione wrapper che gestisce sia funzioni sincrone che asincrone
                # senza richiedere un event loop esistente

                # Funzione wrapper che gestisce le chiamate asincrone in modo sicuro
                def call_async_safely(coro):
                    try:
                        # Prova a ottenere l'event loop corrente
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        # Se non c'è un event loop, creane uno nuovo
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    # Esegui la coroutine nell'event loop
                    if not loop.is_running():
                        return loop.run_until_complete(coro)
                    else:
                        # Se l'event loop è già in esecuzione, crea un task
                        return asyncio.create_task(coro)
                
                if inspect.iscoroutinefunction(self.on_change):
                    # Se è una funzione asincrona, usa il wrapper sicuro
                    call_async_safely(self.on_change(e))
                else:
                    # Altrimenti chiamala normalmente
                    self.on_change(e)
        
        self.switch = ft.Switch(
            label="Usa posizione attuale",
            value=self._value,
            on_change=handle_toggle_change,
            active_color=ft.Colors.BLUE,
            inactive_thumb_color=ft.Colors.GREY,
            thumb_color=ft.Colors.WHITE
        )
        
        return ft.Row([self.switch], alignment=ft.MainAxisAlignment.CENTER)
    
    @property
    def value(self) -> bool:
        """Get the current value of the switch"""
        if self.switch:
            return self.switch.value
        return self._value

