import flet as ft
from typing import List, Optional # Added Optional
import math # ADDED: For floor and ceil functions
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService # Added
import logging

class TemperatureChartDisplay(ft.Container):
    """
    Temperature chart display component.
    Manages its own UI construction, updates, and state observers.
    """
    
    def __init__(self, page: ft.Page, days: Optional[List[str]] = None, 
                 temp_min: Optional[List[int]] = None, temp_max: Optional[List[int]] = None, 
                 **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self._days = days if days is not None else []
        self._temp_min = temp_min if temp_min is not None else []
        self._temp_max = temp_max if temp_max is not None else []
        
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_unit_system = DEFAULT_UNIT_SYSTEM
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._unit_symbol = "°"

        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'legend': 14, 'label': 14, 'axis_title': 14, 'tooltip': 12
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
            self._state_manager.register_observer("unit_event", lambda e=None: self.page.run_task(self.update_ui, e))
        
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
        """Updates the UI based on state changes."""
        if not self.page or not self.visible:
            return

        try:
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                new_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
                
                self._current_language = new_language
                self._current_unit_system = new_unit_system

            # Update unit symbol and text color
            self._unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
            
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._current_text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            if self.page:
                self.update()
        except Exception as e:
            logging.error(f"TemperatureChartDisplay: Error updating UI: {e}")

    def build(self):
        """Constructs the UI for the temperature chart."""
        if not self._days or not self._temp_min or not self._temp_max or \
           len(self._days) != len(self._temp_min) or len(self._days) != len(self._temp_max):
            return ft.Text(
                TranslationService.translate_from_dict("temperature_chart_items", "no_temperature_data", self._current_language),
                color=self._current_text_color,
                size=self._text_handler.get_size('label')
            )

        # Chart Data
        data_points_min = []
        data_points_max = []
        for i, day_label_key in enumerate(self._days):
            day_display_name = TranslationService.translate_from_dict("temperature_chart_items", day_label_key, self._current_language)
            
            # Min temperature point
            data_points_min.append(
                ft.LineChartDataPoint(
                    i, self._temp_min[i],
                    tooltip=f"{day_display_name}: {self._temp_min[i]}{self._unit_symbol}",
                    tooltip_style=ft.TextStyle(size=self._text_handler.get_size('tooltip'), color=ft.Colors.BLACK),
                )
            )
            # Max temperature point
            data_points_max.append(
                ft.LineChartDataPoint(
                    i, self._temp_max[i],
                    tooltip=f"{day_display_name}: {self._temp_max[i]}{self._unit_symbol}",
                    tooltip_style=ft.TextStyle(size=self._text_handler.get_size('tooltip'), color=ft.Colors.BLACK),
                )
            )

        line_min = ft.LineChartData(
            data_points=data_points_min,
            stroke_width=2,
            color=ft.Colors.BLUE_ACCENT,
            curved=True,
            stroke_cap_round=True,
        )
        line_max = ft.LineChartData(
            data_points=data_points_max,
            stroke_width=2,
            color=ft.Colors.RED_ACCENT,
            curved=True,
            stroke_cap_round=True,
        )
        
        # X-axis labels
        x_labels = []
        for i, day_label_key in enumerate(self._days):
            day_display_name = TranslationService.translate_from_dict("temperature_chart_items", day_label_key, self._current_language)
            if day_display_name and isinstance(day_display_name, str):
                day_display_name = day_display_name[0].upper() + day_display_name[1:] if len(day_display_name) > 1 else day_display_name.upper()
            x_labels.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(day_display_name, size=self._text_handler.get_size('label'), color=self._current_text_color)
                )
            )
        
        # Y-axis title
        y_axis_title_text = TranslationService.translate_from_dict("temperature_chart_items", "temperature", self._current_language)
        y_axis_title_control = ft.Text(
            f"{y_axis_title_text} ({self._unit_symbol})", 
            size=self._text_handler.get_size('axis_title'), 
            color=self._current_text_color
        )

        # Determine min/max for Y-axis
        all_temps = self._temp_min + self._temp_max
        step = 5

        if not all_temps:
            min_y_val = 0
            max_y_val = 10
        else:
            data_min_val = min(all_temps)
            data_max_val = max(all_temps)
            
            min_y_val = math.floor((data_min_val - step) / step) * step
            max_y_val = math.ceil((data_max_val + step) / step) * step

            if max_y_val <= min_y_val:
                max_y_val = min_y_val + step * 2 
            
            if max_y_val == min_y_val:
                max_y_val += step

        chart_control = ft.LineChart(
            interactive=False,
            data_series=[line_min, line_max],
            border=ft.border.all(1, ft.Colors.with_opacity(0.5, self._current_text_color)),
            horizontal_grid_lines=ft.ChartGridLines(interval=step, color=ft.Colors.with_opacity(0.2, self._current_text_color), width=1),
            vertical_grid_lines=ft.ChartGridLines(interval=1, color=ft.Colors.with_opacity(0.2, self._current_text_color), width=1),
            left_axis=ft.ChartAxis(
                labels=[ft.ChartAxisLabel(value=y, label=ft.Text(str(int(y)), size=self._text_handler.get_size('label'), color=self._current_text_color)) for y in range(int(min_y_val), int(max_y_val) + 1, step)],
                labels_size=40, 
                title=y_axis_title_control, 
                title_size=self._text_handler.get_size('axis_title') 
            ),
            bottom_axis=ft.ChartAxis(
                labels=x_labels,
                labels_size=40, 
            ),
            tooltip_bgcolor=ft.Colors.WHITE, 
            min_y=int(min_y_val),
            max_y=int(max_y_val),
            expand=True,
        )

        # Legend
        legend_max_text = TranslationService.translate_from_dict("temperature_chart_items", "max", self._current_language)
        legend_min_text = TranslationService.translate_from_dict("temperature_chart_items", "min", self._current_language)

        legend = ft.Row(
            [
                ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.RED_ACCENT, size=self._text_handler.get_size('legend')),
                ft.Text(legend_max_text, color=self._current_text_color, size=self._text_handler.get_size('legend')),
                ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.BLUE_ACCENT, size=self._text_handler.get_size('legend')),
                ft.Text(legend_min_text, color=self._current_text_color, size=self._text_handler.get_size('legend')),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        
        return ft.Column(
            controls=[chart_control, legend],
            spacing=10,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER        )

    def update_data(self, days: List[str], temp_min: List[int], temp_max: List[int]):
        """Allows updating the chart data and refreshing the display."""
        self._days = days if days is not None else []
        self._temp_min = temp_min if temp_min is not None else []
        self._temp_max = temp_max if temp_max is not None else []
        
        if self.page and self.visible:
            self.page.run_task(self.update_ui)
