import flet as ft
from flet import Icons


def main(self, page: ft.Page):

    pb = ft.PopupMenuButton(
        icon=ft.Icons.MENU, 
        items=[
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.WB_SUNNY, color = ft.Colors.YELLOW, icon_size=30),
                        ft.Text("Weather", size=12, color=self.txtcolor, weight="bold"),
                    ]
                ),
                on_click=lambda _: self.on_select("weather") if self.on_select else print("Weather")
            ),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.LOCATION_CITY, color = ft.Colors.CYAN),
                        ft.Text("Cities", size=12, color=self.txtcolor, weight="bold"),
                    ]
                ),
                on_click=lambda _: print("Cities"),
            ),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.MAP_OUTLINED, color = ft.Colors.GREEN),
                        ft.Text("Map", size=12, color=self.txtcolor, weight="bold"),
                    ]
                ),
                on_click=lambda _: self.on_select("weather") if self.on_select else print("Weather")
            ),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.SETTINGS_OUTLINED, color = ft.Colors.BLACK),
                        ft.Text("Settings", size=12, color=self.txtcolor, weight="bold"),
                    ]
                ),
                on_click=lambda _: print("Settings"),
            ),
            
        ]
    )
    page.add(pb)

if __name__ == "__main__":
    ft.app(main)