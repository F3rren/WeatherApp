import flet as ft

class Searchbar:
    def __init__(self):
        self.search_bar = None  # salvare per accesso esterno se necessario

    def createSearchbar(self):
        def close_anchor(e):
            print(f"City selected: {e.control.data}")
            self.search_bar.close_view()

        def handle_change(e):
            print(f"handle_change e.data: {e.data}")

        def handle_submit(e):
            print(f"handle_submit e.data: {e.data}")

        def handle_tap(e):
            print("handle_tap")
            self.search_bar.open_view()

        cities = ["Milano", "Roma", "Napoli", "Torino", "Firenze"]

        self.search_bar = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.Colors.AMBER,
            bar_hint_text="Search for city...",
            view_hint_text="Choose a city from the list...",
            on_change=handle_change,
            on_submit=handle_submit,
            on_tap=handle_tap,
            controls=[
                ft.ListTile(title=ft.Text(city), on_click=close_anchor, data=city)
                for city in cities
            ],
            
        )

        return self.search_bar

    def build(self):
        return self.createSearchbar()  # nessun container, nessuna colonna: è già espandibile
