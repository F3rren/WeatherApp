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
                new_language = self._state_manager.get_state('language')
                new_unit_system = self._state_manager.get_state('unit')
                
                # Usa i valori predefiniti se i nuovi valori sono None
                self._current_language = new_language if new_language is not None else self._current_language
                self._current_unit_system = new_unit_system if new_unit_system is not None else self._current_unit_system

            # Verifica che TranslationService sia disponibile
            if not hasattr(TranslationService, 'get_unit_symbol'):
                logging.warning("TranslationService.get_unit_symbol non disponibile, uso simbolo predefinito")
                self._unit_symbol = "°"
            else:
                # Update unit symbol and text color
                self._unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
            
            # Verifica che la pagina abbia un tema impostato
            if not hasattr(self.page, 'theme_mode'):
                logging.warning("theme_mode non disponibile nella pagina, uso tema chiaro")
                is_dark = False
            else:
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._current_text_color = theme.get("TEXT", ft.Colors.BLACK)

            # Verifica che i dati siano validi prima di ricostruire il contenuto
            if self._validate_data():
                self.content = self.build()
                # Only update if this control is already in the page
                try:
                    if self.page and hasattr(self, 'page') and self.page is not None:
                        self.update()
                except Exception:
                    # Control not yet added to page, update will happen when added
                    pass
            else:
                logging.warning("Dati non validi per l'aggiornamento del grafico")
                
        except Exception as e:
            logging.error(f"TemperatureChartDisplay: Error updating UI: {str(e)}", exc_info=True)
            # Prova a ripristinare uno stato stabile
            self._reset_to_safe_state()

    def _validate_data(self):
        """Validates the chart data for consistency."""
        if not isinstance(self._days, list) or not isinstance(self._temp_min, list) or not isinstance(self._temp_max, list):
            return False
        
        if len(self._days) != len(self._temp_min) or len(self._days) != len(self._temp_max):
            return False
        
        return all(isinstance(temp, (int, float)) for temp in self._temp_min + self._temp_max)

    def _reset_to_safe_state(self):
        """Resets the component to a safe state in case of errors."""
        try:
            self._days = []
            self._temp_min = []
            self._temp_max = []
            self._unit_symbol = "°"
            self.content = ft.Container(
                content=ft.Text(
                    "Error loading temperature chart",
                    color=ft.Colors.RED_400,
                    size=14,
                    weight=ft.FontWeight.W_500
                ),
                alignment=ft.alignment.center,
                padding=20
            )
            # Only update if this control is already in the page
            try:
                if self.page and hasattr(self, 'page') and self.page is not None:
                    self.update()
            except Exception:
                # Control not yet added to page, update will happen when added
                pass
        except Exception as e:
            logging.error(f"Failed to reset to safe state: {str(e)}", exc_info=True)

    def build(self):
        """Constructs modern UI for the temperature chart."""
        if not self._days or not self._temp_min or not self._temp_max or \
           len(self._days) != len(self._temp_min) or len(self._days) != len(self._temp_max):
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

        # Build header
        header = self._build_header()
        
        # Build modern chart
        chart_container = self._build_modern_chart()
        
        # Build modern legend
        legend = self._build_modern_legend()
        
        return ft.Column([
            header,
            chart_container,
            legend
        ], spacing=12)

    def update_data(self, days: List[str], temp_min: List[int], temp_max: List[int]):
        """Allows updating the chart data and refreshing the display."""
        self._days = days if days is not None else []
        self._temp_min = temp_min if temp_min is not None else []
        self._temp_max = temp_max if temp_max is not None else []
        
        if self.page and self.visible:
            self.page.run_task(self.update_ui)
    
    def _build_header(self):
        """Builds a modern header for temperature chart section."""
        header_text = TranslationService.translate_from_dict("temperature_chart_items", "temperature", self._current_language)
        
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.THERMOSTAT_OUTLINED,
                    color=ft.Colors.ORANGE_400 if not is_dark else ft.Colors.ORANGE_300,
                    size=24
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    f"{header_text} ({self._unit_symbol})",
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
        
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        # Enhanced colors for better visibility and modern appeal
        if not is_dark:
            # Light theme: vibrant but not too bright
            max_color = "#ef4444"  # Modern red
            min_color = "#3b82f6"  # Modern blue
        else:
            # Dark theme: softer, more pleasant colors
            max_color = "#f87171"  # Lighter red for dark backgrounds
            min_color = "#60a5fa"  # Lighter blue for dark backgrounds
        
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
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME
        
        # Use theme colors for better integration
        chart_bgcolor = theme.get("CARD_BACKGROUND", "#ffffff" if not is_dark else "#2a2a2a")
        if chart_bgcolor == "#ffffff":
            # Light theme: subtle blue-tinted background
            chart_bgcolor = "#f8fafc"  # Very light blue-gray
        elif chart_bgcolor == "#2a2a2a":
            # Dark theme: darker background with slight blue tint
            chart_bgcolor = "#1e293b"  # Dark blue-gray
        
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
        
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        # Use the same modern colors as the chart
        if not is_dark:
            max_color = "#ef4444"  # Modern red
            min_color = "#3b82f6"  # Modern blue
        else:
            max_color = "#f87171"  # Lighter red for dark backgrounds
            min_color = "#60a5fa"  # Lighter blue for dark backgrounds

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
