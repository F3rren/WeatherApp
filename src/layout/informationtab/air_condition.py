import flet as ft
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
from services.api_service import ApiService
import asyncio
import logging
import traceback

class AirConditionInfo(ft.Container):
    """
    Air condition information display.
    """

    def __init__(self, city: str, feels_like: int, humidity: int, wind_speed: int,
                 pressure: int, page: ft.Page = None, **kwargs):
        super().__init__(**kwargs)
        self._city = city
        self._feels_like_data = feels_like
        self._humidity_data = humidity
        self._wind_speed_data = wind_speed
        self._pressure_data = pressure
        self.page = page
        
        self._state_manager = None
        self._language = DEFAULT_LANGUAGE
        self._unit_system = DEFAULT_UNIT_SYSTEM
        self._text_color = LIGHT_THEME["TEXT"]
        self.padding = 20
        self._api_service = ApiService()

        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 24, 'label': 16, 'value': 16, 'icon': 20,
            },
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
                if self._text_handler:
                    self._text_handler._handle_resize(e)
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
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._language
                new_unit_system = self._state_manager.get_state('unit') or self._unit_system
                
                language_changed = self._language != new_language
                unit_changed = self._unit_system != new_unit_system

                self._language = new_language
                self._unit_system = new_unit_system

                if language_changed or unit_changed:
                    weather_data = await asyncio.to_thread(
                        self._api_service.get_weather_data,
                        city=self._city, language=self._language, unit=self._unit_system
                    )
                    if weather_data:
                        self._feels_like_data = self._api_service.get_feels_like_temperature(weather_data)
                        self._humidity_data = self._api_service.get_humidity(weather_data)
                        self._wind_speed_data = self._api_service.get_wind_speed(weather_data)
                        self._pressure_data = self._api_service.get_pressure(weather_data)

            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            self.update()
        except Exception as e:
            logging.error(f"AirConditionInfo: Error updating UI: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs a modern, professional UI for air condition information."""
        # Get translation service for header
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        header_text = "Air Conditions"
        if translation_service:
            header_text = translation_service.translate_from_dict(
                "air_condition_items", 
                "air_condition_title",
                self._language
            ) or header_text

        # Professional header with accent bar
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        header = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.INFO,
                    color=ft.Colors.ORANGE_400 if not is_dark else ft.Colors.ORANGE_300,
                    size=24
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    header_text,
                    size=self._text_handler.get_size('axis_title') + 2,
                    weight=ft.FontWeight.BOLD,
                    color=self._text_color,
                    font_family="system-ui",
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=20, bottom=16)
        )

        # Get unit symbols
        temp_unit = TranslationService.get_unit_symbol("temperature", self._unit_system)
        wind_unit = TranslationService.get_unit_symbol("wind", self._unit_system)
        pressure_unit = TranslationService.get_unit_symbol("pressure", self._unit_system)

        # Helper function to create modern metric cards
        def create_metric_card(icon, label_key, value, unit="", color_scheme="blue"):
            # Get translated label
            label_text = label_key
            if translation_service:
                label_text = translation_service.translate_from_dict(
                    "air_condition_items", 
                    label_key,
                    self._language
                ) or label_key

            # Color schemes for different metrics
            color_schemes = {
                "blue": {"bg": ft.Colors.BLUE_400, "shadow": ft.Colors.BLUE_200},
                "green": {"bg": ft.Colors.GREEN_400, "shadow": ft.Colors.GREEN_200},
                "orange": {"bg": ft.Colors.ORANGE_400, "shadow": ft.Colors.ORANGE_200},
                "purple": {"bg": ft.Colors.PURPLE_400, "shadow": ft.Colors.PURPLE_200},
                "teal": {"bg": ft.Colors.TEAL_400, "shadow": ft.Colors.TEAL_200},
            }
            
            scheme = color_schemes.get(color_scheme, color_schemes["blue"])
            
            # Create icon container with compact gradient background
            icon_container = ft.Container(
                width=40,  # Smaller icon container
                height=40,
                border_radius=20,
                bgcolor=scheme["bg"],
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=6,  # Reduced blur for subtle effect
                    color=ft.Colors.with_opacity(0.25, scheme["shadow"]),
                    offset=ft.Offset(0, 2),
                ),
                content=ft.Icon(
                    icon,
                    color=ft.Colors.WHITE,
                    size=20,  # Smaller icon
                ),
                alignment=ft.alignment.center,
            )

            # Compact value with unit
            value_text = ft.Text(
                f"{value}{unit}",
                size=18,  # Smaller font
                weight="w700",
                color=self._text_color,
                font_family="system-ui",
            )

            # Compact label text
            label_text_widget = ft.Text(
                label_text,
                size=12,  # Smaller label
                color=ft.Colors.with_opacity(0.7, self._text_color),
                weight="w500",
                font_family="system-ui",
            )

            # Quality indicator for specific metrics
            quality_indicator = None
            
            if label_key == "humidity":
                # Humidity quality indicator
                humidity_val = int(str(value).replace('%', ''))
                if 40 <= humidity_val <= 60:
                    quality_color = ft.Colors.GREEN_400
                    quality_text = "Optimal"
                elif 30 <= humidity_val <= 70:
                    quality_color = ft.Colors.ORANGE_400
                    quality_text = "Good"
                else:
                    quality_color = ft.Colors.RED_400
                    quality_text = "Poor"
                    
                quality_indicator = ft.Container(
                    content=ft.Text(
                        quality_text,
                        size=10,  # Smaller badge text
                        color=ft.Colors.WHITE,
                        weight="w600",
                    ),
                    bgcolor=quality_color,
                    padding=ft.padding.symmetric(horizontal=6, vertical=1),  # Tighter padding
                    border_radius=8,  # Smaller radius
                )
            
            elif label_key == "pressure":
                # Pressure quality indicator
                pressure_val = int(str(value).split()[0])
                if 1013 <= pressure_val <= 1020:
                    quality_color = ft.Colors.GREEN_400
                    quality_text = "Normal"
                elif 1000 <= pressure_val <= 1030:
                    quality_color = ft.Colors.ORANGE_400
                    quality_text = "Fair"
                else:
                    quality_color = ft.Colors.RED_400
                    quality_text = "Unusual"
                    
                quality_indicator = ft.Container(
                    content=ft.Text(
                        quality_text,
                        size=10,  # Smaller badge text
                        color=ft.Colors.WHITE,
                        weight="w600",
                    ),
                    bgcolor=quality_color,
                    padding=ft.padding.symmetric(horizontal=6, vertical=1),  # Tighter padding
                    border_radius=8,  # Smaller radius
                )

            # Compact card content layout
            card_content = ft.Column([
                ft.Row([
                    icon_container,
                    ft.Container(width=12),  # Smaller spacer
                    ft.Column([
                        value_text,
                        label_text_widget,
                        quality_indicator if quality_indicator else ft.Container(height=0),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=2),  # Tighter spacing
                ], alignment=ft.MainAxisAlignment.START),
            ], spacing=4)  # Reduced spacing

            # Compact modern card container
            return ft.Container(
                content=card_content,
                padding=ft.padding.all(16),  # Reduced padding
                border_radius=14,  # Slightly smaller radius
                bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE if not is_dark else ft.Colors.BLACK),
                border=ft.border.all(
                    1, 
                    ft.Colors.with_opacity(0.1, ft.Colors.GREY_400 if not is_dark else ft.Colors.GREY_600)
                ),
                width=180,  # Smaller width
                height=100,  # Smaller height
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            )

        # Create metric cards
        cards = [
            create_metric_card(
                ft.Icons.THERMOSTAT_OUTLINED, 
                "feels_like", 
                self._feels_like_data, 
                temp_unit,
                "orange"
            ),
            create_metric_card(
                ft.Icons.WATER_DROP_OUTLINED, 
                "humidity", 
                self._humidity_data, 
                "%",
                "blue"
            ),
            create_metric_card(
                ft.Icons.AIR_OUTLINED, 
                "wind", 
                self._wind_speed_data, 
                f" {wind_unit}",
                "teal"
            ),
            create_metric_card(
                ft.Icons.COMPRESS_OUTLINED, 
                "pressure", 
                self._pressure_data, 
                f" {pressure_unit}",
                "purple"
            ),
        ]

        # Horizontal layout - all cards in a single row
        grid_content = ft.Row([
            cards[0],  # Feels like
            ft.Container(width=12),  # Spacer
            cards[1],  # Humidity
            ft.Container(width=12),  # Spacer
            cards[2],  # Wind
            ft.Container(width=12),  # Spacer
            cards[3],  # Pressure
        ], alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.AUTO)  # Add scroll for smaller screens

        grid_container = ft.Container(
            content=grid_content,
            padding=ft.padding.symmetric(horizontal=20, vertical=8),
        )

        return ft.Container(
            content=ft.Column([
                header,
                grid_container,
            ], spacing=4),  # Tighter spacing between header and content
            padding=ft.padding.only(bottom=16),  # Reduced bottom padding
        )
