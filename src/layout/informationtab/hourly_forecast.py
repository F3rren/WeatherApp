import flet as ft
from datetime import datetime
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
from services.api_service import ApiService
import logging
import asyncio
import traceback

class HourlyForecastDisplay(ft.Container):
    """
    Manages the display of the entire hourly forecast section.
    """
    def __init__(self, city: str, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self._city = city
        self.page = page
        self._api_service = ApiService()
        self._hourly_data_list = []
        
        self._state_manager = None
        self._language = DEFAULT_LANGUAGE
        self._unit_system = DEFAULT_UNIT_SYSTEM
        self._text_color = LIGHT_THEME["TEXT"]

        self.expand = True 

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={'icon': 60, 'time': 20, 'temp': 25},
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
                if self.text_handler:
                    self.text_handler._handle_resize(e)
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
                new_language = self._state_manager.get_state('language') or self._language
                new_unit_system = self._state_manager.get_state('unit') or self._unit_system
                
                language_changed = self._language != new_language
                unit_changed = self._unit_system != new_unit_system

                self._language = new_language
                self._unit_system = new_unit_system
                
                data_changed = language_changed or unit_changed

            if not self._hourly_data_list or data_changed:
                weather_data = await asyncio.to_thread(
                    self._api_service.get_weather_data,
                    city=self._city, language=self._language, unit=self._unit_system
                )
                if weather_data:
                    self._hourly_data_list = self._api_service.get_hourly_forecast_data(weather_data)

            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            self.update()
        except Exception as e:
            logging.error(f"HourlyForecastDisplay: Error updating UI: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs the Flet UI elements for the hourly forecast."""
        if not self._hourly_data_list:
            return ft.Row([ft.Text("Loading hourly forecast...")])

        forecast_item_controls = []
        for item_data in self._hourly_data_list:
            try:
                time_str = datetime.strptime(item_data["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
                icon_code = item_data["weather"][0]["icon"]
                temp_value = round(item_data["main"]["temp"])
                unit_symbol = TranslationService.get_unit_symbol("temperature", self._unit_system)

                icon_image = ft.Image(
                    src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                    width=self.text_handler.get_size('icon'),
                    height=self.text_handler.get_size('icon'),
                    fit=ft.ImageFit.CONTAIN,
                )
                
                time_text = ft.Text(
                    time_str,
                    size=self.text_handler.get_size('time'),
                    color=self._text_color,
                )
                
                temp_text_val = ft.Text(
                    f"{temp_value}{unit_symbol}",
                    size=self.text_handler.get_size('temp'),
                    weight=ft.FontWeight.BOLD,
                    color=self._text_color,
                )

                item_column = ft.Column(
                    controls=[icon_image, time_text, temp_text_val],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                )
                
                item_container = ft.Container(
                    content=item_column,
                    padding=ft.padding.symmetric(horizontal=5, vertical=10),
                    margin=ft.margin.only(right=5),
                )
                forecast_item_controls.append(item_container)
            except Exception as e:
                logging.error(f"Error processing hourly item: {item_data}, Error: {e}")
                forecast_item_controls.append(ft.Text("Error", color=ft.colors.RED))

        return ft.Row(
            controls=forecast_item_controls,
            scroll=ft.ScrollMode.ADAPTIVE,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
        )
    
    def update_city(self, new_city: str):
        """Allows updating the city and refreshing the forecast."""
        if self._city != new_city:
            self._city = new_city
            self._hourly_data_list = []
            if self.page:
                self.page.run_task(self.update_ui)

