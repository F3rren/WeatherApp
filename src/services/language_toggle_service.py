import logging
import flet as ft
from state_manager import StateManager
from config import DEFAULT_LANGUAGE

class LanguageToggleService:
    def __init__(self, state_manager: StateManager, page: ft.Page):
        self.state_manager = state_manager
        self.page = page # Required for potential UI updates directly or indirectly

    async def handle_language_toggle(self, selected_language_code: str) -> None:
        try:
            current_language = self.state_manager.get_state("language")
            if current_language != selected_language_code:
                await self.state_manager.set_state("language", selected_language_code)
                # Notify all components that the language has changed
                await self.state_manager.notify_all("language_changed", {"new_language": selected_language_code})
                logging.info(f"Language changed to: {selected_language_code}")
                # Potentially update the page if needed, though components should handle their own updates
                # self.page.update()
            else:
                logging.info(f"Language already set to: {selected_language_code}")
        except Exception as e:
            logging.error(f"Error in handle_language_toggle: {e}")

    async def initialize_language(self) -> None:
        try:
            # Get language from state manager, which should have a default
            # or be None if not yet set
            current_language = self.state_manager.get_state("language")
            if current_language is None:
                # If no language is in state (e.g., first run), set it from config
                await self.state_manager.set_state("language", DEFAULT_LANGUAGE)
                logging.info(f"Language initialized to default: {DEFAULT_LANGUAGE}")
                # Notify components about the initial language setting
                await self.state_manager.notify_all("language_changed", {"new_language": DEFAULT_LANGUAGE})
            else:
                # If language is already in state, ensure components are aware (e.g. on a reload)
                logging.info(f"Language already set in state: {current_language}. Ensuring components are notified.")
                await self.state_manager.notify_all("language_changed", {"new_language": current_language})

            # It might be useful to also store it in session if other non-Flet parts of app need it
            # self.page.session.set('language_code', self.state_manager.get_state("language"))
            # self.page.update()

        except Exception as e:
            logging.error(f"Error initializing language: {e}")
