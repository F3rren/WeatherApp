"""
Interactive Maps Alert Dialog for MeteoApp.
Dialog semplificato per le mappe meteo interattive.
"""

import flet as ft
from services.maps.interactive_maps_service import InteractiveMapService


class InteractiveMapAlertDialog:
    """Dialog semplificato per le mappe meteo interattive."""
    
    def __init__(self, page: ft.Page = None, state_manager=None, language: str = "it", theme_handler=None):
        self.page = page
        self.state_manager = state_manager
        self.language = language
        self.theme_handler = theme_handler
        self.dialog = None
        self.colors = self.update_theme_colors()
        
        # Initialize the maps service
        self.maps_service = InteractiveMapService(page, state_manager)
        if self.maps_service:
            self.maps_service.load_preferences()
        
        # Register for theme and language updates
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)

    def update_theme_colors(self):
        """Update and return theme colors based on current theme."""
        is_dark = (hasattr(self.page, 'theme_mode') and 
                  self.page.theme_mode == ft.ThemeMode.DARK)
        
        if is_dark:
            return {
                "bg": "#161b22", "surface": "#21262d", "text": "#f0f6fc",
                "text_secondary": "#8b949e", "accent": "#58a6ff", "border": "#30363d"
            }
        else:
            return {
                "bg": "#ffffff", "surface": "#f6f8fa", "text": "#24292f",
                "text_secondary": "#656d76", "accent": "#0969da", "border": "#d1d9e0"
            }

    def update_ui(self, event_data=None):
        """Update UI when theme or language changes."""
        if event_data and 'language' in event_data:
            self.language = event_data['language']
        
        # Update language from state manager
        if self.state_manager:
            current_language = self.state_manager.get_state('language')
            if current_language and current_language != self.language:
                self.language = current_language
        
        self.colors = self.update_theme_colors()
        
        # If dialog is currently open, refresh it
        if self.dialog and hasattr(self.page, 'dialog') and self.page.dialog and self.page.dialog.open:
            self.show_dialog()

    def show_dialog(self):
        """Show the interactive maps dialog."""
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
            
            self.colors = self.update_theme_colors()
            dialog = self.create_dialog()
            
            if dialog not in self.page.controls:
                self.page.controls.append(dialog)
            self.page.dialog = dialog
            self.page.dialog.open = True
            self.page.update()
            
        except Exception as e:
            print(f"ERROR: Exception in show_dialog: {e}")

    def create_dialog(self) -> ft.AlertDialog:
        """Create the interactive maps alert dialog."""
        texts = self.get_texts()
        quick_options = self.maps_service.get_quick_map_options()
        
        content = ft.Container(
            content=ft.Column([
                ft.Text(f"🗺️ {texts['title']}", size=20, weight=ft.FontWeight.BOLD,
                       text_align=ft.TextAlign.CENTER, color=self.colors["text"]),
                ft.Divider(color=ft.Colors.with_opacity(0.3, self.colors["text"])),
                ft.Text(texts['description'], size=14, color=self.colors["text"], text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                
                # Quick Access Section
                ft.Text(texts['quick_access'], size=16, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
                self.create_quick_access_buttons(quick_options),
                
                ft.Divider(color=ft.Colors.with_opacity(0.3, self.colors["text"])),
                
                # Layer Configuration Section
                ft.Text(texts['layer_config'], size=16, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
                self.create_layer_controls(),
                
                ft.Container(height=10),
                
                # Advanced Options
                ft.Row([
                    ft.ElevatedButton(
                        text=texts['settings'], icon=ft.Icons.SETTINGS, on_click=self.open_map_settings,
                        bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]), color=self.colors["accent"],
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    ),
                    ft.ElevatedButton(
                        text=texts['custom_map'], icon=ft.Icons.MAP, on_click=self.open_custom_map,
                        bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]), color=self.colors["accent"],
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    )
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
                
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, width=600, height=500, bgcolor=self.colors["bg"]
        )
        
        self.dialog = ft.AlertDialog(
            modal=False, scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.MAP, color=self.colors["accent"], size=24),
                ft.Text(texts['dialog_title'], weight=ft.FontWeight.BOLD, color=self.colors["text"])
            ], spacing=10),
            content=content,
            actions=[ft.FilledButton(
                icon=ft.Icons.CLOSE, text=texts['close'], on_click=self.close_dialog,
                style=ft.ButtonStyle(bgcolor=self.colors["accent"], color=ft.Colors.WHITE,
                                   shape=ft.RoundedRectangleBorder(radius=8))
            )],
            actions_alignment=ft.MainAxisAlignment.END, bgcolor=self.colors["bg"],
            title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
            content_text_style=ft.TextStyle(size=14, color=self.colors["text"]),
            inset_padding=ft.padding.all(20)
        )
        
        return self.dialog

    def create_quick_access_buttons(self, quick_options):
        """Create quick access buttons for map options."""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    self.create_quick_button(quick_options[0]),
                    self.create_quick_button(quick_options[1])
                ], spacing=10),
                ft.Row([
                    self.create_quick_button(quick_options[2]),
                    self.create_quick_button(quick_options[3])
                ], spacing=10)
            ], spacing=10), padding=10
        )

    def create_quick_button(self, option):
        """Create a single quick access button."""
        return ft.ElevatedButton(
            content=ft.Row([
                ft.Text(option['icon'], size=20),
                ft.Column([
                    ft.Text(option['name'], size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(option['description'], size=10, color=ft.Colors.with_opacity(0.7, self.colors["text"]))
                ], spacing=2)
            ], spacing=8),
            on_click=lambda _: option['action'](),
            bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]),
            color=self.colors["accent"],
            width=280, height=60,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

    def create_layer_controls(self):
        """Create layer toggle controls."""
        layers = self.maps_service.get_available_layers()
        controls = []
        
        for i in range(0, len(layers), 2):
            row_controls = []
            for j in range(2):
                if i + j < len(layers):
                    layer = layers[i + j]
                    toggle = ft.Switch(
                        value=layer.enabled,
                        active_color=self.colors["accent"],
                        on_change=lambda e, lid=layer.layer_id: self.toggle_layer(lid, e.control.value)
                    )
                    
                    row_controls.append(
                        ft.Container(
                            content=ft.Row([
                                toggle,
                                ft.Column([
                                    ft.Text(layer.name, size=12, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
                                    ft.Text(layer.description, size=10, color=ft.Colors.with_opacity(0.7, self.colors["text"]))
                                ], spacing=2)
                            ], spacing=8),
                            width=250, padding=5
                        )
                    )
            
            if row_controls:
                controls.append(ft.Row(row_controls, spacing=20))
        
        return ft.Column(controls, spacing=5)

    def toggle_layer(self, layer_id: str, enabled: bool):
        """Toggle a map layer."""
        self.maps_service.toggle_layer(layer_id)
        self.maps_service.save_preferences()

    def open_map_settings(self, e=None):
        """Open map settings dialog."""
        self.show_snackbar("Impostazioni mappe - In sviluppo")

    def open_custom_map(self, e=None):
        """Open custom map builder."""
        self.show_snackbar("Mappa personalizzata - In sviluppo")

    def show_snackbar(self, message: str):
        """Show a snackbar message."""
        if self.page:
            snackbar = ft.SnackBar(content=ft.Text(message))
            self.page.snack_bar = snackbar
            snackbar.open = True
            self.page.update()

    def get_texts(self):
        """Get localized texts based on current language."""
        if self.language == "en":
            return {
                "title": "Interactive Weather Maps", "dialog_title": "Interactive Maps",
                "description": "Access interactive weather maps with real-time data and multiple layers",
                "quick_access": "Quick Access", "layer_config": "Layer Configuration",
                "settings": "Settings", "custom_map": "Custom Map", "close": "Close"
            }
        else:  # Italian (default)
            return {
                "title": "Mappe Meteo Interattive", "dialog_title": "Mappe Interattive",
                "description": "Accedi a mappe meteo interattive con dati in tempo reale e layer multipli",
                "quick_access": "Accesso Rapido", "layer_config": "Configurazione Layer",
                "settings": "Impostazioni", "custom_map": "Mappa Personalizzata", "close": "Chiudi"
            }

    def close_dialog(self, e=None):
        """Close the dialog."""
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def cleanup(self):
        """Cleanup method to unregister observers."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
            self.state_manager.unregister_observer("theme_event", self.update_ui)