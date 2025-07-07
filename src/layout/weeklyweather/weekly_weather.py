import flet as ft
import traceback
import asyncio
import logging
from services.api_service import ApiService
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM, LIGHT_THEME, DARK_THEME

class WeeklyForecastDisplay(ft.Container):
    """
    Displays the weekly weather forecast with modern UI design.
    Fetches data and renders daily forecast items internally.
    """

    def __init__(self, page: ft.Page, city: str, **kwargs):
        super().__init__()
        self.page = page
        self._city = city
        self._api_service = ApiService()
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_unit_system = DEFAULT_UNIT_SYSTEM
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._forecast_data = []

        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'header_title': 18,
                'day_label': 16,
                'temp_value': 15,
                'weather_icon': 40,
                'loading_text': 14
            },
            breakpoints=[600, 900, 1200, 1600]
        )

        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(0)  # Remove default padding, handled by internal containers
        
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._state_manager.register_observer("language_event", self._safe_language_update)
            self._state_manager.register_observer("unit", self._safe_unit_update)
            self._state_manager.register_observer("theme_event", self._safe_theme_update)

        if self.page:
            original_on_resize = self.page.on_resize
            def resize_handler(e):
                if original_on_resize:
                    original_on_resize(e)
                if self._text_handler:
                    self._text_handler._handle_resize(e)
                if self.page:
                    self.page.run_task(self.update_ui)
            self.page.on_resize = resize_handler
        
        self.content = self.build()
        if self.page:
            self.page.run_task(self.update_ui)

    async def update_ui(self, event_data=None):
        """Updates the UI based on state changes, fetching new data if necessary."""
        if not self.page or not self.visible:
            return

        try:
            data_changed = False
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                new_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
                
                lang_changed = self._current_language != new_language
                unit_changed = self._current_unit_system != new_unit_system

                self._current_language = new_language
                self._current_unit_system = new_unit_system
                
                data_changed = lang_changed or unit_changed

            if not self._forecast_data or data_changed:
                if self._city:
                    weather_data_payload = await asyncio.to_thread(
                        self._api_service.get_weather_data,
                        city=self._city, 
                        language=self._current_language, 
                        unit=self._current_unit_system
                    )
                    self._forecast_data = self._api_service.get_weekly_forecast_data(weather_data_payload) if weather_data_payload else []
                else:
                    self._forecast_data = []

            # Safe theme detection with robust checking
            is_dark = False
            if self.page and hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._current_text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            # Only update if this control is already in the page - use try/catch for safety
            if self.page:
                try:
                    self.update()
                except (AssertionError, AttributeError) as update_error:
                    # Control not yet added to page, skip update
                    logging.debug(f"WeeklyForecastDisplay: Skipping update - control not in page yet: {update_error}")
        except Exception as e:
            logging.error(f"WeeklyForecastDisplay: Error updating UI: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs the modern UI for the weekly forecast with header and styled cards."""
        # Safe theme detection with robust checking
        is_dark = False
        if self.page and hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME
        
        # Header section
        header_text = TranslationService.translate_from_dict("weekly_forecast_items", "header", self._current_language)
        header = ft.Row(
            controls=[
                ft.Icon(
                    name=ft.Icons.CALENDAR_MONTH,
                    size=24,  # Dimensione fissa come gli altri componenti
                    color=ft.Colors.BLUE_400 if not is_dark else ft.Colors.BLUE_300
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    header_text,
                    size=self._text_handler.get_size('axis_title') + 2,
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )
        

        
        if not self._forecast_data:
            loading_text = TranslationService.translate_from_dict("weekly_forecast_items", "loading", self._current_language)
            return ft.Column([
                ft.Container(
                    content=header,
                    padding=ft.padding.only(left=20, right=20, top=20, bottom=10)
                ),
                ft.Container(
                    content=ft.Text(
                        loading_text,
                        color=self._current_text_color,
                        size=self._text_handler.get_size('loading_text')
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20)
                )
            ])

        daily_cards = []
        
        for i, day_data in enumerate(self._forecast_data):
            try:
                card = self._build_daily_card(day_data, theme)
                daily_cards.append(card)
                
                # Add divider between days (except for the last one)
                if i < len(self._forecast_data) - 1:
                    divider_color = "#404040" if is_dark else "#e0e0e0"  # Use previously calculated is_dark
                    divider = ft.Container(
                        content=ft.Divider(
                            height=1,
                            thickness=1,
                            color=theme.get("BORDER", divider_color)
                        ),
                        padding=ft.padding.symmetric(horizontal=20)
                    )
                    daily_cards.append(divider)
                    
            except Exception as e:
                logging.error(f"[ERROR WeeklyForecastDisplay] Failed to build card for {day_data.get('day_key', 'Unknown Day')}: {e}\nTraceback: {traceback.format_exc()}")
                # Add error placeholder card
                error_card = ft.Container(
                    content=ft.Text("Error loading day", color=ft.Colors.RED, size=12),
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center
                )
                daily_cards.append(error_card)
        
        return ft.Column([
            # Header container
            ft.Container(
                content=header,
                padding=ft.padding.only(left=20, right=20, top=20, bottom=15)
            ),
            # Cards container - simplified, no extra padding
            ft.Column(
                controls=daily_cards,
                spacing=0,
                tight=True
            )
        ], spacing=0)

    def _build_daily_card(self, day_data, theme):
        """Builds a clean styled row for a single day forecast with additional weather information."""
        translated_day = TranslationService.translate_from_dict("weekly_forecast_items", day_data["day_key"], self._current_language)
        
        # Temperature data
        unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
        temp_min_str = f"{day_data['temp_min']}{unit_symbol}"
        temp_max_str = f"{day_data['temp_max']}{unit_symbol}"
        
        # Weather icon - simplified without background
        weather_icon = ft.Image(
            src=f"https://openweathermap.org/img/wn/{day_data['icon']}@2x.png",
            width=self._text_handler.get_size('weather_icon'),
            height=self._text_handler.get_size('weather_icon'),
            fit=ft.ImageFit.CONTAIN
        )
        
        # Day label
        day_label = ft.Text(
            translated_day,
            size=self._text_handler.get_size('day_label'),
            weight=ft.FontWeight.W_600,
            color=self._current_text_color
        )
        
        # Temperature spans
        temperature_text = ft.Text(
            spans=[
                ft.TextSpan(
                    temp_min_str, 
                    ft.TextStyle(
                        weight=ft.FontWeight.W_600, 
                        color=ft.Colors.BLUE_400,
                        size=self._text_handler.get_size('temp_value')
                    )
                ),
                ft.TextSpan(
                    "\n", 
                    ft.TextStyle(
                        color=self._current_text_color, 
                        size=self._text_handler.get_size('temp_value')
                    )
                ),
                ft.TextSpan(
                    temp_max_str, 
                    ft.TextStyle(
                        weight=ft.FontWeight.W_600, 
                        color=ft.Colors.RED_400,
                        size=self._text_handler.get_size('temp_value')
                    )
                )
            ]
        )
        
        # Additional weather information in a compact row
        additional_info_widgets = []
        
        # Rain probability (only if > 0)
        if day_data.get('rain_probability', 0) > 0:
            additional_info_widgets.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.WATER_DROP, size=12, color=ft.Colors.BLUE_400),
                        ft.Text(f"{day_data['rain_probability']}%", size=11, color=ft.Colors.BLUE_400, weight="w500")
                    ], spacing=2),
                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_400),
                )
            )
        
        # Humidity
        additional_info_widgets.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.OPACITY, size=12, color=ft.Colors.CYAN_400),
                    ft.Text(f"{day_data.get('humidity', 0)}%", size=11, color=ft.Colors.CYAN_400, weight="w500")
                ], spacing=2),
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.CYAN_400),
            )
        )
        
        # Wind speed
        wind_unit = "m/s" if self._current_unit_system == "metric" else "mph"
        additional_info_widgets.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.AIR, size=12, color=ft.Colors.GREEN_400),
                    ft.Text(f"{day_data.get('wind_speed', 0)}{wind_unit}", size=11, color=ft.Colors.GREEN_400, weight="w500")
                ], spacing=2),
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400),
            )
        )
        
        # Additional info row
        additional_info_row = ft.Row(
            controls=additional_info_widgets,
            spacing=4,
            alignment=ft.MainAxisAlignment.START
        )
        
        # Main content structure
        main_row = ft.Row(
            controls=[
                # Day name (left)
                ft.Container(
                    content=day_label,
                    alignment=ft.alignment.center_left,
                    expand=2
                ),
                # Weather icon (center)
                ft.Container(
                    content=weather_icon,
                    alignment=ft.alignment.center,
                    expand=1
                ),
                # Temperature (right)
                ft.Container(
                    content=temperature_text,
                    alignment=ft.alignment.center_right,
                    expand=2
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
        
        # Clean card with main info and additional details
        card = ft.Container(
            content=ft.Column([
                main_row,
                ft.Container(height=6),  # Spacer
                ft.Container(
                    content=additional_info_row,
                    padding=ft.padding.only(left=20)  # Align with content above
                )
            ], spacing=0),
            padding=ft.padding.symmetric(horizontal=20, vertical=16),
            border_radius=0,  # Remove border radius for cleaner look
            # No background color - inherit from parent
        )
        
        return card

    def update_city(self, new_city: str):
        """Updates the city and triggers a UI refresh."""
        if self._city != new_city:
            self._city = new_city
            self._forecast_data = []  # Clear cached data
            if self.page:
                self.page.run_task(self.update_ui)

    def _safe_language_update(self, e=None):
        """Safely handle language change event."""
        if self.page and hasattr(self.page, 'run_task'):
            self.page.run_task(self.update_ui, e)
    
    def _safe_unit_update(self, e=None):
        """Safely handle unit change event."""
        if self.page and hasattr(self.page, 'run_task'):
            self.page.run_task(self.update_ui, e)
    
    def _safe_theme_update(self, e=None):
        """Safely handle theme change event."""
        if self.page and hasattr(self.page, 'run_task'):
            self.page.run_task(self.update_ui, e)
