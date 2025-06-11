import flet as ft
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME
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
        self.state_manager = None

        if page and hasattr(page, 'session') and page.session.get('state_manager'):
            self.state_manager = page.session.get('state_manager')
            self.language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            self.unit_system = self.state_manager.get_state('unit') or "metric" # Default to metric
            self.state_manager.register_observer("language_event", self._handle_language_or_unit_change)
            self.state_manager.register_observer("unit_event", self._handle_language_or_unit_change)
            self.state_manager.register_observer("theme_event", self.handle_theme_change)
        else:
            self.language = DEFAULT_LANGUAGE
            self.unit_system = "metric"

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes= {
                'title': 24,
                'label': 16,
                'value': 16,
                'icon': 20,
            },
            breakpoints=[600, 900, 1200, 1600]
        )

        self.text_controls = {}

        # Create UI controls (placeholders, will be updated by _update_all_text_elements)
        self.title_text = ft.Text(size=self.text_handler.get_size('title'), weight="bold", color=self.text_color)
        self.divider = ft.Divider(height=1, color=self.text_color)
        
        feels_like_icon = ft.Icon(ft.Icons.THERMOSTAT, size=self.text_handler.get_size('icon'), color=self.text_color)
        humidity_icon = ft.Icon(ft.Icons.WATER_DROP, size=self.text_handler.get_size('icon'), color=self.text_color)
        wind_icon = ft.Icon(ft.Icons.WIND_POWER, size=self.text_handler.get_size('icon'), color=self.text_color)
        pressure_icon = ft.Icon(ft.Icons.COMPRESS, size=self.text_handler.get_size('icon'), color=self.text_color)
        
        self.feels_like_label_text = ft.Text(size=self.text_handler.get_size('label'), weight=ft.FontWeight.BOLD, color=self.text_color)
        self.humidity_label_text = ft.Text(size=self.text_handler.get_size('label'), weight=ft.FontWeight.BOLD, color=self.text_color)
        self.wind_label_text = ft.Text(size=self.text_handler.get_size('label'), weight=ft.FontWeight.BOLD, color=self.text_color)
        self.pressure_label_text = ft.Text(size=self.text_handler.get_size('label'), weight=ft.FontWeight.BOLD, color=self.text_color)
        
        self.feels_like_label = ft.Row(controls=[feels_like_icon, self.feels_like_label_text])
        self.feels_like_value = ft.Text(size=self.text_handler.get_size('value'), italic=True, color=self.text_color)
        
        self.humidity_label = ft.Row(controls=[humidity_icon, self.humidity_label_text])
        self.humidity_value = ft.Text(size=self.text_handler.get_size('value'), italic=True, color=self.text_color)

        self.wind_label = ft.Row(controls=[wind_icon, self.wind_label_text])
        self.wind_value = ft.Text(size=self.text_handler.get_size('value'), italic=True, color=self.text_color)

        self.pressure_label = ft.Row(controls=[pressure_icon, self.pressure_label_text])
        self.pressure_value = ft.Text(size=self.text_handler.get_size('value'), italic=True, color=self.text_color)

        self.text_controls[self.title_text] = 'title'
        self.text_controls[self.feels_like_label_text] = 'label'
        self.text_controls[self.humidity_label_text] = 'label'
        self.text_controls[self.wind_label_text] = 'label'
        self.text_controls[self.pressure_label_text] = 'label'
        self.text_controls[self.feels_like_value] = 'value'
        self.text_controls[self.humidity_value] = 'value'
        self.text_controls[self.wind_value] = 'value'
        self.text_controls[self.pressure_value] = 'value'
        self.text_controls[feels_like_icon] = 'icon'
        self.text_controls[humidity_icon] = 'icon'
        self.text_controls[wind_icon] = 'icon'
        self.text_controls[pressure_icon] = 'icon'
        
        # Register observer with ResponsiveTextHandler
        self.text_handler.add_observer(self.update_text_controls)
        
        # Sovrascrivi il gestore di ridimensionamento della pagina per questo componente
        if self.page:
            # Salva l'handler originale se presente
            self._original_resize_handler = self.page.on_resize
            
            def combined_resize_handler(e):
                # Aggiorna le dimensioni del testo
                self.text_handler._handle_resize(e)
                # Aggiorna i controlli di testo
                self.update_text_controls()
                # Chiama anche l'handler originale se esiste
                if hasattr(self, '_original_resize_handler') and self._original_resize_handler:
                    self._original_resize_handler(e)
            
            self.page.on_resize = combined_resize_handler
            
        self._update_all_text_elements() # Initial text setup

    def _update_all_text_elements(self):
        """Updates all text elements including labels, values, and unit symbols."""
        # Update title
        self.title_text.value = TranslationService.get_text("air_condition_title", self.language)

        # Update labels
        self.feels_like_label_text.value = TranslationService.get_text("feels_like", self.language)
        self.humidity_label_text.value = TranslationService.get_text("humidity", self.language)
        self.wind_label_text.value = TranslationService.get_text("wind", self.language)
        self.pressure_label_text.value = TranslationService.get_text("pressure", self.language)

        # Update values with units
        temp_unit_symbol = TranslationService.get_unit_symbol("temperature", self.unit_system, self.language)
        self.feels_like_value.value = f"{self.feels_like}{temp_unit_symbol}"
        
        self.humidity_value.value = f"{self.humidity}%" # Humidity is a percentage, no unit symbol needed from service

        wind_unit_symbol = TranslationService.get_unit_symbol("wind", self.unit_system, self.language)
        self.wind_value.value = f"{self.wind_speed} {wind_unit_symbol}"
        
        pressure_unit_symbol = TranslationService.get_unit_symbol("pressure", self.unit_system, self.language)
        self.pressure_value.value = f"{self.pressure} {pressure_unit_symbol}"

        self.update_text_controls() # Apply text sizes and update page

    def _handle_language_or_unit_change(self, event_data=None):
        """Handles language or unit change events."""
        if self.state_manager:
            new_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            new_unit_system = self.state_manager.get_state('unit') or "metric"
            
            changed = False
            if self.language != new_language:
                self.language = new_language
                changed = True
            if self.unit_system != new_unit_system:
                self.unit_system = new_unit_system
                changed = True
            if changed:
                self._update_all_text_elements()
        else: # Fallback if state_manager is not available
            self._update_all_text_elements()
    
    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati"""
        for control, size_category in self.text_controls.items():
            new_size = self.text_handler.get_size(size_category)
            
            if size_category == 'icon':
                # Per le icone, aggiorna size
                if hasattr(control, 'size'):
                    control.size = new_size
                elif hasattr(control, 'width') and hasattr(control, 'height'):
                    control.width = new_size
                    control.height = new_size
            else:
                # Per i testi, aggiorna size
                if hasattr(control, 'size'):
                    control.size = new_size
                elif hasattr(control, 'style') and hasattr(control.style, 'size'):
                    control.style.size = new_size
                # Aggiorna anche i TextSpan se presenti
                if hasattr(control, 'spans'):
                    for span in control.spans:
                        if hasattr(span, 'style') and span.style:
                            span.style.size = new_size
        
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
                # No individual updates needed here, page.update() in _update_all_text_elements or update_text_controls handles it
            
            if hasattr(self.divider, 'color'): 
                self.divider.color = self.text_color

            self._update_all_text_elements() # Re-render texts with new theme and potentially new sizes

    def cleanup(self):
        """Unregister observers to prevent memory leaks."""
        if self.state_manager:
            self.state_manager.unregister_observer("theme_event", self.handle_theme_change)
            self.state_manager.unregister_observer("language_event", self._handle_language_or_unit_change)
            self.state_manager.unregister_observer("unit_event", self._handle_language_or_unit_change)
        
        # Unregister observer from ResponsiveTextHandler
        if hasattr(self, 'text_handler') and self.text_handler:
            self.text_handler.remove_observer(self.update_text_controls)
            
        # Ripristina l'handler originale di resize se esiste
        if hasattr(self, '_original_resize_handler') and self.page:
            self.page.on_resize = self._original_resize_handler

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
