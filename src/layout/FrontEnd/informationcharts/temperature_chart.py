import flet as ft
from typing import List, Optional # Added Optional
import math # ADDED: For floor and ceil functions
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService # Added
import logging

class TemperatureChartDisplay(ft.Container): # CHANGED: Inherits from ft.Container, renamed
    """
    Temperature chart display component.
    Manages its own UI construction, updates, and state observers.
    """
    
    def __init__(self, page: ft.Page, days: Optional[List[str]] = None, 
                 temp_min: Optional[List[int]] = None, temp_max: Optional[List[int]] = None, 
                 **kwargs): # CHANGED: Added **kwargs, made data optional
        super().__init__(**kwargs) # Pass kwargs to ft.Container
        self.page = page
        self._days = days if days is not None else []
        self._temp_min = temp_min if temp_min is not None else []
        self._temp_max = temp_max if temp_max is not None else []
        
        self._state_manager = None
        self._translation_service = None # Will be initialized in did_mount
        self._current_language = DEFAULT_LANGUAGE
        self._current_unit_system = DEFAULT_UNIT_SYSTEM
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._unit_symbol = "°" 
        self._ui_elements_built = False
        self._chart_control: Optional[ft.LineChart] = None # To store the chart control

        self._text_handler = ResponsiveTextHandler(
            page=self.page, # Page context might be None initially if page not passed to constructor
            base_sizes={
                'legend': 14,
                'label': 14, # For axis labels
                'axis_title': 14, # CHANGED: Reduced from 16 to 14
                'tooltip': 12, # For data point tooltips
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Default container properties
        if 'expand' not in kwargs:
            self.expand = True # Or False, depending on desired default
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
        self.content = ft.Text("Loading temperature chart...") # Initial placeholder

    def did_mount(self):
        """Called when the control is added to the page."""
        if self.page and self._text_handler and not self._text_handler.page:
            self._text_handler.page = self.page
        
        self._initialize_services_and_observers()
        
        # Fetch initial data or build UI if data was provided at init
        if self._days and self._temp_min and self._temp_max:
            self._request_ui_rebuild()
        # Else, it might wait for an update_data call

    def _initialize_services_and_observers(self):
        """Initializes services and registers observers."""
        if self.page and hasattr(self.page, 'session'):
            self._state_manager = self.page.session.get('state_manager')
            # Initialize TranslationService here as page.session should be available
            self._translation_service = TranslationService(self.page.session) 

            if self._state_manager:
                self._current_language = self._state_manager.get_state('language') or self._current_language
                self._current_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
                
                self._state_manager.register_observer("language_event", self._handle_language_change)
                self._state_manager.register_observer("theme_event", self._handle_theme_change)
                self._state_manager.register_observer("unit_event", self._handle_unit_system_change) # Assuming "unit_event"
        
        if self.page:
            self._original_on_resize = self.page.on_resize
            self.page.on_resize = self._combined_resize_handler
        
        # Initial update of unit symbol and text color based on current state
        self._update_unit_symbol()
        self._current_text_color = self._determine_text_color_from_theme()


    def will_unmount(self):
        """Called when the control is removed from the page."""
        if self._state_manager:
            self._state_manager.unregister_observer("language_event", self._handle_language_change)
            self._state_manager.unregister_observer("theme_event", self._handle_theme_change)
            self._state_manager.unregister_observer("unit_event", self._handle_unit_system_change)
        
        if self.page and hasattr(self, '_original_on_resize'):
            self.page.on_resize = self._original_on_resize
        elif self.page and self.page.on_resize == self._combined_resize_handler:
            self.page.on_resize = self._original_on_resize # Or None if it was the first

    def _determine_text_color_from_theme(self):
        if self.page and self.page.theme_mode:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config.get("TEXT", ft.Colors.BLACK)
        return LIGHT_THEME.get("TEXT", ft.Colors.BLACK)

    def _update_unit_symbol(self):
        if self._translation_service:
            self._unit_symbol = self._translation_service.get_unit_symbol("temperature", self._current_unit_system)

    def _build_ui_elements(self):
        """Constructs the UI for the temperature chart."""
        if not self._days or not self._temp_min or not self._temp_max or \
           len(self._days) != len(self._temp_min) or len(self._days) != len(self._temp_max):
            return ft.Text(
                self._translation_service.get_text("no_temperature_data", self._current_language) if self._translation_service else "No temperature data",
                color=self._current_text_color,
                size=self._text_handler.get_size('label')
            )

        # Chart Data
        data_points_min = []
        data_points_max = []
        for i, day_label_key in enumerate(self._days): # Assuming _days contains translation keys
            day_display_name = self._translation_service.get_text(day_label_key, self._current_language) if self._translation_service else day_label_key
            
            # Min temperature point
            data_points_min.append(
                ft.LineChartDataPoint(
                    i, self._temp_min[i],
                    tooltip=f"{day_display_name}: {self._temp_min[i]}{self._unit_symbol}",
                    tooltip_style=ft.TextStyle(size=self._text_handler.get_size('tooltip'), color=ft.Colors.BLACK), # Tooltip text color
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
            color=ft.Colors.BLUE_ACCENT, # Or theme-based
            curved=True,
            stroke_cap_round=True,
        )
        line_max = ft.LineChartData(
            data_points=data_points_max,
            stroke_width=2,
            color=ft.Colors.RED_ACCENT, # Or theme-based
            curved=True,
            stroke_cap_round=True,
        )

        # X-axis labels
        x_labels = []
        for i, day_label_key in enumerate(self._days):
            day_display_name = self._translation_service.get_text(day_label_key, self._current_language) if self._translation_service else day_label_key
            x_labels.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(day_display_name[:3], size=self._text_handler.get_size('label'), color=self._current_text_color, data={'type': 'text', 'category': 'label'})
                )
            )
        
        # Y-axis title
        y_axis_title_text = self._translation_service.get_text("temperature", self._current_language) if self._translation_service else "Temperature"
        y_axis_title_control = ft.Text(
            f"{y_axis_title_text} ({self._unit_symbol})", 
            size=self._text_handler.get_size('axis_title'), 
            color=self._current_text_color,
            data={'type': 'text', 'category': 'axis_title'}
        )

        # Determine min/max for Y-axis
        all_temps = self._temp_min + self._temp_max
        step = 5  # Define step for clarity

        if not all_temps:
            min_y_val = 0
            max_y_val = 10  # Default range for empty chart
        else:
            data_min_val = min(all_temps)
            data_max_val = max(all_temps)
            
            # Calculate Y-axis limits to be multiples of step, with padding
            min_y_val = math.floor((data_min_val - step) / step) * step
            max_y_val = math.ceil((data_max_val + step) / step) * step

            # Ensure there's always some range, e.g., if all temps are the same or very close
            if max_y_val <= min_y_val:
                # If data_min_val and data_max_val are same, max_y_val could be min_y_val + step.
                # e.g. data=12. min_y_val=5, max_y_val=math.ceil((12+5)/5)*5 = math.ceil(3.4)*5 = 20.
                # This case (max_y_val <= min_y_val) should be rare with the current padding.
                # Add a default span if it happens.
                max_y_val = min_y_val + step * 2 
            
            # Ensure max_y_val is strictly greater than min_y_val for the range function
            if max_y_val == min_y_val:
                max_y_val += step


        self._chart_control = ft.LineChart(
            interactive=False,
            data_series=[line_min, line_max],
            border=ft.border.all(1, ft.Colors.with_opacity(0.5, self._current_text_color)),
            horizontal_grid_lines=ft.ChartGridLines(interval=step, color=ft.Colors.with_opacity(0.2, self._current_text_color), width=1), # Use step
            vertical_grid_lines=ft.ChartGridLines(interval=1, color=ft.Colors.with_opacity(0.2, self._current_text_color), width=1),
            left_axis=ft.ChartAxis(
                labels= [ft.ChartAxisLabel(value=y, label=ft.Text(str(int(y)), size=self._text_handler.get_size('label'), color=self._current_text_color, data={'type': 'text', 'category': 'label'})) for y in range(int(min_y_val), int(max_y_val) + 1, step)], # Use step
                labels_size=40, 
                title=y_axis_title_control, 
                title_size=self._text_handler.get_size('axis_title') 
            ),
            bottom_axis=ft.ChartAxis(
                labels=x_labels,
                labels_size=40, 
            ),
            tooltip_bgcolor=ft.Colors.WHITE, 
            min_y=int(min_y_val), # Use calculated min_y_val
            max_y=int(max_y_val), # Use calculated max_y_val
            expand=True,
        )

        # Legend
        legend_max_text = self._translation_service.get_text("max", self._current_language) if self._translation_service else "Max"
        legend_min_text = self._translation_service.get_text("min", self._current_language) if self._translation_service else "Min"

        legend = ft.Row(
            [
                ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.RED_ACCENT, size=self._text_handler.get_size('legend')),
                ft.Text(legend_max_text, color=self._current_text_color, size=self._text_handler.get_size('legend'), data={'type': 'text', 'category': 'legend'}),
                ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.BLUE_ACCENT, size=self._text_handler.get_size('legend')),
                ft.Text(legend_min_text, color=self._current_text_color, size=self._text_handler.get_size('legend'), data={'type': 'text', 'category': 'legend'}),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        
        main_column = ft.Column(
            controls=[self._chart_control, legend],
            spacing=10,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self._ui_elements_built = True
        return main_column

    def _request_ui_rebuild(self, event_data=None):
        if not self.page or not self.visible: 
            return

        if self._state_manager: # Ensure state is current before rebuild
            self._current_language = self._state_manager.get_state('language') or self._current_language
            self._current_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
        
        self._update_unit_symbol()
        self._current_text_color = self._determine_text_color_from_theme()
        
        new_content = self._build_ui_elements()
        if self.content != new_content:
            self.content = new_content
        
        if self._ui_elements_built:
            self._update_text_sizes() 

        self.update()

    def _handle_language_change(self, event_data=None):
        self._request_ui_rebuild()

    def _handle_theme_change(self, event_data=None):
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_theme_change received unexpected event_data type: {type(event_data)}")
        self._request_ui_rebuild()

    def _handle_unit_system_change(self, event_data=None):
        # Data might need to be re-fetched or re-processed by the parent (WeatherView)
        # For now, just rebuild UI which will use the new unit symbol.
        # If temperature values themselves change, update_data should be called.
        self._request_ui_rebuild()

    def _update_text_sizes(self):
        if not self._ui_elements_built or not self.content or not isinstance(self.content, ft.Column):
            return

        def _apply_to_controls(control_tree_node):
            if isinstance(control_tree_node, ft.Text) and hasattr(control_tree_node, 'data') and isinstance(control_tree_node.data, dict):
                category = control_tree_node.data.get('category')
                if category:
                    control_tree_node.size = self._text_handler.get_size(category)
                    control_tree_node.color = self._current_text_color # General color update
            
            # For LineChart specific text elements (axis titles, labels)
            if isinstance(control_tree_node, ft.LineChart):
                chart = control_tree_node
                # Left Axis
                if chart.left_axis:
                    # Reserved space for title
                    chart.left_axis.title_size = self._text_handler.get_size('axis_title') # ADDED: Ensure reserved space is updated
                    # Title font size (if Text control)
                    if isinstance(chart.left_axis.title, ft.Text):
                        chart.left_axis.title.size = self._text_handler.get_size('axis_title')
                        chart.left_axis.title.color = self._current_text_color
                    # Left Axis Labels
                    if chart.left_axis.labels:
                        chart.left_axis.labels_size = self._text_handler.get_size('label') * 2.8 # Example scaling
                        for label in chart.left_axis.labels:
                            if isinstance(label.label, ft.Text):
                                label.label.size = self._text_handler.get_size('label')
                                label.label.color = self._current_text_color
                # Bottom Axis
                if chart.bottom_axis:
                    # Bottom Axis Labels
                    if chart.bottom_axis.labels:
                        chart.bottom_axis.labels_size = self._text_handler.get_size('label') * 2.8 # Example scaling
                        for label in chart.bottom_axis.labels:
                            if isinstance(label.label, ft.Text):
                                label.label.size = self._text_handler.get_size('label')
                                label.label.color = self._current_text_color
                    # If bottom axis ever gets a title, its reserved space and font size should also be updated here
                    # For example:
                    # chart.bottom_axis.title_size = self._text_handler.get_size('axis_title') # Or a different category
                    # if isinstance(chart.bottom_axis.title, ft.Text):
                    #     chart.bottom_axis.title.size = self._text_handler.get_size('axis_title') # Or a different category
                    #     chart.bottom_axis.title.color = self._current_text_color
            
            if hasattr(control_tree_node, 'controls') and control_tree_node.controls:
                for child_control in control_tree_node.controls:
                    _apply_to_controls(child_control)
            elif hasattr(control_tree_node, 'content') and control_tree_node.content: # For single content containers
                _apply_to_controls(control_tree_node.content)

        _apply_to_controls(self.content)
        # self.update() # Called by _request_ui_rebuild

    def _combined_resize_handler(self, e):
        if hasattr(self, '_original_on_resize') and self._original_on_resize:
            self._original_on_resize(e) 

        self._text_handler._handle_resize(e) 
        if self._ui_elements_built:
            self._update_text_sizes()
            if self.page: 
                self.update()

    def update_data(self, days: List[str], temp_min: List[int], temp_max: List[int]):
        """Allows updating the chart data and refreshing the display."""
        self._days = days if days is not None else []
        self._temp_min = temp_min if temp_min is not None else []
        self._temp_max = temp_max if temp_max is not None else []
        
        if self.page and self.visible: # Only rebuild if mounted and visible
             self.page.run_task(self._request_ui_rebuild_task)

    async def _request_ui_rebuild_task(self): # Added async wrapper for run_task
        self._request_ui_rebuild()

# Example usage (for testing, not part of the class itself)
# if __name__ == \"__main__\":
#     def main(page: ft.Page):
#         page.title = \"Temperature Chart Test\"
#         # ... (setup state manager, translation service for testing) ...
#         
#         # Sample data
#         days_data = [\"mon\", \"tue\", \"wed\", \"thu\", \"fri\"]
#         min_temps = [10, 12, 11, 13, 14]
#         max_temps = [20, 22, 21, 23, 24]
# 
#         chart_display = TemperatureChartDisplay(page, days_data, min_temps, max_temps)
#         page.add(chart_display)
#     
#     ft.app(target=main)
