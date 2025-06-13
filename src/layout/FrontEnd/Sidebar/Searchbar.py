import logging
import flet as ft
from typing import Callable, Optional, List

class SearchBar:
    def __init__(self, 
                 page: ft.Page, 
                 text_color: dict, # text_color is a dict e.g. {"TEXT": "#000000", ...}
                 text_handler_get_size: Callable, # Made required
                 cities: List[str] = None, 
                 on_city_selected: Optional[Callable] = None, 
                 language: str = "en"):
        self.cities = cities or []
        self.on_city_selected = on_city_selected
        self.page = page
        self.autocomplete: Optional[ft.AutoComplete] = None # Type hint

        # Store new parameters
        self._text_color = text_color 
        self._language = language 
        self._text_handler_get_size = text_handler_get_size
        
    def update_text_sizes(self, get_size_func: Callable, text_color: dict, language: str):
        """Called by parent to update text sizes and colors."""
        self._text_handler_get_size = get_size_func
        self._text_color = text_color # text_color is a dict
        self._language = language 

        if self.autocomplete and self._text_handler_get_size:
            current_size = self._text_handler_get_size('body') 
            text_input_color = self._text_color.get("TEXT")

            if text_input_color is not None and current_size is not None:
                self.autocomplete.text_style = ft.TextStyle(
                    size=current_size,
                    color=text_input_color
                )
            elif current_size is not None: # Only size available
                self.autocomplete.text_style = ft.TextStyle(size=current_size)
            elif text_input_color is not None: # Only color available
                 self.autocomplete.text_style = ft.TextStyle(color=text_input_color)
            # else: no style to apply or clear existing if necessary
            #    self.autocomplete.text_style = None 

        if self.page:
            self.page.update()

    def build(self) -> ft.Column:
        """Builds and returns the search bar component"""
        
        async def handle_select(e):
            """Gestisce la selezione di una città"""
            try:
                selected_city = e.selection
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
                logging.error(f"Errore in handle_select: {ex}")
                
        suggestions = [
            ft.AutoCompleteSuggestion(key=city, value=city)
            for city in self.cities
        ]
        
        self.autocomplete = ft.AutoComplete(
            suggestions=suggestions,
            on_select=handle_select,
            suggestions_max_height=300
            # Removed text_size and color from constructor
        )

        initial_text_style = None
        if self._text_handler_get_size: 
            initial_size = self._text_handler_get_size('body')
            color = self._text_color.get("TEXT")
            if initial_size is not None and color is not None:
                initial_text_style = ft.TextStyle(size=initial_size, color=color)
            elif initial_size is not None:
                initial_text_style = ft.TextStyle(size=initial_size)
            elif color is not None:
                initial_text_style = ft.TextStyle(color=color)
        
        if initial_text_style: # Apply text_style after creation
            self.autocomplete.text_style = initial_text_style
        
        # Example for hint text styling, if you add a hint_text to AutoComplete:
        # self.autocomplete.hint_text="Search..."
        # hint_style_color = self._text_color.get("HINT", self._text_color.get("TEXT_SECONDARY"))
        # if self._text_handler_get_size and hint_style_color:
        #     self.autocomplete.hint_style = ft.TextStyle(
        #         size=self._text_handler_get_size('body_small'), 
        #         color=hint_style_color
        #     )

        styled_autocomplete = ft.Container(
            content=self.autocomplete,
            padding=ft.padding.all(8),
        )
        
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
    
    def cleanup(self):
        """Cleanup method to remove observers"""
        pass 
    
    def get_autocomplete_only(self) -> ft.AutoComplete:
        """Restituisce solo il componente AutoComplete senza la toolbox"""
        return self.autocomplete
