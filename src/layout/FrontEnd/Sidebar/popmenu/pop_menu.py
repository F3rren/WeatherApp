import flet as ft

from layout.frontend.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog


class PopMenu:

    def __init__(self):
        self.setting_alert = SettingsAlertDialog()
        
    def createPopMenu(self, page=None):

        # Crea il menu popup con tutte le opzioni
        pb = ft.PopupMenuButton(
            icon=ft.Icons.MENU, 
            icon_size=50,
            items=[
                self.setting_alert.createAlertDialog(page),

                # Altre opzioni
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SUNNY, color=ft.Colors.YELLOW),
                        ft.Text("Meteo", size=20),
                    ]),
                    on_click=lambda e: print("Meteo clicked")
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.MAP_OUTLINED, color=ft.Colors.GREEN),
                        ft.Text("Mappa", size=20),
                    ]),
                    on_click=lambda e: print("Map clicked")
                )
            ]
        )
        
        return pb
    
    def update_location_toggle_value(self, value):
        """
        Aggiorna il valore interno dello stato del toggle della localizzazione.
        Da chiamare quando lo stato cambia esternamente.
        """
        self.location_toggle_value = value
        
    def build(self, page=None):
        return ft.Container(
            content=ft.Column([
                self.createPopMenu(page)
            ])
        )