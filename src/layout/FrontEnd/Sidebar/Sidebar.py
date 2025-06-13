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
# from components.responsive_text_handler import ResponsiveTextHandler

class Sidebar:
    """
    Sidebar component for the MeteoApp.
    """
    def __init__(self, page: ft.Page, on_city_selected: Optional[Callable] = None, 
                handle_location_toggle: Optional[Callable] = None, location_toggle_value: bool = False,
                handle_theme_toggle: Optional[Callable] = None, theme_toggle_value: bool = False,
                # New parameters for styling and language
                text_color: dict = None, # Changed to dict
                language: str = "en",
                text_handler_get_size: Optional[Callable] = None):
        self.page = page
        self.on_city_selected = on_city_selected
        self.handle_location_toggle = handle_location_toggle
        self.location_toggle_value = location_toggle_value
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.query = SidebarService()
        self.search_bar = None
        self.cities = self._load_cities()

        # Store passed-in style and language parameters
        self._text_color = text_color if text_color is not None else {"TEXT": "#000000"} # Ensure default
        self._language = language
        self._text_handler_get_size = text_handler_get_size # Function to get responsive size

        # PopMenu and Filter will be created in build() and might need these params
        self.pop_menu: Optional[PopMenu] = None
        self.filter_control: Optional[Filter] = None # Renamed to avoid conflict
        
        # No longer owns ResponsiveTextHandler or text_controls directly
        # self.text_handler = ResponsiveTextHandler(...)
        # self.text_controls = {}
        # self.text_handler.add_observer(self.update_text_controls)

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
        """Aggiorna il valore del toggle posizione nella UI del PopMenu."""
        self.location_toggle_value = value # Update internal state
        if self.pop_menu:
            self.pop_menu.update_location_toggle_value(value)
            
    def update_theme_toggle(self, value):
        """Aggiorna il valore del toggle tema nella UI del PopMenu."""
        self.theme_toggle_value = value # Update internal state
        if self.pop_menu:
            self.pop_menu.update_theme_toggle_value(value)

    # Removed update_text_controls as ResponsiveTextHandler is managed by SidebarManager
    # def update_text_controls(self): ...

    def update_internal_text_sizes(self, get_size_func: Callable, text_color: dict, language: str):
        """Chiamato da SidebarManager per aggiornare le dimensioni del testo dei componenti interni."""
        self._text_handler_get_size = get_size_func
        self._text_color = text_color # Update current text_color
        self._language = language # Update current language

        # Aggiorna i componenti che usano text_handler_get_size, es. SearchBar, PopMenu, Filter
        if self.search_bar and hasattr(self.search_bar, 'update_text_sizes'):
            self.search_bar.update_text_sizes(self._text_handler_get_size, self._text_color, self._language)
        if self.pop_menu and hasattr(self.pop_menu, 'update_text_sizes'):
            self.pop_menu.update_text_sizes(self._text_handler_get_size, self._text_color, self._language)
        if self.filter_control and hasattr(self.filter_control, 'update_text_sizes'):
            self.filter_control.update_text_sizes(self._text_handler_get_size, self._text_color, self._language)
        if self.page:
            self.page.update() # Potrebbe essere necessario per riflettere le modifiche

    def build(self) -> ft.Container:
        """Build the sidebar"""
        # Pass text_color, language, and text_handler_get_size to child components
        self.search_bar = SearchBar(
            cities=self.cities, 
            on_city_selected=self.on_city_selected, 
            page=self.page,
            text_color=self._text_color,
            language=self._language, # Pass language
            text_handler_get_size=self._text_handler_get_size
        )
        
        self.pop_menu = PopMenu(
            page=self.page,
            state_manager=self.page.session.get('state_manager'),
            translation_service=self.page.session.get('translation_service'),
            handle_location_toggle=self.handle_location_toggle,
            handle_theme_toggle=self.handle_theme_toggle,
            theme_toggle_value=self.theme_toggle_value,
            location_toggle_value=self.location_toggle_value,
            text_color=self._text_color,
            language=self._language,
            text_handler_get_size=self._text_handler_get_size
        )

        self.filter_control = Filter(
            page=self.page,
            state_manager=self.page.session.get('state_manager'),
            # handle_location_toggle and handle_theme_toggle might not be needed if PopMenu handles them
            # theme_toggle_value and location_toggle_value might also be managed via PopMenu or state
            text_color=self._text_color,
            language=self._language,
            text_handler_get_size=self._text_handler_get_size
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
                        content=self.filter_control.build(self.page),
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
        # ResponsiveTextHandler is no longer owned here
        # if hasattr(self, 'text_handler') and self.text_handler:
        #     self.text_handler.remove_observer(self.update_text_controls)
        
        # Cleanup child components
        if hasattr(self, 'search_bar') and self.search_bar:
            if hasattr(self.search_bar, 'cleanup'):
                self.search_bar.cleanup()
        if hasattr(self, 'pop_menu') and self.pop_menu:
            if hasattr(self.pop_menu, 'cleanup'):
                self.pop_menu.cleanup()
        if hasattr(self, 'filter_control') and self.filter_control:
            if hasattr(self.filter_control, 'cleanup'):
                self.filter_control.cleanup()
        logging.info("Sidebar class cleanup completed.")