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

        # --- REMOVE ALL UI REBUILD/OBSERVER LOGIC ---
        # Instead, create PopMenu, SearchBar, Filter directly as in other frontend components
        from layout.frontend.sidebar.popmenu.pop_menu import PopMenu
        from layout.frontend.sidebar.searchbar import SearchBar
        from layout.frontend.sidebar.filter.filter import Filter
        from services.translation_service import TranslationService
        from components.responsive_text_handler import ResponsiveTextHandler
        # Get theme and language
        translation_service = TranslationService()
        cities = []
        try:
            from services.sidebar_service import SidebarService
            cities = SidebarService().loadAllCity()
            cities = [item["city"] for item in cities if "city" in item and item["city"]]
        except Exception:
            pass

        # Setup responsive text handler for sidebar
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={'title': 20, 'subtitle': 16, 'body': 14, 'container_text': 14, 'spacing': 10},
            breakpoints=[600, 900, 1200, 1600]
        )
        text_color = (DARK_THEME if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME)
        language = self.state_manager.get_state("language") or "en"
        get_size_func = self.text_handler.get_size

        # Create components directly with required args
        self.search_bar = SearchBar(
            page=self.page,
            text_color=text_color,
            text_handler_get_size=get_size_func,
            cities=cities,
            on_city_selected=self.update_weather_callback,
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

        # Compose the sidebar layout
        self.content = ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Container(content=self.pop_menu.build(self.page), col={"xs": 1, "md": 1}),
                    ft.Container(content=self.search_bar.build(), col={"xs": 10, "md": 10}),
                    ft.Container(content=self.filter.build(self.page), col={"xs": 2, "md": 1}),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                run_spacing=10,
            )
        )

    # Remove all other methods related to UI rebuild, observer registration, etc.
