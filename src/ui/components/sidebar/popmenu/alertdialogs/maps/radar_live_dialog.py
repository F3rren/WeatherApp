#!/usr/bin/env python3

import flet as ft
from services.ui.translation_service import TranslationService


class RadarLiveDialog:
    """Dialog per il radar meteorologico live."""
    
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
            self.dialog.title.value = TranslationService.translate_from_dict("popup_menu_items", "radar_live", self.language)
            self.page.update()
    
    def create_dialog(self):
        """Crea il dialog per il radar live."""
        return ft.AlertDialog(
            modal=False,
            title=ft.Text(
                TranslationService.translate_from_dict("popup_menu_items", "radar_live", self.language),
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.RADAR, size=64, color="#E91E63"),
                    ft.Text(
                        "Monitoraggio radar delle precipitazioni in tempo reale.",
                        text_align=ft.TextAlign.CENTER,
                        size=16
                    ),
                    ft.Divider(),
                    ft.Row([
                        ft.Icon(ft.Icons.WATER_DROP, color="#2196F3", size=20),
                        ft.Text("Intensità delle precipitazioni", size=14)
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.SPEED, color="#FF9800", size=20),
                        ft.Text("Velocità di movimento delle nuvole", size=14)
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.TIMELINE, color="#4CAF50", size=20),
                        ft.Text("Animazione delle ultime 3 ore", size=14)
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, color="#F44336", size=20),
                        ft.Text("Zoom sulla tua posizione", size=14)
                    ]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                width=400,
                height=300
            ),
            actions=[
                ft.TextButton(
                    icon=ft.Icons.SEARCH,
                    text=TranslationService.translate_from_dict("dialog_buttons", "open_radar_live", self.language),
                    on_click=self._open_radar_live,
                    style=ft.ButtonStyle(
                        bgcolor="#EC6693",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
                
                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=TranslationService.translate_from_dict("dialog_buttons", "close", self.language),
                    on_click=self.close_dialog,
                    style=ft.ButtonStyle(
                        bgcolor="#E91E63",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def _open_radar_live(self, e):
        """Apre il radar live."""
        # TODO: Implementare il radar live
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Radar Live in sviluppo"),
            bgcolor="#E91E63"
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
