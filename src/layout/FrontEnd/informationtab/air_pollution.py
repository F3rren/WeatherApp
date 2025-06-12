import flet as ft
# import traceback # Removed unused import
from services.api_service import ApiService
from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME # Removed DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler

class AirPollutionDisplay(ft.Container): # CHANGED: Inherits from ft.Container, renamed for clarity
    """
    Air pollution display component.
    Shows detailed air quality information.
    Manages its own UI construction, updates, and state observers.
    """
    
    def __init__(self, page: ft.Page, lat: float = None, lon: float = None, **kwargs):
        super().__init__(**kwargs) # Pass kwargs to ft.Container
        self.page = page
        self._lat = lat # Store initial lat
        self._lon = lon # Store initial lon
        
        self._api_service = ApiService()
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        # Air pollution units (μg/m³) are standard, no _current_unit_system needed for data fetching
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._pollution_data = {} # To store fetched pollution data
        self._ui_elements_built = False

        # ResponsiveTextHandler for elements within this component
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20,
                'label': 15,
                'value': 15,
                'subtitle': 15, # Retained from original, though might not be used directly
                'aqi_value': 16 # Specific size for AQI value text
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Default container properties (can be overridden by kwargs)
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
        self.content = ft.Text("Loading air pollution data...") # Initial placeholder

    def did_mount(self):
        """Called when the control is added to the page."""
        if self.page and self._text_handler and not self._text_handler.page:
            self._text_handler.page = self.page # Ensure text_handler has page context
        
        self._initialize_state_and_observers()
        if self._lat is not None and self._lon is not None:
            if self.page:
                self.page.run_task(self._fetch_data_and_request_rebuild)

    async def _fetch_data_and_request_rebuild(self):
        """Fetches data and then requests a UI rebuild."""
        await self._fetch_air_pollution_data()
        self._request_ui_rebuild()

    def _initialize_state_and_observers(self):
        """Initializes state manager and registers observers."""
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._current_language = self._state_manager.get_state('language') or self._current_language
            
            self._state_manager.register_observer("language_event", self._handle_language_change)
            self._state_manager.register_observer("theme_event", self._handle_theme_change)
        
        if self.page:
            self._original_on_resize = self.page.on_resize
            self.page.on_resize = self._combined_resize_handler

    def will_unmount(self):
        """Called when the control is removed from the page."""
        if self._state_manager:
            self._state_manager.unregister_observer("language_event", self._handle_language_change)
            self._state_manager.unregister_observer("theme_event", self._handle_theme_change)
        
        if self.page and hasattr(self, '_original_on_resize'):
            # Restore the original on_resize handler that was present before this component was mounted
            self.page.on_resize = self._original_on_resize
        elif self.page and self.page.on_resize == self._combined_resize_handler:
            # If this component's handler is still the active one and no original was stored (e.g., it was the first)
            # set it to None or a default handler if appropriate. For now, setting to original (which might be None).
            self.page.on_resize = self._original_on_resize


    def _determine_text_color_from_theme(self):
        """Determines text color based on the current page theme."""
        if self.page and self.page.theme_mode:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config.get("TEXT", ft.Colors.BLACK)
        return LIGHT_THEME.get("TEXT", ft.Colors.BLACK) # Default if page or theme_mode not set

    async def _fetch_air_pollution_data(self):
        """Fetches air pollution data using ApiService."""
        if self._lat is None or self._lon is None:
            self._pollution_data = {}
            return
        # ApiService.get_air_pollution now returns a processed dictionary
        self._pollution_data = self._api_service.get_air_pollution(self._lat, self._lon) or {}

    def _build_ui_elements(self):
        """Constructs the UI for air pollution data."""
        # CHANGED: Check for 'aqi' key in the processed data
        if not self._pollution_data or "aqi" not in self._pollution_data:
            return ft.Text(
                TranslationService.get_text("no_air_pollution_data", self._current_language),
                color=self._current_text_color,
                size=self._text_handler.get_size('label')
            )

        # CHANGED: Directly access 'aqi' and 'components' from the processed self._pollution_data
        aqi = self._pollution_data.get("aqi", 0) # Use .get for safety
        # Components are the other keys in self._pollution_data, excluding 'aqi'
        components = {k: v for k, v in self._pollution_data.items() if k != "aqi"}


        # AQI Title and Value
        aqi_title_text = TranslationService.get_text("air_quality_index", self._current_language)
        aqi_title_control = ft.Text(
            aqi_title_text, 
            weight=ft.FontWeight.BOLD, 
            color=self._current_text_color,
            size=self._text_handler.get_size('title'),
            data={'type': 'text', 'category': 'title'}
        )
        
        aqi_desc = self._get_aqi_description(aqi)
        aqi_value_control = ft.Text(
            aqi_desc, 
            weight=ft.FontWeight.BOLD, 
            color="#ffffff" if aqi > 2 else self._current_text_color, # White text on darker AQI backgrounds
            size=self._text_handler.get_size('aqi_value'),
            data={'type': 'text', 'category': 'aqi_value'}
        )
        
        aqi_row = ft.Row([
            aqi_title_control,
            ft.Container(
                content=aqi_value_control,
                bgcolor=self._get_aqi_color(aqi),
                border_radius=10, padding=10, alignment=ft.alignment.center, expand=True
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
        # Pollutant Details
        elements = TranslationService.get_chemical_elements(self._current_language)
        # Map API component keys to display names and values
        pollutant_details_map = {
            "co": {"name": elements.get("CO", "CO"), "value": components.get("co", 0)},
            "no": {"name": elements.get("NO", "NO"), "value": components.get("no", 0)},
            "no2": {"name": elements.get("NO2", "NO2"), "value": components.get("no2", 0)},
            "o3": {"name": elements.get("O3", "O3"), "value": components.get("o3", 0)},
            "so2": {"name": elements.get("SO2", "SO2"), "value": components.get("so2", 0)},
            "pm2_5": {"name": elements.get("PM2.5", "PM2.5"), "value": components.get("pm2_5", 0)},
            "pm10": {"name": elements.get("PM10", "PM10"), "value": components.get("pm10", 0)},
            "nh3": {"name": elements.get("NH3", "NH3"), "value": components.get("nh3", 0)},
        }

        column1_controls = []
        column2_controls = []
        
        # Ensure consistent order for display if relying on dict insertion order (Python 3.7+)
        # Or use a list of keys for defined order:
        ordered_keys = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

        mid_point = (len(ordered_keys) + 1) // 2

        for i, key in enumerate(ordered_keys):
            detail = pollutant_details_map.get(key)
            if not detail: 
                continue # Corrected: put continue on a new line

            value_str = f"{detail['value']:.2f} μg/m³"
            
            desc_text_control = ft.Text(
                detail['name'], 
                color=self._current_text_color,
                size=self._text_handler.get_size('label'),
                data={'type': 'text', 'category': 'label'}
            )
            
            symbol_text_control = ft.Text( # Displaying the chemical symbol/key
                f"{key.upper().replace('_', '.')}:", # Format key nicely e.g. PM2.5
                weight=ft.FontWeight.BOLD, 
                color=self._current_text_color,
                size=self._text_handler.get_size('value'),
                data={'type': 'text', 'category': 'value'}
            )
            
            value_text_control = ft.Text(
                value_str, 
                color=self._current_text_color,
                size=self._text_handler.get_size('value'),
                data={'type': 'text', 'category': 'value'}
            )

            pollutant_item_column = ft.Column(
                controls=[
                    desc_text_control,
                    ft.Row([symbol_text_control, value_text_control], spacing=5)
                ],
                spacing=2,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            )
            item_container = ft.Container(
                content=pollutant_item_column,
                padding=ft.padding.symmetric(vertical=5)
            )
            
            if i < mid_point:
                column1_controls.append(item_container)
            else:
                column2_controls.append(item_container)
        
        pollutants_row = ft.Row(
            controls=[
                ft.Column(column1_controls, spacing=10, expand=True, alignment=ft.MainAxisAlignment.START),
                ft.Column(column2_controls, spacing=10, expand=True, alignment=ft.MainAxisAlignment.START)
            ],
            spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        
        divider_color = DARK_THEME.get("BORDER", ft.Colors.WHITE38) if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME.get("BORDER", ft.Colors.BLACK26)
        main_column = ft.Column(
            controls=[aqi_row, ft.Divider(height=1, color=divider_color), pollutants_row],
            spacing=15,
            expand=True
        )
        self._ui_elements_built = True
        return main_column

    def _request_ui_rebuild(self, event_data=None):
        """Updates state, rebuilds UI, and updates the control."""
        if not self.page or not self.visible: 
            return # Corrected: put return on a new line

        if self._state_manager:
            self._current_language = self._state_manager.get_state('language') or self._current_language
        
        self._current_text_color = self._determine_text_color_from_theme()
        
        new_content = self._build_ui_elements()
        if self.content != new_content: # Avoid unnecessary updates if content is identical
            self.content = new_content
        
        # If UI wasn't built properly (e.g. no data), _update_text_sizes might not be effective
        # or try to operate on placeholder. Ensure it's called after content is set.
        if self._ui_elements_built:
             self._update_text_sizes() # Update sizes after rebuilding content

        self.update()

    def _handle_language_change(self, event_data=None):
        """Handles language changes: updates text and rebuilds UI."""
        # Pollution data itself doesn't change with language, only labels
        self._request_ui_rebuild()

    def _handle_theme_change(self, event_data=None):
        """Handles theme changes: updates colors and rebuilds UI."""
        self._current_text_color = self._determine_text_color_from_theme()
        self._request_ui_rebuild()

    def _update_text_sizes(self): # Renamed from _update_text_and_icon_sizes
        """Updates sizes of all registered text elements based on ResponsiveTextHandler."""
        if not self._ui_elements_built or not isinstance(self.content, ft.Column):
            return

        # Helper to recursively find Text controls with 'data'
        def _apply_to_text_controls(control_tree_node):
            if isinstance(control_tree_node, ft.Text) and hasattr(control_tree_node, 'data') and isinstance(control_tree_node.data, dict):
                category = control_tree_node.data.get('category')
                if category:
                    new_size = self._text_handler.get_size(category)
                    control_tree_node.size = new_size
                    # Update color too, respecting AQI value's special background logic
                    if category == 'aqi_value':
                         # CHANGED: Access 'aqi' directly from self._pollution_data
                         aqi_val_for_color = self._pollution_data.get("aqi", 0)
                         control_tree_node.color = "#ffffff" if aqi_val_for_color > 2 else self._current_text_color
                    else:
                         control_tree_node.color = self._current_text_color
            
            if hasattr(control_tree_node, 'controls') and control_tree_node.controls:
                for child_control in control_tree_node.controls:
                    _apply_to_text_controls(child_control)
            elif hasattr(control_tree_node, 'content') and control_tree_node.content:
                _apply_to_text_controls(control_tree_node.content)

        _apply_to_text_controls(self.content)
        # self.update() # Update is called by _request_ui_rebuild

    def _combined_resize_handler(self, e):
        """Handles page resize events for this component."""
        if hasattr(self, '_original_on_resize') and self._original_on_resize:
            self._original_on_resize(e) 

        self._text_handler._handle_resize(e) 
        if self._ui_elements_built: # Only update sizes if UI is built
            self._update_text_sizes()
            if self.page: 
                self.update() # Corrected: put self.update() on a new line

    def _get_aqi_description(self, aqi_value: int) -> str:
        """Get localized description based on Air Quality Index"""
        lang_code = TranslationService.normalize_lang_code(self._current_language)
        # Fallback to English if specific language or key is missing
        aqi_translations = TranslationService.TRANSLATIONS.get(lang_code, TranslationService.TRANSLATIONS.get("en", {}))
        aqi_descriptions = aqi_translations.get("aqi_descriptions", 
            TranslationService.TRANSLATIONS.get("en", {}).get("aqi_descriptions", ["N/A"] * 6) # Default to English or N/A
        )
        idx = min(aqi_value, 5) # AQI is 1-5, description list is 0-indexed for value 0, then 1-5
        if idx == 0: # API AQI is 1-based, descriptions might be 0-indexed if "N/A" or similar is at index 0
            # Assuming aqi_descriptions[0] is for an invalid/unknown state, and aqi_descriptions[1] for AQI 1 (Good)
            # If API returns AQI 1, we need aqi_descriptions[1].
            # Let's adjust: if aqi_value is 1, use index 1. If aqi_value is 0 (error/default), use index 0.
             actual_idx = aqi_value # if aqi_value is 0, use index 0. if 1, use 1.
        else:
             actual_idx = aqi_value # API AQI is 1-5. List index should be aqi_value.
                                    # Example: AQI 1 -> index 1 ("Good")

        if actual_idx < len(aqi_descriptions):
            return aqi_descriptions[actual_idx]
        return aqi_descriptions[0] if aqi_descriptions else "N/A" # Fallback
    
    def _get_aqi_color(self, aqi_value: int) -> str:
        """Get color based on Air Quality Index"""
        colors = [
            "#D3D3D3",  # Light Gray for index 0 (e.g. N/A or before "Good")
            "#00E400",  # Green for Good (AQI 1)
            "#FFFF00",  # Yellow for Fair (AQI 2)
            "#FF7E00",  # Orange for Moderate (AQI 3)
            "#FF0000",  # Red for Poor (AQI 4)
            "#99004C"   # Purple for Very Poor (AQI 5)
        ]
        # Ensure aqi_value is within the bounds of the colors list (0-5)
        idx = max(0, min(aqi_value, len(colors) - 1))
        return colors[idx]

    def update_location(self, lat: float, lon: float):
        """Allows updating the location and refreshing the air pollution data."""
        if self._lat != lat or self._lon != lon:
            self._lat = lat
            self._lon = lon
            if self.page:
                self.page.run_task(self._fetch_data_and_request_rebuild)
            else:
                # Fallback or log if page context not available for task
                print(f"[AirPollutionDisplay] Page context not available for task on location update to ({lat}, {lon})")


