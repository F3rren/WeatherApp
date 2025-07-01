import flet as ft
from utils.config import DARK_THEME, LIGHT_THEME
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService

class MapsAlertDialog:
    def __init__(self, page: ft.Page, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, 
                 text_color: str = None, language: str = "en"):
        self.page = page
        self.state_manager = state_manager
        self.current_language = language
        self.text_color = text_color if text_color else (DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"])
        self.dialog = None
        
        # Map-specific properties
        self.current_city = "Roma"  # Default city
        self.current_lat = 41.9028
        self.current_lon = 12.4964
        self.active_layers = {"temp": True, "rain": False, "wind": False, "clouds": False}
        self.map_container = None
        self.is_webview_available = True  # Track if WebView is available
        
        # ResponsiveTextHandler locale
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20,
                'body': 14,
                'icon': 16,
                'small': 12,
            },
            breakpoints=[600, 900, 1200, 1600]
        )

        # Controls to be initialized in createAlertDialog
        self.title_text_control = None
        self.description_text_control = None
        self.close_button_text_control = None
        self.fullscreen_button_text_control = None
        self.layer_status_text_control = None
        
        if state_manager:
            # Register observers for real-time updates
            state_manager.register_observer("city_changed", self._handle_city_change)
            state_manager.register_observer("language_changed", self._handle_language_change)
            state_manager.register_observer("theme_changed", self._handle_theme_change)

        self.createAlertDialog()

    def _handle_city_change(self, event_data):
        """Handle city change events from state manager."""
        if event_data and "city" in event_data:
            new_city = event_data["city"]
            print(f"Maps: City changed to {new_city}")
            self.current_city = new_city
            self._update_location_from_main_app()
            self._update_map_display()

    def _handle_language_change(self, event_data):
        """Handle language change events."""
        if event_data and "language" in event_data:
            self.current_language = event_data["language"]
            self._update_map_display()

    def _handle_theme_change(self, event_data):
        """Handle theme change events."""
        self._update_map_display()

    def _update_location_from_main_app(self):
        """Get current location coordinates from main weather app."""
        try:
            # Get weather view instance from session
            main_app = self.page.session.get('main_app')
            if main_app and hasattr(main_app, 'weather_view_instance'):
                weather_view = main_app.weather_view_instance
                if hasattr(weather_view, 'current_coordinates'):
                    coords = weather_view.current_coordinates
                    if coords and len(coords) >= 2:
                        self.current_lat = float(coords[0])
                        self.current_lon = float(coords[1])
                        print(f"Maps: Updated coordinates to {self.current_lat}, {self.current_lon}")
                        return True
        except Exception as e:
            print(f"Maps: Error getting coordinates: {e}")
        return False

    def _update_map_display(self):
        """Update the map display with current settings."""
        if not self.dialog:
            return
            
        # Update title and description
        if self.title_text_control:
            self.title_text_control.value = self._get_translation("interactive_weather_map")
            
        if self.description_text_control:
            self.description_text_control.value = f"{self._get_translation('showing_weather_for')} {self.current_city}"
            
        # Update layer status
        self._update_layer_status()
        
        # Update map URL
        self._update_map_url()
        
        # Update theme colors
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        if self.dialog:
            self.dialog.bgcolor = current_theme["DIALOG_BACKGROUND"]
            
        try:
            if self.dialog.page:
                self.dialog.update()
        except Exception:
            pass

    def _update_map_url(self):
        """Update the map iframe URL with current settings."""
        if not self.map_container:
            return
            
        # Build overlay parameter based on active layers
        overlays = []
        if self.active_layers.get("temp", False):
            overlays.append("temp")
        if self.active_layers.get("rain", False):
            overlays.append("rain")
        if self.active_layers.get("wind", False):
            overlays.append("wind")  
        if self.active_layers.get("clouds", False):
            overlays.append("clouds")
            
        # Ensure at least one layer is active (default to temperature)
        if not overlays:
            overlays.append("temp")
            self.active_layers["temp"] = True
            
        overlay_param = ",".join(overlays)
        
        # Build Windy URL
        zoom_level = 8
        windy_url = f"https://embed.windy.com/embed2.html?lat={self.current_lat}&lon={self.current_lon}&detailLat={self.current_lat}&detailLon={self.current_lon}&width=650&height=450&zoom={zoom_level}&level=surface&overlay={overlay_param}&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
        
        # Update iframe source
        if self.is_webview_available:
            if hasattr(self.map_container, 'content') and hasattr(self.map_container.content, 'url'):
                self.map_container.content.url = windy_url
                try:
                    self.map_container.update()
                except Exception:
                    pass
        else:
            # For fallback mode, update the city text
            if hasattr(self.map_container, 'content') and hasattr(self.map_container.content, 'controls'):
                city_text = self.map_container.content.controls[2]  # Third element is city text
                if hasattr(city_text, 'value'):
                    city_text.value = f"Città: {self.current_city}"
                try:
                    self.map_container.update()
                except Exception:
                    pass

    def _create_layer_controls(self):
        """Create interactive layer control checkboxes."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        
        controls = []
        
        # Layer checkboxes with icons and colors
        layer_configs = [
            ("temp", "🌡️", "temperature", ft.Colors.ORANGE_400),
            ("rain", "🌧️", "precipitation", ft.Colors.BLUE_400), 
            ("wind", "💨", "wind", ft.Colors.GREEN_400),
            ("clouds", "☁️", "clouds", ft.Colors.GREY_400)
        ]
        
        for layer_key, icon, label_key, color in layer_configs:
            checkbox = ft.Checkbox(
                label=f"{icon} {self._get_translation(label_key)}",
                value=self.active_layers.get(layer_key, False),
                on_change=lambda e, layer=layer_key: self._toggle_layer(layer, e.control.value),
                active_color=color,
                check_color=current_theme.get("BACKGROUND", ft.Colors.WHITE)
            )
            controls.append(checkbox)
        
        # Add preset buttons
        preset_row = ft.Row([
            ft.ElevatedButton(
                text="☀️ Solo Meteo",
                on_click=lambda e: self._apply_preset("weather_only"),
                bgcolor=ft.Colors.ORANGE_100 if not is_dark else ft.Colors.ORANGE_900,
                color=current_theme.get("TEXT")
            ),
            ft.ElevatedButton(
                text="🌍 Completo", 
                on_click=lambda e: self._apply_preset("complete"),
                bgcolor=ft.Colors.BLUE_100 if not is_dark else ft.Colors.BLUE_900,
                color=current_theme.get("TEXT")
            )
        ], spacing=10)
        
        controls.append(ft.Divider(height=10, color=current_theme.get("OUTLINE")))
        controls.append(preset_row)
        
        return ft.Column(controls, spacing=8)

    def _toggle_layer(self, layer_key, is_active):
        """Toggle a weather layer on/off."""
        self.active_layers[layer_key] = is_active
        
        # Ensure at least one layer is always active
        if not any(self.active_layers.values()):
            self.active_layers["temp"] = True
            # Update the temperature checkbox
            if self.dialog and self.dialog.content:
                self._update_layer_checkboxes()
        
        self._update_layer_status()
        self._update_map_url()

    def _apply_preset(self, preset_type):
        """Apply a layer preset configuration."""
        if preset_type == "weather_only":
            self.active_layers = {"temp": True, "rain": False, "wind": False, "clouds": False}
        elif preset_type == "complete":
            self.active_layers = {"temp": True, "rain": True, "wind": True, "clouds": True}
            
        self._update_layer_checkboxes()
        self._update_layer_status()
        self._update_map_url()

    def _update_layer_checkboxes(self):
        """Update checkbox states to match active layers."""
        if not self.dialog or not self.dialog.content:
            return
            
        try:
            # Find and update checkboxes in the dialog content
            self.dialog.update()
        except Exception:
            pass

    def _update_layer_status(self):
        """Update the layer status text."""
        if not self.layer_status_text_control:
            return
            
        active_layers = [key for key, active in self.active_layers.items() if active]
        if len(active_layers) == 1:
            status = f"Layer attivo: {active_layers[0]}"
        elif len(active_layers) > 1:
            status = f"Layer attivi: {', '.join(active_layers)}"
        else:
            status = "Nessun layer attivo"
            
        self.layer_status_text_control.value = status
        try:
            self.layer_status_text_control.update()
        except Exception:
            pass

    def update_text_sizes(self, text_color, language):
        self.text_color = text_color
        self.current_language = language

        if not self.dialog or not self._text_handler:
            return

        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        self.dialog.bgcolor = current_theme["DIALOG_BACKGROUND"]

        title_size = self._text_handler.get_size('title')
        body_size = self._text_handler.get_size('body')

        if self.title_text_control:
            self.title_text_control.value = self._get_translation("interactive_weather_map")
            self.title_text_control.size = title_size
            self.title_text_control.color = self.text_color

        if self.description_text_control:
            self.description_text_control.value = f"{self._get_translation('showing_weather_for')} {self.current_city}"
            self.description_text_control.size = body_size
            self.description_text_control.color = self.text_color

        if self.close_button_text_control:
            self.close_button_text_control.value = self._get_translation("close_button")
            self.close_button_text_control.color = current_theme["ACCENT"]
            self.close_button_text_control.size = body_size
            if self.dialog.actions and len(self.dialog.actions) > 0:
                if isinstance(self.dialog.actions[0], ft.TextButton):
                    self.dialog.actions[0].style.color = current_theme["ACCENT"]
                    self.dialog.actions[0].style.overlay_color = ft.Colors.with_opacity(0.1, current_theme["ACCENT"])
        
        if self.fullscreen_button_text_control:
            self.fullscreen_button_text_control.value = self._get_translation("fullscreen")
            self.fullscreen_button_text_control.color = current_theme["ACCENT"]
            self.fullscreen_button_text_control.size = body_size
        
        if self.dialog.page:
            self.dialog.update()
        elif self.page:
            self.page.update()

    def _get_translation(self, key):
        return TranslationService.translate(key, str(self.current_language))

    def createAlertDialog(self):
        get_size = self._text_handler.get_size
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        dialog_text_color = self.text_color
        bg_color = current_theme["DIALOG_BACKGROUND"]

        title_size = get_size('title')
        body_size = get_size('body')

        self.title_text_control = ft.Text(
            self._get_translation("interactive_weather_map"),
            size=title_size,
            weight=ft.FontWeight.BOLD, 
            color=dialog_text_color
        )
        
        self.description_text_control = ft.Text(
            f"{self._get_translation('showing_weather_for')} {self.current_city}",
            size=body_size, 
            color=dialog_text_color
        )
        
        # Layer status text
        self.layer_status_text_control = ft.Text(
            "Layer attivo: temp",
            size=get_size('small'),
            color=dialog_text_color,
            italic=True
        )
        
        # Create map iframe
        initial_overlay = "temp"  # Default to temperature
        windy_url = f"https://embed.windy.com/embed2.html?lat={self.current_lat}&lon={self.current_lon}&detailLat={self.current_lat}&detailLon={self.current_lon}&width=650&height=450&zoom=8&level=surface&overlay={initial_overlay}&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
        
        try:
            # Try to use WebView if available
            self.map_container = ft.Container(
                content=ft.WebView(
                    url=windy_url,
                    width=650,
                    height=450,
                    expand=False
                ),
                border=ft.border.all(1, current_theme.get("OUTLINE", ft.Colors.OUTLINE)),
                border_radius=8,
                padding=2
            )
            self.is_webview_available = True
        except (AttributeError, NameError):
            # Fallback: Create a container with link to open in external browser
            self.is_webview_available = False
            self.map_container = ft.Container(
                content=ft.Column([
                    ft.Icon(
                        ft.Icons.MAP,
                        size=100,
                        color=current_theme.get("ACCENT", ft.Colors.BLUE)
                    ),
                    ft.Text(
                        "🗺️ Mappa Meteorologica",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        f"Città: {self.current_city}",
                        size=16,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.ElevatedButton(
                        text="🌐 Apri Mappa Completa",
                        on_click=lambda e: self._open_fullscreen_map(),
                        bgcolor=current_theme.get("ACCENT", ft.Colors.BLUE),
                        color=ft.Colors.WHITE
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
                ),
                width=650,
                height=450,
                border=ft.border.all(1, current_theme.get("OUTLINE", ft.Colors.OUTLINE)),
                border_radius=8,
                padding=20,
                alignment=ft.alignment.center
            )
        
        # Create layer controls
        layer_controls = self._create_layer_controls()
        
        self.close_button_text_control = ft.Text(
            self._get_translation("close_button"), 
            color=current_theme["ACCENT"], 
            size=body_size
        )
        
        self.fullscreen_button_text_control = ft.Text(
            self._get_translation("fullscreen"),
            color=current_theme["ACCENT"],
            size=body_size
        )

        self.dialog = ft.AlertDialog(
            title=self.title_text_control,
            bgcolor=bg_color,
            content=ft.Container(
                width=700,
                content=ft.Column(
                    controls=[
                        self.description_text_control,
                        ft.Divider(height=10, color=current_theme.get("OUTLINE")),
                        
                        # Map section
                        ft.Text("🗺️ Mappa Interattiva", weight=ft.FontWeight.BOLD, size=get_size('body')),
                        self.map_container,
                        
                        ft.Divider(height=10, color=current_theme.get("OUTLINE")),
                        
                        # Layer controls section
                        ft.Text("⚙️ Controlli Layer", weight=ft.FontWeight.BOLD, size=get_size('body')),
                        layer_controls,
                        self.layer_status_text_control,
                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO
                ),
                height=600,
            ),
            actions=[
                ft.TextButton(
                    content=self.fullscreen_button_text_control,
                    style=ft.ButtonStyle(
                        color=current_theme["ACCENT"],
                        overlay_color=ft.Colors.with_opacity(0.1, current_theme["ACCENT"])
                    ),
                    on_click=lambda e: self._open_fullscreen_map()
                ),
                ft.TextButton(
                    content=self.close_button_text_control,
                    style=ft.ButtonStyle(
                        color=current_theme["ACCENT"],
                        overlay_color=ft.Colors.with_opacity(0.1, current_theme["ACCENT"])
                    ),
                    on_click=lambda e: self.close_dialog()
                ),
            ],
            on_dismiss=lambda e: self.close_dialog(),
            modal=True
        )

    def _open_fullscreen_map(self):
        """Open map in fullscreen mode in external browser."""
        import webbrowser
        
        # Build overlay parameter
        overlays = [key for key, active in self.active_layers.items() if active]
        if not overlays:
            overlays = ["temp"]
        overlay_param = ",".join(overlays)
        
        fullscreen_url = f"https://www.windy.com/{self.current_lat}/{self.current_lon}?{overlay_param},{self.current_lat},{self.current_lon},8"
        
        try:
            webbrowser.open(fullscreen_url)
            print(f"Opened fullscreen map: {fullscreen_url}")
        except Exception as e:
            print(f"Error opening browser: {e}")
            # Fallback: just print the URL
            print(f"Please open this URL manually: {fullscreen_url}")

    def open_dialog(self):
        """Open the maps dialog with updated location and layers."""
        if not self.dialog:
            self.createAlertDialog()
            
        # Update location from main app before opening
        self._update_location_from_main_app()
        self._update_map_display()
        
        if self.page and self.dialog:
            if self.dialog not in self.page.controls:
                self.page.controls.append(self.dialog)
            self.page.dialog = self.dialog
            self.page.dialog.open = True
            self.update_text_sizes(self.text_color, self.current_language)
            self.page.update()

    def close_dialog(self):
        if self.dialog:
            self.dialog.open = False
            if self.page:
                 self.page.update()
        
    def cleanup(self):
        """Cleanup observers and resources."""
        if self.state_manager:
            try:
                self.state_manager.unregister_observer("city_changed", self._handle_city_change)
                self.state_manager.unregister_observer("language_changed", self._handle_language_change)
                self.state_manager.unregister_observer("theme_changed", self._handle_theme_change)
                print("Maps dialog cleanup: Unregistered observers")
            except Exception as e:
                print(f"Maps dialog cleanup error: {e}")
        print(f"Cleaning up MapsAlertDialog for page: {self.page}")
