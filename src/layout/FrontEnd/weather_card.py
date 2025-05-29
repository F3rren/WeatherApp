import flet as ft

class WeatherCard:
    """
    A card displaying weather information.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        # Remove gradient - background will be managed by the main containers in app.py
    
    def build(self, content: ft.Control) -> ft.Container:
        """Build the card with the provided content"""
        return ft.Container(
            # Remove gradient property - let the main container handle background color
            border_radius=15,
            padding=20,
            content=content,
            expand=True,
        )
