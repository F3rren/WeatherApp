import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService

class AirConditionInfo:
    """
    Air condition information display.
    """
    
    def __init__(self, feels_like: int, humidity: int, wind_speed: int, 
                 pressure: int, text_color: str, page: ft.Page = None):
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.pressure = pressure
        self.text_color = text_color
        self.page = page 
        
        # Inizializza la lingua dinamicamente PRIMA di usarla
        if page and hasattr(page, 'session') and page.session.get('state_manager'):
            state_manager = page.session.get('state_manager')
            self.language = state_manager.get_state('language') or 'en'
            state_manager.register_observer("language_event", self.handle_language_change)
        else:
            self.language = 'en'

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes= {
                'title': 24,      # Titoli principali (ridotto da 30)
                'label': 16,      # Etichette (ridotto da 20)
                'value': 16,      # Valori (ridotto da 20)
                'icon': 20,       # Icone (aggiunto)
            },
            breakpoints=[600, 900, 1200, 1600]  # Aggiunti breakpoint per il ridimensionamento
        )

        # Dizionario dei controlli per aggiornamento facile
        self.text_controls = {}

        # Creazione dei controlli UI con dimensioni responsive
        self.title_text = ft.Text(TranslationService.get_text("air_condition_title", self.language), size=self.text_handler.get_size('title'), weight="bold", color=self.text_color)
        self.divider = ft.Divider(height=1, color=self.text_color)
        
        # Creazione delle icone con dimensioni responsive
        feels_like_icon = ft.Icon(ft.Icons.THERMOSTAT, size=self.text_handler.get_size('icon'), color=self.text_color)
        humidity_icon = ft.Icon(ft.Icons.WATER_DROP, size=self.text_handler.get_size('icon'), color=self.text_color)
        wind_icon = ft.Icon(ft.Icons.WIND_POWER, size=self.text_handler.get_size('icon'), color=self.text_color)
        pressure_icon = ft.Icon(ft.Icons.COMPRESS, size=self.text_handler.get_size('icon'), color=self.text_color)
        
        # Creazione delle etichette con dimensioni responsive
        feels_like_text = ft.Text(TranslationService.get_text("feels_like", self.language), size=self.text_handler.get_size('label'), weight=ft.FontWeight.BOLD, color=self.text_color)
        humidity_text = ft.Text(TranslationService.get_text("humidity", self.language), size=self.text_handler.get_size('label'), weight=ft.FontWeight.BOLD, color=self.text_color)
        wind_text = ft.Text(TranslationService.get_text("wind", self.language), size=self.text_handler.get_size('label'), weight=ft.FontWeight.BOLD, color=self.text_color)
        pressure_text = ft.Text(TranslationService.get_text("pressure", self.language), size=self.text_handler.get_size('label'), weight=ft.FontWeight.BOLD, color=self.text_color)
        
        self.feels_like_label = ft.Row(
            controls=[feels_like_icon, feels_like_text]
        )
        self.feels_like_value = ft.Text(f"{self.feels_like}°", size=self.text_handler.get_size('value'), italic=True, color=self.text_color)
        
        self.humidity_label = ft.Row(
            controls=[humidity_icon, humidity_text]
        )
        self.humidity_value = ft.Text(f"{self.humidity}%", size=self.text_handler.get_size('value'), italic=True, color=self.text_color)

        self.wind_label = ft.Row(
            controls=[wind_icon, wind_text]
        )
        self.wind_value = ft.Text(f"{self.wind_speed} km/h", size=self.text_handler.get_size('value'), italic=True, color=self.text_color)

        self.pressure_label = ft.Row(
            controls=[pressure_icon, pressure_text]
        )
        self.pressure_value = ft.Text(f"{self.pressure} hPa", size=self.text_handler.get_size('value'), italic=True, color=self.text_color)

        # Registra i controlli di testo nel dizionario per l'aggiornamento
        self.text_controls[self.title_text] = 'title'
        self.text_controls[feels_like_text] = 'label'
        self.text_controls[humidity_text] = 'label'
        self.text_controls[wind_text] = 'label'
        self.text_controls[pressure_text] = 'label'
        self.text_controls[self.feels_like_value] = 'value'
        self.text_controls[self.humidity_value] = 'value'
        self.text_controls[self.wind_value] = 'value'
        self.text_controls[self.pressure_value] = 'value'
        self.text_controls[feels_like_icon] = 'icon'
        self.text_controls[humidity_icon] = 'icon'
        self.text_controls[wind_icon] = 'icon'
        self.text_controls[pressure_icon] = 'icon'
        
        # Sovrascrivi il gestore di ridimensionamento della pagina
        if self.page:
            # Registra l'handler per il cambiamento del tema
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                state_manager.register_observer("theme_event", self.handle_theme_change)
            
            # Registra l'evento di ridimensionamento personalizzato
            original_resize_handler = self.page.on_resize
            
            def combined_resize_handler(e):
                # Aggiorna le dimensioni del testo
                self.text_handler._handle_resize(e)
                # Aggiorna i controlli di testo
                self.update_text_controls()
                # Chiama anche l'handler originale se esiste
                if original_resize_handler:
                    original_resize_handler(e)
            
            self.page.on_resize = combined_resize_handler

    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati"""
        for control, size_category in self.text_controls.items():
            if size_category == 'icon':
                # Per le icone, aggiorna size
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
            else:
                # Per i testi, aggiorna size
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
                elif hasattr(control, 'style') and hasattr(control.style, 'size'):
                    control.style.size = self.text_handler.get_size(size_category)
                # Aggiorna anche i TextSpan se presenti
                if hasattr(control, 'spans'):
                    for span in control.spans:
                        span.style.size = self.text_handler.get_size(size_category)
        
        # Richiedi l'aggiornamento della pagina
        if self.page:
            self.page.update()

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text and divider colors."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]
            
            # Update colors of all relevant controls
            for control, _ in self.text_controls.items():
                if hasattr(control, 'color'):
                    control.color = self.text_color
                if hasattr(control, 'page') and control.page:
                    control.update()
            
            if hasattr(self.divider, 'color'): # Divider color
                self.divider.color = self.text_color
            if hasattr(self.divider, 'page') and self.divider.page:
                self.divider.update()
                    
            # Aggiorna anche le dimensioni del testo
            self.update_text_controls()

    def handle_language_change(self, event_data=None):
        """Aggiorna le label quando cambia la lingua."""
        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                self.language = state_manager.get_state('language') or 'en'
        self.title_text.value = TranslationService.get_text("air_condition_title", self.language)
        # Aggiorna le label delle righe
        for row, key in zip([self.feels_like_label, self.humidity_label, self.wind_label, self.pressure_label], ["feels_like", "humidity", "wind", "pressure"]):
            if isinstance(row.controls[1], ft.Text):
                row.controls[1].value = TranslationService.get_text(key, self.language)
                row.controls[1].update()
        self.title_text.update()
        self.update_text_controls()

    def build(self) -> ft.Container:
        """Build the air condition information"""
        # Quando il componente viene costruito, assicurati che il testo sia correttamente dimensionato
        self.update_text_controls()
        
        return ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    self.title_text,
                    self.divider,
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    self.feels_like_label,
                                    self.feels_like_value,
                                    self.humidity_label,
                                    self.humidity_value,
                                ],
                                expand=True,
                            ),
                            ft.Column(
                                controls=[
                                    self.wind_label,
                                    self.wind_value,
                                    self.pressure_label,
                                    self.pressure_value,
                                ],
                                expand=True,
                            ),
                        ],
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )

