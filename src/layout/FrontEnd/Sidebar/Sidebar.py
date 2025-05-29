"""
Sidebar for the MeteoApp.
Handles the sidebar functionality.
"""

import flet as ft
from typing import List, Callable, Optional
from layout.backend.sidebar.sidebarquery import SidebarQuery
from layout.frontend.sidebar.popmenu.pop_menu import PopMenu
from layout.frontend.sidebar.searchbar import SearchBar

class Sidebar:
    """
    Sidebar component for the MeteoApp.
    """
    def __init__(self, page: ft.Page, on_city_selected: Optional[Callable] = None, 
                handle_location_toggle: Optional[Callable] = None, location_toggle_value: bool = False,
                handle_theme_toggle: Optional[Callable] = None, theme_toggle_value: bool = False):
        self.page = page
        self.on_city_selected = on_city_selected
        self.handle_location_toggle = handle_location_toggle
        self.location_toggle_value = location_toggle_value
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.query = SidebarQuery()
        
        self.cities = self._load_cities()

    def _load_cities(self) -> List[str]:
        """Load city names from JSON (via SidebarQuery)"""
        try:
            cities_data = self.query.loadAllCity()  # dovrebbe essere una lista di dizionari
            city_names = sorted([item["city"] for item in cities_data if "city" in item])
            return city_names
        except Exception as e:
            print(f"Errore nel caricamento delle città: {e}")
            return []

        
    def update_location_toggle(self, value):
        """Aggiorna il valore del toggle posizione"""
        if hasattr(self, 'pop_menu'):
            self.pop_menu.update_location_toggle_value(value)
            
    def update_theme_toggle(self, value):
        """Aggiorna il valore del toggle tema"""
        if hasattr(self, 'pop_menu'):
            self.pop_menu.update_theme_toggle_value(value)
    
    def build(self) -> ft.Container:
        """Build the sidebar"""
        # Create search bar
        search_bar = SearchBar(self.cities, self.on_city_selected)
        
        # Create pop menu with location toggle callback
        self.pop_menu = PopMenu(
            page=self.page,
            state_manager=self.page.session.get('state_manager'),
            handle_location_toggle=self.handle_location_toggle,
            handle_theme_toggle=self.handle_theme_toggle,
            theme_toggle_value=self.theme_toggle_value,
            location_toggle_value=self.location_toggle_value
        )
        
        # Create sidebar container
        return ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=self.pop_menu.build(self.page),
                        col={"xs": 2, "md": 1},
                        alignment=ft.alignment.center_left
                    ),
                    ft.Container(
                        content=search_bar.build(),
                        col={"xs": 10, "md": 11},
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                run_spacing=10,
            )
        )