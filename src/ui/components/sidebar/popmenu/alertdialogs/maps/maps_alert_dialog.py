import flet as ft
import webbrowser
import logging

from core.state_manager import StateManager
from translations import translation_manager  # New modular translation system
from .map_view import MapView

class MapsAlertDialog:
    def __init__(self, page: ft.Page, state_manager: StateManager):
        self.page = page
        self.state_manager = state_manager
        self.dialog = None
        self.map_view_instance = None
        self.current_city = None
        self.current_lat = None
        self.current_lon = None
        
        # Register for theme and language updates
        if self.state_manager:
            self.state_manager.register_observer("theme_event", self._on_theme_change)
            self.state_manager.register_observer("language_event", self._on_language_change)

    def build(self):
        """Costruisce l'interfaccia dell'AlertDialog con supporto tema e traduzione."""
        try:
            self.map_view_instance = MapView(
                self.page, 
                lat=self.current_lat, 
                lon=self.current_lon,
                state_manager=self.state_manager
            )

            # Get current theme
            is_dark = self._is_dark_mode()
            
            # Get theme colors
            if is_dark:
                dialog_bg = "#161b22"
                content_bg = "#0d1117"
                button_color = "#58a6ff"
                text_color = "#f0f6fc"
                border_color = "#30363d"
            else:
                dialog_bg = "#ffffff"
                content_bg = "#f8f9fa"
                button_color = "#0969da"
                text_color = "#24292f"
                border_color = "#d1d9e0"

            # Get translations
            translations = self._get_translations()
            
            # Create title with icon
            title_content = ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.MAP,
                        color=button_color,
                        size=24
                    ),
                    ft.Text(
                        f"{translations['weather_map_title']} - {self.current_city}",
                        size=18,
                        weight=ft.FontWeight.W_600,
                        color=text_color
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=8
            )

            # Create map container with enhanced styling
            map_container = ft.Container(
                content=self.map_view_instance.build(),
                width=min(600, self.page.width * 0.9),  # Responsive width
                bgcolor=content_bg,
                border_radius=12,
                border=ft.border.all(1, border_color),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
                padding=8
            )

            # Create action buttons with enhanced styling
            fullscreen_btn = ft.ElevatedButton(
                text=translations['fullscreen'],
                icon=ft.Icons.FULLSCREEN,
                on_click=self._open_fullscreen_map,
                bgcolor=button_color,
                color="#ffffff",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    elevation=2,
                    shadow_color=ft.Colors.with_opacity(0.3, button_color)
                )
            )
            
            close_btn = ft.FilledButton(
                text=translations['close'],
                icon=ft.Icons.CLOSE,
                on_click=self.close_dialog,
                style=ft.ButtonStyle(
                    bgcolor=button_color,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=8)
                )
            )

            # Create dialog with enhanced styling
            dialog = ft.AlertDialog(
                modal=False,
                scrollable=True,  # Make dialog scrollable
                title=title_content,
                bgcolor=dialog_bg,
                surface_tint_color=button_color,
                content=map_container,
                actions=[fullscreen_btn, close_btn],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: self.close_dialog(e),
                shape=ft.RoundedRectangleBorder(radius=16),
                elevation=8,
                title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                content_text_style=ft.TextStyle(size=14),
                inset_padding=ft.padding.all(20)
            )
            
            return dialog
            
        except Exception as e:
            logging.error(f"Error building maps alert dialog: {e}")
            return self._build_error_dialog()

    def _build_error_dialog(self):
        """Build a simple error dialog if main build fails."""
        translations = self._get_translations()
        text_color = self.theme_handler.get_text_color() if self.theme_handler else {"ACCENT": ft.Colors.BLUE}
        if isinstance(text_color, str):
            text_color = {"ACCENT": ft.Colors.BLUE}
        
        return ft.AlertDialog(
            modal=False,
            scrollable=True,  # Make dialog scrollable
            title=ft.Text(translations['weather_map_title']),
            content=ft.Text(translations['error']),
            actions=[
                ft.FilledButton(
                    text=translations['close'], 
                    on_click=self.close_dialog,
                    style=ft.ButtonStyle(
                        bgcolor=text_color.get("ACCENT", ft.Colors.BLUE),
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
            content_text_style=ft.TextStyle(size=14),
            inset_padding=ft.padding.all(20)
        )

    def open_dialog(self):
        """Apre direttamente la mappa di Windy nel browser."""
        try:
            logging.info("Opening Windy map directly in browser...")
            
            self.current_city = self.state_manager.get_state('city')
            self.current_lat = self.state_manager.get_state('current_lat')
            self.current_lon = self.state_manager.get_state('current_lon')

            # Fallback to default if values are None
            if self.current_city is None:
                self.current_city = "Milano"
            if self.current_lat is None or self.current_lon is None:
                self.current_lat = 45.4642  # Default to Milan
                self.current_lon = 9.1900

            logging.info(f"Opening Windy for: city={self.current_city}, lat={self.current_lat}, lon={self.current_lon}")
            
            # Open Windy directly
            windy_url = f"https://www.windy.com/?{self.current_lat},{self.current_lon},16"
            webbrowser.open(windy_url)
            logging.info(f"Windy opened: {windy_url}")
                
        except Exception as e:
            logging.error(f"Error opening Windy: {e}")
            # Show fallback error dialog only if direct opening fails
            try:
                text_color = self.theme_handler.get_text_color() if self.theme_handler else {"ACCENT": ft.Colors.BLUE}
                if isinstance(text_color, str):
                    text_color = {"ACCENT": ft.Colors.BLUE}
                    
                error_dialog = ft.AlertDialog(
                    modal=False,
                    title=ft.Text("Errore Mappa"),
                    scrollable=True,  # Make dialog scrollable
                    content=ft.Text(f"Impossibile aprire Windy: {str(e)}"),
                    actions=[
                        ft.FilledButton(
                            icon=ft.Icons.CLOSE,
                            text="Chiudi", 
                            on_click=lambda e: self._close_error_dialog(e, error_dialog),
                            style=ft.ButtonStyle(
                                bgcolor=text_color.get("ACCENT", ft.Colors.BLUE),
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ]
                )
                if self.page:
                    self.page.dialog = error_dialog
                    error_dialog.open = True
                    self.page.update()
            except Exception as fallback_error:
                logging.error(f"Even error dialog failed: {fallback_error}")

    def _open_browser_fallback(self, e=None):
        """Open map in browser as fallback."""
        try:
            import webbrowser
            url = f"https://www.windy.com/?{self.current_lat},{self.current_lon},10"
            webbrowser.open(url)
            if self.page and self.page.dialog:
                self.page.dialog.open = False
                self.page.update()
        except Exception as ex:
            logging.error(f"Error opening browser: {ex}")

    def _close_error_dialog(self, e, dialog):
        """Close error dialog."""
        try:
            if dialog:
                dialog.open = False
                if self.page:
                    self.page.update()
        except Exception as ex:
            logging.error(f"Error closing dialog: {ex}")

    def close_dialog(self, e=None):
        """Close the dialog when close button is clicked"""
        try:
            if self.dialog and hasattr(self.dialog, 'open'):
                self.dialog.open = False
                if self.page:
                    self.page.update()
        except Exception as ex:
            logging.error(f"Error closing dialog: {ex}")

    def _open_fullscreen_map(self, e=None):
        """Apre la mappa a schermo intero nel browser."""
        try:
            fullscreen_url = f"https://www.windy.com/?{self.current_lat},{self.current_lon},10"
            webbrowser.open(fullscreen_url)
        except Exception as ex:
            logging.error(f"Error opening fullscreen map: {ex}")

    def _is_dark_mode(self) -> bool:
        """Check if the current theme is dark mode."""
        try:
            if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
                return self.page.theme_mode == ft.ThemeMode.DARK
        except Exception:
            pass
        return False

    def _get_translations(self) -> dict:
        """Get current translations for maps alert dialog."""
        try:
            # Ensure translation service is available
            self._ensure_translation_service()
            
            if self.state_manager:
                current_language = self.state_manager.get_state('language') or 'en'
                # Use modular translation system
                return {
                    'weather_map_title': translation_manager.get_translation('maps', 'maps_alert_dialog_items', 'weather_map_title', current_language),
                    'fullscreen': translation_manager.get_translation('maps', 'maps_alert_dialog_items', 'fullscreen', current_language),
                    'close': translation_manager.get_translation('maps', 'maps_alert_dialog_items', 'close', current_language),
                    'loading': translation_manager.get_translation('maps', 'maps_alert_dialog_items', 'loading', current_language),
                    'error': translation_manager.get_translation('maps', 'maps_alert_dialog_items', 'error', current_language)
                }
        except Exception as e:
            logging.debug(f"Using fallback translations: {e}")
        
        # Fallback translations
        return {
            'weather_map_title': 'Weather Map',
            'fullscreen': 'Fullscreen',
            'close': 'Close',
            'loading': 'Loading map...',
            'error': 'Error loading map'
        }

    def _on_theme_change(self, event_data=None):
        """Handle theme change events."""
        try:
            if self.dialog and hasattr(self.dialog, 'open') and self.dialog.open:
                # Rebuild dialog with new theme
                new_dialog = self.build()
                if new_dialog:
                    self.dialog = new_dialog
                    self.page.dialog = self.dialog
                    self.page.dialog.open = True
                    self.page.update()
        except Exception as e:
            logging.error(f"Error handling theme change: {e}")

    def _on_language_change(self, event_data=None):
        """Handle language change events."""
        try:
            if self.dialog and hasattr(self.dialog, 'open') and self.dialog.open:
                # Rebuild dialog with new language
                new_dialog = self.build()
                if new_dialog:
                    self.dialog = new_dialog
                    self.page.dialog = self.dialog
                    self.page.dialog.open = True
                    self.page.update()
        except Exception as e:
            logging.error(f"Error handling language change: {e}")

    def cleanup(self):
        """Clean up resources."""
        try:
            if self.map_view_instance:
                self.map_view_instance.cleanup()
            if self.dialog:
                self.dialog = None
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")