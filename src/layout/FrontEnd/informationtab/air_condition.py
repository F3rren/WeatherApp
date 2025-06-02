import flet as ft
from config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class AirConditionInfo:
    """
    Air condition information display.
    """
    
    def __init__(self, feels_like: int, humidity: int, wind_speed: int, 
                 pressure: int, text_color: str, page: ft.Page = None): # Added page
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.pressure = pressure
        self.text_color = text_color
        self.page = page # Store page
        
        # Inizializza il gestore del testo responsive
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 45,   # Titolo "Condizioni Atmosferiche" (aumentato da 25 a 45)
                'label': 40,   # Etichette come "Percepita", "Umidità" (aumentato da 20 a 40)
                'value': 40    # Valori come temperature, percentuali (aumentato da 20 a 40)
            }
        )

        # Store text controls that need dynamic color updates
        self.title_text = ft.Text("Condizioni Atmosferiche", size=self.text_handler.get_size('title'), weight="bold", color=self.text_color)
        self.divider = ft.Divider(height=1, color=self.text_color)

        self.feels_like_label = ft.Text("Percepita", size=self.text_handler.get_size('label'), color=self.text_color)
        self.feels_like_value = ft.Text(f"{self.feels_like}°", size=self.text_handler.get_size('value'), weight="bold", color=self.text_color)
        self.humidity_label = ft.Text("Umidità", size=self.text_handler.get_size('label'), color=self.text_color)
        self.humidity_value = ft.Text(f"{self.humidity}%", size=self.text_handler.get_size('value'), weight="bold", color=self.text_color)
        
        self.wind_label = ft.Text("Vento", size=self.text_handler.get_size('label'), color=self.text_color)
        self.wind_value = ft.Text(f"{self.wind_speed} km/h", size=self.text_handler.get_size('value'), weight="bold", color=self.text_color)
        self.pressure_label = ft.Text("Pressione", size=self.text_handler.get_size('label'), color=self.text_color)
        self.pressure_value = ft.Text(f"{self.pressure} hPa", size=self.text_handler.get_size('value'), weight="bold", color=self.text_color)
        
        # Dizionario dei controlli per aggiornamento facile
        self.text_controls = {
            self.title_text: 'title',
            self.feels_like_label: 'label',
            self.feels_like_value: 'value',
            self.humidity_label: 'label',
            self.humidity_value: 'value',
            self.wind_label: 'label',
            self.wind_value: 'value',
            self.pressure_label: 'label',
            self.pressure_value: 'value'
        }
        
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
                self.text_handler.update_text_controls(self.text_controls)
                # Chiama anche l'handler originale se esiste
                if original_resize_handler:
                    original_resize_handler(e)
            
            self.page.on_resize = combined_resize_handler

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text and divider colors."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]

            # Update colors of all relevant controls
            controls_to_update = list(self.text_controls.keys())
            
            for control in controls_to_update:
                if hasattr(control, 'color'):
                    control.color = self.text_color
                if hasattr(control, 'page') and control.page:
                    control.update()
            
            if hasattr(self.divider, 'color'): # Divider color
                self.divider.color = self.text_color
                if hasattr(self.divider, 'page') and self.divider.page:
                    self.divider.update()
                    
            # Aggiorna anche le dimensioni del testo
            self.text_handler.update_text_controls(self.text_controls)

    def build(self) -> ft.Container:
        """Build the air condition information"""
        return ft.Container(
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

