import flet as ft
from typing import List, Optional
import math
from utils.config import DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
from services.theme_handler import ThemeHandler
import logging

class TemperatureChartDisplay(ft.Container):
    """
    Temperature chart display component.
    Simple structure similar to MainWeatherInfo.
    """
    
    def __init__(self, page: ft.Page, days: Optional[List[str]] = None, 
                 temp_min: Optional[List[int]] = None, temp_max: Optional[List[int]] = None, 
                 theme_handler: ThemeHandler = None, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self._days = days if days is not None else []
        self._temp_min = temp_min if temp_min is not None else []
        self._temp_max = temp_max if temp_max is not None else []

        # ThemeHandler centralizzato
        self.theme_handler = theme_handler or ThemeHandler(self.page)

        # Initialize state variables
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_unit_system = DEFAULT_UNIT_SYSTEM
        self._current_text_color = self.theme_handler.get_text_color()

        # ResponsiveTextHandler
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'legend': 14, 'label': 14, 'axis_title': 14, 'tooltip': 12
            },
            breakpoints=[600, 900, 1200, 1600]
        )

        # Set default properties
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)

        # Setup observers and handlers
        if self.page:
            if self._text_handler and not self._text_handler.page:
                self._text_handler.page = self.page
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            if self._state_manager:
                self._state_manager.register_observer("unit_text_change", self._handle_unit_change)
                self._state_manager.register_observer("unit", self._handle_unit_change)

        # Build initial content
        self.content = self.build()

    def update(self):
        """Updates state and rebuilds the UI - simple like MainWeatherInfo."""
        if not self.page or not self.visible:
            return

        try:
            # Update state from state_manager
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                new_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
                self._current_language = new_language
                self._current_unit_system = new_unit_system

            # Update theme color (centralizzato)
            self._current_text_color = self.theme_handler.get_text_color()

            # Rebuild and update UI - no cache, always fresh
            self.content = self.build()

            # Update the component itself
            try:
                super().update()
            except (AssertionError, AttributeError):
                pass

        except Exception as e:
            logging.error(f"TemperatureChartDisplay: Error updating: {e}")

    def build(self):
        """Constructs the UI for the temperature chart - simple and direct."""
        try:
            # Validate data
            if not self._days or not self._temp_min or not self._temp_max or \
               len(self._days) != len(self._temp_min) or len(self._days) != len(self._temp_max):
                return self._build_no_data_view()

            # Build components
            header = self._build_header()
            chart_container = self._build_chart()
            legend = self._build_legend()
            
            return ft.Column([
                header,
                chart_container,
                legend
            ], spacing=12)
            
        except Exception as e:
            logging.error(f"TemperatureChartDisplay: Error building: {e}")
            return self._build_error_view()

    def _build_header(self):
        """Builds header - simple, no cache."""
        # Get current values directly
        header_text = TranslationService.translate_from_dict("temperature_chart_items", "temperature", self._current_language)
        unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
        
        # Build complete header title with unit
        complete_title = f"{header_text} ({unit_symbol})"

        # Usa ThemeHandler per il colore icona
        icon_color = ft.Colors.ORANGE_400 if self.theme_handler.get_theme() == self.theme_handler.get_theme() else ft.Colors.ORANGE_300
        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.THERMOSTAT_OUTLINED,
                    color=icon_color,
                    size=24
                ),
                ft.Container(width=12),
                ft.Text(
                    complete_title,
                    size=self._text_handler.get_size('axis_title') + 2,
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=20, bottom=10)
        )
    
    def _build_modern_chart(self):
        """Builds a modern styled temperature chart."""
        # Chart Data with enhanced styling
        data_points_min = []
        data_points_max = []
        
        # Usa ThemeHandler per i colori (se vuoi ruoli diversi, puoi estendere qui)
        is_dark = self.theme_handler.get_theme() == self.theme_handler.get_theme()
        max_color = "#ef4444" if not is_dark else "#f87171"
        min_color = "#3b82f6" if not is_dark else "#60a5fa"
        
        for i, day_label_key in enumerate(self._days):
            day_display_name = TranslationService.translate_from_dict("temperature_chart_items", day_label_key, self._current_language)
            
            # Min temperature point
            data_points_min.append(
                ft.LineChartDataPoint(
                    i, self._temp_min[i],
                    tooltip=f"{day_display_name}: {self._temp_min[i]}{self._unit_symbol}",
                    tooltip_style=ft.TextStyle(
                        size=self._text_handler.get_size('tooltip'), 
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_500
                    ),
                )
            )
            # Max temperature point
            data_points_max.append(
                ft.LineChartDataPoint(
                    i, self._temp_max[i],
                    tooltip=f"{day_display_name}: {self._temp_max[i]}{self._unit_symbol}",
                    tooltip_style=ft.TextStyle(
                        size=self._text_handler.get_size('tooltip'), 
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_500
                    ),
                )
            )

        # Enhanced line styling with better visual appeal
        line_min = ft.LineChartData(
            data_points=data_points_min,
            stroke_width=4,  # Thicker for better visibility
            color=min_color,
            curved=True,
            stroke_cap_round=True,
        )
        line_max = ft.LineChartData(
            data_points=data_points_max,
            stroke_width=4,  # Thicker for better visibility
            color=max_color,
            curved=True,
            stroke_cap_round=True,
        )
        
        # X-axis labels with better formatting
        x_labels = []
        for i, day_label_key in enumerate(self._days):
            day_display_name = TranslationService.translate_from_dict("temperature_chart_items", day_label_key, self._current_language)
            if day_display_name and isinstance(day_display_name, str):
                # Make first letter uppercase, keep rest as is for abbreviations
                day_display_name = day_display_name[0].upper() + day_display_name[1:] if len(day_display_name) > 1 else day_display_name.upper()
            x_labels.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(
                        day_display_name, 
                        size=self._text_handler.get_size('label'), 
                        color=self._current_text_color,
                        weight=ft.FontWeight.W_500
                    )
                )
            )
        
        # Calculate Y-axis range with better spacing
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

        # Modern chart with enhanced styling
        chart_control = ft.LineChart(
            interactive=False,  # Make it interactive
            data_series=[line_min, line_max],
            border=ft.border.all(
                1, 
                ft.Colors.with_opacity(0.1, self._current_text_color)
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=step, 
                color=ft.Colors.with_opacity(0.08, self._current_text_color), 
                width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1, 
                color=ft.Colors.with_opacity(0.08, self._current_text_color), 
                width=1
            ),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=y, 
                        label=ft.Text(
                            str(int(y)), 
                            size=self._text_handler.get_size('label'), 
                            color=self._current_text_color,
                            weight=ft.FontWeight.W_500
                        )
                    ) for y in range(int(min_y_val), int(max_y_val) + 1, step)
                ],
                labels_size=45, 
                title_size=self._text_handler.get_size('axis_title') 
            ),
            bottom_axis=ft.ChartAxis(
                labels=x_labels,
                labels_size=45, 
            ),
            tooltip_bgcolor=ft.Colors.BLACK87 if not is_dark else ft.Colors.WHITE12,
            min_y=int(min_y_val),
            max_y=int(max_y_val),
            expand=True,
        )
        
        # Modern chart container with better background
        # Usa ThemeHandler per il background
        chart_bgcolor = self.theme_handler.get_background_color()
        if chart_bgcolor == "#ffffff":
            chart_bgcolor = "#f8fafc"
        elif chart_bgcolor == "#2a2a2a":
            chart_bgcolor = "#1e293b"
        
        # Container with modern styling
        return ft.Container(
            content=chart_control,
            height=300,  # Fixed height for better layout
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            border_radius=16,  # More rounded corners
            bgcolor=chart_bgcolor,
            border=ft.border.all(
                1, 
                ft.Colors.with_opacity(0.08, ft.Colors.GREY_400 if not is_dark else ft.Colors.GREY_600)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            )
        )
    
    def _build_modern_legend(self):
        """Builds a modern styled legend."""
        legend_max_text = TranslationService.translate_from_dict("temperature_chart_items", "max", self._current_language)
        legend_min_text = TranslationService.translate_from_dict("temperature_chart_items", "min", self._current_language)
        
        is_dark = self.theme_handler.get_theme() == self.theme_handler.get_theme()
        max_color = "#ef4444" if not is_dark else "#f87171"
        min_color = "#3b82f6" if not is_dark else "#60a5fa"

        # Modern legend items
        max_item = ft.Container(
            content=ft.Row([
                ft.Container(
                    width=16,
                    height=4,
                    bgcolor=max_color,
                    border_radius=2
                ),
                ft.Container(width=8),
                ft.Text(
                    legend_max_text,
                    color=self._current_text_color,
                    size=self._text_handler.get_size('legend'),
                    weight=ft.FontWeight.W_500
                )
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.05, max_color)
        )
        
        min_item = ft.Container(
            content=ft.Row([
                ft.Container(
                    width=16,
                    height=4,
                    bgcolor=min_color,
                    border_radius=2
                ),
                ft.Container(width=8),
                ft.Text(
                    legend_min_text,
                    color=self._current_text_color,
                    size=self._text_handler.get_size('legend'),
                    weight=ft.FontWeight.W_500
                )
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.05, min_color)
        )
        
        return ft.Container(
            content=ft.Row([
                max_item,
                ft.Container(width=16),
                min_item
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=20, vertical=10)
        )

    def _build_chart(self):
        """Builds the temperature chart - simple version."""
        # Chart Data with enhanced styling
        data_points_min = []
        data_points_max = []
        
        # Get current unit symbol directly
        unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
        
        is_dark = self.theme_handler.get_theme() == self.theme_handler.get_theme()
        max_color = "#ef4444" if not is_dark else "#f87171"
        min_color = "#3b82f6" if not is_dark else "#60a5fa"
        
        for i, day_label_key in enumerate(self._days):
            day_display_name = TranslationService.translate_from_dict("temperature_chart_items", day_label_key, self._current_language)
            
            # Min temperature point
            data_points_min.append(
                ft.LineChartDataPoint(
                    i, self._temp_min[i],
                    tooltip=f"{day_display_name}: {self._temp_min[i]}{unit_symbol}",
                    tooltip_style=ft.TextStyle(
                        size=self._text_handler.get_size('tooltip'), 
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_500
                    ),
                )
            )
            # Max temperature point
            data_points_max.append(
                ft.LineChartDataPoint(
                    i, self._temp_max[i],
                    tooltip=f"{day_display_name}: {self._temp_max[i]}{unit_symbol}",
                    tooltip_style=ft.TextStyle(
                        size=self._text_handler.get_size('tooltip'), 
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_500
                    ),
                )
            )

        # Line chart data
        line_min = ft.LineChartData(
            data_points=data_points_min,
            stroke_width=4,
            color=min_color,
            curved=True,
            stroke_cap_round=True,
        )
        line_max = ft.LineChartData(
            data_points=data_points_max,
            stroke_width=4,
            color=max_color,
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
                    label=ft.Text(
                        day_display_name, 
                        size=self._text_handler.get_size('label'), 
                        color=self._current_text_color,
                        weight=ft.FontWeight.W_500
                    )
                )
            )
        
        # Calculate Y-axis range
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

        # Chart
        chart_control = ft.LineChart(
            interactive=False,
            data_series=[line_min, line_max],
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, self._current_text_color)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=step, 
                color=ft.Colors.with_opacity(0.08, self._current_text_color), 
                width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1, 
                color=ft.Colors.with_opacity(0.08, self._current_text_color), 
                width=1
            ),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=y, 
                        label=ft.Text(
                            str(int(y)), 
                            size=self._text_handler.get_size('label'), 
                            color=self._current_text_color,
                            weight=ft.FontWeight.W_500
                        )
                    ) for y in range(int(min_y_val), int(max_y_val) + 1, step)
                ],
                labels_size=45, 
                
                title_size=self._text_handler.get_size('axis_title') 
            ),
            bottom_axis=ft.ChartAxis(
                labels=x_labels,
                labels_size=45, 
            ),
            tooltip_bgcolor=ft.Colors.BLACK87 if not is_dark else ft.Colors.WHITE12,
            min_y=int(min_y_val),
            max_y=int(max_y_val),
            expand=True,
        )
        
        chart_bgcolor = self.theme_handler.get_background_color()
        if chart_bgcolor == "#ffffff":
            chart_bgcolor = "#f8fafc"
        elif chart_bgcolor == "#2a2a2a":
            chart_bgcolor = "#1e293b"
        
        return ft.Container(
            content=chart_control,
            height=300,
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            border_radius=16,
            bgcolor=chart_bgcolor,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.GREY_400 if not is_dark else ft.Colors.GREY_600)),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            )
        )
    
    def _build_legend(self):
        """Builds legend - simple version."""
        legend_max_text = TranslationService.translate_from_dict("temperature_chart_items", "max", self._current_language)
        legend_min_text = TranslationService.translate_from_dict("temperature_chart_items", "min", self._current_language)
        
        is_dark = self.theme_handler.get_theme() == self.theme_handler.get_theme()
        max_color = "#ef4444" if not is_dark else "#f87171"
        min_color = "#3b82f6" if not is_dark else "#60a5fa"

        # Legend items
        max_item = ft.Container(
            content=ft.Row([
                ft.Container(width=16, height=4, bgcolor=max_color, border_radius=2),
                ft.Container(width=8),
                ft.Text(legend_max_text, color=self._current_text_color, size=self._text_handler.get_size('legend'), weight=ft.FontWeight.W_500)
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.05, max_color)
        )
        
        min_item = ft.Container(
            content=ft.Row([
                ft.Container(width=16, height=4, bgcolor=min_color, border_radius=2),
                ft.Container(width=8),
                ft.Text(legend_min_text, color=self._current_text_color, size=self._text_handler.get_size('legend'), weight=ft.FontWeight.W_500)
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.05, min_color)
        )
        
        return ft.Container(
            content=ft.Row([max_item, ft.Container(width=16), min_item], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=20, vertical=10)
        )

    def _build_no_data_view(self):
        """Builds view when no data is available."""
        return ft.Column([
            self._build_header(),
            ft.Container(
                content=ft.Text(
                    TranslationService.translate_from_dict("temperature_chart_items", "no_temperature_data", self._current_language),
                    color=self._current_text_color,
                    size=self._text_handler.get_size('label')
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.all(20)
            )
        ])

    def _build_error_view(self):
        """Builds view when there's an error."""
        return ft.Container(
            content=ft.Text(
                "Error loading temperature chart",
                color=ft.Colors.RED_400,
                size=14,
                weight=ft.FontWeight.W_500
            ),
            alignment=ft.alignment.center,
            padding=20
        )

    def update_data(self, days: List[str], temp_min: List[int], temp_max: List[int]):
        """Updates chart data and refreshes display."""
        self._days = days if days is not None else []
        self._temp_min = temp_min if temp_min is not None else []
        self._temp_max = temp_max if temp_max is not None else []
        
        if self.page and self.visible:
            try:
                self.update()
            except Exception as e:
                logging.error(f"Error updating temperature chart: {e}")

    def _handle_unit_change(self, event_data=None):
        """Handle unit system change events by updating the component."""
        try:
            if self.page and self.visible:
                self.update()
        except Exception as e:
            logging.error(f"TemperatureChartDisplay: Error handling unit change: {e}")

    def cleanup(self):
        """Clean up observers and resources."""
        if self._state_manager:
            try:
                self._state_manager.unregister_observer("unit_text_change", self._handle_unit_change)
                self._state_manager.unregister_observer("unit", self._handle_unit_change)
            except Exception as e:
                logging.error(f"TemperatureChartDisplay: Error during cleanup: {e}")
