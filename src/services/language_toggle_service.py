import logging
import flet as ft

from config import DEFAULT_LANGUAGE
from state_manager import StateManager

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
            await self.state_manager.set_state("using_language", using_language)

            # Cambia il tema della pagina
            self.page.theme_mode = ft.ThemeMode.DARK if using_language == "it" else ft.ThemeMode.LIGHT

            # Notifica il cambio lingua globalmente
            self.page.session.set('language_mode', self.page.language_mode)

            # Notifica a eventuali osservatori che il tema è cambiato
            # In modo che possano aggiornare i colori dei loro componenti
            language_event = {"type": "language_changed", "is_language": using_language}
            await self.state_manager.notify_all("language_event", language_event)

            # Aggiorna la pagina per applicare il nuovo tema
            self.page.update()

            logging.info(f"Lingua cambiato: {'italiano' if using_language == 'it' else DEFAULT_LANGUAGE}")

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
            using_language = self.state_manager.get_state("using_language")
            
            # Se non è definito, usa lingua inglese come predefinita
            if using_language is None:
                using_language = "en"  # Imposta la lingua predefinita a inglese
            logging.info(f"Lingua inizializzato: {using_language}")

            await self.state_manager.set_state("using_language", using_language)


        except Exception as e:
            logging.error(f"Errore nell'inizializzazione della lingua: {e}")
