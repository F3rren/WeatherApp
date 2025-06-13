"""
SearchBar component for the MeteoApp.
"""

import flet as ft
from typing import Callable, Optional
import logging

from services.translation_service import TranslationService
from services.sidebar_service import SidebarService # Added import
from components.state_manager import StateManager
from utils.config import LIGHT_THEME, DARK_THEME

class SearchBar(ft.Container):
    """
    A search bar component that allows users to input a city name, with future support for query-based suggestions.
    """
    def __init__(self, page: ft.Page, state_manager: StateManager, 
                 translation_service: TranslationService, 
                 sidebar_service: SidebarService, # Added sidebar_service
                 on_city_selected: Optional[Callable[[str], None]] = None):
        super().__init__()
        self.page = page
        self.state_manager = state_manager
        self.translation_service = translation_service
        self.sidebar_service = sidebar_service # Store sidebar_service
        self.on_city_selected = on_city_selected

        self._text_color = self._get_current_text_color()
        self._border_color = self._get_current_border_color()
        self._bg_color = self._get_current_bg_color() # Kept for potential future use with suggestions background
        self._current_language = self.state_manager.get_state("language") or "en"

        # UI Elements
        self.search_field: ft.TextField | None = None
        self.search_button: ft.IconButton | None = None
        self.suggestions_view: ft.Column | None = None # To display suggestions
        
        # Container properties
        self.padding = ft.padding.symmetric(horizontal=5)
        self.alignment = ft.alignment.top_center # Align to top to accommodate suggestions below
        self.expand = True

    def _get_current_text_color(self) -> str:
        return DARK_THEME["TEXT"] if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"]

    def _get_current_border_color(self) -> str:
        return DARK_THEME["BORDER"] if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["BORDER"]
    
    def _get_current_bg_color(self) -> str:
        # This might be used for the background of the suggestions_view
        return DARK_THEME["BACKGROUND"] if self.page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["BACKGROUND"]

    def did_mount(self):
        """Called when the component is added to the page."""
        self.state_manager.register_observer("theme_event", self._handle_theme_change)
        self.state_manager.register_observer("language_event", self._handle_language_change)
        self._request_ui_rebuild()

    def will_unmount(self):
        """Called when the component is removed from the page."""
        self.state_manager.unregister_observer("theme_event", self._handle_theme_change)
        self.state_manager.unregister_observer("language_event", self._handle_language_change)

    def _handle_theme_change(self, event_data=None):
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_theme_change received unexpected event_data type: {type(event_data)}")
        self._text_color = self._get_current_text_color()
        self._border_color = self._get_current_border_color()
        self._bg_color = self._get_current_bg_color()
        self._request_ui_rebuild()

    def _handle_language_change(self, event_data=None):
        self._current_language = self.state_manager.get_state("language") or "en"
        self._request_ui_rebuild()

    def _request_ui_rebuild(self):
        self._update_and_build_ui()

    def _update_and_build_ui(self):
        self._build_ui_elements()
        if self.page: 
            try:
                self.update()
            except Exception as e:
                logging.error(f"SearchBar: Error during update: {e}")

    def _build_ui_elements(self):
        """Creates or updates the UI elements for the search bar."""
        placeholder_text = self.translation_service.get_text("search_placeholder", self._current_language)
        search_tooltip = self.translation_service.get_text("search_tooltip", self._current_language)

        if not self.search_field:
            self.search_field = ft.TextField(
                hint_text=placeholder_text,
                autofocus=False,
                expand=True,
                text_size=14,
                content_padding=ft.padding.symmetric(vertical=5, horizontal=10),
                border_color=self._border_color,
                color=self._text_color,
                on_submit=self._on_search_submit,
                on_change=self._on_input_change, # For autocomplete
                border_radius=ft.border_radius.all(5),
            )
        else:
            self.search_field.hint_text = placeholder_text
            self.search_field.border_color = self._border_color
            self.search_field.color = self._text_color

        if not self.search_button:
            self.search_button = ft.IconButton(
                icon=ft.Icons.SEARCH, # Corrected: ft.Icons (lowercase)
                icon_color=self._text_color,
                tooltip=search_tooltip,
                on_click=self._on_search_click,
                icon_size=20,
            )
        else:
            self.search_button.icon_color = self._text_color
            self.search_button.tooltip = search_tooltip

        if not self.suggestions_view:
            self.suggestions_view = ft.Column(
                spacing=2,
                tight=True,
                visible=False # Initially hidden
            )
        
        search_row = ft.Row(
            controls=[
                self.search_field,
                self.search_button,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        )

        self.content = ft.Column(
            controls=[
                search_row,
                self.suggestions_view
            ],
            spacing=5 # Spacing between search row and suggestions
        )

    def _on_input_change(self, e):
        query = e.data.strip().lower()
        if query:
            suggestions = self._fetch_city_suggestions(query)
            self._update_suggestions_display(suggestions)
        else:
            self._clear_suggestions()
            self._hide_suggestions()

    def _fetch_city_suggestions(self, query: str) -> list:
        """Fetches city suggestions based on the query using SidebarService."""
        if self.sidebar_service:
            return self.sidebar_service.search_cities_by_name(query, limit=7) # Fetch up to 7 suggestions
        return []

    def _update_suggestions_display(self, suggestions: list):
        """Updates the suggestions view with new suggestions."""
        if not self.suggestions_view:
            return

        self.suggestions_view.controls.clear()
        if suggestions:
            for city_data in suggestions:
                # city_data is expected to be a dict like: 
                # {'city': 'Rome', 'admin_name': 'Lazio', 'country': 'Italy', ...}
                city_name = city_data.get('city', 'N/A')
                admin_name = city_data.get('admin_name', '')
                country_name = city_data.get('country', '')
                
                display_text = f"{city_name}"
                if admin_name and admin_name.lower() != city_name.lower(): # Avoid "Rome, Rome"
                    display_text += f", {admin_name}"
                if country_name:
                    display_text += f" ({country_name})"

                tile = ft.ListTile(
                    title=ft.Text(display_text, size=12, color=self._text_color),
                    # MODIFIED: Make lambda async and await _select_city
                    on_click=lambda _, cn=city_name: self.page.run_task(self._select_city, cn),
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=2)
                )
                self.suggestions_view.controls.append(tile)
            self._show_suggestions()
        else:
            self._hide_suggestions()
        
        try:
            self.suggestions_view.update()
            self.update() # Update the main container to adjust size if suggestions appear/disappear
        except Exception as e:
            logging.error(f"SearchBar: Error updating suggestions display: {e}")

    def _clear_suggestions(self):
        """Clears all suggestions from the view."""
        if self.suggestions_view:
            self.suggestions_view.controls.clear()
            try:
                self.suggestions_view.update()
            except Exception as e:
                logging.error(f"SearchBar: Error clearing suggestions: {e}")

    def _show_suggestions(self):
        """Makes the suggestions view visible."""
        if self.suggestions_view:
            self.suggestions_view.visible = True
            try:
                self.suggestions_view.update()
                self.update()
            except Exception as e:
                logging.error(f"SearchBar: Error showing suggestions: {e}")

    def _hide_suggestions(self):
        """Hides the suggestions view."""
        if self.suggestions_view:
            self.suggestions_view.visible = False
            try:
                self.suggestions_view.update()
                self.update()
            except Exception as e:
                logging.error(f"SearchBar: Error hiding suggestions: {e}")

    async def _on_search_click(self, e): # MODIFIED: Added async
        """Handles the search button click event."""
        if self.search_field and self.search_field.value:
            await self._select_city(self.search_field.value.strip()) # MODIFIED: Added await

    async def _on_search_submit(self, e): # MODIFIED: Added async
        """Handles the search field submission (e.g., Enter key)."""
        if self.search_field and self.search_field.value:
            await self._select_city(self.search_field.value.strip()) # MODIFIED: Added await

    async def _select_city(self, city_name: str): # MODIFIED: Added async
        """Handles the selection of a city, either from input or suggestions."""
        logging.info(f"SearchBar: City selected: {city_name}")
        if self.on_city_selected and city_name:
            await self.on_city_selected(city_name) # MODIFIED: Added await
        self._clear_suggestions()
        self._hide_suggestions()
        if self.search_field:
            self.search_field.value = "" # Clear the search field after selection
            try:
                self.search_field.update()
            except Exception as e:
                logging.error(f"SearchBar: Error clearing search field: {e}")

    def get_value(self) -> Optional[str]:
        return self.search_field.value if self.search_field else None

    def clear_value(self):
        if self.search_field:
            self.search_field.value = ""
            self.search_field.update()
        self._clear_suggestions()
