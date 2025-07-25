import logging
import flet as ft
import os
from typing import Callable, Optional, List

from services.ui.theme_handler import ThemeHandler

class SearchBar:

    def __init__(self, page: ft.Page, cities: List[str] = None, on_city_selected: Optional[Callable] = None,
        language: str = None, prefix_widget: Optional[ft.Control] = None, suffix_widget: Optional[ft.Control] = None,
        theme_handler: ThemeHandler = None
    ):
        self.cities = cities or []
        self.on_city_selected = on_city_selected
        self.page = page
        self.theme_handler = theme_handler or ThemeHandler(page)
        self.language = language or os.getenv("DEFAULT_LANGUAGE")
        self.prefix_widget = prefix_widget
        self.suffix_widget = suffix_widget
        self.focused = False
        self.search_field = None

    def update_text_sizes(self, get_size_func: Callable, language: str):
        pass  # Non serve più, la gestione è locale

    def build(self, popmenu_widget=None, filter_widget=None, clear_icon_size=None) -> ft.Container:
        
        def on_submit(e):
            value = e.control.value.strip()
            logging.info(f"DEBUG: SearchBar on_submit called with value: '{value}'")
            if value:
                if self.on_city_selected:
                    logging.info(f"DEBUG: Calling on_city_selected callback for city: {value}")
                    # Use page.run_task for proper async handling in Flet
                    if self.page:
                        self.page.run_task(self.on_city_selected, value)
                    else:
                        # Fallback for sync callbacks
                        self.on_city_selected(value)
                else:
                    logging.error("DEBUG: No on_city_selected callback defined")

        def clear_text(e):
            self.search_field.value = ""
            self.search_field.update()

        clear_btn = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=14,
            on_click=clear_text,
            tooltip="Cancella",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )

        # Use theme_handler for text color if available
        text_color = self.theme_handler.get_text_color() if self.theme_handler else self.text_color.get("TEXT", "#000000")
        self.search_field = ft.TextField(
            text_style=ft.TextStyle(size=14, color=text_color),
            border_radius=24,
            bgcolor="transparent",
            border_color="transparent",
            content_padding=ft.padding.symmetric(horizontal=10, vertical=12),
            border=ft.InputBorder.NONE,
            on_submit=on_submit,
            expand=True,
        )

        row_children = []
        
        #searchbar field - ora prende più spazio
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

        # Use theme_handler for background and border if available
        bg_color = self.theme_handler.get_background_color('sidebar_search') if self.theme_handler else ("#fafbfc" if self.page.theme_mode != ft.ThemeMode.DARK else "#2c2f33")
        border_color = self.theme_handler.get_theme().get("BORDER", "#e0e0e0" if self.page.theme_mode != ft.ThemeMode.DARK else "#3c3f43") if self.theme_handler else ("#e0e0e0" if self.page.theme_mode != ft.ThemeMode.DARK else "#3c3f43")
        container = ft.Container(
            content=row,
            border_radius=32,
            bgcolor=bg_color,
            border=ft.border.all(1, border_color),
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
