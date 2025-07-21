#!/usr/bin/env python3

import flet as ft
from services.ui.translation_service import TranslationService
from services.location.location_manager_service import LocationManagerService


class LocationManagerDialog:
    """Dialog per gestire le località salvate."""
    
    def __init__(self, page: ft.Page, state_manager=None, language=None):
        self.page = page
        self.state_manager = state_manager
        self.language = language or (state_manager.get_state("language", "en") if state_manager else "en")
        self.dialog = None
        self.location_service = LocationManagerService()
        self.search_field = None
        self.locations_column = None
        
        # Observer per aggiornamenti di lingua e tema
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_language)
            self.state_manager.register_observer("theme_event", self.update_ui)
        # Località di esempio
        self.sample_locations = [
            {"name": "Roma, Italia", "coords": "41.9028, 12.4964", "favorite": True},
            {"name": "Milano, Italia", "coords": "45.4642, 9.1900", "favorite": False},
            {"name": "Napoli, Italia", "coords": "40.8518, 14.2681", "favorite": False},
        ]
        
    def update_language(self, language):
        """Aggiorna la lingua del dialog."""
        self.language = language
        if self.dialog:
            self.update_ui()
            
    def update_ui(self, *args):
        """Aggiorna l'UI del dialog."""
        if self.dialog:
            self.dialog.title.value = TranslationService.translate_from_dict("popup_menu_items", "location_manager", self.language)
            self.page.update()
    
    def create_locations_list(self):
        """Crea la lista delle località."""
        self.locations_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=250)
        
        locations = self.location_service.get_all_locations()
        
        for location in locations:
            location_row = ft.Row([
                ft.IconButton(
                    icon=ft.Icons.STAR if location.get("favorite", False) else ft.Icons.STAR_BORDER,
                    icon_color="#FFD700" if location.get("favorite", False) else "#757575",
                    tooltip="Toggle Preferito",
                    on_click=lambda e, loc_id=location["id"]: self._toggle_favorite(loc_id)
                ),
                ft.Column([
                    ft.Text(location["name"], weight=ft.FontWeight.BOLD, size=14),
                    ft.Text(f"{location['lat']:.4f}, {location['lon']:.4f}", size=12, color="#757575"),
                ], spacing=2, expand=True),
                ft.IconButton(
                    icon=ft.Icons.LOCATION_ON,
                    icon_color="#2196F3",
                    tooltip="Usa questa località",
                    on_click=lambda e, loc=location: self._use_location(loc)
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color="#F44336",
                    tooltip="Rimuovi",
                    on_click=lambda e, loc_id=location["id"]: self._remove_location(loc_id)
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            
            self.locations_column.controls.append(
                ft.Container(
                    content=location_row,
                    padding=10,
                    border=ft.border.all(1, "#E0E0E0"),
                    border_radius=8,
                    margin=ft.margin.only(bottom=5)
                )
            )
        
        if not locations:
            self.locations_column.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Nessuna località salvata",
                        text_align=ft.TextAlign.CENTER,
                        color="#757575"
                    ),
                    padding=20
                )
            )
        
        return self.locations_column
    
    def create_dialog(self):
        """Crea il dialog per il gestore località."""
        self.search_field = ft.TextField(
            hint_text="Cerca per nome città (es: Roma, Italia)...",
            expand=True,
            prefix_icon=ft.Icons.SEARCH,
            on_submit=self._search_and_add_location
        )
        
        return ft.AlertDialog(
            modal=False,
            title=ft.Text(
                TranslationService.translate_from_dict("popup_menu_items", "location_manager", self.language),
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Gestisci le tue località salvate",
                        text_align=ft.TextAlign.CENTER,
                        size=16,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Divider(),
                    ft.Row([
                        self.search_field,
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            tooltip="Aggiungi",
                            on_click=self._search_and_add_location,
                            bgcolor="#4CAF50",
                            icon_color="white"
                        )
                    ]),
                    ft.Divider(),
                    ft.Text("Località salvate:", weight=ft.FontWeight.BOLD),
                    self.create_locations_list(),
                ]),
                padding=20,
                width=500,
                height=450
            ),
            actions=[
                ft.TextButton(
                    icon=ft.Icons.GPS_FIXED,
                    text=TranslationService.translate_from_dict("dialog_buttons", "use_current_location", self.language),
                    on_click=self._use_current_location,
                    style=ft.ButtonStyle(
                        bgcolor="#6ABBFD",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=TranslationService.translate_from_dict("dialog_buttons", "close", self.language),
                    on_click=self.close_dialog,
                    style=ft.ButtonStyle(
                        bgcolor="#2196F3",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def _toggle_favorite(self, location_id):
        """Toggle lo stato preferito di una località."""
        if self.location_service.toggle_favorite(location_id):
            self._refresh_locations_list()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Preferito aggiornato"),
                bgcolor="#4CAF50"
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _use_location(self, location):
        """Usa la località selezionata."""
        if self.state_manager:
            self.state_manager.set_state("selected_location", {
                "name": location["name"],
                "lat": location["lat"], 
                "lon": location["lon"]
            })
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Località impostata: {location['name']}"),
            bgcolor="#2196F3"
        )
        self.page.snack_bar.open = True
        self.page.update()
        self.close_dialog()
    
    def _remove_location(self, location_id):
        """Rimuove una località."""
        if self.location_service.remove_location(location_id):
            self._refresh_locations_list()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Località rimossa"),
                bgcolor="#F44336"
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _refresh_locations_list(self):
        """Aggiorna la lista delle località."""
        if self.dialog and self.locations_column:
            # Trova il container della lista e aggiorna i suoi controlli
            new_list = self.create_locations_list()
            self.locations_column.controls = new_list.controls
            self.page.update()
    
    def _search_and_add_location(self, e=None):
        """Cerca e aggiunge una nuova località."""
        if not self.search_field.value:
            return
            
        # Per ora aggiungiamo una località di esempio basata sul testo
        # TODO: Integrare con un servizio di geocoding reale
        search_text = self.search_field.value.strip()
        
        # Esempio di parsing semplice per "Città, Paese"
        if "," in search_text:
            # Coordinate di esempio (andrebbero ottenute da un servizio di geocoding)
            # Per ora usiamo coordinate casuali vicino a Roma
            import random
            lat = 41.9 + random.uniform(-0.5, 0.5)
            lon = 12.5 + random.uniform(-0.5, 0.5)
            
            if self.location_service.add_location(search_text, lat, lon, ""):
                self.search_field.value = ""
                self._refresh_locations_list()
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Località aggiunta: {search_text}"),
                    bgcolor="#4CAF50"
                )
                self.page.snack_bar.open = True
                self.page.update()
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Località già esistente o errore"),
                    bgcolor="#F44336"
                )
                self.page.snack_bar.open = True
                self.page.update()
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Formato: Città, Paese"),
                bgcolor="#FF9800"
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _use_current_location(self, e):
        """Usa la posizione corrente."""
        # TODO: Implementare il GPS
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Funzionalità GPS in sviluppo"),
            bgcolor="#2196F3"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def show_dialog(self):
        """Mostra il dialog."""
        self.dialog = self.create_dialog()
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def close_dialog(self, e=None):
        """Chiude il dialog."""
        if self.dialog:
            self.dialog.open = False
            self.page.update()
            if self.dialog in self.page.overlay:
                self.page.overlay.remove(self.dialog)
    
    def cleanup(self):
        """Cleanup del dialog."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_language)
            self.state_manager.unregister_observer("theme_event", self.update_ui)
