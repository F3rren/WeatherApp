#!/usr/bin/env python3

import flet as ft
from services.ui.translation_service import TranslationService


class SatelliteViewDialog:
    """Dialog per la vista satellitare."""
    
    def __init__(self, page: ft.Page, state_manager=None, language=None):
        self.page = page
        self.state_manager = state_manager
        self.language = language or "en"
        self.dialog = None
        
        # Observer per aggiornamenti di lingua e tema
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_language)
            self.state_manager.register_observer("theme_event", self.update_ui)
        
    def update_language(self, language):
        """Aggiorna la lingua del dialog."""
        self.language = language
        if self.dialog:
            self.update_ui()
            
    def update_ui(self, *args):
        """Aggiorna l'UI del dialog."""
        if self.dialog:
            self.dialog.title.value = TranslationService.translate_from_dict("popup_menu_items", "satellite_view", self.language)
            self.page.update()
    
    def create_dialog(self):
        """Crea il dialog per la vista satellitare."""
        return ft.AlertDialog(
            modal=False,
            title=ft.Text(
                TranslationService.translate_from_dict("popup_menu_items", "satellite_view", self.language),
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.SATELLITE_ALT, size=64, color="#607D8B"),
                    ft.Text(
                        "Visualizza immagini satellitari in tempo reale della tua zona.",
                        text_align=ft.TextAlign.CENTER,
                        size=16
                    ),
                    ft.Divider(),
                    ft.Row([
                        ft.Icon(ft.Icons.CLOUD, color="#2196F3", size=20),
                        ft.Text("Copertura nuvolosa in tempo reale", size=14)
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.VISIBILITY, color="#4CAF50", size=20),
                        ft.Text("Vista ad alta risoluzione", size=14)
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.LAYERS, color="#FF9800", size=20),
                        ft.Text("Layer di temperatura e vento", size=14)
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.REFRESH, color="#9C27B0", size=20),
                        ft.Text("Aggiornamento ogni 15 minuti", size=14)
                    ]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                width=400,
                height=300
            ),
            actions=[
                ft.FilledButton(
                    icon=ft.Icons.SEARCH,
                    text=TranslationService.translate_from_dict("dialog_buttons", "open_satellite_view", self.language),
                    on_click=self._open_satellite_view,
                    style=ft.ButtonStyle(
                        bgcolor="#98A3A8",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),

                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=TranslationService.translate_from_dict("dialog_buttons", "close", self.language),
                    on_click=lambda e: self.close_dialog(e),
                    style=ft.ButtonStyle(
                        bgcolor="#607D8B",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def _open_satellite_view(self, e):
        """Apre la vista satellitare."""
        # TODO: Implementare la vista satellitare
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Vista Satellite in sviluppo"),
            bgcolor="#607D8B"
        )
        self.page.snack_bar.open = True
        self.page.update()
        self.close_dialog(e)
    
    def show_dialog(self):
        """Mostra il dialog."""
        self.dialog = self.create_dialog()
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def close_dialog(self, e=None):
        """Close the dialog when close button is clicked"""
        if self.dialog and hasattr(self.dialog, 'open'):
            self.dialog.open = False
            self.page.update()

    def cleanup(self):
        """Cleanup del dialog."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_language)
            self.state_manager.unregister_observer("theme_event", self.update_ui)
