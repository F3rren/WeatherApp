import flet as ft
import logging
from services.api_service import ApiService
from utils.config import LIGHT_THEME, DARK_THEME, UNIT_SYSTEMS, DEFAULT_LANGUAGE
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService

class DropdownMeasurement:

    def __init__(self, state_manager=None, page: ft.Page = None):
        self.selected_unit = None
        self.state_manager = state_manager
        self.page = page
        self.dropdown = None
        # Sistemi di misura disponibili
        self.units = UNIT_SYSTEMS
        # Mappiamo i codici dei sistemi di misura alle loro chiavi di traduzione per i nomi
        self.unit_name_keys = {code: details["name_key"] for code, details in UNIT_SYSTEMS.items()} # Corrected this line
        self.api = ApiService()  # Assuming ApiService is defined elsewhere

        # Initialize ResponsiveTextHandler
        if self.page:
            self.text_handler = ResponsiveTextHandler(
                page=self.page,
                base_sizes={
                    'dropdown_text': 14,  # Dropdown text size
                    'hint_text': 13,      # Hint text size
                },
                breakpoints=[600, 900, 1200, 1600]
            )
            
            # Dictionary to track text controls
            self.text_controls = {}
            
            # Register as observer for responsive updates
            self.text_handler.add_observer(self.update_text_controls)

    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        if not self.page or not self.text_handler: # Add checks for page and text_handler
            return
        if self.dropdown:
            if hasattr(self.dropdown, 'text_style') and self.dropdown.text_style:
                 self.dropdown.text_style.size = self.text_handler.get_size('dropdown_text')
            if hasattr(self.dropdown, 'hint_style') and self.dropdown.hint_style:
                 self.dropdown.hint_style.size = self.text_handler.get_size('hint_text')
        
        if self.dropdown and self.dropdown.page: # Check if dropdown is on page
            self.dropdown.update()
        # elif self.page: # Avoid redundant page update if dropdown itself is updated
            # self.page.update()

    def get_options(self, theme=None):
        # Accept theme so we can set the correct color for option content
        current_language = DEFAULT_LANGUAGE
        if self.state_manager:
            current_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE

        # Determine theme if not provided
        effective_theme = theme
        if effective_theme is None:
            is_dark = False
            if self.page: # Check if self.page exists
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            effective_theme = DARK_THEME if is_dark else LIGHT_THEME
        
        options = []
        for unit_system_code, details in self.units.items(): # Iterate through UNIT_SYSTEMS directly
            name_key = details["name_key"]
            translated_name = TranslationService.translate(name_key, current_language)
            options.append(
                ft.dropdown.Option(
                    key=unit_system_code,
                    text=translated_name, # Use translated name for accessibility/search
                    content=ft.Text(
                        value=translated_name,
                        color=effective_theme["TEXT"]
                    ),
                )
            )
        return options
    
    def build(self): # This is the single method for creating the dropdown
        """Costruisce e restituisce il controllo Dropdown per le unità di misura."""
        # Ensure page context is available from __init__
        if not self.page:
            logging.error("DropdownMeasurement: Page context not available to build dropdown.")
            return ft.Text("Error: Page context missing for Measurement Dropdown", color="red")

        current_language = DEFAULT_LANGUAGE
        if self.state_manager:
            current_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
        
        # Determine colors based on current theme
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        text_color = current_theme["TEXT"]
        bgcolor = current_theme.get("BACKGROUND_SECONDARY", current_theme["BACKGROUND"])
        border_color = current_theme.get("BORDER", current_theme.get("OUTLINE", ft.Colors.BLACK))

        current_unit = "metric" # Default
        if self.state_manager:
            current_unit = self.state_manager.get_state('unit') or "metric"
            self.selected_unit = current_unit

        translated_hint_text = TranslationService.translate("select_measurement_hint", current_language)

        self.dropdown = ft.Dropdown(
            value=self.selected_unit,
            options=self.get_options(theme=current_theme), # Pass theme to get_options
            on_change=self.on_unit_change, # Changed to a dedicated async method
            # Styling consistent with DropdownLanguage
            width=250,
            text_style=ft.TextStyle(color=text_color, size=self.text_handler.get_size('dropdown_text') if self.text_handler else 14),
            hint_text=translated_hint_text,
            hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, text_color), size=self.text_handler.get_size('hint_text') if self.text_handler else 13),
            bgcolor=bgcolor,
            border_color=border_color,
            border_radius=ft.border_radius.all(8),
            border_width=1,
            focused_border_color=current_theme["ACCENT"],
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
        )

        # Register the dropdown for responsive text updates
        if self.text_handler:
            # self.text_controls[self.dropdown] = 'dropdown_text' # Not needed if updating style directly
            self.update_text_controls() # Apply initial size

        return self.dropdown

    async def on_unit_change(self, e):
        """Gestisce il cambio dell'unità di misura."""
        unit_code = e.control.value
        logging.info(f"DropdownMeasurement: Selected unit - {unit_code}")
        self.selected_unit = unit_code
        if self.state_manager:
            await self.state_manager.set_state("unit", unit_code)
        # No explicit update call here, parent dialog/page should handle updates if needed

    # This method seems redundant if on_unit_change handles state update.
    # Keeping it for now in case it's used elsewhere, but it might be a candidate for removal.
    def set_unit(self, unit_code):
        self.selected_unit = unit_code
        # Update the dropdown value if it exists and is on the page
        if self.dropdown and self.dropdown.page:
            self.dropdown.value = unit_code
            self.dropdown.update() # This might be better handled by the parent dialog

    def update_language(self, language_code):
        """Aggiorna le traduzioni nel dropdown quando cambia la lingua."""
        if not self.page: # Add safety check
            return

        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        
        if self.dropdown:
            self.dropdown.options = self.get_options(theme=current_theme)
            # Update hint text translation
            translated_hint_text = TranslationService.translate("select_measurement_hint", language_code)
            self.dropdown.hint_text = translated_hint_text
            if self.dropdown.page: # Check if dropdown is on page
                self.dropdown.update()

    def update_theme(self):
        """Aggiorna il tema del dropdown."""
        if not self.page or not self.dropdown: # Add safety checks
            return

        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        text_color = current_theme["TEXT"]
        bgcolor = current_theme.get("BACKGROUND_SECONDARY", current_theme["BACKGROUND"])
        border_color = current_theme.get("BORDER", current_theme["OUTLINE"])

        self.dropdown.text_style.color = text_color
        if self.dropdown.hint_style:
            self.dropdown.hint_style.color = ft.Colors.with_opacity(0.6, text_color)
        self.dropdown.bgcolor = bgcolor
        self.dropdown.border_color = border_color
        self.dropdown.focused_border_color = current_theme["ACCENT"]
        
        # Re-fetch options to update text color within options content
        self.dropdown.options = self.get_options(theme=current_theme)

        if self.dropdown.page: # Check if dropdown is on page
            self.dropdown.update()
