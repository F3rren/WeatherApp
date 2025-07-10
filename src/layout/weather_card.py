import flet as ft

class WeatherCard:
    """
    A card displaying weather information.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    # update_text_controls removed (no longer needed)
    
    def build(self, content: ft.Control) -> ft.Container:
        """Builds the weather card with the given content."""
        return ft.Container(
            content=content,
            border_radius=15,
            padding=10, # Reduced padding as inner components might have their own
            margin=0, # LayoutManager handles margin for the main containers
            expand=True # Ensure the card itself expands
        )
        
    def cleanup(self):
        """Cleanup method (no observers to remove)"""
        pass
