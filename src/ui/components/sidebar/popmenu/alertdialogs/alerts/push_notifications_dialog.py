#!/usr/bin/env python3

import flet as ft
from services.ui.translation_service import TranslationService


class PushNotificationsDialog:
    """Dialog per gestire le notifiche push."""
    
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
            self.dialog.title.value = TranslationService.translate_from_dict("popup_menu_items", "push_notifications", self.language)
            self.page.update()
    
    def create_dialog(self):
        """Crea il dialog per le notifiche push."""
        return ft.AlertDialog(
            modal=False,
            title=ft.Text(
                TranslationService.translate_from_dict("popup_menu_items", "push_notifications", self.language),
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.NOTIFICATIONS, size=64, color="#FF9800"),
                    ft.Text(
                        "Configura le notifiche push per ricevere aggiornamenti meteo importanti.",
                        text_align=ft.TextAlign.CENTER,
                        size=16
                    ),
                    ft.Divider(),
                    ft.Row([
                        ft.Checkbox(label="Allerte meteo severe", value=True),
                    ]),
                    ft.Row([
                        ft.Checkbox(label="Previsioni mattutine", value=False),
                    ]),
                    ft.Row([
                        ft.Checkbox(label="Aggiornamenti orari", value=False),
                    ]),
                    ft.Row([
                        ft.Checkbox(label="Cambiamenti di temperatura", value=True),
                    ]),
                    ft.Row([
                        ft.Checkbox(label="Probabilità di pioggia", value=True),
                    ]),
                    ft.Divider(),
                    ft.Row([
                        ft.Text("Orario notifiche:", size=14, weight=ft.FontWeight.BOLD),
                        ft.Dropdown(
                            width=150,
                            options=[
                                ft.dropdown.Option("07:00"),
                                ft.dropdown.Option("08:00"),
                                ft.dropdown.Option("09:00"),
                            ],
                            value="08:00"
                        )
                    ]),
                ], horizontal_alignment=ft.CrossAxisAlignment.START),
                padding=20,
                width=450,
                height=400
            ),
            actions=[
                ft.TextButton(
                    icon=ft.Icons.SAVE,
                    text=TranslationService.translate_from_dict("dialog_buttons", "save_settings", self.language),
                    on_click=self._save_settings,
                    style=ft.ButtonStyle(
                        bgcolor="#F8B249",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=TranslationService.translate_from_dict("dialog_buttons", "close", self.language),
                    on_click=lambda e: self.close_dialog(e),
                    style=ft.ButtonStyle(
                        bgcolor="#FF9800",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def _save_settings(self, e):
        """Salva le impostazioni delle notifiche."""
        # TODO: Implementare il salvataggio delle impostazioni
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Impostazioni notifiche salvate"),
            bgcolor="#FF9800"
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
