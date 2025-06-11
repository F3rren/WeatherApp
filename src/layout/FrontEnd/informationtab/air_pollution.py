import flet as ft
from services.api_service import ApiService
from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME, DEFAULT_UNIT_SYSTEM # Added DEFAULT_UNIT_SYSTEM
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
        self.initial_text_color = text_color # Store initial text color
        self._state_manager = None
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

        if page and hasattr(page, 'session') and page.session.get('state_manager'):
            self._state_manager = page.session.get('state_manager')
            self.language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
            self.unit_system = self._state_manager.get_state('unit_system') or DEFAULT_UNIT_SYSTEM # Added
            self.text_color = self._determine_text_color()

            self._state_manager.register_observer("language_event", self._handle_state_change)
            self._state_manager.register_observer("theme_event", self._handle_state_change) # Combined handler
            # No unit_event needed here as air pollution units (μg/m³) are standard and not switchable by user
        else:
            self.language = DEFAULT_LANGUAGE
            self.unit_system = DEFAULT_UNIT_SYSTEM # Added
            self.text_color = self.initial_text_color if self.initial_text_color else (DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"])

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

        self.text_controls_map = {} # To store {control: category} for resize updates
        self.container_control = None # Will hold the main ft.Container
        
        original_resize_handler = self.page.on_resize
        def combined_resize_handler(e):
            self.text_handler._handle_resize(e)
            self._update_text_sizes_and_colors() # Update on resize
            if original_resize_handler:
                original_resize_handler(e)
        self.page.on_resize = combined_resize_handler

        if lat is not None and lon is not None:
            self.update_data(lat, lon) # This will also trigger a build if container_control exists

    def _determine_text_color(self):
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config["TEXT"]
        return self.initial_text_color

    def _handle_state_change(self, event_data=None):
        """Handles language or theme changes."""
        if self._state_manager:
            self.language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
            # self.unit_system remains as air pollution units are fixed
        self.text_color = self._determine_text_color()
        self._rebuild_ui() # Rebuild UI to reflect changes

    def _update_text_sizes_and_colors(self):
        """Updates sizes and colors of all registered text controls."""
        for control, category in self.text_controls_map.items():
            new_size = self.text_handler.get_size(category)
            if hasattr(control, 'size'):
                control.size = new_size
            if hasattr(control, 'color'): # Update color for simple Text controls
                 if not (control == self.aqi_value_text and self.aqi > 2): # Special case for AQI value background
                    control.color = self.text_color
            
            # Handle TextSpans within a Text control (e.g., pollution details)
            if hasattr(control, 'spans'):
                for span in control.spans:
                    if hasattr(span, 'style') and span.style:
                        span.style.size = new_size
                        # Color for spans is handled during creation based on context
                        # or updated directly if needed (e.g. a general text color change)
                        if span != self.value_span: # Assuming value_span might have specific color logic
                             span.style.color = self.text_color
            if hasattr(control, 'page') and control.page: # Guard update
                control.update()
        # Removed self.page.update() - let higher level components manage page updates if needed

    def _rebuild_ui(self):
        """Reconstructs the UI elements when language or theme changes."""
        if self.container_control and self.lat is not None and self.lon is not None:
            # Pollution data itself doesn't change with language/theme, only its display
            new_content = self.createAirPollutionTab() # This now calls _update_text_sizes_and_colors internally at the end
            self.container_control.content = new_content
            if hasattr(self.container_control, 'page') and self.container_control.page: # Guard update
                self.container_control.update()
            # REMOVED: self._update_text_sizes_and_colors() call from here as it's in createAirPollutionTab

    def update_data(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.pollution_data = self.api.get_air_pollution(lat, lon) or {}
        
        self.aqi = self.pollution_data.get("aqi", 0)
        self.co = self.pollution_data.get("co", 0)
        self.no = self.pollution_data.get("no", 0)
        self.no2 = self.pollution_data.get("no2", 0)
        self.o3 = self.pollution_data.get("o3", 0)
        self.so2 = self.pollution_data.get("so2", 0)
        self.pm2_5 = self.pollution_data.get("pm2_5", 0)
        self.pm10 = self.pollution_data.get("pm10", 0)
        self.nh3 = self.pollution_data.get("nh3", 0)
        
        self._rebuild_ui() # Rebuild UI with new data
    
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
        self.text_controls_map.clear()
        
        aqi_title_text = TranslationService.get_text("air_quality_index", self.language)
        aqi_title = ft.Text(aqi_title_text, weight="bold", color=self.text_color)
        self.text_controls_map[aqi_title] = 'title'

        aqi_desc = self._get_aqi_description()
        self.aqi_value_text = ft.Text(
            aqi_desc, weight="bold", 
            color=self.text_color if self.aqi <= 2 else "#ffffff" # White text on darker backgrounds
        )
        self.text_controls_map[self.aqi_value_text] = 'title' 
        
        aqi_row = ft.Row([
            aqi_title,
            ft.Container(
                content=self.aqi_value_text,
                bgcolor=self._get_aqi_color(),
                border_radius=10, padding=10, alignment=ft.alignment.center, expand=True
            )
        ])
        
        elements = TranslationService.get_chemical_elements(self.language)
        pollution_values = [self.co, self.no, self.no2, self.o3, self.so2, self.pm2_5, self.pm10, self.nh3]
        
        # Create two columns for pollutant details
        column1_controls = []
        column2_controls = []

        num_elements = len(elements) # elements is a dict here
        mid_point = (num_elements + 1) // 2

        # Iterate over dictionary items (key-value pairs)
        # The order of elements.items() should be consistent with pollution_values
        # if Python version is 3.7+ and the dictionary in translations_data.py has a fixed order.
        for i, (symbol, description) in enumerate(elements.items()):
            # symbol is the key (e.g., "CO"), description is the value (e.g., "Carbon Monoxide")
            if i < len(pollution_values): # Ensure we don't go out of bounds for pollution_values
                value = pollution_values[i]
            else:
                value = 0 # Default value if pollution_values is shorter for some reason
            
            value_str = f"{value:.2f} μg/m³"
            
            desc_text = ft.Text(description, color=self.text_color)
            self.text_controls_map[desc_text] = 'label'
            
            # Using separate Text controls for symbol and value for clarity
            symbol_text = ft.Text(f"{symbol}:", weight=ft.FontWeight.BOLD, color=self.text_color)
            self.text_controls_map[symbol_text] = 'value' 
            
            value_text_control = ft.Text(value_str, color=self.text_color) # Renamed from item_text to avoid confusion
            self.text_controls_map[value_text_control] = 'value'

            pollutant_item_column = ft.Column(
                controls=[
                    desc_text,
                    ft.Row([symbol_text, value_text_control], spacing=5) # Symbol and value in a row
                ],
                spacing=2, # Reduced spacing within the item
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            )

            item_container = ft.Container(
                content=pollutant_item_column,
                padding=ft.padding.symmetric(vertical=5) # Add some vertical padding
            )
            
            if i < mid_point:
                column1_controls.append(item_container)
            else:
                column2_controls.append(item_container)
        
        pollutants_row = ft.Row(
            controls=[
                ft.Column(column1_controls, spacing=10, expand=True),
                ft.Column(column2_controls, spacing=10, expand=True)
            ],
            spacing=20 # Spacing between the two main columns
        )
        
        main_column = ft.Column(
            controls=[aqi_row, ft.Divider(height=1, color=self.text_color), pollutants_row],
            spacing=15, # Increased spacing between AQI and pollutants
            expand=True
        )
        return main_column

    def build(self):
        # Initial build, or rebuild if called directly
        # Create content first
        content = self.createAirPollutionTab()
        self.container_control = ft.Container(
            content=content,
            expand=True,
            padding=10
        )
        # After container_control is created and has content, if it were added to the page here,
        # then a call to _update_text_sizes_and_colors would be appropriate.
        # Since build() just returns the control, the caller (WeatherView) is responsible for adding it.
        # WeatherView should then trigger an update if necessary, or rely on state changes.
        return self.container_control


