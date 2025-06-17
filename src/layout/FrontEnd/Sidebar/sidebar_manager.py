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

        translation_service = TranslationService()
        cities = []  # Rimosso il caricamento delle città dal DB

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={'title': 20, 'subtitle': 16, 'body': 14, 'container_text': 14, 'spacing': 10},
            breakpoints=[600, 900, 1200, 1600]
        )
        text_color = (DARK_THEME if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME)
        language = self.state_manager.get_state("language") or "en"
        get_size_func = self.text_handler.get_size

        def handle_city_selected(city):
            language = self.state_manager.get_state("language") or "en"
            unit = self.state_manager.get_state("unit") or "metric"
            # Restituisci sempre la coroutine, sarà attesa da chi la invoca (SearchBar)
            return self.update_weather_callback(city, language, unit)

        self.search_bar = SearchBar(
            page=self.page,
            text_color=text_color,
            cities=cities,  # Lista vuota per le città
            on_city_selected=handle_city_selected,
            language=language
        )
        self.pop_menu = PopMenu(
            page=self.page,
            state_manager=self.state_manager,
            handle_location_toggle=self.location_toggle_service.handle_location_toggle,
            handle_theme_toggle=self.theme_toggle_service.handle_theme_toggle,
            theme_toggle_value=(self.page.theme_mode == ft.ThemeMode.DARK),
            location_toggle_value=self.state_manager.get_state("using_location") or False,
            text_color=text_color,
            language=language,
            text_handler_get_size=get_size_func
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
            text_handler_get_size=get_size_func
        )

        # --- MODERN SIDEBAR LAYOUT ---
        self.border_radius = 22
        self.shadow = ft.BoxShadow(blur_radius=18, color="#00000033")

        # Usa la logica del text_handler anche per le icone della X e del filtro
        icon_menu_size = self.text_handler.get_size('icon_menu')
        icon_clear_size = self.text_handler.get_size('icon_clear')
        icon_filter_size = self.text_handler.get_size('icon_filter')
        popmenu_widget = self.pop_menu.build(self.page, icon_size=icon_menu_size, text_size=16)
        filter_widget = self.filter.build(self.page, icon_size=icon_filter_size, text_size=16)

        # Row con popmenu a sinistra, searchbar al centro (espansa), filter a destra
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=self.search_bar.build(
                                    popmenu_widget=popmenu_widget,
                                    filter_widget=filter_widget,
                                    clear_icon_size=icon_clear_size  # Passa la size della X
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
