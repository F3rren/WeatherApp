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
        self._language = DEFAULT_LANGUAGE
        self._unit_system = DEFAULT_UNIT_SYSTEM
        self._precipitation_data = []
        self._forecast_data = {}
        
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
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Register for events
        if self._state_manager:
            self._state_manager.register_observer("language_event", lambda e=None: self.page.run_task(self._update_ui, e))
            self._state_manager.register_observer("unit_event", lambda e=None: self.page.run_task(self._update_ui, e))
            self._state_manager.register_observer("theme_event", lambda e=None: self.page.run_task(self._update_ui, e))
        
        # Set up page resize handler
        if self.page:
            original_on_resize = self.page.on_resize
            def resize_handler(e):
                if original_on_resize:
                    original_on_resize(e)
                if self._text_handler:
                    self._text_handler.handle_resize()
                self.page.run_task(self._update_chart_layout)
            self.page.on_resize = resize_handler
        
        # Initialize content
        self.content = self._build_loading_content()
        self.padding = 16
        self.border_radius = 12
        self.animate = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        
        # Apply initial theme
        self._apply_theme()

    def _apply_theme(self):
        """Apply current theme colors."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK if self.page else False
        theme = DARK_THEME if is_dark else LIGHT_THEME
        
        self.bgcolor = theme.get("CHART", ft.Colors.WHITE)
        self.border = ft.border.all(
            1, 
            ft.Colors.with_opacity(0.1, theme.get("TEXT", ft.Colors.BLACK))
        )

    def _build_loading_content(self) -> ft.Control:
        """Build loading state content with translations."""
        # Get translation service
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        # Get translated strings
        title_text = "Precipitation Forecast"
        loading_text = "Loading precipitation data..."
        
        if translation_service:
            title_text = translation_service.translate_from_dict(
                "precipitation_chart_items", 
                "precipitation_chart_title",
                self._language
            ) or title_text
            
            loading_text = translation_service.translate_from_dict(
                "precipitation_chart_items", 
                "loading",
                self._language
            ) or loading_text
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.WATER_DROP, size=24, color=ft.Colors.BLUE_400),
                    ft.Text(
                        title_text,
                        size=self._text_handler.get_size('title'),
                        weight=ft.FontWeight.BOLD
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=20),
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
            height=300,
            alignment=ft.alignment.center
        )

    def _build_chart_content(self) -> ft.Control:
        """Build the actual precipitation chart."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK if self.page else False
        theme = DARK_THEME if is_dark else LIGHT_THEME
        text_color = theme.get("TEXT", ft.Colors.BLACK)
        
        # Get translation service
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        # Get translated title
        title_text = "Precipitation Forecast"
        if translation_service:
            title_text = translation_service.translate_from_dict(
                "precipitation_chart_items", 
                "precipitation_chart_title",
                self._language
            ) or title_text

        # Get translated labels
        precipitation_unit = "mm"  # Precipitation is typically always in mm
        time_label = "Time"
        
        if translation_service:
            # We could add translations for "Time" if needed
            pass
        
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
                title=ft.Text(precipitation_unit, size=10, color=ft.Colors.with_opacity(0.7, text_color)),
                title_size=40,
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text(time_label, size=10, color=ft.Colors.with_opacity(0.7, text_color)),
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

        # Get translated legend label
        precipitation_label = "Precipitation (mm)"
        if translation_service:
            precipitation_label = translation_service.translate_from_dict(
                "precipitation_chart_items",
                "precipitation_mm",
                self._language
            ) or precipitation_label

        # Create legend (only precipitation) with translations
        legend = ft.Row([
            ft.Row([
                ft.Container(
                    width=16, height=3,
                    bgcolor=ft.Colors.BLUE_500,
                    border_radius=2
                ),
                ft.Text(precipitation_label, size=10, color=ft.Colors.with_opacity(0.8, text_color))
            ], spacing=8)
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        return ft.Column([
            # Header
            ft.Row([
                ft.Icon(ft.Icons.WATER_DROP, size=20, color=ft.Colors.BLUE_400),
                ft.Text(
                    title_text,
                    size=self._text_handler.get_size('title'),
                    weight=ft.FontWeight.BOLD,
                    color=text_color
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Container(height=10),
            
            # Chart
            ft.Container(
                content=chart,
                height=200,
                padding=ft.padding.all(10)
            ),
            
            ft.Container(height=5),
            
            # Legend
            legend
        ], spacing=5)

    def _build_no_data_content(self) -> ft.Control:
        """Build content when no data is available with translations."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK if self.page else False
        theme = DARK_THEME if is_dark else LIGHT_THEME
        text_color = theme.get("TEXT", ft.Colors.BLACK)
        
        # Get translation service
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        # Get translated text
        no_data_text = "No precipitation data available"
        if translation_service:
            no_data_text = translation_service.translate_from_dict(
                "precipitation_chart_items",
                "no_data",
                self._language
            ) or no_data_text
        
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.WATER_DROP_OUTLINED, size=48, color=ft.Colors.GREY_400),
                ft.Text(
                    no_data_text,
                    size=self._text_handler.get_size('body'),
                    color=ft.Colors.with_opacity(0.7, text_color)
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
        
        print(f"DEBUG: Prepared chart data - {len(precipitation_points)} precipitation points, max: {max_precipitation}")
        
        return {
            "precipitation_points": precipitation_points,
            "max_precipitation": max_precipitation
        }

    async def _update_ui(self, event_data=None):
        """Update UI based on language, unit, or theme changes."""
        if not self.page or not self.visible:
            return
        
        try:
            data_needs_refresh = False
            
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._language
                new_unit_system = self._state_manager.get_state('unit') or self._unit_system
                
                # Check if data needs to be refreshed
                if new_unit_system != self._unit_system:
                    data_needs_refresh = True
                
                self._language = new_language
                self._unit_system = new_unit_system
            
            # Apply current theme
            self._apply_theme()
            
            # Refresh data if units changed
            if data_needs_refresh and hasattr(self, '_forecast_data') and self._forecast_data:
                # Re-process existing forecast data with new units
                self.update_data(self._forecast_data)
            else:
                # Just rebuild UI with current data
                if self._precipitation_data:
                    self.content = self._build_chart_content()
                else:
                    self.content = self._build_loading_content()
                
                try:
                    self.update()
                except AssertionError:
                    # Component not yet added to page
                    pass
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error updating UI: {e}")

    async def _update_chart_layout(self):
        """Update chart layout for responsive design."""
        if not self.page or not self.visible:
            return
        
        try:
            if self._precipitation_data:
                self.content = self._build_chart_content()
                try:
                    self.update()
                except AssertionError:
                    pass
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error updating chart layout: {e}")

    def update_data(self, forecast_data: Dict[str, Any]):
        """
        Update precipitation chart with new forecast data.
        
        Args:
            forecast_data: Weather forecast data containing precipitation info
        """
        try:
            print(f"DEBUG: PrecipitationChart received forecast_data keys: {list(forecast_data.keys()) if forecast_data else 'None'}")
            self._forecast_data = forecast_data
            old_data_count = len(self._precipitation_data) if self._precipitation_data else 0
            self._precipitation_data = self._extract_precipitation_data(forecast_data)
            new_data_count = len(self._precipitation_data) if self._precipitation_data else 0
            print(f"DEBUG: Precipitation data changed from {old_data_count} to {new_data_count} points")
            
            # Force rebuild of content
            if self._precipitation_data:
                print(f"DEBUG: Building chart with first 3 data points: {self._precipitation_data[:3] if len(self._precipitation_data) >= 3 else self._precipitation_data}")
                self.content = self._build_chart_content()
                print("DEBUG: Built chart content with data")
            else:
                self.content = self._build_no_data_content()
                print("DEBUG: Built no-data content")
            
            # Force update with page refresh
            try:
                if self.page:
                    self.update()
                    self.page.update()  # Force page update too
                    print("DEBUG: Updated chart container and page")
            except AssertionError:
                # Component not yet added to page
                print("DEBUG: Chart container not yet added to page")
                pass
                
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error updating data: {e}")
            print(f"DEBUG: Exception in update_data: {e}")
            # Show no data content on error
            self.content = self._build_no_data_content()
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
            print(f"DEBUG: Forecast data structure: {list(forecast_data.keys()) if forecast_data else 'None'}")
            
            # OpenWeatherMap 5-day forecast structure: forecast_data['list'] contains hourly data
            if 'list' in forecast_data:
                print(f"DEBUG: Found 'list' with {len(forecast_data['list'])} items")
                
                for i, item in enumerate(forecast_data['list'][:24]):  # Next 24 hours
                    precipitation = 0
                    probability = 0
                    
                    # Get precipitation amount (rain or snow)
                    if 'rain' in item:
                        if '3h' in item['rain']:  # OpenWeatherMap uses 3h intervals
                            precipitation = item['rain']['3h']
                        elif '1h' in item['rain']:
                            precipitation = item['rain']['1h']
                        print(f"DEBUG: Item {i} rain: {precipitation}mm")
                    
                    if 'snow' in item:
                        if '3h' in item['snow']:
                            precipitation += item['snow']['3h']  # Add snow to precipitation
                        elif '1h' in item['snow']:
                            precipitation += item['snow']['1h']
                        print(f"DEBUG: Item {i} snow: {precipitation}mm")
                    
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
                    
                    print(f"DEBUG: Item {i}: precipitation={precipitation}, probability={probability}")
            
            print(f"DEBUG: Real precipitation data extracted: {len(precipitation_data)} items")
                
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error extracting precipitation data: {e}")
            print(f"DEBUG: Exception in _extract_precipitation_data: {e}")
            import traceback
            traceback.print_exc()
            
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
        
        print(f"DEBUG: Final precipitation_data length: {len(precipitation_data)}")
        return precipitation_data

    def will_unmount(self):
        """Cleanup method called when component is removed."""
        try:
            if self._state_manager:
                # Unregister observers if needed
                pass
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error during cleanup: {e}")
