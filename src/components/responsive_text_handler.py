"""
Responsive Text Handler per l'applicazione MeteoApp.
Gestisce il ridimensionamento dinamico del testo in base alla dimensione della finestra.
"""

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
        
        # Dimensioni predefinite se non specificate
        self.base_sizes = base_sizes or {
            'title': 25,      # Titoli principali
            'subtitle': 20,   # Sottotitoli
            'label': 16,      # Etichette
            'body': 14,       # Testo normale
            'caption': 12,    # Testo piccolo/caption
            'value': 20,       # Valori (es. temperature, percentuali)
            'icon': 100       # Icone (dimensione base),
        }
        
        # Breakpoint predefiniti se non specificati (in pixel)
        self.breakpoints = breakpoints or [600, 900, 1200, 1600]
        
        # Inizializza le dimensioni correnti
        self.current_sizes = {}
        self._calculate_sizes()
        
        # Registra il callback per il ridimensionamento se la pagina è disponibile
        if self.page:
            self.page.on_resize = self._handle_resize
            self.page.window_width_trigger_points = self.breakpoints
    
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
            self.current_sizes[key] = round(base_size * scale_factor)
    
    def _handle_resize(self, e=None):
        """Gestisce l'evento di ridimensionamento della finestra."""
        old_sizes = self.current_sizes.copy()
        self._calculate_sizes()
        
        # Verifica se le dimensioni sono effettivamente cambiate
        if old_sizes != self.current_sizes:
            # Qui potresti notificare agli osservatori che le dimensioni sono cambiate
            # se implementi un pattern observer
            pass
        
        return self.current_sizes
    
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
            self.page.on_resize = self._handle_resize
            self.page.window_width_trigger_points = self.breakpoints
