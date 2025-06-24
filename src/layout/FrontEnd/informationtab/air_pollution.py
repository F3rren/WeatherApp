import flet as ft
import logging
import traceback
from services.api_service import ApiService
from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class AirPollutionDisplay(ft.Container):
    """
    Air pollution display component.
    Shows detailed air quality information.
    Manages its own UI construction, updates, and state observers.
    """
    
    def __init__(self, page: ft.Page, lat: float = None, lon: float = None, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self._lat = lat
        self._lon = lon
        
        self._api_service = ApiService()
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._pollution_data = {}

        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20, 'label': 15, 'value': 15, 
                'subtitle': 15, 'aqi_value': 16
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
        self._initialize_state_and_observers()
        
        self.content = self.build()
        if self.page:
            self.page.run_task(self.update_ui)

    def _initialize_state_and_observers(self):
        """Initializes state manager and registers observers.""" 
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._state_manager.register_observer("language_event", lambda e=None: self.page.run_task(self.update_ui, e))
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

    async def update_ui(self, event_data=None):
        """Updates the UI based on state changes, fetching new data if necessary."""
        if not self.page or not self.visible:
            return

        try:
            data_changed = False
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                language_changed = self._current_language != new_language
                self._current_language = new_language
                data_changed = language_changed

            if not self._pollution_data or data_changed:
                if self._lat is not None and self._lon is not None:
                    self._pollution_data = await self._api_service.get_air_pollution_async(self._lat, self._lon) or {}
                else:
                    self._pollution_data = {}

            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._current_text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            if self.page:
                self.update()
        except Exception as e:
            logging.error(f"AirPollutionDisplay: Error updating UI: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs the UI for air pollution data."""
        if not self._pollution_data or "aqi" not in self._pollution_data:
            return ft.Column([
                ft.Text(
                    TranslationService.translate_from_dict("air_pollution_items", "no_air_pollution_data", self._current_language),
                    color=self._current_text_color,
                    size=self._text_handler.get_size('label')
                )
            ])

        aqi = self._pollution_data.get("aqi", 0)
        components = {k: v for k, v in self._pollution_data.items() if k != "aqi"}

        aqi_title_control = ft.Text(
            TranslationService.translate_from_dict("air_pollution_items", "air_quality_index", self._current_language),
            weight=ft.FontWeight.BOLD, 
            color=self._current_text_color,
            size=self._text_handler.get_size('title')
        )
        
        aqi_desc = self._get_aqi_description(aqi)
        aqi_value_control = ft.Text(
            aqi_desc, 
            weight=ft.FontWeight.BOLD, 
            color="#ffffff" if aqi > 2 else self._current_text_color,
            size=self._text_handler.get_size('aqi_value')
        )
        
        aqi_row = ft.Row([
            aqi_title_control,
            ft.Container(
                content=aqi_value_control,
                bgcolor=self._get_aqi_color(aqi),
                border_radius=10, padding=10, alignment=ft.alignment.center, expand=True
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
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
        ordered_keys = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
        mid_point = (len(ordered_keys) + 1) // 2

        for i, key in enumerate(ordered_keys):
            detail = pollutant_details_map.get(key)
            if not detail: continue

            value_str = f"{detail['value']:.2f} μg/m³"
            
            desc_text_control = ft.Text(
                detail['name'], 
                color=self._current_text_color,
                size=self._text_handler.get_size('label')
            )
            
            symbol_text_control = ft.Text(
                f"{key.upper().replace('_', '.')}:",
                weight=ft.FontWeight.BOLD, 
                color=self._current_text_color,
                size=self._text_handler.get_size('value')
            )
            
            value_text_control = ft.Text(
                value_str, 
                color=self._current_text_color,
                size=self._text_handler.get_size('value')
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
        
        return ft.Column(
            controls=[aqi_row, ft.Divider(height=1, color=divider_color), pollutants_row],
            spacing=15,
            expand=True
        )

    def _get_aqi_description(self, aqi_value: int) -> str:
        """Get localized description based on Air Quality Index using only translations_data.py"""
        from utils.translations_data import TRANSLATIONS
        lang_code = TranslationService.normalize_lang_code(self._current_language)
        aqi_descriptions = TRANSLATIONS.get(lang_code, {}).get("air_pollution_items", {}).get("aqi_descriptions")
        if not aqi_descriptions:
            aqi_descriptions = TRANSLATIONS.get("en", {}).get("air_pollution_items", {}).get("aqi_descriptions", ["N/A"] * 6)
        idx = min(max(aqi_value, 0), 5)
        return aqi_descriptions[idx] if idx < len(aqi_descriptions) else "N/A"

    def _get_aqi_color(self, aqi_value: int) -> str:
        """Get color based on Air Quality Index"""
        colors = [
            "#D3D3D3", "#00E400", "#FFFF00", "#FF7E00", "#FF0000", "#99004C"
        ]
        idx = max(0, min(aqi_value, len(colors) - 1))
        return colors[idx]

    def update_location(self, lat: float, lon: float):
        """Allows updating the location and refreshing the air pollution data."""
        if self._lat != lat or self._lon != lon:
            self._lat = lat
            self._lon = lon
            self._pollution_data = {} # Force refetch
            if self.page:
                self.page.run_task(self.update_ui)

    async def refresh(self):
        """Forces a data refetch and UI update."""
        self._pollution_data = {} # By clearing the data, we ensure update_ui will fetch new data.
        if self.page:
            await self.update_ui()


