"""
Sidebar Manager for the MeteoApp.
Handles the initialization and management of the sidebar.
"""

import flet as ft
import logging
from typing import Callable, Optional

from layout.frontend.sidebar.sidebar import Sidebar
from state_manager import StateManager
from services.location_toggle_service import LocationToggleService
from services.theme_toggle_service import ThemeToggleService

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
        )
        
        return self.sidebar
