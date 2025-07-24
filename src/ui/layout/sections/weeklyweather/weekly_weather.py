import os
import flet as ft
import traceback
import asyncio
import logging
from services.api.api_service import ApiService, load_dotenv
from translations import translation_manager
from services.ui.translation_service import TranslationService  # For unit symbols
from services.ui.theme_handler import ThemeHandler
from utils.responsive_utils import ResponsiveTextFactory

class WeeklyForecastDisplay(ft.Container):
    """
    Displays the weekly weather forecast with modern UI design.
    Fetches data and renders daily forecast items internally.
    """

    def __init__(self, page: ft.Page, city: str, theme_handler: ThemeHandler = None, **kwargs):
        load_dotenv()
        super().__init__()
        self.page = page
        self._city = city
        self._api_service = ApiService()
        self._state_manager = None
        self._current_language = os.getenv("DEFAULT_LANGUAGE")
        self._current_unit_system = os.getenv("DEFAULT_UNIT_SYSTEM")
        self.theme_handler = theme_handler or ThemeHandler(page)
        self._current_text_color = self.theme_handler.get_text_color()
        self._forecast_data = []



        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(0)  # Remove default padding, handled by internal containers
        
        if self.page and hasattr(self.page, 'session') and self.page.session and self.page.session.get('state_manager'):
            try:
                self._state_manager = self.page.session.get('state_manager')
                # Register observers with try-catch protection for each one
                try:
                    self._state_manager.register_observer("language_event", self._safe_language_update)
                except Exception as e:
                    logging.warning(f"WeeklyForecastDisplay: Failed to register language observer: {e}")
                try:
                    self._state_manager.register_observer("unit", self._safe_unit_update)
                except Exception as e:
                    logging.warning(f"WeeklyForecastDisplay: Failed to register unit observer: {e}")
                try:
                    self._state_manager.register_observer("theme_event", self._safe_theme_update)
                except Exception as e:
                    logging.warning(f"WeeklyForecastDisplay: Failed to register theme observer: {e}")
                logging.debug("WeeklyForecastDisplay: Successfully registered state observers")
            except Exception as e:
                logging.error(f"WeeklyForecastDisplay: Error registering observers: {e}")
                self._state_manager = None

        if self.page and hasattr(self.page, "on_resize"):
            original_on_resize = self.page.on_resize
            def resize_handler(e):
                if original_on_resize:
                    original_on_resize(e)
                if self.page:
                    self.page.run_task(self.update_ui)
            self.page.on_resize = resize_handler
        
        self.content = self.build()
        # Schedule async UI update after the component is initialized, but don't block the constructor
        if self.page:
            # Use a small delay to ensure the component is properly added to the page
            def delayed_update():
                try:
                    if self.page and hasattr(self.page, 'run_task'):
                        self.page.run_task(self.update_ui)
                except Exception as e:
                    logging.debug(f"WeeklyForecastDisplay: Failed to schedule initial update: {e}")
            
            # Try to schedule the update, but don't fail if it doesn't work
            try:
                import threading
                timer = threading.Timer(0.1, delayed_update)
                timer.start()
            except Exception:
                pass  # Ignore if threading is not available or fails

    async def update_ui(self, event_data=None):
        """Updates the UI based on state changes, fetching new data if necessary."""
        if not self.page or not self.visible:
            return

        try:
            data_changed = False
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                new_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
                
                lang_changed = self._current_language != new_language
                unit_changed = self._current_unit_system != new_unit_system

                self._current_language = new_language
                self._current_unit_system = new_unit_system
                
                data_changed = lang_changed or unit_changed

            if not self._forecast_data or data_changed:
                if self._city:
                    weather_response = await asyncio.to_thread(
                        self._api_service.get_weather_data,
                        city=self._city, 
                        language=self._current_language, 
                        unit=self._current_unit_system
                    )
                    
                    # Check if API call was successful and extract data
                    if weather_response and weather_response.get('success', False):
                        weather_data_payload = weather_response.get('data', {})
                        self._forecast_data = self._api_service.get_weekly_forecast_data(weather_data_payload) if weather_data_payload else []
                    else:
                        error_info = weather_response.get('error', {}) if weather_response else {}
                        error_message = error_info.get('message', 'Failed to fetch weather data')
                        logging.warning(f"WeeklyWeather: {error_message}")
                        self._forecast_data = []
                else:
                    self._forecast_data = []

            # Safe theme detection with robust checking
            self._current_text_color = self.theme_handler.get_text_color()

            self.content = self.build()
            
            # Robust update logic - check multiple conditions before updating
            can_update = False
            
            # First check - basic page connection
            if self.page and hasattr(self, 'page') and self.page is not None:
                # Second check - check if this control has a parent (is in the widget tree)
                if hasattr(self, 'parent') and self.parent is not None:
                    # Third check - verify the parent is also connected to the page
                    if hasattr(self.parent, 'page') and self.parent.page is not None:
                        can_update = True
                    else:
                        # Alternative check - try to see if we can access page through control hierarchy
                        try:
                            current = self
                            while current and hasattr(current, 'parent') and current.parent:
                                current = current.parent
                                if hasattr(current, 'page') and current.page is not None:
                                    can_update = True
                                    break
                        except Exception:
                            pass
            
            if can_update:
                try:
                    self.update()
                    logging.debug("WeeklyForecastDisplay: Successfully updated UI")
                except (AssertionError, AttributeError) as update_error:
                    # Control not yet fully added to page, this is expected during initialization
                    logging.debug(f"WeeklyForecastDisplay: Skipping update - control not fully initialized: {update_error}")
                except RuntimeError as update_error:
                    # Handle "Container Control must be added to the page first" error
                    if "must be added to the page first" in str(update_error):
                        logging.debug(f"WeeklyForecastDisplay: Skipping update - control not added to page: {update_error}")
                    else:
                        logging.warning(f"WeeklyForecastDisplay: Runtime error during update: {update_error}")
                except Exception as update_error:
                    logging.warning(f"WeeklyForecastDisplay: Unexpected error during update: {update_error}")
            else:
                logging.debug("WeeklyForecastDisplay: Control not ready for update (not properly connected to page)")
                
        except Exception as e:
            # Only log actual errors, not expected initialization issues
            error_msg = str(e)
            if "must be added to the page first" in error_msg:
                logging.debug(f"WeeklyForecastDisplay: Control not ready for update: {e}")
            else:
                logging.error(f"Error updating component WeeklyForecastDisplay: {e}")
            
            # Set fallback content on error only for actual errors
            if "must be added to the page first" not in error_msg:
                try:
                    self.content = ft.Container(
                        content=ResponsiveTextFactory.create_adaptive_text(
                            page=self.page,
                            text="Error loading weekly forecast",
                            text_type="body_primary",
                            color=ft.Colors.RED_400
                        ),
                        alignment=ft.alignment.center,
                        padding=20
                    )
                    # Only try to update if we're connected to the page
                    if self.page and hasattr(self, 'parent') and self.parent is not None:
                        try:
                            self.update()
                        except Exception:
                            pass  # Ignore update errors in fallback
                except Exception:
                    pass  # Ignore errors in fallback

    def build(self):
        """Constructs the modern UI for the weekly forecast with header and styled cards."""
        # Safe theme detection with robust checking
        theme = self.theme_handler.get_theme()
        
        # Header section
        header_text = translation_manager.get_translation("weather", "weekly_forecast_items", "header", self._current_language)
        is_dark = theme == self.theme_handler.get_theme() and theme.get("BACKGROUND", "").lower() == "#0d1117"
        header = ft.Row(
            controls=[
                ft.Icon(
                    name=ft.Icons.CALENDAR_MONTH,
                    size=24,
                    color=ft.Colors.BLUE_400 if not is_dark else ft.Colors.BLUE_300
                ),
                ft.Container(width=5),
                ResponsiveTextFactory.create_adaptive_text(
                    page=self.page,
                    text=header_text,
                    text_type="title_main",
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )
        

        
        if not self._forecast_data:
            loading_text = translation_manager.get_translation("weather", "weekly_forecast_items", "loading", self._current_language)
            return ft.Column([
                ft.Container(
                    content=header,
                    padding=ft.padding.only(left=20, right=20, top=20, bottom=10)
                ),
                ft.Container(
                    content=ResponsiveTextFactory.create_adaptive_text(
                        page=self.page,
                        text=loading_text,
                        text_type="subtitle",
                        color=self._current_text_color
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20)
                )
            ])

        daily_cards = []
        
        for i, day_data in enumerate(self._forecast_data):
            try:
                card = self._build_daily_card(day_data, theme)
                daily_cards.append(card)
                
                # Add divider between days (except for the last one)
                if i < len(self._forecast_data) - 1:
                    divider_color = "#404040" if is_dark else "#e0e0e0"
                    divider = ft.Container(
                        content=ft.Divider(
                            height=1,
                            thickness=1,
                            color=theme.get("BORDER", divider_color)
                        ),
                        padding=ft.padding.symmetric(horizontal=20)
                    )
                    daily_cards.append(divider)
                    
            except Exception as e:
                logging.error(f"[ERROR WeeklyForecastDisplay] Failed to build card for {day_data.get('day_key', 'Unknown Day')}: {e}\nTraceback: {traceback.format_exc()}")
                # Add error placeholder card
                error_card = ft.Container(
                    content=ResponsiveTextFactory.create_adaptive_text(
                        page=self.page,
                        text="Error loading day",
                        text_type="caption",
                        color=ft.Colors.RED
                    ),
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center
                )
                daily_cards.append(error_card)
        
        return ft.Column([
            # Header container
            ft.Container(
                content=header,
                padding=ft.padding.only(left=20, right=20, top=20, bottom=15)
            ),
            # Cards container - simplified, no extra padding
            ft.Column(
                controls=daily_cards,
                spacing=0,
                tight=True
            )
        ], spacing=0)

    def _build_daily_card(self, day_data, theme):
        """Builds a clean styled row for a single day forecast with additional weather information."""
        translated_day = translation_manager.get_translation("weather", "weekly_forecast_items", day_data["day_key"], self._current_language)
        
        # Temperature data
        unit_symbol = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
        temp_min_str = f"{day_data['temp_min']}{unit_symbol}"
        temp_max_str = f"{day_data['temp_max']}{unit_symbol}"
        
        # Weather icon - simplified without background
        weather_icon = ft.Image(
            src=f"https://openweathermap.org/img/wn/{day_data['icon']}@2x.png",
            width=40,
            height=40,
            fit=ft.ImageFit.CONTAIN
        )
        
        # Day label
        day_label = ResponsiveTextFactory.create_adaptive_text(
            page=self.page,
            text=translated_day,
            text_type="title_main",
            weight=ft.FontWeight.W_600,
            color=self._current_text_color
        )
        
        # Temperature spans
        temperature_text = ResponsiveTextFactory.create_adaptive_text(
            page=self.page,
            text="",  # Il testo sarà impostato tramite spans
            text_type="title_section"
        )
        # Imposta manualmente gli spans dopo la creazione
        temperature_text.spans = [
            ft.TextSpan(
                temp_min_str, 
                ft.TextStyle(
                    weight=ft.FontWeight.W_600,
                        color=ft.Colors.BLUE_400,
                        #size=15
                    )
                ),
                ft.TextSpan(
                    "\n", 
                    ft.TextStyle(
                        color=self._current_text_color, 
                        #size=15
                    )
                ),
                ft.TextSpan(
                    temp_max_str, 
                    ft.TextStyle(
                        weight=ft.FontWeight.W_600, 
                        color=ft.Colors.RED_400,
                        #size=15
                    )
                )
            ]
        
        
        # Additional weather information in a compact row
        additional_info_widgets = []
        
        # Rain probability (only if > 0)
        if day_data.get('rain_probability', 0) > 0:
            additional_info_widgets.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.WATER_DROP, size=12, color=ft.Colors.BLUE_400),
                        ResponsiveTextFactory.create_adaptive_text(
                            page=self.page,
                            text=f"{day_data['rain_probability']}%",
                            text_type="tiny",
                            color=ft.Colors.BLUE_400,
                            weight="w500"
                        )
                    ], spacing=2),
                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_400),
                )
            )
        
        # Humidity
        additional_info_widgets.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.OPACITY, size=12, color=ft.Colors.CYAN_400),
                    ResponsiveTextFactory.create_adaptive_text(
                        page=self.page,
                        text=f"{day_data.get('humidity', 0)}%",
                        text_type="tiny",
                        color=ft.Colors.CYAN_400,
                        weight="w500"
                    )
                ], spacing=2),
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.CYAN_400),
            )
        )
        
        # Wind speed
        wind_unit = "m/s" if self._current_unit_system == "metric" else "mph"
        additional_info_widgets.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.AIR, size=12, color=ft.Colors.GREEN_400),
                    ResponsiveTextFactory.create_adaptive_text(
                        page=self.page,
                        text=f"{day_data.get('wind_speed', 0)}{wind_unit}",
                        text_type="tiny",
                        color=ft.Colors.GREEN_400,
                        weight="w500"
                    )
                ], spacing=2),
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400),
            )
        )
        
        # Additional info row
        additional_info_row = ft.Row(
            controls=additional_info_widgets,
            spacing=4,
            alignment=ft.MainAxisAlignment.START
        )
        
        # Main content structure
        main_row = ft.Row(
            controls=[
                # Day name (left)
                ft.Container(
                    content=day_label,
                    alignment=ft.alignment.center_left,
                    expand=2
                ),
                # Weather icon (center)
                ft.Container(
                    content=weather_icon,
                    alignment=ft.alignment.center,
                    expand=1
                ),
                # Temperature (right)
                ft.Container(
                    content=temperature_text,
                    alignment=ft.alignment.center_right,
                    expand=2
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
        
        # Clean card with main info and additional details
        card = ft.Container(
            content=ft.Column([
                main_row,
                ft.Container(height=6),  # Spacer
                ft.Container(
                    content=additional_info_row,
                    padding=ft.padding.only(left=20)  # Align with content above
                )
            ], spacing=0),
            padding=ft.padding.symmetric(horizontal=20, vertical=16),
            border_radius=0,  # Remove border radius for cleaner look
            # No background color - inherit from parent
        )
        
        return card

    def update_city(self, new_city: str):
        """Updates the city and triggers a UI refresh."""
        try:
            if self._city != new_city:
                self._city = new_city
                self._forecast_data = []  # Clear cached data
                if self.page and hasattr(self.page, 'run_task'):
                    self.page.run_task(self.update_ui)
        except Exception as e:
            logging.error(f"WeeklyForecastDisplay: Error updating city: {e}")

    def _safe_language_update(self, e=None):
        """Safely handle language change event."""
        try:
            # Check if component is still valid and connected
            if not self.page or not hasattr(self, '_city') or not self._city:
                logging.debug("WeeklyForecastDisplay: Skipping language update - component not ready")
                return
                
            if self.page and hasattr(self.page, 'run_task') and callable(getattr(self.page, 'run_task', None)):
                self.page.run_task(self.update_ui, e)
            else:
                logging.debug("WeeklyForecastDisplay: Cannot schedule language update - page.run_task not available")
        except Exception as ex:
            logging.error(f"WeeklyForecastDisplay: Error in safe language update: {ex}")
    
    def _safe_unit_update(self, e=None):
        """Safely handle unit change event."""
        try:
            # Check if component is still valid and connected
            if not self.page or not hasattr(self, '_city') or not self._city:
                logging.debug("WeeklyForecastDisplay: Skipping unit update - component not ready")
                return
                
            if self.page and hasattr(self.page, 'run_task') and callable(getattr(self.page, 'run_task', None)):
                self.page.run_task(self.update_ui, e)
            else:
                logging.debug("WeeklyForecastDisplay: Cannot schedule unit update - page.run_task not available")
        except Exception as ex:
            logging.error(f"WeeklyForecastDisplay: Error in safe unit update: {ex}")
    
    def _safe_theme_update(self, e=None):
        """Force a full rebuild of the component on theme change, but only update if attached to page."""
        try:
            if not self.page or not hasattr(self, '_city') or not self._city:
                logging.debug("WeeklyForecastDisplay: Skipping theme update - component not ready")
                return
            self.content = self.build()
            # Only call update if attached to page and parent
            if getattr(self, 'page', None) and getattr(self, 'parent', None):
                try:
                    self.update()
                except Exception as ex:
                    logging.debug(f"WeeklyForecastDisplay: update() skipped (not attached yet): {ex}")
            logging.debug("WeeklyForecastDisplay: Full rebuild triggered on theme change.")
        except Exception as ex:
            logging.error(f"WeeklyForecastDisplay: Error in safe theme update: {ex}")

    def cleanup(self):
        """Clean up observers and resources when component is destroyed."""
        try:
            if self._state_manager:
                # Unregister all observers
                try:
                    self._state_manager.unregister_observer("language_event", self._safe_language_update)
                except Exception as e:
                    logging.debug(f"WeeklyForecastDisplay: Error unregistering language observer: {e}")
                try:
                    self._state_manager.unregister_observer("unit", self._safe_unit_update)
                except Exception as e:
                    logging.debug(f"WeeklyForecastDisplay: Error unregistering unit observer: {e}")
                try:
                    self._state_manager.unregister_observer("theme_event", self._safe_theme_update)
                except Exception as e:
                    logging.debug(f"WeeklyForecastDisplay: Error unregistering theme observer: {e}")
                
                logging.debug("WeeklyForecastDisplay: Successfully cleaned up observers")
                self._state_manager = None
        except Exception as e:
            logging.error(f"WeeklyForecastDisplay: Error during cleanup: {e}")
