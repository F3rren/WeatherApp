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
    and providing theme utilities for components.
    """
    
    def __init__(self, page: ft.Page):
        """
        Initialize the theme handler.
        
        Args:
            page: The Flet page reference
        """
        self.page = page
        self._observers = set()  # Optionally, for future observer pattern

    def get_theme(self):
        theme_mode = self.page.theme_mode if self.page else ft.ThemeMode.LIGHT
        return LIGHT_THEME if theme_mode == ft.ThemeMode.LIGHT else DARK_THEME

    def get_text_color(self, role: str = None):
        theme = self.get_theme()
        # Espandi la logica per ruoli diversi
        if role == "SECONDARY_TEXT":
            return theme.get("SECONDARY_TEXT", ft.Colors.GREY_700)
        # Puoi aggiungere altri ruoli qui se necessario
        return theme.get("TEXT", ft.Colors.BLACK)

    def get_background_color(self, role: str = None):
        theme = self.get_theme()
        if role == 'info':
            main_info_config = theme.get("MAIN_INFO_BACKGROUND", LIGHT_THEME.get("MAIN_INFO_BACKGROUND"))
            return main_info_config.get("color", "#37acbb")
        return theme.get("CARD_BACKGROUND", "#ffffff")

    def get_gradient(self, role: str = None):
        theme = self.get_theme()
        if role == 'info':
            main_info_config = theme.get("MAIN_INFO_BACKGROUND", LIGHT_THEME.get("MAIN_INFO_BACKGROUND"))
            gradient_info = main_info_config.get("gradient")
            if gradient_info:
                return ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=gradient_info["colors"],
                    stops=[gradient_info["start"], gradient_info["end"]]
                )
        return None

    def apply_theme(self, component, role: str = None):
        """
        Apply theme (background, gradient, text color) to a component based on its role.
        """
        if hasattr(component, 'bgcolor'):
            component.bgcolor = self.get_background_color(role)
        if hasattr(component, 'gradient'):
            component.gradient = self.get_gradient(role)
        if hasattr(component, 'color'):
            component.color = self.get_text_color(role)
        if hasattr(component, 'update'):
            try:
                component.update()
            except Exception:
                pass

    async def update_container_colors(self, containers: Dict[str, ft.Container], event_data: Optional[Any] = None) -> None:
        """
        Updates the background colors of main containers based on the theme.
        
        Args:
            containers: Dictionary of containers to update with their IDs as keys
            event_data: Optional event data from theme change event
        """
        if not self.page:
            return
            
        theme = self.get_theme()
        card_bg_color = theme.get("CARD_BACKGROUND", "#ffffff" if theme == LIGHT_THEME else "#262626")
        
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
                # Only update if the container is attached to the page
                if getattr(container, 'page', None):
                    container.update()
        
        # Update page background
        self.page.bgcolor = theme.get("BACKGROUND", "#f5f5f5" if theme == LIGHT_THEME else "#1a1a1a")
        self.page.update()
