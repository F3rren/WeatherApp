"""
Search Bar component for the MeteoApp sidebar.
Refactored to follow the robust sidebar pattern.
"""

import logging
import flet as ft
from typing import Callable, Optional, List
from utils.config import DEFAULT_LANGUAGE, DARK_THEME, LIGHT_THEME

# Configure logging
logger = logging.getLogger(__name__)

class SearchBar:
    """
    Search bar component with robust update pattern.
    Handles theme changes, language changes, and event management.
    """

    def __init__(
        self,
        page: ft.Page,
        text_color: dict,  # text_color is a dict e.g. {"TEXT": "#000000", ...}
        cities: List[str] = None,
        on_city_selected: Optional[Callable] = None,
        language: str = DEFAULT_LANGUAGE,
        prefix_widget: Optional[ft.Control] = None,
        suffix_widget: Optional[ft.Control] = None,
        text_handler_get_size: Optional[Callable] = None
    ):
        logger.info("Initializing SearchBar with robust pattern")
        
        # Core references
        self.page = page
        self.on_city_selected = on_city_selected
        self.text_handler_get_size = text_handler_get_size
        
        # Component state
        self.cities = cities or []
        self.text_color = text_color
        self.language = language
        self.prefix_widget = prefix_widget
        self.suffix_widget = suffix_widget
        self.focused = False
        
        # Component instances (will be recreated on updates)
        self.search_field = None
        self.container_instance = None
        
        # Initialize component
        self._initialize_component()
        
        # Register event handlers following sidebar pattern
        self._register_event_handlers()

    def _initialize_component(self) -> None:
        """Initialize the search bar component with current state."""
        logger.debug("Initializing SearchBar component")
        
        # Update current theme and language from page/state
        self._update_current_state()

    def _update_current_state(self) -> None:
        """Update current state from page and state manager."""
        try:
            # Update text color based on current theme
            self.text_color = (
                DARK_THEME if self.page.theme_mode == ft.ThemeMode.DARK 
                else LIGHT_THEME
            )
            
            # Update language from state manager if available
            state_manager = getattr(self.page, 'session', {}).get('state_manager')
            if state_manager:
                self.language = state_manager.get_state("language") or DEFAULT_LANGUAGE
                
            logger.debug(f"Updated SearchBar state: theme={'dark' if self.page.theme_mode == ft.ThemeMode.DARK else 'light'}, language={self.language}")
            
        except Exception as e:
            logger.warning(f"Error updating SearchBar state: {e}")

    def _register_event_handlers(self) -> None:
        """Register event handlers for theme and language changes."""
        try:
            state_manager = getattr(self.page, 'session', {}).get('state_manager')
            if state_manager:
                state_manager.register_observer("theme_event", self.handle_theme_change)
                state_manager.register_observer("language_event", self.handle_language_change)
                logger.debug("SearchBar event handlers registered")
            else:
                logger.warning("No state manager available for SearchBar event registration")
        except Exception as e:
            logger.warning(f"Error registering SearchBar event handlers: {e}")

    def handle_theme_change(self, event_data=None) -> None:
        """
        Handle theme change events following the sidebar pattern.
        
        Args:
            event_data: Theme change event data
        """
        logger.info("SearchBar handling theme change")
        
        try:
            # STEP 1: Update internal state
            self._update_current_state()
            
            # STEP 2: Rebuild component (LIKE SIDEBAR PATTERN)
            # Note: The container will be rebuilt when parent calls build()
            
            # STEP 3: Update container if it exists and is attached
            if self.container_instance:
                self._safe_container_update()
                
            logger.info("SearchBar theme change handled successfully")
            
        except Exception as e:
            logger.error(f"Error handling SearchBar theme change: {e}")

    def handle_language_change(self, event_data=None) -> None:
        """
        Handle language change events following the sidebar pattern.
        
        Args:
            event_data: Language change event data
        """
        logger.info("SearchBar handling language change")
        
        try:
            # STEP 1: Update internal state
            self._update_current_state()
            
            # STEP 2: Rebuild component (LIKE SIDEBAR PATTERN)
            # Note: The container will be rebuilt when parent calls build()
            
            # STEP 3: Update container if it exists and is attached
            if self.container_instance:
                self._safe_container_update()
                
            logger.info("SearchBar language change handled successfully")
            
        except Exception as e:
            logger.error(f"Error handling SearchBar language change: {e}")

    def _safe_container_update(self) -> bool:
        """
        Safely update the container following the sidebar pattern.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.container_instance:
            return False
            
        try:
            # Check if container is attached to page
            if hasattr(self.container_instance, 'page') and self.container_instance.page:
                self.container_instance.update()
                logger.debug("SearchBar container updated successfully")
                return True
            else:
                logger.debug("SearchBar container not attached to page, skipping update")
                return False
                
        except (AssertionError, AttributeError) as e:
            logger.debug(f"SearchBar container not ready for update: {e}")
            return False
        except Exception as e:
            logger.error(f"Error updating SearchBar container: {e}")
            return False

    def build(self, popmenu_widget=None, filter_widget=None, clear_icon_size=None) -> ft.Container:
        """
        Build the search bar component following the sidebar pattern.
        This method ALWAYS rebuilds the component with current state.
        
        Args:
            popmenu_widget: Optional popup menu widget
            filter_widget: Optional filter widget
            clear_icon_size: Optional clear icon size
            
        Returns:
            ft.Container: The built search bar container
        """
        logger.debug("Building SearchBar component")
        
        try:
            # STEP 1: Update current state (LIKE SIDEBAR PATTERN)
            self._update_current_state()
            
            # STEP 2: Create event handlers
            def on_submit(e):
                value = e.control.value.strip()
                logger.info(f"SearchBar submit: '{value}'")
                
                if value and self.on_city_selected:
                    logger.debug(f"Calling on_city_selected callback for city: {value}")
                    try:
                        if self.page:
                            self.page.run_task(self.on_city_selected, value)
                        else:
                            # Fallback for sync callbacks
                            self.on_city_selected(value)
                    except Exception as e:
                        logger.error(f"Error in on_city_selected callback: {e}")
                elif not value:
                    logger.debug("Empty search value, ignoring submit")
                else:
                    logger.warning("No on_city_selected callback defined")

            def clear_text(e):
                if self.search_field:
                    self.search_field.value = ""
                    try:
                        self.search_field.update()
                    except Exception as e:
                        logger.debug(f"Error updating search field after clear: {e}")

            # STEP 3: Create components with current state
            clear_btn = ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_size=self.text_handler_get_size('icon') if self.text_handler_get_size else 20,
                on_click=clear_text,
                tooltip="Clear",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
            )

            self.search_field = ft.TextField(
                text_style=ft.TextStyle(
                    size=self.text_handler_get_size('body') if self.text_handler_get_size else 14,
                    color=self.text_color.get("TEXT", "#000000")
                ),
                border_radius=24,
                bgcolor="transparent",
                border_color="transparent",
                content_padding=ft.padding.symmetric(horizontal=10, vertical=12),
                border=ft.InputBorder.NONE,
                on_submit=on_submit,
                expand=True,
                hint_text="Search for a city...",
                hint_style=ft.TextStyle(
                    color=self.text_color.get("SECONDARY_TEXT", "#666666"),
                    size=self.text_handler_get_size('body') if self.text_handler_get_size else 14
                )
            )

            # STEP 4: Build row with components
            row_children = []
            
            # Add popup menu if provided
            if popmenu_widget:
                row_children.append(
                    ft.Container(
                        content=popmenu_widget, 
                        margin=ft.margin.only(right=4)
                    )
                )

            # Add search field
            row_children.append(self.search_field)
            
            # Add clear button
            row_children.append(clear_btn)

            # Add filter widget if provided
            if filter_widget:
                row_children.append(
                    ft.Container(
                        content=filter_widget, 
                        margin=ft.margin.only(left=4)
                    )
                )

            row = ft.Row(
                row_children,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4
            )

            # STEP 5: Create container with theme-aware styling
            is_dark_theme = self.page.theme_mode == ft.ThemeMode.DARK
            
            container = ft.Container(
                content=row,
                border_radius=32,
                bgcolor="#fafbfc" if not is_dark_theme else "#2c2f33",
                border=ft.border.all(1, "#e0e0e0" if not is_dark_theme else "#3c3f43"),
                shadow=ft.BoxShadow(blur_radius=4, color="#00000010"),
                padding=ft.padding.symmetric(horizontal=12, vertical=2),
                animate=ft.Animation(200, "decelerate"),
            )

            # STEP 6: Setup focus handlers
            def on_focus_handler(e):
                self.focused = True
                if container:
                    container.bgcolor = "#ffffff" if not is_dark_theme else "#33373b"
                    container.shadow = ft.BoxShadow(blur_radius=16, color="#1976d230")
                    try:
                        container.update()
                    except Exception as e:
                        logger.debug(f"Error updating container on focus: {e}")

            def on_blur_handler(e):
                self.focused = False
                if container:
                    container.bgcolor = "#fafbfc" if not is_dark_theme else "#2c2f33"
                    container.shadow = ft.BoxShadow(blur_radius=4, color="#00000010")
                    try:
                        container.update()
                    except Exception as e:
                        logger.debug(f"Error updating container on blur: {e}")

            container.on_focus = on_focus_handler
            container.on_blur = on_blur_handler

            # STEP 7: Store reference and return (LIKE SIDEBAR PATTERN)
            self.container_instance = container
            
            logger.debug("SearchBar component built successfully")
            return container
            
        except Exception as e:
            logger.error(f"Error building SearchBar component: {e}")
            # Return a fallback container
            return ft.Container(
                content=ft.Text(
                    "Search unavailable",
                    color=ft.colors.RED,
                    size=12
                ),
                padding=ft.padding.all(10)
            )

    def update_cities(self, new_cities: List[str]) -> bool:
        """
        Update the cities list following the sidebar pattern.
        
        Args:
            new_cities: New list of cities
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug(f"Updating SearchBar cities: {len(new_cities)} cities")
        
        try:
            self.cities = new_cities or []
            
            # If we have a container instance, rebuild it to reflect the new cities
            # Note: Cities list is not directly displayed but could affect autocomplete
            logger.info(f"SearchBar cities updated successfully: {len(self.cities)} cities")
            return True
            
        except Exception as e:
            logger.error(f"Error updating SearchBar cities: {e}")
            return False

    def get_selected_value(self) -> str:
        """
        Get the current value in the search field.
        
        Returns:
            str: Current search field value
        """
        try:
            if hasattr(self, 'search_field') and self.search_field:
                return self.search_field.value or ""
            return ""
        except Exception as e:
            logger.debug(f"Error getting SearchBar selected value: {e}")
            return ""

    def clear_selection(self) -> bool:
        """
        Clear the search field following the sidebar pattern.
        
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug("Clearing SearchBar selection")
        
        try:
            if hasattr(self, 'search_field') and self.search_field:
                self.search_field.value = ""
                # Try to update the field
                try:
                    self.search_field.update()
                except (AssertionError, AttributeError) as e:
                    logger.debug(f"Search field not ready for update: {e}")
                
                logger.debug("SearchBar selection cleared successfully")
                return True
            else:
                logger.debug("No search field available to clear")
                return False
                
        except Exception as e:
            logger.error(f"Error clearing SearchBar selection: {e}")
            return False

    def cleanup(self) -> None:
        """
        Cleanup the SearchBar component following the sidebar pattern.
        Unregister event handlers to prevent memory leaks.
        """
        logger.info("Cleaning up SearchBar component")
        
        try:
            # Unregister event handlers
            state_manager = getattr(self.page, 'session', {}).get('state_manager')
            if state_manager:
                state_manager.unregister_observer("theme_event", self.handle_theme_change)
                state_manager.unregister_observer("language_event", self.handle_language_change)
                logger.debug("SearchBar event handlers unregistered")
            
            # Clear references
            self.search_field = None
            self.container_instance = None
            self.on_city_selected = None
            
            logger.info("SearchBar cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Error during SearchBar cleanup: {e}")

    def update_language(self, new_language: str) -> bool:
        """
        Update language and refresh component following the sidebar pattern.
        
        Args:
            new_language: New language code
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Updating SearchBar language to: {new_language}")
        
        try:
            self.language = new_language
            
            # Trigger rebuild by updating state and container
            self._update_current_state()
            if self.container_instance:
                self._safe_container_update()
                
            logger.info(f"SearchBar language updated successfully to: {new_language}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating SearchBar language: {e}")
            return False

    def update_theme(self, text_color: dict) -> bool:
        """
        Update theme and refresh component following the sidebar pattern.
        
        Args:
            text_color: New text color dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info("Updating SearchBar theme")
        
        try:
            self.text_color = text_color
            
            # Trigger rebuild by updating state and container
            self._update_current_state()
            if self.container_instance:
                self._safe_container_update()
                
            logger.info("SearchBar theme updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error updating SearchBar theme: {e}")
            return False
