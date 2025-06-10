import flet as ft
from typing import List
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler

class TemperatureChart:
    """
    Temperature chart display.
    """
    
    def __init__(self, page: ft.Page, days: List[str], temp_min: List[int], 
                 temp_max: List[int], text_color: str = None): # text_color can be optional if derived from theme
        self.page = page
        self.days = days 
        self.temp_min = temp_min
        self.temp_max = temp_max
        
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'legend': 14,
                'label': 14,
                'axis_title': 16,
                'icon': 20,
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        self.text_controls = {}
        
        self.state_manager = self.page.session.get('state_manager')
        self.translation_service = self.page.session.get('translation_service')

        if self.state_manager:
            self.language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            self.unit_system = self.state_manager.get_state('unit_system') or DEFAULT_UNIT_SYSTEM
            current_theme_mode = self.state_manager.get_state('theme_mode') or self.page.theme_mode
        else:
            self.language = DEFAULT_LANGUAGE
            self.unit_system = DEFAULT_UNIT_SYSTEM
            current_theme_mode = self.page.theme_mode
        
        self.text_color = DARK_THEME["TEXT"] if current_theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"]
        if text_color: # Allow override if explicitly passed, though theme-based is preferred
             self.text_color = text_color

        self.unit_symbol = "°" # Default
        if self.translation_service:
            self.unit_symbol = self.translation_service.get_unit_symbol("temperature", self.unit_system, self.language)

        max_text_str = "Max"
        min_text_str = "Min"
        if self.translation_service:
            max_text_str = self.translation_service.get_text("max", self.language)
            min_text_str = self.translation_service.get_text("min", self.language)

        self.legend_max_text = ft.Text(max_text_str, color=self.text_color, size=self.text_handler.get_size('legend'))
        self.legend_min_text = ft.Text(min_text_str, color=self.text_color, size=self.text_handler.get_size('legend'))
        
        self.text_controls[self.legend_max_text] = 'legend'
        self.text_controls[self.legend_min_text] = 'legend'
        
        self.y_axis_title = ft.Text(color=self.text_color, size=self.text_handler.get_size('axis_title'))
        self._update_y_axis_title_text() 
        self.text_controls[self.y_axis_title] = 'axis_title'

        if self.page:
            original_resize_handler = self.page.on_resize
            def combined_resize_handler(e):
                self.text_handler._handle_resize(e)
                self.update_text_controls()
                if original_resize_handler:
                    original_resize_handler(e)
            self.page.on_resize = combined_resize_handler
            
        if self.state_manager:
            self.state_manager.register_observer("theme_event", self._handle_state_change)
            self.state_manager.register_observer("language_event", self._handle_state_change)
            self.state_manager.register_observer("unit_system_event", self._handle_state_change)


    def _update_y_axis_title_text(self):
        title_str = "Temperature"
        if self.translation_service:
            title_str = self.translation_service.get_text("temperature", self.language)
        self.y_axis_title.value = f"{title_str} ({self.unit_symbol})"
        if self.y_axis_title.page:
            self.y_axis_title.update()

    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati"""
        for control, size_category in self.text_controls.items():
            new_size = self.text_handler.get_size(size_category)
            if hasattr(control, 'size'):
                control.size = new_size
            elif hasattr(control, 'style') and hasattr(control.style, 'size'): # For TextSpans
                control.style.size = new_size
            
            if hasattr(control, 'spans'): # For ft.Text with spans
                for span in control.spans:
                    if hasattr(span, 'style') and span.style:
                        span.style.size = new_size
                    else:
                        span.style = ft.TextStyle(size=new_size)
            
            if control.page: # Guard update
                control.update()
        
        # Update chart specific label sizes if not covered by individual controls
        if hasattr(self, 'chart_control') and self.chart_control:
            if self.chart_control.left_axis:
                self.chart_control.left_axis.labels_size = self.text_handler.get_size('label') * 2.8 # Adjust multiplier as needed
                if self.chart_control.left_axis.title:
                     self.chart_control.left_axis.title_size = self.text_handler.get_size('axis_title') * 1.2 # Adjust
            if self.chart_control.bottom_axis:
                self.chart_control.bottom_axis.labels_size = self.text_handler.get_size('label') * 2.8 # Adjust
            if self.chart_control.page:
                self.chart_control.update()


    def _handle_state_change(self, event_data=None):
        if not self.page or not self.state_manager or not self.translation_service:
            return

        new_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
        new_unit_system = self.state_manager.get_state('unit_system') or DEFAULT_UNIT_SYSTEM
        
        language_changed = self.language != new_language
        unit_system_changed = self.unit_system != new_unit_system
        
        self.language = new_language
        self.unit_system = new_unit_system
        
        current_theme_mode = self.state_manager.get_state('theme_mode') or self.page.theme_mode
        self.text_color = DARK_THEME["TEXT"] if current_theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"]

        if language_changed or unit_system_changed:
            self.unit_symbol = self.translation_service.get_unit_symbol("temperature", self.unit_system, self.language)
            self.legend_max_text.value = self.translation_service.get_text("max", self.language)
            self.legend_min_text.value = self.translation_service.get_text("min", self.language)
            self._update_y_axis_title_text() 

        self.legend_max_text.color = self.text_color
        self.legend_min_text.color = self.text_color
        self.y_axis_title.color = self.text_color
        
        if hasattr(self, 'chart_control') and self.chart_control.page:
            self._update_chart_axis_colors() 
            if language_changed: # If days are keys like "monday", they need retranslation
                self.chart_control.bottom_axis.labels = self._build_x_labels()
            self.chart_control.left_axis.title = self.y_axis_title
            self.chart_control.update()
        
        self.update_text_controls() 
        
        if self.legend_max_text.page: 
            self.legend_max_text.update()
        if self.legend_min_text.page: 
            self.legend_min_text.update()
        # y_axis_title is updated within _update_y_axis_title_text and update_text_controls

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color and chart elements."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]

            # Update legend text colors
            if hasattr(self, 'legend_max_text'):
                self.legend_max_text.color = self.text_color
                if self.legend_max_text.page:
                    self.legend_max_text.update()
            
            if hasattr(self, 'legend_min_text'):
                self.legend_min_text.color = self.text_color
                if self.legend_min_text.page:
                    self.legend_min_text.update()

            # For axis labels, the chart might need to be rebuilt
            if hasattr(self, 'chart_control') and self.chart_control.page:
                 # Update axis label colors directly
                 self._update_chart_axis_colors()
                 self.chart_control.update()

    def _update_chart_axis_colors(self):
        """Updates the colors of chart axis labels."""
        if hasattr(self, 'chart_control'):
            # Update X-axis labels
            if self.chart_control.bottom_axis and self.chart_control.bottom_axis.labels:
                for label in self.chart_control.bottom_axis.labels:
                    if isinstance(label.label, ft.Container) and isinstance(label.label.content, ft.Text):
                        label.label.content.color = self.text_color
                        
                        # Aggiorna il dizionario dei controlli di testo
                        self.text_controls[label.label.content] = 'label'
            
            # Update Y-axis labels
            if self.chart_control.left_axis and self.chart_control.left_axis.labels:
                for label in self.chart_control.left_axis.labels:
                    if isinstance(label.label, ft.Text):
                        label.label.color = self.text_color
                        
                        # Aggiorna il dizionario dei controlli di testo
                        self.text_controls[label.label] = 'label'
            
            # Aggiorna le dimensioni dopo aver cambiato colore
            self.update_text_controls()

    def _build_x_labels(self) -> List[ft.ChartAxisLabel]:
        x_labels = []
        for i, day_input in enumerate(self.days): # self.days could be keys or already processed strings
            day_display_text = day_input # Default to the input

            if self.translation_service:
                # translate_weekday should handle various inputs:
                # - Known keys (e.g., "monday") will be translated.
                # - Unknown keys/already translated strings should be returned appropriately (e.g., as is or capitalized).
                day_display_text = self.translation_service.translate_weekday(str(day_input), self.language)
            elif isinstance(day_input, str):
                # Fallback if no translation_service and input is a string (e.g., "monday")
                day_display_text = day_input.capitalize()
            else:
                # Fallback for non-string inputs if no translation service
                day_display_text = str(day_input)

            label_text_control = ft.Text(
                day_display_text,
                size=self.text_handler.get_size('label'),
                weight=ft.FontWeight.BOLD,
                color=self.text_color
            )
            self.text_controls[label_text_control] = 'label' # Register for responsive sizing
            x_labels.append(ft.ChartAxisLabel(
                value=i + 1, # Chart typically 1-indexed for categories
                label=ft.Container(
                    label_text_control,
                    margin=ft.margin.only(top=10),
                )
            ))
        return x_labels

    def _build_y_labels(self, min_y, max_y) -> List[ft.ChartAxisLabel]:
        y_labels = []
        for y_val in range(min_y, max_y + 1, 5): # Assuming step of 5
            label_text_control = ft.Text(
                str(y_val), 
                size=self.text_handler.get_size('label'), 
                color=self.text_color
            )
            self.text_controls[label_text_control] = 'label' # Register
            y_labels.append(ft.ChartAxisLabel(value=y_val, label=label_text_control))
        return y_labels

    def build(self) -> ft.Column:
        min_temp_val = min(self.temp_min) if self.temp_min else 0
        max_temp_val = max(self.temp_max) if self.temp_max else 30
        
        # Dynamic Y-axis range calculation
        min_y = int((min_temp_val - 5) // 5 * 5) 
        max_y = int((max_temp_val + 5) // 5 * 5)
        if min_y == max_y: # Ensure there's some range
            max_y += 5 
        min_y = max(min_y, 0) # Ensure min_y is not negative unless intended for specific chart types

        data_series = [
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i + 1, t) for i, t in enumerate(self.temp_min)],
                stroke_width=3, color=ft.Colors.BLUE, curved=True, stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i + 1, t) for i, t in enumerate(self.temp_max)],
                stroke_width=3, color=ft.Colors.RED, curved=True, stroke_cap_round=True,
            ),
        ]
        
        x_axis_labels = self._build_x_labels()
        y_axis_labels = self._build_y_labels(min_y, max_y)
        
        self.chart_control = ft.LineChart(
            data_series=data_series,
            border=ft.border.all(3, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=max(1, (max_y - min_y) / 5 if (max_y - min_y) > 0 else 1), # Dynamic interval
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
            ),
            left_axis=ft.ChartAxis(
                labels=y_axis_labels, 
                title=self.y_axis_title,
            ),
            bottom_axis=ft.ChartAxis(labels=x_axis_labels),
            min_y=min_y, max_y=max_y,
            min_x=0, max_x=len(self.days) +1 if self.days else 1, # Adjusted max_x for padding
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            expand=True,
            interactive=False,  # Disable hover/tooltips
        )
        
        self.update_text_controls() # Apply initial sizes and colors registered in build methods

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.RED, size=self.text_handler.get_size('icon')),
                        self.legend_max_text,
                        ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.BLUE, size=self.text_handler.get_size('icon')),
                        self.legend_min_text,
                    ], 
                    spacing=10, # Reduced spacing
                    alignment=ft.MainAxisAlignment.CENTER # Center legends
                ),
                self.chart_control
            ],
            expand=True, # Ensure Column expands
            # horizontal_alignment=ft.CrossAxisAlignment.CENTER # Center chart if needed
        )
