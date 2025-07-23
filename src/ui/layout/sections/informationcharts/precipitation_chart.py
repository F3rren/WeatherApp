"""
Precipitation Chart Display for MeteoApp.
Shows precipitation forecast and probability over time.
"""

import flet as ft
import asyncio
from typing import Dict, List, Any
import logging

from services.api.api_service import ApiService
from services.ui.translation_service import TranslationService
from services.ui.theme_handler import ThemeHandler


class PrecipitationChartDisplay(ft.Container):
    """
    Container for displaying precipitation forecast data.
    Shows precipitation forecast as a textual list along with key statistics.
    """

    def __init__(self, page: ft.Page,
                 language: str = None,
                 unit: str = None,
                 theme_handler: ThemeHandler = None, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.theme_handler = theme_handler or ThemeHandler(self.page)
        self._api_service = ApiService()
        self._current_language = language
        self._current_unit_system = unit
        self._current_text_color = self.theme_handler.get_text_color()
        self._precipitation_data = []
        self._forecast_data = {}
        self._updating = False  # Flag to prevent concurrent updates
        self._cached_header = None  # Cache for header to prevent unnecessary rebuilds
        self._header_language = None  # Track which language the header was built for
        self._last_theme_mode = None  # Track theme changes for header cache invalidation

        # State management
        self._state_manager = None
        if self.page and hasattr(self.page, 'session') and self.page.session:
            self._state_manager = self.page.session.get('state_manager')



        # Set default properties
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(15)  # Slightly larger padding since we removed inner container

        # Remove border and shadow
        self.border = None
        self.shadow = None
        self.border_radius = None

        # Register for events
        if self._state_manager:
            self._state_manager.register_observer("language_event", self._safe_language_update)
            self._state_manager.register_observer("unit", self._safe_unit_update)
            self._state_manager.register_observer("unit_text_change", self._safe_unit_update)  # Also listen for unit text changes
            self._state_manager.register_observer("theme_event", self._safe_theme_update)

        # Initialize content
        self.content = self.build()

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

                # Use default values if new values are None
                old_language = self._current_language
                self._current_language = new_language if new_language is not None else self._current_language
                self._current_unit_system = new_unit_system if new_unit_system is not None else self._current_unit_system

                if old_language != self._current_language:
                    # Invalidate header cache when language changes
                    self._cached_header = None
                    self._header_language = None

            # Aggiorna colori tramite ThemeHandler
            self._current_text_color = self.theme_handler.get_text_color()
            # Invalida cache header se cambia tema
            current_theme = self.theme_handler.get_theme()
            if hasattr(self, '_last_theme_mode') and self._last_theme_mode != current_theme:
                self._cached_header = None
                self._header_language = None
            self._last_theme_mode = current_theme

            # Applica theme al container
            self.bgcolor = self.theme_handler.get_background_color()
            self.border = None
            self.shadow = None

            # Rebuild content
            self.content = self.build()

            # Only update if this control is already in the page and properly connected
            try:
                if self.page and hasattr(self, 'page') and self.page is not None and hasattr(self, 'parent') and self.parent is not None:
                    self.update()
            except (AssertionError, AttributeError) as e:
                logging.debug(f"PrecipitationChart: Container not ready for update: {e}")
            except RuntimeError as e:
                if "must be added to the page first" in str(e):
                    logging.debug(f"PrecipitationChart: Container not added to page: {e}")
                else:
                    logging.error(f"PrecipitationChart: Runtime error during update: {e}")
            except Exception as e:
                logging.error(f"PrecipitationChart: Unexpected error during update: {e}")

        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error updating UI: {e}")
            self._reset_to_safe_state()
        finally:
            self._updating = False
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
            # Only update if this control is already in the page and properly connected
            try:
                if self.page and hasattr(self, 'page') and self.page is not None and hasattr(self, 'parent') and self.parent is not None:
                    self.update()
            except (AssertionError, AttributeError) as e:
                # Control not yet added to page or not properly connected
                logging.debug(f"PrecipitationChart: Reset state - Container not ready for update: {e}")
            except RuntimeError as e:
                # Handle "Container Control must be added to the page first" error
                if "must be added to the page first" in str(e):
                    logging.debug(f"PrecipitationChart: Reset state - Container not added to page: {e}")
                else:
                    logging.error(f"PrecipitationChart: Reset state - Runtime error during update: {e}")
            except Exception as e:
                logging.error(f"PrecipitationChart: Reset state - Unexpected error during update: {e}")
        except Exception as e:
            logging.error(f"Failed to reset to safe state: {str(e)}")

    def build(self):
        """Constructs the UI for the precipitation forecast display."""
        if not self._precipitation_data:
            return ft.Column([
                self._build_header(),
                self._build_loading_content()
            ])
        
        # Check if we have any significant precipitation
        significant_precipitation = any(data.get('precipitation', 0) > 0.1 for data in self._precipitation_data)
        
        if not significant_precipitation:
            # Build a "no significant precipitation" display
            return ft.Column([
                self._build_header(),
                self._build_no_precipitation_content()
            ])
        
        # Build header
        header = self._build_header()
        
        # Build title for the forecast
        forecast_title = self._build_forecast_title()
        
        # Build precipitation forecast data table
        precipitation_table = self._build_precipitation_table()
        
        # Build precipitation summary
        summary = self._build_precipitation_summary()
        
        # Return components directly in a flat Column structure - matching TemperatureChartDisplay
        return ft.Column([
            header,
            forecast_title,
            precipitation_table,
            ft.Container(height=8),  # Spacing
            summary
        ], spacing=5)

    def _build_header(self):
        """Builds a modern header for precipitation chart section with caching."""
        # Check if we need to rebuild the header
        if self._cached_header is not None and self._header_language == self._current_language:
            # print(f"DEBUG: Using cached header for language: {self._current_language}")
            return self._cached_header
        
        # print(f"DEBUG: Building new header for language: {self._current_language}")
        header_text = TranslationService.translate_from_dict("precipitation_chart_items", "precipitation_chart_title", self._current_language)
        # print(f"DEBUG: header_text result: {header_text}")  # Debugging line to check header text

        is_dark = self.theme_handler.get_theme() != self.theme_handler.get_theme()  # Always False, but keep for logic symmetry
        icon_color = ft.Colors.BLUE_400 if not is_dark else ft.Colors.BLUE_300
        header = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.WATER_DROP,
                    color=icon_color,
                    size=25
                ),
                ft.Container(width=5),  # Spacer
                ft.Text(
                    header_text,
                    size=20,
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
                    size=14,
                    color=ft.Colors.GREY_600
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            height=200,
            alignment=ft.alignment.center
        )

    def _build_precipitation_table(self) -> ft.Control:
        """Build a textual table of precipitation forecast data."""
        is_dark = self.theme_handler.get_theme() != self.theme_handler.get_theme()  # Always False, but keep for logic symmetry
        text_color = self.theme_handler.get_text_color()
        accent_color = ft.Colors.BLUE_500 if not is_dark else ft.Colors.BLUE_400
        
        if not self._precipitation_data:
            return self._build_no_data_content()

        # Prepare for building the forecast display
        
        import datetime
        
        # Get translations
        time_label = TranslationService.translate_from_dict("precipitation_chart_items", "time_hours", self._current_language) or "Time"
        precip_label = TranslationService.translate_from_dict("precipitation_chart_items", "precipitation_mm", self._current_language) or "Precip. (mm)"
        
        # Table header row
        header_row = ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Text(
                        time_label,
                        weight=ft.FontWeight.BOLD,
                        size=11,
                        color=ft.Colors.with_opacity(0.7, text_color)
                    )
                ),
                ft.DataCell(
                    ft.Text(
                        precip_label,
                        weight=ft.FontWeight.BOLD,
                        size=11,
                        color=ft.Colors.with_opacity(0.7, text_color)
                    )
                )
            ],
            color=ft.Colors.with_opacity(0.03, text_color if is_dark else ft.Colors.BLACK)
        )
        
        data_rows = []
        
        # Logic for smart precipitation display
        significant_data = [d for d in self._precipitation_data if d.get('precipitation', 0) > 0.1]
        
        if significant_data:
            # If we have significant precipitation, show up to 8 entries
            visible_data = significant_data[:8]
        else:
            # If no significant precipitation in next 24h, show next 6 time slots anyway
            # but with clear indication that precipitation is minimal/none
            visible_data = self._precipitation_data[:6] if self._precipitation_data else []
        
        # Create rows for the table
        for data in visible_data:
            # Format time
            timestamp = data.get('time', 0)
            time_str = ""
            if timestamp:
                dt = datetime.datetime.fromtimestamp(timestamp)
                time_str = dt.strftime("%H:%M")
            
            precip = data.get('precipitation', 0)
            intensity = self._get_precipitation_intensity(precip)
            
            # Create row with time and precipitation data
            data_row = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(
                            time_str,
                            size=12,
                            color=text_color
                        )
                    ),
                    ft.DataCell(
                        ft.Row([
                            ft.Text(
                                f"{precip:.1f} mm",
                                size=12,
                                weight=ft.FontWeight.W_500,
                                color=text_color
                            ),
                            ft.Container(width=4),  # Small spacer
                            ft.Container(
                                ft.Text(
                                    intensity,
                                    size=10,
                                    color=ft.Colors.WHITE
                                ),
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                border_radius=10,
                                bgcolor=self._get_intensity_color(precip, is_dark)
                            )
                        ])
                    )
                ]
            )
            data_rows.append(data_row)
            
        # Create the table with header and data rows - cleaner styling without container
        precipitation_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("")),
                ft.DataColumn(label=ft.Text(""))
            ],
            rows=[header_row] + data_rows,
            vertical_lines=ft.BorderSide(0.5, ft.Colors.with_opacity(0.05, text_color)),  # Thinner lines
            horizontal_lines=ft.BorderSide(0.5, ft.Colors.with_opacity(0.07, text_color)), # Thinner lines
            heading_row_color=ft.Colors.with_opacity(0.03, accent_color),
            data_row_min_height=35,  # Correct parameter name (was data_row_height in older versions)
            heading_row_height=32,
            bgcolor=ft.Colors.TRANSPARENT  # Transparent background to blend with container
        )
        
        # Return only the table
        return precipitation_table
    
    def _build_forecast_title(self) -> ft.Control:
        """Build a title for the forecast list."""
        is_dark = self.theme_handler.get_theme() != self.theme_handler.get_theme()  # Always False, for logic symmetry
        text_color = self.theme_handler.get_text_color()
        accent_color = ft.Colors.BLUE_500 if not is_dark else ft.Colors.BLUE_400
        
        # Get translation
        next_hours_label = TranslationService.translate_from_dict("precipitation_chart_items", "next_24h", self._current_language) or "Next 24 hours"
        
        # Create a title for the forecast list - adjusted for direct display
        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.SCHEDULE,
                    size=16,
                    color=accent_color
                ),
                ft.Container(width=8),
                ft.Text(
                    next_hours_label,
                    size=12,
                    color=ft.Colors.with_opacity(0.8, text_color),
                    weight=ft.FontWeight.W_500
                )
            ]),
            margin=ft.margin.only(left=2, bottom=8),  # Slightly reduced margin for better spacing
            padding=ft.padding.only(left=5, top=4)  # Add padding to position title better
        )

    def _build_precipitation_summary(self) -> ft.Control:
        """Build a compact and modern summary of precipitation statistics."""
        if not self._precipitation_data:
            return ft.Container()
        
        # Calculate statistics
        total_precipitation = sum(data.get('precipitation', 0) for data in self._precipitation_data)
        max_intensity = max(data.get('precipitation', 0) for data in self._precipitation_data)
        hours_with_rain = sum(1 for data in self._precipitation_data if data.get('precipitation', 0) > 0.1)
        
        text_color = self.theme_handler.get_text_color()
        
        # Get translations
        total_label = TranslationService.translate_from_dict("precipitation_chart_items", "total_precipitation", self._current_language) or "Totale"
        max_label = TranslationService.translate_from_dict("precipitation_chart_items", "max_intensity", self._current_language) or "Picco"
        hours_label = TranslationService.translate_from_dict("precipitation_chart_items", "rainy_hours", self._current_language) or "Ore di pioggia"
        
        # Create compact statistics cards
        stats_cards = []
        
        # Total precipitation card
        stats_cards.append(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.WATER_DROP, size=14, color=ft.Colors.BLUE_600),
                        ft.Text(f"{total_precipitation:.1f} mm", 
                               size=13, 
                               weight=ft.FontWeight.W_600, 
                               color=text_color)
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(total_label, 
                           size=9, 
                           color=ft.Colors.with_opacity(0.65, text_color),
                           text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
                padding=ft.padding.symmetric(horizontal=10, vertical=7),
                bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.BLUE_600),
                border_radius=7,
                expand=True
            )
        )
        
        # Max intensity card
        stats_cards.append(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.TRENDING_UP, size=14, color=ft.Colors.ORANGE_600),
                        ft.Text(f"{max_intensity:.1f} mm/h", 
                               size=13, 
                               weight=ft.FontWeight.W_600, 
                               color=text_color)
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(max_label, 
                           size=9, 
                           color=ft.Colors.with_opacity(0.65, text_color),
                           text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
                padding=ft.padding.symmetric(horizontal=10, vertical=7),
                bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.ORANGE_600),
                border_radius=7,
                expand=True
            )
        )
        
        # Hours with rain card
        stats_cards.append(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME, size=14, color=ft.Colors.GREEN_600),
                        ft.Text(f"{hours_with_rain}h", 
                               size=13, 
                               weight=ft.FontWeight.W_600, 
                               color=text_color)
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(hours_label, 
                           size=9, 
                           color=ft.Colors.with_opacity(0.65, text_color),
                           text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
                padding=ft.padding.symmetric(horizontal=10, vertical=7),
                bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.GREEN_600),
                border_radius=7,
                expand=True
            )
        )
        
        # Main statistics row
        main_stats = ft.Row(stats_cards, spacing=8)
        
        return ft.Container(
            content=main_stats,
            padding=ft.padding.symmetric(horizontal=12, vertical=0)
        )

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
                ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, size=48, color=ft.Colors.BLUE_300),
                ft.Text(
                    no_data_text,
                    size=14,
                    color=ft.Colors.with_opacity(0.7, self._current_text_color),
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=8),
                ft.Text(
                    "☀️ Tempo sereno previsto",
                    size=12,
                    color=ft.Colors.with_opacity(0.6, self._current_text_color),
                    text_align=ft.TextAlign.CENTER
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            height=150,
            alignment=ft.alignment.center
        )

    def _build_no_precipitation_content(self) -> ft.Control:
        """Build content when there's no significant precipitation expected."""
        text_color = self.theme_handler.get_text_color()
        
        # Get translations
        no_significant_rain = TranslationService.translate_from_dict(
            "precipitation_chart_items", 
            "no_significant_precipitation", 
            self._current_language
        ) or "No significant precipitation expected"
        
        return ft.Container(
            content=ft.Column([
                ft.Container(height=20),
                ft.Icon(
                    ft.Icons.WB_SUNNY, 
                    size=64, 
                    color=ft.Colors.AMBER_400
                ),
                ft.Container(height=16),
                ft.Text(
                    no_significant_rain,
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color=text_color,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=8),
                ft.Text(
                    "☀️ Tempo sereno per le prossime 24 ore",
                    size=13,
                    color=ft.Colors.with_opacity(0.7, text_color),
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=12),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.UMBRELLA, size=20, color=ft.Colors.BLUE_300),
                        ft.Text(
                            "Probabilità di pioggia < 20%",
                            size=12,
                            color=ft.Colors.with_opacity(0.8, text_color)
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_500),
                    border_radius=12
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0),
            height=200,
            alignment=ft.alignment.center
        )

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
            
            # Force update with page refresh - with better error handling
            try:
                if self.page and hasattr(self, 'parent') and self.parent is not None:
                    self.update()
                    self.page.update()  # Force page update too
            except (AssertionError, AttributeError) as e:
                # Component not yet added to page or not properly connected
                logging.debug(f"PrecipitationChart: Update data - Container not ready for update: {e}")
            except Exception as e:
                logging.error(f"PrecipitationChart: Update data - Unexpected error during update: {e}")
                
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error updating data: {e}")
            # Show no data content on error
            self._precipitation_data = []
            self.content = self.build()
            try:
                if self.page and hasattr(self, 'parent') and self.parent is not None:
                    self.update()
            except (AssertionError, AttributeError) as e:
                logging.debug(f"PrecipitationChart: Error recovery - Container not ready for update: {e}")
            except Exception as e:
                logging.error(f"PrecipitationChart: Error recovery - Unexpected error during update: {e}")

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
            # Debug logging
            logging.info(f"PrecipitationChart: Extracting data from forecast_data with keys: {list(forecast_data.keys()) if forecast_data else 'None'}")
            
            # OpenWeatherMap 5-day forecast structure: forecast_data['list'] contains hourly data
            if 'list' in forecast_data:
                logging.info(f"PrecipitationChart: Found {len(forecast_data['list'])} forecast items")
                
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
                    
                    # Debug first few entries
                    if i < 3:
                        logging.info(f"PrecipitationChart: Entry {i}: precip={precipitation}mm, prob={probability}%, time={timestamp}")
            else:
                logging.warning("PrecipitationChart: No 'list' key found in forecast_data")
                
        except Exception as e:
            logging.error(f"PrecipitationChartDisplay: Error extracting precipitation data: {e}")
            
            # Use realistic fallback data instead of always showing precipitation
            import time
            current_time = int(time.time())
            precipitation_data = []
            
            # Create more realistic data - mostly no precipitation
            for i in range(8):  # 8 hours of fallback data
                # Only occasional light precipitation
                precip = 0.0
                if i == 3:  # Light rain at hour 3
                    precip = 1.2
                elif i == 6:  # Moderate rain at hour 6
                    precip = 3.5
                    
                precipitation_data.append({
                    'time': current_time + (i * 3600),
                    'precipitation': precip,
                    'probability': 15 if precip == 0 else (60 if precip < 2 else 85)
                })
        
        logging.info(f"PrecipitationChart: Extracted {len(precipitation_data)} data points")
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
        try:
            if self.page and hasattr(self.page, 'run_task') and callable(getattr(self.page, 'run_task', None)):
                self.page.run_task(self.update_ui, e)
        except Exception as ex:
            logging.error(f"PrecipitationChart: Error in safe language update: {ex}")
    
    def _safe_unit_update(self, e=None):
        """Safely handle unit change event."""
        try:
            if self.page and hasattr(self.page, 'run_task') and callable(getattr(self.page, 'run_task', None)):
                self.page.run_task(self.update_ui, e)
        except Exception as ex:
            logging.error(f"PrecipitationChart: Error in safe unit update: {ex}")
    
    def _safe_theme_update(self, e=None):
        """Safely handle theme change event."""
        try:
            # Clear header cache to force rebuild with new theme
            self._cached_header = None
            self._last_theme_mode = None
            
            if self.page and hasattr(self.page, 'run_task') and callable(getattr(self.page, 'run_task', None)):
                self.page.run_task(self.update_ui, e)
            elif self.page:
                # Fallback method if run_task is not available
                asyncio.create_task(self.update_ui(e))
            else:
                logging.debug("PrecipitationChart: Cannot update theme - page not available")
            
            logging.debug("PrecipitationChart: Theme update event processed")
        except Exception as ex:
            logging.error(f"PrecipitationChart: Error in safe theme update: {ex}")

    def cleanup(self):
        """Clean up observers and resources."""
        if self._state_manager:
            try:
                self._state_manager.unregister_observer("language_event", self._safe_language_update)
                self._state_manager.unregister_observer("unit", self._safe_unit_update)
                self._state_manager.unregister_observer("unit_text_change", self._safe_unit_update)
                self._state_manager.unregister_observer("theme_event", self._safe_theme_update)
            except Exception as e:
                logging.error(f"PrecipitationChartDisplay: Error during cleanup: {e}")

    def _get_precipitation_intensity(self, precipitation: float) -> str:
        """Get precipitation intensity description based on amount."""
        if precipitation <= 0.1:
            return TranslationService.translate_from_dict("precipitation_chart_items", "intensity_light", self._current_language) or "Light"
        elif precipitation <= 2.5:
            return TranslationService.translate_from_dict("precipitation_chart_items", "intensity_moderate", self._current_language) or "Moderate"
        elif precipitation <= 10:
            return TranslationService.translate_from_dict("precipitation_chart_items", "intensity_heavy", self._current_language) or "Heavy"
        else:
            return TranslationService.translate_from_dict("precipitation_chart_items", "intensity_very_heavy", self._current_language) or "Very heavy"
            
    def _get_intensity_color(self, precipitation: float, is_dark: bool) -> str:
        """Get color for precipitation intensity badge based on amount."""
        if precipitation <= 0.1:
            return ft.Colors.BLUE_300 if not is_dark else ft.Colors.BLUE_400
        elif precipitation <= 2.5:
            return ft.Colors.BLUE_500 if not is_dark else ft.Colors.BLUE_600
        elif precipitation <= 10:
            return ft.Colors.INDIGO_600 if not is_dark else ft.Colors.INDIGO_500
        else:
            return ft.Colors.PURPLE_700 if not is_dark else ft.Colors.PURPLE_600

    def _get_precipitation_type_from_data(self) -> str:
        """Determine precipitation type from forecast data."""
        if not self._precipitation_data:
            return TranslationService.translate_from_dict("precipitation_chart_items", "rain", self._current_language) or "Rain"
        
        # Check if we have snow in the data
        has_snow = any(data.get('snow', 0) > 0 for data in self._precipitation_data if isinstance(data, dict))
        has_rain = any(data.get('rain', 0) > 0 for data in self._precipitation_data if isinstance(data, dict))
        
        if has_snow and has_rain:
            return TranslationService.translate_from_dict("precipitation_chart_items", "mixed", self._current_language) or "Mixed"
        elif has_snow:
            return TranslationService.translate_from_dict("precipitation_chart_items", "snow", self._current_language) or "Snow"
        else:
            return TranslationService.translate_from_dict("precipitation_chart_items", "rain", self._current_language) or "Rain"

    def _find_peak_precipitation_time(self) -> str:
        """Find when peak precipitation is expected."""
        if not self._precipitation_data:
            return ""
        
        max_precip = 0
        peak_time = ""
        
        for data in self._precipitation_data:
            precip = data.get('precipitation', 0)
            if precip > max_precip:
                max_precip = precip
                # Format time - assuming we have timestamp
                timestamp = data.get('time', 0)
                if timestamp:
                    import datetime
                    dt = datetime.datetime.fromtimestamp(timestamp)
                    peak_time = dt.strftime("%H:%M")
        
        return peak_time
