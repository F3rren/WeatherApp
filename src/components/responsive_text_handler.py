"""
Responsive Text Handler per l'applicazione MeteoApp.
Gestisce il ridimensionamento dinamico del testo in base alla dimensione della finestra.
"""

import asyncio
import logging
import flet as ft

class ResponsiveTextHandler:
    """
    Classe che gestisce il ridimensionamento del testo in base alla dimensione dello schermo.
    Permette di definire dimensioni di base e regole di scalabilità per diversi breakpoint.
    """
    def __init__(self, page: ft.Page = None, 
                 base_sizes: dict = None,
                 breakpoints: list = None):
        """
        Inizializza il gestore di testo responsive.
        
        Args:
            page: L'oggetto ft.Page di riferimento, necessario per ottenere la dimensione dello schermo
            base_sizes: Un dizionario con le dimensioni base per diversi tipi di testo (es. {'title': 20, 'body': 16})
            breakpoints: Lista di breakpoint in pixel per la larghezza della finestra [xs, sm, md, lg]
        """
        self.page = page
        self.observers = []  # Lista di callback da chiamare quando le dimensioni cambiano
        
        # Dimensioni predefinite se non specificate
        self.base_sizes = base_sizes or {
            'title': 28,       # Titoli principali (più contenuto)
            'subtitle': 18,    # Sottotitoli (ridotto per coerenza)
            'label': 14,       # Etichette (standardizzato)
            'body': 14,        # Testo normale (base standard)
            'caption': 12,     # Testo piccolo/caption (ridotto)
            'value': 16,       # Valori (temperature, percentuali - moderato)
            'sidebar_icon': 30,        # Icone (molto ridotto, più proporzionato)
            'legend': 13,      # Per legende dei grafici
            'axis_title': 25,  # Per titoli degli assi dei grafici
        }
        
        # Breakpoint predefiniti se non specificati (in pixel)
        self.breakpoints = breakpoints or [600, 900, 1200, 1600]
        
        # Inizializza le dimensioni correnti
        self.current_sizes = {}
        self._calculate_sizes()
        
        # Registra il callback per il ridimensionamento se la pagina è disponibile
        if self.page:
            # self.page.on_resize = self._handle_resize # MODIFIED: Removed this line
            # Aggiungi controllo periodico come fallback
            import asyncio
            asyncio.create_task(self._periodic_size_check())
    
    async def _periodic_size_check(self):
        """Controlla periodicamente la dimensione della finestra come fallback."""
        last_width = None
        while True:
            await asyncio.sleep(0.5)  # Controlla ogni 500ms
            
            if self.page and hasattr(self.page, 'width') and self.page.width:
                current_width = self.page.width
                
                if last_width != current_width:
                    self._handle_resize()
                    last_width = current_width
    
    def _calculate_sizes(self):
        """Calcola le dimensioni del testo in base alla larghezza corrente della finestra."""
        if not self.page:
            # Se la pagina non è disponibile, usa le dimensioni base
            self.current_sizes = self.base_sizes.copy()
            return
        
        # Ottieni la larghezza corrente della finestra
        width = self.page.width if hasattr(self.page, 'width') and self.page.width else 1200
        
        # Calcola il fattore di scala in base alla larghezza
        if width < self.breakpoints[0]:  # xs
            scale_factor = 0.85  # Riduce del 15%
        elif width < self.breakpoints[1]:  # sm
            scale_factor = 0.9   # Riduce del 10%
        elif width < self.breakpoints[2]:  # md
            scale_factor = 1.0   # Dimensione base
        elif width < self.breakpoints[3]:  # lg
            scale_factor = 1.1   # Aumenta del 10%
        else:  # xl
            scale_factor = 1.2   # Aumenta del 20%
        
        # Applica il fattore di scala a tutte le dimensioni base
        for key, base_size in self.base_sizes.items():
            new_size = round(base_size * scale_factor)
            self.current_sizes[key] = new_size
    
    def _handle_resize(self, e=None):
        """Gestisce l'evento di ridimensionamento della finestra."""
        old_sizes = self.current_sizes.copy()
        self._calculate_sizes()
        
        # Verifica se le dimensioni sono effettivamente cambiate
        sizes_changed = old_sizes != self.current_sizes
        
        if sizes_changed:
            # Notifica tutti gli osservatori che le dimensioni sono cambiate
            self._notify_observers()
        
        return self.current_sizes
    
    def add_observer(self, callback):
        """Aggiunge un observer che viene chiamato quando le dimensioni cambiano."""
        if callback not in self.observers:
            self.observers.append(callback)
    
    def remove_observer(self, callback):
        """Rimuove un observer."""
        if callback in self.observers:
            self.observers.remove(callback)
    
    def _notify_observers(self):
        """Notifica tutti gli observers che le dimensioni sono cambiate."""
        for callback in self.observers:
            try:
                callback()
            except Exception as e:
                logging.error(f"Errore nella notifica observer: {e}")
    
    def get_size(self, text_type: str) -> int:
        """
        Ritorna la dimensione corrente per il tipo di testo specificato.
        
        Args:
            text_type: Tipo di testo (es. 'title', 'body', 'label')
            
        Returns:
            Dimensione del testo in pixel
        """
        if text_type not in self.current_sizes:
            # Fallback alla dimensione del corpo del testo
            return self.current_sizes.get('body', 14)
        
        return self.current_sizes[text_type]
    
    def update_text_controls(self, controls_dict: dict):
        """
        Aggiorna le dimensioni del testo per tutti i controlli nel dizionario passato.
        
        Args:
            controls_dict: Un dizionario che mappa i controlli ai tipi di testo (es. {text_control: 'title'})
        """
        for control, text_type in controls_dict.items():
            # Aggiorna il controllo standard con proprietà size
            if hasattr(control, 'size'):
                control.size = self.get_size(text_type)
                if hasattr(control, 'page') and control.page:
                    control.update()
            
            # Aggiorna lo stile se il controllo ha un attributo style con size
            elif hasattr(control, 'style') and hasattr(control.style, 'size'):
                control.style.size = self.get_size(text_type)
                if hasattr(control, 'page') and control.page:
                    control.update()
            
            # Aggiorna gli span se il controllo è un Text con spans
            if hasattr(control, 'spans') and control.spans:
                for span in control.spans:
                    if hasattr(span, 'style') and span.style:
                        span.style.size = self.get_size(text_type)
                if hasattr(control, 'page') and control.page:
                    control.update()
    
    def attach_to_page(self, page: ft.Page):
        """
        Collega questo handler a una pagina (utile se non è stata fornita al costruttore).
        
        Args:
            page: L'oggetto ft.Page a cui collegare questo handler
        """
        self.page = page
        self._calculate_sizes()
        
        if self.page:
            # self.page.on_resize = self._handle_resize # MODIFIED: Removed this line
            # Aggiungi controllo periodico come fallback
            import asyncio
            asyncio.create_task(self._periodic_size_check())
