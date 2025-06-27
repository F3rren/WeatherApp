import flet as ft
import logging
import traceback
from services.api_service import ApiService
from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class AirPollutionDisplay(ft.Container):
    """
    Air pollution display component.
    Shows detailed air quality information.
    Manages its own UI construction, updates, and state observers.
    """
    
    def __init__(self, page: ft.Page, lat: float = None, lon: float = None, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self._lat = lat
        self._lon = lon
        
        self._api_service = ApiService()
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._pollution_data = {}

        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20, 'label': 15, 'value': 15, 
                'subtitle': 15, 'aqi_value': 16
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._state_manager.register_observer("language_event", lambda e=None: self.page.run_task(self.update_ui, e))
            self._state_manager.register_observer("theme_event", lambda e=None: self.page.run_task(self.update_ui, e))
        
        if self.page:
            original_on_resize = self.page.on_resize
            def resize_handler(e):
                if original_on_resize:
                    original_on_resize(e)
                if self._text_handler:
                    self._text_handler._handle_resize(e)
                # Trigger UI rebuild on resize for responsive grid
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
                new_language = self._state_manager.get_state('language') or self._current_language
                language_changed = self._current_language != new_language
                self._current_language = new_language
                data_changed = language_changed

            if not self._pollution_data or data_changed:
                if self._lat is not None and self._lon is not None:
                    self._pollution_data = await self._api_service.get_air_pollution_async(self._lat, self._lon) or {}
                else:
                    self._pollution_data = {}

            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._current_text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            # Only update if this control is already in the page
            try:
                if self.page and hasattr(self, 'page') and self.page is not None:
                    self.update()
            except Exception:
                # Control not yet added to page, update will happen when added
                pass
        except Exception as e:
            logging.error(f"AirPollutionDisplay: Error updating UI: {e}\n{traceback.format_exc()}")

    def build(self):
        """Constructs modern, card-based UI for air pollution data."""
        if not self._pollution_data or "aqi" not in self._pollution_data:
            loading_text = TranslationService.translate_from_dict("air_pollution_items", "no_air_pollution_data", self._current_language)
            return ft.Column([
                self._build_header(),
                ft.Container(
                    content=ft.Text(
                        loading_text,
                        color=self._current_text_color,
                        size=self._text_handler.get_size('label')
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

    def _build_header(self):
        """Builds a modern header for air pollution section."""
        header_text = TranslationService.translate_from_dict("air_pollution_items", "air_quality_index", self._current_language)
        
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.AIR_OUTLINED,
                    color=ft.Colors.GREEN_400 if not is_dark else ft.Colors.GREEN_300,
                    size=24
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    header_text,
                    size=self._text_handler.get_size('axis_title') + 2,
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=20, bottom=10)
        )
    
    def _build_header_with_aqi(self, aqi):
        """Builds header with AQI badge."""
        header_text = TranslationService.translate_from_dict("air_pollution_items", "air_quality_index", self._current_language)
        
        # Get AQI description and color
        from utils.translations_data import TRANSLATIONS
        lang_code = TranslationService.normalize_lang_code(self._current_language)
        aqi_descriptions = TRANSLATIONS.get(lang_code, {}).get("air_pollution_items", {}).get("aqi_descriptions")
        if not aqi_descriptions:
            aqi_descriptions = TRANSLATIONS.get("en", {}).get("air_pollution_items", {}).get("aqi_descriptions", ["N/A"] * 6)
        aqi_idx = min(max(aqi, 0), 5)
        aqi_desc = aqi_descriptions[aqi_idx] if aqi_idx < len(aqi_descriptions) else "N/A"
        
        # AQI colors
        aqi_colors = ["#D3D3D3", "#00E400", "#FFFF00", "#FF7E00", "#FF0000", "#99004C"]
        aqi_color_idx = max(0, min(aqi, len(aqi_colors) - 1))
        aqi_color = aqi_colors[aqi_color_idx]
        
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.AIR_OUTLINED,
                    color=ft.Colors.GREEN_400 if not is_dark else ft.Colors.GREEN_300,
                    size=24
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    header_text,
                    size=self._text_handler.get_size('axis_title') + 2,
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
            name = TranslationService.translate_from_dict("air_pollution_items", key.upper().replace("_", "."), self._current_language)
            
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
        
        # Quality indicator based on value ranges (simplified)
        def get_quality_indicator(val, pollutant_key):
            if pollutant_key in ["pm2_5", "pm10"]:
                if val < 12:
                    return ("Good", ft.Colors.GREEN_400)
                elif val < 35:
                    return ("Moderate", ft.Colors.ORANGE_400)
                else:
                    return ("Poor", ft.Colors.RED_400)
            elif pollutant_key == "o3":
                if val < 100:
                    return ("Good", ft.Colors.GREEN_400)
                elif val < 160:
                    return ("Moderate", ft.Colors.ORANGE_400)
                else:
                    return ("Poor", ft.Colors.RED_400)
            else:
                # Generic ranges for other pollutants
                if val < 50:
                    return ("Good", ft.Colors.GREEN_400)
                elif val < 100:
                    return ("Moderate", ft.Colors.ORANGE_400)
                else:
                    return ("Poor", ft.Colors.RED_400)
        
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
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
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
        
        # Determine grid layout based on screen size
        grid_rows = []
        
        # Check if small screen (less than 600px)
        is_small_screen = (self.page.window.width < 600) if (self.page.window.width and self.page.window.width > 0) else False
        
        if is_small_screen:
            # Single column layout for small screens (8 rows x 1 column)
            for card in cards:
                row = ft.Row(
                    controls=[
                        ft.Container(
                            content=card,
                            expand=True,
                            alignment=ft.alignment.center
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
                grid_rows.append(row)
        else:
            # Two-column layout for larger screens (4 rows x 2 columns)
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
                    spacing=16 if (self.page.window.width and self.page.window.width > 900) else 12
                )
                grid_rows.append(row)
        
        return ft.Container(
            content=ft.Column(
                controls=grid_rows,
                spacing=14,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.symmetric(
                horizontal=20 if (self.page.window.width and self.page.window.width > 600) else 15,
                vertical=10
            )
        )
               

