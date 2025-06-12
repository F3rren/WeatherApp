import flet as ft
import logging
from services.api_service import ApiService
from utils.config import LIGHT_THEME, DARK_THEME, UNIT_SYSTEMS, DEFAULT_LANGUAGE # Added DEFAULT_LANGUAGE
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService # Added TranslationService

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
        if self.dropdown:
            if hasattr(self.dropdown, 'text_size'):
                self.dropdown.text_size = self.text_handler.get_size('dropdown_text')
        
        # Request page update
        if self.page:
            self.page.update()

    def get_options(self, theme=None):
        # Accept theme so we can set the correct color for option content
        current_language = DEFAULT_LANGUAGE
        if self.state_manager:
            current_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE

        if theme is None:
            is_dark = False
            if self.state_manager and hasattr(self.state_manager, 'page'):
                is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
        options = []
        for unit_system_code, name_key in self.unit_name_keys.items():
            translated_name = TranslationService.get_text(name_key, current_language)
            options.append(
                ft.dropdown.Option(
                    key=unit_system_code,
                    text=translated_name, # Use translated name for accessibility/search
                    content=ft.Text(
                        value=translated_name,
                        color=theme["TEXT"]
                    ),
                )
            )
        return options
    
    def createDropdown(self):
        current_language = DEFAULT_LANGUAGE
        if self.state_manager:
            current_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
        
        def dropdown_changed(e):
            unit_code = e.control.value
            print(f"Selected unit: {unit_code}")
            self.set_unit(unit_code) # Call set_unit to handle selection and state update
            # if self.state_manager: # Removed direct state update from here
                # Use asyncio.create_task to avoid blocking if set_state is async
                # import asyncio # Removed
                # asyncio.create_task(self.state_manager.set_state("unit", unit_code)) # Removed
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        current_unit = "metric"
        if self.state_manager:
            current_unit = self.state_manager.get_state('unit') or "metric"
            self.selected_unit = current_unit

        is_dark = False
        if self.state_manager and hasattr(self.state_manager, 'page'):
            is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME

        translated_hint_text = TranslationService.get_text("select_measurement_hint", current_language)

        dropdown = ft.Dropdown(
            autofocus=True,
            hint_text=translated_hint_text, # Use translated hint text
            options=self.get_options(theme),
            on_change=dropdown_changed,
            # expand=True, # Removed to allow custom width
            width=200, # Set a common width
            value=current_unit,
            border_width=2,
            border_color=theme["BORDER"],
            focused_border_color=theme["ACCENT"],
            focused_border_width=2,
            bgcolor=theme["CARD_BACKGROUND"],
            color=theme["TEXT"],
            content_padding=ft.padding.symmetric(horizontal=10, vertical=8), # Adjusted padding
            text_size=self.text_handler.get_size('dropdown_text') if hasattr(self, 'text_handler') else 14,
        )
        # Imposta label_style e hint_style come nel dropdown lingua
        if dropdown.hint_style is None:
            dropdown.hint_style = ft.TextStyle()
        dropdown.hint_style.color = theme.get("SECONDARY_TEXT", ft.Colors.GREY_700)
        if dropdown.label_style is None:
            dropdown.label_style = ft.TextStyle()
        dropdown.label_style.color = theme.get("SECONDARY_TEXT", ft.Colors.GREY_700)
        self.dropdown = dropdown
        return dropdown

    def set_unit(self, unit_code):
        self.selected_unit = unit_code
        logging.info(f"DropdownMeasurement: selected_unit updated to {unit_code}")
        
        # Aggiorna lo stato dell'applicazione se state_manager è disponibile
        if self.state_manager and self.page:
            # import asyncio # Removed
            
            # Funzione wrapper per gestire chiamate asincrone in modo sicuro
            # This local helper might be redundant if set_state is already robustly handling async calls
            # Consider removing if direct asyncio.create_task(self.state_manager.set_state(...)) is sufficient
            # def call_async_safely(coro): # Removed call_async_safely
            #     try:
            #         loop = asyncio.get_event_loop()
            #     except RuntimeError: # pragma: no cover
            #         loop = asyncio.new_event_loop()
            #         asyncio.set_event_loop(loop)
            #     
            #     if not loop.is_running(): # pragma: no cover
            #         return loop.run_until_complete(coro)
            #     else: # pragma: no cover
            #         return asyncio.create_task(coro) # Ensure it\'s a task
            
            # Aggiorna lo stato con la nuova unità di misura
            # Directly call set_state, which should handle notifying observers.
            # The WeatherView will observe the "unit" state change and update the UI.
            # asyncio.create_task(self.state_manager.set_state("unit", unit_code)) # Removed
            logging.info(f"DropdownMeasurement: Queuing state update for unit: {unit_code} via page.run_task")
            self.page.run_task(self.state_manager.set_state, "unit", unit_code)
            # logging.info(f"State \'unit\' set to: {unit_code}") # Old log message
        elif not self.page:
            logging.warning("DropdownMeasurement: self.page is not available, cannot run task for set_state.")
        elif not self.state_manager:
            logging.warning("DropdownMeasurement: self.state_manager is not available, cannot set state.")

    def handle_theme_change(self, event_data=None):
        """Handle theme change events by updating the dropdown appearance"""
        if self.dropdown and self.state_manager:
            current_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            is_dark = False
            if event_data and "is_dark" in event_data:
                is_dark = event_data["is_dark"]
            elif hasattr(self.state_manager, 'page'):  # Fallback
                is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self.dropdown.border_color = theme.get("BORDER", ft.Colors.BLACK)
            self.dropdown.focused_border_color = theme.get("ACCENT", ft.Colors.BLUE)
            self.dropdown.bgcolor = theme.get("CARD_BACKGROUND", ft.Colors.WHITE)
            self.dropdown.color = theme.get("TEXT", ft.Colors.BLACK)
            
            translated_hint_text = TranslationService.get_text("select_measurement_hint", current_language)
            self.dropdown.hint_text = translated_hint_text

            # Imposta label_style e hint_style come nel dropdown lingua
            if self.dropdown.hint_style is None:
                self.dropdown.hint_style = ft.TextStyle()
            self.dropdown.hint_style.color = theme.get("SECONDARY_TEXT", ft.Colors.GREY_700)
            if self.dropdown.label_style is None:
                self.dropdown.label_style = ft.TextStyle()
            self.dropdown.label_style.color = theme.get("SECONDARY_TEXT", ft.Colors.GREY_700)
            self.dropdown.options = self.get_options(theme)
            self.dropdown.update()

    def get_selected_unit(self):
        return self.selected_unit

    def build(self):
        if not self.dropdown: # Create dropdown only if it doesn't exist
            self.dropdown = self.createDropdown()
        return self.dropdown
