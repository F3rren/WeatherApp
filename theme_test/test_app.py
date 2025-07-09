import flet as ft
from theme_handler import ThemeHandler
from utils.config import LIGHT_THEME, DARK_THEME
class TestComponent():
    def __init__(self, theme_handler):
        super().__init__()
        self.theme_handler = theme_handler

    def build(self):
        return ft.Column([
            ft.Text("Testo principale", color=self.theme_handler.get_color("TEXT")),
            ft.Text("Testo secondario", color=self.theme_handler.get_color("SECONDARY_TEXT")),
            ft.ElevatedButton("Cambia tema", on_click=self.toggle_theme)
        ])

    def toggle_theme(self, e):
        # Cambia il tema della pagina
        self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        self.page.update()
        self.update()

def main(page: ft.Page):
    theme_handler = ThemeHandler(page)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(TestComponent(theme_handler))

if __name__ == "__main__":
    ft.app(target=main)
