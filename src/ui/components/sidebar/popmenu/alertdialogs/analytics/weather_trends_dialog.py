#!/usr/bin/env python3

import flet as ft
from services.ui.translation_service import TranslationService


class WeatherTrendsDialog:
    """Dialog per visualizzare le tendenze meteorologiche."""
    
    def __init__(self, page: ft.Page, state_manager=None, language=None):
        self.page = page
        self.state_manager = state_manager
        self.language = language or (state_manager.get_state("language", "en") if state_manager else "en")
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
            self.dialog.title.value = TranslationService.translate_from_dict("popup_menu_items", "weather_trends", self.language)
            self.page.update()
    
    def create_dialog(self):
        """Crea il dialog per le tendenze meteorologiche."""
        return ft.AlertDialog(
            modal=False,
            title=ft.Text(
                TranslationService.translate_from_dict("popup_menu_items", "weather_trends", self.language),
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.TRENDING_UP, size=64, color="#4CAF50"),
                    ft.Text(
                        "Analizza le tendenze meteorologiche a lungo termine per la tua zona.",
                        text_align=ft.TextAlign.CENTER,
                        size=16
                    ),
                    ft.Divider(),
                    ft.Row([
                        ft.Icon(ft.Icons.TIMELINE, color="#2196F3", size=20),
                        ft.Text("Grafici di tendenza mensili e stagionali", size=14)
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.COMPARE_ARROWS, color="#FF9800", size=20),
                        ft.Text("Confronto con anni precedenti", size=14)
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.INSIGHTS, color="#9C27B0", size=20),
                        ft.Text("Previsioni basate sui dati storici", size=14)
                    ]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                width=400,
                height=300
            ),
            actions=[
                ft.FilledButton(
                    icon=ft.Icons.VIEW_COMFY,
                    text=TranslationService.translate_from_dict("dialog_buttons", "view_trends", self.language),
                    on_click=self._open_trends_view,
                    style=ft.ButtonStyle(
                        bgcolor="#4CAF50",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
                
                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=TranslationService.translate_from_dict("settings_alert_dialog_items", "close", self.language),
                    on_click=lambda e: self.close_dialog(e),
                    style=ft.ButtonStyle(
                        bgcolor="#378039",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def _open_trends_view(self, e):
        """Apre la vista delle tendenze meteorologiche."""
        # TODO: Implementare la vista delle tendenze
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Funzionalità Tendenze Meteo in sviluppo"),
            bgcolor="#4CAF50"
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
