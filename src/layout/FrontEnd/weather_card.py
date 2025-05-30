import flet as ft

class WeatherCard:
    """
    A card displaying weather information.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        # Remove gradient - background will be managed by the main containers in app.py
    
    def build(self, content: ft.Control) -> ft.Container:
        """Builds the weather card with the given content."""
        return ft.Container(
            content=content,
            border_radius=15,
            padding=10, # Reduced padding as inner components might have their own
            margin=0, # LayoutManager handles margin for the main containers
            expand=True # Ensure the card itself expands
        )
