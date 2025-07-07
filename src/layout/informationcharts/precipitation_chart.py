"""
Precipitation Chart Display for MeteoApp.
Shows precipitation forecast and probability over time.
"""

import flet as ft
from typing import Dict, List, Any
import logging

from services.api_service import ApiService
from services.translation_service import TranslationService
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler

class PrecipitationChartDisplay(ft.Container):
    """
    Container for displaying precipitation forecast chart.
    Shows both precipitation amount and probability.
    """

    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self._api_service = ApiService()
        self._current_language = DEFAULT_LANGUAGE
        self._current_unit_system = DEFAULT_UNIT_SYSTEM
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._precipitation_data = []
        self._forecast_data = {}
        self._updating = False  # Flag to prevent concurrent updates
        self._cached_header = None  # Cache for header to prevent unnecessary rebuilds
        self._header_language = None  # Track which language the header was built for
        self._last_theme_mode = None  # Track theme changes for header cache invalidation
        
        # State management
        self._state_manager = None
        if self.page and hasattr(self.page, 'session'):
            self._state_manager = self.page.session.get('state_manager')
        
        # Initialize responsive text handler
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 18,
                'subtitle': 14,
                'body': 12,
                'small': 10,
                'axis_title': 14,  # Match other components sizing
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Set default properties
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
        # Register for events
        if self._state_manager:
            self._state_manager.register_observer("language_event", self._safe_language_update)
            self._state_manager.register_observer("unit", self._safe_unit_update)
            self._state_manager.register_observer("theme_event", self._safe_theme_update)
        
        # Set up page resize handler
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
        
        # Initialize content
        self.content = self.build()
        self.border_radius = 12
        self.animate = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        
        # Apply initial theme and update
        if self.page:
            self.page.run_task(self.update_ui)

    async def update_ui(self, event_data=None):
        """Update UI based on language, unit, or theme changes."""
        if not self.page or not self.visible or self._updating:
            return
        
        self._updating = True
        try:
            if self._state_manager:
                new_language = self._state_manager.get_state('language')
                new_unit_system = self._state_manager.get_state('unit')
                
                # print(f"DEBUG: PrecipitationChart update_ui - old language: {self._current_language}, new language: {new_language}")
                
                # Use default values if new values are None
                old_language = self._current_language
                self._current_language = new_language if new_language is not None else self._current_language
                self._current_unit_system = new_unit_system if new_unit_system is not None else self._current_unit_system
                
                # print(f"DEBUG: PrecipitationChart after assignment - current language: {self._current_language}")
                
                if old_language != self._current_language:
                    # print(f"DEBUG: Language changed from {old_language} to {self._current_language}, invalidating header cache")
                    # Invalidate header cache when language changes
                    self._cached_header = None
                    self._header_language = None
            else:
                # print("DEBUG: PrecipitationChart - no state_manager available")
                pass
            
            # Update theme colors
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK if hasattr(self.page, 'theme_mode') else False
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._current_text_color = theme.get("TEXT", ft.Colors.BLACK)
            
            # Also invalidate header cache when theme changes
            if hasattr(self, '_last_theme_mode') and self._last_theme_mode != is_dark:
                self._cached_header = None
                self._header_language = None
            self._last_theme_mode = is_dark
            
            # Apply theme to container
            self.bgcolor = theme.get("CHART", ft.Colors.WHITE)
            self.border = ft.border.all(
                1, 
                ft.Colors.with_opacity(0.1, theme.get("TEXT", ft.Colors.BLACK))
            )
            
            # Rebuild content
            self.content = self.build()
            
            # Only update if this control is already in the page
            try:
                if self.page and hasattr(self, 'page') and self.page is not None:
                    self.update()
            except Exception:
                # Control not yet added to page, update will happen when added
                pass
                
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error updating UI: {e}")
            self._reset_to_safe_state()

    def _reset_to_safe_state(self):
        """Resets the component to a safe state in case of errors."""
        try:
            self._precipitation_data = []
            self.content = ft.Container(
                content=ft.Text(
                    "Error loading precipitation chart",
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
            logging.error(f"Failed to reset to safe state: {str(e)}")

    def build(self):
        """Constructs the UI for the precipitation chart."""
        if not self._precipitation_data:
            return ft.Column([
                self._build_header(),
                self._build_loading_content()
            ])
        
        # Build header
        header = self._build_header()
        
        # Build chart
        chart_container = self._build_chart_content()
        
        # Build legend
        legend = self._build_legend()
        
        return ft.Column([
            header,
            chart_container,
            legend
        ], spacing=12)

    def _build_header(self):
        """Builds a modern header for precipitation chart section with caching."""
        # Check if we need to rebuild the header
        if self._cached_header is not None and self._header_language == self._current_language:
            # print(f"DEBUG: Using cached header for language: {self._current_language}")
            return self._cached_header
        
        # print(f"DEBUG: Building new header for language: {self._current_language}")
        header_text = TranslationService.translate_from_dict("precipitation_chart_items", "precipitation_chart_title", self._current_language)
        # print(f"DEBUG: header_text result: {header_text}")  # Debugging line to check header text

        is_dark = self.page.theme_mode == ft.ThemeMode.DARK if hasattr(self.page, 'theme_mode') else False
        
        header = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.WATER_DROP,
                    color=ft.Colors.BLUE_400 if not is_dark else ft.Colors.BLUE_300,
                    size=24
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    header_text,
                    size=self._text_handler.get_size('axis_title') + 2,
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color,
                    font_family="system-ui",
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=16, bottom=12)
        )
        
        # Cache the header and language
        self._cached_header = header
        self._header_language = self._current_language
        
        return header

    def _build_loading_content(self) -> ft.Control:
        """Build loading state content with translations."""
        loading_text = TranslationService.translate_from_dict(
            "precipitation_chart_items", 
            "loading",
            self._current_language
        ) or "Loading precipitation data..."
        
        return ft.Container(
            content=ft.Column([
                ft.ProgressRing(width=50, height=50),
                ft.Container(height=10),
                ft.Text(
                    loading_text,
                    size=self._text_handler.get_size('body'),
                    color=ft.Colors.GREY_600
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            height=200,
            alignment=ft.alignment.center
        )

    def _build_chart_content(self) -> ft.Control:
        """Build the actual precipitation chart."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK if hasattr(self.page, 'theme_mode') else False
        theme = DARK_THEME if is_dark else LIGHT_THEME
        text_color = theme.get("TEXT", ft.Colors.BLACK)
        
        if not self._precipitation_data:
            return self._build_no_data_content()

        # Prepare chart data
        chart_data = self._prepare_chart_data()
        
        # Create chart series (only precipitation, no probability)
        precipitation_series = ft.LineChartData(
            data_points=chart_data["precipitation_points"],
            stroke_width=3,
            color=ft.Colors.BLUE_500,
            curved=True,
            stroke_cap_round=True
        )

        # Create chart with only precipitation data
        chart = ft.LineChart(
            interactive=False,
            data_series=[precipitation_series],  # Only precipitation series
            border=ft.Border(
                bottom=ft.BorderSide(2, ft.Colors.with_opacity(0.2, text_color)),
                left=ft.BorderSide(2, ft.Colors.with_opacity(0.2, text_color))
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.with_opacity(0.1, text_color),
                width=1,
                dash_pattern=[5, 5]
            ),
            vertical_grid_lines=ft.ChartGridLines(
                color=ft.Colors.with_opacity(0.1, text_color),
                width=1,
                dash_pattern=[5, 5]
            ),
            left_axis=ft.ChartAxis(
                title=ft.Text("mm", size=10, color=ft.Colors.with_opacity(0.7, text_color)),
                title_size=40,
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text("Time", size=10, color=ft.Colors.with_opacity(0.7, text_color)),
                title_size=40,
                labels_size=40,
            ),
            tooltip_bgcolor=theme.get("CARD_BACKGROUND", ft.Colors.WHITE),
            min_y=0,
            max_y=max(chart_data["max_precipitation"], 10),
            min_x=0,
            max_x=len(self._precipitation_data) - 1,
            animate=5000,
        )

        return ft.Container(
            content=chart,
            height=200,
            padding=ft.padding.all(10)
        )

    def _build_legend(self) -> ft.Control:
        """Build legend for the chart."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK if hasattr(self.page, 'theme_mode') else False
        theme = DARK_THEME if is_dark else LIGHT_THEME
        text_color = theme.get("TEXT", ft.Colors.BLACK)
        
        # Get translated legend label
        precipitation_label = TranslationService.translate_from_dict(
            "precipitation_chart_items",
            "precipitation_mm",
            self._current_language
        ) or "Precipitation (mm)"

        # Create legend with translations
        return ft.Row([
            ft.Row([
                ft.Container(
                    width=16, height=3,
                    bgcolor=ft.Colors.BLUE_500,
                    border_radius=2
                ),
                ft.Text(precipitation_label, size=10, color=ft.Colors.with_opacity(0.8, text_color))
            ], spacing=8)
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

    def _build_no_data_content(self) -> ft.Control:
        """Build content when no data is available with translations."""
        # Get translated text
        no_data_text = TranslationService.translate_from_dict(
            "precipitation_chart_items",
            "no_data",
            self._current_language
        ) or "No precipitation data available"
        
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.WATER_DROP_OUTLINED, size=48, color=ft.Colors.GREY_400),
                ft.Text(
                    no_data_text,
                    size=self._text_handler.get_size('body'),
                    color=ft.Colors.with_opacity(0.7, self._current_text_color)
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            height=200,
            alignment=ft.alignment.center
        )

    def _prepare_chart_data(self) -> Dict[str, Any]:
        """Prepare data for the chart display."""
        precipitation_points = []
        max_precipitation = 0
        
        for i, data in enumerate(self._precipitation_data):
            # Precipitation amount
            precipitation = data.get('precipitation', 0)
            if precipitation > max_precipitation:
                max_precipitation = precipitation
            
            # Create new instances to force re-rendering
            precipitation_points.append(
                ft.LineChartDataPoint(x=float(i), y=float(precipitation))
            )
        
        return {
            "precipitation_points": precipitation_points,
            "max_precipitation": max_precipitation
        }

    def update_data(self, forecast_data: Dict[str, Any]):
        """
        Update precipitation chart with new forecast data.
        
        Args:
            forecast_data: Weather forecast data containing precipitation info
        """
        try:
            self._forecast_data = forecast_data
            self._precipitation_data = self._extract_precipitation_data(forecast_data)
            
            # Rebuild content
            self.content = self.build()
            
            # Force update with page refresh
            try:
                if self.page:
                    self.update()
                    self.page.update()  # Force page update too
            except AssertionError:
                # Component not yet added to page
                pass
                
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error updating data: {e}")
            # Show no data content on error
            self._precipitation_data = []
            self.content = self.build()
            try:
                self.update()
            except AssertionError:
                pass

    def _extract_precipitation_data(self, forecast_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract precipitation data from forecast data.
        
        Args:
            forecast_data: Raw forecast data
            
        Returns:
            List of precipitation data points
        """
        precipitation_data = []
        
        try:            
            # OpenWeatherMap 5-day forecast structure: forecast_data['list'] contains hourly data
            if 'list' in forecast_data:
                for i, item in enumerate(forecast_data['list'][:24]):  # Next 24 hours
                    precipitation = 0
                    probability = 0
                    
                    # Get precipitation amount (rain or snow)
                    if 'rain' in item:
                        if '3h' in item['rain']:  # OpenWeatherMap uses 3h intervals
                            precipitation = item['rain']['3h']
                        elif '1h' in item['rain']:
                            precipitation = item['rain']['1h']
                    
                    if 'snow' in item:
                        if '3h' in item['snow']:
                            precipitation += item['snow']['3h']  # Add snow to precipitation
                        elif '1h' in item['snow']:
                            precipitation += item['snow']['1h']
                    
                    # Get precipitation probability (if available)
                    if 'pop' in item:
                        probability = item['pop'] * 100  # Convert to percentage
                    else:
                        # Estimate probability based on weather conditions
                        weather_main = item.get('weather', [{}])[0].get('main', '').lower()
                        if 'rain' in weather_main or 'drizzle' in weather_main:
                            probability = 80
                        elif 'snow' in weather_main:
                            probability = 90
                        elif 'cloud' in weather_main:
                            probability = 30
                        else:
                            probability = 10
                    
                    # Get time
                    timestamp = item.get('dt', 0)
                    
                    precipitation_data.append({
                        'time': timestamp,
                        'precipitation': precipitation,
                        'probability': probability
                    })
                
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error extracting precipitation data: {e}")
            
            # Fallback sample data on error
            import time
            current_time = int(time.time())
            precipitation_data = []
            for i in range(8):  # 8 hours of fallback data
                precipitation_data.append({
                    'time': current_time + (i * 3600),
                    'precipitation': 3 + i * 0.5,  # Increasing precipitation
                    'probability': 20 + i * 10  # Increasing probability
                })
        
        return precipitation_data

    def will_unmount(self):
        """Cleanup method called when component is removed."""
        try:
            if self._state_manager:
                # Unregister observers if needed
                pass
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error during cleanup: {e}")

    def _safe_language_update(self, e=None):
        """Safely handle language change event."""
        if self.page and hasattr(self.page, 'run_task'):
            self.page.run_task(self.update_ui, e)
    
    def _safe_unit_update(self, e=None):
        """Safely handle unit change event."""
        if self.page and hasattr(self.page, 'run_task'):
            self.page.run_task(self.update_ui, e)
    
    def _safe_theme_update(self, e=None):
        """Safely handle theme change event."""
        if self.page and hasattr(self.page, 'run_task'):
            self.page.run_task(self.update_ui, e)
