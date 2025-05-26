import flet as ft

class WeatherCard:
    """
    A card displaying weather information.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.gradient = self._get_gradient()
    
    def _get_gradient(self) -> ft.LinearGradient:
        """Get gradient based on theme mode"""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            return ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.BLUE, ft.Colors.YELLOW],
            )
        else:
            return ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
                    ft.Colors.GREY_900,
                ],
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
