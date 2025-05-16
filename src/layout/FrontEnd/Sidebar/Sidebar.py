import flet as ft
from flet import Icons

class Sidebar:

    def __init__(self, page):
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" 
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" 
        page.update()

    def create_sidebar(self):
        buttons = []
        buttons.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.IconButton(
                            icon=Icons.WB_SUNNY,  # Weather, 
                            icon_color=ft.Colors.YELLOW, 
                            icon_size=30, 
                            tooltip="Weather",
                        ),
                        ft.Text("Weather", size=12, color=self.txtcolor, weight="bold"),
                        ft.IconButton(
                            icon=Icons.MAP_OUTLINED,  # Cities
                            icon_color=ft.Colors.CYAN, 
                            icon_size=30, 
                            tooltip="Cities",
                        ),
                        ft.Text("Cities", size=12, color=self.txtcolor, weight="bold"),
                        ft.IconButton(
                            icon=Icons.MAP_OUTLINED,  # Map
                            icon_color=ft.Colors.GREEN, 
                            icon_size=30, 
                            tooltip="Map",
                        ),
                        ft.Text("Map", size=12, color=self.txtcolor, weight="bold"),
                        ft.IconButton(
                            icon=ft.Icons.SETTINGS_OUTLINED,
                            icon_color=ft.Colors.BLACK,
                            icon_size=30,
                            tooltip="Settings",
                        ),
                        ft.Text("Settings", size=12, color=self.txtcolor, weight="bold")
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
            )
        )
        return buttons

    def build(self):
        return ft.Container(
            bgcolor = self.bgcolor,
            border_radius=15,
            padding=20,
            margin=10,
            content=ft.Column(controls=self.create_sidebar())
        )
