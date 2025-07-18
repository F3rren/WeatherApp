"""
Location Toggle Service per MeteoApp.
Gestisce la funzionalità di attivazione/disattivazione della geolocalizzazione.
"""

import logging
import flet as ft
from typing import Callable, Awaitable

from services.location.geolocation_service import GeolocationService
from core.state_manager import StateManager

class LocationToggleService:
    """
    Servizio che gestisce la funzionalità di toggle della posizione.
    
    Centralizza la logica per attivare/disattivare la geolocalizzazione
    e aggiornare lo stato dell'applicazione di conseguenza.
    """
    
    def __init__(
        self, 
        page: ft.Page, 
        geolocation_service: GeolocationService,
        state_manager: StateManager,
        update_weather_callback: Callable[..., Awaitable[None]]
    ):
        """
        Inizializza il servizio di location toggle.
        
        Args:
            page: Pagina Flet
            geolocation_service: Servizio di geolocalizzazione
            state_manager: Gestore dello stato
            update_weather_callback: Callback per aggiornare il meteo con coordinate
        """
        self.page = page
        self.geolocation_service = geolocation_service
        self.state_manager = state_manager
        self.update_weather_callback = update_weather_callback
        
    async def handle_location_toggle(self, e: ft.ControlEvent) -> None:
        """
        Gestisce l'evento di toggle della posizione.
        
        Args:
            e: Evento di controllo Flet
        """
        try:
            using_location = e.control.value
            await self.state_manager.set_state("using_location", using_location)
            
            if using_location:
                await self._enable_location()
            else:
                self._disable_location()
                
        except Exception as ex:
            logging.error(f"Errore nel toggle posizione: {ex}")
            # Ripristina lo stato del toggle in caso di errore
            e.control.value = not using_location
            self.page.update()

    async def _enable_location(self) -> None:
        """Attiva la geolocalizzazione e aggiorna il meteo con le coordinate attuali."""
        if self.geolocation_service.has_coordinates:
            # Usa le coordinate esistenti
            lat, lon = self.geolocation_service.current_coordinates
            await self._update_with_coordinates(lat, lon)
            self.geolocation_service.set_location_callback(self.handle_location_change)
        else:
            # Inizia il tracking della posizione
            success = await self.geolocation_service.start_tracking(
                page=self.page,
                on_location_change=self.handle_location_change
            )
            if not success:
                # Reset dello stato se il tracking fallisce
                await self.state_manager.set_state("using_location", False)
                logging.warning("Impossibile attivare il tracking della posizione")

    def _disable_location(self) -> None:
        """Disattiva il tracking della posizione."""
        self.geolocation_service.set_location_callback(None)
        logging.info("Tracking della posizione disattivato")

    async def handle_location_change(self, lat: float, lon: float) -> None:
        """
        Gestisce il cambio di posizione.
        
        Args:
            lat: Latitudine
            lon: Longitudine
        """
        try:
            await self.state_manager.update_state({
                "current_lat": lat,
                "current_lon": lon
            })
            
            # Aggiorna il meteo solo se stiamo usando la posizione
            if self.state_manager.get_state("using_location"):
                await self._update_with_coordinates(lat, lon)
                
        except Exception as e:
            logging.error(f"Errore nel cambio posizione: {e}")

    async def _update_with_coordinates(self, lat: float, lon: float) -> None:
        """
        Aggiorna il meteo utilizzando le coordinate specificate.
        
        Args:
            lat: Latitudine
            lon: Longitudine
        """
        language = self.state_manager.get_state("language")
        unit = self.state_manager.get_state("unit")
        
        await self.update_weather_callback(lat, lon, language, unit)
        logging.info(f"Meteo aggiornato con coordinate: {lat}, {lon}")

    async def initialize_tracking(self) -> None:
        """
        Inizializza il tracking della posizione all'avvio dell'applicazione.
        """
        try:
            # Add timeout to prevent blocking the app startup
            import asyncio
            
            async def _init_with_timeout():
                success = await self.geolocation_service.start_tracking(
                    page=self.page,
                    on_location_change=None
                )
                
                if success:
                    lat, lon = await self.geolocation_service.get_current_location(self.page)
                    if lat and lon:
                        await self.state_manager.update_state({
                            "current_lat": lat,
                            "current_lon": lon
                        })
                else:
                    logging.warning("Failed to start location tracking")
                    
                return success
            
            # Set timeout to 10 seconds for location initialization (increased from 5)
            try:
                await asyncio.wait_for(_init_with_timeout(), timeout=10.0)
                logging.info("Location tracking initialized successfully")
            except asyncio.TimeoutError:
                logging.warning("Location tracking initialization timed out")
            except Exception as e:
                logging.error(f"Error starting location tracking: {e}")
                
        except Exception as e:
            logging.error(f"Error initializing geolocation: {e}")
