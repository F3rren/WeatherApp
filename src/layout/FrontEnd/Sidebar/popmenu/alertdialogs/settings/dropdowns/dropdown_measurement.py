import flet as ft
import logging
from utils.config import UNIT_SYSTEMS
from services.translation_service import TranslationService

class DropdownMeasurement:

    def __init__(self, page: ft.Page, state_manager, text_color: dict, language: str, text_handler_get_size):
        self.page = page
        self.state_manager = state_manager
        self.text_color = text_color
        self.current_language_display = language # Used for translating options
        self.text_handler_get_size = text_handler_get_size
        
        self.selected_unit = None # This will be set from state_manager or during selection
        self.dropdown = None
        self.units = UNIT_SYSTEMS
        self.unit_name_keys = {code: details["name_key"] for code, details in UNIT_SYSTEMS.items()}

    def update_text_sizes(self, text_handler_get_size, text_color: dict, language: str):
        """Update text sizes, colors, and translated text for the dropdown."""
        self.text_handler_get_size = text_handler_get_size
        self.text_color = text_color
        self.current_language_display = language # Update current language for translations

        if self.dropdown:
            self.dropdown.text_size = self.text_handler_get_size('dropdown_text')
            self.dropdown.color = self.text_color["TEXT"]
            self.dropdown.border_color = self.text_color["BORDER"]
            self.dropdown.focused_border_color = self.text_color["ACCENT"]
            self.dropdown.bgcolor = self.text_color["CARD_BACKGROUND"]

            translated_hint_text = TranslationService.get_text("select_measurement_hint", self.current_language_display)
            self.dropdown.hint_text = translated_hint_text

            if self.dropdown.hint_style:
                self.dropdown.hint_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else:
                self.dropdown.hint_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            
            if self.dropdown.label_style: # Though label is not used
                self.dropdown.label_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else: # Though label is not used
                self.dropdown.label_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))

            # Re-generate options to update their translated text and style
            self.dropdown.options = self.get_options()
            if self.dropdown.page:
                self.dropdown.update()
                if self.page:
                    self.page.update()

    def get_options(self):
        # Uses self.current_language_display and self.text_color for styling options
        options = []
        for unit_system_code, name_key in self.unit_name_keys.items():
            translated_name = TranslationService.get_text(name_key, self.current_language_display)
            options.append(
                ft.dropdown.Option(
                    key=unit_system_code,
                    text=translated_name, 
                    content=ft.Text(
                        value=translated_name,
                        color=self.text_color["TEXT"] # Apply current text color to options
                    ),
                )
            )
        return options
    
    def createDropdown(self):
        # current_language is now self.current_language_display, set in __init__ and update_text_sizes
        
        def dropdown_changed(e):
            unit_code = e.control.value
            print(f"Selected unit: {unit_code}")
            self.set_unit(unit_code) # Call set_unit to handle selection and state update
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        current_unit = "metric"
        if self.state_manager:
            current_unit = self.state_manager.get_state('unit') or "metric"
            self.selected_unit = current_unit

        # Use the passed-in text_color (theme) and text_handler_get_size
        translated_hint_text = TranslationService.get_text("select_measurement_hint", self.current_language_display)

        self.dropdown = ft.Dropdown(
            hint_text=translated_hint_text,
            options=self.get_options(), # Options will use self.text_color and self.current_language_display
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
            text_size=self.text_handler_get_size('dropdown_text'),
            hint_style=ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
        )
        # label_style is not actively used for this dropdown based on current setup
        # if self.dropdown.label_style is None: self.dropdown.label_style = ft.TextStyle()
        # self.dropdown.label_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
        return self.dropdown

    def set_unit(self, unit_code):
        self.selected_unit = unit_code
        logging.info(f"DropdownMeasurement: selected_unit updated to {unit_code}")
        
        # Aggiorna lo stato dell'applicazione se state_manager è disponibile
        if self.state_manager and self.page:
            logging.info(f"DropdownMeasurement: Queuing state update for unit: {unit_code} via page.run_task")
            self.page.run_task(self.state_manager.set_state, "unit", unit_code)
        elif not self.page:
            logging.warning("DropdownMeasurement: self.page is not available, cannot run task for set_state.")
        elif not self.state_manager:
            logging.warning("DropdownMeasurement: self.state_manager is not available, cannot set state.")

    def handle_theme_change(self, event_data=None): # This method might be deprecated by direct calls to update_text_sizes
        """Handle theme change events by updating the dropdown appearance using stored text_color and language."""
        if self.dropdown:
            # self.text_color and self.current_language_display should be updated by the parent.
            # This method just re-applies them.
            self.dropdown.border_color = self.text_color.get("BORDER", ft.Colors.BLACK)
            self.dropdown.focused_border_color = self.text_color.get("ACCENT", ft.Colors.BLUE)
            self.dropdown.bgcolor = self.text_color.get("CARD_BACKGROUND", ft.Colors.WHITE)
            self.dropdown.color = self.text_color.get("TEXT", ft.Colors.BLACK)
            
            translated_hint_text = TranslationService.get_text("select_measurement_hint", self.current_language_display)
            self.dropdown.hint_text = translated_hint_text

            if self.dropdown.hint_style:
                self.dropdown.hint_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else:
                self.dropdown.hint_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            
            # label_style not actively used
            # if self.dropdown.label_style: self.dropdown.label_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            # else: self.dropdown.label_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            
            self.dropdown.options = self.get_options() # Re-generate options with new language/theme
            self.dropdown.update()

    def get_selected_unit(self):
        return self.selected_unit

    def build(self):
        if not self.dropdown: # Create dropdown only if it doesn't exist
            self.dropdown = self.createDropdown()
        return self.dropdown
