import flet as ft
from typing import Callable, Optional, List

class SearchBar:
    def __init__(self,
                 page: ft.Page,
                 text_color: dict, # text_color is a dict e.g. {"TEXT": "#000000", ...}
                 text_handler_get_size: Callable,
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
        self._text_handler_get_size = text_handler_get_size
        self._prefix_widget = prefix_widget
        self._suffix_widget = suffix_widget

    def update_text_sizes(self, get_size_func: Callable, text_color: dict, language: str):
        self._text_handler_get_size = get_size_func
        self._text_color = text_color
        self._language = language
        if self.page:
            self.page.update()

    def build(self) -> ft.Container:
        self._snackbar = ft.SnackBar(
            content=ft.Text(""),
            bgcolor="#ffcccc", # Consider a theme-based color
            duration=2000
        )

        # Note: show_city_not_found is defined but not used in the current build method.
        # If it's intended for use with on_submit or other logic, it should be called.
        # def show_city_not_found(city_name):
        #     self._snackbar.content.value = f"La città '{city_name}' non esiste." # Localize
        #     self.page.snack_bar = self._snackbar
        #     self._snackbar.open = True
        #     self.page.update()

        def on_submit(e):
            value = e.control.value.strip()
            if value:
                if self.on_city_selected:
                    res = self.on_city_selected(value)
                    if hasattr(res, '__await__'):
                        import asyncio
                        async def run_and_update():
                            await res
                        try:
                            asyncio.run(run_and_update())
                        except RuntimeError:
                            # If already in an event loop, fallback to create_task (for completeness)
                            asyncio.create_task(run_and_update())
                        # No return here, TextField handles its own update on submit typically
                # self.page.update() # Avoid redundant updates if on_city_selected handles it

        self._focused = False
        # Container needs to be defined before on_focus and on_blur can reference it.
        # This will be addressed by defining `container` later and then assigning these methods
        # or by passing `container` to them if they become static/helper methods.
        # For now, assuming `container` will be accessible in their scope.

        initial_text_style = None
        if self._text_handler_get_size:
            initial_size = self._text_handler_get_size('body')
            color = self._text_color.get("TEXT", "#000000") # Default color if not in dict
            if initial_size is not None:
                initial_text_style = ft.TextStyle(size=initial_size, color=color)
            else:
                initial_text_style = ft.TextStyle(color=color)

        def clear_text(e):
            search_field.value = ""
            search_field.update() # Update only the TextField

        clear_btn = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=18,
            on_click=clear_text,
            tooltip="Cancella", # Localize
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )

        search_field = ft.TextField(
            hint_text="Cerca città...", # Localize
            text_style=initial_text_style,
            border_radius=24,
            bgcolor="transparent",
            border_color="transparent", # Usually no border shown directly on TextField in this style
            content_padding=ft.padding.symmetric(horizontal=10, vertical=12), # Adjusted padding
            border=ft.InputBorder.NONE,
            on_submit=on_submit,
            # on_focus and on_blur will be set on the outer container
            expand=True,
        )

        row_children = []
        if self._prefix_widget:
            row_children.append(self._prefix_widget)

        # Add a small margin if prefix widget exists to separate it from icon
        search_icon_margin = ft.margin.only(left=8) if self._prefix_widget else ft.margin.only(left=0)
        row_children.append(
            ft.Container(
                content=ft.Icon(ft.Icons.SEARCH, size=20, color=self._text_color.get("ICON", "#888888")),
                margin=search_icon_margin
            )
        )
        row_children.append(search_field)
        row_children.append(clear_btn) # Suffix clear button

        if self._suffix_widget:
            row_children.append(self._suffix_widget)

        row = ft.Row(
            row_children,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
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
