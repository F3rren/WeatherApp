"""
Sidebar Manager for the MeteoApp.
Handles the initialization and management of the sidebar.
Now a Flet component itself.
"""

import flet as ft
from typing import Callable, Optional

from utils.config import DARK_THEME, LIGHT_THEME
from state_manager import StateManager
from services.location_toggle_service import LocationToggleService
from services.theme_toggle_service import ThemeToggleService
from layout.frontend.sidebar.popmenu.pop_menu import PopMenu
from layout.frontend.sidebar.searchbar import SearchBar
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
        cities = []
        try:
            from services.sidebar_service import SidebarService
            cities = SidebarService().loadAllCity()
            cities = [item["city"] for item in cities if "city" in item and item["city"]]
        except Exception:
            pass

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
            # Usa sempre page.run_task per chiamate async
            if hasattr(self.page, 'run_task'):
                return self.page.run_task(self.update_weather_callback, city, language, unit)
            else:
                res = self.update_weather_callback(city, language, unit)
                if hasattr(res, '__await__'):
                    import asyncio
                    return asyncio.create_task(res)
                return res

        self.search_bar = SearchBar(
            page=self.page,
            text_color=text_color,
            text_handler_get_size=get_size_func,
            cities=cities,
            on_city_selected=handle_city_selected,
            language=language
        )
        self.pop_menu = PopMenu(
            page=self.page,
            state_manager=self.state_manager,
            translation_service=translation_service,
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
        # Sidebar minimal stile flat con PopMenu e Filter integrati nella SearchBar
        divider_color = "#e0e0e0" if self.page.theme_mode != ft.ThemeMode.DARK else "#333"
        text_col = text_color["TEXT"]

        header = ft.Row([
            ft.Image(src="/assets/icon.png", width=28, height=28),
            ft.Text(
                "MeteoApp",
                size=16,
                weight=ft.FontWeight.W_500,
                color=text_col,
                style=ft.TextStyle(font_family="Arial Rounded MT Bold")
            ),
        ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)

        # PopMenu e Filter come widget prefix/suffix della SearchBar
        popmenu_size = 22  # come la x/clear e il filtro
        popmenu_container = ft.Container(
            content=self.pop_menu.createPopMenu(self.page, icon_size=popmenu_size, text_size=14),
            bgcolor=None,
            width=34,  # 22 icona + padding
            height=34,
            alignment=ft.alignment.center,
            padding=ft.padding.all(6),
        )
        # Filter come suffix_widget, dentro la searchbar, rotondo e centrato perfettamente
        filter_bg = "#23272f" if self.page.theme_mode == ft.ThemeMode.DARK else "#f7f9fb"
        filter_border = "#333" if self.page.theme_mode == ft.ThemeMode.DARK else "#e0e0e0"
        filter_icon = ft.Icon(
            ft.Icons.FILTER_ALT_OUTLINED,
            size=22,
            color=text_color["TEXT"]
        )
        filter_container = ft.Container(
            content=filter_icon,
            bgcolor=filter_bg,
            border=ft.border.all(1, filter_border),
            border_radius=32,
            width=34,
            height=34,
            padding=0,
            alignment=ft.alignment.center,
        )
        searchbar_field = self.search_bar.build(
            prefix_widget=popmenu_container,
            suffix_widget=filter_container
        )
        searchbar_field.width = None  # Espandibile
        searchbar_field.expand = True
        searchbar_field.padding = ft.padding.symmetric(horizontal=4, vertical=0)
        searchbar_row = ft.Row(
            [
                searchbar_field,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )

        self.content = ft.Column(
            [
                ft.Container(content=searchbar_row, padding=ft.padding.only(top=8, bottom=4)),
            ],
            spacing=0,
            expand=False,
        )
        self.padding = ft.padding.only(left=0, right=0)
        self.border_radius = 0
        self.shadow = None

        # Collega l'aggiornamento dinamico delle dimensioni del testo al resize della pagina
        def on_resize(e):
            self.update_text_sizes(self.text_handler.get_size, text_color, language)
        self.page.on_resize = on_resize

    def update_text_sizes(self, get_size_func: Callable, text_color: dict, language: str):
        """Aggiorna dinamicamente le dimensioni del testo e i colori in base alla finestra."""
        self.text_handler = get_size_func  # Per coerenza con altri componenti
        if hasattr(self.pop_menu, 'update_text_sizes'):
            self.pop_menu.update_text_sizes(get_size_func, text_color, language)
        if hasattr(self.filter, 'update_text_sizes'):
            self.filter.update_text_sizes(get_size_func, text_color, language)
        if hasattr(self.search_bar, 'update_text_sizes'):
            self.search_bar.update_text_sizes(get_size_func, text_color, language)
        if self.page:
            self.page.update()
