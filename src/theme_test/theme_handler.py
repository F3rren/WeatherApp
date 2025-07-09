
import flet as ft

from config import DARK_THEME, LIGHT_THEME



class ThemeHandler:
    def __init__(self, page: ft.Page):
        self.page = page

    def get_theme(self):
        theme_mode = self.page.theme_mode if self.page else ft.ThemeMode.LIGHT
        return LIGHT_THEME if theme_mode == ft.ThemeMode.LIGHT else DARK_THEME

    def get_color(self, role="TEXT"):
        theme = self.get_theme()
        return theme.get(role, "#000000")
