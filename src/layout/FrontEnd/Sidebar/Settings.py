import flet as ft

class Settings:
    def __init__(self, page: ft.Page):
        self.page = page

    def create_settings_dialog(self):
        return ft.AlertDialog(
            title=ft.Text("Impostazioni"),
            content=ft.Text("Desideri modificare le impostazioni dell'app?"),
            actions=[
                ft.TextButton("OK", on_click=self.handle_settings_change),
                ft.TextButton("Annulla", on_click=self.close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def handle_settings_change(self, e):
        self.page.add(ft.Text("Impostazioni aggiornate"))
        self.close_dialog()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()
