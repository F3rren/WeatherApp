import flet as ft
from config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class MainWeatherInfo:
    """
    Main weather information display.
    """
    
    def __init__(self, city: str, location: str, temperature: int, 
                 weather_icon: str, text_color: str, page: ft.Page = None): # Added page for state_manager access
        self.city = city.upper() # Changed to accept city name as string
        self.location = location
        self.temperature = temperature
        self.weather_icon = weather_icon
        self.text_color = text_color
        self.page = page # Store page to access state_manager if needed for observing theme
        
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes= {
                'title': 36,      # Ridotto da 50 (Titoli principali)
                'subtitle': 20,   # Ridotto da 30 (Sottotitoli)
                'label': 30,      # Ridotto da 40 (Etichette)
                'icon': 80,       # Aggiunto per icone meteo
            },
            breakpoints=[600, 900, 1200, 1600]  # Aggiunti breakpoint per il ridimensionamento
        )
        
        # Dizionario dei controlli di testo per aggiornamento facile
        self.text_controls = {}

        # Text controls that need dynamic color updates
        self.city_text = ft.Text(
            self.city.split(", ")[0], 
            size=self.text_handler.get_size('title'), 
            weight="bold", 
            color=self.text_color
        ) 
        
        self.location_text = ft.Text(
            self.location, 
            size=self.text_handler.get_size('subtitle'), 
            color=self.text_color
        )
        
        self.temperature_text = ft.Text(
            f"{self.temperature}°", 
            size=self.text_handler.get_size('label'), 
            weight="bold", 
            color=self.text_color
        )
        
        self.icon_size = self.text_handler.get_size('icon')

        # Aggiungi i controlli al dizionario per l'aggiornamento dinamico
        self.text_controls[self.city_text] = 'title'
        self.text_controls[self.location_text] = 'subtitle'
        self.text_controls[self.temperature_text] = 'label'

        # Register for theme change events if page and state_manager are available
        if self.page:
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
                # Per le icone, aggiorna width e height
                if hasattr(control, 'width') and hasattr(control, 'height'):
                    control.width = self.text_handler.get_size(size_category)
                    control.height = self.text_handler.get_size(size_category)
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
        """Handles theme change events by updating text color."""
        if self.page: # Ensure page context is available
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]
            
            # Update text colors of the controls
            if hasattr(self, 'city_text'): # Check if attribute exists
                self.city_text.color = self.text_color
                if self.city_text.page: 
                    self.city_text.update()
                    
            if hasattr(self, 'location_text'):
                self.location_text.color = self.text_color
                if self.location_text.page: 
                    self.location_text.update()
                    
            if hasattr(self, 'temperature_text'):
                self.temperature_text.color = self.text_color
                if self.temperature_text.page:
                    self.temperature_text.update()
            
            # Aggiorna anche le dimensioni del testo
            self.update_text_controls()
            
    def build(self) -> ft.Container:
        """Build the main weather information"""
        # Verifica che l'icona meteo sia aggiunta al dizionario dei controlli se utilizzata
        if hasattr(self, 'weather_icon') and self.weather_icon:
            weather_icon_img = ft.Image(
                src=f"https://openweathermap.org/img/wn/{self.weather_icon}@4x.png",
                width=self.text_handler.get_size('icon'),
                height=self.text_handler.get_size('icon'),
            )
            self.text_controls[weather_icon_img] = 'icon'
        
        # Aggiornamento iniziale delle dimensioni del testo
        self.update_text_controls()
        
        return ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Container(
                        ft.Column(
                            controls=[
                                self.city_text,
                                self.location_text,
                                self.temperature_text,
                            ],
                            expand=True, 
                        ),
                        padding=5,
                        col={"xs": 12, "md": 6, "lg": 11},
                    ),
                ],
                expand=True,
            ),
            padding=20
        )
