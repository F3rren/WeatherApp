import flet as ft

class PopMenu:

    def createPopMenu(self):
        pb = ft.PopupMenuButton(
            icon=ft.Icons.MENU, 
            icon_size=50,
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.WB_SUNNY, color = ft.Colors.YELLOW),
                            ft.Text("Weather", size=20),
                        ]
                    ),
                    on_click=lambda _: print("Weather"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOCATION_CITY, color = ft.Colors.CYAN),
                            ft.Text("Cities", size=20,),
                        ]
                    ),
                    on_click=lambda _: print("Cities"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.MAP_OUTLINED, color = ft.Colors.GREEN),
                            ft.Text("Map", size=20,),
                        ]
                    ),
                    on_click=lambda _: print("Map"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SETTINGS_OUTLINED, color = ft.Colors.BLACK),
                            ft.Text("Settings", size=20,),
                        ]
                    ),
                    on_click=lambda _: print("Settings"),
                ),
            ]
        )
        return pb
    
    def build(self):
        return ft.Container(
            content=ft.Column([self.createPopMenu()],
            )            
        )