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
        # self.autocomplete: Optional[ft.AutoComplete] = None # Type hint

        # Store new parameters
        self._text_color = text_color 
        self._language = language 
        self._text_handler_get_size = text_handler_get_size
        
    def update_text_sizes(self, get_size_func: Callable, text_color: dict, language: str):
        """Called by parent to update text sizes and colors."""
        self._text_handler_get_size = get_size_func
        self._text_color = text_color # text_color is a dict
        self._language = language 

        # if self.autocomplete and self._text_handler_get_size:
        #     current_size = self._text_handler_get_size('body') 
        #     text_input_color = self._text_color.get("TEXT")

        #     if text_input_color is not None and current_size is not None:
        #         self.autocomplete.text_style = ft.TextStyle(
        #             size=current_size,
        #             color=text_input_color
        #         )
        #     elif current_size is not None: # Only size available
        #         self.autocomplete.text_style = ft.TextStyle(size=current_size)
        #     elif text_input_color is not None: # Only color available
        #          self.autocomplete.text_style = ft.TextStyle(color=text_input_color)
        #     # else: no style to apply or clear existing if necessary
        #     #    self.autocomplete.text_style = None 

        if self.page:
            self.page.update()

    def build(self, prefix_widget=None, suffix_widget=None) -> ft.Container:
        """SearchBar stile Firefox: pill, ombra e sfondo al focus, icona search a sinistra, clear a destra, animazione espansione.
        Ora accetta un widget prefix (es. PopMenu) e suffix opzionale (es. PopMenu a destra)."""
        self._snackbar = ft.SnackBar(
            content=ft.Text(""),
            bgcolor="#ffcccc",
            duration=2000
        )

        def show_city_not_found(city_name):
            self._snackbar.content.value = f"La città '{city_name}' non esiste."
            self.page.snack_bar = self._snackbar
            self._snackbar.open = True
            self.page.update()

        def on_submit(e):
            value = e.control.value.strip()
            if value:
                if self.on_city_selected:
                    res = self.on_city_selected(value)
                    if hasattr(res, '__await__'):
                        import asyncio
                        async def run_and_update():
                            await res
                            self.page.update()
                        asyncio.create_task(run_and_update())
                        return
                self.page.update()

        # Stato per focus/espansione
        self._focused = False
        def on_focus(e):
            self._focused = True
            container.bgcolor = "#fff" if not self.page.theme_mode == ft.ThemeMode.DARK else "#23272f"
            container.shadow = ft.BoxShadow(blur_radius=16, color="#1976d220")
            container.width = 340
            container.update()
        def on_blur(e):
            self._focused = False
            container.bgcolor = "#fafbfc" if not self.page.theme_mode == ft.ThemeMode.DARK else "#23272f"
            container.shadow = ft.BoxShadow(blur_radius=4, color="#00000010")
            container.width = 280
            container.update()

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

        # Pulsante clear
        def clear_text(e):
            search_field.value = ""
            search_field.update()
        clear_btn = ft.IconButton(icon=ft.Icons.CLOSE, icon_size=18, on_click=clear_text, tooltip="Cancella", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)))

        search_field = ft.TextField(
            hint_text="Cerca città...",
            text_style=initial_text_style,
            border_radius=24,
            bgcolor="transparent",
            border_color="#e0e0e0",
            content_padding=ft.padding.symmetric(horizontal=0, vertical=12),
            border=ft.InputBorder.NONE,
            on_submit=on_submit,
            on_focus=on_focus,
            on_blur=on_blur,
            expand=True,
        )

        row_children = []
        if prefix_widget:
            row_children.append(prefix_widget)
        row_children.append(ft.Icon(ft.Icons.SEARCH, size=20, color="#888"))
        row_children.append(search_field)
        row_children.append(clear_btn)
        if suffix_widget:
            row_children.append(suffix_widget)

        row = ft.Row(row_children, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)

        container = ft.Container(
            content=row,
            border_radius=32,
            bgcolor="#fafbfc" if not self.page.theme_mode == ft.ThemeMode.DARK else "#23272f",
            border=ft.border.all(1, "#e0e0e0" if not self.page.theme_mode == ft.ThemeMode.DARK else "#333"),
            shadow=ft.BoxShadow(blur_radius=4, color="#00000010"),
            padding=ft.padding.symmetric(horizontal=12, vertical=0),
            animate=ft.Animation(200, "decelerate"),
        )
        return container
    
    def update_cities(self, new_cities: List[str]):
        """Aggiorna l'elenco delle città disponibili"""
        self.cities = new_cities
        # if self.autocomplete:
        #     suggestions = [
        #         ft.AutoCompleteSuggestion(key=city, value=city)
        #         for city in self.cities
        #     ]
        #     self.autocomplete.suggestions = suggestions
        #     self.autocomplete.update() 
    
    def get_selected_value(self) -> str:
        """Restituisce il valore attualmente selezionato"""
        # if self.autocomplete:
        #     return self.autocomplete.value or ""
        return ""
    
    def clear_selection(self):
        """Pulisce la selezione corrente"""
        # if self.autocomplete:
        #     self.autocomplete.value = ""
        #     self.autocomplete.update()
    
    def cleanup(self):
        """Cleanup method to remove observers"""
        pass 
    
    # def get_autocomplete_only(self) -> ft.AutoComplete:
    #     """Restituisce solo il componente AutoComplete senza la toolbox"""
    #     return self.autocomplete
