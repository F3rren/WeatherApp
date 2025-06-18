import logging
import flet as ft

from utils.config import DEFAULT_LANGUAGE
from state_manager import StateManager
from services.translation_service import TranslationService

class LanguageToggleService:
    def __init__(self, state_manager: StateManager, page):
        self.page = page
        self.state_manager = state_manager

    async def handle_language_toggle(self, e: ft.ControlEvent) -> None:
        """
        Gestisce l'evento di toggle del tema.
        
        Args:
            e: Evento di controllo Flet
        """
        try:
            using_language = e.control.value
            
            # Aggiorna lo stato dell'applicazione
            await self.state_manager.set_state("language", using_language)

            # Notifica a eventuali osservatori che il tema è cambiato
            # In modo che possano aggiornare i colori dei loro componenti
            language_event_data = using_language
            await self.state_manager.notify_all("language_event", language_event_data)

            # Aggiorna la pagina per applicare il nuovo tema
            self.page.update()

            logging.info(f"Language changed to: {using_language} via LanguageToggleService")

        except Exception as ex:
            logging.error(f"Errore nel cambio tema: {ex}")
            # Ripristina lo stato del toggle in caso di errore
            if e.control:
                e.control.value = not e.control.value
                self.page.update()


    async def initialize_language(self) -> None:
        """
        Inizializza il tema all'avvio dell'applicazione basandosi sullo stato salvato.
        """
        try:
            # Ottieni il tema salvato nello stato, se presente
            current_language = self.state_manager.get_state("language")
            
            # Se non è definito, usa lingua inglese come predefinita
            if current_language is None:
                current_language = DEFAULT_LANGUAGE  # Imposta la lingua predefinita a inglese
            logging.info(f"Language initialized to: {current_language}")

            await self.state_manager.set_state("language", current_language)


        except Exception as e:
            logging.error(f"Errore nell'inizializzazione della lingua: {e}")
