import flet as ft
from typing import Callable, Optional, List
from utils.config import DEFAULT_LANGUAGE

class SearchBar:

    def __init__(
        self,
        page: ft.Page,
        text_color: dict,  # text_color is a dict e.g. {"TEXT": "#000000", ...}
        cities: List[str] = None,
        on_city_selected: Optional[Callable] = None,
        language: str = DEFAULT_LANGUAGE,
        prefix_widget: Optional[ft.Control] = None,
        suffix_widget: Optional[ft.Control] = None,
        text_handler_get_size: Optional[Callable] = None  # aggiunto parametro
    ):
        self.cities = cities or []
        self.on_city_selected = on_city_selected
        self.page = page
        self.text_color = text_color
        self.language = language
        self.prefix_widget = prefix_widget
        self.suffix_widget = suffix_widget
        self.text_handler_get_size = text_handler_get_size  # salva funzione
        self.focused = False
        self.search_field = None

    def update_text_sizes(self, get_size_func: Callable, text_color: dict, language: str):
        # ...existing code...
        pass  # Non serve più, la gestione è locale

    def build(self, popmenu_widget=None, filter_widget=None, clear_icon_size=None) -> ft.Container:
        
        def on_submit(e):
            value = e.control.value.strip()
            print(f"DEBUG: SearchBar on_submit called with value: '{value}'")
            if value:
                if self.on_city_selected:
                    print(f"DEBUG: Calling on_city_selected callback for city: {value}")
                    # Use page.run_task for proper async handling in Flet
                    if self.page:
                        self.page.run_task(self.on_city_selected, value)
                    else:
                        # Fallback for sync callbacks
                        self.on_city_selected(value)
                else:
                    print("DEBUG: No on_city_selected callback defined")

        def clear_text(e):
            self.search_field.value = ""
            self.search_field.update()

        clear_btn = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=self.text_handler_get_size('icon'),
            on_click=clear_text,
            tooltip="Cancella",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )

        self.search_field = ft.TextField(
            text_style=ft.TextStyle(size=self.text_handler_get_size('body'), color=self.text_color.get("TEXT", "#000000")),
            border_radius=24,
            bgcolor="transparent",
            border_color="transparent",
            content_padding=ft.padding.symmetric(horizontal=10, vertical=12),
            border=ft.InputBorder.NONE,
            on_submit=on_submit,
            expand=True,
        )

        row_children = []
        #popmenu alert dialog
        if popmenu_widget:
            row_children.append(ft.Container(content=popmenu_widget, margin=ft.margin.only(right=4)))

        #searchbar field
        row_children.append(self.search_field)
        #clear button 
        row_children.append(clear_btn)

        row_children.append(ft.Container(content=filter_widget, margin=ft.margin.only(left=4)))

        row = ft.Row(
            row_children,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4
        )

        container = ft.Container(
            content=row,
            border_radius=32,
            bgcolor="#fafbfc" if self.page.theme_mode != ft.ThemeMode.DARK else "#2c2f33",
            border=ft.border.all(1, "#e0e0e0" if self.page.theme_mode != ft.ThemeMode.DARK else "#3c3f43"),
            shadow=ft.BoxShadow(blur_radius=4, color="#00000010"),
            padding=ft.padding.symmetric(horizontal=12, vertical=2),
            animate=ft.Animation(200, "decelerate"),
        )
        container_instance = container

        def on_focus_handler(e, ctrl_container):
            self.focused = True
            ctrl_container.bgcolor = "#ffffff" if self.page.theme_mode != ft.ThemeMode.DARK else "#33373b"
            ctrl_container.shadow = ft.BoxShadow(blur_radius=16, color="#1976d230")
            ctrl_container.update()

        def on_blur_handler(e, ctrl_container):
            self.focused = False
            ctrl_container.bgcolor = "#fafbfc" if self.page.theme_mode != ft.ThemeMode.DARK else "#2c2f33"
            ctrl_container.shadow = ft.BoxShadow(blur_radius=4, color="#00000010")
            ctrl_container.update()

        container.on_focus = lambda e: on_focus_handler(e, container_instance)
        container.on_blur = lambda e: on_blur_handler(e, container_instance)

        return container

    def update_cities(self, new_cities: List[str]):
        self.cities = new_cities

    def get_selected_value(self) -> str:
        if hasattr(self, 'search_field') and self.search_field:
            return self.search_field.value or ""
        return ""

    def clear_selection(self):
        if hasattr(self, 'search_field') and self.search_field:
            self.search_field.value = ""
            self.search_field.update()

    def cleanup(self):
        pass
