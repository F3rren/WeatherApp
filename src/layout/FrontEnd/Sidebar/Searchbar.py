import flet as ft
from typing import Callable, Optional, List

class SearchBar:
    def __init__(self, cities: List[str] = None, on_city_selected: Optional[Callable] = None):
        self.cities = cities or []
        self.on_city_selected = on_city_selected
        self.autocomplete = None

    def build(self) -> ft.Column:
        # Crea una barra degli strumenti (Toolbox) con un'etichetta
    
        async def handle_select(e):
            """Gestisce la selezione di una città"""
            try:
                selected_city = e.selection
                # If selection is an AutoCompleteSuggestion, extract the value
                if hasattr(selected_city, "value"):
                    selected_city_value = selected_city.value
                else:
                    selected_city_value = selected_city
                if selected_city_value and self.on_city_selected:
                    if callable(self.on_city_selected):
                        res = self.on_city_selected(selected_city_value)
                        if hasattr(res, '__await__'):
                            await res
            except Exception as ex:
                print(f"Errore in handle_select: {ex}")

        # Crea le suggestions dall'elenco delle città
        suggestions = [
            ft.AutoCompleteSuggestion(key=city, value=city)
            for city in self.cities
        ]

        self.autocomplete = ft.AutoComplete(
            suggestions=suggestions,
            on_select=handle_select,
            suggestions_max_height=300,
        )
        
        # Avvolgiamo l'AutoComplete in un Container per il styling
        styled_autocomplete = ft.Container(
            content=self.autocomplete,
            padding=ft.padding.all(8),
        )
        
        # Restituisce una colonna con toolbox e autocomplete stilizzato
        return ft.Column(
            controls=[
                styled_autocomplete,
            ],
            spacing=5,
            tight=True,
        )
    
    def update_cities(self, new_cities: List[str]):
        """Aggiorna l'elenco delle città disponibili"""
        self.cities = new_cities
        if self.autocomplete:
            suggestions = [
                ft.AutoCompleteSuggestion(key=city, value=city)
                for city in self.cities
            ]
            self.autocomplete.suggestions = suggestions
            self.autocomplete.update()
    
    def get_selected_value(self) -> str:
        """Restituisce il valore attualmente selezionato"""
        if self.autocomplete:
            return self.autocomplete.value or ""
        return ""
    
    def clear_selection(self):
        """Pulisce la selezione corrente"""
        if self.autocomplete:
            self.autocomplete.value = ""
            self.autocomplete.update()
    
    def get_autocomplete_only(self) -> ft.AutoComplete:
        """Restituisce solo il componente AutoComplete senza la toolbox"""
        return self.autocomplete
    
    def get_toolbox_only(self) -> ft.Container:
        """Restituisce solo la toolbox senza l'autocomplete"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.LOCATION_CITY, color=ft.Colors.AMBER, size=20),
                    ft.Text("Scrivi il nome della città:", size=14, weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.padding.only(bottom=10),
        )
