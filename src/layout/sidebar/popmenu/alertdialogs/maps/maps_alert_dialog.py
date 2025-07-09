import flet as ft
import webbrowser

from components.state_manager import StateManager
from .map_view import MapView

class MapsAlertDialog:
    def __init__(self, page: ft.Page, state_manager: StateManager):
        self.page = page
        self.state_manager = state_manager
        self.dialog = None
        self.map_view_instance = None
        self.current_city = None
        self.current_lat = None
        self.current_lon = None

    def build(self):
        """Costruisce l'interfaccia dell'AlertDialog con supporto tema chiaro/scuro."""
        self.map_view_instance = MapView(self.page, lat=self.current_lat, lon=self.current_lon)

        # Supporto dark mode per il background del dialog
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        dialog_bg = "#161b22" if is_dark else "#ffffff"

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Mappa Meteo - {self.current_city}"),
            bgcolor=dialog_bg,
            content=ft.Container(
                content=self.map_view_instance.build(),
                width=800,
                height=600,
                bgcolor=dialog_bg,
                opacity=1.0,
            ),
            actions=[
                ft.TextButton("Schermo Intero", on_click=self._open_fullscreen_map),
                ft.TextButton("Chiudi", on_click=self.close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: self.close_dialog(e), # Add this line to close on outside click
        )
        return dialog

    def open_dialog(self):
        """Apre il dialogo dopo aver aggiornato la posizione dallo StateManager."""
        self.current_city = self.state_manager.get_state('city')
        self.current_lat = self.state_manager.get_state('current_lat')
        self.current_lon = self.state_manager.get_state('current_lon')

        # Fallback to default if values are None
        if self.current_city is None:
            self.current_city = "N/A"
        if self.current_lat is None or self.current_lon is None:
            self.current_lat = None  # Default to Rome
            self.current_lon = None

        self.dialog = self.build()
        
        if self.page and self.dialog:
            if self.dialog not in self.page.controls:
                self.page.controls.append(self.dialog)
            self.page.dialog = self.dialog
            self.page.dialog.open = True
            self.page.update()

    def close_dialog(self, e=None):
        """Close the dialog when close button is clicked"""
        if self.dialog and hasattr(self.dialog, 'open'):
            self.dialog.open = False
            self.page.update()

    def _open_fullscreen_map(self, e=None):
        """Apre la mappa a schermo intero nel browser."""
        fullscreen_url = f"https://www.windy.com/?{self.current_lat},{self.current_lon},8"
        webbrowser.open(fullscreen_url)
