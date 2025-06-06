import flet as ft
from config import LANGUAGES, LIGHT_THEME, DARK_THEME
import os

class DropdownLanguage:
    
    def __init__(self, state_manager=None):
        self.selected_language = None
        self.state_manager = state_manager
        self.dropdown = None
        
        # Register for theme change events if state_manager is available
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_change)

        # Aggiungi un metodo per verificare l'esistenza delle immagini delle bandiere
        self._verify_flag_images()

    def _verify_flag_images(self):
        """Verifica che le immagini delle bandiere esistano."""
        # Percorso base per le bandiere
        base_path = os.path.join("assets", "flags")
        
        # Log delle bandiere mancanti
        missing_flags = []
        for lang in LANGUAGES:
            flag_file = lang.get("flag", "")
            if flag_file:
                # Controlla se il file esiste
                flag_path = os.path.join(base_path, flag_file)
                if not os.path.isfile(flag_path):
                    missing_flags.append(flag_file)
        
        # Se ci sono bandiere mancanti, registra un avviso
        if missing_flags:
            print(f"WARNING: The following flag images are missing: {', '.join(missing_flags)}")
            print(f"Searched in: {os.path.abspath(base_path)}")

    def get_language_name_by_code(self, code):
        """Restituisce il nome della lingua dato il codice"""
        for language in LANGUAGES:
            if language["code"] == code:
                return language["name"]
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
                    print(f"Error loading flag for {code}: {e}")
                    # Aggiungi un placeholder se l'immagine non può essere caricata
                    option_content.controls.append(ft.Container(width=24, height=16))
            else:
                # Aggiungi un placeholder se non è specificata alcuna bandiera
                option_content.controls.append(ft.Container(width=24, height=16))
            
            # Aggiungi il testo del nome della lingua
            option_content.controls.append(ft.Text(name))
            
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
            # Notifica anche l'evento language_event
            call_async_safely(self.state_manager.notify_all("language_event", language))
        
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
            self.dropdown.hint_style.color = theme.get("SECONDARY_TEXT", ft.colors.GRAY_700)
            if self.dropdown.hint_style is None:
                self.dropdown.hint_style = ft.TextStyle()
            self.dropdown.label_style.color = theme.get("SECONDARY_TEXT", ft.colors.GRAY_700)
            if self.dropdown.label_style is None:
                self.dropdown.label_style = ft.TextStyle()
            # Request update of the dropdown
            self.dropdown.update()
            
    def build(self):
        self.dropdown = self.createDropdown()
        return self.dropdown
