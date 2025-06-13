import flet as ft
import traceback
import logging
from services.api_service import ApiService
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM, LIGHT_THEME, DARK_THEME

class WeeklyForecastDisplay(ft.Container):
    """
    Displays the weekly weather forecast.
    Fetches data and renders daily forecast items internally.
    """

    def __init__(self, page: ft.Page, city: str, **kwargs):
        super().__init__(**kwargs) # Ensure expand, padding etc. can be passed
        self.page = page
        self._city = city # Store city for data fetching
        
        self._api_service = ApiService() # Initialize ApiService
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_unit_system = DEFAULT_UNIT_SYSTEM
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._forecast_data = [] # To store fetched forecast data

        # ResponsiveTextHandler for elements within this component
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={'day_label': 18, 'temp_value': 16, 'weather_icon': 50, 'divider_height': 1},
            breakpoints=[600, 900, 1200, 1600]
        )
        self._ui_elements_built = False
        
        # Default container properties (can be overridden by kwargs)
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
        self.content = ft.Text("Loading weekly forecast...") # Initial placeholder

    def did_mount(self):
        """Called when the control is added to the page."""
        if self.page and self._text_handler and not self._text_handler.page:
            self._text_handler.page = self.page
        
        self._initialize_state_and_observers()
        # Fetch data and build UI
        # Run as a task to avoid blocking UI thread during initial data fetch
        if self.page:
            self.page.run_task(self._fetch_data_and_request_rebuild)

    async def _fetch_data_and_request_rebuild(self):
        """Fetches data and then requests a UI rebuild."""
        await self._fetch_forecast_data()
        self._request_ui_rebuild()

    def _initialize_state_and_observers(self):
        """Initializes state manager and registers observers."""
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._current_language = self._state_manager.get_state('language') or self._current_language
            self._current_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
            
            self._state_manager.register_observer("language_event", self._handle_language_or_unit_change)
            self._state_manager.register_observer("unit_event", self._handle_language_or_unit_change) # Corrected key from 'unit' to 'unit_event' if consistent
            self._state_manager.register_observer("theme_event", self._handle_theme_change)
        
        if self.page: # ResponsiveTextHandler's observer is managed by its own on_resize binding
            self._original_on_resize = self.page.on_resize
            self.page.on_resize = self._combined_resize_handler

    def will_unmount(self):
        """Called when the control is removed from the page."""
        if self._state_manager:
            self._state_manager.unregister_observer("language_event", self._handle_language_or_unit_change)
            self._state_manager.unregister_observer("unit_event", self._handle_language_or_unit_change)
            self._state_manager.unregister_observer("theme_event", self._handle_theme_change)
        
        if self.page and hasattr(self, '_original_on_resize'):
            self.page.on_resize = self._original_on_resize

    def _determine_text_color_from_theme(self):
        """Determines text color based on the current page theme."""
        if self.page and self.page.theme_mode:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config.get("TEXT", ft.Colors.BLACK)
        return LIGHT_THEME.get("TEXT", ft.Colors.BLACK)

    async def _fetch_forecast_data(self):
        """Fetches weekly forecast data using ApiService."""
        if not self._city:
            self._forecast_data = []
            return

        # ApiService needs language and unit for the get_weather_data call
        # These are now maintained by this class (_current_language, _current_unit_system)
        weather_data_payload = self._api_service.get_weather_data(
            city=self._city, 
            language=self._current_language, 
            unit=self._current_unit_system
        )
        self._forecast_data = self._api_service.get_weekly_forecast_data(weather_data_payload) if weather_data_payload else []

    def _build_ui_elements(self):
        """Constructs the UI for the weekly forecast as a ft.Column of daily items."""
        if not self._forecast_data:
            return ft.Text(
                TranslationService.get_text("no_forecast_data", self._current_language), 
                color=self._current_text_color
            )

        daily_item_controls = []
        text_size = self._text_handler.get_size('day_label')
        icon_size = self._text_handler.get_size('weather_icon')
        temp_text_size = self._text_handler.get_size('temp_value')
        divider_color = DARK_THEME.get("BORDER", ft.Colors.WHITE38) if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME.get("BORDER", ft.Colors.BLACK26)


        for i, day_data in enumerate(self._forecast_data):
            try:
                translated_day = TranslationService.translate_weekday(day_data["day_key"], self._current_language)
                day_text_control = ft.Text(
                    translated_day,
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color,
                    size=text_size,
                    data={'type': 'text', 'category': 'day_label'}
                )
                
                unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
                temp_min_str = f"{day_data['temp_min']}{unit_symbol}"
                temp_max_str = f"{day_data['temp_max']}{unit_symbol}"

                temperature_text_control = ft.Text(
                    spans=[
                        ft.TextSpan(temp_min_str, ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_ACCENT_200, size=temp_text_size)),
                        ft.TextSpan(" / ", ft.TextStyle(color=self._current_text_color, size=temp_text_size)),
                        ft.TextSpan(temp_max_str, ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.RED_ACCENT_200, size=temp_text_size))
                    ],
                    data={'type': 'text_spans', 'category': 'temp_value'} # Special handling for spans if needed
                )
                
                weather_icon_control = ft.Image(
                    src=f"https://openweathermap.org/img/wn/{day_data['icon']}@2x.png", # Using @2x for better resolution
                    width=icon_size,
                    height=icon_size,
                    fit=ft.ImageFit.CONTAIN,
                    data={'type': 'icon', 'category': 'weather_icon'}
                )

                daily_row = ft.Row(
                    controls=[
                        ft.Container(content=day_text_control, alignment=ft.alignment.center_left, expand=1),
                        ft.Container(content=weather_icon_control, alignment=ft.alignment.center, expand=0), # Icon takes its own space
                        ft.Container(content=temperature_text_control, alignment=ft.alignment.center_right, expand=1)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                )
                daily_item_controls.append(daily_row)

                if i < len(self._forecast_data) - 1:
                    daily_item_controls.append(
                        ft.Divider(height=self._text_handler.get_size('divider_height'), color=divider_color)
                    )
            except Exception as e:
                print(f"[ERROR WeeklyForecastDisplay] Failed to build item for {day_data.get('day_key', 'Unknown Day')}: {e}\\nTraceback: {traceback.format_exc()}")
                daily_item_controls.append(ft.Text("Error loading item.", color=ft.Colors.RED))
        
        self._ui_elements_built = True
        return ft.Column(
            controls=daily_item_controls,
            spacing=5, # Spacing between rows/dividers
            # expand=True # The column itself can expand within the container
        )

    def _request_ui_rebuild(self, event_data=None):
        """Updates state, rebuilds UI, and updates the control."""
        if not self.page or not self.visible:
            return

        if self._state_manager:
            self._current_language = self._state_manager.get_state('language') or self._current_language
            self._current_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
        
        self._current_text_color = self._determine_text_color_from_theme()
        
        # If language or unit changed, we might need to re-fetch data
        # For simplicity in this step, _fetch_forecast_data is called before _build_ui_elements
        # A more optimized way would be to check if the event_data indicates a change that requires data refetch.
        # For now, let's assume _handle_language_or_unit_change will call _fetch_data_and_request_rebuild.

        new_content = self._build_ui_elements()
        if self.content != new_content:
            self.content = new_content
        self.update()

    async def _handle_language_or_unit_change(self, event_data=None):
        """Handles language or unit changes: re-fetches data and rebuilds UI."""
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_language_or_unit_change received unexpected event_data type: {type(event_data)}")
        
        # Update state from manager
        if self._state_manager:
            lang_changed = self._current_language != (self._state_manager.get_state('language') or self._current_language)
            unit_changed = self._current_unit_system != (self._state_manager.get_state('unit') or self._current_unit_system)

            if lang_changed:
                 self._current_language = self._state_manager.get_state('language') or self._current_language
            if unit_changed:
                 self._current_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
            
            if lang_changed or unit_changed:
                await self._fetch_forecast_data() # Re-fetch data with new lang/unit
        
        self._request_ui_rebuild() # Rebuild UI with potentially new data and translations

    def _handle_theme_change(self, event_data=None):
        """Handles theme changes: updates colors and rebuilds UI."""
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_theme_change received unexpected event_data type: {type(event_data)}")
        self._current_text_color = self._determine_text_color_from_theme()
        self._request_ui_rebuild() # Rebuild UI with new colors

    def _update_text_and_icon_sizes(self):
        """Updates sizes of all registered text and icon elements."""
        if not self._ui_elements_built or not isinstance(self.content, ft.Column):
            return

        # The content is a Column of Rows and Dividers
        for control in self.content.controls:
            if isinstance(control, ft.Row): # This is a daily_row
                for item_container in control.controls: # These are the containers for day, icon, temp
                    if isinstance(item_container, ft.Container) and item_container.content:
                        element = item_container.content
                        if hasattr(element, 'data') and isinstance(element.data, dict):
                            category = element.data.get('category')
                            el_type = element.data.get('type')
                            if category:
                                new_size = self._text_handler.get_size(category)
                                if el_type == 'icon' and hasattr(element, 'width') and hasattr(element, 'height'):
                                    element.width = new_size
                                    element.height = new_size
                                elif el_type == 'text' and hasattr(element, 'size'):
                                    element.size = new_size
                                elif el_type == 'text_spans' and hasattr(element, 'spans'):
                                    for span in element.spans:
                                        if hasattr(span, 'style') and span.style:
                                            span.style.size = new_size
                                        else:
                                            span.style = ft.TextStyle(size=new_size)
            elif isinstance(control, ft.Divider):
                 control.height = self._text_handler.get_size('divider_height')
        
        if self.page:
            self.update() # Corrected: self.update() on a new line

    def _combined_resize_handler(self, e):
        """Handles page resize events for this component."""
        if hasattr(self, '_original_on_resize') and self._original_on_resize:
            self._original_on_resize(e) # Call previously registered handler first

        self._text_handler._handle_resize(e) # Update ResponsiveTextHandler
        self._update_text_and_icon_sizes()   # Update elements within this component

    def update_city(self, new_city: str):
        """Allows updating the city and refreshing the forecast."""
        if self._city != new_city:
            self._city = new_city
            # Re-fetch data and rebuild
            if self.page:
                self.page.run_task(self._fetch_data_and_request_rebuild)
            else: # Fallback if page context not available for task
                # This might happen if called before did_mount or in a non-Flet context
                # Consider logging or alternative handling
                print(f"[WeeklyForecastDisplay] Page context not available for task on city update to {new_city}")

    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati"""
        for control, size_category in self.text_controls.items():
            if hasattr(control, 'size'):
                control.size = self.text_handler.get_size(size_category)
            if hasattr(control, 'spans'):
                for span in control.spans:
                    if hasattr(span, 'style') and hasattr(span.style, 'size'):
                        span.style.size = self.text_handler.get_size(size_category)
