"""
Interactive Maps Alert Dialog for MeteoApp.
Provides access to interactive weather maps with multiple layers and options.
"""

import flet as ft
from services.maps.interactive_maps_service import InteractiveMapService


class InteractiveMapAlertDialog:
    """Interactive maps dialog with layer selection and map options."""
    
    def __init__(self, page: ft.Page = None, state_manager=None, language: str = "it", theme_handler=None):
        self.page = page
        self.state_manager = state_manager
        self.language = language
        self.theme_handler = theme_handler
        self.dialog = None
        
        # Initialize the maps service
        self.maps_service = InteractiveMapService(page, state_manager)
        
        # Load preferences
        if self.maps_service:
            self.maps_service.load_preferences()
        
        # Register for theme and language updates
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)

    def update_ui(self, event_data=None):
        """Update UI when theme or language changes."""
        if event_data:
            if 'language' in event_data:
                self.language = event_data['language']
        
        # Update language from state manager
        if self.state_manager:
            current_language = self.state_manager.get_state('language')
            if current_language and current_language != self.language:
                self.language = current_language
        
        # If dialog is currently open, refresh it
        if self.dialog and hasattr(self.page, 'dialog') and self.page.dialog and self.page.dialog.open:
            # Rebuild and apply current styling and text
            new_dialog = self.createAlertDialog()
            self.page.dialog = new_dialog
            self.page.update()

    def build(self):
        """Build the interactive maps dialog."""
        return self.createAlertDialog()

    def open_dialog(self):
        """Always (re)builds and opens the alert dialog with instant theme application."""
        if not self.page:
            print("ERROR: Page context not available for InteractiveMapAlertDialog")
            return
        
        try:
            # Update location from state manager if available
            if self.state_manager:
                location = self.state_manager.get_state('current_location')
                if location and isinstance(location, dict):
                    lat = location.get('lat')
                    lon = location.get('lon')
                    if lat and lon:
                        self.maps_service.set_location(float(lat), float(lon))
            
            # Build the dialog first
            dialog = self.build()
            
            # Apply immediate theme and language updates
            self.update_ui()
            
            # Ensure the dialog is properly added to the page
            if dialog not in self.page.controls:
                self.page.controls.append(dialog)
            self.page.dialog = dialog
            self.page.dialog.open = True
            
            # Force a complete page update
            self.page.update()
            
        except Exception as e:
            print(f"ERROR: Exception in open_dialog: {e}")
            import traceback
            traceback.print_exc()

    def show_dialog(self):
        """Alias for open_dialog to maintain compatibility."""
        return self.open_dialog()

    def createAlertDialog(self) -> ft.AlertDialog:
        """Create the interactive maps alert dialog."""
        # Get theme colors following the same pattern as other dialogs
        theme_colors = self.theme_handler.get_text_color() if self.theme_handler else {"TEXT": "#000000"}
        if isinstance(theme_colors, str):
            theme_colors = {"TEXT": theme_colors, "DIALOG_BACKGROUND": "#fff", "ACCENT": "#0078d4"}
        
        # Support dark mode for dialog background
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        dialog_bg = "#161b22" if is_dark else "#ffffff"
        text_color = theme_colors["TEXT"]
        accent_color = theme_colors.get("ACCENT", "#0078d4")
        
        # Get texts based on language
        texts = self._get_texts()
        
        # Get quick map options
        quick_options = self.maps_service.get_quick_map_options()
        
        content = ft.Container(
            content=ft.Column([
                ft.Text(
                    f"🗺️ {texts['title']}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=text_color
                ),
                ft.Divider(color=ft.Colors.with_opacity(0.3, text_color)),
                ft.Text(
                    texts['description'],
                    size=14,
                    color=text_color,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=10),
                
                # Quick Access Section
                ft.Text(
                    texts['quick_access'],
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=text_color
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Text(quick_options[0]['icon'], size=20),
                                    ft.Column([
                                        ft.Text(quick_options[0]['name'], size=12, weight=ft.FontWeight.BOLD),
                                        ft.Text(quick_options[0]['description'], size=10, color=ft.Colors.with_opacity(0.7, text_color))
                                    ], spacing=2)
                                ], spacing=8),
                                on_click=lambda _: quick_options[0]['action'](),
                                bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                                color=accent_color,
                                width=280,
                                height=60,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            ),
                            ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Text(quick_options[1]['icon'], size=20),
                                    ft.Column([
                                        ft.Text(quick_options[1]['name'], size=12, weight=ft.FontWeight.BOLD),
                                        ft.Text(quick_options[1]['description'], size=10, color=ft.Colors.with_opacity(0.7, text_color))
                                    ], spacing=2)
                                ], spacing=8),
                                on_click=lambda _: quick_options[1]['action'](),
                                bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                                color=accent_color,
                                width=280,
                                height=60,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            )
                        ], spacing=10),
                        ft.Row([
                            ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Text(quick_options[2]['icon'], size=20),
                                    ft.Column([
                                        ft.Text(quick_options[2]['name'], size=12, weight=ft.FontWeight.BOLD),
                                        ft.Text(quick_options[2]['description'], size=10, color=ft.Colors.with_opacity(0.7, text_color))
                                    ], spacing=2)
                                ], spacing=8),
                                on_click=lambda _: quick_options[2]['action'](),
                                bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                                color=accent_color,
                                width=280,
                                height=60,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            ),
                            ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Text(quick_options[3]['icon'], size=20),
                                    ft.Column([
                                        ft.Text(quick_options[3]['name'], size=12, weight=ft.FontWeight.BOLD),
                                        ft.Text(quick_options[3]['description'], size=10, color=ft.Colors.with_opacity(0.7, text_color))
                                    ], spacing=2)
                                ], spacing=8),
                                on_click=lambda _: quick_options[3]['action'](),
                                bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                                color=accent_color,
                                width=280,
                                height=60,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            )
                        ], spacing=10)
                    ], spacing=10),
                    padding=10
                ),
                
                ft.Divider(color=ft.Colors.with_opacity(0.3, text_color)),
                
                # Layer Configuration Section
                ft.Text(
                    texts['layer_config'],
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=text_color
                ),
                self._build_layer_controls(theme_colors, accent_color, text_color),
                
                ft.Container(height=10),
                
                # Advanced Options
                ft.Row([
                    ft.ElevatedButton(
                        text=texts['settings'],
                        icon=ft.Icons.SETTINGS,
                        on_click=self._open_map_settings,
                        bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                        color=accent_color,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    ),
                    ft.ElevatedButton(
                        text=texts['custom_map'],
                        icon=ft.Icons.MAP,
                        on_click=self._open_custom_map,
                        bgcolor=ft.Colors.with_opacity(0.1, accent_color),
                        color=accent_color,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    )
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
                
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            width=600,
            height=500,
            bgcolor=dialog_bg
        )
        
        self.dialog = ft.AlertDialog(
            modal=False,  # Allow clicking outside to close
            scrollable=True,  # Make dialog scrollable
            title=ft.Row([
                ft.Icon(ft.Icons.MAP, color=accent_color, size=24),
                ft.Text(texts['dialog_title'], weight=ft.FontWeight.BOLD, color=text_color)
            ], spacing=10),
            content=content,
            actions=[
                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=texts['close'], 
                    on_click=self._close_dialog, 
                    style=ft.ButtonStyle(
                        bgcolor=accent_color,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=dialog_bg,
            title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=text_color),
            content_text_style=ft.TextStyle(size=14, color=text_color),
            inset_padding=ft.padding.all(20)
        )
        
        return self.dialog

    def _build_layer_controls(self, theme_colors, accent_color, text_color):
        """Build layer toggle controls."""
        layers = self.maps_service.get_available_layers()
        controls = []
        
        for i in range(0, len(layers), 2):
            row_controls = []
            for j in range(2):
                if i + j < len(layers):
                    layer = layers[i + j]
                    toggle = ft.Switch(
                        value=layer.enabled,
                        active_color=accent_color,
                        on_change=lambda e, lid=layer.layer_id: self._toggle_layer(lid, e.control.value)
                    )
                    
                    row_controls.append(
                        ft.Container(
                            content=ft.Row([
                                toggle,
                                ft.Column([
                                    ft.Text(layer.name, size=12, weight=ft.FontWeight.BOLD, color=text_color),
                                    ft.Text(layer.description, size=10, color=ft.Colors.with_opacity(0.7, text_color))
                                ], spacing=2)
                            ], spacing=8),
                            width=250,
                            padding=5
                        )
                    )
            
            if row_controls:
                controls.append(ft.Row(row_controls, spacing=20))
        
        return ft.Column(controls, spacing=5)

    def _toggle_layer(self, layer_id: str, enabled: bool):
        """Toggle a map layer."""
        self.maps_service.toggle_layer(layer_id)
        # Save preferences
        self.maps_service.save_preferences()

    def _open_map_settings(self, e):
        """Open map settings dialog."""
        # TODO: Implement map settings dialog
        self._show_snackbar("Impostazioni mappe - In sviluppo")

    def _open_custom_map(self, e):
        """Open custom map builder."""
        # TODO: Implement custom map builder
        self._show_snackbar("Mappa personalizzata - In sviluppo")

    def _show_snackbar(self, message: str):
        """Show a snackbar message."""
        if self.page:
            snackbar = ft.SnackBar(content=ft.Text(message))
            self.page.snack_bar = snackbar
            snackbar.open = True
            self.page.update()

    def _get_texts(self):
        """Get localized texts based on current language."""
        if self.language == "en":
            return {
                "title": "Interactive Weather Maps",
                "dialog_title": "Interactive Maps",
                "description": "Access interactive weather maps with real-time data and multiple layers",
                "quick_access": "Quick Access",
                "layer_config": "Layer Configuration",
                "settings": "Settings",
                "custom_map": "Custom Map",
                "close": "Close"
            }
        else:  # Italian (default)
            return {
                "title": "Mappe Meteo Interattive",
                "dialog_title": "Mappe Interattive",
                "description": "Accedi a mappe meteo interattive con dati in tempo reale e layer multipli",
                "quick_access": "Accesso Rapido",
                "layer_config": "Configurazione Layer",
                "settings": "Impostazioni",
                "custom_map": "Mappa Personalizzata",
                "close": "Chiudi"
            }

    def _close_dialog(self, e):
        """Close the dialog."""
        self.close_dialog()
    
    def close_dialog(self):
        """Closes the alert dialog."""
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def cleanup(self):
        """Cleanup method to unregister observers."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
            self.state_manager.unregister_observer("theme_event", self.update_ui)
