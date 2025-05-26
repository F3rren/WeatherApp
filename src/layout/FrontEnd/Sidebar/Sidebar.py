"""
Modern sidebar component with search and location features.
"""

import flet as ft
from typing import Optional, Callable
from layout.frontend.sidebar.pop_menu import PopMenu
from layout.frontend.sidebar.searchbar import SearchBar
from layout.backend.sidebar.sidebarquery import SidebarQuery

class Sidebar:
    def __init__(
        self,
        page: ft.Page,
        on_city_select: Optional[Callable] = None,
        on_location_toggle: Optional[Callable] = None,
        on_theme_change: Optional[Callable] = None,
        on_units_change: Optional[Callable] = None,
        on_language_change: Optional[Callable] = None,
    ):
        self.page = page
        self.on_city_select = on_city_select
        self.on_location_toggle = on_location_toggle
        self.on_theme_change = on_theme_change
        self.on_units_change = on_units_change
        self.on_language_change = on_language_change
        self.query = SidebarQuery()
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626"
        self.txtcolor = "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff"
        self.cities = self._load_cities()
        self.searchbar = SearchBar(cities=self.cities, on_city_selected=self.on_city_select)

    def _load_cities(self):
        """Load cities from database"""
        try:
            cities_data = self.query.loadAllCity()
            return sorted([item["city"] for item in cities_data if "city" in item])
        except Exception as e:
            print(f"Error loading cities: {e}")
            return []
            
    def build(self) -> ft.Container:
        """Build the sidebar"""
        return ft.Container(
            bgcolor=self.bgcolor,
            content=ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=PopMenu()._create_pop_menu(),
                        col={"xs": 2, "md": 1},
                        alignment=ft.alignment.center_left
                    ),
                    ft.Container(
                        content=self.searchbar.build(),
                        col={"xs": 10, "md": 11},
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                run_spacing=10,
            ),
            padding=ft.padding.symmetric(horizontal=10, vertical=10),
            border_radius=15,
        )
    
    def _show_settings(self, e):
        """Show settings dialog"""
        self.page.dialog = self.settings_dialog.show()
        self.page.dialog.open = True
        self.page.update()
