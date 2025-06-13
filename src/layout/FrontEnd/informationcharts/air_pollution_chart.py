import flet as ft
import math
import logging
from services.api_service import ApiService
from services.translation_service import TranslationService
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE
from components.responsive_text_handler import ResponsiveTextHandler
from typing import Optional, Dict, Any

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
        self._translation_service = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._pollution_data: Dict[str, Any] = {}
        self._ui_elements_built = False
        self._chart_control: Optional[ft.BarChart] = None

        self._text_handler = ResponsiveTextHandler(
            page=self.page, 
            base_sizes={
                'axis_title': 14, # CHANGED: Reduced from 16 to 14
                'label': 14,
                'tooltip': 12, 
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
        self.content = ft.Text("Loading air pollution chart...")

    def did_mount(self):
        if self.page and self._text_handler and not self._text_handler.page:
            self._text_handler.page = self.page
        
        self._initialize_services_and_observers()
        
        if self._lat is not None and self._lon is not None:
            if self.page:
                self.page.run_task(self._fetch_data_and_request_rebuild)

    async def _fetch_data_and_request_rebuild(self):
        await self._fetch_air_pollution_data()
        self._request_ui_rebuild()

    def _initialize_services_and_observers(self):
        if self.page and hasattr(self.page, 'session'):
            self._state_manager = self.page.session.get('state_manager')
            self._translation_service = TranslationService(self.page.session) 

            if self._state_manager:
                self._current_language = self._state_manager.get_state('language') or self._current_language
                self._state_manager.register_observer("language_event", self._handle_language_change)
                self._state_manager.register_observer("theme_event", self._handle_theme_change)
        
        if self.page:
            self._original_on_resize = self.page.on_resize
            self.page.on_resize = self._combined_resize_handler
        
        self._current_text_color = self._determine_text_color_from_theme()

    def will_unmount(self):
        if self._state_manager:
            self._state_manager.unregister_observer("language_event", self._handle_language_change)
            self._state_manager.unregister_observer("theme_event", self._handle_theme_change)
        
        if self.page and hasattr(self, '_original_on_resize'):
            self.page.on_resize = self._original_on_resize
        elif self.page and self.page.on_resize == self._combined_resize_handler:
            # Fallback if _original_on_resize was not set but handler was attached
            # This might happen if will_unmount is called before did_mount fully completes
            # or if there's an unusual lifecycle sequence.
            # To be safe, try to revert to a generic handler or None if no other known handler.
            # For now, we assume _original_on_resize should exist if _combined_resize_handler was set.
            # If this becomes an issue, a more robust way to store original handlers might be needed.
            pass # Or set to a default if one exists, or None

    def _determine_text_color_from_theme(self):
        if self.page and self.page.theme_mode:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config.get("TEXT", ft.Colors.BLACK)
        return LIGHT_THEME.get("TEXT", ft.Colors.BLACK)

    async def _fetch_air_pollution_data(self):
        if self._lat is None or self._lon is None:
            self._pollution_data = {}
            return
        self._pollution_data = self._api_service.get_air_pollution(self._lat, self._lon) or {}

    def _build_ui_elements(self):
        if not self._pollution_data or "co" not in self._pollution_data:
            return ft.Text(
                self._translation_service.get_text("no_air_pollution_data", self._current_language) if self._translation_service else "No air pollution data",
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

        unit_text = self._translation_service.get_text("micrograms_per_cubic_meter_short", self._current_language) if self._translation_service else "μg/m³"

        bar_groups = []
        component_keys = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
        component_colors = [
            ft.Colors.with_opacity(0.8, ft.Colors.RED_ACCENT_700), # CO
            ft.Colors.with_opacity(0.8, ft.Colors.ORANGE_ACCENT_700), # NO
            ft.Colors.with_opacity(0.8, ft.Colors.AMBER_ACCENT_700),  # NO2
            ft.Colors.with_opacity(0.8, ft.Colors.LIME_ACCENT_700),   # O3
            ft.Colors.with_opacity(0.8, ft.Colors.LIGHT_BLUE_ACCENT_700), # SO2
            ft.Colors.with_opacity(0.8, ft.Colors.INDIGO_ACCENT_700), # PM2.5
            ft.Colors.with_opacity(0.8, ft.Colors.PURPLE_ACCENT_700), # PM10
            ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY_700) # NH3
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
                            tooltip=f"{key.upper()}: {round(value)} {unit_text}", # CHANGED: Added component name to tooltip
                            border_radius=0,
                        )
                    ]
                )
            )
        
        y_axis_title_text = self._translation_service.get_text("air_pollution_chart_y_axis_title", self._current_language) if self._translation_service else "Pollutant Level"
        y_axis_title_control = ft.Text(
            y_axis_title_text,
            color=self._current_text_color,
            size=self._text_handler.get_size('axis_title'),
            data={'type': 'text', 'category': 'axis_title'}
        )

        bottom_axis_labels_text = {
            "co": "CO", "no": "NO", "no2": "NO₂", "o3": "O₃", 
            "so2": "SO₂", "pm2_5": "PM₂.₅", "pm10": "PM₁₀", "nh3": "NH₃" # Corrected subscripts
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
                        size=self._text_handler.get_size('label'),
                        data={'type': 'text', 'category': 'label'}
                    )
                )
            )

        self._chart_control = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, self._current_text_color)), # Reduced opacity
            left_axis=ft.ChartAxis(
                labels_size=self._text_handler.get_size('label') * 2.8, 
                title=y_axis_title_control,
                title_size=self._text_handler.get_size('axis_title') # Ensure this is updated in _update_text_sizes
            ),
            bottom_axis=ft.ChartAxis(
                labels=bottom_axis_labels,
                labels_size=self._text_handler.get_size('label') * 3.5, 
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.with_opacity(0.15, self._current_text_color), width=1, dash_pattern=[6, 3] # Softer grid
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.BLACK if self.page.theme_mode == ft.ThemeMode.DARK else ft.Colors.WHITE), # Theme aware tooltip
            max_y=final_max_y,
            interactive=False,
            expand=True,
        )
        
        self._ui_elements_built = True
        return self._chart_control

    def _request_ui_rebuild(self, event_data=None):
        if not self.page or not self.visible: 
            return

        if self._state_manager:
            self._current_language = self._state_manager.get_state('language') or self._current_language
        
        self._current_text_color = self._determine_text_color_from_theme()
        
        new_content = self._build_ui_elements()
        if self.content != new_content:
            self.content = new_content
        
        if self._ui_elements_built:
            self._update_text_sizes() 

        if self.page: # Ensure page context before calling update
            self.update()

    def _handle_language_change(self, event_data=None):
        self._request_ui_rebuild()

    def _handle_theme_change(self, event_data=None):
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_theme_change received unexpected event_data type: {type(event_data)}")
        self._request_ui_rebuild()

    def _update_text_sizes(self):
        if not self._ui_elements_built or not self.content or not isinstance(self.content, ft.BarChart):
            return

        chart = self.content

        if chart.left_axis and isinstance(chart.left_axis.title, ft.Text):
            category = chart.left_axis.title.data.get('category') if isinstance(chart.left_axis.title.data, dict) else 'axis_title'
            new_size = self._text_handler.get_size(category)
            if chart.left_axis.title.size != new_size:
                 chart.left_axis.title.size = new_size
            if chart.left_axis.title.color != self._current_text_color:
                chart.left_axis.title.color = self._current_text_color
            # Ensure the reserved space for the title is also updated based on the new text size.
            # This might involve a multiplier or a fixed padding, depending on Flet's behavior.
            # For ft.ChartAxis, title_size directly controls this reserved space.
            if chart.left_axis.title_size != new_size: # Check if update is needed
                chart.left_axis.title_size = new_size 

        # Update Bottom Axis Labels
        if chart.bottom_axis and chart.bottom_axis.labels:
            new_label_size_val = self._text_handler.get_size('label')
            # Update reserved space for labels
            # The multiplier (e.g., * 3.5) should be consistent with _build_ui_elements
            new_labels_space = new_label_size_val * 3.5 
            if chart.bottom_axis.labels_size != new_labels_space:
                chart.bottom_axis.labels_size = new_labels_space

            for label_obj in chart.bottom_axis.labels:
                if isinstance(label_obj.label, ft.Text):
                    category = label_obj.label.data.get('category') if isinstance(label_obj.label.data, dict) else 'label'
                    if label_obj.label.size != new_label_size_val:
                        label_obj.label.size = new_label_size_val
                    if label_obj.label.color != self._current_text_color:
                        label_obj.label.color = self._current_text_color
        
        # self.update() # This is typically called by the caller of _update_text_sizes or _request_ui_rebuild

    def _combined_resize_handler(self, e):
        if hasattr(self, '_original_on_resize') and self._original_on_resize:
            # Check if _original_on_resize is callable before calling it
            if callable(self._original_on_resize):
                self._original_on_resize(e)
            else:
                # Log or handle the case where _original_on_resize is not callable
                # print(f"Warning: _original_on_resize is not callable: {self._original_on_resize}")
                pass # Or raise an error, or attempt a default behavior

        self._text_handler._handle_resize(e) 
        if self._ui_elements_built:
            self._update_text_sizes()
            if self.page: 
                self.update()

    def update_location(self, lat: float, lon: float):
        if self._lat != lat or self._lon != lon:
            self._lat = lat
            self._lon = lon
            if self.page and self.visible:
                self.page.run_task(self._fetch_data_and_request_rebuild)