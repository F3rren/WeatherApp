import flet as ft
import logging # Added import for logging
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
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._pollution_data = {} 
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
        """Fetches air pollution data using ApiService (async)."""
        if self._lat is None or self._lon is None:
            self._pollution_data = {}
            return
        self._pollution_data = await self._api_service.get_air_pollution_async(self._lat, self._lon) or {}

    def _build_ui_elements(self):
        """Constructs the UI for air pollution data."""
        # CHANGED: Check for 'aqi' key in the processed data
        if not self._pollution_data or "aqi" not in self._pollution_data:
            return ft.Text(
                TranslationService.translate_from_dict("air_pollution_items", "no_air_pollution_data", self._current_language),
                color=self._current_text_color,
                size=self._text_handler.get_size('label')
            )

        # CHANGED: Directly access 'aqi' and 'components' from the processed self._pollution_data
        aqi = self._pollution_data.get("aqi", 0) # Use .get for safety
        # Components are the other keys in self._pollution_data, excluding 'aqi'
        components = {k: v for k, v in self._pollution_data.items() if k != "aqi"}


        # AQI Title and Value
        aqi_title_control = ft.Text(
            TranslationService.translate_from_dict("air_pollution_items", "air_quality_index", self._current_language),
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
        # Map API component keys to display names and values
        pollutant_details_map = {
            "co": {"name": TranslationService.translate_from_dict("air_pollution_items", "CO", self._current_language), "value": components.get("co", 0)},
            "no": {"name": TranslationService.translate_from_dict("air_pollution_items", "NO", self._current_language), "value": components.get("no", 0)},
            "no2": {"name": TranslationService.translate_from_dict("air_pollution_items", "NO2", self._current_language), "value": components.get("no2", 0)},
            "o3": {"name": TranslationService.translate_from_dict("air_pollution_items", "O3", self._current_language), "value": components.get("o3", 0)},
            "so2": {"name": TranslationService.translate_from_dict("air_pollution_items", "SO2", self._current_language), "value": components.get("so2", 0)},
            "pm2_5": {"name": TranslationService.translate_from_dict("air_pollution_items", "PM2.5", self._current_language), "value": components.get("pm2_5", 0)},
            "pm10": {"name": TranslationService.translate_from_dict("air_pollution_items", "PM10", self._current_language), "value": components.get("pm10", 0)},
            "nh3": {"name": TranslationService.translate_from_dict("air_pollution_items", "NH3", self._current_language), "value": components.get("nh3", 0)},
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

        # RIMOSSO: self.page.update() globale

    def _update_text_elements(self):
        """Updates only the text elements without rebuilding the entire UI"""
        if not self.content or not isinstance(self.content, ft.Column):
            return
        
        # Find and update title and category text
        for control in self.content.controls:
            if isinstance(control, ft.Text):
                if getattr(control, "data", {}).get("type") == "title":
                    control.value = TranslationService.translate_from_dict("air_pollution_items", "air_quality_index", self._language)
                    control.update()
            elif isinstance(control, ft.Row):
                # Update the category titles
                for child in control.controls:
                    if isinstance(child, ft.Column):
                        for text in child.controls:
                            if isinstance(text, ft.Text):
                                category = getattr(text, "data", {}).get("category")
                                if category and category.startswith("aqi_"):
                                    text.value = TranslationService.translate(category, self._current_language)
                                    text.update()
        
        self.update()

    def _handle_language_change(self, event_data=None):
        """Handles language changes: rebuilds UI if language changes."""
        if self._state_manager:
            new_language = self._state_manager.get_state('language') or self._current_language
            language_changed = self._current_language != new_language

            self._current_language = new_language
            # Rebuild UI if language changes
            if language_changed:
                self._request_ui_rebuild()

    def on_language_change(self, new_language_code):
        """Metodo chiamato dal parent observer per aggiornare la lingua e i testi."""
        self._current_language = new_language_code
        self._update_text_elements()  # Aggiorna i testi senza rifetch dei dati

    def _handle_theme_change(self, event_data=None):
        """Handles theme changes: updates colors and rebuilds UI."""
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_theme_change received unexpected event_data type: {type(event_data)}")
        self._current_text_color = self._determine_text_color_from_theme()
        if getattr(self, "page", None) and getattr(self, "visible", True):
            self._request_ui_rebuild()
            self._update_text_colors()

    def _safe_update(self):
        # Only update if the control is attached to the page and has a UID
        if getattr(self, "page", None) and getattr(self, "visible", True) and getattr(self, "_Control__uid", None):
            self.update()

    def _update_text_colors(self):
        """Recursively update color of all ft.Text elements in self.content to match current theme."""
        def _apply_color(control):
            if isinstance(control, ft.Text):
                category = getattr(control, 'data', {}).get('category') if hasattr(control, 'data') else None
                if category == 'aqi_value':
                    aqi_val_for_color = self._pollution_data.get("aqi", 0)
                    control.color = "#ffffff" if aqi_val_for_color > 2 else self._current_text_color
                else:
                    control.color = self._current_text_color
            if hasattr(control, 'controls') and control.controls:
                for child in control.controls:
                    _apply_color(child)
            elif hasattr(control, 'content') and control.content:
                _apply_color(control.content)
        if self.content:
            _apply_color(self.content)
        self._safe_update()

    def _update_text_sizes(self): # Renamed from _update_text_and_icon_sizes
        """Updates sizes of all registered text elements based on ResponsiveTextHandler and updates their color."""
        if not self._ui_elements_built or not isinstance(self.content, ft.Column):
            return
        def _apply_to_text_controls(control_tree_node):
            if isinstance(control_tree_node, ft.Text) and hasattr(control_tree_node, 'data') and isinstance(control_tree_node.data, dict):
                category = control_tree_node.data.get('category')
                if category:
                    new_size = self._text_handler.get_size(category)
                    control_tree_node.size = new_size
                    # Update color too, respecting AQI value's special background logic
                    if category == 'aqi_value':
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
        self._safe_update()

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
        """Get localized description based on Air Quality Index using only translations_data.py"""
        from utils.translations_data import TRANSLATIONS
        lang_code = TranslationService.normalize_lang_code(self._current_language)
        aqi_descriptions = TRANSLATIONS.get(lang_code, {}).get("air_pollution_items", {}).get("aqi_descriptions")
        if not aqi_descriptions:
            aqi_descriptions = TRANSLATIONS.get("en", {}).get("air_pollution_items", {}).get("aqi_descriptions", ["N/A"] * 6)
        idx = min(max(aqi_value, 0), 5)  # AQI is 1-5, fallback to 0 if out of range
        return aqi_descriptions[idx] if idx < len(aqi_descriptions) else "N/A"

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
    
    async def refresh(self):
        """Forza il fetch e la ricostruzione della UI, anche se la posizione non cambia."""
        if self.page:
            await self._fetch_data_and_request_rebuild()


