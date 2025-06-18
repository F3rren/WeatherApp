import flet as ft
import logging
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE
from utils.translations_data import LANGUAGES 
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService # Added import

class DropdownLanguage:
    
    def __init__(self, state_manager=None, page: ft.Page = None):
        self.selected_language = None
        self.state_manager = state_manager
        self.page = page
        self.dropdown = None
        
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
            
            # Dictionary to track text controls (currently not used by update_text_controls in this class)
            self.text_controls = {} 
            
            # Register as observer for responsive updates
            self.text_handler.add_observer(self.update_text_controls)

    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        if not self.page or not hasattr(self, 'text_handler') or not self.text_handler:
            return

        if self.dropdown:
            if hasattr(self.dropdown, 'text_style') and self.dropdown.text_style:
                 self.dropdown.text_style.size = self.text_handler.get_size('dropdown_text')
            if hasattr(self.dropdown, 'hint_style') and self.dropdown.hint_style:
                 self.dropdown.hint_style.size = self.text_handler.get_size('hint_text')
            elif hasattr(self.dropdown, 'text_size'): # Fallback
                self.dropdown.text_size = self.text_handler.get_size('dropdown_text')
        
        if self.dropdown and self.dropdown.page:
            self.dropdown.update()
        

    def get_language_name_by_code(self, code):
        """Restituisce il nome della lingua dato il codice"""
        for language in LANGUAGES:
            if language["code"] == code:
                return language["name"]
        return "English"  # Default

    def get_options(self, theme=None): # Added theme argument
        options = []
        base_path = "/flags/"

        effective_theme = theme
        if effective_theme is None: # Determine theme if not provided
            if self.page:
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
                effective_theme = DARK_THEME if is_dark else LIGHT_THEME
            else: # Fallback if page is somehow None
                effective_theme = LIGHT_THEME 
        
        text_color_for_options = effective_theme.get("TEXT", ft.Colors.BLACK)

        for lang in LANGUAGES:
            code = lang["code"]
            name = lang["name"]
            flag = lang.get("flag", "")
            
            option_content = ft.Row(
                controls=[],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            
            if flag:
                try:
                    flag_path = f"{base_path}{flag}"
                    flag_image = ft.Image(src=flag_path, width=24, height=16, fit=ft.ImageFit.CONTAIN)
                    option_content.controls.append(flag_image)
                except Exception as e:
                    logging.error(f"Error loading flag for {code}: {e}")
                    option_content.controls.append(ft.Container(width=24, height=16))
            else:
                option_content.controls.append(ft.Container(width=24, height=16))
            
            option_content.controls.append(ft.Text(name, color=text_color_for_options)) # Themed text
            
            options.append(ft.dropdown.Option(key=code, text=name, content=option_content))
        
        return options

    def get_language_code_by_name(self, name):
        """Restituisce il codice lingua dato il nome"""
        for language in LANGUAGES:
            if language["name"] == name:
                return language["code"]
        return "en"  # Default

    def set_language(self, language_code): # Parameter renamed for clarity
        self.selected_language = language_code
        logging.info(f'Impostazione lingua: {language_code} - {self.get_language_name_by_code(language_code)}')

        if self.state_manager:
            import asyncio
            
            def call_async_safely(coro):
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                if not loop.is_running():
                    return loop.run_until_complete(coro)
                else: # If loop is already running (e.g. in Flet context)
                    return asyncio.create_task(coro) 
            
            call_async_safely(self.state_manager.set_state("language", language_code))
            logging.info(f'Stato aggiornato con lingua: {language_code}')
            call_async_safely(self.state_manager.notify_all("language_event", {"language": language_code}))
        
        logging.info(f'Lingua impostata con successo: {self.selected_language} - {self.get_language_name_by_code(self.selected_language)}')

    def handle_theme_change(self, event_data=None):
        """Handle theme change events by updating the dropdown appearance"""
        if not self.dropdown or not self.page:
            return

        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        if event_data and "is_dark" in event_data: # Event data can override
            is_dark = event_data["is_dark"]
        
        current_theme = DARK_THEME if is_dark else LIGHT_THEME # Renamed to current_theme for consistency
        
        text_color = current_theme["TEXT"]
        if self.dropdown.text_style:
            self.dropdown.text_style.color = text_color
        
        if self.dropdown.hint_style:
            self.dropdown.hint_style.color = ft.Colors.with_opacity(0.6, text_color)
        
        self.dropdown.bgcolor = current_theme.get("BACKGROUND_SECONDARY", current_theme["BACKGROUND"])
        self.dropdown.border_color = current_theme.get("BORDER", current_theme["OUTLINE"])
        self.dropdown.focused_border_color = current_theme["ACCENT"]
        
        # Re-fetch options to update text color within options content
        self.dropdown.options = self.get_options(theme=current_theme)

        if self.dropdown.page:
            self.dropdown.update()

    def cleanup(self):
        """Cleanup method to remove observers"""
        if hasattr(self, 'text_handler') and self.text_handler:
            self.text_handler.remove_observer(self.update_text_controls)
    
    def build(self):
        """Costruisce e restituisce il controllo Dropdown."""
        if not self.page:
            logging.error("DropdownLanguage: Page context not available to build dropdown.")
            return ft.Text("Error: Page context missing for Language Dropdown", color="red")

        current_language = DEFAULT_LANGUAGE
        if self.state_manager:
            current_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE

        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        text_color = current_theme["TEXT"]
        bgcolor = current_theme.get("BACKGROUND_SECONDARY", current_theme["BACKGROUND"])
        # Ensure "OUTLINE" also has a fallback if it's missing from the theme
        border_color = current_theme.get("BORDER", current_theme.get("OUTLINE", ft.Colors.BLACK)) # Added .get() for OUTLINE
        current_language_code = "en" 
        if self.state_manager:
            current_language_code = self.state_manager.get_state("language") or "en"
        self.selected_language = current_language_code # Ensure selected_language is initialized

        translated_hint_text = TranslationService.get_text("select_language_hint", current_language)

        self.dropdown = ft.Dropdown(
            value=current_language_code,
            options=self.get_options(theme=current_theme), # Pass theme
            on_change=self.on_language_change,
            width=250, 
            text_style=ft.TextStyle(color=text_color, size=self.text_handler.get_size('dropdown_text') if self.text_handler else 14),
            hint_text=translated_hint_text, # Translated hint
            hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, text_color), size=self.text_handler.get_size('hint_text') if self.text_handler else 13),
            bgcolor=bgcolor,
            border_color=border_color,
            border_radius=ft.border_radius.all(8),
            border_width=1,
            focused_border_color=current_theme["ACCENT"],
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
        )
        
        if self.text_handler:
            # self.text_controls[self.dropdown] = 'dropdown_text' # Removed: not used by update_text_controls
            self.update_text_controls() 

        return self.dropdown

    async def on_language_change(self, e):
        selected_code = e.control.value
        # set_language already handles state_manager update and notification
        self.set_language(selected_code) 
        # Removed: if hasattr(self, 'parent') and self.parent: self.parent.update()
        # Parent dialog should react to 'language_event' from state_manager if it needs to update.
