"""
Responsive Utilities per MeteoApp.
Fornisce utility per gestire layout responsive e breakpoint.
"""

import flet as ft
from typing import Dict
from enum import Enum

class DeviceType(Enum):
    """Enum per i tipi di dispositivo."""
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"
    LARGE_DESKTOP = "large_desktop"

class ResponsiveBreakpoints:
    """Definisce i breakpoint responsive per l'applicazione."""
    
    # Breakpoint in pixel (larghezza schermo)
    MOBILE_MAX = 599
    TABLET_MAX = 1023
    DESKTOP_MAX = 1439
    LARGE_DESKTOP_MIN = 1440
    
    # Breakpoint per altezza (utili per layout verticali)
    SHORT_HEIGHT = 600
    MEDIUM_HEIGHT = 800
    TALL_HEIGHT = 1000

class ResponsiveHelper:
    """Helper class per gestire layout responsive."""
    
    @staticmethod
    def get_device_type(width: float) -> DeviceType:
        """
        Determina il tipo di dispositivo basato sulla larghezza dello schermo.
        
        Args:
            width: Larghezza dello schermo in pixel
            
        Returns:
            DeviceType: Tipo di dispositivo
        """
        if width <= ResponsiveBreakpoints.MOBILE_MAX:
            return DeviceType.MOBILE
        elif width <= ResponsiveBreakpoints.TABLET_MAX:
            return DeviceType.TABLET
        elif width <= ResponsiveBreakpoints.DESKTOP_MAX:
            return DeviceType.DESKTOP
        else:
            return DeviceType.LARGE_DESKTOP
    
    @staticmethod
    def get_responsive_columns(device_type: DeviceType) -> Dict[str, int]:
        """
        Restituisce la configurazione delle colonne per il tipo di dispositivo.
        
        Args:
            device_type: Tipo di dispositivo
            
        Returns:
            Dict: Configurazione colonne responsive
        """
        base_configs = {
            DeviceType.MOBILE: {
                "sidebar": {"xs": 12},
                "main_content": {"xs": 12},
                "card_single": {"xs": 12},
                "card_half": {"xs": 12},
                "card_third": {"xs": 12}
            },
            DeviceType.TABLET: {
                "sidebar": {"sm": 12, "md": 4},
                "main_content": {"sm": 12, "md": 8},
                "card_single": {"sm": 12},
                "card_half": {"sm": 6},
                "card_third": {"sm": 12, "md": 6}
            },
            DeviceType.DESKTOP: {
                "sidebar": {"lg": 3},
                "main_content": {"lg": 9},
                "card_single": {"lg": 12},
                "card_half": {"lg": 6},
                "card_third": {"lg": 4}
            },
            DeviceType.LARGE_DESKTOP: {
                "sidebar": {"xl": 3},
                "main_content": {"xl": 9},
                "card_single": {"xl": 12},
                "card_half": {"xl": 6},
                "card_third": {"xl": 4}
            }
        }
        return base_configs.get(device_type, base_configs[DeviceType.DESKTOP])
    
    @staticmethod
    def get_responsive_padding(device_type: DeviceType, element_type: str = "default") -> ft.Padding:
        """
        Restituisce il padding appropriato per il tipo di dispositivo.
        
        Args:
            device_type: Tipo di dispositivo
            element_type: Tipo di elemento ("container", "card", "sidebar", "default")
            
        Returns:
            ft.Padding: Padding configurato
        """
        if device_type == DeviceType.MOBILE:
            paddings = {
                "container": ft.padding.all(6),   # Ridotto da 8 a 6
                "card": ft.padding.all(8),        # Ridotto da 12 a 8
                "sidebar": ft.padding.all(8),     # Ridotto da 12 a 8
                "default": ft.padding.all(6)      # Ridotto da 8 a 6
            }
        elif device_type == DeviceType.TABLET:
            paddings = {
                "container": ft.padding.all(12),
                "card": ft.padding.all(16),
                "sidebar": ft.padding.all(16),
                "default": ft.padding.all(12)
            }
        else:  # Desktop e Large Desktop
            paddings = {
                "container": ft.padding.all(16),
                "card": ft.padding.all(20),
                "sidebar": ft.padding.all(20),
                "default": ft.padding.all(16)
            }
        
        return paddings.get(element_type, paddings["default"])
    
    @staticmethod
    def get_responsive_spacing(device_type: DeviceType) -> int:
        """
        Restituisce lo spacing appropriato per il tipo di dispositivo.
        
        Args:
            device_type: Tipo di dispositivo
            
        Returns:
            int: Spacing in pixel
        """
        spacing_map = {
            DeviceType.MOBILE: 6,              # Ridotto da 8 a 6
            DeviceType.TABLET: 10,             # Ridotto da 12 a 10
            DeviceType.DESKTOP: 16,
            DeviceType.LARGE_DESKTOP: 20
        }
        return spacing_map.get(device_type, 12)
    
    @staticmethod
    def get_responsive_border_radius(device_type: DeviceType, element_type: str = "default") -> int:
        """
        Restituisce il border radius appropriato per il tipo di dispositivo.
        
        Args:
            device_type: Tipo di dispositivo
            element_type: Tipo di elemento ("card", "button", "default")
            
        Returns:
            int: Border radius in pixel
        """
        if device_type == DeviceType.MOBILE:
            radius_map = {
                "card": 12,
                "button": 8,
                "default": 10
            }
        elif device_type == DeviceType.TABLET:
            radius_map = {
                "card": 16,
                "button": 10,
                "default": 12
            }
        else:  # Desktop e Large Desktop
            radius_map = {
                "card": 20,
                "button": 12,
                "default": 16
            }
        
        return radius_map.get(element_type, radius_map["default"])
    
    @staticmethod
    def should_use_stack_layout(device_type: DeviceType) -> bool:
        """
        Determina se utilizzare layout stack (verticale) invece di layout grid.
        
        Args:
            device_type: Tipo di dispositivo
            
        Returns:
            bool: True se utilizzare stack layout
        """
        return device_type in [DeviceType.MOBILE, DeviceType.TABLET]
    
    @staticmethod
    def get_optimal_chart_height(device_type: DeviceType) -> int:
        """
        Restituisce l'altezza ottimale per i grafici basata sul tipo di dispositivo.
        
        Args:
            device_type: Tipo di dispositivo
            
        Returns:
            int: Altezza in pixel
        """
        height_map = {
            DeviceType.MOBILE: 180,            # Ridotto da 200 a 180
            DeviceType.TABLET: 220,            # Ridotto da 250 a 220
            DeviceType.DESKTOP: 300,
            DeviceType.LARGE_DESKTOP: 350
        }
        return height_map.get(device_type, 250)
    
    @staticmethod
    def create_responsive_column_config(**kwargs) -> Dict[str, int]:
        """
        Crea una configurazione colonna responsive personalizzata.
        
        Args:
            **kwargs: Configurazioni per diversi breakpoint (xs, sm, md, lg, xl)
            
        Returns:
            Dict: Configurazione colonna
        """
        config = {}
        for breakpoint, value in kwargs.items():
            if breakpoint in ["xs", "sm", "md", "lg", "xl"] and isinstance(value, int):
                config[breakpoint] = value
        return config

    @staticmethod
    def is_mobile_platform(page) -> bool:
        """
        Verifica se la piattaforma corrente è un dispositivo mobile basandosi su ft.PagePlatform.
        
        Args:
            page: Pagina flet (ft.Page)
            
        Returns:
            bool: True se è un dispositivo mobile, False altrimenti
        """
        if not page:
            return False
            
        try:
            # Verifica la piattaforma direttamente
            if hasattr(page, 'platform'):
                return page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
        except Exception:
            pass
            
        return False
    
    @staticmethod
    def get_device_type_smart(page) -> DeviceType:
        """
        Determina il tipo di dispositivo in modo intelligente utilizzando molteplici fattori.
        
        Args:
            page: Pagina flet (ft.Page)
            
        Returns:
            DeviceType: Tipo di dispositivo rilevato
        """
        # Verifica se è una piattaforma mobile
        if ResponsiveHelper.is_mobile_platform(page):
            return DeviceType.MOBILE
            
        # Verifica la larghezza della pagina
        width = getattr(page, 'width', None)
        if width is not None:
            return ResponsiveHelper.get_device_type(width)
            
        # Verifica la larghezza della finestra
        window = getattr(page, 'window', None)
        if window and hasattr(window, 'width') and window.width:
            return ResponsiveHelper.get_device_type(window.width)
            
        # Fallback: restituisce MOBILE per sicurezza
        return DeviceType.MOBILE


class ResponsivePageHelper:
    """Helper per gestire la responsività a livello di pagina."""
    
    def __init__(self, page: ft.Page):
        """
        Inizializza l'helper con una pagina.
        
        Args:
            page: Pagina Flet
        """
        self.page = page
        self.current_device_type = None
        self.resize_callbacks = []
        
        # Registra handler per resize
        if hasattr(page, 'on_resize'):
            original_handler = page.on_resize
            page.on_resize = self._handle_resize
            if original_handler:
                self.resize_callbacks.append(original_handler)
    
    def _handle_resize(self, e=None):
        """Gestisce eventi di resize della pagina."""
        if self.page and hasattr(self.page, 'width') and self.page.width:
            new_device_type = ResponsiveHelper.get_device_type(self.page.width)
            
            if new_device_type != self.current_device_type:
                self.current_device_type = new_device_type
                self._notify_device_type_change(new_device_type)
        
        # Chiama callbacks originali
        for callback in self.resize_callbacks:
            try:
                callback(e)
            except Exception as ex:
                print(f"Error in resize callback: {ex}")
    
    def _notify_device_type_change(self, device_type: DeviceType):
        """Notifica il cambio di tipo dispositivo."""
        # Qui puoi aggiungere logica per notificare i componenti del cambio
        print(f"Device type changed to: {device_type.value}")
    
    def get_current_device_type(self) -> DeviceType:
        """
        Restituisce il tipo di dispositivo corrente.
        
        Returns:
            DeviceType: Tipo di dispositivo corrente
        """
        if self.page and hasattr(self.page, 'width') and self.page.width:
            return ResponsiveHelper.get_device_type(self.page.width)
        return DeviceType.DESKTOP  # Default
    
    def add_resize_callback(self, callback):
        """
        Aggiunge un callback per eventi di resize.
        
        Args:
            callback: Funzione da chiamare al resize
        """
        self.resize_callbacks.append(callback)


class ResponsiveComponentMixin:
    """
    Mixin per aggiungere funzionalità responsive a componenti Flet.
    
    Esempio di utilizzo:
    ```python
    class MyComponent(ft.Container, ResponsiveComponentMixin):
        def __init__(self, page, **kwargs):
            super().__init__(**kwargs)
            self.page = page
            self.init_responsive()  # Inizializza funzionalità responsive
    ```
    """
    
    def init_responsive(self, force_mobile=False):
        """
        Inizializza le funzionalità responsive del componente.
        
        Args:
            force_mobile: Se True, forza il layout mobile indipendentemente dalla dimensione reale
        """
        if not hasattr(self, 'page'):
            return
            
        # Proprietà di tracciamento responsive
        self._last_page_width = getattr(self.page, 'width', None)
        self._force_mobile = force_mobile
        
        # Collega l'handler di resize
        self._setup_resize_handler()
    
    def _setup_resize_handler(self):
        """Configura l'handler per il ridimensionamento della pagina."""
        if not hasattr(self, 'page') or not self.page:
            return
            
        try:
            # Salva l'handler originale se esiste
            original_handler = getattr(self.page, 'on_resize', None)
            
            # Crea una funzione wrapper che chiama entrambi gli handler
            def combined_resize_handler(e):
                self._handle_resize(e)
                if callable(original_handler):
                    original_handler(e)
            
            # Imposta il nuovo handler
            self.page.on_resize = combined_resize_handler
            
            # Prova anche con on_window_event per supporto desktop
            original_window_handler = getattr(self.page, 'on_window_event', None)
            
            def combined_window_handler(e):
                if getattr(e, 'data', None) == 'resize':
                    self._handle_resize(e)
                if callable(original_window_handler):
                    original_window_handler(e)
            
            # Imposta il nuovo handler per eventi finestra
            if hasattr(self.page, 'on_window_event'):
                self.page.on_window_event = combined_window_handler
        except Exception:
            pass  # Ignora errori nella configurazione degli handler
    
    def _handle_resize(self, e=None):
        """Gestisce eventi di ridimensionamento e aggiorna il layout."""
        if not hasattr(self, 'page') or not hasattr(self, '_last_page_width'):
            return
            
        # Ottieni la larghezza attuale
        current_width = getattr(self.page, 'width', None)
        if current_width is None:
            return
            
        # Verifica se la larghezza è cambiata significativamente
        width_changed = (self._last_page_width is None or 
                         abs(current_width - self._last_page_width) > 50)
        
        if width_changed:
            self._last_page_width = current_width
            
            # Aggiorna il layout solo se il componente ha un metodo build e update
            if hasattr(self, 'build') and hasattr(self, 'update'):
                try:
                    self.content = self.build()
                    self.update()
                except Exception:
                    pass  # Ignora errori nell'aggiornamento
    
    def get_current_device_type(self):
        """
        Determina il tipo di dispositivo attuale in modo intelligente.
        
        Returns:
            DeviceType: Tipo di dispositivo rilevato
        """
        if self._force_mobile:
            return DeviceType.MOBILE
            
        if hasattr(self, 'page') and self.page:
            return ResponsiveHelper.get_device_type_smart(self.page)
            
        return DeviceType.DESKTOP  # Default fallback
