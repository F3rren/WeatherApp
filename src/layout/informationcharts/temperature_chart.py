import traceback
import flet as ft
from typing import List, Optional
import math
from services.translation_service import TranslationService
from services.theme_handler import ThemeHandler
import logging

class TemperatureChartDisplay(ft.Container):
    """
    Temperature chart display component.
    Simple structure similar to MainWeatherInfo.
    """
    
    def __init__(self, 
                 page: ft.Page, 
                 days: Optional[List[str]] = None, 
                 temp_min: Optional[List[int]] = None, 
                 temp_max: Optional[List[int]] = None, 
                 language: str = None,
                 unit: str = None,
                 theme_handler: ThemeHandler = None, 
                 **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.days = days if days is not None else []
        self.temp_min = temp_min if temp_min is not None else []
        self.temp_max = temp_max if temp_max is not None else []

        # ThemeHandler centralizzato
        self.theme_handler = theme_handler or ThemeHandler(self.page)

        # State manager e variabili di stato
        self.state_manager = None
        self.current_language = language
        self.current_unit_system = unit
        self.current_text_color = self.theme_handler.get_text_color()

        # Setup state manager
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._state_manager.register_observer("theme_event", self.update_theme)
            self._state_manager.register_observer("language_event", self.update_language)
            self._state_manager.register_observer("unit", self.update_unit)

        # Build initial content
        self.content = self.build()

    def update_theme(self, event_data=None):
        """
        Update only the theme-related properties of this component.
        """
        # Usa ThemeHandler per aggiornare il colore testo
        self._current_text_color = self.theme_handler.get_text_color()
        self.content = self.build()
        try:
            super().update()
        except Exception:
            pass
    def update_language(self, event_data=None):
        """
        Update only the language-dependent texts of this component.
        """
        if self._state_manager:
            new_language = self._state_manager.get_state('language') or self.current_language
            self.current_language = new_language
        self.content = self.build()
        try:
            super().update()
        except Exception:
            pass

    def update_unit(self, event_data=None):
        """
        Update only the unit-dependent values of this component.
        """
        if self._state_manager:
            new_unit_system = self._state_manager.get_state('unit') or self.current_unit_system
            self.current_unit_system = new_unit_system
        self.content = self.build()
        try:
            super().update()
        except Exception:
            pass

    def cleanup(self):
        """
        Deregister this component from all observers.
        """
        if self._state_manager:
            self._state_manager.remove_observer("theme_event", self.update_theme)
            self._state_manager.remove_observer("language_event", self.update_language)
            self._state_manager.remove_observer("unit", self.update_unit)

    def update(self):
        """Updates state and rebuilds the UI without fetching new data."""
        if not self.page or not self.visible:
            return

        try:
            # Update state from state_manager
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self.current_language
                new_unit_system = self._state_manager.get_state('unit') or self.current_unit_system
                self.current_language = new_language
                self.current_unit_system = new_unit_system

            # Aggiorna il colore testo tramite ThemeHandler
            self._current_text_color = self.theme_handler.get_text_color()

            # Rebuild and update UI
            self.content = self.build()
            
            # Update the component itself
            try:
                super().update()
            except (AssertionError, AttributeError):
                # Component not yet added to page, skip update
                pass
            # Also try to update the parent container if possible
            if hasattr(self, 'parent') and self.parent:
                try:
                    self.parent.update()
                except (AssertionError, AttributeError):
                    pass
        except Exception as e:
            logging.error(f"MainWeatherInfo: Error updating: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs the UI for the temperature chart - simple and direct."""
        try:
            # Validate data
            if not self.days or not self.temp_min or not self.temp_max or \
               len(self.days) != len(self.temp_min) or len(self.days) != len(self.temp_max):
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
        header_text = TranslationService.translate_from_dict("temperature_chart_items", "temperature", self.current_language)
        unit_symbol = TranslationService.get_unit_symbol("temperature", self.current_unit_system)
        complete_title = f"{header_text} ({unit_symbol})"
        icon_color = ft.Colors.ORANGE_400
        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.THERMOSTAT_OUTLINED,
                    color=icon_color,
                    size=25
                ),
                ft.Container(width=5),
                ft.Text(
                    complete_title,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=self.current_text_color
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=20, bottom=10)
        )
    
    def _build_chart(self):
        """Builds the temperature chart - simple version."""
        data_points_min = []
        data_points_max = []
        unit_symbol = TranslationService.get_unit_symbol("temperature", self.current_language)
        max_color = "#ef4444"
        min_color = "#3b82f6"
        for i, day_label_key in enumerate(self.days):
            day_display_name = TranslationService.translate_from_dict("temperature_chart_items", day_label_key, self.current_language)
            data_points_min.append(
                ft.LineChartDataPoint(
                    i, self.temp_min[i],
                    tooltip=f"{day_display_name}: {self.temp_min[i]}{unit_symbol}",
                    tooltip_style=ft.TextStyle(
                        size=12,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_500
                    ),
                )
            )
            data_points_max.append(
                ft.LineChartDataPoint(
                    i, self.temp_max[i],
                    tooltip=f"{day_display_name}: {self.temp_max[i]}{unit_symbol}",
                    tooltip_style=ft.TextStyle(
                        size=12,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_500
                    ),
                )
            )
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
        x_labels = []
        for i, day_label_key in enumerate(self.days):
            day_display_name = TranslationService.translate_from_dict("temperature_chart_items", day_label_key, self.current_language)
            if day_display_name and isinstance(day_display_name, str):
                day_display_name = day_display_name[0].upper() + day_display_name[1:] if len(day_display_name) > 1 else day_display_name.upper()
            x_labels.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(
                        day_display_name,
                        size=14,
                        color=self.current_text_color,
                        weight=ft.FontWeight.W_500
                    )
                )
            )
        all_temps = self.temp_min + self.temp_max
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
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.current_text_color)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=step,
                color=ft.Colors.with_opacity(0.08, self.current_text_color),
                width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.Colors.with_opacity(0.08, self.current_text_color),
                width=1
            ),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=y,
                        label=ft.Text(
                            str(int(y)),
                            size=14,
                            color=self.current_text_color,
                            weight=ft.FontWeight.W_500
                        )
                    ) for y in range(int(min_y_val), int(max_y_val) + 1, step)
                ],
                labels_size=45,
                title_size=16
            ),
            bottom_axis=ft.ChartAxis(
                labels=x_labels,
                labels_size=45,
            ),
            tooltip_bgcolor=ft.Colors.BLACK87,
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
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.GREY_400)),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            )
        )
    
    def _build_legend(self):
        """Builds legend - simple version."""
        legend_max_text = TranslationService.translate_from_dict("temperature_chart_items", "max", self.current_language)
        legend_min_text = TranslationService.translate_from_dict("temperature_chart_items", "min", self.current_language)
        max_color = "#ef4444"
        min_color = "#3b82f6"
        max_item = ft.Container(
            content=ft.Row([
                ft.Container(width=16, height=4, bgcolor=max_color, border_radius=2),
                ft.Container(width=8),
                ft.Text(legend_max_text, color=self.current_text_color, size=14, weight=ft.FontWeight.W_500)
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.05, max_color)
        )
        min_item = ft.Container(
            content=ft.Row([
                ft.Container(width=16, height=4, bgcolor=min_color, border_radius=2),
                ft.Container(width=8),
                ft.Text(legend_min_text, color=self.current_text_color, size=14, weight=ft.FontWeight.W_500)
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
                    TranslationService.translate_from_dict("temperature_chart_items", "no_temperature_data", self.current_language),
                    color=self.current_text_color,
                    size=14
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
        self.days = days if days is not None else []
        self.temp_min = temp_min if temp_min is not None else []
        self.temp_max = temp_max if temp_max is not None else []
        
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
        if self.state_manager:
            try:
                self.state_manager.unregister_observer("unit_text_change", self._handle_unit_change)
                self.state_manager.unregister_observer("unit", self._handle_unit_change)
            except Exception as e:
                logging.error(f"TemperatureChartDisplay: Error during cleanup: {e}")
