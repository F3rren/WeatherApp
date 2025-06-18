import flet as ft
import logging
from utils.translations_data import LANGUAGES 

class DropdownLanguage:
    
    def __init__(self, page: ft.Page, state_manager, text_color: dict, language: str, text_handler_get_size):
        self.page = page
        self.state_manager = state_manager
        self.text_color = text_color
        self.current_language_display = language # For potential future use if this component had its own translatable text
        self.text_handler_get_size = text_handler_get_size
        self.translation_service = self.page.session.get('translation_service') if self.page and hasattr(self.page, 'session') else None
        
        self.selected_language = None # This will be set from state_manager or during selection
        self.dropdown = None

    def update_text_sizes(self, text_handler_get_size, text_color: dict, language: str):
        """Update text sizes and colors for the dropdown."""
        self.text_handler_get_size = text_handler_get_size
        self.text_color = text_color
        self.current_language_display = language # Update if this component had its own text

        if self.dropdown:
            translated_hint_text = "Select language" # Default fallback
            if self.translation_service: # Ensure translation_service is available
                translated_hint_text = self.translation_service.get_text("select_language", self.current_language_display)
            self.dropdown.hint_text = translated_hint_text
            self.dropdown.text_size = self.text_handler_get_size('dropdown_text')
            self.dropdown.color = self.text_color["TEXT"]
            self.dropdown.border_color = self.text_color["BORDER"]
            self.dropdown.focused_border_color = self.text_color["ACCENT"]
            self.dropdown.bgcolor = self.text_color["CARD_BACKGROUND"]

            if self.dropdown.hint_style:
                self.dropdown.hint_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else:
                self.dropdown.hint_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            
            if self.dropdown.label_style: # Though label is not used in current createDropdown
                self.dropdown.label_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else: # Though label is not used
                self.dropdown.label_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))

            # Options might need re-styling if their text color is static; however, ft.Text defaults to inheriting.
            # If options had complex styling that doesn't inherit, they'd need updating here.
            # For now, assume ft.Text within options inherits color or is handled by Flet's theme propagation.

            if self.dropdown.page:
                self.dropdown.update()
                if self.page:
                    self.page.update()

    def get_language_name_by_code(self, code):
        """Restituisce il nome della lingua dato il codice"""
        for language_item in LANGUAGES:
            if language_item["code"] == code:
                return language_item["name"]
        return "English"  # Default


    def get_options(self):
        options = []
        
        # Usa un percorso assoluto rispetto alla cartella assets dell'applicazione
        # Flet cerca le risorse nella cartella assets specificata nell'ft.app() in main.py
        base_path = "/flags/"
        
        for lang in LANGUAGES:
            code = lang["code"]
            name = lang["name"]
            flag = lang.get("flag", "")
            
            # Crea l'opzione con un'immagine per la bandiera e il nome della lingua
            option_content = ft.Row(
                controls=[],  # Inizia con una lista vuota
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            
            # Aggiungi l'immagine della bandiera, se disponibile
            if flag:
                try:
                    flag_path = f"{base_path}{flag}"
                    flag_image = ft.Image(
                        src=flag_path,
                        width=24,
                        height=16,
                        fit=ft.ImageFit.CONTAIN,
                    )
                    option_content.controls.append(flag_image)
                except Exception as e:
                    logging.error(f"Error loading flag for {code}: {e}")
                    # Aggiungi un placeholder se l'immagine non può essere caricata
                    option_content.controls.append(ft.Container(width=24, height=16))
            else:
                # Aggiungi un placeholder se non è specificata alcuna bandiera
                option_content.controls.append(ft.Container(width=24, height=16))
            
            # Aggiungi il testo del nome della lingua
            # Ensure text color for options is also dynamic if needed, though ft.Text usually inherits.
            # If not, explicitly set color: self.text_color["TEXT"]
            option_content.controls.append(ft.Text(name)) # Potentially: ft.Text(name, color=self.text_color["TEXT"])
            
            # Aggiungi l'opzione al dropdown
            options.append(
                ft.dropdown.Option(
                    key=code,
                    text=name,
                    content=option_content,
                )
            )
        
        return options

    def createDropdown(self):
        
        def dropdown_changed(e):
            # Ottieni direttamente il codice lingua dalla selezione
            # Poiché hai impostato key=language["code"] nelle opzioni
            selected_code = e.control.value
            self.set_language(selected_code)
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        # Ottieni il valore corrente della lingua dallo state manager, se disponibile
        current_language_code = 'en'  # Valore predefinito
        if self.state_manager:
            current_language_code = self.state_manager.get_state('language') or 'en'
            self.selected_language = current_language_code
            logging.info(f'Lingua corrente dallo state manager: {current_language_code}')

        # Use the passed-in text_color (theme) and text_handler_get_size
        
        translated_hint_text = "Select language" # Default fallback
        if self.translation_service:
            translated_hint_text = self.translation_service.get_text("select_language", self.current_language_display)

        self.dropdown = ft.Dropdown(
            hint_text=translated_hint_text,
            options=self.get_options(),
            on_change=dropdown_changed,
            width=200, 
            value=current_language_code,
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
        
        return self.dropdown # Return the created dropdown

    def get_language_code_by_name(self, name):
        """Restituisce il codice lingua dato il nome"""
        for language_item in LANGUAGES:
            if language_item["name"] == name:
                return language_item["code"]
        return "en"  # Default

    def set_language(self, language_code): # Renamed parameter for clarity
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
                else:
                    return asyncio.create_task(coro)
            
            call_async_safely(self.state_manager.set_state("language", language_code))
            logging.info(f'Stato aggiornato con lingua: {language_code}')
            call_async_safely(self.state_manager.notify_all("language_event", language_code))
        
        logging.info(f'Lingua impostata con successo: {self.selected_language} - {self.get_language_name_by_code(self.selected_language)}')

    def handle_theme_change(self, event_data=None): # This method might be deprecated by direct calls to update_text_sizes
        """Handle theme change events by updating the dropdown appearance using stored text_color."""
        if self.dropdown:
            # The actual theme (dark/light) determination is now external,
            # self.text_color should be updated by the parent.
            # This method just re-applies the current self.text_color.
            self.dropdown.border_color = self.text_color.get("BORDER", ft.Colors.BLACK)
            self.dropdown.focused_border_color = self.text_color.get("ACCENT", ft.Colors.BLUE)
            self.dropdown.bgcolor = self.text_color.get("CARD_BACKGROUND", ft.Colors.WHITE)
            self.dropdown.color = self.text_color.get("TEXT", ft.Colors.BLACK)
            
            if self.dropdown.hint_style:
                self.dropdown.hint_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else:
                self.dropdown.hint_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))

            if self.dropdown.label_style: # Though label is not used
                self.dropdown.label_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else: # Though label is not used
                self.dropdown.label_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            
            self.dropdown.update()
            
    def build(self):
        if not self.dropdown: # Create dropdown only if it doesn't exist
            self.dropdown = self.createDropdown()
        return self.dropdown
