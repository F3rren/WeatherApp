import flet as ft
from datetime import datetime
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.api_service import ApiService
import logging
import asyncio
import traceback

class HourlyForecastDisplay(ft.Container):
    """
    Manages the display of the entire hourly forecast section.
    """
    def __init__(self, city: str, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self._city = city
        self.page = page
        self._api_service = ApiService()
        self._hourly_data_list = []
        
        self._state_manager = None
        self._language = DEFAULT_LANGUAGE
        self._unit_system = DEFAULT_UNIT_SYSTEM
        self._text_color = LIGHT_THEME["TEXT"]

        self.expand = True 

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={'icon': 60, 'time': 20, 'temp': 25},
            breakpoints=[600, 900, 1200, 1600]
        )

        if self.page:
            if hasattr(self.page, 'session') and self.page.session.get('state_manager'):
                self._state_manager = self.page.session.get('state_manager')
                self._state_manager.register_observer("language_event", lambda e=None: self.page.run_task(self.update_ui, e))
                self._state_manager.register_observer("unit_event", lambda e=None: self.page.run_task(self.update_ui, e))
                self._state_manager.register_observer("theme_event", lambda e=None: self.page.run_task(self.update_ui, e))

            original_on_resize = self.page.on_resize
            def resize_handler(e):
                if original_on_resize:
                    original_on_resize(e)
                if self.text_handler:
                    self.text_handler._handle_resize(e)
                if self.page:
                    self.page.run_task(self.update_ui)
            self.page.on_resize = resize_handler

        self.content = self.build()
        if self.page:
            self.page.run_task(self.update_ui)

    async def update_ui(self, event_data=None):
        """Updates the UI based on state changes, fetching new data if necessary."""
        if not self.page or not self.visible:
            return

        try:
            data_changed = False
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._language
                new_unit_system = self._state_manager.get_state('unit') or self._unit_system
                
                language_changed = self._language != new_language
                unit_changed = self._unit_system != new_unit_system

                self._language = new_language
                self._unit_system = new_unit_system
                
                data_changed = language_changed or unit_changed

            if not self._hourly_data_list or data_changed:
                weather_data = await asyncio.to_thread(
                    self._api_service.get_weather_data,
                    city=self._city, language=self._language, unit=self._unit_system
                )
                if weather_data:
                    # Get exactly 24 hours of data and then limit to 24 in the display
                    all_hourly_data = self._api_service.get_hourly_forecast_data(weather_data, hours=40)  # Get more data
                    self._hourly_data_list = all_hourly_data[:24]  # But use only first 24 hours

            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            self.update()
        except Exception as e:
            logging.error(f"HourlyForecastDisplay: Error updating UI: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs a clean, minimal UI for the hourly forecast exactly like the design shown."""
        if not self._hourly_data_list:
            # Get translation service for loading message
            translation_service = None
            if self.page and hasattr(self.page, 'session'):
                translation_service = self.page.session.get('translation_service')
            
            loading_text = "Loading 24-hour forecast..."
            if translation_service:
                loading_text = translation_service.translate_from_dict(
                    "hourly_forecast_items", 
                    "loading_forecast",
                    self._language
                ) or loading_text
            
            return ft.Container(
                content=ft.Text(
                    loading_text,
                    size=16,
                    color=self._text_color
                ),
                padding=ft.padding.all(20)
            )

        # Get translation service for header
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        header_text = "Hourly Forecast"
        if translation_service:
            header_text = translation_service.translate_from_dict(
                "hourly_forecast_items", 
                "hourly_forecast",
                self._language
            ) or header_text

        # Professional header with enhanced typography and subtle accent
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        header = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.TIMELINE,
                    color=ft.Colors.GREEN_400 if not is_dark else ft.Colors.GREEN_300,
                    size=24
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    header_text,
                    size=self.text_handler.get_size('axis_title') + 2,
                    weight=ft.FontWeight.BOLD,
                    color=self._text_color,
                    font_family="system-ui",
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=24, bottom=20)
        )

        forecast_item_controls = []
        
        # Show only first 8 hours for cleaner display
        for index, item_data in enumerate(self._hourly_data_list[:8]):  # Limit to 8 hours for better UX
            try:
                # Format time to show only hour (like "12", "15", "18", etc.)
                hour = datetime.strptime(item_data["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%H")
                icon_code = item_data["weather"][0]["icon"]
                temp_value = round(item_data["main"]["temp"])
                
                # Extract additional weather data
                feels_like = round(item_data["main"]["feels_like"])
                humidity = item_data["main"]["humidity"]
                rain_probability = round(item_data.get("pop", 0) * 100)  # Probability of precipitation in %
                
                # Determine icon color and style based on weather condition
                is_day = icon_code.endswith('d')
                is_sunny = icon_code.startswith('01')  # Clear sky
                is_cloudy = icon_code.startswith(('02', '03', '04'))  # Clouds
                is_rain = icon_code.startswith(('09', '10'))  # Rain
                is_storm = icon_code.startswith('11')  # Thunderstorm
                is_snow = icon_code.startswith('13')  # Snow
                
                # Create beautiful weather icons with better proportions
                if is_sunny and is_day:
                    weather_icon = ft.Container(
                        width=32,  # Slightly smaller for better spacing
                        height=32,
                        border_radius=16,
                        bgcolor=ft.Colors.AMBER_400,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=6,
                            color=ft.Colors.with_opacity(0.3, ft.Colors.AMBER_300),
                            offset=ft.Offset(0, 2),
                        ),
                        content=ft.Icon(
                            ft.Icons.WB_SUNNY,
                            color=ft.Colors.WHITE,
                            size=18,  # Smaller icon to fit better
                        ),
                        alignment=ft.alignment.center,
                    )
                elif is_rain:
                    weather_icon = ft.Container(
                        width=32,
                        height=32,
                        border_radius=16,
                        bgcolor=ft.Colors.BLUE_500,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=6,
                            color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_300),
                            offset=ft.Offset(0, 2),
                        ),
                        content=ft.Icon(
                            ft.Icons.WATER_DROP,
                            color=ft.Colors.WHITE,
                            size=18,
                        ),
                        alignment=ft.alignment.center,
                    )
                elif is_storm:
                    weather_icon = ft.Container(
                        width=32,
                        height=32,
                        border_radius=16,
                        bgcolor=ft.Colors.PURPLE_600,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=6,
                            color=ft.Colors.with_opacity(0.3, ft.Colors.PURPLE_400),
                            offset=ft.Offset(0, 2),
                        ),
                        content=ft.Icon(
                            ft.Icons.FLASH_ON,
                            color=ft.Colors.WHITE,
                            size=18,
                        ),
                        alignment=ft.alignment.center,
                    )
                elif is_snow:
                    weather_icon = ft.Container(
                        width=32,
                        height=32,
                        border_radius=16,
                        bgcolor=ft.Colors.LIGHT_BLUE_300,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=6,
                            color=ft.Colors.with_opacity(0.3, ft.Colors.LIGHT_BLUE_200),
                            offset=ft.Offset(0, 2),
                        ),
                        content=ft.Icon(
                            ft.Icons.AC_UNIT,
                            color=ft.Colors.BLUE_800,
                            size=18,
                        ),
                        alignment=ft.alignment.center,
                    )
                elif is_cloudy:
                    weather_icon = ft.Container(
                        width=32,
                        height=32,
                        border_radius=16,
                        bgcolor=ft.Colors.GREY_500 if is_day else ft.Colors.BLUE_GREY_700,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=6,
                            color=ft.Colors.with_opacity(0.25, ft.Colors.GREY_400 if is_day else ft.Colors.BLUE_GREY_500),
                            offset=ft.Offset(0, 2),
                        ),
                        content=ft.Icon(
                            ft.Icons.CLOUD,
                            color=ft.Colors.WHITE,
                            size=18,
                        ),
                        alignment=ft.alignment.center,
                    )
                else:  # Night or other conditions
                    weather_icon = ft.Container(
                        width=32,
                        height=32,
                        border_radius=16,
                        bgcolor=ft.Colors.INDIGO_600 if not is_day else ft.Colors.ORANGE_300,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=6,
                            color=ft.Colors.with_opacity(0.3, ft.Colors.INDIGO_300 if not is_day else ft.Colors.ORANGE_200),
                            offset=ft.Offset(0, 2),
                        ),
                        content=ft.Icon(
                            ft.Icons.NIGHTLIGHT_ROUND if not is_day else ft.Icons.WB_SUNNY,
                            color=ft.Colors.WHITE,
                            size=18,
                        ),
                        alignment=ft.alignment.center,
                    )
                
                # Professional hour display with better typography
                time_text = ft.Text(
                    hour,
                    size=14,
                    color=ft.Colors.with_opacity(0.7, self._text_color),
                    weight="w500",
                    text_align=ft.TextAlign.CENTER,
                    font_family="system-ui",
                )
                
                # Professional temperature display with emphasis
                temp_text = ft.Text(
                    f"{temp_value}°",
                    size=16,
                    weight="w600",
                    color=self._text_color,
                    text_align=ft.TextAlign.CENTER,
                    font_family="system-ui",
                )
                
                # Additional weather info display
                # Rain probability (only show if > 0)
                rain_info = None
                if rain_probability > 0:
                    rain_info = ft.Container(
                        content=ft.Row([
                            ft.Icon(
                                ft.Icons.WATER_DROP,
                                size=10,
                                color=ft.Colors.BLUE_400,
                            ),
                            ft.Text(
                                f"{rain_probability}%",
                                size=10,
                                color=ft.Colors.BLUE_400,
                                weight="w500",
                            )
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                        height=14,
                        alignment=ft.alignment.center,
                    )
                
                # Humidity info
                humidity_info = ft.Container(
                    content=ft.Row([
                        ft.Icon(
                            ft.Icons.OPACITY,
                            size=10,
                            color=ft.Colors.CYAN_400,
                        ),
                        ft.Text(
                            f"{humidity}%",
                            size=10,
                            color=ft.Colors.CYAN_400,
                            weight="w500",
                        )
                    ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                    height=14,
                    alignment=ft.alignment.center,
                )
                
                # Feels like temperature (only show if different from actual temp)
                feels_like_info = None
                if abs(feels_like - temp_value) > 2:  # Show only if difference is significant
                    feels_like_info = ft.Container(
                        content=ft.Text(
                            f"↸{feels_like}°",
                            size=10,
                            color=ft.Colors.ORANGE_400,
                            weight="w500",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        height=14,
                        alignment=ft.alignment.center,
                    )

                # Professional layout with optimized spacing and hierarchy
                controls_list = [
                    ft.Container(
                        content=time_text,
                        height=20,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=4),  # Spacer
                    ft.Container(
                        content=weather_icon,
                        height=36,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=4),  # Spacer
                    ft.Container(
                        content=temp_text,
                        height=20,
                        alignment=ft.alignment.center,
                    ),
                ]
                
                # Add additional info only if available
                if rain_info:
                    controls_list.extend([
                        ft.Container(height=2),
                        rain_info
                    ])
                
                controls_list.extend([
                    ft.Container(height=2),
                    humidity_info
                ])
                
                if feels_like_info:
                    controls_list.extend([
                        ft.Container(height=2),
                        feels_like_info
                    ])
                
                item_column = ft.Column(
                    controls=controls_list,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,  # Use container heights instead
                )
                
                # Professional container with subtle design elements
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
                
                # Determine if this is current hour for special styling
                current_hour = datetime.now().strftime("%H")
                is_current = hour == current_hour
                
                item_container = ft.Container(
                    content=item_column,
                    padding=ft.padding.symmetric(horizontal=12, vertical=16),
                    width=85,
                    height=155,  # Increased height to accommodate additional info
                    alignment=ft.alignment.center,
                    border_radius=20,
                    bgcolor=ft.Colors.BLUE_50 if is_current and not is_dark else 
                           ft.Colors.BLUE_GREY_900 if is_current and is_dark else
                           ft.Colors.with_opacity(0.03, ft.Colors.WHITE if not is_dark else ft.Colors.BLACK),
                    border=ft.border.all(
                        1.5 if is_current else 1, 
                        ft.Colors.BLUE_200 if is_current and not is_dark else
                        ft.Colors.BLUE_400 if is_current and is_dark else
                        ft.Colors.with_opacity(0.08, ft.Colors.GREY_400 if not is_dark else ft.Colors.GREY_600)
                    ),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                )
                forecast_item_controls.append(item_container)
                
            except Exception as e:
                logging.error(f"Error processing hourly item: {item_data}, Error: {e}")

        # Professional horizontal scroll with enhanced spacing
        hourly_row = ft.Container(
            content=ft.Row(
                controls=forecast_item_controls,
                alignment=ft.MainAxisAlignment.START,
                spacing=16,  # More generous spacing for professional look
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=16),
        )

        return ft.Container(
            content=ft.Column([
                header,
                hourly_row,
            ], spacing=8),
            padding=ft.padding.only(bottom=24),
            # Optional: Add subtle background to entire section
            bgcolor=ft.Colors.with_opacity(0.01, ft.Colors.WHITE if not is_dark else ft.Colors.BLACK),
            border_radius=ft.border_radius.only(
                top_left=16,
                top_right=16,
                bottom_left=16,
                bottom_right=16,
            ),
        )
    
    def update_city(self, new_city: str):
        """Allows updating the city and refreshing the forecast."""
        if self._city != new_city:
            self._city = new_city
            self._hourly_data_list = []
            if self.page:
                self.page.run_task(self.update_ui)

