import flet as ft
from services.api_service import ApiService
from services.translation_service import TranslationService
from utils.config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class AirPollution:
    """
    Air pollution display component.
    Shows detailed air quality information.
    """
    
    def __init__(self, page, lat=None, lon=None, text_color: str = None):
        """
        Initialize the AirPollution component.
        
        Args:
            page: Flet page object
            lat: Latitude (optional)
            lon: Longitude (optional)
            text_color: Initial text color (optional)
        """
        self.page = page
        self.lat = lat
        self.lon = lon
        # Set initial text_color or derive from theme
        if text_color:
            self.text_color = text_color
        else:
            self.text_color = DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"]
    
        self.api = ApiService()
        self.pollution_data = {}
        
        # Initialize with default values
        self.aqi = 0
        self.co = 0
        self.no = 0
        self.no2 = 0
        self.o3 = 0
        self.so2 = 0
        self.pm2_5 = 0
        self.pm10 = 0
        self.nh3 = 0


         # Inizializza la lingua dinamicamente PRIMA di usarla
        if page and hasattr(page, 'session') and page.session.get('state_manager'):
            state_manager = page.session.get('state_manager')
            self.language = state_manager.get_state('language') or 'en'
            state_manager.register_observer("language_event", self.handle_language_change)
        else:
            self.language = 'en'

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20,      # Titoli principali
                'label': 15,      # Etichette
                'value': 15,      # Valori (es. temperature, percentuali)
                'subtitle': 15,   # Sottotitoli
            },
            breakpoints=[600, 900, 1200, 1600]  # Aggiunti breakpoint per il ridimensionamento
        )

        # Dizionario dei controlli di testo per aggiornamento facile
        self.text_controls = {}
        
        # Sovrascrivi il gestore di ridimensionamento della pagina
        if self.page:
            # Salva l'handler originale se presente
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

        # Update data if coordinates are provided
        if lat is not None and lon is not None:
            self.update_data(lat, lon)


    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati"""
        for control, size_category in self.text_controls.items():
            if hasattr(control, 'size'):
                control.size = self.text_handler.get_size(size_category)
            elif hasattr(control, 'style') and hasattr(control.style, 'size'):
                control.style.size = self.text_handler.get_size(size_category)
            # Aggiorna anche i TextSpan se presenti
            if hasattr(control, 'spans'):
                for span in control.spans:
                    span.style.size = self.text_handler.get_size(size_category)
        # Non chiamare self.page.update() qui per evitare errori se i controlli non sono ancora nella pagina

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color and relevant UI elements."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]
            
            # Aggiorna il colore e le dimensioni del testo per tutti gli elementi
            if hasattr(self, 'container_control') and self.container_control.page:
                # Ricostruisci il contenuto con i nuovi colori
                if self.lat is not None and self.lon is not None:
                    self.container_control.content = self.createAirPollutionTab()
                    self.container_control.update()

    def update_data(self, lat, lon):
        """
        Update air pollution data with new coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
        """
        self.lat = lat
        self.lon = lon
        
        # Get air pollution data
        self.pollution_data = self.api.get_air_pollution(lat, lon)
        
        # Update component properties
        self.aqi = self.pollution_data.get("aqi", 0)
        self.co = self.pollution_data.get("co", 0)
        self.no = self.pollution_data.get("no", 0)
        self.no2 = self.pollution_data.get("no2", 0)
        self.o3 = self.pollution_data.get("o3", 0)
        self.so2 = self.pollution_data.get("so2", 0)
        self.pm2_5 = self.pollution_data.get("pm2_5", 0)
        self.pm10 = self.pollution_data.get("pm10", 0)
        self.nh3 = self.pollution_data.get("nh3", 0)
    
    def _get_aqi_description(self) -> str:
        """Get localized description based on Air Quality Index"""
        lang_code = TranslationService.normalize_lang_code(self.language)
        aqi_descriptions = TranslationService.TRANSLATIONS.get(lang_code, TranslationService.TRANSLATIONS["en"]).get("aqi_descriptions", [])
        # Ensure the list has at least 6 elements, fallback to English or generic labels if not
        if len(aqi_descriptions) < 6:
            aqi_descriptions = TranslationService.TRANSLATIONS["en"].get("aqi_descriptions", ["N/A", "Good", "Fair", "Moderate", "Poor", "Very Poor"])
        idx = min(self.aqi, 5)
        if idx >= len(aqi_descriptions):
            return aqi_descriptions[0] if aqi_descriptions else "N/A"
        return aqi_descriptions[idx]
    
    def _get_aqi_color(self) -> str:
        """Get color based on Air Quality Index"""
        colors = [
            "#808080",  # Gray for N/A
            "#00E400",  # Green for Good
            "#FFFF00",  # Yellow for Fair
            "#FF7E00",  # Orange for Moderate
            "#FF0000",  # Red for Poor
            "#99004C"   # Purple for Very Poor
        ]
        return colors[min(self.aqi, 5)]
    
    def createAirPollutionTab(self):
        """Create the air pollution tab content"""
        # Reset text controls dictionary before rebuilding
        self.text_controls = {}
        
        # AQI indicator
        aqi_title = ft.Text(TranslationService.get_text("air_quality_index", self.language),size=self.text_handler.get_size('title'), weight="bold", color=self.text_color)

        aqi_value = ft.Text(
            self._get_aqi_description(),
            size=self.text_handler.get_size('title'),
            weight="bold",
            color=self.text_color if self.aqi <= 2 else "#ffffff"
        )
        
        # Register text controls
        self.text_controls[aqi_title] = 'title'
        self.text_controls[aqi_value] = 'title'
        
        aqi_row = ft.Row([
            aqi_title,
            ft.Container(
                content=aqi_value,
                bgcolor=self._get_aqi_color(),
                border_radius=10,
                padding=10,
                alignment=ft.alignment.center,
                expand=True
            )
        ])
        
        # Ottieni la lista delle descrizioni localizzate degli elementi chimici tramite deep_translator
        elements = TranslationService.get_chemical_elements(self.language)
        pollution_data = []
        values = [self.co, self.no, self.no2, self.o3, self.so2, self.pm2_5, self.pm10, self.nh3]
        for (symbol, desc), value in zip(elements, values):
            pollution_data.append((symbol, value, "μg/m³", desc))
        
        pollution_rows = []
        divider = ft.Divider(height=20, color=self.text_color)
        
        # Create rows with 2 items per row
        for i in range(0, len(pollution_data), 2):
            row_items = []
            
            # Add first item
            name1, value1, unit1, desc1 = pollution_data[i]
            name1_text = ft.Text(name1, weight="bold", size=self.text_handler.get_size('label'), color=self.text_color)
            value1_text = ft.Text(f"{value1} {unit1}", size=self.text_handler.get_size('value'), color=self.text_color)
            desc1_text_control = ft.Text(desc1, size=self.text_handler.get_size('value'), color=self.text_color, italic=True)

            # Register text controls
            self.text_controls[name1_text] = 'label'
            self.text_controls[value1_text] = 'value'
            self.text_controls[desc1_text_control] = 'value'
            
            row_items.append(
                ft.Container(
                    content=ft.Column([name1_text, value1_text, desc1_text_control]),
                    padding=10,
                    border_radius=10,
                    expand=True
                )
            )
            
            # Add second item if exists
            if i + 1 < len(pollution_data):
                name2, value2, unit2, desc2 = pollution_data[i+1]
                name2_text = ft.Text(name2, weight="bold", size=self.text_handler.get_size('label'), color=self.text_color)
                value2_text = ft.Text(f"{value2} {unit2}", size=self.text_handler.get_size('value'), color=self.text_color)
                desc2_text_control = ft.Text(desc2, size=self.text_handler.get_size('value'), color=self.text_color, italic=True)
                
                # Register text controls
                self.text_controls[name2_text] = 'label'
                self.text_controls[value2_text] = 'value'
                self.text_controls[desc2_text_control] = 'value'
                
                row_items.append(
                    ft.Container(
                        content=ft.Column([name2_text, value2_text, desc2_text_control]),
                        padding=10,
                        border_radius=10,
                        expand=True
                    )
                )
            
            pollution_rows.append(ft.Row(row_items, spacing=10))

        return ft.Column(
            controls=[
                aqi_row,
                divider,
                *pollution_rows
            ],
            spacing=10,
            #expand=True # remove expand true if it causes issues
        )
    
    def handle_language_change(self, event_data=None):
        """Aggiorna le label quando cambia la lingua, mostrando un messaggio di caricamento durante la traduzione."""
        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                self.language = state_manager.get_state('language') or 'en'
        # Mostra messaggio di caricamento se il controllo è già renderizzato
        if hasattr(self, 'container_control') and getattr(self.container_control, 'page', None) is not None:
            self.container_control.content = ft.Column([
                ft.Text("Traduzione in corso...", italic=True, color=self.text_color)
            ])
            self.container_control.update()
            # Ricostruisci il contenuto reale dopo un breve delay per permettere il rendering del messaggio
            import threading
            def delayed_update():
                import time
                time.sleep(0.05)  # 50ms per mostrare il messaggio
                if hasattr(self, 'container_control') and getattr(self.container_control, 'page', None) is not None:
                    self.container_control.content = self.createAirPollutionTab()
                    self.container_control.update()
            threading.Thread(target=delayed_update).start()

    def build(self):
        """Build the air pollution component"""
        self.container_control = ft.Container(
            border_radius=15,
            padding=20,
            content=self.createAirPollutionTab(),
        )
        return self.container_control
