import flet as ft

from config import LANGUAGES

class DropdownLanguage:
    
    def __init__(self, state_manager=None):
        self.selected_language = None
        self.state_manager = state_manager

    def get_language_name_by_code(self, code):
        """Restituisce il nome della lingua dato il codice"""
        for language in LANGUAGES:
            if language["code"] == code:
                return language["name"]
        return "English"  # Default


    def get_options(self):
        options = []
        for language in LANGUAGES:
            # Converte il codice paese in formato corretto per l'API (lowercase)
            country_code = language['code'].lower()
            
            # Crea il contenuto con bandiera e testo
            content = ft.Row(
                controls=[
                    ft.Image(
                        src=f"/flags/{country_code}.png",
                        width=24,
                        height=16,
                        fit=ft.ImageFit.COVER,
                        border_radius=ft.border_radius.all(2),
                        # Fallback in caso l'immagine non si carichi
                        error_content=ft.Container(
                            width=24,
                            height=16,
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
                    key=language["name"],  # Usa il nome come key
                    text=language["name"],  # Testo che verrà mostrato quando selezionato
                    content=content,
                )
            )
        return options

    def createDropdown(self):
        
        def dropdown_changed(e):
            # Trova il codice lingua dal nome selezionato
            selected_name = e.control.value
            language_code = self.get_language_code_by_name(selected_name)
            self.set_language(language_code)
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        # Ottieni il valore corrente della lingua dallo state manager, se disponibile
        current_language_code = 'en'  # Valore predefinito
        if self.state_manager:
            current_language_code = self.state_manager.get_state('language') or 'en'
            self.selected_language = current_language_code

        # Converti il codice lingua nel nome per il dropdown
        current_language_name = self.get_language_name_by_code(current_language_code)

        return ft.Dropdown(
            autofocus=True,
            label='Language',
            hint_text='Select language',
            options=self.get_options(),
            on_change=dropdown_changed,
            expand=True,  # Usa tutto lo spazio disponibile
            value=current_language_name,  # Usa il nome invece del codice
            # text_size rimosso poiché non supportato in Flet 0.28.2
            border_width=2,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.BLUE,
            focused_border_width=2,
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
        
        print(f'Language set to: {self.selected_language}')

    def get_selected_language(self):
        return self.selected_language

    def build(self):
        return self.createDropdown()
