import flet as ft

from config import LANGUAGES, LIGHT_THEME, DARK_THEME

class DropdownLanguage:
    
    def __init__(self, state_manager=None):
        self.selected_language = None
        self.state_manager = state_manager
        self.dropdown = None
        
        # Register for theme change events if state_manager is available
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_change)

    def get_language_name_by_code(self, code):
        """Restituisce il nome della lingua dato il codice"""
        for language in LANGUAGES:
            if language["code"] == code:
                return language["name"]
        return "English"  # Default


    def get_options(self):
        options = []
        for language in LANGUAGES: 
            # Crea il contenuto con bandiera e testo
            content = ft.Row(
                controls=[
                    ft.Image(
                        src=f"flags/{language['code']}.png",
                        width=40,
                        height=20,
                        # Fallback in caso l'immagine non si carichi
                        error_content=ft.Container(
                            width=30,
                            height=20,
                            bgcolor=ft.Colors.GREY_300,
                            border_radius=ft.border_radius.all(2),
                            content=ft.Text(
                                language['code'][:2], 
                                size=8, 
                                text_align=ft.TextAlign.CENTER
                            )
                        )
                    ),
                    ft.Text(
                        value=language["name"],
                        size=14,
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            
            options.append(
                ft.DropdownOption(
                    key=language["code"],  # Usa il codice come key
                    text=language["name"],  # Testo che verrà mostrato quando selezionato
                    content=content,
                )
            )
        return options

    def createDropdown(self):
        
        def dropdown_changed(e):
            # Ottieni direttamente il codice lingua dalla selezione
            # Poiché hai impostato key=language["code"] nelle opzioni
            selected_code = e.control.value
            print(f'Lingua selezionata dal dropdown: {selected_code}')
            print(f'Nome lingua: {self.get_language_name_by_code(selected_code)}')
            self.set_language(selected_code)
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        # Ottieni il valore corrente della lingua dallo state manager, se disponibile
        current_language_code = 'en'  # Valore predefinito
        if self.state_manager:
            current_language_code = self.state_manager.get_state('language') or 'en'
            self.selected_language = current_language_code
            print(f'Lingua corrente dallo state manager: {current_language_code}')
        
        # Assumiamo che il valore nel dropdown debba essere il codice lingua
        # dato che abbiamo impostato key=language["code"] nelle opzioni

        # Determina i colori in base al tema corrente
        is_dark = False
        if self.state_manager and hasattr(self.state_manager, 'page'):
            is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME
        
        return ft.Dropdown(
            autofocus=True,
            label='Language',
            hint_text='Select language',
            options=self.get_options(),
            on_change=dropdown_changed,
            expand=True,  # Usa tutto lo spazio disponibile
            value=current_language_code,  # Usando direttamente il codice
            # text_size rimosso poiché non supportato in Flet 0.28.2
            border_width=2,
            border_color=theme["BORDER"],
            focused_border_color=theme["ACCENT"],
            focused_border_width=2,
            bgcolor=theme["CARD_BACKGROUND"],
            color=theme["TEXT"],
            content_padding=ft.padding.all(8)
        )

    def get_language_code_by_name(self, name):
        """Restituisce il codice lingua dato il nome"""
        for language in LANGUAGES:
            if language["name"] == name:
                return language["code"]
        return "en"  # Default

    def set_language(self, language):
        self.selected_language = language
        print(f'Impostazione lingua: {language} - {self.get_language_name_by_code(language)}')
        
        # Aggiorna lo stato dell'applicazione se state_manager è disponibile
        if self.state_manager:
            import asyncio
            
            # Funzione wrapper per gestire chiamate asincrone in modo sicuro
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
            
            # Aggiorna lo stato con il nuovo linguaggio
            call_async_safely(self.state_manager.set_state("language", language))
            print(f'Stato aggiornato con lingua: {language}')
        
        print(f'Lingua impostata con successo: {self.selected_language} - {self.get_language_name_by_code(self.selected_language)}')

    def handle_theme_change(self, event_data=None):
        """Handle theme change events by updating the dropdown appearance"""
        if self.dropdown and self.state_manager:
            is_dark = False
            if event_data and "is_dark" in event_data:
                is_dark = event_data["is_dark"]
            elif hasattr(self.state_manager, 'page'):  # Fallback
                is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
            
            theme = DARK_THEME if is_dark else LIGHT_THEME
            
            # Update dropdown appearance with the new theme colors
            self.dropdown.border_color = theme.get("BORDER", ft.colors.BLACK)
            self.dropdown.focused_border_color = theme.get("ACCENT", ft.colors.BLUE)
            self.dropdown.bgcolor = theme.get("CARD_BACKGROUND", ft.colors.WHITE)
            self.dropdown.color = theme.get("TEXT", ft.colors.BLACK)
            
            # Update label and hint text colors
            # Ensure label_style and hint_style are initialized if they are None
            if self.dropdown.label_style is None:
                self.dropdown.label_style = ft.TextStyle()
            self.dropdown.label_style.color = theme.get("SECONDARY_TEXT", ft.colors.GRAY_700)

            if self.dropdown.hint_style is None:
                self.dropdown.hint_style = ft.TextStyle()
            self.dropdown.hint_style.color = theme.get("SECONDARY_TEXT", ft.colors.GRAY_700)

            # Request update of the dropdown
            self.dropdown.update()
            
    def build(self):
        self.dropdown = self.createDropdown()
        return self.dropdown
