import flet as ft
from typing import Callable, Optional, List

class SearchBar:
    def __init__(self, cities: List[str] = None, on_city_selected: Optional[Callable] = None):
        self.cities = cities or []
        self.on_city_selected = on_city_selected
        self.search_bar = None
        self.filtered_cities = self.cities.copy()

    def build(self) -> ft.SearchBar:
        async def close_anchor(e):
            city = e.control.data
            self.search_bar.close_view(city)
            if self.on_city_selected:
                # Supporta callback async
                if callable(self.on_city_selected):
                    res = self.on_city_selected(city)
                    if hasattr(res, '__await__'):
                        import asyncio
                        asyncio.create_task(res)

        def handle_change(e):
            query = e.data.lower() if e.data else ""
            self.filtered_cities = [c for c in self.cities if query in c.lower()][:10]
            self.search_bar.controls = [
                ft.ListTile(title=ft.Text(city if isinstance(city, str) else str(city)), on_click=close_anchor, data=city)
                for city in self.filtered_cities
            ]
            self.search_bar.update()

        def handle_submit(e):
            if self.filtered_cities:
                city = self.filtered_cities[0]
                self.search_bar.close_view(city)
                if self.on_city_selected:
                    # Supporta callback async
                    if callable(self.on_city_selected):
                        res = self.on_city_selected(city)
                        if hasattr(res, '__await__'):
                            import asyncio
                            asyncio.create_task(res)

        def handle_tap(e):
            self.search_bar.open_view()

        self.search_bar = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.Colors.AMBER,
            bar_hint_text="Cerca città...",
            view_hint_text="Scegli una città dalla lista...",
            on_change=handle_change,
            on_submit=handle_submit,
            on_tap=handle_tap,
            controls=[
                ft.ListTile(title=ft.Text(city if isinstance(city, str) else str(city)), on_click=close_anchor, data=city)
                for city in self.filtered_cities[:10]
            ],
        )
        return self.search_bar
