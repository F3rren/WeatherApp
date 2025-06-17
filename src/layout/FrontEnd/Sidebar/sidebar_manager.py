"""
Sidebar Manager for the MeteoApp.
Handles the initialization and management of the sidebar.
Now a Flet component itself.
"""

import flet as ft
from typing import Callable, Optional

from state_manager import StateManager
from services.location_toggle_service import LocationToggleService
from services.theme_toggle_service import ThemeToggleService
from utils.config import DARK_THEME, LIGHT_THEME
from layout.frontend.sidebar.popmenu.pop_menu import PopMenu
from layout.frontend.sidebar.searchbar.search_bar import SearchBar
from layout.frontend.sidebar.filter.filter import Filter
from services.translation_service import TranslationService
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

        cities = []  # Rimosso il caricamento delle città dal DB

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

        text_color = (DARK_THEME if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME)
        language = self.state_manager.get_state("language") or "en"

        def handle_city_selected(city):
            language = self.state_manager.get_state("language") or "en"
            unit = self.state_manager.get_state("unit") or "metric"
            # Restituisci sempre la coroutine, sarà attesa da chi la invoca (SearchBar)
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
            cities=cities,  # Lista vuota per le città
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

        # --- MODERN SIDEBAR LAYOUT ---
        self.border_radius = 22
        self.shadow = ft.BoxShadow(blur_radius=18, color="#00000033")

        # Usa la logica del text_handler anche per le icone della X e del filtro

        # Row con popmenu a sinistra, searchbar al centro (espansa), filter a destra
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=self.search_bar.build(
                                    popmenu_widget=self.pop_menu.build(),
                                    clear_icon_size=self.text_handler.get_size('icon'),
                                    filter_widget=self.filter.build()
                                ),
                                expand=True,
                                margin=ft.margin.only(right=8, left=8)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    margin=ft.margin.only(bottom=8)
                ),
            ],
            spacing=0,
            expand=False,
        )
