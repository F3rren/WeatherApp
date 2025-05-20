import flet as ft

from layout.BackEnd.Sidebar.SidebarOperations import SidebarOperations

class Searchbar:
    
    def __init__(self, on_city_selected=None):
        self.sidebarOperation = SidebarOperations()
        self.cities = self.sidebarOperation.getCapitalCities()
        self.search_bar = None
        self.on_city_selected = on_city_selected  # 👈 Callback esterna


    def createSearchbar(self):

        def close_anchor(e):
            city = e.control.data
            self.search_bar.close_view(city)
            if self.on_city_selected:
                self.on_city_selected(city)

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

    def build(self):
        return self.createSearchbar()  # nessun container, nessuna colonna: è già espandibile