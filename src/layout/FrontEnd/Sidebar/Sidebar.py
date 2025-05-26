import flet as ft
from layout.FrontEnd.Sidebar.PopMenu import PopMenu
from layout.FrontEnd.Sidebar.Searchbar import Searchbar

class Sidebar:

    def __init__(self, page, on_city_selected=None):
        self.page = page
        self.on_city_selected = on_city_selected  
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626"
        self.txtcolor = "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff"
        self.searchbar = Searchbar(on_city_selected=self.on_city_selected) 

    def build(self):
        return ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=PopMenu().build(),
                        col={"xs": 2, "md": 1},
                        alignment=ft.alignment.center_left
                    ),
                    ft.Container(
                        content=self.searchbar.build(), 
                        col={"xs": 10, "md": 11},
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                run_spacing=10,
            )
        )
