import flet as ft
from components.responsive_text_handler import ResponsiveTextHandler

class WeatherCard:
    """
    A card displaying weather information.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        # Remove gradient - background will be managed by the main containers in app.py
        
        # Initialize ResponsiveTextHandler
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'card_title': 18,    # Titolo della card
                'card_text': 14,     # Testo normale nella card
                'card_small': 12,    # Testo piccolo nella card
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Dictionary to track text controls
        self.text_controls = {}
        
        # Register as observer for responsive updates
        self.text_handler.add_observer(self.update_text_controls)
        
    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        for control, size_category in self.text_controls.items():
            if hasattr(control, 'size'):
                control.size = self.text_handler.get_size(size_category)
        
        # Request page update
        if self.page:
            self.page.update()
    
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
        """Cleanup method to remove observers"""
        if hasattr(self, 'text_handler') and self.text_handler:
            self.text_handler.remove_observer(self.update_text_controls)
