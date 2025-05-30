import flet as ft

class TranslatorService:
    """
    Service for managing translations in the application.
    This service handles the translation of text based on the selected language.
    It can be extended to support multiple languages and dynamic updates.
    """

    def __init__(self, page: ft.Page):
        self.page = page
        
