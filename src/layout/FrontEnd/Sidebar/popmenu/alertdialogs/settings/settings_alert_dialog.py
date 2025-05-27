import flet as ft
from layout.frontend.sidebar.popmenu.alertdialogs.settings.location_toggle import LocationToggle
        
class SettingsAlertDialog:
    """
    A class representing a settings alert dialog in the frontend sidebar.
    This class is used to manage the display and functionality of the settings alert dialog.
    """
    def createAlertDialog(self, page):

        self.dlg = ft.AlertDialog(
            title=ft.Text("Settings"),
            content=ft.Text("You are notified!"),
            actions=[
                ft.TextButton("Close settings", on_click=lambda e: page.close(self.dlg)),
            ],
            alignment=ft.alignment.center,
            on_dismiss=lambda e: print("Dialog dismissed!"),
            title_padding=ft.padding.all(25),
        )
        
        # Creare un pulsante con testo grande
        return ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.GREY),
                    ft.Text(
                        "SETTINGS",
                        size=18,  # Dimensione aumentata
                    ),
                ]
            ),

            on_click=lambda e: page.open(self.dlg),            

        )
        
