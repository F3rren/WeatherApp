import flet as ft
import logging
from utils.config import UNIT_SYSTEMS
from services.translation_service import TranslationService

class DropdownMeasurement:

    def __init__(self, page: ft.Page, state_manager, text_color: dict, language: str):
        self.page = page
        self.state_manager = state_manager
        self.text_color = text_color
        self.current_language_display = language # Used for translating options
        
        self.selected_unit = None # This will be set from state_manager or during selection
        self.dropdown = None
        self.units = UNIT_SYSTEMS
        self.unit_name_keys = {code: details["name_key"] for code, details in UNIT_SYSTEMS.items()}

    def update_text_sizes(self, text_color: dict, language: str):
        """Update text sizes, colors, and translated text for the dropdown."""
        self.text_color = text_color
        self.current_language_display = language # Update current language for translations

        # If dropdown exists, update it
        if self.dropdown:
            # Save current unit code (e.g. "metric", "imperial")
            current_unit_code = self.dropdown.value
            
            # Update dropdown styling
            self.dropdown.color = self.text_color["TEXT"]
            self.dropdown.border_color = self.text_color["BORDER"]
            self.dropdown.focused_border_color = self.text_color["ACCENT"]
            self.dropdown.bgcolor = self.text_color["CARD_BACKGROUND"]
            
            # Update hint text with translation
            translated_hint_text = TranslationService.translate_from_dict("unit_items", "measurement", self.current_language_display)
            self.dropdown.hint_text = translated_hint_text
            
            # Update dropdown options with new translations
            self.dropdown.options = self.get_options()
            
            # Re-select the current value to force option text update
            self.dropdown.value = current_unit_code
            
            # Update styles
            if self.dropdown.hint_style:
                self.dropdown.hint_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else:
                self.dropdown.hint_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            
            if self.dropdown.label_style:
                self.dropdown.label_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else:
                self.dropdown.label_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            
            # Force UI update
            self.dropdown.update()
            if self.page:
                self.page.update()

    def get_options(self):
        """Get translated dropdown options based on the current language."""
        # Defensive: ensure self.text_color is a dict, not a string
        if isinstance(self.text_color, str):
            from utils.config import DARK_THEME, LIGHT_THEME
            if self.text_color.lower() in ("#fff", "#ffffff", "white"):
                self.text_color = LIGHT_THEME
            else:
                self.text_color = DARK_THEME
        options = []
        for unit_system_code, name_key in self.unit_name_keys.items():
            translated_name = TranslationService.translate_from_dict("unit_items", name_key, self.current_language_display)
            options.append(
                ft.dropdown.Option(
                    key=unit_system_code,
                    text=translated_name,
                    content=ft.Text(
                        value=translated_name,
                        color=self.text_color["TEXT"]
                    ),
                )
            )
        return options
    
    def createDropdown(self):
        """Create a new dropdown with the current settings."""
        # Always set self.text_color based on current theme
        from utils.config import DARK_THEME, LIGHT_THEME
        if self.page and hasattr(self.page, 'theme_mode'):
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            self.text_color = DARK_THEME if is_dark else LIGHT_THEME
        elif isinstance(self.text_color, str):
            if self.text_color.lower() in ("#fff", "#ffffff", "white"):
                self.text_color = LIGHT_THEME
            else:
                self.text_color = DARK_THEME
        
        def dropdown_changed(e):
            unit_code = e.control.value
            logging.info(f"Selected unit: {unit_code}")
            self.set_unit(unit_code)
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        # Get current unit from state manager or default to metric
        current_unit = "metric"
        if self.state_manager:
            current_unit = self.state_manager.get_state('unit') or "metric"
            self.selected_unit = current_unit
        
        # Get translated text for the dropdown hint
        translated_hint_text = TranslationService.translate_from_dict("unit_items", "measurement", self.current_language_display)

        # Create the dropdown with translated options
        self.dropdown = ft.Dropdown(
            hint_text=translated_hint_text,
            options=self.get_options(),
            on_change=dropdown_changed,
            width=200,
            value=current_unit,
            border_width=2,
            border_color=self.text_color["BORDER"],
            focused_border_color=self.text_color["ACCENT"],
            focused_border_width=2,
            bgcolor=self.text_color["CARD_BACKGROUND"],
            color=self.text_color["TEXT"],
            content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
            hint_style=ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
        )
        return self.dropdown
    
    def set_unit(self, unit_code):
        """Set the selected unit and update application state."""
        self.selected_unit = unit_code
        logging.info(f"DropdownMeasurement: selected_unit updated to {unit_code}")
        
        # Update application state if state_manager is available
        if self.state_manager and self.page:
            logging.info(f"DropdownMeasurement: Queuing state update for unit: {unit_code} via page.run_task")
            
            # First send a unit_text_change event to allow UI to update texts
            # without refetching data or complete reconstruction
            import asyncio
            
            def call_async_safely(coro):
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                if not loop.is_running():
                    return loop.run_until_complete(coro)
                else:
                    return asyncio.create_task(coro)
            
            # First notify for updating text only (without complete reconstruction)
            call_async_safely(self.state_manager.notify_all("unit_text_change", {"unit": unit_code}))
            
            # Then update state which may cause data refetch
            self.page.run_task(self.state_manager.set_state, "unit", unit_code)
        elif not self.page:
            logging.warning("DropdownMeasurement: self.page is not available, cannot run task for set_state.")
        elif not self.state_manager:
            logging.warning("DropdownMeasurement: self.state_manager is not available, cannot set state.")

    def handle_theme_change(self, event_data=None):
        """Handle theme change events by updating the dropdown appearance."""
        if self.dropdown:
            # Update styles and colors
            self.dropdown.border_color = self.text_color.get("BORDER", ft.Colors.BLACK)
            self.dropdown.focused_border_color = self.text_color.get("ACCENT", ft.Colors.BLUE)
            self.dropdown.bgcolor = self.text_color.get("CARD_BACKGROUND", ft.Colors.WHITE)
            self.dropdown.color = self.text_color.get("TEXT", ft.Colors.BLACK)
            
            # Update translations
            translated_hint_text = TranslationService.translate_from_dict("unit_items", "measurement", self.current_language_display)
            self.dropdown.hint_text = translated_hint_text

            # Update styles
            if self.dropdown.hint_style:
                self.dropdown.hint_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else:
                self.dropdown.hint_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            
            # Re-generate options with new language/theme
            current_value = self.dropdown.value  # Save current selection
            self.dropdown.options = self.get_options()  # Update options with translations
            self.dropdown.value = current_value  # Restore selection
            
            # Force UI update
            self.dropdown.update()
            
    def get_selected_unit(self):
        """Get the currently selected unit."""
        return self.selected_unit
        
    def build(self):
        """Build and return the dropdown widget."""
        if not self.dropdown: # Create dropdown only if it doesn't exist
            self.dropdown = self.createDropdown()
        return self.dropdown
        
    def on_language_change(self, new_language_code):
        """Handle language change event by updating translations."""
        self.current_language_display = new_language_code
        
        # Get the current selected value before updating
        current_unit_code = self.dropdown.value if self.dropdown else None
        
        if self.dropdown:
            # The most reliable way to force Flet to update the displayed text is to recreate the dropdown
            # Store parent container
            parent_container = self.dropdown.parent
            old_dropdown = self.dropdown
            
            # Create a new dropdown with updated language
            self.dropdown = None
            new_dropdown = self.createDropdown()
            
            # Make sure the same value is selected
            if current_unit_code:
                new_dropdown.value = current_unit_code
            
            # Replace old dropdown in parent container if possible
            if parent_container and hasattr(parent_container, "controls"):
                try:
                    for i, control in enumerate(parent_container.controls):
                        if control == old_dropdown:
                            parent_container.controls[i] = new_dropdown
                            parent_container.update()
                            break
                except Exception as e:
                    logging.error(f"Error replacing dropdown: {e}")
                    # If failed, restore old dropdown and try simpler update
                    self.dropdown = old_dropdown
                    
            else:
                # If no parent or controls, fallback to simpler update
                self.dropdown = old_dropdown
                
        else:
            # If dropdown doesn't exist yet, just update settings
            pass