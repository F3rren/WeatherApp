# filepath: c:\Users\Utente\Desktop\Progetti\Python\MeteoApp\src\layout\frontend\sidebar\popmenu\alertdialogs\settings\dropdowns\dropdown_language.py
import flet as ft

from config import LANGUAGES

class DropdownLanguage:
    
    def __init__(self, state_manager=None):
        self.selected_language = None
        self.state_manager = state_manager

    def get_options(self):
        options = []
        for language in LANGUAGES:
            options.append(
                ft.DropdownOption(
                    key=language["name"],
                    content=ft.Text(
                        value=language["name"],
                    ),
                )
            )
        return options

    def createDropdown(self):
        
        def dropdown_changed(e):
            self.set_language(e.control.value)
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        # Ottieni il valore corrente della lingua dallo state manager, se disponibile
        current_language = 'en'  # Valore predefinito
        if self.state_manager:
            current_language = self.state_manager.get_state('language') or 'en'
            self.selected_language = current_language

        return ft.Dropdown(
            autofocus=True,
            label='Language',
            hint_text='Select language',
            options=self.get_options(),
            on_change=dropdown_changed,
            expand=True,  # Usa tutto lo spazio disponibile
            value=current_language,
            # text_size rimosso poiché non supportato in Flet 0.28.2
            border_width=2,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.BLUE,
            focused_border_width=2,
            content_padding=ft.padding.all(8)
        )

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
