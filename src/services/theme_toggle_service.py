"""
Theme Toggle Service per MeteoApp.
Gestisce la funzionalità di cambio tema dell'app.
"""

import logging
import flet as ft

from state_manager import StateManager

class ThemeToggleService:
    """
    Servizio che gestisce il cambio di tema dell'applicazione.
    
    Centralizza la logica per cambiare tra tema chiaro e scuro
    e aggiornare lo stato dell'applicazione di conseguenza.
    """
    def __init__(
        self, 
        page: ft.Page, 
        state_manager: StateManager
    ):
        """
        Inizializza il servizio di theme toggle.
        
        Args:
            page: Pagina Flet
            state_manager: Gestore dello stato
        """
        self.page = page
        self.state_manager = state_manager
        self.settings_service = page.session.get('settings_service') if page and page.session else None

    async def handle_theme_toggle(self, e: ft.ControlEvent) -> None:
        """
        Gestisce l'evento di toggle del tema.
        
        Args:
            e: Evento di controllo Flet
        """
        try:
            using_dark_theme = e.control.value
            
            # Aggiorna lo stato dell'applicazione
            await self.state_manager.set_state("using_theme", using_dark_theme)
            
            # Cambia il tema della pagina
            self.page.theme_mode = ft.ThemeMode.DARK if using_dark_theme else ft.ThemeMode.LIGHT
            
            # Notifica il cambio tema globalmente
            self.page.session.set('theme_mode', self.page.theme_mode)
            
            # Notifica a eventuali osservatori che il tema è cambiato
            # In modo che possano aggiornare i colori dei loro componenti
            theme_event = {"type": "theme_changed", "is_dark": using_dark_theme}
            await self.state_manager.notify_all("theme_event", theme_event)
            
            # Aggiorna la pagina per applicare il nuovo tema
            self.page.update()
            
            logging.info(f"Tema cambiato: {'scuro' if using_dark_theme else 'chiaro'}")
            
        except Exception as ex:
            logging.error(f"Errore nel cambio tema: {ex}")
            # Ripristina lo stato del toggle in caso di errore
            if e.control:
                e.control.value = not e.control.value
                self.page.update()
                
    async def initialize_theme(self) -> None:
        """
        Inizializza il tema all'avvio dell'applicazione basandosi sullo stato salvato.
        """
        try:
            # Ottieni il tema salvato nello stato, se presente
            using_dark_theme = self.state_manager.get_state("using_theme")
            
            # Se non è definito, usa il tema corrente della pagina
            if using_dark_theme is None:
                using_dark_theme = self.page.theme_mode == ft.ThemeMode.DARK
                # Salva il valore iniziale nello stato
                await self.state_manager.set_state("using_theme", using_dark_theme)
            
            # Imposta il tema della pagina in base allo stato
            self.page.theme_mode = ft.ThemeMode.DARK if using_dark_theme else ft.ThemeMode.LIGHT
            
            # Salva il tema corrente nella sessione per accedervi da altre parti dell'app
            self.page.session.set('theme_mode', self.page.theme_mode)
            
            if self.settings_service:
                saved_theme = self.settings_service.get_setting('theme_mode', 'light')
                theme_mode = ft.ThemeMode.DARK if saved_theme == 'dark' else ft.ThemeMode.LIGHT
                
                if self.page.theme_mode != theme_mode:
                    self.page.theme_mode = theme_mode
                    self.page.update()
                    
                    # Notifica il cambio di tema al gestore dello stato
                    await self.state_manager.notify_observers("theme_event", {"theme_mode": saved_theme})
            
            self.page.update()
            
            logging.info(f"Tema inizializzato: {'scuro' if using_dark_theme else 'chiaro'}")
            
        except Exception as e:
            logging.error(f"Errore nell'inizializzazione del tema: {e}")
