import flet as ft
from services.translation_service import TranslationService
from utils.config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class DailyForecastItems:
    """
    An item displaying daily forecast information.
    """
    
    def __init__(self, day: str, icon_code: str, temp_min: int, temp_max: int, text_color: str, page: ft.Page = None):
        self.day = day
        self.icon_code = icon_code
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.text_color = text_color
        self.page = page

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'label': 30,      # Etichette
                'icon': 100,       # Icone (dimensione base),
                'value': 18,       # Valori (es. temperature, percentuali)
            },
            breakpoints=[600, 900, 1200, 1600]  # Breakpoint per il ridimensionamento
        )        

        # Inizializza la lingua dinamicamente PRIMA di usarla
        if page and hasattr(page, 'session') and page.session.get('state_manager'):
            state_manager = page.session.get('state_manager')
            self.language = state_manager.get_state('language') or 'en'
            state_manager.register_observer("language_event", self.handle_language_change)
        else:
            self.language = 'en'

        # Traduci il giorno della settimana nella lingua selezionata
        self.day_text = ft.Text(
            TranslationService.translate_weekday(self.day, self.language),
            size=self.text_handler.get_size('value'),
            weight="bold",
            color=self.text_color
        )

        self.temp_span_min = ft.TextSpan(
            f"{self.temp_min}°",
            ft.TextStyle(
                size=self.text_handler.get_size('value'),
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE, # Keep specific Colors for min/max temp for now
            )
        )
        self.temp_span_separator = ft.TextSpan(" / ",
            ft.TextStyle(
                size=self.text_handler.get_size('value'),
                weight=ft.FontWeight.BOLD,
                color=self.text_color # Separator sahould follow theme
            )
        )
        self.temp_span_max = ft.TextSpan(
            f"{self.temp_max}°",
            ft.TextStyle(
                size=self.text_handler.get_size('value'),
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED, # Keep specific Colors for min/max temp for now
            )
        )
        self.temperature_text = ft.Text(
            spans=[
                self.temp_span_min,
                self.temp_span_separator,
                self.temp_span_max,
            ],
            expand=True,
        )

        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                state_manager.register_observer("theme_event", self.handle_theme_change)


    def handle_language_change(self, event_data=None):
        """Aggiorna il giorno quando cambia la lingua."""
        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                self.language = state_manager.get_state('language') or 'en'
        # Aggiorna solo il testo del giorno della settimana con la traduzione corretta
        self.day_text.value = TranslationService.translate_weekday(self.day, self.language)
        # Aggiorna solo se il controllo è già aggiunto alla pagina
        if hasattr(self.day_text, 'page') and self.day_text.page:
            self.day_text.update()

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]

            if hasattr(self, 'day_text'):
                self.day_text.color = self.text_color
                if getattr(self.day_text, 'page', None):
                    self.day_text.update()

            if hasattr(self, 'temp_span_separator'):
                self.temp_span_separator.style.color = self.text_color
                # We need to update the parent Text control for TextSpan changes to be visible
                if hasattr(self, 'temperature_text') and getattr(self.temperature_text, 'page', None):
                    self.temperature_text.update()

    def build(self) -> ft.Row:
        """Build the daily forecast item"""
        # Modifica della struttura della riga per distribuire meglio gli spazi
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Contenitore per il giorno con larghezza fissa
                    ft.Container(
                        content=self.day_text,
                        alignment=ft.alignment.center_left
                    ),
                    # Icona al centro
                    ft.Container(
                        content=ft.Image(
                            src=f"https://openweathermap.org/img/wn/{self.icon_code}@4x.png",
                            width=self.text_handler.get_size('icon'), 
                            height=self.text_handler.get_size('icon'),
                        ),
                        width=100,  # Fissa una larghezza per l'icona
                        alignment=ft.alignment.center,
                    ),
                    # Contenitore per la temperatura con larghezza fissa
                    ft.Container(
                        content=self.temperature_text,
                        alignment=ft.alignment.center_right
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            padding=ft.padding.only(left=10, right=10)
        )
