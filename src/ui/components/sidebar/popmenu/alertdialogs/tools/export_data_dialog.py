#!/usr/bin/env python3

import flet as ft
from services.ui.translation_service import TranslationService


class ExportDataDialog:
    """Dialog per esportare i dati meteorologici."""
    
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
            self.dialog.title.value = TranslationService.translate_from_dict("popup_menu_items", "export_data", self.language)
            self.page.update()
    
    def create_dialog(self):
        """Crea il dialog per l'esportazione dati."""
        return ft.AlertDialog(
            modal=False,
            title=ft.Text(
                TranslationService.translate_from_dict("popup_menu_items", "export_data", self.language),
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.DOWNLOAD, size=64, color="#3F51B5"),
                    ft.Text(
                        "Esporta i dati meteorologici in diversi formati",
                        text_align=ft.TextAlign.CENTER,
                        size=16
                    ),
                    ft.Divider(),
                    ft.Text("Seleziona il periodo:", weight=ft.FontWeight.BOLD),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value="week", label="Ultima settimana"),
                            ft.Radio(value="month", label="Ultimo mese"),
                            ft.Radio(value="year", label="Ultimo anno"),
                            ft.Radio(value="custom", label="Periodo personalizzato"),
                        ]),
                        value="week"
                    ),
                    ft.Divider(),
                    ft.Text("Seleziona i dati:", weight=ft.FontWeight.BOLD),
                    ft.Column([
                        ft.Checkbox(label="Temperature", value=True),
                        ft.Checkbox(label="Umidità", value=True),
                        ft.Checkbox(label="Precipitazioni", value=False),
                        ft.Checkbox(label="Vento", value=False),
                        ft.Checkbox(label="Pressione", value=False),
                    ]),
                    ft.Divider(),
                    ft.Text("Formato di esportazione:", weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        width=200,
                        options=[
                            ft.dropdown.Option("csv", "CSV"),
                            ft.dropdown.Option("excel", "Excel (.xlsx)"),
                            ft.dropdown.Option("json", "JSON"),
                            ft.dropdown.Option("pdf", "PDF Report"),
                        ],
                        value="csv"
                    ),
                ], spacing=10),
                padding=20,
                width=400,
                height=500
            ),
            actions=[
                ft.TextButton(
                    icon=ft.Icons.SAVE,
                    text=TranslationService.translate_from_dict("dialog_buttons", "export", self.language),
                    on_click=self._export_data,
                    style=ft.ButtonStyle(
                        bgcolor="#5C73F5",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=TranslationService.translate("close", self.language),
                    on_click=self.close_dialog,
                    style=ft.ButtonStyle(
                        bgcolor="#3F51B5",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def _export_data(self, e):
        """Esporta i dati selezionati."""
        # TODO: Implementare l'esportazione dati
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Esportazione dati completata!"),
            bgcolor="#3F51B5"
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
