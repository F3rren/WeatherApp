import os
import flet as ft
import logging
import traceback
from services.api.api_service import ApiService, load_dotenv
from services.ui.translation_service import TranslationService
from services.ui.theme_handler import ThemeHandler
from translations import translation_manager

from utils.translations_data import TRANSLATIONS

class AirPollutionDisplay(ft.Container):
    """
    Air pollution display component.
    Shows detailed air quality information.
    Manages its own UI construction, updates, and state observers.
    """
    
    def __init__(self, page: ft.Page, lat: float = None, lon: float = None, theme_handler: ThemeHandler = None, **kwargs):
        load_dotenv()
        super().__init__(**kwargs)
        self.page = page
        self.theme_handler = theme_handler or ThemeHandler(self.page)
        self._lat = lat
        self._lon = lon

        self._api_service = ApiService()
        self._state_manager = None
        self._current_language = os.getenv("DEFAULT_LANGUAGE")
        self._current_text_color = self.theme_handler.get_text_color()
        self._pollution_data = {}



        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)

        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')

        self.content = self.build()

    async def update(self):
        """Updates state and rebuilds the UI, fetching new data if needed."""
        if not self.page or not self.visible:
            return

        try:
            data_changed = False
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                language_changed = self._current_language != new_language
                self._current_language = new_language
                data_changed = language_changed

            if not self._pollution_data or data_changed:
                if self._lat is not None and self._lon is not None:
                    self._pollution_data = await self._api_service.get_air_pollution_async(self._lat, self._lon) or {}
                else:
                    self._pollution_data = {}

            # Safe theme detection centralizzata
            self._current_text_color = self.theme_handler.get_text_color()

            self.content = self.build()
            # Only update if this control is already in the page
            try:
                super().update()
            except Exception:
                # Control not yet added to page, update will happen when added
                pass
        except Exception as e:
            logging.error(f"AirPollutionDisplay: Error updating: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs modern, card-based UI for air pollution data."""
        if not self._pollution_data or "aqi" not in self._pollution_data:
            loading_text = translation_manager.get_translation("air_quality", "general", "no_air_pollution_data", self._current_language)
            return ft.Column([
                self._build_header(),
                ft.Container(
                    content=ft.Text(
                        loading_text,
                        color=self._current_text_color,
                        size=14
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20)
                )
            ])

        aqi = self._pollution_data.get("aqi", 0)
        components = {k: v for k, v in self._pollution_data.items() if k != "aqi"}

        # Build header with AQI badge
        header = self._build_header_with_aqi(aqi)
        
        # Build pollutant cards
        cards = self._build_pollutant_cards(components)
        
        # Cards container with responsive grid layout (2x4 vertical)
        cards_container = self._build_responsive_grid(cards)
        
        return ft.Column([
            header,
            cards_container
        ], spacing=8)

    async def refresh(self):
        """Forces a data refetch and UI update."""
        self._pollution_data = {}  # By clearing the data, we ensure update_ui will fetch new data.
        if self.page:
            await self.update_ui()

    async def update_location(self, lat: float, lon: float):
        """Updates the coordinates and clears cached data to force refresh."""
        self._lat = lat
        self._lon = lon
        self._pollution_data = {}  # Clear cached data to force refresh
        if self.page:
            await self.update_ui()

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

    def _build_header(self):
        """Builds a modern header for air pollution section."""
        # Get translation service
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')

        header_text = "Inquinamento dell'aria"
        if translation_service:
            header_text = translation_manager.get_translation("air_quality", "general", "air_quality_index", self._current_language)
        
        # Get theme mode using helper method
        is_dark = self._get_theme_mode()
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.AIR_OUTLINED,
                    color=ft.Colors.GREEN_400 if not is_dark else ft.Colors.GREEN_300,
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
    
    def _build_header_with_aqi(self, aqi):
        """Builds header with AQI badge."""
        header_text = translation_manager.get_translation("air_quality", "general", "air_quality_index", self._current_language)
        
        # Get AQI description and color
        lang_code = TranslationService.normalize_lang_code(self._current_language)
        aqi_descriptions = TRANSLATIONS.get(lang_code, {}).get("air_pollution_items", {}).get("aqi_descriptions")
        
        if not aqi_descriptions:
            aqi_descriptions = TRANSLATIONS.get(self._current_language, {}).get("air_pollution_items", {}).get("aqi_descriptions", ["N/A"] * 6)
        aqi_idx = min(max(aqi, 0), 5)
        aqi_desc = aqi_descriptions[aqi_idx] if aqi_idx < len(aqi_descriptions) else "N/A"
        
        # AQI colors
        aqi_colors = ["#D3D3D3", "#00E400", "#FFFF00", "#FF7E00", "#FF0000", "#99004C"]
        aqi_color_idx = max(0, min(aqi, len(aqi_colors) - 1))
        aqi_color = aqi_colors[aqi_color_idx]
        
        # Safe theme detection
        if self.page and hasattr(self.page, 'theme_mode'):
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        else:
            is_dark = False
        
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(
                        ft.Icons.AIR_OUTLINED,
                        color=ft.Colors.GREEN_400 if not is_dark else ft.Colors.GREEN_300,
                        size=24
                    ),
                    ft.Container(width=12),
                    ft.Text(
                        header_text,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=self._current_text_color
                    ),
                    ft.Container(
                    content=ft.Text(
                        aqi_desc,
                        size=12,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.WHITE if aqi > 2 else ft.Colors.BLACK
                    ),
                    bgcolor=aqi_color,
                    border_radius=12,
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                        offset=ft.Offset(0, 2)
                    )
                )
                ], alignment=ft.MainAxisAlignment.START, expand=True),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.only(left=20, right=20, top=20, bottom=10)
        )
    
    def _build_pollutant_cards(self, components):
        """Builds modern cards for each pollutant."""
        pollutant_configs = [
            {"key": "co", "icon": ft.Icons.SMOKING_ROOMS_OUTLINED, "color": "red"},
            {"key": "so2", "icon": ft.Icons.CLOUD_OUTLINED, "color": "orange"},
            {"key": "no", "icon": ft.Icons.FACTORY_OUTLINED, "color": "purple"},
            {"key": "no2", "icon": ft.Icons.LOCAL_GAS_STATION_OUTLINED, "color": "purple"},
            {"key": "pm2_5", "icon": ft.Icons.GRAIN_OUTLINED, "color": "brown"},
            {"key": "pm10", "icon": ft.Icons.SCATTER_PLOT_OUTLINED, "color": "brown"},
            {"key": "o3", "icon": ft.Icons.WB_SUNNY_OUTLINED, "color": "blue"},
            {"key": "nh3", "icon": ft.Icons.AGRICULTURE_OUTLINED, "color": "green"},
        ]
        
        cards = []
        
        for config in pollutant_configs:
            key = config["key"]
            # Always show all pollutants, even if data is missing (show 0)
            value = components.get(key, 0)
            name = translation_manager.get_translation("air_quality", "pollutants", key, self._current_language)
            
            card = self._create_pollutant_card(
                icon=config["icon"],
                name=name,
                symbol=key.upper().replace("_", "."),
                value=value,
                color_scheme=config["color"]
            )
            cards.append(card)
        
        return cards
    
    def _create_pollutant_card(self, icon, name, symbol, value, color_scheme="blue"):
        """Creates a modern card for a single pollutant."""
        # Color schemes
        color_schemes = {
            "red": {"bg": ft.Colors.RED_400, "light": ft.Colors.RED_100},
            "orange": {"bg": ft.Colors.ORANGE_400, "light": ft.Colors.ORANGE_100},
            "purple": {"bg": ft.Colors.PURPLE_400, "light": ft.Colors.PURPLE_100},
            "brown": {"bg": ft.Colors.BROWN_400, "light": ft.Colors.BROWN_100},
            "blue": {"bg": ft.Colors.BLUE_400, "light": ft.Colors.BLUE_100},
            "green": {"bg": ft.Colors.GREEN_400, "light": ft.Colors.GREEN_100},
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
        
        # Quality indicator based on value ranges
        def get_quality_indicator(val, pollutant_key):
            #CO calculation ranges
            if pollutant_key == "co":
                if val < 0 or val is None:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "na", self._current_language), ft.Colors.GREY_400)
                if val >= 0 and val < 4400:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "good", self._current_language), ft.Colors.GREEN_400)
                elif val >= 4400 and val < 9400:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "fair", self._current_language), ft.Colors.YELLOW_400)
                elif val >= 9400 and val < 12400:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "moderate", self._current_language), ft.Colors.ORANGE_400)
                if val >= 12400 and val < 15400:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "poor", self._current_language), ft.Colors.RED_400)
                else:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "very_poor", self._current_language), ft.Colors.PURPLE_400)
            #SO2 calculation ranges
            elif pollutant_key == "so2":
                if val < 0 or val is None:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "na", self._current_language), ft.Colors.GREY_400)
                if val >= 0 and val < 20:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "good", self._current_language), ft.Colors.GREEN_400)
                elif val >= 20 and val < 80:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "fair", self._current_language), ft.Colors.YELLOW_400)
                elif val >= 80 and val < 250:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "moderate", self._current_language), ft.Colors.ORANGE_400)
                if val >= 250 and val < 350:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "poor", self._current_language), ft.Colors.RED_400)
                else:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "very_poor", self._current_language), ft.Colors.PURPLE_400)                
            #NO calculation ranges
            elif pollutant_key == "no":
                #if no data, return "N/A"
                if val < 0 or val is None:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "na", self._current_language), ft.Colors.GREY_400)
                if val >= 0 and val < 40:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "good", self._current_language), ft.Colors.GREEN_400)
                elif val >= 40 and val < 70:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "fair", self._current_language), ft.Colors.YELLOW_400)
                elif val >= 70 and val < 150:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "moderate", self._current_language), ft.Colors.ORANGE_400)
                if val >= 150 and val < 200:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "poor", self._current_language), ft.Colors.RED_400)
                else:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "very_poor", self._current_language), ft.Colors.PURPLE_400)
            #NO2 calculation ranges
            elif pollutant_key == "no2":
                #if no data, return "N/A"
                if val < 0 or val is None:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "na", self._current_language), ft.Colors.GREY_400)
                if val >= 0 and val < 40:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "good", self._current_language), ft.Colors.GREEN_400)
                elif val >= 40 and val < 70:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "fair", self._current_language), ft.Colors.YELLOW_400)
                elif val >= 70 and val < 150:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "moderate", self._current_language), ft.Colors.ORANGE_400)
                if val >= 150 and val < 200:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "poor", self._current_language), ft.Colors.RED_400)
                else:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "very_poor", self._current_language), ft.Colors.PURPLE_400)
            #PM2_5 calculation ranges
            elif pollutant_key  == "pm2_5":
                if val < 0 or val is None:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "na", self._current_language), ft.Colors.GREY_400)
                if val >= 0 and val < 10:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "good", self._current_language), ft.Colors.GREEN_400)
                elif val >= 10 and val < 25:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "fair", self._current_language), ft.Colors.YELLOW_400)
                elif val >= 25 and val < 50:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "moderate", self._current_language), ft.Colors.ORANGE_400)
                if val >= 50 and val < 75:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "poor", self._current_language), ft.Colors.RED_400)
                else:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "very_poor", self._current_language), ft.Colors.PURPLE_400)
            #PM10 calculation ranges
            if pollutant_key == "pm10":
                if val < 0 or val is None:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "na", self._current_language), ft.Colors.GREY_400)
                if val >= 0 and val < 20:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "good", self._current_language), ft.Colors.GREEN_400)
                elif val >= 20 and val < 50:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "fair", self._current_language), ft.Colors.YELLOW_400)
                elif val >= 50 and val < 100:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "moderate", self._current_language), ft.Colors.ORANGE_400)
                if val >= 100 and val < 200:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "poor", self._current_language), ft.Colors.RED_400)
                else:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "very_poor", self._current_language), ft.Colors.PURPLE_400)
            #O3 calculation ranges
            elif pollutant_key == "o3":
                if val < 0 or val is None:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "na", self._current_language), ft.Colors.GREY_400)
                if val >= 0 and val < 60:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "good", self._current_language), ft.Colors.GREEN_400)
                elif val >= 60 and val < 100:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "fair", self._current_language), ft.Colors.YELLOW_400)
                elif val >= 100 and val < 140:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "moderate", self._current_language), ft.Colors.ORANGE_400)
                if val >= 140 and val < 180:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "poor", self._current_language), ft.Colors.RED_400)
                else:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "very_poor", self._current_language), ft.Colors.PURPLE_400)
            #NH3 calculation ranges
            elif pollutant_key == "nh3":
                if val < 0 or val is None:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "na", self._current_language), ft.Colors.GREY_400)
                if val >= 0 and val < 10:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "good", self._current_language), ft.Colors.GREEN_400)
                elif val >= 10 and val < 20:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "fair", self._current_language), ft.Colors.YELLOW_400)
                elif val >= 20 and val < 50:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "moderate", self._current_language), ft.Colors.ORANGE_400)
                if val >= 50 and val < 100:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "poor", self._current_language), ft.Colors.RED_400)
                else:
                    return (translation_manager.get_translation("air_quality", "quality_levels", "very_poor", self._current_language), ft.Colors.PURPLE_400)
            else:
                return ("", ft.Colors.TRANSPARENT)
        
        quality_text, quality_color = get_quality_indicator(value, symbol.lower().replace(".", "_"))
        
        quality_badge = ft.Container(
            content=ft.Text(
                quality_text,
                size=10,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.W_600
            ),
            bgcolor=quality_color,
            padding=ft.padding.symmetric(horizontal=6, vertical=2),
            border_radius=8
        )
        
        # Card content
        card_content = ft.Column([
            ft.Row([
                icon_container,
                ft.Container(width=8),
                ft.Column([
                    ft.Text(
                        f"{value:.1f}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=self._current_text_color
                    ),
                    ft.Text(
                        "μg/m³",
                        size=10,
                        color=ft.Colors.with_opacity(0.7, self._current_text_color)
                    )
                ], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=4),  # Spacer
            ft.Row([
                ft.Text(
                    f"{symbol}:",
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=self._current_text_color
                ),
                ft.Container(expand=True),
                quality_badge
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text(
                name,
                size=10,
                color=ft.Colors.with_opacity(0.8, self._current_text_color),
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS
            )
        ], spacing=4)
        
        # Card container
        # Safe theme detection
        if self.page and hasattr(self.page, 'theme_mode'):
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        else:
            is_dark = False
        
        return ft.Container(
            content=card_content,
            width=None,  # Let container expand based on available space
            height=110,   # Slightly reduced height for better grid layout
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
        """Builds a responsive grid layout for pollutant cards (2x4 vertical)."""
        if not cards:
            return ft.Container()
        
        # Ensure we always have 8 cards (add empty ones if needed)
        while len(cards) < 8:
            cards.append(ft.Container())  # Empty placeholder
        
        # Take only first 8 cards to ensure 2x4 grid
        cards = cards[:8]
        
        # Build grid layout with 2 columns (4 rows x 2 columns)
        grid_rows = []
        
        for i in range(0, len(cards), 2):
            row_cards = cards[i:i+2]
            
            # Create containers with equal width
            row_controls = []
            for card in row_cards:
                row_controls.append(
                    ft.Container(
                        content=card,
                        expand=True,
                        alignment=ft.alignment.center
                    )
                )
            
            # Ensure we always have 2 cards per row (add empty container if needed)
            while len(row_controls) < 2:
                row_controls.append(ft.Container(expand=True))
            
            row = ft.Row(
                controls=row_controls,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=16
            )
            grid_rows.append(row)
        
        return ft.Container(
            content=ft.Column(
                controls=grid_rows,
                spacing=14,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.symmetric(
                horizontal=20,
                vertical=10
            )
        )


