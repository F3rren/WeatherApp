import flet as ft
from src.core.state_manager import StateManager


class LocationManagerDialog:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state_manager = StateManager(page)
        theme_mode = self.state_manager.get_state("theme_mode")
        self.theme = "dark" if theme_mode == ft.ThemeMode.DARK else "light"
        self.language = self.state_manager.get_state("language") or "italian"
        
        # Sample locations for demonstration
        self.sample_locations = [
            {"id": 1, "name": "Roma, Italia", "lat": 41.9028, "lon": 12.4964, "favorite": True},
            {"id": 2, "name": "Milano, Italia", "lat": 45.4642, "lon": 9.1900, "favorite": False},
            {"id": 3, "name": "Napoli, Italia", "lat": 40.8518, "lon": 14.2681, "favorite": False},
        ]
        
        # Centralized color management  
        self.colors = {}
        self.update_theme_colors()
        
        # Register observers
        self.state_manager.register_observer("language_event", self.update_ui)
        self.state_manager.register_observer("theme_event", self.update_ui)
        
        # Dialog components
        self.dialog = None
        self.search_field = None
    
    def update_theme_colors(self):
        """Update theme colors based on current theme."""
        if self.theme == "dark":
            self.colors.update({
                "bg": "#1E1E1E", "surface": "#2D2D2D", "text": "#FFFFFF", 
                "text_secondary": "#B0B0B0", "border": "#404040", "accent": "#2196F3"
            })
        else:  # light
            self.colors.update({
                "bg": "#FFFFFF", "surface": "#F5F5F5", "text": "#212121", 
                "text_secondary": "#757575", "border": "#E0E0E0", "accent": "#2196F3"
            })
    
    def update_ui(self, event=None):
        """Update UI when theme or language changes."""
        if event and event.get("type") == "theme_event":
            theme_mode = event.get("data")
            self.theme = "dark" if theme_mode == ft.ThemeMode.DARK else "light"
            self.update_theme_colors()
        elif event and event.get("type") == "language_event":
            self.language = event.get("data", "italian")
        
        if self.page and self.dialog and self.dialog.open:
            self.show_dialog()  # Refresh dialog with new settings
    
    def show_dialog(self):
        """Show the location manager dialog."""
        if self.dialog and self.dialog in self.page.overlay:
            self.page.overlay.remove(self.dialog)
        
        self.dialog = self.create_dialog()
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def create_dialog(self):
        """Create the location manager dialog."""
        texts = self.get_texts()
        
        # Create search field
        self.search_field = ft.TextField(
            hint_text=texts['search_hint'], expand=True, border_radius=8,
            prefix_icon=ft.Icons.SEARCH, bgcolor=self.colors["surface"],
            color=self.colors["text"], hint_style=ft.TextStyle(color=self.colors["text_secondary"]),
            on_submit=self.add_location
        )
        
        # Main content
        content = ft.Container(
            content=ft.Column([
                ft.Text(texts['description'], text_align=ft.TextAlign.CENTER, 
                       size=14, color=self.colors["text_secondary"]),
                ft.Divider(color=self.colors["border"]),
                
                # Add location section
                ft.Text(texts['add_location'], weight=ft.FontWeight.BOLD, 
                       color=self.colors["text"], size=16),
                ft.Row([
                    self.search_field,
                    ft.IconButton(icon=ft.Icons.ADD, tooltip=texts['add'], on_click=self.add_location,
                                bgcolor=self.colors["accent"], icon_color=ft.Colors.WHITE)
                ], spacing=10),
                
                ft.Divider(color=self.colors["border"]),
                
                # Saved locations section
                ft.Row([
                    ft.Text(texts['saved_locations'], weight=ft.FontWeight.BOLD, 
                           color=self.colors["text"], size=16),
                    ft.TextButton(icon=ft.Icons.GPS_FIXED, text=texts['use_current'], 
                                on_click=lambda e: self.use_current_location(),
                                style=ft.ButtonStyle(color=self.colors["accent"]))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                self.create_locations_list(),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            width=500, height=400, padding=20, bgcolor=self.colors["bg"]
        )
        
        return ft.AlertDialog(
            modal=False, scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.LOCATION_ON, color=self.colors["accent"], size=24),
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
    
    def create_locations_list(self):
        """Create the list of saved locations."""
        locations_column = ft.Column([], spacing=5)
        
        for location in self.sample_locations:
            location_row = ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.STAR if location["favorite"] else ft.Icons.STAR_BORDER,
                        icon_color="#FFD700" if location["favorite"] else self.colors["text_secondary"],
                        tooltip="Toggle Favorite",
                        on_click=lambda e, loc_id=location["id"]: self.toggle_favorite(loc_id)
                    ),
                    ft.Column([
                        ft.Text(location["name"], weight=ft.FontWeight.BOLD, size=13, 
                               color=self.colors["text"]),
                        ft.Text(f"{location['lat']:.4f}, {location['lon']:.4f}", size=11, 
                               color=self.colors["text_secondary"]),
                    ], spacing=2, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.LOCATION_ON,
                        icon_color=self.colors["accent"],
                        tooltip="Use Location",
                        on_click=lambda e, loc=location: self.use_location(loc)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="#F44336",
                        tooltip="Remove",
                        on_click=lambda e, loc_id=location["id"]: self.remove_location(loc_id)
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=8,
                border=ft.border.all(1, self.colors["border"]),
                border_radius=8,
                bgcolor=self.colors["surface"]
            )
            locations_column.controls.append(location_row)
        
        return ft.Container(
            content=locations_column,
            height=150,
            padding=5
        )
    
    def get_texts(self):
        """Get localized texts based on current language."""
        if self.language == "en":
            return {
                "title": "Location Manager", "dialog_title": "Location Manager",
                "description": "Manage your saved weather locations",
                "add_location": "Add New Location", "saved_locations": "Saved Locations",
                "search_hint": "Search city name (e.g., Rome, Italy)...",
                "add": "Add", "use_current": "Use Current Location", "close": "Close"
            }
        else:  # Italian (default)
            return {
                "title": "Gestione Località", "dialog_title": "Gestione Località",
                "description": "Gestisci le tue località meteo salvate",
                "add_location": "Aggiungi Nuova Località", "saved_locations": "Località Salvate",
                "search_hint": "Cerca nome città (es: Roma, Italia)...",
                "add": "Aggiungi", "use_current": "Usa Posizione Attuale", "close": "Chiudi"
            }
    
    def add_location(self, e=None):
        """Add a new location from search field."""
        if self.search_field and self.search_field.value:
            # Simulate adding location (in real app, would geocode the search)
            new_location = {
                "id": len(self.sample_locations) + 1,
                "name": self.search_field.value,
                "lat": 45.0,  # Placeholder coordinates
                "lon": 9.0,
                "favorite": False
            }
            self.sample_locations.append(new_location)
            self.search_field.value = ""
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Località '{new_location['name']}' aggiunta"),
                    bgcolor=self.colors["accent"]
                )
                self.page.snack_bar.open = True
                self.page.update()
                
            # Refresh dialog to show new location
            self.show_dialog()
    
    def toggle_favorite(self, location_id: int):
        """Toggle favorite status of a location."""
        for location in self.sample_locations:
            if location["id"] == location_id:
                location["favorite"] = not location["favorite"]
                break
        
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Preferito aggiornato"),
                bgcolor=self.colors["accent"]
            )
            self.page.snack_bar.open = True
            self.page.update()
            
        # Refresh dialog
        self.show_dialog()
    
    def use_location(self, location):
        """Use selected location as current location."""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Usando località: {location['name']}"),
                bgcolor=self.colors["accent"]
            )
            self.page.snack_bar.open = True
            self.page.update()
        
        # Close dialog after selection
        self.close_dialog()
    
    def remove_location(self, location_id: int):
        """Remove a location from saved locations."""
        self.sample_locations = [loc for loc in self.sample_locations if loc["id"] != location_id]
        
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Località rimossa"),
                bgcolor="#F44336"
            )
            self.page.snack_bar.open = True
            self.page.update()
            
        # Refresh dialog
        self.show_dialog()
    
    def use_current_location(self):
        """Use current GPS location."""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Funzionalità GPS in sviluppo"),
                bgcolor=self.colors["accent"]
            )
            self.page.snack_bar.open = True
            self.page.update()
    
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
