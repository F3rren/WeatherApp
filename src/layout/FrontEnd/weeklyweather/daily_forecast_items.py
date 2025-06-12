import flet as ft
from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME, DEFAULT_UNIT_SYSTEM # Added DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler

class DailyForecastItems:
    """
    An item displaying daily forecast information.
    """
    
    def __init__(self, day: str, icon_code: str, temp_min: int, temp_max: int, text_color: str, page: ft.Page = None):
        self.day = day
        self.icon_code = icon_code
        self.temp_min = temp_min
        self.temp_max = temp_max
        # self.text_color is initialized by WeatherView based on current theme
        self.initial_text_color = text_color 
        self.page = page
        self._state_manager = None

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'label': 30,
                'icon': 100,
                'value': 18,
            },
            breakpoints=[600, 900, 1200, 1600]
        )        

        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self.unit_system = self._state_manager.get_state('unit_system') or DEFAULT_UNIT_SYSTEM
            self.text_color = self._determine_text_color()

            self._state_manager.register_observer("theme_event", self._handle_state_change)
            self._state_manager.register_observer("unit_event", self._handle_state_change)   # Added
            
            original_resize_handler = self.page.on_resize
            
            def combined_resize_handler(e):
                self.text_handler._handle_resize(e)
                self._update_all_item_visuals() # Update visuals on resize
                if original_resize_handler:
                    original_resize_handler(e)
            self.page.on_resize = combined_resize_handler
        else:
            self.unit_system = DEFAULT_UNIT_SYSTEM
            self.text_color = self.initial_text_color

        # Create Text controls (will be updated by _update_text_elements)
        self.day_text = ft.Text(size=self.text_handler.get_size('value'))
        
        self.temp_span_min = ft.TextSpan(
            style=ft.TextStyle(
                size=self.text_handler.get_size('value'),
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE, 
            )
        )
        self.temp_span_separator = ft.TextSpan(
            " ",
            ft.TextStyle(
                size=self.text_handler.get_size('value'),
                weight=ft.FontWeight.BOLD,
            )
        )
        self.temp_span_max = ft.TextSpan(
            style=ft.TextStyle(
                size=self.text_handler.get_size('value'),
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED,
            )
        )
        self.temperature_text = ft.Text(
            spans=[
                self.temp_span_min,
                self.temp_span_separator,
                self.temp_span_max,
            ],
            expand=True,
        )
        
        self._update_text_elements() # Initial population of text and styles

    def _determine_text_color(self):
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config["TEXT"]
        return self.initial_text_color

    def _update_text_elements(self):
        """Updates all text content, styles, and units."""
        # Update language and unit system from state manager, just in case
        if self._state_manager:
            self.language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
            self.unit_system = self._state_manager.get_state('unit') or DEFAULT_UNIT_SYSTEM
        self.text_color = self._determine_text_color()

        # Translate day
        self.day_text.value = TranslationService.translate_weekday(self.day, self.language)
        self.day_text.color = self.text_color


        # Update temperature with units
        unit_symbol = TranslationService.get_unit_symbol("temperature", self.unit_system)
        self.temp_span_min.text = f"{self.temp_min}{unit_symbol}"
        self.temp_span_max.text = f"{self.temp_max}{unit_symbol}"
        
        # Update separator color
        self.temp_span_separator.style.color = self.text_color

        # Update sizes (in case of resize before this update)
        self.day_text.size = self.text_handler.get_size('value')
        self.temp_span_min.style.size = self.text_handler.get_size('value')
        self.temp_span_separator.style.size = self.text_handler.get_size('value')
        self.temp_span_max.style.size = self.text_handler.get_size('value')
        
        if hasattr(self.day_text, 'page') and self.day_text.page:
            self.day_text.update()
        if hasattr(self.temperature_text, 'page') and self.temperature_text.page:
            self.temperature_text.update()

    def _handle_state_change(self, event_data=None):
        """Handles language, unit, or theme change events."""
        self._update_text_elements()

    def build(self) -> ft.Container:
        # ... existing build method ...
        # Ensure day_text and temperature_text are used from self
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=self.day_text,
                        alignment=ft.alignment.center_left
                    ),
                    ft.Container(
                        content=ft.Image(
                            src=f"https://openweathermap.org/img/wn/{self.icon_code}@4x.png",
                            width=self.text_handler.get_size('icon'), 
                            height=self.text_handler.get_size('icon'),
                        ),
                        width=100,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=self.temperature_text,
                        alignment=ft.alignment.center_right
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            padding=ft.padding.only(left=10, right=10)
        )