import logging
import flet as ft
import webbrowser

class MapView:
    """
    A view component to display a weather map using WebView with enhanced error handling and theming.
    """
    def __init__(self, page: ft.Page, lat: float = None, lon: float = None, 
                 state_manager=None, translation_service=None):
        super().__init__()
        self.page = page
        self.latitude = lat if lat is not None else 45.4642  # Default to Milan
        self.longitude = lon if lon is not None else 9.1900
        self.state_manager = state_manager
        self.translation_service = translation_service
        self.webview = None
        self.container = None
        self.loading_indicator = None

    def build(self):
        """Build the map view - opens Windy directly in browser."""
        try:
            logging.info(f"Opening Windy map directly for coordinates: lat={self.latitude}, lon={self.longitude}")
            
            # Open Windy directly in browser
            windy_url = f"https://www.windy.com/?{self.latitude},{self.longitude},10"
            logging.info(f"Opening Windy URL: {windy_url}")
            
            webbrowser.open(windy_url)
            
            # Return a simple confirmation view
            return self._build_confirmation_view()
            
        except Exception as e:
            logging.error(f"Error opening map: {e}")
            return self._build_fallback_view()

    def _build_confirmation_view(self):
        """Build a confirmation view showing that the map has been opened."""
        is_dark = self._is_dark_mode()
        
        # Get theme colors
        if is_dark:
            bg_color = "#161b22"
            text_color = "#f0f6fc"
            button_color = "#58a6ff"
            secondary_color = "#8b949e"
        else:
            bg_color = "#f8f9fa"
            text_color = "#24292f"
            button_color = "#0969da"
            secondary_color = "#656d76"

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE_OUTLINE,
                        size=64,
                        color=button_color
                    ),
                    ft.Text(
                        "🌦️ Mappa Aperta!",
                        size=24,
                        color=text_color,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_600
                    ),
                    ft.Text(
                        "La mappa meteo di Windy è stata aperta nel tuo browser",
                        size=14,
                        color=secondary_color,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        f"📍 Coordinates: {self.latitude:.4f}, {self.longitude:.4f}",
                        size=12,
                        color=secondary_color,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.ElevatedButton(
                        text="Apri di nuovo",
                        icon=ft.Icons.LAUNCH,
                        on_click=lambda e: self._open_windy_again(),
                        bgcolor=button_color,
                        color="#ffffff",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            elevation=2
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16
            ),
            bgcolor=bg_color,
            alignment=ft.alignment.center,
            border_radius=12,
            padding=30,
            expand=True
        )

    def _open_windy_again(self):
        """Open Windy again if user clicks the button."""
        try:
            windy_url = f"https://www.windy.com/?{self.latitude},{self.longitude},10"
            logging.info(f"Re-opening Windy: {windy_url}")
            webbrowser.open(windy_url)
        except Exception as e:
            logging.error(f"Error re-opening Windy: {e}")
            logging.error(f"Error building map view: {e}")
            return self._build_fallback_view()

    def _build_map_url(self) -> str:
        """Build the map URL - trying multiple alternatives that work better in WebView."""
        try:
            # Option 1: Try OpenStreetMap with weather overlay (more WebView-friendly)
            osm_url = f"https://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}#map=10/{self.latitude}/{self.longitude}"
            logging.info(f"Using OpenStreetMap URL: {osm_url}")
            return osm_url
            
            # Option 2: Google Maps (fallback) - usually works in WebView
            # google_url = f"https://www.google.com/maps/@{self.latitude},{self.longitude},10z"
            
            # Option 3: Windy (original - often blocked)
            # windy_url = f"https://www.windy.com/?{self.latitude},{self.longitude},10"
            
        except Exception as e:
            logging.error(f"Error building map URL: {e}")
            return f"https://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}#map=10/{self.latitude}/{self.longitude}"

    def _create_loading_indicator(self):
        """Create a loading indicator with theme support."""
        is_dark = self._is_dark_mode()
        
        # Get theme colors
        if is_dark:
            bg_color = "#161b22"
            text_color = "#f0f6fc"
            accent_color = "#58a6ff"
        else:
            bg_color = "#ffffff"
            text_color = "#24292f"
            accent_color = "#0969da"

        # Get loading text
        loading_text = self._get_loading_text()

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(
                        color=accent_color,
                        stroke_width=4,
                        width=50,
                        height=50
                    ),
                    ft.Text(
                        loading_text,
                        color=text_color,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16
            ),
            bgcolor=ft.Colors.with_opacity(0.9, bg_color),
            alignment=ft.alignment.center,
            border_radius=8,
            visible=True
        )

    def _build_fallback_view(self):
        """Build an enhanced fallback view with multiple map options."""
        is_dark = self._is_dark_mode()
        
        # Get theme colors
        if is_dark:
            bg_color = "#161b22"
            text_color = "#f0f6fc"
            button_color = "#58a6ff"
            secondary_color = "#8b949e"
            card_color = "#21262d"
        else:
            bg_color = "#f8f9fa"
            text_color = "#24292f"
            button_color = "#0969da"
            secondary_color = "#656d76"
            card_color = "#ffffff"

        # Create coordinate info card
        coord_info = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "📍 Coordinates",
                        size=14,
                        color=secondary_color,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Text(
                        f"Lat: {self.latitude:.4f}",
                        size=12,
                        color=text_color
                    ),
                    ft.Text(
                        f"Lon: {self.longitude:.4f}",
                        size=12,
                        color=text_color
                    )
                ],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=card_color,
            border_radius=8,
            padding=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, text_color))
        )

        # Create multiple map service buttons
        map_buttons = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Windy",
                    icon=ft.Icons.CLOUD,
                    on_click=lambda e: self._open_map_service("windy"),
                    bgcolor=button_color,
                    color="#ffffff",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=2
                    )
                ),
                ft.ElevatedButton(
                    text="Google Maps",
                    icon=ft.Icons.MAP,
                    on_click=lambda e: self._open_map_service("google"),
                    bgcolor=button_color,
                    color="#ffffff",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=2
                    )
                ),
                ft.ElevatedButton(
                    text="OpenStreetMap",
                    icon=ft.Icons.PUBLIC,
                    on_click=lambda e: self._open_map_service("osm"),
                    bgcolor=button_color,
                    color="#ffffff",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=2
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.MAP_OUTLINED,
                        size=72,
                        color=button_color
                    ),
                    ft.Text(
                        "🗺️ Weather Map",
                        size=24,
                        color=text_color,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_600
                    ),
                    ft.Text(
                        "View weather conditions for this location",
                        size=14,
                        color=secondary_color,
                        text_align=ft.TextAlign.CENTER
                    ),
                    coord_info,
                    ft.Text(
                        "Choose a map service to view weather data:",
                        size=14,
                        color=text_color,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500
                    ),
                    map_buttons
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            bgcolor=bg_color,
            alignment=ft.alignment.center,
            border_radius=12,
            padding=30,
            expand=True
        )

    def _open_map_service(self, service: str):
        """Open different map services based on selection."""
        try:
            if service == "windy":
                url = f"https://www.windy.com/?{self.latitude},{self.longitude},10"
            elif service == "google":
                url = f"https://www.google.com/maps/@{self.latitude},{self.longitude},10z"
            elif service == "osm":
                url = f"https://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}#map=10/{self.latitude}/{self.longitude}"
            else:
                url = f"https://www.windy.com/?{self.latitude},{self.longitude},10"
            
            logging.info(f"Opening {service} map service: {url}")
            webbrowser.open(url)
        except Exception as ex:
            logging.error(f"Error opening {service} map: {ex}")

    def _open_fullscreen_map_fallback(self, e=None):
        """Apre la mappa a schermo intero nel browser (usato nel fallback)."""
        try:
            fullscreen_url = f"https://www.windy.com/?{self.latitude},{self.longitude},10"
            webbrowser.open(fullscreen_url)
        except Exception as ex:
            logging.error(f"Error opening fullscreen map: {ex}")

    def _setup_loading_timeout(self):
        """Set up a timeout for map loading."""
        import threading
        
        def timeout_handler():
            try:
                import time
                time.sleep(5)  # Reduce timeout to 5 seconds - if WebView doesn't work, fail fast
                if self.loading_indicator and self.loading_indicator.visible:
                    logging.warning("Map loading timeout reached, showing fallback view")
                    # Replace the webview with fallback view
                    if self.container and hasattr(self.container, 'controls'):
                        fallback_view = self._build_fallback_view()
                        self.container.controls = [fallback_view]
                        if self.page:
                            self.page.update()
                            logging.info("Replaced WebView with fallback due to timeout")
            except Exception as e:
                logging.error(f"Error in timeout handler: {e}")
        
        thread = threading.Thread(target=timeout_handler, daemon=True)
        thread.start()

    def _on_page_started(self, e):
        """Handle page started event."""
        try:
            logging.info(f"Map page started loading for coordinates: {self.latitude}, {self.longitude}")
            if hasattr(e, 'url'):
                logging.info(f"Loading URL: {e.url}")
            if self.loading_indicator:
                self.loading_indicator.visible = True
                if self.page:
                    self.page.update()
                    logging.info("Loading indicator shown")
        except Exception as ex:
            logging.error(f"Error in page started handler: {ex}")

    def _on_page_ended(self, e):
        """Handle page ended event."""
        try:
            logging.info("Map page finished loading successfully")
            if hasattr(e, 'url'):
                logging.info(f"Finished loading URL: {e.url}")
            if self.loading_indicator:
                self.loading_indicator.visible = False
                if self.page:
                    self.page.update()
                    logging.info("Loading indicator hidden - map loaded successfully")
        except Exception as ex:
            logging.error(f"Error in page ended handler: {ex}")

    def _on_web_resource_error(self, e):
        """Handle web resource error event."""
        try:
            error_details = {
                'data': getattr(e, 'data', 'No data available'),
                'error_code': getattr(e, 'error_code', 'No error code'),
                'description': getattr(e, 'description', 'No description'),
                'failing_url': getattr(e, 'failing_url', 'No URL'),
            }
            logging.error(f"Web resource error in map loading: {error_details}")
            
            # Hide loading indicator and show fallback
            if self.loading_indicator:
                self.loading_indicator.visible = False
            
            # Replace with fallback view
            if self.container and hasattr(self.container, 'controls'):
                fallback_view = self._build_fallback_view()
                self.container.controls = [fallback_view]
                if self.page:
                    self.page.update()
                    logging.info("Replaced WebView with fallback due to error")
                    
        except Exception as ex:
            logging.error(f"Error in web resource error handler: {ex}")

    def _is_dark_mode(self) -> bool:
        """Check if the current theme is dark mode."""
        try:
            if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
                return self.page.theme_mode == ft.ThemeMode.DARK
        except Exception:
            pass
        return False

    def _get_translations(self) -> dict:
        """Get current translations for map view."""
        try:
            if self.translation_service and self.state_manager:
                current_language = self.state_manager.get_state('language') or 'en'
                # Build translations dict from individual keys
                return {
                    'loading': self.translation_service.translate_from_dict('maps_alert_dialog_items', 'loading', current_language),
                    'error': self.translation_service.translate_from_dict('maps_alert_dialog_items', 'error', current_language),
                    'fullscreen': self.translation_service.translate_from_dict('maps_alert_dialog_items', 'fullscreen', current_language)
                }
        except Exception as e:
            logging.warning(f"Failed to get translations in MapView: {e}")
        
        # Fallback translations
        return {
            'loading': 'Loading map...',
            'error': 'Error loading map',
            'fullscreen': 'Open in Browser'
        }

    def _get_loading_text(self) -> str:
        """Get localized loading text."""
        try:
            translations = self._get_translations()
            return translations.get('loading', 'Loading map...')
        except Exception:
            return 'Loading map...'

    def update_coordinates(self, lat: float, lon: float):
        """Update map coordinates and reload if needed."""
        try:
            self.latitude = lat
            self.longitude = lon
            
            # If webview exists, update its URL
            if self.webview:
                new_url = self._build_map_url()
                self.webview.url = new_url
                if self.page:
                    self.page.update()
                    
        except Exception as e:
            logging.error(f"Error updating map coordinates: {e}")

    def cleanup(self):
        """Clean up resources."""
        try:
            if self.webview:
                self.webview = None
            if self.container:
                self.container = None
            if self.loading_indicator:
                self.loading_indicator = None
        except Exception as e:
            logging.error(f"Error during MapView cleanup: {e}")
