import flet as ft
from layout.FrontEnd.Sidebar.PopMenu import PopMenu
from layout.FrontEnd.Sidebar.Searchbar import Searchbar

class Sidebar:
    def __init__(self, page):
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626"
        self.txtcolor = "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff"
        self.page = page
        self.popMenu = PopMenu()
        self.searchbar = Searchbar()

    def build(self):
        return ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=self.popMenu.build(),
                        col={"xs": 2, "md": 1},  # stretto
                        alignment=ft.alignment.center_left
                    ),
                    ft.Container(
                        content=self.searchbar.build(),
                        col={"xs": 10, "md": 11},  # largo
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                run_spacing=10,
            )
        )
