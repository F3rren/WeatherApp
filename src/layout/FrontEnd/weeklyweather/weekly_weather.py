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
    Displays the weekly weather forecast.
    Fetches data and renders daily forecast items internally.
    """

    def __init__(self, page: ft.Page, city: str, **kwargs):
        super().__init__(**kwargs)
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
            base_sizes={'day_label': 18, 'temp_value': 16, 'weather_icon': 50, 'divider_height': 1},
            breakpoints=[600, 900, 1200, 1600]
        )

        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._state_manager.register_observer("language_event", lambda e=None: self.page.run_task(self.update_ui, e))
            self._state_manager.register_observer("unit_event", lambda e=None: self.page.run_task(self.update_ui, e))
            self._state_manager.register_observer("theme_event", lambda e=None: self.page.run_task(self.update_ui, e))

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

            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._current_text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            if self.page:
                self.update()
        except Exception as e:
            logging.error(f"WeeklyForecastDisplay: Error updating UI: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs the UI for the weekly forecast as a ft.Column of daily items."""
        if not self._forecast_data:
            no_data_text = TranslationService.translate_from_dict("weekly_forecast_items", "no_forecast_data", self._current_language)
            return ft.Column([
                ft.Text(
                    no_data_text,
                    color=self._current_text_color
                )
            ])

        daily_item_controls = []
        text_size = self._text_handler.get_size('day_label')
        icon_size = self._text_handler.get_size('weather_icon')
        temp_text_size = self._text_handler.get_size('temp_value')
        divider_color = DARK_THEME.get("BORDER", ft.Colors.WHITE38) if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME.get("BORDER", ft.Colors.BLACK26)

        for i, day_data in enumerate(self._forecast_data):
            try:
                translated_day = TranslationService.translate_from_dict("weekly_forecast_items", day_data["day_key"], self._current_language)
                day_text_control = ft.Text(
                    translated_day,
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color,
                    size=text_size
                )
                
                unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
                temp_min_str = f"{day_data['temp_min']}{unit_symbol}"
                temp_max_str = f"{day_data['temp_max']}{unit_symbol}"

                temperature_text_control = ft.Text(
                    spans=[
                        ft.TextSpan(temp_min_str, ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_ACCENT_200, size=temp_text_size)),
                        ft.TextSpan(" / ", ft.TextStyle(color=self._current_text_color, size=temp_text_size)),
                        ft.TextSpan(temp_max_str, ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.RED_ACCENT_200, size=temp_text_size))
                    ]
                )
                
                weather_icon_control = ft.Image(
                    src=f"https://openweathermap.org/img/wn/{day_data['icon']}@2x.png",
                    width=icon_size,
                    height=icon_size,
                    fit=ft.ImageFit.CONTAIN
                )

                daily_row = ft.Row(
                    controls=[
                        ft.Container(content=day_text_control, alignment=ft.alignment.center_left, expand=1),
                        ft.Container(content=weather_icon_control, alignment=ft.alignment.center, expand=0),
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
                logging.error(f"[ERROR WeeklyForecastDisplay] Failed to build item for {day_data.get('day_key', 'Unknown Day')}: {e}\nTraceback: {traceback.format_exc()}")
                daily_item_controls.append(ft.Text("Error loading item.", color=ft.Colors.RED))
        
        return ft.Column(
            controls=daily_item_controls,
            spacing=5,
        )
