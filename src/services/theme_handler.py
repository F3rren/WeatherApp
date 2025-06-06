"""
Theme Handler for MeteoApp.
Centralizes theme management and container color updating based on theme changes.
"""

import flet as ft
from typing import Dict, Optional, Any

from utils.config import LIGHT_THEME, DARK_THEME

class ThemeHandler:
    """
    Handles theme-related operations including updating container colors
    based on theme changes.
    """
    
    def __init__(self, page: ft.Page):
        """
        Initialize the theme handler.
        
        Args:
            page: The Flet page reference
        """
        self.page = page
        
    async def update_container_colors(self, containers: Dict[str, ft.Container], event_data: Optional[Any] = None) -> None:
        """
        Updates the background colors of main containers based on the theme.
        
        Args:
            containers: Dictionary of containers to update with their IDs as keys
            event_data: Optional event data from theme change event
        """
        if not self.page:
            return
            
        theme_mode = self.page.theme_mode
        theme = LIGHT_THEME if theme_mode == ft.ThemeMode.LIGHT else DARK_THEME
        card_bg_color = theme.get("CARD_BACKGROUND", "#ffffff" if theme_mode == ft.ThemeMode.LIGHT else "#262626")
        
        for container_name, container in containers.items():
            if container:
                # Configure gradient for main info container only
                if container_name == 'info':
                    main_info_config = theme.get("MAIN_INFO_BACKGROUND", LIGHT_THEME.get("MAIN_INFO_BACKGROUND"))
                    gradient_info = main_info_config.get("gradient")
                    if gradient_info:
                        container.gradient = ft.LinearGradient(
                            begin=ft.alignment.top_center,
                            end=ft.alignment.bottom_center,
                            colors=gradient_info["colors"],
                            stops=[gradient_info["start"], gradient_info["end"]]
                        )
                        container.opacity = main_info_config.get("opacity", 1.0)
                        container.bgcolor = None
                    else:
                        container.bgcolor = main_info_config.get("color", "#37acbb")
                        container.opacity = main_info_config.get("opacity", 1.0)
                else:
                    container.gradient = None
                    container.bgcolor = card_bg_color
                container.update()
        
        # Update page background
        self.page.bgcolor = theme.get("BACKGROUND", "#f5f5f5" if theme_mode == ft.ThemeMode.LIGHT else "#1a1a1a")
        self.page.update()
