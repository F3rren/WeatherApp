import flet as ft

from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_language import DropdownLanguage
from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_measurement import DropdownMeasurement

class SettingsAlertDialog:
    """
    Versione semplificata per test dell'alert dialog delle impostazioni.
    """
    def __init__(self, state_manager=None):
        self.state_manager = state_manager
        self.language_dropdown = DropdownLanguage(state_manager)
        self.measurement_dropdown = DropdownMeasurement(state_manager)

    def createAlertDialog(self, page):
        # Dialog semplificato per test
        self.dlg = ft.AlertDialog(
            title=ft.Text("Settings", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                controls=[
                    # Sezione lingua
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.LANGUAGE, size=20),
                            ft.Text("Language:", size=14),
                            self.language_dropdown.build(),
                        ],
                        spacing=10,
                    ),
                    # Sezione unità di misura
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.STRAIGHTEN, size=20),
                            ft.Text("Measurement:", size=14),
                            self.measurement_dropdown.build(),
                        ],
                        spacing=10,
                    ),
                ],
                height=150,
                spacing=20,
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: page.close(self.dlg)),
            ],
            on_dismiss=lambda e: print("Dialog closed"),
        )
        
        # Pulsante semplificato per aprire il dialog
        return ft.ElevatedButton(
            text="Settings",
            icon=ft.Icons.SETTINGS,
            on_click=lambda e: page.open(self.dlg),
        )