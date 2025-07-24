import flet as ft
from core.state_manager import StateManager
from services.location.location_manager_service import LocationManagerService
from services.location.geocoding_service import GeocodingService
from translations import translation_manager
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Constants for better maintainability
@dataclass
class UIConstants:
    """UI constants for consistent design."""
    DIALOG_MIN_WIDTH: int = 600
    DIALOG_MAX_WIDTH: int = 800
    LOCATIONS_LIST_HEIGHT: int = 280
    SEARCH_RESULTS_MAX_HEIGHT: int = 350
    SEARCH_RESULTS_ITEM_HEIGHT: int = 70
    MAX_SEARCH_RESULTS: int = 10
    ANIMATION_DURATION: int = 250
    BORDER_RADIUS_SMALL: int = 6
    BORDER_RADIUS_MEDIUM: int = 8
    BORDER_RADIUS_LARGE: int = 12
    ICON_SIZE_SMALL: int = 16
    ICON_SIZE_MEDIUM: int = 18
    ICON_SIZE_LARGE: int = 24
    BUTTON_HEIGHT: int = 40
    SEARCH_TIMEOUT: int = 15

@dataclass 
class ColorScheme:
    """Color scheme for theming."""
    bg: str
    surface: str
    surface_variant: str
    text: str
    text_secondary: str
    border: str
    accent: str
    success: str
    warning: str
    error: str
    favorite: str


class LocationManagerDialog:
    """Advanced location manager dialog with enhanced UI/UX features."""
    
    def __init__(self, page: ft.Page, update_weather_callback=None, state_manager=None, language=None):
        # Core dependencies
        self.page = page
        self.state_manager = state_manager if state_manager else StateManager(page)
        self.location_service = LocationManagerService()
        self.geocoding_service = GeocodingService()
        self.update_weather_callback = update_weather_callback
        
        # UI constants
        self.ui_constants = UIConstants()
        
        # Theme and language setup
        theme_mode = self.state_manager.get_state("theme_mode")
        self.theme = "dark" if theme_mode == ft.ThemeMode.DARK else "light"
        self.language = language if language else (self.state_manager.get_state("language") or "it")
        
        # Enhanced color management with better organization
        self.colors = self._create_color_scheme()
        
        # Component state management
        self._init_component_state()
        
        # Register observers for reactive UI updates
        self._register_observers()
        
        logger.info(f"LocationManagerDialog initialized - Theme: {self.theme}, Language: {self.language}")
    
    def _create_color_scheme(self) -> ColorScheme:
        """Create appropriate color scheme based on current theme."""
        if self.theme == "dark":
            return ColorScheme(
                bg="#1E1E1E",
                surface="#2D2D2D", 
                surface_variant="#373737",
                text="#FFFFFF",
                text_secondary="#B0B0B0",
                border="#404040",
                accent="#2196F3",
                success="#4CAF50",
                warning="#FF9800", 
                error="#F44336",
                favorite="#FFD700"
            )
        else:
            return ColorScheme(
                bg="#FFFFFF",
                surface="#F5F5F5",
                surface_variant="#EEEEEE", 
                text="#212121",
                text_secondary="#757575",
                border="#E0E0E0",
                accent="#2196F3",
                success="#4CAF50",
                warning="#FF9800",
                error="#F44336", 
                favorite="#FFD700"
            )
    
    def _init_component_state(self):
        """Initialize component state variables."""
        # Dialog components
        self.dialog = None
        self.locations_list = None
        
        # Search components  
        self.city_field = None
        self.state_field = None
        self.country_field = None
        self.search_button = None
        self.search_results_container = None
        self.is_searching = False
        
        # Secondary dialogs
        self.stats_dialog = None
        
        # Performance optimization - cache frequently used translations
        self._translation_cache = {}
    
    def _register_observers(self):
        """Register state observers for reactive updates."""
        self.state_manager.register_observer("language_event", self._handle_language_change)
        self.state_manager.register_observer("theme_event", self._handle_theme_change)
    
    def _get_field_value(self, field, allow_empty=False):
        """Safely extract and clean field value with improved error handling."""
        if not field or not hasattr(field, 'value'):
            return None if allow_empty else ""
        
        try:
            value = field.value
            if value is None:
                return None if allow_empty else ""
                
            cleaned_value = str(value).strip()
            return cleaned_value if cleaned_value or allow_empty else (None if allow_empty else "")
            
        except (AttributeError, TypeError, ValueError) as e:
            logger.warning(f"Error extracting field value: {e}")
            return None if allow_empty else ""
    
    def _get_country_name(self, country_code: str) -> str:
        """Convert country code to localized full name with enhanced coverage."""
        # Extended country mapping with more comprehensive coverage
        country_names = {
            # European countries
            "IT": "Italia", "FR": "Francia", "ES": "Spagna", "DE": "Germania",
            "GB": "Regno Unito", "UK": "Regno Unito", "CH": "Svizzera", "AT": "Austria", 
            "NL": "Paesi Bassi", "BE": "Belgio", "PT": "Portogallo", "GR": "Grecia", 
            "PL": "Polonia", "CZ": "Repubblica Ceca", "HU": "Ungheria", "RO": "Romania", 
            "BG": "Bulgaria", "HR": "Croazia", "SI": "Slovenia", "SK": "Slovacchia", 
            "LT": "Lituania", "LV": "Lettonia", "EE": "Estonia", "FI": "Finlandia", 
            "SE": "Svezia", "NO": "Norvegia", "DK": "Danimarca", "IE": "Irlanda", 
            "LU": "Lussemburgo", "MT": "Malta", "CY": "Cipro", "IS": "Islanda",
            
            # Major world countries
            "US": "Stati Uniti", "CA": "Canada", "MX": "Messico", "BR": "Brasile",
            "AR": "Argentina", "CL": "Cile", "PE": "Perù", "CO": "Colombia",
            "AU": "Australia", "NZ": "Nuova Zelanda", "JP": "Giappone", "KR": "Corea del Sud",
            "CN": "Cina", "IN": "India", "RU": "Russia", "TR": "Turchia", "EG": "Egitto",
            "ZA": "Sudafrica", "NG": "Nigeria", "KE": "Kenya", "MA": "Marocco",
            "IL": "Israele", "AE": "Emirati Arabi Uniti", "SA": "Arabia Saudita",
            "TH": "Tailandia", "VN": "Vietnam", "ID": "Indonesia", "MY": "Malesia",
            "SG": "Singapore", "PH": "Filippine"
        }
        
        if not country_code:
            return "Sconosciuto"
            
        return country_names.get(country_code.upper(), country_code.upper())
    
    def _handle_theme_change(self, event=None):
        """Handle theme change events with optimized updates."""
        if event and event.get("type") == "theme_event":
            theme_mode = event.get("data")
            self.theme = "dark" if theme_mode == ft.ThemeMode.DARK else "light"
            self.colors = self._create_color_scheme()
            self._clear_translation_cache()  # Clear cache on theme change
            
            if self.dialog and self.dialog.open:
                self._refresh_dialog_ui()
    
    def _handle_language_change(self, event=None):
        """Handle language change events with optimized updates."""
        if event and event.get("type") == "language_event":
            self.language = event.get("data", "italian")
            self._clear_translation_cache()  # Clear cache on language change
            
            if self.dialog and self.dialog.open:
                self._refresh_dialog_ui()
    
    # Legacy method kept for backward compatibility
    def update_theme_Colors(self):
        """Legacy method - use _create_color_scheme instead."""
        logger.warning("update_theme_Colors is deprecated, use _create_color_scheme")
        self.colors = self._create_color_scheme()
    
    # Legacy method kept for backward compatibility  
    def update_ui(self, event=None):
        """Legacy method - use specific handlers instead."""
        if event and event.get("type") == "theme_event":
            self._handle_theme_change(event)
        elif event and event.get("type") == "language_event":
            self._handle_language_change(event)
    
    def _clear_translation_cache(self):
        """Clear translation cache for memory optimization."""
        self._translation_cache.clear()
    
    def _refresh_dialog_ui(self):
        """Refresh dialog UI with current theme and language."""
        try:
            if self.page and self.dialog and self.dialog.open:
                # Close current dialog
                self.page.close(self.dialog)
                # Recreate and reopen with new settings
                self.dialog = self.create_dialog()
                self.page.open(self.dialog)
        except Exception as e:
            logger.error(f"Error refreshing dialog UI: {e}")
    
    def show_dialog(self):
        """Show the location manager dialog with enhanced error handling."""
        try:
            # Close any existing dialogs safely
            if self.dialog and self.page:
                self.page.close(self.dialog)
                self.dialog = None
            
            # Create and show new dialog
            self.dialog = self.create_dialog()
            self.page.open(self.dialog)
            logger.info("LocationManagerDialog opened successfully")
            
        except Exception as ex:
            logger.error(f"Error showing dialog: {ex}")
            self._show_error_snackbar(f"Errore apertura dialog: {str(ex)}")
    
    def create_dialog(self):
        """Create the enhanced location manager dialog with improved UI/UX."""
        texts = self.get_texts()
        
        # Calculate responsive dialog width
        dialog_width = min(
            self.ui_constants.DIALOG_MAX_WIDTH, 
            max(self.ui_constants.DIALOG_MIN_WIDTH, self.page.width * 0.9)
        ) if self.page else self.ui_constants.DIALOG_MIN_WIDTH
        
        # Create enhanced search fields with better styling
        self._create_search_fields()
        
        # Create enhanced search results container
        self._create_search_results_container()
        
        return ft.AlertDialog(
            modal=False,
            title=self._create_dialog_title(texts),
            bgcolor=self.colors.bg,
            content=ft.Container(
                width=dialog_width,
                bgcolor=self.colors.bg,
                padding=20,
                content=ft.Column([
                    # Enhanced search section
                    self._create_search_section(),
                    
                    # Search results container
                    self.search_results_container,
                    
                    # Visual separator
                    ft.Divider(
                        color=ft.Colors.with_opacity(0.15, self.colors.text),
                        height=20
                    ),
                    
                    # Enhanced saved locations section
                    self._create_saved_locations_section(texts),
                    
                    # Locations list
                    self.create_locations_list(),
                    
                    # Bottom spacing
                    ft.Container(height=10),

                ], spacing=16, scroll=ft.ScrollMode.AUTO)
            ),
            actions=[
                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=self.get_translation("dialog_buttons.close"),
                    on_click=self.close_dialog,
                    style=ft.ButtonStyle(
                        bgcolor=self.colors.accent,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(
                            radius=self.ui_constants.BORDER_RADIUS_LARGE
                        ),
                        padding=ft.padding.symmetric(horizontal=24, vertical=12)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content_padding=ft.padding.all(8),
            title_padding=ft.padding.all(16),
            open=False,
        )
    
    def _create_dialog_title(self, texts):
        """Create enhanced dialog title with better visual hierarchy."""
        return ft.Row([
            ft.Container(
                content=ft.Icon(
                    ft.Icons.LOCATION_ON_OUTLINED, 
                    color=self.colors.accent, 
                    size=self.ui_constants.ICON_SIZE_LARGE
                ),
                padding=ft.padding.only(right=8)
            ),
            ft.Text(
                texts['dialog_title'], 
                weight=ft.FontWeight.BOLD, 
                color=self.colors.text,
                size=18
            )
        ], spacing=8)
    
    def _create_search_fields(self):
        """Create enhanced search input fields with better UX."""
        field_style = {
            "border_color": self.colors.border,
            "focused_border_color": self.colors.accent,
            "color": self.colors.text,
            "bgcolor": self.colors.surface,
            "border_radius": self.ui_constants.BORDER_RADIUS_MEDIUM,
            "content_padding": ft.padding.symmetric(horizontal=12, vertical=8)
        }
        
        self.city_field = ft.TextField(
            label=self.get_translation("location_manager_dialog.city_label"),
            hint_text=self.get_translation("location_manager_dialog.city_hint"),
            width=180,
            **field_style
        )
        
        self.state_field = ft.TextField(
            label=self.get_translation("location_input_dialog.state_label"),
            hint_text=self.get_translation("location_input_dialog.state_hint"),
            width=140,
            **field_style
        )
        
        self.country_field = ft.TextField(
            label=self.get_translation("location_input_dialog.country_label"),
            hint_text=self.get_translation("location_input_dialog.country_hint"),
            width=130,
            **field_style
        )
        
        self.search_button = ft.ElevatedButton(
            text=self.get_translation("location_manager_dialog.search_button"),
            icon=ft.Icons.SEARCH,
            on_click=self._handle_search_click,
            bgcolor=ft.Colors.with_opacity(0.1, self.colors.accent),
            color=self.colors.accent,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    radius=self.ui_constants.BORDER_RADIUS_MEDIUM
                )
            ),
            width=120,
            height=self.ui_constants.BUTTON_HEIGHT
        )
    
    def _create_search_results_container(self):
        """Create enhanced search results container with better animations."""
        self.search_results_container = ft.Container(
            content=ft.Column([], spacing=6),
            visible=False,
            height=0,
            bgcolor=ft.Colors.with_opacity(0.03, self.colors.text),
            border=ft.border.all(1, ft.Colors.with_opacity(0.12, self.colors.text)),
            border_radius=self.ui_constants.BORDER_RADIUS_MEDIUM,
            padding=12,
            animate=ft.Animation(
                self.ui_constants.ANIMATION_DURATION, 
                ft.AnimationCurve.EASE_OUT
            )
        )
    
    def _create_search_section(self):
        """Create enhanced search section with better visual organization."""
        return ft.Column([
            # Section header with icon and title
            ft.Row([
                ft.Icon(
                    ft.Icons.SEARCH_OUTLINED, 
                    size=self.ui_constants.ICON_SIZE_MEDIUM, 
                    color=self.colors.accent
                ),
                ft.Text(
                    self.get_translation("location_manager_dialog.search_new_location"), 
                    weight=ft.FontWeight.W_600,
                    color=self.colors.text, 
                    size=16
                ),
            ], spacing=8),
            
            # Input fields row with responsive scrolling
            ft.Container(
                content=ft.Row([
                    self.city_field,
                    self.state_field,
                    self.country_field,
                    self.search_button
                ], spacing=12, scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.only(top=8)
            )
        ], spacing=12)
    
    def _create_saved_locations_section(self, texts):
        """Create enhanced saved locations header with action buttons."""
        return ft.Row([
            ft.Icon(
                ft.Icons.BOOKMARK_OUTLINE, 
                size=self.ui_constants.ICON_SIZE_MEDIUM, 
                color=self.colors.success
            ),
            ft.Text(
                texts['saved_locations'], 
                weight=ft.FontWeight.W_600,
                color=self.colors.text, 
                size=16
            ),
            ft.Container(expand=True),
            
            # Action buttons with enhanced styling
            ft.Row([
                self._create_action_button(
                    ft.Icons.BAR_CHART_OUTLINED,
                    texts['stats'],
                    self.show_statistics,
                    self.colors.accent
                ),
                self._create_action_button(
                    ft.Icons.GPS_FIXED,
                    texts['use_current'],
                    self.use_current_location,
                    self.colors.success
                )
            ], spacing=4)
        ], spacing=8)
    
    def _create_action_button(self, icon, tooltip, on_click, color):
        """Create standardized action button with consistent styling."""
        return ft.Container(
            content=ft.IconButton(
                icon=icon,
                tooltip=tooltip,
                on_click=lambda e: on_click(),
                icon_color=color,
                icon_size=self.ui_constants.ICON_SIZE_MEDIUM
            ),
            bgcolor=ft.Colors.with_opacity(0.08, color),
            border_radius=self.ui_constants.BORDER_RADIUS_MEDIUM,
            width=36,
            height=36
        )
    
    def create_locations_list(self):
        """Create enhanced locations list with improved UI/UX and performance."""
        locations_column = ft.Column([], spacing=6, scroll=ft.ScrollMode.AUTO)
        
        # Get locations with enhanced error handling
        try:
            all_locations = self.location_service.get_all_locations()
            logger.info(f"Loading {len(all_locations)} locations for display")
        except Exception as e:
            logger.error(f"Error loading locations: {e}")
            all_locations = []
        
        if not all_locations:
            # Enhanced empty state with better visual design
            locations_column.controls.append(self._create_empty_state())
        else:
            # Sort locations with enhanced logic
            sorted_locations = self._sort_locations(all_locations)
            
            # Create location cards with enhanced design
            for location in sorted_locations:
                location_card = self._create_location_card(location)
                locations_column.controls.append(location_card)
        
        return ft.Container(
            content=locations_column,
            height=self.ui_constants.LOCATIONS_LIST_HEIGHT,
            padding=12,
            border=ft.border.all(
                1, 
                ft.Colors.with_opacity(0.12, self.colors.text)
            ),
            border_radius=self.ui_constants.BORDER_RADIUS_LARGE,
            bgcolor=ft.Colors.with_opacity(0.03, self.colors.text)
        )
    
    def _create_empty_state(self):
        """Create enhanced empty state with better visual hierarchy."""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.LOCATION_OFF_OUTLINED, 
                        size=56, 
                        color=self.colors.text_secondary
                    ),
                    padding=ft.padding.only(bottom=12)
                ),
                ft.Text(
                    self.get_translation("location_manager_dialog.no_saved_locations"), 
                    weight=ft.FontWeight.BOLD, 
                    color=self.colors.text_secondary,
                    text_align=ft.TextAlign.CENTER,
                    size=16
                ),
                ft.Text(
                    self.get_translation("location_manager_dialog.add_location_to_start"), 
                    size=13, 
                    color=self.colors.text_secondary,
                    text_align=ft.TextAlign.CENTER
                )
            ], 
            spacing=10, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=30,
            alignment=ft.alignment.center
        )
    
    def _sort_locations(self, locations):
        """Sort locations with enhanced logic for better UX."""
        return sorted(
            locations, 
            key=lambda x: (
                not x.get('last_selected', False),  # Current location first
                not x.get('favorite', False),       # Then favorites
                x.get('name', '').lower()           # Then alphabetical
            )
        )
    
    def _create_location_card(self, location):
        """Create enhanced location card with improved design and interactions."""
        # Status indicators with enhanced design
        status_indicators = self._create_status_indicators(location)
        
        # Location information with better formatting
        location_info = self._create_location_info(location)
        
        # Action buttons with consistent design
        action_buttons = self._create_location_action_buttons(location)
        
        # Enhanced card styling based on location status
        card_bgcolor = self._get_card_background_color(location)
        
        return ft.Container(
            content=ft.Row([
                # Left side: Status + Info
                ft.Row([
                    status_indicators,
                    ft.Container(width=8),  # Spacing
                    location_info
                ], expand=True),
                
                # Right side: Action buttons
                action_buttons
                
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            padding=16,
            margin=ft.margin.symmetric(vertical=3),
            border=ft.border.all(
                1, 
                ft.Colors.with_opacity(0.12, self.colors.text)
            ),
            border_radius=self.ui_constants.BORDER_RADIUS_LARGE,
            bgcolor=card_bgcolor,
            animate=ft.Animation(
                self.ui_constants.ANIMATION_DURATION, 
                ft.AnimationCurve.EASE_OUT
            )
        )
    
    def _create_status_indicators(self, location):
        """Create enhanced status indicators for location cards."""
        indicators = []
        
        if location.get("last_selected", False):
            indicators.append(
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.MY_LOCATION, 
                        color=self.colors.accent, 
                        size=self.ui_constants.ICON_SIZE_SMALL
                    ),
                    tooltip="Località corrente",
                    bgcolor=ft.Colors.with_opacity(0.15, self.colors.accent),
                    border_radius=self.ui_constants.BORDER_RADIUS_SMALL,
                    padding=4
                )
            )
        
        if location.get("favorite", False):
            indicators.append(
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.STAR, 
                        color=self.colors.favorite, 
                        size=self.ui_constants.ICON_SIZE_SMALL
                    ),
                    tooltip="Preferito",
                    bgcolor=ft.Colors.with_opacity(0.15, self.colors.favorite),
                    border_radius=self.ui_constants.BORDER_RADIUS_SMALL,
                    padding=4
                )
            )
        
        return ft.Container(
            content=ft.Column(indicators, spacing=4),
            width=40,
        )
    
    def _create_location_info(self, location):
        """Create enhanced location information display."""
        info_items = [
            ft.Text(
                location["name"], 
                weight=ft.FontWeight.BOLD, 
                size=14,
                color=self.colors.text
            ),
            ft.Text(
                f"📍 {location['lat']:.4f}, {location['lon']:.4f}", 
                size=11, 
                color=self.colors.text_secondary
            )
        ]
        
        # Add country info if available and meaningful
        country = location.get("country", "").strip()
        if country and country.lower() not in ["unknown", "sconosciuto", ""]:
            country_display = self._get_country_name(country) if len(country) <= 3 else country
            info_items.insert(1, 
                ft.Text(
                    f"🌍 {country_display}", 
                    size=11, 
                    color=self.colors.text_secondary
                )
            )
        
        return ft.Column(info_items, spacing=3, expand=True)
    
    def _create_location_action_buttons(self, location):
        """Create enhanced action buttons for location cards."""
        buttons = []
        
        # Favorite toggle button
        is_favorite = location.get("favorite", False)
        buttons.append(
            self._create_location_button(
                icon=ft.Icons.STAR if is_favorite else ft.Icons.STAR_OUTLINE,
                tooltip=self.get_translation("toggle_favorite"),
                on_click=lambda e, loc_id=location["id"]: self.toggle_favorite(loc_id),
                color=self.colors.favorite if is_favorite else self.colors.text_secondary,
                bg_color=self.colors.favorite if is_favorite else None
            )
        )
        
        # Use location button
        buttons.append(
            self._create_location_button(
                icon=ft.Icons.LOCATION_ON,
                tooltip="Usa località",
                on_click=lambda e, loc=location: self.use_location(loc),
                color=self.colors.accent,
                bg_color=self.colors.accent
            )
        )
        
        # Settings button
        buttons.append(
            self._create_location_button(
                icon=ft.Icons.SETTINGS_OUTLINED,
                tooltip="Impostazioni",
                on_click=lambda e, loc=location: self.show_location_settings(loc),
                color=self.colors.text_secondary
            )
        )
        
        # Delete button
        buttons.append(
            self._create_location_button(
                icon=ft.Icons.DELETE_OUTLINE,
                tooltip="Rimuovi",
                on_click=lambda e, loc_id=location["id"]: self.remove_location(loc_id),
                color=self.colors.error,
                bg_color=self.colors.error
            )
        )
        
        return ft.Row(buttons, spacing=6)
    
    def _create_location_button(self, icon, tooltip, on_click, color, bg_color=None):
        """Create standardized location action button."""
        return ft.Container(
            content=ft.IconButton(
                icon=icon,
                icon_color=color,
                tooltip=tooltip,
                on_click=on_click,
                icon_size=self.ui_constants.ICON_SIZE_MEDIUM
            ),
            width=36,
            height=36,
            border_radius=self.ui_constants.BORDER_RADIUS_MEDIUM,
            bgcolor=ft.Colors.with_opacity(
                0.12 if bg_color else 0.06, 
                bg_color or color
            )
        )
    
    def _get_card_background_color(self, location):
        """Get appropriate background color for location card."""
        if location.get("last_selected", False):
            return ft.Colors.with_opacity(0.08, self.colors.accent)
        else:
            return self.colors.surface
    
    def get_translation(self, key: str) -> str:
        """Get translation with caching for improved performance."""
        # Check cache first
        cache_key = f"{self.language}:{key}"
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]
        
        # Get translation
        if "." in key:
            parts = key.split(".", 1)
            section = parts[0]
            sub_key = parts[1]
            translation = translation_manager.get_translation("weather", section, sub_key, self.language)
        else:
            # Fallback for simple keys
            translation = translation_manager.get_translation("weather", "general", key, self.language)
        
        # Cache and return
        self._translation_cache[cache_key] = translation
        return translation
    
    def get_texts(self):
        """Get localized texts with enhanced caching and organization."""
        base_texts = {
            "title": self.get_translation("location_manager_dialog.title"),
            "dialog_title": self.get_translation("location_manager_dialog.dialog_title"),
            "description": self.get_translation("location_manager_dialog.description"),
            "add_location": self.get_translation("location_manager_dialog.add_location"),
            "saved_locations": self.get_translation("location_manager_dialog.saved_locations"),
            "open_location_input": self.get_translation("location_manager_dialog.open_location_input"),
            "add": self.get_translation("location_manager_dialog.add_button"),
            "use_current": self.get_translation("location_manager_dialog.use_current"),
            "close": self.get_translation("dialog_buttons.close"),
            "stats": self.get_translation("location_manager_dialog.stats"),
            "export": self.get_translation("location_manager_dialog.export"),
            "import": self.get_translation("location_manager_dialog.import")
        }
        
        return base_texts
    
    def _handle_search_click(self, e=None):
        """Enhanced search handler with better UX feedback."""
        try:
            if self.is_searching:
                logger.info("Search already in progress, ignoring duplicate request")
                return
                
            # Validate search fields
            if not self._validate_search_input():
                return
                
            # Clear previous results
            self._clear_search_results()
            
            # Execute search with enhanced feedback
            self._search_locations_sync(e)
            
        except Exception as ex:
            logger.error(f"Error in search handler: {ex}")
            self._show_error_snackbar(f"{self.get_translation('location_manager_dialog.search_error')}: {str(ex)}")
    
    def _validate_search_input(self) -> bool:
        """Validate search input with enhanced user feedback."""
        if not self.city_field or not self.state_field or not self.country_field:
            logger.error("Search fields not initialized")
            self._show_error_snackbar("Errore interno: campi di ricerca non inizializzati")
            return False
            
        city = self._get_field_value(self.city_field)
        if not city or len(city.strip()) < 2:
            self._show_warning_snackbar(
                self.get_translation("location_manager_dialog.enter_city_name")
            )
            self._focus_field(self.city_field)
            return False
            
        return True
    
    def _clear_search_results(self):
        """Clear search results with smooth animation."""
        if self.search_results_container:
            self.search_results_container.visible = False
            self.search_results_container.height = 0
            if self.page:
                self.page.update()
    
    def _focus_field(self, field):
        """Focus on a specific field for better UX."""
        try:
            if field and self.page:
                field.focus()
                self.page.update()
        except Exception as e:
            logger.warning(f"Could not focus field: {e}")
    
    def _search_locations_sync(self, e=None):
        """Enhanced synchronous search with better error handling and feedback."""
        if self.is_searching:
            return
        
        city = self._get_field_value(self.city_field)
        state = self._get_field_value(self.state_field, allow_empty=True)
        country = self._get_field_value(self.country_field, allow_empty=True)
        
        # Set loading state with enhanced UI feedback
        self._set_search_loading_state(True)
        
        try:
            logger.info(f"Starting search for: city='{city}', state='{state}', country='{country}'")
            
            # Perform synchronous geocoding
            results = self._geocode_sync(city, state, country)
            
            if results:
                logger.info(f"Search completed successfully: {len(results)} results found")
                self.display_search_results(results)
                self._show_success_snackbar(
                    f"Trovati {len(results)} risultati per '{city}'"
                )
            else:
                logger.info("Search completed: no results found")
                self._show_search_message(
                    self.get_translation("location_manager_dialog.no_locations_found"), 
                    self.colors.warning
                )
                
        except Exception as ex:
            logger.error(f"Search error: {ex}")
            self._show_search_message(
                f"{self.get_translation('location_manager_dialog.search_error')}: {str(ex)}", 
                self.colors.error
            )
        finally:
            self._set_search_loading_state(False)
    
    def _set_search_loading_state(self, is_loading: bool):
        """Set search loading state with enhanced visual feedback."""
        if not self.search_button:
            return
            
        self.is_searching = is_loading
        
        if is_loading:
            self.search_button.text = self.get_translation("location_manager_dialog.searching")
            self.search_button.icon = ft.Icons.HOURGLASS_EMPTY
            self.search_button.disabled = True
        else:
            self.search_button.text = self.get_translation("location_manager_dialog.search_button")
            self.search_button.icon = ft.Icons.SEARCH
            self.search_button.disabled = False
        
        if self.page:
            self.page.update()
    
    def _geocode_sync(self, city: str, state: str = None, country: str = None):
        """Synchronous geocoding using requests."""
        try:
            import requests
            import os
            from services.location.geocoding_service import LocationCandidate
            
            # Get API key
            api_key = os.getenv("API_KEY")
            if not api_key:
                raise Exception("OpenWeatherMap API key not found in environment variables")
            
            # Build query
            query_parts = [city.strip()]
            if state and state.strip():
                query_parts.append(state.strip())
            if country and country.strip():
                query_parts.append(country.strip())
            
            query = ",".join(query_parts)
            logger.info(f"Geocoding query: {query}")
            
            # Make API call
            url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": query,
                "limit": 5,
                "appid": api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"API returned {len(data)} results")
            
            # Parse response
            candidates = []
            for item in data:
                try:
                    # Extract info from API response
                    name = item.get("name", "")
                    lat = float(item.get("lat", 0))
                    lon = float(item.get("lon", 0))
                    country_code = item.get("country", "")  # This is actually the country code from API
                    state = item.get("state", "")
                    
                    # Get full country name
                    country_name = self._get_country_name(country_code)
                    
                    candidate = LocationCandidate(
                        name=name,
                        country=country_name,
                        country_code=country_code,
                        state=state,
                        lat=lat,
                        lon=lon
                    )
                    candidates.append(candidate)
                except Exception as e:
                    logger.warning(f"Error parsing location item: {e}")
                    continue
            
            return candidates
            
        except requests.exceptions.Timeout:
            logger.error("Geocoding API timeout")
            raise Exception("Search timeout - please try again")
        except requests.exceptions.ConnectionError:
            logger.error("Geocoding API connection error")
            raise Exception("Connection error - check your internet connection")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Geocoding API HTTP error: {e}")
            raise Exception(f"API error: {e}")
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            raise
    
    async def _run_search_async(self):
        """Run the async search in a thread-safe manner."""
        await self.search_locations()
    
    async def search_locations(self, e=None):
        """Search for locations using the integrated search."""
        if self.is_searching:
            return
        
        # Ensure fields are initialized
        if not self.city_field or not self.state_field or not self.country_field:
            logger.error("Search fields not initialized. Dialog must be shown first.")
            return
            
        city = self._get_field_value(self.city_field)
        if not city:
            self.show_snackbar(self.get_translation("location_manager_dialog.enter_city_name"), "#FF9800")
            return
        
        self.is_searching = True
        self.search_button.text = self.get_translation("location_manager_dialog.searching")
        self.search_button.disabled = True
        self.page.update()
        
        try:
            # Prepara query di ricerca strutturata
            state = self._get_field_value(self.state_field, allow_empty=True)
            country = self._get_field_value(self.country_field, allow_empty=True)
            
            # Esegui ricerca
            results = await self.geocoding_service.search_by_structured_input(city, state, country)
            
            if results:
                self.display_search_results(results)
            else:
                self.show_search_message(self.get_translation("location_manager_dialog.no_locations_found"), "#FF9800")
                
        except Exception as ex:
            logger.error(f"Errore durante la ricerca: {ex}")
            self.show_search_message(f"{self.get_translation('location_manager_dialog.search_error')}: {str(ex)}", "#F44336")
        finally:
            self.is_searching = False
            self.search_button.text = self.get_translation("location_manager_dialog.search_button")
            self.search_button.disabled = False
            self.page.update()
    
    def display_search_results(self, results):
        """Display search results with enhanced UI design and animations."""
        if not self.search_results_container or not results:
            return
            
        results_column = ft.Column([], spacing=8)
        
        # Enhanced header with result count and styling
        header = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.SEARCH_OUTLINED, 
                    size=self.ui_constants.ICON_SIZE_MEDIUM,
                    color=self.colors.accent
                ),
                ft.Text(
                    f"Trovati {len(results)} risultati:", 
                    weight=ft.FontWeight.BOLD, 
                    color=self.colors.text, 
                    size=15
                )
            ], spacing=8),
            padding=ft.padding.only(bottom=8)
        )
        results_column.controls.append(header)
        
        # Limit results for better performance and UX
        display_results = results[:self.ui_constants.MAX_SEARCH_RESULTS]
        if len(results) > self.ui_constants.MAX_SEARCH_RESULTS:
            logger.info(f"Limiting display to {self.ui_constants.MAX_SEARCH_RESULTS} of {len(results)} results")
        
        # Create enhanced result cards
        for i, candidate in enumerate(display_results):
            result_card = self._create_search_result_card(candidate, i)
            results_column.controls.append(result_card)
        
        # Add truncation notice if needed
        if len(results) > self.ui_constants.MAX_SEARCH_RESULTS:
            truncation_notice = ft.Container(
                content=ft.Text(
                    f"... e altri {len(results) - self.ui_constants.MAX_SEARCH_RESULTS} risultati. Affina la ricerca per risultati più precisi.",
                    size=11,
                    color=self.colors.text_secondary,
                    italic=True
                ),
                padding=ft.padding.only(top=8)
            )
            results_column.controls.append(truncation_notice)
        
        # Update container with smooth animation
        self.search_results_container.content = results_column
        self.search_results_container.visible = True
        self.search_results_container.height = min(
            self.ui_constants.SEARCH_RESULTS_MAX_HEIGHT,
            len(display_results) * self.ui_constants.SEARCH_RESULTS_ITEM_HEIGHT + 80
        )
        
        if self.page:
            self.page.update()
    
    def _create_search_result_card(self, candidate, index):
        """Create enhanced search result card with improved design."""
        return ft.Container(
            content=ft.Row([
                # Result information with enhanced layout
                ft.Column([
                    ft.Text(
                        candidate.full_name, 
                        weight=ft.FontWeight.BOLD,
                        size=14, 
                        color=self.colors.text
                    ),
                    ft.Row([
                        ft.Text(
                            f"📍 {candidate.lat:.4f}, {candidate.lon:.4f}", 
                            size=11, 
                            color=self.colors.text_secondary
                        ),
                        ft.Container(width=8),
                        ft.Text(
                            f"� {candidate.country_code}", 
                            size=11, 
                            color=self.colors.text_secondary
                        )
                    ], spacing=0)
                ], spacing=4, expand=True),
                
                # Enhanced add button
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ADD, size=16),
                            ft.Text("Aggiungi", size=12)
                        ], spacing=4, tight=True),
                        on_click=lambda e, loc=candidate: self.add_location_from_search(loc),
                        bgcolor=ft.Colors.with_opacity(0.1, self.colors.success),
                        color=self.colors.success,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(
                                radius=self.ui_constants.BORDER_RADIUS_MEDIUM
                            ),
                            padding=ft.padding.symmetric(horizontal=12, vertical=8)
                        ),
                        height=36
                    )
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            padding=12,
            margin=ft.margin.symmetric(vertical=2),
            border=ft.border.all(
                1, 
                ft.Colors.with_opacity(0.12, self.colors.text)
            ),
            border_radius=self.ui_constants.BORDER_RADIUS_MEDIUM,
            bgcolor=self.colors.surface_variant,
            animate=ft.Animation(
                self.ui_constants.ANIMATION_DURATION, 
                ft.AnimationCurve.EASE_OUT
            )
        )
    
    def show_search_message(self, message, color):
        """Show enhanced message in search results with better visual design."""
        # Determine appropriate icon based on message type
        if "errore" in message.lower() or "error" in message.lower():
            icon = ft.Icons.ERROR_OUTLINE
        elif "nessun" in message.lower() or "no " in message.lower():
            icon = ft.Icons.SEARCH_OFF
        else:
            icon = ft.Icons.INFO_OUTLINE
        
        message_content = ft.Column([
            ft.Container(
                content=ft.Icon(icon, size=40, color=color),
                padding=ft.padding.only(bottom=12)
            ),
            ft.Text(
                message, 
                text_align=ft.TextAlign.CENTER, 
                color=color,
                size=14,
                weight=ft.FontWeight.W_500
            )
        ], 
        spacing=8, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.search_results_container.content = ft.Container(
            content=message_content,
            padding=20,
            alignment=ft.alignment.center
        )
        self.search_results_container.visible = True
        self.search_results_container.height = 120
        
        if self.page:
            self.page.update()
    
    # Legacy method kept for backward compatibility
    def show_search_message_old(self, message, color):
        """Legacy method - use show_search_message instead."""
        self.show_search_message(message, color)
    
    def add_location_from_search(self, candidate):
        """Add location from search results with enhanced feedback and validation."""
        try:
            # Validate candidate
            if not candidate or not hasattr(candidate, 'full_name'):
                logger.error("Invalid candidate provided")
                self._show_error_snackbar("Errore: candidato non valido")
                return
            
            logger.info(f"Adding location: {candidate.full_name}")
            
            # Add location using service
            result = self.location_service.add_location(
                name=candidate.full_name,
                lat=candidate.lat,
                lon=candidate.lon,
                country=candidate.country_code
            )
            
            if result:
                logger.info(f"Location added successfully: {candidate.full_name}")
                
                # Reload locations
                self.location_service.load_locations()
                
                # Clear search with smooth animation
                self.clear_search()
                
                # Refresh locations list
                self.refresh_locations_list()
                
                # Show success notification
                self._show_success_snackbar(
                    f"{self.get_translation('location_manager_dialog.location_added_successfully')}: {candidate.full_name}"
                )
                
                # Update main UI if callback is available
                if self.update_weather_callback:
                    try:
                        # Get current settings for the callback
                        language = self.language or "it"
                        unit = self.state_manager.get_state("unit") or "metric"
                        
                        # Call the callback with proper async handling
                        if hasattr(self.page, 'run_task'):
                            self.page.run_task(self.update_weather_callback, candidate.full_name, language, unit)
                        else:
                            logger.warning("Page doesn't support run_task, skipping weather update")
                    except Exception as e:
                        logger.warning(f"Weather callback error: {e}")
                        
            else:
                self._show_warning_snackbar(
                    self.get_translation('location_manager_dialog.location_already_exists')
                )
                
        except Exception as e:
            logger.error(f"Error adding location: {e}")
            self._show_error_snackbar(
                f"{self.get_translation('location_manager_dialog.error_adding_location')}: {str(e)}"
            )
    
    def clear_search(self):
        """Clear search results and reset form with enhanced UX."""
        if self.search_results_container:
            self.search_results_container.visible = False
            self.search_results_container.height = 0
            
        # Clear form fields
        if self.city_field:
            self.city_field.value = ""
        if self.state_field:
            self.state_field.value = ""
        if self.country_field:
            self.country_field.value = ""
            
        if self.page:
            self.page.update()
    
    def refresh_locations_list(self):
        """Enhanced refresh that updates only the locations list for better performance."""
        try:
            if not self.dialog or not self.dialog.content:
                logger.warning("Dialog not available for refresh")
                return
                
            # Get the main column container
            main_column = self.dialog.content.content
            if not hasattr(main_column, 'controls'):
                logger.warning("Dialog structure unexpected")
                return
            
            # Find and update the locations list container
            # The locations list should be the second-to-last control (before the bottom spacing)
            locations_list_index = -2  # Second to last position
            
            if len(main_column.controls) > abs(locations_list_index):
                # Create new locations list
                new_locations_list = self.create_locations_list()
                
                # Replace the old list with the new one
                main_column.controls[locations_list_index] = new_locations_list
                
                # Update the page
                if self.page:
                    self.page.update()
                    
                logger.info("Locations list refreshed successfully")
            else:
                logger.warning("Could not find locations list in dialog structure")
                
        except Exception as ex:
            logger.error(f"Error refreshing locations list: {ex}")
            logger.info("Attempting fallback: partial dialog refresh")
            # Enhanced fallback: try to refresh dialog UI instead of full recreation
            self._refresh_dialog_ui()
    
    def toggle_favorite(self, location_id: str):
        """Toggle favorite status using professional service."""
        try:
            location = self.location_service.get_location_by_id(location_id)
            if not location:
                return
                
            # Usa il metodo toggle_favorite del servizio invece di set_favorite
            success = self.location_service.toggle_favorite(location_id)
            
            if success and self.page:
                # Ottieni lo stato aggiornato dopo il toggle
                updated_location = self.location_service.get_location_by_id(location_id)
                is_favorite = updated_location.get("favorite", False) if updated_location else False
                status_text = self.get_translation("added_to_favorites") if is_favorite else self.get_translation("removed_from_favorites")
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Località {status_text} {self.get_translation('favorites')}"),
                    bgcolor=self.colors.accent
                )
                self.page.snack_bar.open = True
                self.page.update()
                
                # Refresh only the locations list instead of the entire dialog
                self.refresh_locations_list()
            
        except Exception as ex:
            logger.error(f"Errore nel toggle favorite: {ex}")
    
    def refresh_dialog_safely(self):
        """Safely refresh the dialog without causing overlay issues."""
        try:
            if self.dialog and self.page:
                # Instead of closing and reopening, just refresh the locations list
                self.refresh_locations_list()
                logger.info("Dialog refreshed by updating locations list only")
                
        except Exception as ex:
            logger.error(f"Errore durante il refresh sicuro del dialog: {ex}")
            # Fallback to full refresh only if list refresh fails
            try:
                self.page.close(self.dialog)
                self.dialog = self.create_dialog()
                self.page.open(self.dialog)
            except Exception as fallback_ex:
                logger.error(f"Fallback refresh failed: {fallback_ex}")
    
    def use_location(self, location):
        """Use selected location as current location."""
        try:
            # Seleziona la località nel servizio
            success = self.location_service.select_location(location['id'])
            
            if success:
                # Aggiorna lo stato nell'app principale usando il metodo sincrono
                if self.state_manager:
                    self.state_manager.set_state_sync('current_lat', location['lat'])
                    self.state_manager.set_state_sync('current_lon', location['lon'])
                    self.state_manager.set_state_sync('current_city', location['name'])
                
                # Triggerare l'aggiornamento completo dell'UI
                if self.update_weather_callback:
                    # Ottieni impostazioni correnti
                    language = self.state_manager.get_state("language") or "it"
                    unit = self.state_manager.get_state("unit") or "metric"
                    
                    # Chiama il callback per aggiornare l'UI usando run_task di Flet
                    self.page.run_task(self._update_ui_async, location['name'], language, unit)
                
                # Show success feedback
                self._show_success_snackbar(f"Località selezionata: {location['name']}")
                
                # Refresh the locations list to show the new current location
                self.refresh_locations_list()
                
                # Close dialog after a brief moment to allow user to see the feedback
                if self.page:
                    import asyncio
                    async def delayed_close():
                        await asyncio.sleep(1.5)  # 1.5 second delay
                        self.close_dialog()
                    
                    self.page.run_task(delayed_close)
                
        except Exception as ex:
            logger.error(f"Errore nell'uso della località: {ex}")
            self._show_error_snackbar(f"Errore nell'uso della località: {str(ex)}")
    
    async def _update_ui_async(self, city_name, language, unit):
        """Aggiorna l'UI in modo asincrono."""
        try:
            if self.update_weather_callback:
                result = await self.update_weather_callback(city_name, language, unit)
                if result:
                    logger.info(f"UI aggiornata con successo per: {city_name}")
                else:
                    logger.warning(f"Errore nell'aggiornamento UI per: {city_name}")
        except Exception as ex:
            logger.error(f"Errore nell'aggiornamento asincrono: {ex}")
    
    def remove_location(self, location_id: str):
        """Remove a location using professional service."""
        try:
            location = self.location_service.get_location_by_id(location_id)
            if not location:
                return
                
            location_name = location['name']
            success = self.location_service.remove_location(location_id)
            
            if success and self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"{self.get_translation('location_manager_dialog.location_removed')}: '{location_name}'"),
                    bgcolor="#F44336"
                )
                self.page.snack_bar.open = True
                self.page.update()
                
            # Refresh dialog
            self.show_dialog()
            
        except Exception as ex:
            logger.error(f"Errore nella rimozione della località: {ex}")
    
    def show_location_settings(self, location):
        """Show location-specific settings dialog."""
        # Per ora mostra solo un messaggio, in futuro implementeremo il dialog completo
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Configurazioni per {location['name']} (in sviluppo)"),
                bgcolor=self.colors.accent
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def show_statistics(self):
        """Show location statistics dialog."""
        try:
            stats = self.location_service.get_statistics()
            
            stats_content = ft.Column([
                ft.Text("Statistiche Località", weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(),
                ft.Text(f"📍 Totale località: {stats['total_locations']}"),
                ft.Text(f"⭐ Località preferite: {stats['favorite_locations']}"),
                ft.Text(f"🗂️ File storage: {stats['storage_size_bytes']} bytes"),
                
                ft.Text("📊 Paesi rappresentati:", weight=ft.FontWeight.BOLD, size=14),
                *[ft.Text(f"  🏳️ {country}: {count}") 
                  for country, count in stats['countries'].items()],
                
            ], spacing=8)
            
            self.stats_dialog = ft.AlertDialog(
                title=ft.Text("Statistiche"),
                content=ft.Container(content=stats_content, width=300),
                actions=[ft.TextButton("Chiudi", on_click=lambda e: self.close_stats_dialog())]
            )
            
            self.page.open(self.stats_dialog)
            
        except Exception as e:
            logger.error(f"Errore durante la visualizzazione delle statistiche: {e}")
            self.show_snackbar("Errore durante il caricamento delle statistiche")
    
    def refresh_locations(self):
        """Refresh the locations list."""
        try:
            logger.info("Refreshing locations list")
            self.show_dialog()  # Ricarica completamente il dialog
            self.show_snackbar("Lista località aggiornata!", "#4CAF50")
        except Exception as e:
            logger.error(f"Errore durante l'aggiornamento: {e}")
            self.show_snackbar("Errore durante l'aggiornamento")
    
    def export_locations(self):
        """Export locations to a file."""
        try:
            all_locations = self.location_service.get_all_locations()
            if not all_locations:
                self.show_snackbar("Nessuna località da esportare")
                return
            
            # Simulazione esportazione (in futuro potresti implementare il salvataggio file)
            export_count = len(all_locations)
            logger.info(f"Exported {export_count} locations")
            self.show_snackbar(f"Esportate {export_count} località!", "#4CAF50")
            
        except Exception as e:
            logger.error(f"Errore durante l'esportazione: {e}")
            self.show_snackbar("Errore durante l'esportazione")
    
    def close_stats_dialog(self):
        """Close statistics dialog properly."""
        try:
            if self.stats_dialog and self.page:
                self.page.close(self.stats_dialog)
                self.stats_dialog = None
                
        except Exception as ex:
            logger.error(f"Errore durante la chiusura del stats dialog: {ex}")
    
    def use_current_location(self):
        """Use current GPS location."""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Funzionalità GPS in sviluppo"),
                bgcolor=self.colors.accent
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def close_dialog(self, e=None):
        """Enhanced dialog closure with proper cleanup and error handling."""
        try:
            logger.info("Closing LocationManagerDialog")
            
            # Close secondary dialogs first
            if self.stats_dialog and self.page:
                try:
                    self.page.close(self.stats_dialog)
                    self.stats_dialog = None
                    logger.info("Stats dialog closed")
                except Exception as ex:
                    logger.warning(f"Error closing stats dialog: {ex}")
            
            # Close main dialog
            if self.dialog and self.page:
                try:
                    self.page.close(self.dialog)
                    self.dialog = None
                    logger.info("Main dialog closed successfully")
                except Exception as ex:
                    logger.warning(f"Error closing main dialog: {ex}")
            
            # Clear component references for memory optimization
            self._clear_component_references()
            
            logger.info("LocationManagerDialog closed successfully")
            
        except Exception as ex:
            logger.error(f"Error during dialog closure: {ex}")
            # Fallback cleanup
            self._force_cleanup()
    
    def _clear_component_references(self):
        """Clear component references for memory optimization."""
        try:
            self.city_field = None
            self.state_field = None
            self.country_field = None
            self.search_button = None
            self.search_results_container = None
            self.locations_list = None
            self.is_searching = False
        except Exception as e:
            logger.warning(f"Error clearing component references: {e}")
    
    def _force_cleanup(self):
        """Force cleanup in case of errors."""
        try:
            if self.page:
                # Try to close any open dialogs
                for dialog_attr in ['dialog', 'stats_dialog']:
                    dialog = getattr(self, dialog_attr, None)
                    if dialog:
                        try:
                            self.page.close(dialog)
                            setattr(self, dialog_attr, None)
                        except Exception:
                            pass
        except Exception as e:
            logger.error(f"Error in force cleanup: {e}")

    def _show_success_snackbar(self, message: str):
        """Show success snackbar with consistent styling."""
        self._show_snackbar(message, self.colors.success, ft.Icons.CHECK_CIRCLE_OUTLINE)
    
    def _show_warning_snackbar(self, message: str):
        """Show warning snackbar with consistent styling."""
        self._show_snackbar(message, self.colors.warning, ft.Icons.WARNING_OUTLINED)
    
    def _show_error_snackbar(self, message: str):
        """Show error snackbar with consistent styling."""
        self._show_snackbar(message, self.colors.error, ft.Icons.ERROR_OUTLINE)
    
    def _show_snackbar(self, message: str, color: str, icon=None):
        """Enhanced snackbar with consistent design and icons."""
        if not self.page:
            return
            
        content = ft.Row([
            ft.Icon(icon, color=ft.Colors.WHITE, size=20) if icon else ft.Container(),
            ft.Text(message, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
        ], spacing=8, tight=True)
        
        self.page.snack_bar = ft.SnackBar(
            content=content,
            bgcolor=color,
            duration=3000,
            show_close_icon=True
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    # Legacy method for backward compatibility
    def show_snackbar(self, message, color="#4CAF50"):
        """Legacy method - use specific snackbar methods instead."""
        if color == "#4CAF50":
            self._show_success_snackbar(message)
        elif color in ["#FF9800", "#FFC107"]:
            self._show_warning_snackbar(message)
        elif color in ["#F44336", "#D32F2F"]:
            self._show_error_snackbar(message)
        else:
            self._show_snackbar(message, color)

    def cleanup(self):
        """Enhanced cleanup with comprehensive resource management."""
        try:
            logger.info("Starting LocationManagerDialog cleanup")
            
            # Close all dialogs
            self.close_dialog()
            
            # Unregister observers to prevent memory leaks
            if self.state_manager:
                try:
                    self.state_manager.unregister_observer("language_event", self._handle_language_change)
                    self.state_manager.unregister_observer("theme_event", self._handle_theme_change)
                    # Legacy observers for backward compatibility
                    self.state_manager.unregister_observer("language_event", self.update_ui)
                    self.state_manager.unregister_observer("theme_event", self.update_ui)
                    logger.info("State observers unregistered")
                except Exception as ex:
                    logger.warning(f"Error unregistering observers: {ex}")
            
            # Clear translation cache
            self._clear_translation_cache()
            
            # Clear component references
            self._clear_component_references()
            
            logger.info("LocationManagerDialog cleanup completed successfully")
            
        except Exception as ex:
            logger.error(f"Error during cleanup: {ex}")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except Exception:
            pass  # Ignore errors in destructor
