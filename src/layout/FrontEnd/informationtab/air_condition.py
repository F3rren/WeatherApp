import flet as ft
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
from services.api_service import ApiService
import asyncio
import logging
import traceback

class AirConditionInfo(ft.Container):
    """
    Air condition information display.
    """

    def __init__(self, city: str, feels_like: int, humidity: int, wind_speed: int,
                 pressure: int, page: ft.Page = None, **kwargs):
        super().__init__(**kwargs)
        self._city = city
        self._feels_like_data = feels_like
        self._humidity_data = humidity
        self._wind_speed_data = wind_speed
        self._pressure_data = pressure
        self.page = page
        
        self._state_manager = None
        self._language = DEFAULT_LANGUAGE
        self._unit_system = DEFAULT_UNIT_SYSTEM
        self._text_color = LIGHT_THEME["TEXT"]
        self.padding = 20
        self._api_service = ApiService()

        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 24, 'label': 16, 'value': 16, 'icon': 20,
            },
            breakpoints=[600, 900, 1200, 1600]
        )

        if self.page:
            if hasattr(self.page, 'session') and self.page.session.get('state_manager'):
                self._state_manager = self.page.session.get('state_manager')
                self._state_manager.register_observer("language_event", lambda e=None: self.page.run_task(self.update_ui, e))
                self._state_manager.register_observer("unit_event", lambda e=None: self.page.run_task(self.update_ui, e))
                self._state_manager.register_observer("theme_event", lambda e=None: self.page.run_task(self.update_ui, e))

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
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._language
                new_unit_system = self._state_manager.get_state('unit') or self._unit_system
                
                language_changed = self._language != new_language
                unit_changed = self._unit_system != new_unit_system

                self._language = new_language
                self._unit_system = new_unit_system

                if language_changed or unit_changed:
                    weather_data = await asyncio.to_thread(
                        self._api_service.get_weather_data,
                        city=self._city, language=self._language, unit=self._unit_system
                    )
                    if weather_data:
                        self._feels_like_data = self._api_service.get_feels_like_temperature(weather_data)
                        self._humidity_data = self._api_service.get_humidity(weather_data)
                        self._wind_speed_data = self._api_service.get_wind_speed(weather_data)
                        self._pressure_data = self._api_service.get_pressure(weather_data)

            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            self.update()
        except Exception as e:
            logging.error(f"AirConditionInfo: Error updating UI: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs the UI elements for the air condition information."""
        title_text = ft.Text(
            value=TranslationService.translate_from_dict("air_condition_items", "air_condition_title", self._language),
            size=self._text_handler.get_size('title'),
            weight="bold",
            color=self._text_color
        )

        divider = ft.Divider(height=1, color=self._text_color)

        def create_info_column(items):
            controls = []
            for item in items:
                icon = ft.Icon(item["icon"], size=self._text_handler.get_size('icon'), color=self._text_color)
                label = ft.Text(
                    value=TranslationService.translate_from_dict("air_condition_items", item["label"], self._language),
                    size=self._text_handler.get_size('label'),
                    weight=ft.FontWeight.BOLD,
                    color=self._text_color
                )
                value = ft.Text(
                    value=item["value"],
                    size=self._text_handler.get_size('value'),
                    italic=True,
                    color=self._text_color
                )
                controls.extend([ft.Row(controls=[icon, label]), value])
            return ft.Column(controls=controls, expand=True)

        temp_unit = TranslationService.get_unit_symbol("temperature", self._unit_system)
        wind_unit = TranslationService.get_unit_symbol("wind", self._unit_system)
        pressure_unit = TranslationService.get_unit_symbol("pressure", self._unit_system)

        col1_items = [
            {"icon": ft.Icons.THERMOSTAT, "label": "feels_like", "value": f"{self._feels_like_data}{temp_unit}"},
            {"icon": ft.Icons.WATER_DROP, "label": "humidity", "value": f"{self._humidity_data}%"},
        ]

        col2_items = [
            {"icon": ft.Icons.WIND_POWER, "label": "wind", "value": f"{self._wind_speed_data} {wind_unit}"},
            {"icon": ft.Icons.COMPRESS, "label": "pressure", "value": f"{self._pressure_data} {pressure_unit}"},
        ]

        return ft.Column(
            controls=[
                title_text,
                divider,
                ft.Row(
                    controls=[
                        create_info_column(col1_items),
                        create_info_column(col2_items),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
