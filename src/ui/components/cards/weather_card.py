import flet as ft
from ui.components.cards.adaptive_card import ResponsiveLayoutMixin
from utils.responsive_utils import ResponsiveHelper

class WeatherCard(ResponsiveLayoutMixin):
    """
    A responsive card displaying weather information that adapts to different devices.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_responsive(page)
        
    def build(self, content: ft.Control, card_type: str = "default") -> ft.Container:
        """
        Builds the weather card with responsive design based on device type.
        
        Args:
            content: Content of the card
            card_type: Type of card ("weather_info", "chart", "sidebar", "hourly")
            
        Returns:
            ft.Container: Responsive card configured for the device
        """
        if card_type == "weather_info":
            return self.adaptive_card.create_weather_info_card(content)
        elif card_type == "chart":
            return self.adaptive_card.create_chart_card(content)
        elif card_type == "sidebar":
            return self.adaptive_card.create_sidebar_card(content)
        elif card_type == "hourly":
            return self.adaptive_card.create_hourly_forecast_card(content)
        else:
            # Default responsive card
            return self.adaptive_card.create_weather_info_card(content)
    
    def build_with_title(self, content: ft.Control, title: str, card_type: str = "default") -> ft.Container:
        """
        Builds the weather card with a title.
        
        Args:
            content: Content of the card
            title: Title of the card
            card_type: Type of card
            
        Returns:
            ft.Container: Responsive card with title
        """
        if card_type == "chart":
            return self.adaptive_card.create_chart_card(content, title)
        else:
            return self.adaptive_card.create_weather_info_card(content, title)
    
    def _handle_responsive_resize(self, e):
        """Handle responsive resize events."""
        # Update card styling based on new device type
        if self.page:
            ResponsiveHelper.get_device_type(
                self.page.width if hasattr(self.page, 'width') and self.page.width else 1200
            )
            # Card will automatically adapt on next build() call
            self.page.update()
        
    def cleanup(self):
        """Cleanup method for removing event handlers."""
        pass
