"""
Sidebar for the MeteoApp.
Handles the sidebar functionality.
"""

import logging
import flet as ft
from typing import List, Callable, Optional
from services.sidebar_service import SidebarService 
from layout.frontend.sidebar.popmenu.pop_menu import PopMenu
from layout.frontend.sidebar.searchbar import SearchBar
from layout.frontend.sidebar.filter.filter import Filter
from components.responsive_text_handler import ResponsiveTextHandler

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
        self.query = SidebarService()
        self.search_bar = None
        self.cities = self._load_cities()
        
        # Initialize ResponsiveTextHandler
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'container_text': 14,  # General text in containers
                'spacing': 10,  # Base spacing value
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Dictionary to track text controls
        self.text_controls = {}
        
        # Register as observer for responsive updates
        self.text_handler.add_observer(self.update_text_controls)

    def _load_cities(self) -> List[str]:
        """Load city names from JSON (via SidebarQuery)"""
        try:
            cities_data = self.query.loadAllCity()  # dovrebbe essere una lista di dizionari
            cities_name = [item["city"] for item in cities_data if "city" in item and item["city"]]
            cities_admin = [item["admin_name"] for item in cities_data if "admin_name" in item and item["admin_name"]]
            cities_country = [item["country"] for item in cities_data if "country" in item and item["country"]]
            cities_info = sorted(zip(cities_name, cities_admin, cities_country))
            cities = [f"{name}, {admin}, {country}" for name, admin, country in cities_info]
            return cities
        except Exception as e:
            logging.error(f"Errore nel caricamento delle città: {e}")
            return []

        
    def update_location_toggle(self, value):
        """Aggiorna il valore del toggle posizione"""
        if hasattr(self, 'pop_menu'):
            self.pop_menu.update_location_toggle_value(value)
            
    def update_theme_toggle(self, value):
        """Aggiorna il valore del toggle tema"""
        if hasattr(self, 'pop_menu'):
            self.pop_menu.update_theme_toggle_value(value)
    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        for control, size_category in self.text_controls.items():
            if hasattr(control, 'size'):
                control.size = self.text_handler.get_size(size_category)
        
        # Request page update
        if self.page:
            self.page.update()

    def build(self) -> ft.Container:
        """Build the sidebar"""
        # Create search bar with page for ResponsiveTextHandler
        self.search_bar = SearchBar(self.cities, self.on_city_selected, self.page)
          # Create pop menu with location toggle callback
        self.pop_menu = PopMenu(
            page=self.page,
            state_manager=self.page.session.get('state_manager'),
            translation_service=self.page.session.get('translation_service'),
            handle_location_toggle=self.handle_location_toggle,
            handle_theme_toggle=self.handle_theme_toggle,
            theme_toggle_value=self.theme_toggle_value,
            location_toggle_value=self.location_toggle_value
        )

        self.filter = Filter(
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
                        col={"xs": 1, "md": 1},
                    ),
                    ft.Container(
                        content=self.search_bar.build(),
                        col={"xs": 10, "md": 10},
                    ),                    ft.Container(
                        content=self.filter.build(self.page),
                        col={"xs": 2, "md": 1},
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                run_spacing=10,
            )
        )

    def cleanup(self):
        """Cleanup method to remove observers"""
        if hasattr(self, 'text_handler') and self.text_handler:
            self.text_handler.remove_observer(self.update_text_controls)
        
        # Cleanup child components
        if hasattr(self, 'search_bar') and self.search_bar:
            if hasattr(self.search_bar, 'cleanup'):
                self.search_bar.cleanup()