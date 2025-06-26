"""
Sidebar Manager for the MeteoApp.
Handles the initialization and management of the sidebar.
Now a Flet component itself.
"""

import flet as ft
from typing import Callable, Optional

from layout.sidebar.filter.filter import Filter
from layout.sidebar.popmenu.pop_menu import PopMenu
from layout.sidebar.searchbar.search_bar import SearchBar
from state_manager import StateManager
from services.location_toggle_service import LocationToggleService
from services.theme_toggle_service import ThemeToggleService
from utils.config import DARK_THEME, LIGHT_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class SidebarManager(ft.Container):
    """
    Manager per la sidebar dell'applicazione.
    Gestisce l'inizializzazione e il comportamento della sidebar.
    Ora è un componente Flet che contiene la UI della Sidebar.
    """
    def __init__(self, 
                 page: ft.Page, 
                 state_manager: StateManager, 
                 location_toggle_service: LocationToggleService,
                 theme_toggle_service: ThemeToggleService,
                 update_weather_callback: Optional[Callable] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.state_manager = state_manager
        self.location_toggle_service = location_toggle_service
        self.theme_toggle_service = theme_toggle_service
        self.update_weather_callback = update_weather_callback
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'icon': 25, #grandezza icone della sidebar
                'search_bar_text': 30, #grandezza testo della sidebar
                'popup_menu_button_icon': 20, #grandezza icone popup della sidebar (popmenu, filtro, etc.)
                'alert_dialog_text': 15, #grandezza testo dialogo di alert
                'alert_dialog_subtext': 15, #grandezza testo dei bottoni del dialogo di alert
                'alert_dialog_subicon': 15 #grandezza icone dei bottoni del dialogo di alert
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        self.cities = []  # Lista vuota per le città
        self.pop_menu = None
        self.search_bar = None
        self.filter = None
        self.update_ui()  # Initial UI setup
        self.content = self.build()

    def update_ui(self):
        """
        Aggiorna lo stato e i componenti della sidebar in base a tema, lingua, ecc.
        """
        text_color = (DARK_THEME if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME)
        language = self.state_manager.get_state("language") or "en"
        def handle_city_selected(city):
            language = self.state_manager.get_state("language") or "en"
            unit = self.state_manager.get_state("unit") or "metric"
            return self.update_weather_callback(city, language, unit)
        self.pop_menu = PopMenu(
            page=self.page,
            state_manager=self.state_manager,
            handle_location_toggle=self.location_toggle_service.handle_location_toggle,
            handle_theme_toggle=self.theme_toggle_service.handle_theme_toggle,
            theme_toggle_value=(self.page.theme_mode == ft.ThemeMode.DARK),
            location_toggle_value=self.state_manager.get_state("using_location") or False,
            text_color=text_color,
            language=language,
            text_handler_get_size=self.text_handler.get_size
        )
        self.search_bar = SearchBar(
            page=self.page,
            text_color=text_color,
            cities=self.cities,
            on_city_selected=handle_city_selected,
            language=language,
            text_handler_get_size=self.text_handler.get_size,
        )
        self.filter = Filter(
            page=self.page,
            state_manager=self.state_manager,
            handle_location_toggle=self.location_toggle_service.handle_location_toggle,
            handle_theme_toggle=self.theme_toggle_service.handle_theme_toggle,
            theme_toggle_value=(self.page.theme_mode == ft.ThemeMode.DARK),
            location_toggle_value=self.state_manager.get_state("using_location") or False,
            text_color=text_color,
            language=language,
            text_handler_get_size=self.text_handler.get_size
        )
        self.border_radius = 22
        self.shadow = ft.BoxShadow(blur_radius=18, color="#00000033")
        self.content = self.build()
        # self.update()  # <-- RIMOSSO: Non chiamare update() finché il controllo non è aggiunto alla pagina

    def build(self):
        """
        Costruisce una moderna sidebar con previsioni giornaliere simile al design mostrato.
        """
        # Header della sidebar con controlli
        header_section = ft.Container(
            content=ft.Row([
                # Search bar compatta
                ft.Container(
                    content=self.search_bar.build(
                        popmenu_widget=self.pop_menu.build(),
                        clear_icon_size=self.text_handler.get_size('icon'),
                    ),
                    expand=True,
                ),
            ]),
            padding=ft.padding.all(15),
            margin=ft.margin.only(bottom=10)
        )

        # Sezione previsioni giornaliere
        daily_forecasts = self._build_daily_forecast_list()
        
        return ft.Column([
            header_section,
            daily_forecasts,
        ], spacing=0, expand=True)

    def _build_daily_forecast_list(self):
        """Costruisce la lista delle previsioni giornaliere per la sidebar."""
        # Dati esempio per le previsioni giornaliere (sostituisci con dati reali)
        daily_data = [
            {"day": "Today", "high": 41, "low": 37, "icon": "01d", "desc": "Sunny cloudy"},
            {"day": "Tomorrow", "high": 39, "low": 33, "icon": "02d", "desc": "Partly cloudy"},
            {"day": "Wednesday", "high": 37, "low": 31, "icon": "03d", "desc": "Mostly cloudy"},
            {"day": "Thursday", "high": 36, "low": 30, "icon": "04d", "desc": "Cloudy"},
            {"day": "Friday", "high": 37, "low": 29, "icon": "01d", "desc": "Sunny"},
            {"day": "Saturday", "high": 39, "low": 31, "icon": "02d", "desc": "Partly cloudy"},
            {"day": "Sunday", "high": 38, "low": 32, "icon": "01d", "desc": "Sunny"},
            {"day": "Monday", "high": 36, "low": 29, "icon": "03d", "desc": "Cloudy"},
            {"day": "Tuesday", "high": 34, "low": 28, "icon": "04d", "desc": "Overcast"},
            {"day": "Wednesday", "high": 33, "low": 27, "icon": "09d", "desc": "Rain"},
        ]

        daily_items = []
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME
        text_color = theme.get("TEXT")

        for index, day_data in enumerate(daily_data):
            # Icona meteo piccola
            weather_icon = ft.Container(
                content=ft.Image(
                    src=f"https://openweathermap.org/img/wn/{day_data['icon']}@2x.png",
                    width=32,
                    height=32,
                    fit=ft.ImageFit.CONTAIN,
                ),
                width=40,
                alignment=ft.alignment.center
            )

            # Informazioni giorno
            day_info = ft.Column([
                ft.Text(
                    day_data["day"],
                    size=14,
                    weight="w500" if index == 0 else "w400",
                    color=text_color
                ),
                ft.Text(
                    day_data["desc"],
                    size=12,
                    color=theme.get("SECONDARY_TEXT"),
                    opacity=0.8
                )
            ], spacing=2, expand=True)

            # Temperature high/low
            temp_display = ft.Text(
                f"{day_data['high']}°/{day_data['low']}°",
                size=14,
                weight="w500",
                color=text_color
            )

            # Container per ogni giorno
            day_container = ft.Container(
                content=ft.Row([
                    weather_icon,
                    day_info,
                    temp_display,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
                padding=ft.padding.symmetric(horizontal=15, vertical=12),
                margin=ft.margin.only(bottom=2),
                bgcolor=theme.get("ACCENT", ft.Colors.BLUE_50) if index == 0 else None,  # Highlight today
                border_radius=10,
                on_click=lambda e, day=day_data: self._on_day_selected(day)
            )

            daily_items.append(day_container)

        return ft.Container(
            content=ft.Column(
                daily_items,
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
            padding=ft.padding.symmetric(horizontal=5)
        )

    def _on_day_selected(self, day_data):
        """Gestisce la selezione di un giorno specifico."""
        print(f"Selected day: {day_data['day']}")
        
        # Notifica il cambio di giorno attraverso lo state manager
        if self.state_manager:
            # Salva i dati del giorno selezionato
            self.state_manager.set_state('selected_day', day_data)
            
            # Notifica l'evento per aggiornare l'UI
            self.page.run_task(
                self.state_manager._notify_observers, 
                'day_selected_event', 
                day_data
            )
