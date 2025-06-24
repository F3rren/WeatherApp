import flet as ft
import math
import logging
from services.api_service import ApiService
from services.translation_service import TranslationService
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE
from components.responsive_text_handler import ResponsiveTextHandler
from typing import Optional

class AirPollutionChartDisplay(ft.Container):
    """
    Air Pollution chart display component.
    Manages its own UI construction, updates, and state observers.
    """
    
    def __init__(self, page: ft.Page, lat: Optional[float] = None, lon: Optional[float] = None, **kwargs):
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
                'axis_title': 14, 'label': 14, 'tooltip': 12
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
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
            logging.error(f"AirPollutionChartDisplay: Error updating UI: {e}")

    def build(self):
        """Constructs the UI for the air pollution chart."""
        if not self._pollution_data or "co" not in self._pollution_data:
            return ft.Text(
                TranslationService.translate_from_dict("air_pollution_chart_items", "no_air_pollution_data", self._current_language),
                color=self._current_text_color,
                size=self._text_handler.get_size('label')
            )

        components_data = {
            "co": float(self._pollution_data.get("co", 0.0)),
            "no": float(self._pollution_data.get("no", 0.0)),
            "no2": float(self._pollution_data.get("no2", 0.0)),
            "o3": float(self._pollution_data.get("o3", 0.0)),
            "so2": float(self._pollution_data.get("so2", 0.0)),
            "pm2_5": float(self._pollution_data.get("pm2_5", 0.0)),
            "pm10": float(self._pollution_data.get("pm10", 0.0)),
            "nh3": float(self._pollution_data.get("nh3", 0.0)),
        }

        all_metrics = list(components_data.values())
        max_val = max(all_metrics) if all_metrics else 0.0
        
        raw_dynamic_max_y = 0.0
        if max_val == 0.0:
            raw_dynamic_max_y = 50.0
        else:
            buffered_max_percentage = max_val * 1.2
            buffered_max_fixed = max_val + 10.0
            raw_dynamic_max_y = max(buffered_max_percentage, buffered_max_fixed, 20.0)

        if raw_dynamic_max_y <= 0:
            final_max_y = 50.0
        elif raw_dynamic_max_y <= 50:
            final_max_y = math.ceil(raw_dynamic_max_y / 10) * 10
        elif raw_dynamic_max_y <= 200:
            final_max_y = math.ceil(raw_dynamic_max_y / 20) * 20
        else:
            final_max_y = math.ceil(raw_dynamic_max_y / 50) * 50
        final_max_y = max(final_max_y, 10.0)

        unit_text = TranslationService.translate_from_dict("air_pollution_chart_items", "micrograms_per_cubic_meter_short", self._current_language)

        bar_groups = []
        component_keys = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
        component_colors = [
            ft.Colors.with_opacity(0.8, ft.Colors.RED_ACCENT_700),
            ft.Colors.with_opacity(0.8, ft.Colors.ORANGE_ACCENT_700),
            ft.Colors.with_opacity(0.8, ft.Colors.AMBER_ACCENT_700),
            ft.Colors.with_opacity(0.8, ft.Colors.LIME_ACCENT_700),
            ft.Colors.with_opacity(0.8, ft.Colors.LIGHT_BLUE_ACCENT_700),
            ft.Colors.with_opacity(0.8, ft.Colors.INDIGO_ACCENT_700),
            ft.Colors.with_opacity(0.8, ft.Colors.PURPLE_ACCENT_700),
            ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY_700)
        ]

        for i, key in enumerate(component_keys):
            value = components_data[key]
            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0, to_y=value, width=30,
                            color=component_colors[i],
                            tooltip=f"{key.upper()}: {round(value)} {unit_text}",
                            border_radius=0,
                        )
                    ]
                )
            )
        
        y_axis_title_text = TranslationService.translate_from_dict("air_pollution_chart_items", "air_pollution_chart_y_axis_title", self._current_language)
        y_axis_title_control = ft.Text(
            y_axis_title_text,
            color=self._current_text_color,
            size=self._text_handler.get_size('axis_title')
        )

        bottom_axis_labels_text = {
            "co": "CO", "no": "NO", "no2": "NO₂", "o3": "O₃", 
            "so2": "SO₂", "pm2_5": "PM₂.₅", "pm10": "PM₁₀", "nh3": "NH₃"
        }
        bottom_axis_labels = []
        for i, key in enumerate(component_keys):
            label_text = bottom_axis_labels_text.get(key, key.upper())
            bottom_axis_labels.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(
                        label_text, 
                        color=self._current_text_color, 
                        size=self._text_handler.get_size('label')
                    )
                )
            )

        return ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, self._current_text_color)),
            left_axis=ft.ChartAxis(
                labels_size=self._text_handler.get_size('label') * 2.8, 
                title=y_axis_title_control,
                title_size=self._text_handler.get_size('axis_title')
            ),
            bottom_axis=ft.ChartAxis(
                labels=bottom_axis_labels,
                labels_size=self._text_handler.get_size('label') * 3.5, 
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.with_opacity(0.15, self._current_text_color), width=1, dash_pattern=[6, 3]
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.BLACK if self.page.theme_mode == ft.ThemeMode.DARK else ft.Colors.WHITE),
            max_y=final_max_y,
            interactive=False,
            expand=True,
        )

    def update_location(self, lat: float, lon: float):
        """Allows updating the location and refreshing the air pollution chart data."""
        if self._lat != lat or self._lon != lon:
            self._lat = lat
            self._lon = lon
            if self.page:
                self.page.run_task(self.update_ui)