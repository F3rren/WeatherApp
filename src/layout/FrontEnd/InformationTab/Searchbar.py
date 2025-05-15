import flet as ft

class Searchbar:

    def createSearchbar(self):  # Usa 'self' qui
        def close_anchor(e):
            text = f"Color {e.control.data}"
            print(f"closing view from {text}")
            anchor.close_view(text)

        def handle_change(e):
            print(f"handle_change e.data: {e.data}")

        def handle_submit(e):
            print(f"handle_submit e.data: {e.data}")

        def handle_tap(e):
            print("handle_tap")
            anchor.open_view()

        anchor = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.Colors.AMBER,
            bar_hint_text="Search for city...",
            view_hint_text="Choose a color from the suggestions...",
            on_change=handle_change,
            on_submit=handle_submit,
            on_tap=handle_tap,
            controls=[ft.ListTile(title=ft.Text(f"Color {i}"), on_click=close_anchor, data=i) for i in range(10)],
        )

        return anchor

    def build(self):
        return ft.Container(
            padding=10,
            content=ft.Column(controls=[self.createSearchbar()])
        )
