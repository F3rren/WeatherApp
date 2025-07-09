"""
PopMenu component for the MeteoApp sidebar.
Refactored to follow the robust sidebar pattern.
"""

import logging
import flet as ft
from typing import Callable, Optional

from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME
from layout.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from layout.sidebar.popmenu.alertdialogs.maps.maps_alert_dialog import MapsAlertDialog
from layout.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog

# Configure logging
logger = logging.getLogger(__name__)


class PopMenu(ft.Container):
    """
    PopMenu component with robust update pattern.
    Handles theme changes, language changes, and event management.
    """

    def __init__(self, 
                 page: ft.Page = None, 
                 state_manager=None, 
                 handle_location_toggle: Optional[Callable] = None, 
                 handle_theme_toggle: Optional[Callable] = None, 
                 theme_toggle_value: bool = False, 
                 location_toggle_value: bool = False, 
                 text_color: dict = None, 
                 language: str = None, 
                 text_handler_get_size: Optional[Callable] = None, 
                 **kwargs):
        super().__init__(**kwargs)
        
        logger.info("Initializing PopMenu with robust pattern")
        
        # Core references
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.text_handler_get_size = text_handler_get_size
        
        # Component state
        self.theme_toggle_value = theme_toggle_value
        self.location_toggle_value = location_toggle_value
        self.text_color = text_color if text_color else self._determine_text_color_from_theme()
        self.language = language if language else DEFAULT_LANGUAGE
        
        # Component instances (will be recreated on updates)
        self.weather_alert = None
        self.map_alert = None
        self.setting_alert = None
        self.pop_menu_items = None
        self.popup_menu_button_control = None
        
        # Initialize component
        self._initialize_component()
        
        # Register event handlers following sidebar pattern
        self._register_event_handlers()
        
        # Build initial content
        self.content = self.build()

    def _initialize_component(self) -> None:
        """Initialize the PopMenu component with current state."""
        logger.debug("Initializing PopMenu component")
        
        # Update current theme and language from page/state
        self._update_current_state()

    def _update_current_state(self) -> None:
        """Update current state from page and state manager."""
        try:
            # Update text color based on current theme
            self.text_color = self._determine_text_color_from_theme()
            
            # Update language from state manager if available
            if self.state_manager:
                self.language = self.state_manager.get_state("language") or DEFAULT_LANGUAGE
                self.theme_toggle_value = self.page.theme_mode == ft.ThemeMode.DARK if self.page else False
                self.location_toggle_value = self.state_manager.get_state("using_location") or False
                
            logger.debug(f"Updated PopMenu state: theme={'dark' if self.page and self.page.theme_mode == ft.ThemeMode.DARK else 'light'}, language={self.language}")
            
        except Exception as e:
            logger.warning(f"Error updating PopMenu state: {e}")

    def _determine_text_color_from_theme(self) -> dict:
        """
        Determine text color from current theme.
        
        Returns:
            dict: Theme color dictionary
        """
        try:
            if self.page and self.page.theme_mode:
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
                return DARK_THEME if is_dark else LIGHT_THEME
            else:
                return LIGHT_THEME
        except Exception as e:
            logger.warning(f"Error determining theme color: {e}")
            return LIGHT_THEME

    def _register_event_handlers(self) -> None:
        """Register event handlers for theme and language changes."""
        try:
            if self.state_manager:
                self.state_manager.register_observer("theme_event", self.handle_theme_change)
                self.state_manager.register_observer("language_event", self.handle_language_change)
                logger.debug("PopMenu event handlers registered")
            else:
                logger.warning("No state manager available for PopMenu event registration")
        except Exception as e:
            logger.warning(f"Error registering PopMenu event handlers: {e}")

    def handle_theme_change(self, event_data=None) -> None:
        """
        Handle theme change events following the sidebar pattern.
        
        Args:
            event_data: Theme change event data
        """
        logger.info("PopMenu handling theme change")
        
        try:
            # STEP 1: Update internal state
            self._update_current_state()
            
            # STEP 2: Update child components
            self._update_child_components()
            
            # STEP 3: Rebuild component (LIKE SIDEBAR PATTERN)
            self.content = self.build()
            
            # STEP 4: Update container if attached to page
            if self._safe_container_update():
                logger.info("PopMenu theme change handled successfully")
            else:
                logger.debug("PopMenu not ready for update after theme change")
                
        except Exception as e:
            logger.error(f"Error handling PopMenu theme change: {e}")

    def handle_language_change(self, event_data=None) -> None:
        """
        Handle language change events following the sidebar pattern.
        
        Args:
            event_data: Language change event data
        """
        logger.info("PopMenu handling language change")
        
        try:
            # STEP 1: Update internal state
            self._update_current_state()
            
            # STEP 2: Update child components
            self._update_child_components()
            
            # STEP 3: Rebuild component (LIKE SIDEBAR PATTERN)
            self.content = self.build()
            
            # STEP 4: Update container if attached to page
            if self._safe_container_update():
                logger.info("PopMenu language change handled successfully")
            else:
                logger.debug("PopMenu not ready for update after language change")
                
        except Exception as e:
            logger.error(f"Error handling PopMenu language change: {e}")

    def _safe_container_update(self) -> bool:
        """
        Safely update the container following the sidebar pattern.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if container is attached to page
            if hasattr(self, 'page') and self.page:
                self.update()
                logger.debug("PopMenu container updated successfully")
                return True
            else:
                logger.debug("PopMenu container not attached to page, skipping update")
                return False
                
        except (AssertionError, AttributeError) as e:
            logger.debug(f"PopMenu container not ready for update: {e}")
            return False
        except Exception as e:
            logger.error(f"Error updating PopMenu container: {e}")
            return False

    def _update_child_components(self) -> None:
        """Update child dialog components with current state."""
        logger.debug("Updating PopMenu child components")
        
        try:
            # Update child dialogs with current state
            self.weather_alert = WeatherAlertDialog(
                page=self.page, 
                state_manager=self.state_manager, 
                text_color=self.text_color, 
                language=self.language
            )
            
            self.map_alert = MapsAlertDialog(
                page=self.page, 
                state_manager=self.state_manager
            )
            
            self.setting_alert = SettingsAlertDialog(
                page=self.page, 
                state_manager=self.state_manager, 
                handle_location_toggle=self.handle_location_toggle, 
                handle_theme_toggle=self.handle_theme_toggle, 
                text_color=self.text_color, 
                language=self.language
            )
            
            # Update popup menu items with current translations
            self.pop_menu_items = {
                "weather": ft.Text(
                    value=TranslationService.translate_from_dict("popup_menu_items", "weather", self.language), 
                    color=self.text_color.get("TEXT", "#000000")
                ),
                "map": ft.Text(
                    value=TranslationService.translate_from_dict("popup_menu_items", "map", self.language), 
                    color=self.text_color.get("TEXT", "#000000")
                ),
                "settings": ft.Text(
                    value=TranslationService.translate_from_dict("popup_menu_items", "settings", self.language), 
                    color=self.text_color.get("TEXT", "#000000")
                )
            }
            
            logger.debug("PopMenu child components updated successfully")
            
        except Exception as e:
            logger.error(f"Error updating PopMenu child components: {e}")

    # For backward compatibility with old method name
    def update_ui(self, event_data=None):
        """
        Legacy method for backward compatibility.
        Redirects to proper event handlers.
        """
        logger.debug("PopMenu update_ui called (legacy method)")
        
        # Determine what kind of update this is and call appropriate handler
        if hasattr(event_data, 'get') and event_data.get('type') == 'theme':
            self.handle_theme_change(event_data)
        elif hasattr(event_data, 'get') and event_data.get('type') == 'language':
            self.handle_language_change(event_data)
        else:
            # Default: update both theme and language
            self._update_current_state()
            self._update_child_components()
            self.content = self.build()
            self._safe_container_update()

    def build(self) -> ft.PopupMenuButton:
        """
        Build the PopMenu component following the sidebar pattern.
        This method ALWAYS rebuilds the component with current state.
        
        Returns:
            ft.PopupMenuButton: The built popup menu button
        """
        logger.debug("Building PopMenu component")
        
        try:
            # STEP 1: Update current state (LIKE SIDEBAR PATTERN)
            self._update_current_state()
            
            # STEP 2: Update child components
            self._update_child_components()
            
            # STEP 3: Create popup menu items with current state
            def build_popup_menu_items():
                try:
                    return [
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(
                                    ft.Icons.SUNNY, 
                                    color="#FF8C00", 
                                    size=self.text_handler_get_size('popup_menu_button_icon') if self.text_handler_get_size else 20
                                ),
                                self.pop_menu_items["weather"]
                            ], spacing=8),
                            on_click=lambda _: self._safe_open_dialog(self.weather_alert)
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(
                                    ft.Icons.MAP_OUTLINED, 
                                    color="#0000FF", 
                                    size=self.text_handler_get_size('popup_menu_button_icon') if self.text_handler_get_size else 20
                                ),
                                self.pop_menu_items["map"]
                            ], spacing=8),
                            on_click=lambda _: self._safe_open_dialog(self.map_alert)
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row([
                                ft.Icon(
                                    ft.Icons.SETTINGS, 
                                    color="#808080", 
                                    size=self.text_handler_get_size('popup_menu_button_icon') if self.text_handler_get_size else 20
                                ),
                                self.pop_menu_items["settings"]
                            ], spacing=8),
                            on_click=lambda _: self._safe_open_dialog(self.setting_alert)
                        ),
                    ]
                except Exception as e:
                    logger.error(f"Error building popup menu items: {e}")
                    return []
            
            # STEP 4: Create popup menu button with current state
            popup_button = ft.PopupMenuButton(
                content=ft.Icon(
                    ft.Icons.MENU, 
                    color=self.text_color.get("TEXT", "#000000"), 
                    size=self.text_handler_get_size('icon') if self.text_handler_get_size else 24
                ),
                items=build_popup_menu_items(),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                tooltip="Menu"
            )
            
            # STEP 5: Store reference and update content (LIKE SIDEBAR PATTERN)
            self.popup_menu_button_control = popup_button
            self.content = popup_button  # Update container content
            
            logger.debug("PopMenu component built successfully")
            return popup_button
            
        except Exception as e:
            logger.error(f"Error building PopMenu component: {e}")
            # Return a fallback button
            fallback_button = ft.IconButton(
                icon=ft.icons.ERROR,
                tooltip="Menu unavailable",
                on_click=lambda _: logger.warning("PopMenu not available")
            )
            self.content = fallback_button
            return fallback_button

    def _safe_open_dialog(self, dialog_instance) -> None:
        """
        Safely open a dialog following the sidebar pattern.
        
        Args:
            dialog_instance: Dialog instance to open
        """
        try:
            if dialog_instance and hasattr(dialog_instance, 'open_dialog'):
                dialog_instance.open_dialog()
                logger.debug(f"Dialog opened: {dialog_instance.__class__.__name__}")
            else:
                logger.warning(f"Dialog not available: {dialog_instance}")
        except Exception as e:
            logger.error(f"Error opening dialog: {e}")

    def update_theme(self, text_color: dict) -> bool:
        """
        Update theme and refresh component following the sidebar pattern.
        
        Args:
            text_color: New text color dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info("Updating PopMenu theme")
        
        try:
            self.text_color = text_color
            
            # Trigger rebuild by updating state and content
            self._update_current_state()
            self._update_child_components()
            self.content = self.build()
            
            # Update container if attached to page
            success = self._safe_container_update()
            
            if success:
                logger.info("PopMenu theme updated successfully")
            else:
                logger.debug("PopMenu theme updated but container not ready")
                
            return success
            
        except Exception as e:
            logger.error(f"Error updating PopMenu theme: {e}")
            return False

    def update_language(self, new_language: str) -> bool:
        """
        Update language and refresh component following the sidebar pattern.
        
        Args:
            new_language: New language code
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Updating PopMenu language to: {new_language}")
        
        try:
            self.language = new_language
            
            # Trigger rebuild by updating state and content
            self._update_current_state()
            self._update_child_components()
            self.content = self.build()
            
            # Update container if attached to page
            success = self._safe_container_update()
            
            if success:
                logger.info(f"PopMenu language updated successfully to: {new_language}")
            else:
                logger.debug("PopMenu language updated but container not ready")
                
            return success
            
        except Exception as e:
            logger.error(f"Error updating PopMenu language: {e}")
            return False

    def cleanup(self) -> None:
        """
        Cleanup the PopMenu component following the sidebar pattern.
        Unregister event handlers and cleanup child components.
        """
        logger.info("Cleaning up PopMenu component")
        
        try:
            # Unregister event handlers
            if self.state_manager:
                self.state_manager.unregister_observer("theme_event", self.handle_theme_change)
                self.state_manager.unregister_observer("language_event", self.handle_language_change)
                logger.debug("PopMenu event handlers unregistered")
            
            # Cleanup child components
            if self.weather_alert and hasattr(self.weather_alert, 'cleanup'):
                self.weather_alert.cleanup()
            
            if self.map_alert and hasattr(self.map_alert, 'cleanup'):
                self.map_alert.cleanup()
            
            if self.setting_alert and hasattr(self.setting_alert, 'cleanup'):
                self.setting_alert.cleanup()
            
            # Clear references
            self.weather_alert = None
            self.map_alert = None
            self.setting_alert = None
            self.pop_menu_items = None
            self.popup_menu_button_control = None
            
            logger.info("PopMenu cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Error during PopMenu cleanup: {e}")
