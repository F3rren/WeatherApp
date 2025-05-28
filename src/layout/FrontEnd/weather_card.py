import flet as ft
from config import LIGHT_THEME, DARK_THEME

class WeatherCard:
    """
    A card displaying weather information.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.gradient = self._get_gradient()
    
    def _get_gradient(self) -> ft.LinearGradient:
        """Get the gradient based on the current theme"""
        if self.page.theme_mode == ft.ThemeMode.DARK:
            return ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE, ft.Colors.YELLOW]
            )
        else:
            return ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#1a1a1a", "#333333"],
            )
                
            
    
    def build(self, content: ft.Control) -> ft.Container:
        """Build the card with the provided content"""
        return ft.Container(
            gradient=self.gradient,
            border_radius=15,
            padding=20,
            content=content,
            expand=True,
        )
