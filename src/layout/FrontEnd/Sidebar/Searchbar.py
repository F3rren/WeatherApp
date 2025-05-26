import flet as ft
from typing import Callable, Optional, List
import asyncio

class SearchBar:
    """
    A search bar for searching cities.
    """
    
    def __init__(self, cities: List[str], on_city_selected: Optional[Callable] = None):
        self.cities = cities
        self.on_city_selected = on_city_selected
        self.search_bar = None
    
    def build(self) -> ft.SearchBar:
        """Build the search bar"""
        async def close_anchor(e):
            city = e.control.data
            self.search_bar.close_view(city)
            if self.on_city_selected:
                # Create a task to run the async callback without blocking
                asyncio.create_task(self.on_city_selected(city))

        def handle_tap(e):
            self.search_bar.open_view()

        self.search_bar = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.Colors.AMBER,
            bar_hint_text="Search for city...",
            view_hint_text="Choose a city from the list...",
            on_tap=handle_tap,
            controls=[
                ft.ListTile(title=ft.Text(city), on_click=close_anchor, data=city)
                for city in self.cities
            ],
        )

        return self.search_bar
