"""
Sidebar Manager for the MeteoApp.
Handles the initialization and management of the sidebar.
"""

import flet as ft
import logging
from typing import Callable, Optional


from layout.frontend.sidebar.Sidebar import Sidebar
from state_manager import StateManager
from services.location_toggle_service import LocationToggleService
from services.theme_toggle_service import ThemeToggleService
from components.responsive_text_handler import ResponsiveTextHandler

class SidebarManager:
    """
    Manager per la sidebar dell'applicazione.
    Gestisce l'inizializzazione e il comportamento della sidebar.
    """
    
    def __init__(self, 
                 page: ft.Page, 
                 state_manager: StateManager, 
                 location_toggle_service: LocationToggleService,
                 theme_toggle_service: ThemeToggleService,
                 update_weather_callback: Optional[Callable] = None):
        """
        Inizializza il gestore della sidebar.
        
        Args:
            page: Oggetto pagina di Flet
            state_manager: Gestore dello stato dell'applicazione
            location_toggle_service: Servizio per la gestione della geolocalizzazione
            theme_toggle_service: Servizio per la gestione del tema
            update_weather_callback: Callback per l'aggiornamento delle previsioni meteo
        """
        self.page = page
        self.state_manager = state_manager
        self.location_toggle_service = location_toggle_service
        self.theme_toggle_service = theme_toggle_service
        self.update_weather_callback = update_weather_callback
        self.sidebar = None
        
        # Initialize ResponsiveTextHandler
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20,      # Titoli
                'subtitle': 16,   # Sottotitoli
                'body': 14,       # Testo normale
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Dictionary to track text controls
        self.text_controls = {}
        
        # Register as observer for responsive updates
        self.text_handler.add_observer(self.update_text_controls)
          # Debug print
        print("DEBUG: SidebarManager initialized with ResponsiveTextHandler")
    
    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        for control, size_category in self.text_controls.items():
            if hasattr(control, 'size'):
                control.size = self.text_handler.get_size(size_category)
        
        # Request page update
        if self.page:
            self.page.update()
    
    async def handle_city_change(self, city: str):
        """
        Gestisce il cambio di città selezionata.
        
        Args:
            city: Nome della città selezionata
        """
        try:
            # Aggiorna lo stato: quando si seleziona una città, disabilita la localizzazione
            await self.state_manager.update_state({
                "city": city,
                "using_location": False
            })
            
            # Aggiorna la UI: se esiste l'istanza della sidebar, aggiorna il toggle
            if self.sidebar and hasattr(self.sidebar, 'update_location_toggle'):
                self.sidebar.update_location_toggle(False)
            
            # Aggiorna la visualizzazione del meteo con la città selezionata
            if self.update_weather_callback:
                await self.update_weather_callback(
                    city=city,
                    language=self.state_manager.get_state("language"),
                    unit=self.state_manager.get_state("unit")
                )
            
            logging.info(f"Città cambiata: {city}, localizzazione disattivata")
        except Exception as e:
            logging.error(f"Errore nel cambio città: {e}")
    
    def initialize_sidebar(self):
        """
        Inizializza la sidebar dell'applicazione.
        
        Returns:
            Sidebar: L'istanza della sidebar inizializzata
        """
        # Creazione dell'istanza della sidebar con tutti i callback necessari
        self.sidebar = Sidebar(
            page=self.page, 
            on_city_selected=self.handle_city_change,
            handle_location_toggle=self.location_toggle_service.handle_location_toggle,
            location_toggle_value=self.state_manager.get_state("using_location") or False,
            handle_theme_toggle=self.theme_toggle_service.handle_theme_toggle,
            theme_toggle_value=self.state_manager.get_state("using_theme") or False
        ).build()
        
        return self.sidebar
    
    def cleanup(self):
        """Cleanup method to remove observers"""
        if hasattr(self, 'text_handler') and self.text_handler:
            self.text_handler.remove_observer(self.update_text_controls)
        
        # Cleanup della sidebar se disponibile
        if hasattr(self, 'sidebar') and self.sidebar and hasattr(self.sidebar, 'cleanup'):
            self.sidebar.cleanup()
        
        print("DEBUG: SidebarManager cleanup completed")
