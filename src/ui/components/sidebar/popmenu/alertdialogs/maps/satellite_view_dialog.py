#!/usr/bin/env python3
"""
Satellite View Dialog for MeteoApp.
Dialog semplificato per la vista satellitare.
"""

import flet as ft


class SatelliteViewDialog:
    """Dialog semplificato per la vista satellitare."""
    
    def __init__(self, page: ft.Page = None, state_manager=None, language: str = "it", theme_handler=None):
        self.page = page
        self.state_manager = state_manager
        self.language = language
        self.theme_handler = theme_handler
        self.dialog = None
        self.colors = self.update_theme_colors()
        
        # Register for theme and language updates if state_manager is available
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
                "text_secondary": "#8b949e", "accent": "#607d8b", "border": "#30363d"
            }
        else:
            return {
                "bg": "#ffffff", "surface": "#f6f8fa", "text": "#24292f",
                "text_secondary": "#656d76", "accent": "#607d8b", "border": "#d1d9e0"
            }
    
    def update_ui(self, event_data=None):
        """Update UI when theme or language changes."""
        if event_data and 'language' in event_data:
            self.language = event_data['language']
        
        self.colors = self.update_theme_colors()
        
        # If dialog is currently open, refresh it
        if self.dialog and hasattr(self.page, 'dialog') and self.page.dialog and self.page.dialog.open:
            self.show_dialog()
    
    def show_dialog(self):
        """Show the satellite view dialog."""
        if not self.page:
            print("ERROR: Page context not available for SatelliteViewDialog")
            return
        
        try:
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
        """Create the satellite view alert dialog."""
        texts = self.get_texts()
        
        content = ft.Container(
            content=ft.Column([
                ft.Text(f"{texts['title']}", size=20, weight=ft.FontWeight.BOLD,
                       text_align=ft.TextAlign.CENTER, color=self.colors["text"]),
                ft.Divider(color=ft.Colors.with_opacity(0.3, self.colors["text"])),
                ft.Text(texts['description'], size=14, color=self.colors["text_secondary"], 
                       text_align=ft.TextAlign.CENTER),
                ft.Container(height=15),
                
                # Features list
                ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CLOUD, color="#2196F3", size=20),
                        ft.Text("Copertura nuvolosa in tempo reale", size=14, color=self.colors["text"])
                    ], spacing=8),
                    ft.Row([
                        ft.Icon(ft.Icons.VISIBILITY, color="#4CAF50", size=20),
                        ft.Text("Vista ad alta risoluzione", size=14, color=self.colors["text"])
                    ], spacing=8),
                    ft.Row([
                        ft.Icon(ft.Icons.LAYERS, color="#FF9800", size=20),
                        ft.Text("Layer di temperatura e vento", size=14, color=self.colors["text"])
                    ], spacing=8),
                    ft.Row([
                        ft.Icon(ft.Icons.REFRESH, color="#9C27B0", size=20),
                        ft.Text("Aggiornamento ogni 15 minuti", size=14, color=self.colors["text"])
                    ], spacing=8)
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.START),
                
                ft.Container(height=20),
                
                # Action button
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SATELLITE_ALT, color=ft.Colors.GREY_400, size=20),
                        ft.Text(f"{texts['open_satellite']}", color=self.colors["accent"], weight=ft.FontWeight.W_500)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    on_click=lambda _: self.open_satellite_view(),
                    bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]), 
                    width=300, 
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
                
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, width=min(400, self.page.width * 0.9), bgcolor=self.colors["bg"]
        )
        
        return ft.AlertDialog(
            modal=False, scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.SATELLITE_ALT, color=self.colors["accent"], size=24),
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
    
    def get_texts(self):
        """Get localized texts based on current language."""
        if self.language == "en":
            return {
                "title": "Satellite View", "dialog_title": "Satellite View",
                "description": "View real-time satellite imagery of your area",
                "open_satellite": "Open Satellite View", "close": "Close"
            }
        else:  # Italian (default)
            return {
                "title": "Vista Satellitare", "dialog_title": "Vista Satellitare",
                "description": "Visualizza immagini satellitari in tempo reale della tua zona",
                "open_satellite": "Apri Vista Satellitare", "close": "Chiudi"
            }
    
    def open_satellite_view(self):
        """Open satellite view (placeholder)."""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Vista Satellite in sviluppo"),
                bgcolor=self.colors["accent"]
            )
            self.page.snack_bar.open = True
            self.page.update()
        self.close_dialog()
    
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
