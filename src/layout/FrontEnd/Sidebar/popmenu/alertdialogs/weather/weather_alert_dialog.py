import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService

class WeatherAlertDialog:
        
    def __init__(self, page, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, text_color=None):
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.text_color = text_color if text_color else (DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"])
        self.dialog = None
        
        # Inizializzazione del ResponsiveTextHandler
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 20,      # Titolo del dialogo
                'body': 14,       # Testo normale
                'icon': 20,       # Icone
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Dizionario dei controlli di testo per aggiornamento facile
        self.text_controls = {}
        
        # Sovrascrivi il gestore di ridimensionamento della pagina
        if self.page:
            # Salva l'handler originale se presente
            original_resize_handler = self.page.on_resize
            
            def combined_resize_handler(e):
                # Aggiorna le dimensioni del testo
                self.text_handler._handle_resize(e)
                # Aggiorna i controlli di testo
                self.update_text_controls()
                # Chiama anche l'handler originale se esiste
                if original_resize_handler:
                    original_resize_handler(e)
            
            self.page.on_resize = combined_resize_handler
 
    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati"""
        for control, size_category in self.text_controls.items():
            if size_category == 'icon':
                # Per le icone, aggiorna size
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
            else:
                # Per i testi, aggiorna size
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
        
        # Richiedi l'aggiornamento della pagina
        if self.page and self.dialog and self.dialog.page:
            self.dialog.update()

    def createAlertDialog(self, page):
        # Reset text controls dictionary before rebuilding
        self.text_controls = {}
        
        # Determina i colori in base al tema corrente
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        self.text_color = current_theme["TEXT"]
        
        # Utilizza i colori dal tema corrente
        bg_color = current_theme["DIALOG_BACKGROUND"]

        # Creare i controlli di testo con dimensioni responsive
        # Get current language
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            state_manager = self.page.session.get('state_manager')
            self.language = state_manager.get_state('language') or 'en'
        else:
            self.language = 'en'
            
        title_text = ft.Text(
            TranslationService.get_text("weather", self.language),
            size=self.text_handler.get_size('title'),
            weight=ft.FontWeight.BOLD,
            color=self.text_color
        )
        
        # Creazione delle icone con dimensioni responsive
        language_icon = ft.Icon(ft.Icons.LANGUAGE, size=self.text_handler.get_size('icon'), color="#ff6b35")
        measurement_icon = ft.Icon(ft.Icons.STRAIGHTEN, size=self.text_handler.get_size('icon'), color="#22c55e")
        location_icon = ft.Icon(ft.Icons.LOCATION_ON, size=self.text_handler.get_size('icon'), color="#ef4444")
        theme_icon = ft.Icon(ft.Icons.DARK_MODE, size=self.text_handler.get_size('icon'), color="#3b82f6")
        
        # Creazione dei testi con dimensioni responsive
        language_text = ft.Text(TranslationService.get_text("language", self.language), size=self.text_handler.get_size('body'), weight=ft.FontWeight.W_500, color=self.text_color)
        measurement_text = ft.Text(TranslationService.get_text("measurement", self.language), size=self.text_handler.get_size('body'), weight=ft.FontWeight.W_500, color=self.text_color)
        location_text = ft.Text(TranslationService.get_text("use_current_location", self.language), size=self.text_handler.get_size('body'), weight=ft.FontWeight.W_500, color=self.text_color)
        theme_text = ft.Text(TranslationService.get_text("dark_theme", self.language), size=self.text_handler.get_size('body'), weight=ft.FontWeight.W_500, color=self.text_color)
        close_button_text = ft.Text(TranslationService.get_text("close", self.language), color=current_theme["ACCENT"], size=self.text_handler.get_size('body'))
        
        # Registra i controlli nel dizionario
        self.text_controls[title_text] = 'title'
        self.text_controls[language_text] = 'body'
        self.text_controls[measurement_text] = 'body'
        self.text_controls[location_text] = 'body'
        self.text_controls[theme_text] = 'body'
        self.text_controls[language_icon] = 'icon'
        self.text_controls[measurement_icon] = 'icon'
        self.text_controls[location_icon] = 'icon'
        self.text_controls[theme_icon] = 'icon'
        self.text_controls[close_button_text] = 'body'

        # Dialog semplificato per test
        self.dialog = ft.AlertDialog(
            title=title_text,
            bgcolor=bg_color,
            content=ft.Container(
                #width=400,  # Imposta una larghezza fissa per il dialogo
                content=ft.Column(
                controls=[
                    # Sezione lingua
                    ft.Row(
                        controls=[
                            ft.Row(                                
                                controls=[language_icon, language_text],
                                spacing=10,
                            ),
                            #self.language_dropdown.build(),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    # Sezione unità di misura
                    ft.Row(
                        controls=[
                            ft.Row(                                
                                controls=[measurement_icon, measurement_text],
                                spacing=10,
                            ),
                            #self.measurement_dropdown.build(),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    # Sezione posizione attuale
                    ft.Row(
                        controls=[
                            ft.Row(                                
                                controls=[location_icon, location_text],
                                spacing=10,
                            ),
                            #self.create_location_toggle(),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Row(                                
                                controls=[theme_icon, theme_text],
                                spacing=10,
                            ),
                            #self.create_theme_toggle(),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                height=280,
                expand=True,
                spacing=20,
                ),
            ),
            actions=[
                ft.TextButton(
                    TranslationService.get_text("close", self.language),
                    content=close_button_text,
                    style=ft.ButtonStyle(
                        color=current_theme["ACCENT"],
                        overlay_color=ft.Colors.with_opacity(0.1, current_theme["ACCENT"]),
                    ),
                    on_click=lambda e: page.close(self.dialog)
                ),
            ],
        )
        
        return self.dialog