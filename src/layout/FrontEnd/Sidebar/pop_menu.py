import flet as ft


class PopMenu:


    def createPopMenu(self, page=None):

        setting_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete all those files?"),
            actions=[
                ft.TextButton("Yes", on_click=lambda e: page.close(setting_modal)),
                ft.TextButton("No", on_click=lambda e: page.close(setting_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        setting_btn = ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOCATION_CITY, color=ft.Colors.CYAN),
                            ft.Text("Cities", size=20),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    on_click=lambda e: page.open(setting_modal)
                )

        pb = ft.PopupMenuButton(
            icon=ft.Icons.MENU, 
            icon_size=50,
            items=[
                    setting_btn,
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOCATION_CITY, color = ft.Colors.CYAN),
                            ft.Text("Cities", size=20,),
                        ]
                    ),
                    on_click=lambda e: print("Cities"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.MAP_OUTLINED, color = ft.Colors.GREEN),
                            ft.Text("Map", size=20,),
                        ]
                    ),
                    on_click=lambda e: print("Map"),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SETTINGS_OUTLINED, color = ft.Colors.BLACK),
                            ft.Text("Settings", size=20,),
                        ]
                    ),
                    on_click=lambda e: print("Settings"),
                ),
            ]
        )
        return pb
    
    def build(self, page=None):
        return ft.Container(
            content=ft.Column([
                self.createPopMenu(page)
            ])            
        )