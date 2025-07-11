import flet as ft
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
from services.api_service import ApiService
import asyncio
import logging
import traceback

def get_wind_direction_icon(wind_direction_deg):
    """
    Restituisce l'icona appropriata per la direzione del vento.
    
    Args:
        wind_direction_deg: Direzione del vento in gradi (0-360)
        
    Returns:
        Tupla (icona, descrizione) con l'icona ft.Icons e descrizione testuale
    """
    if wind_direction_deg is None:
        return ft.Icons.QUESTION_MARK, "N/A"
    
    # Normalizza i gradi a 0-360
    wind_direction_deg = wind_direction_deg % 360
    
    # Definisce le direzioni con le relative icone
    # N = 0°, NE = 45°, E = 90°, SE = 135°, S = 180°, SW = 225°, W = 270°, NW = 315°
    if wind_direction_deg >= 337.5 or wind_direction_deg < 22.5:
        return ft.Icons.NORTH, "N"
    elif 22.5 <= wind_direction_deg < 67.5:
        return ft.Icons.NORTH_EAST, "NE"
    elif 67.5 <= wind_direction_deg < 112.5:
        return ft.Icons.EAST, "E"
    elif 112.5 <= wind_direction_deg < 157.5:
        return ft.Icons.SOUTH_EAST, "SE"
    elif 157.5 <= wind_direction_deg < 202.5:
        return ft.Icons.SOUTH, "S"
    elif 202.5 <= wind_direction_deg < 247.5:
        return ft.Icons.SOUTH_WEST, "SW"
    elif 247.5 <= wind_direction_deg < 292.5:
        return ft.Icons.WEST, "W"
    elif 292.5 <= wind_direction_deg < 337.5:
        return ft.Icons.NORTH_WEST, "NW"
    else:
        return ft.Icons.QUESTION_MARK, "N/A"

class AirConditionInfo(ft.Container):
    """
    Air condition information display - simplified elementary approach.
    """

    def __init__(self, city: str, feels_like: int, humidity: int, wind_speed: int,
                 pressure: int, wind_direction: int = None, wind_gust: float = None, 
                 visibility: int = None, uv_index: float = None, dew_point: int = None, 
                 cloud_coverage: int = None, page: ft.Page = None, **kwargs):
        super().__init__(**kwargs)
        self._city = city
        self._feels_like_data = feels_like
        self._humidity_data = humidity
        self._wind_speed_data = wind_speed
        self._wind_direction_data = wind_direction
        self._wind_gust_data = wind_gust
        self._pressure_data = pressure
        self._visibility_data = visibility
        self._uv_index_data = uv_index
        self._dew_point_data = dew_point
        self._cloud_coverage_data = cloud_coverage
        self.page = page
        
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_unit_system = DEFAULT_UNIT_SYSTEM
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self.padding = 16
        self._api_service = ApiService()

        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={'title': 24, 'label': 16, 'value': 16, 'icon': 20},
            breakpoints=[600, 900, 1200, 1600]
        )

        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')

        self.content = self.build()

    async def update(self):
        """Update language, unit, theme and rebuild content."""
        if not self.page:
            return

        try:
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                new_unit_system = self._state_manager.get_state('unit') or self._current_unit_system
                
                unit_changed = self._current_unit_system != new_unit_system
                self._current_language = new_language
                self._current_unit_system = new_unit_system

                # Only fetch new data if unit system changed
                if unit_changed:
                    weather_data = await asyncio.to_thread(
                        self._api_service.get_weather_data,
                        city=self._city, language=self._current_language, unit=self._current_unit_system
                    )
                    if weather_data:
                        self._feels_like_data = self._api_service.get_feels_like_temperature(weather_data)
                        self._humidity_data = self._api_service.get_humidity(weather_data)
                        self._wind_speed_data = self._api_service.get_wind_speed(weather_data)
                        self._wind_direction_data = self._api_service.get_wind_direction(weather_data)
                        self._wind_gust_data = self._api_service.get_wind_gust(weather_data)
                        self._pressure_data = self._api_service.get_pressure(weather_data)
                        self._visibility_data = self._api_service.get_visibility(weather_data)
                        self._uv_index_data = self._api_service.get_uv_index(weather_data)
                        self._dew_point_data = self._api_service.get_dew_point(weather_data)
                        self._cloud_coverage_data = self._api_service.get_cloud_coverage(weather_data)

            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._current_text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            try:
                super().update()
            except AssertionError:
                pass
        except Exception as e:
            logging.error(f"AirConditionInfo: Error updating: {e}\n{traceback.format_exc()}")

    def build(self):
        """Create the air condition display following AirPollution's modern design."""
        if not self._feels_like_data and not self._humidity_data:
            loading_text = "Loading air conditions..."
            return ft.Column([
                self._build_header(),
                ft.Container(
                    content=ft.Text(
                        loading_text,
                        color=self._current_text_color,
                        size=16
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20)
                )
            ])

        # Build header
        header = self._build_header()
        
        # Build metric cards
        cards = self._build_metric_cards()
        
        # Cards container with responsive grid layout
        cards_container = self._build_responsive_grid(cards)
        
        return ft.Column([
            header,
            cards_container
        ], spacing=8)
    
    def _build_header(self):
        """Builds a modern header for air condition section."""
        # Get translation service
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        header_text = "Condizioni dell'aria"
        if translation_service:
            header_text = translation_service.translate_from_dict("air_condition_items", "air_condition_title", self._current_language) or header_text
        
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.AIR_OUTLINED,
                    color=ft.Colors.BLUE_400 if not is_dark else ft.Colors.BLUE_300,
                    size=24
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    header_text,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=20, bottom=10)
        )
    
    def _build_metric_cards(self):
        """Builds modern cards for each air condition metric."""
        # Get translation service
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        # Get unit symbols
        temp_unit = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
        wind_unit = TranslationService.get_unit_symbol("wind", self._current_unit_system)
        pressure_unit = TranslationService.get_unit_symbol("pressure", self._current_unit_system)
        
        # Helper to get translations
        def get_label(key):
            if translation_service:
                return translation_service.translate_from_dict("air_condition_items", key, self._current_language) or key.replace('_', ' ').title()
            return key.replace('_', ' ').title()
        
        metric_configs = [
            {"key": "feels_like", "data": self._feels_like_data, "unit": temp_unit, "icon": ft.Icons.THERMOSTAT_OUTLINED, "color": "orange"},
            {"key": "humidity", "data": self._humidity_data, "unit": "%", "icon": ft.Icons.WATER_DROP_OUTLINED, "color": "blue"},
            {"key": "wind", "data": self._wind_speed_data, "unit": wind_unit, "icon": ft.Icons.AIR, "color": "teal"},
            {"key": "pressure", "data": self._pressure_data, "unit": pressure_unit, "icon": ft.Icons.SPEED, "color": "purple"},
            {"key": "visibility", "data": self._visibility_data, "unit": "m", "icon": ft.Icons.VISIBILITY_OUTLINED, "color": "cyan"},
            {"key": "uv_index", "data": self._uv_index_data, "unit": "", "icon": ft.Icons.WB_SUNNY_OUTLINED, "color": "yellow"},
            {"key": "dew_point", "data": self._dew_point_data, "unit": temp_unit, "icon": ft.Icons.WATER_OUTLINED, "color": "indigo"},
            {"key": "cloud_coverage", "data": self._cloud_coverage_data, "unit": "%", "icon": ft.Icons.CLOUD_OUTLINED, "color": "grey"},
        ]
        
        cards = []
        
        for config in metric_configs:
            if config["data"] is not None:
                value = config["data"]
                
                # Special formatting for wind (add direction)
                if config["key"] == "wind" and self._wind_direction_data is not None:
                    wind_icon, wind_desc = get_wind_direction_icon(self._wind_direction_data)
                    value_text = f"{value} {config['unit']} {wind_desc}"
                else:
                    value_text = f"{value}{config['unit']}"
                
                # Special formatting for visibility (convert to km)
                if config["key"] == "visibility":
                    value_text = f"{value/1000:.1f} km"
                
                # Special formatting for UV index
                if config["key"] == "uv_index":
                    value_text = f"{round(value, 1)}"
                
                name = get_label(config["key"])
                
                card = self._create_metric_card(
                    icon=config["icon"],
                    name=name,
                    value_text=value_text,
                    raw_value=value,
                    metric_key=config["key"],
                    color_scheme=config["color"]
                )
                cards.append(card)
        
        return cards
    
    def _create_metric_card(self, icon, name, value_text, raw_value, metric_key, color_scheme="blue"):
        """Creates a modern card for a single air condition metric."""
        # Color schemes
        color_schemes = {
            "orange": {"bg": ft.Colors.ORANGE_400, "light": ft.Colors.ORANGE_100},
            "blue": {"bg": ft.Colors.BLUE_400, "light": ft.Colors.BLUE_100},
            "teal": {"bg": ft.Colors.TEAL_400, "light": ft.Colors.TEAL_100},
            "purple": {"bg": ft.Colors.PURPLE_400, "light": ft.Colors.PURPLE_100},
            "cyan": {"bg": ft.Colors.CYAN_400, "light": ft.Colors.CYAN_100},
            "yellow": {"bg": ft.Colors.YELLOW_600, "light": ft.Colors.YELLOW_100},
            "indigo": {"bg": ft.Colors.INDIGO_400, "light": ft.Colors.INDIGO_100},
            "grey": {"bg": ft.Colors.GREY_600, "light": ft.Colors.GREY_100},
        }
        
        scheme = color_schemes.get(color_scheme, color_schemes["blue"])
        
        # Icon container
        icon_container = ft.Container(
            content=ft.Icon(
                icon,
                color=ft.Colors.WHITE,
                size=20
            ),
            width=40,
            height=40,
            bgcolor=scheme["bg"],
            border_radius=20,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=ft.Colors.with_opacity(0.25, scheme["bg"]),
                offset=ft.Offset(0, 2)
            )
        )
        
        # Quality indicator based on metric type
        def get_quality_indicator(value, key):
            if key == "humidity":
                if 30 <= value <= 50:
                    return ("Ideale", ft.Colors.GREEN_400)
                elif 20 <= value <= 70:
                    return ("Buona", ft.Colors.BLUE_400)
                else:
                    return ("Non ideale", ft.Colors.ORANGE_400)
            elif key == "uv_index":
                if value <= 2:
                    return ("Basso", ft.Colors.GREEN_400)
                elif value <= 5:
                    return ("Moderato", ft.Colors.YELLOW_600)
                elif value <= 7:
                    return ("Alto", ft.Colors.ORANGE_400)
                else:
                    return ("Molto alto", ft.Colors.RED_400)
            elif key == "pressure":
                if 1013 <= value <= 1023:
                    return ("Normale", ft.Colors.GREEN_400)
                elif value < 1013:
                    return ("Bassa", ft.Colors.BLUE_400)
                else:
                    return ("Alta", ft.Colors.ORANGE_400)
            elif key == "visibility":
                if value >= 10000:
                    return ("Ottima", ft.Colors.GREEN_400)
                elif value >= 5000:
                    return ("Buona", ft.Colors.BLUE_400)
                else:
                    return ("Limitata", ft.Colors.ORANGE_400)
            else:
                return ("", ft.Colors.TRANSPARENT)
        
        quality_text, quality_color = get_quality_indicator(raw_value, metric_key)
        
        quality_badge = ft.Container(
            content=ft.Text(
                quality_text,
                size=10,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.W_600
            ),
            bgcolor=quality_color,
            padding=ft.padding.symmetric(horizontal=6, vertical=2),
            border_radius=8,
            visible=bool(quality_text)
        )
        
        # Card content
        card_content = ft.Column([
            ft.Row([
                icon_container,
                ft.Container(width=8),
                ft.Column([
                    ft.Text(
                        value_text,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=self._current_text_color,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                    ft.Text(
                        name,
                        size=11,
                        color=ft.Colors.with_opacity(0.7, self._current_text_color),
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS
                    )
                ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True)
            ], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=4),  # Spacer
            ft.Row([
                ft.Container(expand=True),
                quality_badge
            ], alignment=ft.MainAxisAlignment.END) if quality_text else ft.Container(height=18)
        ], spacing=4)
        
        # Card container
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        return ft.Container(
            content=card_content,
            width=None,  # Let container expand based on available space
            height=100,   # Slightly smaller than air pollution cards
            padding=ft.padding.all(14),
            border_radius=14,
            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE if not is_dark else ft.Colors.BLACK),
            border=ft.border.all(
                1, 
                ft.Colors.with_opacity(0.1, ft.Colors.GREY_400 if not is_dark else ft.Colors.GREY_600)
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            expand=True  # Allow card to expand within its container
        )
    
    def _build_responsive_grid(self, cards):
        """Creates a responsive grid layout for cards."""
        if not cards:
            return ft.Container()
        
        # Calculate cards per row based on screen size
        if self.page and hasattr(self.page, 'window') and self.page.window:
            screen_width = self.page.window.width or 1200
        else:
            screen_width = 1200
        
        # Determine optimal card count per row
        if screen_width < 600:
            cards_per_row = 1
        elif screen_width < 900:
            cards_per_row = 2
        elif screen_width < 1200:
            cards_per_row = 3
        else:
            cards_per_row = 4
        
        # Split cards into rows
        rows = []
        for i in range(0, len(cards), cards_per_row):
            row_cards = cards[i:i + cards_per_row]
            # Pad the last row if needed
            while len(row_cards) < cards_per_row:
                row_cards.append(ft.Container(expand=True))
            
            row = ft.Row(
                controls=row_cards,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12,
                tight=False
            )
            rows.append(row)
        
        return ft.Container(
            content=ft.Column(
                controls=rows,
                spacing=12,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=10)
        )
