"""
Adaptive Card Component per MeteoApp.
Crea card che si adattano automaticamente al tipo di dispositivo.
"""

import flet as ft
from utils.responsive_utils import ResponsiveHelper, DeviceType


class AdaptiveCard:
    """
    Componente card che si adatta automaticamente al tipo di dispositivo.
    """
    
    def __init__(self, page: ft.Page):
        """
        Inizializza la card adattiva.
        
        Args:
            page: Pagina Flet per determinare il tipo di dispositivo
        """
        self.page = page
        self.device_type = self._get_current_device_type()
    
    def _get_current_device_type(self) -> DeviceType:
        """Ottiene il tipo di dispositivo corrente."""
        if self.page and hasattr(self.page, 'width') and self.page.width:
            return ResponsiveHelper.get_device_type(self.page.width)
        return DeviceType.DESKTOP
    
    def create_weather_info_card(self, content: ft.Control, title: str = None) -> ft.Container:
        """
        Crea una card per informazioni meteo adattiva.
        
        Args:
            content: Contenuto della card
            title: Titolo opzionale della card
            
        Returns:
            ft.Container: Card configurata per il dispositivo
        """
        device_type = self._get_current_device_type()
        
        # Padding adattivo
        padding = ResponsiveHelper.get_responsive_padding(device_type, "card")
        
        # Border radius adattivo
        border_radius = ResponsiveHelper.get_responsive_border_radius(device_type, "card")
        
        # Crea il contenuto finale
        final_content = content
        if title:
            final_content = ft.Column([
                ft.Text(
                    title, 
                    size=self._get_title_size(),
                    weight=ft.FontWeight.W_600
                ),
                ft.Divider(height=8),
                content
            ], spacing=8)
        
        return ft.Container(
            content=final_content,
            padding=padding,
            border_radius=border_radius,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            expand=True
        )
    
    def create_chart_card(self, chart_content: ft.Control, title: str = None) -> ft.Container:
        """
        Crea una card ottimizzata per grafici.
        
        Args:
            chart_content: Contenuto del grafico
            title: Titolo opzionale del grafico
            
        Returns:
            ft.Container: Card configurata per grafici
        """
        device_type = self._get_current_device_type()
        
        # Altezza ottimale per il grafico
        chart_height = ResponsiveHelper.get_optimal_chart_height(device_type)
        
        # Contenuto con altezza fissa per grafici
        content_with_height = ft.Container(
            content=chart_content,
            height=chart_height,
            expand=True
        )
        
        return self.create_weather_info_card(content_with_height, title)
    
    def create_sidebar_card(self, content: ft.Control) -> ft.Container:
        """
        Crea una card per la sidebar adattiva.
        
        Args:
            content: Contenuto della sidebar
            
        Returns:
            ft.Container: Card sidebar configurata
        """
        device_type = self._get_current_device_type()
        
        # Padding ridotto per sidebar
        if device_type == DeviceType.MOBILE:
            padding = ft.padding.all(8)
        elif device_type == DeviceType.TABLET:
            padding = ft.padding.all(12)
        else:
            padding = ft.padding.all(16)
        
        border_radius = ResponsiveHelper.get_responsive_border_radius(device_type, "card")
        
        return ft.Container(
            content=content,
            padding=padding,
            border_radius=border_radius,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            ),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            expand=True
        )
    
    def create_hourly_forecast_card(self, content: ft.Control) -> ft.Container:
        """
        Crea una card per le previsioni orarie con scroll orizzontale su mobile.
        
        Args:
            content: Contenuto delle previsioni orarie
            
        Returns:
            ft.Container: Card configurata per previsioni orarie
        """
        device_type = self._get_current_device_type()
        
        # Su mobile, avvolgi il contenuto in uno scroll orizzontale
        if device_type == DeviceType.MOBILE:
            scrollable_content = ft.Container(
                content=content,
                scroll=ft.ScrollMode.HIDDEN  # Nasconde scrollbar ma consente scroll
            )
            final_content = scrollable_content
        else:
            final_content = content
        
        return self.create_weather_info_card(final_content)
    
    def _get_title_size(self) -> int:
        """Ottiene la dimensione del titolo basata sul dispositivo."""
        device_type = self._get_current_device_type()
        
        size_map = {
            DeviceType.MOBILE: 16,
            DeviceType.TABLET: 18,
            DeviceType.DESKTOP: 20,
            DeviceType.LARGE_DESKTOP: 22
        }
        
        return size_map.get(device_type, 18)
    
    def get_responsive_column_config(self, layout_type: str = "default") -> dict:
        """
        Ottiene la configurazione delle colonne responsive per diversi tipi di layout.
        
        Args:
            layout_type: Tipo di layout ("sidebar", "main", "card_single", "card_half", "card_third")
            
        Returns:
            dict: Configurazione colonne
        """
        configs = {
            "sidebar": {
                "xs": 12,    # Mobile: full width
                "sm": 12,    # Tablet portrait: full width
                "md": 4,     # Tablet landscape: 33%
                "lg": 3,     # Desktop: 25%
                "xl": 3      # Large desktop: 25%
            },
            "main": {
                "xs": 12,    # Mobile: full width
                "sm": 12,    # Tablet portrait: full width
                "md": 8,     # Tablet landscape: 67%
                "lg": 9,     # Desktop: 75%
                "xl": 9      # Large desktop: 75%
            },
            "card_single": {
                "xs": 12,    # Mobile: full width
                "sm": 12,    # Tablet: full width
                "md": 12,    # Tablet landscape: full width
                "lg": 12,    # Desktop: full width
                "xl": 12     # Large desktop: full width
            },
            "card_half": {
                "xs": 12,    # Mobile: full width (stack)
                "sm": 12,    # Tablet portrait: full width
                "md": 6,     # Tablet landscape: 50%
                "lg": 6,     # Desktop: 50%
                "xl": 6      # Large desktop: 50%
            },
            "card_third": {
                "xs": 12,    # Mobile: full width (stack)
                "sm": 12,    # Tablet portrait: full width
                "md": 6,     # Tablet landscape: 50% (2 per riga)
                "lg": 4,     # Desktop: 33% (3 per riga)
                "xl": 4      # Large desktop: 33%
            }
        }
        
        return configs.get(layout_type, configs["card_single"])


class ResponsiveLayoutMixin:
    """
    Mixin per aggiungere funzionalità responsive a componenti esistenti.
    """
    
    def setup_responsive(self, page: ft.Page):
        """
        Configura il componente per essere responsive.
        
        Args:
            page: Pagina Flet
        """
        self.page = page
        self.adaptive_card = AdaptiveCard(page)
        
        # Registra callback per resize se la pagina lo supporta
        if hasattr(page, 'on_resize'):
            original_resize = page.on_resize
            
            def combined_resize(e):
                if original_resize:
                    original_resize(e)
                self._handle_responsive_resize(e)
            
            page.on_resize = combined_resize
    
    def _handle_responsive_resize(self, e):
        """
        Gestisce eventi di resize per aggiornare il layout responsive.
        Deve essere implementato dalle classi che usano questo mixin.
        
        Args:
            e: Evento di resize
        """
        pass
    
    def get_device_adaptive_spacing(self) -> int:
        """Ottiene lo spacing adattivo per il dispositivo corrente."""
        if hasattr(self, 'page') and self.page:
            device_type = ResponsiveHelper.get_device_type(
                self.page.width if hasattr(self.page, 'width') and self.page.width else 1200
            )
            return ResponsiveHelper.get_responsive_spacing(device_type)
        return 12  # Default
    
    def should_use_vertical_layout(self) -> bool:
        """Determina se utilizzare layout verticale basato sul dispositivo."""
        if hasattr(self, 'page') and self.page:
            device_type = ResponsiveHelper.get_device_type(
                self.page.width if hasattr(self.page, 'width') and self.page.width else 1200
            )
            return ResponsiveHelper.should_use_stack_layout(device_type)
        return False
