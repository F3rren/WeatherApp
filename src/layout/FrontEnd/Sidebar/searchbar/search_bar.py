import flet as ft
from typing import Callable, Optional, List
from components.responsive_text_handler import ResponsiveTextHandler

class SearchBar:
    def __init__(self,
                 page: ft.Page,
                 text_color: dict, # text_color is a dict e.g. {"TEXT": "#000000", ...}
                 cities: List[str] = None,
                 on_city_selected: Optional[Callable] = None,
                 language: str = "en",
                 prefix_widget: Optional[ft.Control] = None,
                 suffix_widget: Optional[ft.Control] = None):
        self.cities = cities or []
        self.on_city_selected = on_city_selected
        self.page = page
        self._text_color = text_color
        self._language = language
        self._prefix_widget = prefix_widget
        self._suffix_widget = suffix_widget
        # ResponsiveTextHandler locale
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'body': 16,
                'icon': 24,
                'icon_filter': 24,
                'icon_clear': 24,
            },
            breakpoints=[600, 900, 1200, 1600]
        )

    def update_text_sizes(self, get_size_func: Callable, text_color: dict, language: str):
        # ...existing code...
        pass  # Non serve più, la gestione è locale

    def build(self, popmenu_widget=None, filter_widget=None, clear_icon_size=None) -> ft.Container:
        self._snackbar = ft.SnackBar(
            content=ft.Text(""),
            bgcolor="#ffcccc",
            duration=2000
        )

        def on_submit(e):
            value = e.control.value.strip()
            if value:
                if self.on_city_selected:
                    res = self.on_city_selected(value)
                    if hasattr(res, '__await__'):
                        import asyncio
                        async def run_and_update():
                            await res
                            # self.page.update() # Page update might be handled by the callback itself
                        asyncio.create_task(run_and_update())
                        # No return here, TextField handles its own update on submit typically
                # self.page.update() # Avoid redundant updates if on_city_selected handles it

        self._focused = False

        get_size = self._text_handler.get_size
        initial_size = get_size('body')
        color = self._text_color.get("TEXT", "#000000") # Default color if not in dict
        initial_text_style = ft.TextStyle(size=initial_size, color=color)

        # Determina la grandezza delle icone tramite text_handler_get_size
        icon_size = get_size('icon')

        def clear_text(e):
            search_field.value = ""
            search_field.update()

        clear_btn = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=get_size('icon_clear'),
            on_click=clear_text,
            tooltip="Cancella",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )

        search_field = ft.TextField(
            hint_text="Cerca città...",
            text_style=initial_text_style,
            border_radius=24,
            bgcolor="transparent",
            border_color="transparent",
            content_padding=ft.padding.symmetric(horizontal=10, vertical=12),
            border=ft.InputBorder.NONE,
            on_submit=on_submit,
            expand=True,
        )

        row_children = []
        # PopMenu a sinistra
        if popmenu_widget:
            row_children.append(ft.Container(content=popmenu_widget, margin=ft.margin.only(right=4)))
        # Icona search
        row_children.append(ft.Container(
            content=ft.Icon(ft.Icons.SEARCH, size=icon_size, color=self._text_color.get("ICON", "#888888")),
            margin=ft.margin.only(right=4)
        ))
        row_children.append(search_field)
        row_children.append(clear_btn)
        if filter_widget:
            # Forza la size del filtro
            filter_widget.icon_size = get_size('icon_filter') if hasattr(filter_widget, 'icon_size') else get_size('icon_filter')
            row_children.append(ft.Container(content=filter_widget, margin=ft.margin.only(left=4)))

        row = ft.Row(
            row_children,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4
        )

        # Define container here so on_focus and on_blur can access it
        container = ft.Container(
            content=row,
            border_radius=32,
            bgcolor="#fafbfc" if self.page.theme_mode != ft.ThemeMode.DARK else "#2c2f33", # Theme-aware
            border=ft.border.all(1, "#e0e0e0" if self.page.theme_mode != ft.ThemeMode.DARK else "#3c3f43"), # Theme-aware
            shadow=ft.BoxShadow(blur_radius=4, color="#00000010"),
            padding=ft.padding.symmetric(horizontal=12, vertical=2), # Adjusted vertical padding
            animate=ft.Animation(200, "decelerate"),
        )
        container_instance = container # Assign to a variable that can be captured by lambda

        def on_focus_handler(e, ctrl_container): # ctrl_container is the ft.Container instance
            self._focused = True
            ctrl_container.bgcolor = "#ffffff" if self.page.theme_mode != ft.ThemeMode.DARK else "#33373b" # Theme-aware
            ctrl_container.shadow = ft.BoxShadow(blur_radius=16, color="#1976d230") # Softer shadow
            # ctrl_container.width = 340 # Optional: Animate width
            ctrl_container.update()

        def on_blur_handler(e, ctrl_container): # ctrl_container is the ft.Container instance
            self._focused = False
            ctrl_container.bgcolor = "#fafbfc" if self.page.theme_mode != ft.ThemeMode.DARK else "#2c2f33" # Theme-aware
            ctrl_container.shadow = ft.BoxShadow(blur_radius=4, color="#00000010")
            # ctrl_container.width = 280 # Optional: Animate width
            ctrl_container.update()

        # Assign handlers now that container_instance is defined
        container.on_focus = lambda e: on_focus_handler(e, container_instance)
        container.on_blur = lambda e: on_blur_handler(e, container_instance)


        return container

    def update_cities(self, new_cities: List[str]):
        self.cities = new_cities
        # If using an AutoComplete feature, update its suggestions here

    def get_selected_value(self) -> str:
        # This would typically get the value from the search_field if needed externally
        # For now, SearchBar primarily uses on_city_selected callback
        if hasattr(self, 'search_field') and self.search_field:
             return self.search_field.value or ""
        return ""

    def clear_selection(self):
        if hasattr(self, 'search_field') and self.search_field:
            self.search_field.value = ""
            self.search_field.update()

    def cleanup(self):
        pass
