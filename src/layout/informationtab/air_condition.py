import flet as ft
from utils.config import DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from utils.translations_data import AIR_QUALITY_INDICATORS

from services.theme_handler import ThemeHandler
from services.translation_service import TranslationService
from services.api_service import ApiService
import asyncio
import logging

class AirConditionInfo(ft.Container):
    """
    Air condition information display - simplified elementary approach.
    """

    def __init__(self, city, feels_like, humidity, wind_speed, pressure, wind_direction=None, wind_gust=None,
                 visibility=None, uv_index=None, dew_point=None, cloud_coverage=None, page=None, theme_handler=None,
                 language=None, unit=None, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.theme_handler = theme_handler if theme_handler else ThemeHandler(self.page)
        self._api_service = ApiService()
        self._state_manager = page.session.get('state_manager') if page and hasattr(page, 'session') else None
        self._current_language = language or DEFAULT_LANGUAGE
        self._current_unit_system = unit or DEFAULT_UNIT_SYSTEM
        self._current_text_color = self.theme_handler.get_text_color()
        self._city = city
        self._data = {
            "feels_like": feels_like, "humidity": humidity, "wind": wind_speed, "pressure": pressure,
            "wind_direction": wind_direction, "wind_gust": wind_gust, "visibility": visibility,
            "uv_index": uv_index, "dew_point": dew_point, "cloud_coverage": cloud_coverage
        }
        self._register_observers()
        self.content = self.build()

    def _register_observers(self):
        if not self._state_manager: 
            return
        for event, handler in [("unit", self._on_change), ("language_event", self._on_change), ("theme_event", self._on_change)]:
            self._state_manager.register_observer(event, handler)


    def _on_change(self, *_):
        if self.page and hasattr(self.page, 'run_task'):
            self.page.run_task(self.update)

    def cleanup(self):
        if not self._state_manager: 
            return
        for event, handler in [("unit", self._on_change), ("language_event", self._on_change), ("theme_event", self._on_change)]:
            self._state_manager.unregister_observer(event, handler)
    
    def _get_theme_mode(self) -> bool:
        """
        Safely get the current theme mode (dark or light).
        
        Returns:
            bool: True if dark theme is active, False for light theme
        """
        is_dark = False
        try:
            if self.page and hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            elif self._state_manager:
                # Fallback to state manager if page theme_mode is not available
                is_dark = self._state_manager.get_state('using_theme') or False
            logging.debug(f"AirConditionInfo: Theme mode is {'dark' if is_dark else 'light'}")
        except Exception as e:
            logging.warning(f"AirConditionInfo: Error determining theme mode: {e}")
            # Default to light theme if there's an error
        return is_dark

    async def update(self):
        if not self.page: 
            return
        if self._state_manager:
            lang = self._state_manager.get_state('language') or self._current_language
            unit = self._state_manager.get_state('unit') or self._current_unit_system
            if lang != self._current_language or unit != self._current_unit_system:
                self._current_language, self._current_unit_system = lang, unit
                weather_data = await asyncio.to_thread(
                    self._api_service.get_weather_data,
                    city=self._city, language=lang, unit=unit
                )
                if weather_data:
                    for key, func in [
                        ("feels_like", self._api_service.get_feels_like_temperature),
                        ("humidity", self._api_service.get_humidity),
                        ("wind", self._api_service.get_wind_speed),
                        ("wind_direction", self._api_service.get_wind_direction),
                        ("wind_gust", self._api_service.get_wind_gust),
                        ("pressure", self._api_service.get_pressure),
                        ("visibility", self._api_service.get_visibility),
                        ("uv_index", self._api_service.get_uv_index),
                        ("dew_point", self._api_service.get_dew_point),
                        ("cloud_coverage", self._api_service.get_cloud_coverage)
                    ]:
                        self._data[key] = func(weather_data)
        self.content = self.build()
        try:
            super().update()
        except Exception:
            pass

    def build(self):
        if not self._data.get("feels_like") and not self._data.get("humidity"):
            loading_text = "Loading air conditions..."
            return ft.Column([
                self._build_header(),
                ft.Container(
                    content=ft.Text(
                        loading_text,
                        color=self.theme_handler.get_text_color() if self.theme_handler else ft.Colors.BLACK,
                        size=16
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20)
                )
            ])
        header = self._build_header()
        cards = self._build_metric_cards()
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
        
        # Get theme mode using helper method
        is_dark = self._get_theme_mode()

        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.AIR_OUTLINED,
                    color=ft.Colors.BLUE_400 if not is_dark else ft.Colors.BLUE_300,
                    size=25
                ),
                ft.Container(width=5),  # Spacer
                ft.Text(
                    header_text,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=20, bottom=10)
        )
    
    def get_wind_direction_icon(self, wind_direction_deg):
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

    def _build_metric_cards(self):
        translation_service = self.page.session.get('translation_service') if self.page and hasattr(self.page, 'session') else None
        get_label = lambda k: translation_service.translate_from_dict("air_condition_items", k, self._current_language) if translation_service else k.replace('_', ' ').title()
        temp_unit = TranslationService.get_unit_symbol("temperature", self._current_unit_system)
        wind_unit = TranslationService.get_unit_symbol("wind", self._current_unit_system)
        pressure_unit = TranslationService.get_unit_symbol("pressure", self._current_unit_system)
        metrics = [
            ("feels_like", temp_unit, ft.Icons.THERMOSTAT_OUTLINED, "orange"),
            ("humidity", "%", ft.Icons.WATER_DROP_OUTLINED, "blue"),
            ("wind", wind_unit, ft.Icons.AIR, "teal"),
            ("pressure", pressure_unit, ft.Icons.SPEED, "purple"),
            ("visibility", "m", ft.Icons.VISIBILITY_OUTLINED, "cyan"),
            ("uv_index", "", ft.Icons.WB_SUNNY_OUTLINED, "yellow"),
            ("dew_point", temp_unit, ft.Icons.WATER_OUTLINED, "indigo"),
            ("cloud_coverage", "%", ft.Icons.CLOUD_OUTLINED, "grey"),
        ]
        cards = []
        for key, unit, icon, color in metrics:
            value = self._data.get(key)
            if value is None:
                continue
            value_text = f"{value}{unit}"
            wind_desc = None
            # Sigla direzione vento sempre visibile se disponibile
            if key == "wind":
                wind_direction = self._data.get("wind_direction")
                if wind_direction is not None:
                    wind_desc = self.get_wind_direction_icon(wind_direction)
            if key == "visibility":
                value_text = f"{value/1000:.1f} km"
            if key == "uv_index":
                value_text = f"{round(value, 1)}"
            cards.append(self._create_metric_card(icon, get_label(key), value_text, value, key, color, wind_desc))
        return cards
    
    def _create_metric_card(self, icon, name, value_text, raw_value, metric_key, color_scheme="blue", wind_desc=None):
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
            lang = self._current_language
            
            if key == "humidity":
                if 40 <= value <= 60:
                    label = AIR_QUALITY_INDICATORS["humidity"]["excellent"].get(lang, "Ottima")
                    color = ft.Colors.GREEN_400
                elif 30 <= value <= 70:
                    label = AIR_QUALITY_INDICATORS["humidity"]["good"].get(lang, "Buona")
                    color = ft.Colors.BLUE_400
                elif 20 <= value <= 80:
                    label = AIR_QUALITY_INDICATORS["humidity"]["moderate"].get(lang, "Moderata")
                    color = ft.Colors.YELLOW_600
                elif 10 <= value <= 90:
                    label = AIR_QUALITY_INDICATORS["humidity"]["poor"].get(lang, "Scarsa")
                    color = ft.Colors.ORANGE_400
                else:
                    label = AIR_QUALITY_INDICATORS["humidity"]["very_poor"].get(lang, "Molto scarsa")
                    color = ft.Colors.RED_400
                return (label, color)
            elif key == "uv_index":
                if value <= 2:
                    label = AIR_QUALITY_INDICATORS["uv_index"]["low"].get(lang, "Basso")
                    color = ft.Colors.GREEN_400
                elif value <= 5:
                    label = AIR_QUALITY_INDICATORS["uv_index"]["moderate"].get(lang, "Moderato")
                    color = ft.Colors.YELLOW_600
                elif value <= 7:
                    label = AIR_QUALITY_INDICATORS["uv_index"]["high"].get(lang, "Alto")
                    color = ft.Colors.ORANGE_400
                elif value <= 10:
                    label = AIR_QUALITY_INDICATORS["uv_index"]["very_high"].get(lang, "Molto alto")
                    color = ft.Colors.RED_400
                else:
                    label = AIR_QUALITY_INDICATORS["uv_index"]["extreme"].get(lang, "Estremo")
                    color = ft.Colors.PURPLE_400
                return (label, color)
            elif key == "pressure":
                if 1013 <= value <= 1023:
                    label = AIR_QUALITY_INDICATORS["pressure"]["normal"].get(lang, "Normale")
                    color = ft.Colors.GREEN_400
                elif 1000 <= value < 1013:
                    label = AIR_QUALITY_INDICATORS["pressure"]["low"].get(lang, "Bassa")
                    color = ft.Colors.YELLOW_600
                elif 1023 < value <= 1030:
                    label = AIR_QUALITY_INDICATORS["pressure"]["high"].get(lang, "Alta")
                    color = ft.Colors.ORANGE_400
                elif value < 1000:
                    label = AIR_QUALITY_INDICATORS["pressure"]["very_low"].get(lang, "Molto bassa")
                    color = ft.Colors.RED_400
                else:  # > 1030
                    label = AIR_QUALITY_INDICATORS["pressure"]["very_high"].get(lang, "Molto alta")
                    color = ft.Colors.PURPLE_400
                return (label, color)
            elif key == "visibility":
                if value >= 20000:
                    label = AIR_QUALITY_INDICATORS["visibility"]["excellent"].get(lang, "Ottima")
                    color = ft.Colors.GREEN_400
                elif value >= 10000:
                    label = AIR_QUALITY_INDICATORS["visibility"]["good"].get(lang, "Buona")
                    color = ft.Colors.BLUE_400
                elif value >= 5000:
                    label = AIR_QUALITY_INDICATORS["visibility"]["moderate"].get(lang, "Moderata")
                    color = ft.Colors.YELLOW_600
                elif value >= 1000:
                    label = AIR_QUALITY_INDICATORS["visibility"]["poor"].get(lang, "Scarsa")
                    color = ft.Colors.ORANGE_400
                else:
                    label = AIR_QUALITY_INDICATORS["visibility"]["very_poor"].get(lang, "Molto scarsa")
                    color = ft.Colors.RED_400
                return (label, color)
            elif key == "feels_like":
                if 18 <= value <= 24:
                    label = AIR_QUALITY_INDICATORS["feels_like"]["ideal"].get(lang, "Ideale")
                    color = ft.Colors.GREEN_400
                elif 15 <= value <= 28:
                    label = AIR_QUALITY_INDICATORS["feels_like"]["comfortable"].get(lang, "Confortevole")
                    color = ft.Colors.BLUE_400
                elif 10 <= value <= 32:
                    label = AIR_QUALITY_INDICATORS["feels_like"]["acceptable"].get(lang, "Accettabile")
                    color = ft.Colors.YELLOW_600
                elif 5 <= value <= 38:
                    label = AIR_QUALITY_INDICATORS["feels_like"]["uncomfortable"].get(lang, "Scomodo")
                    color = ft.Colors.ORANGE_400
                else:
                    label = AIR_QUALITY_INDICATORS["feels_like"]["extreme"].get(lang, "Estremo")
                    color = ft.Colors.RED_400
                return (label, color)
            elif key == "wind":
                if value <= 10:
                    label = AIR_QUALITY_INDICATORS["wind"]["calm"].get(lang, "Calmo")
                    color = ft.Colors.GREEN_400
                elif value <= 20:
                    label = AIR_QUALITY_INDICATORS["wind"]["light"].get(lang, "Leggero")
                    color = ft.Colors.BLUE_400
                elif value <= 40:
                    label = AIR_QUALITY_INDICATORS["wind"]["moderate"].get(lang, "Moderato")
                    color = ft.Colors.YELLOW_600
                elif value <= 60:
                    label = AIR_QUALITY_INDICATORS["wind"]["strong"].get(lang, "Forte")
                    color = ft.Colors.ORANGE_400
                else:
                    label = AIR_QUALITY_INDICATORS["wind"]["very_strong"].get(lang, "Molto forte")
                    color = ft.Colors.RED_400
                return (label, color)
            elif key == "dew_point":
                if value <= 10:
                    label = AIR_QUALITY_INDICATORS["dew_point"]["dry"].get(lang, "Secco")
                    color = ft.Colors.GREEN_400
                elif value <= 15:
                    label = AIR_QUALITY_INDICATORS["dew_point"]["comfortable"].get(lang, "Confortevole")
                    color = ft.Colors.BLUE_400
                elif value <= 20:
                    label = AIR_QUALITY_INDICATORS["dew_point"]["humid"].get(lang, "Umido")
                    color = ft.Colors.YELLOW_600
                elif value <= 24:
                    label = AIR_QUALITY_INDICATORS["dew_point"]["unpleasant"].get(lang, "Sgradevole")
                    color = ft.Colors.ORANGE_400
                else:
                    label = AIR_QUALITY_INDICATORS["dew_point"]["oppressive"].get(lang, "Oppressivo")
                    color = ft.Colors.RED_400
                return (label, color)
            elif key == "cloud_coverage":
                if value <= 10:
                    label = AIR_QUALITY_INDICATORS["cloud_coverage"]["clear"].get(lang, "Sereno")
                    color = ft.Colors.GREEN_400
                elif value <= 30:
                    label = AIR_QUALITY_INDICATORS["cloud_coverage"]["partly_cloudy"].get(lang, "Poco nuvoloso")
                    color = ft.Colors.BLUE_400
                elif value <= 70:
                    label = AIR_QUALITY_INDICATORS["cloud_coverage"]["partly_cloudy_moderate"].get(lang, "Parzialmente nuvoloso")
                    color = ft.Colors.YELLOW_600
                elif value <= 90:
                    label = AIR_QUALITY_INDICATORS["cloud_coverage"]["mostly_cloudy"].get(lang, "Molto nuvoloso")
                    color = ft.Colors.ORANGE_400
                else:
                    label = AIR_QUALITY_INDICATORS["cloud_coverage"]["overcast"].get(lang, "Coperto")
                    color = ft.Colors.GREY_600
                return (label, color)
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
        # Se è la card del vento, aggiungi l'icona e la descrizione della direzione accanto al valore
        value_row = [
            ft.Text(
                value_text,
                size=14,
                weight=ft.FontWeight.BOLD,
                color=self._current_text_color,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS
            )
        ]
        # Mostra la sigla della direzione sempre accanto al valore della card del vento
        if metric_key == "wind" and wind_desc is not None:
            wind_icon, wind_direction_text = wind_desc
            # Aggiungi l'icona della direzione
            value_row.append(ft.Icon(
                wind_icon,
                size=16,
                color=ft.Colors.with_opacity(0.85, self._current_text_color)
            ))
            # Aggiungi la sigla testuale
            value_row.append(ft.Container(
                content=ft.Text(
                    wind_direction_text,
                    size=13,
                    color=ft.Colors.with_opacity(0.85, self._current_text_color),
                    weight=ft.FontWeight.W_700,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                padding=ft.padding.only(left=2, right=2, top=0, bottom=0),
                alignment=ft.alignment.center
            ))

        card_content = ft.Column([
            ft.Row([
                icon_container,
                ft.Container(width=8),
                ft.Column([
                    ft.Row(value_row, spacing=4, alignment=ft.MainAxisAlignment.START),
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
        is_dark = self._get_theme_mode()
        
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
