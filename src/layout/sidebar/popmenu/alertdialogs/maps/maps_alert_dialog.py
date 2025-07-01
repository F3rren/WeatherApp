import flet as ft
import webbrowser
from .map_view import MapView

class MapsAlertDialog:
    def __init__(self, page: ft.Page, state_manager=None, language: str = "en"):
        self.page = page
        self.state_manager = state_manager
        self.dialog = None
        self.map_view_instance = None

        # Proprietà della mappa
        self.current_city = "Roma"
        self.current_lat = 41.9028
        self.current_lon = 12.4964
        
        # Costruisce il dialogo inizialmente
        self.update_ui()

    def update_ui(self, event_data=None):
        """Aggiorna e ricostruisce il dialogo."""
        self.dialog = self.build()

    def build(self):
        """Costruisce l'interfaccia dell'AlertDialog."""
        self._update_location()  # Assicura che la posizione sia aggiornata
        
        self.map_view_instance = MapView(self.page, lat=self.current_lat, lon=self.current_lon)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Mappa Meteo - {self.current_city}"),
            content=ft.Container(
                content=self.map_view_instance.build(),
                width=800,
                height=600,
            ),
            actions=[
                ft.TextButton("Schermo Intero", on_click=self._open_fullscreen_map),
                ft.TextButton("Chiudi", on_click=self.close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog

    def _update_location(self):
        """Aggiorna la posizione corrente dall'istanza principale dell'app."""
        try:
            main_app = self.page.session.get('main_app')
            if main_app and hasattr(main_app, 'weather_view_instance'):
                weather_view = main_app.weather_view_instance
                if hasattr(weather_view, 'current_coordinates') and weather_view.current_coordinates:
                    self.current_lat = float(weather_view.current_coordinates[0])
                    self.current_lon = float(weather_view.current_coordinates[1])
                if hasattr(weather_view, 'current_city') and weather_view.current_city:
                    self.current_city = weather_view.current_city
        except Exception as e:
            print(f"Mappe: Impossibile aggiornare la posizione: {e}")

    def open_dialog(self):
        if not self.dialog:
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
