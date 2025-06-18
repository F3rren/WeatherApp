import flet as ft
from utils.config import DARK_THEME, LIGHT_THEME

from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_language import DropdownLanguage
from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_measurement import DropdownMeasurement
from components.responsive_text_handler import ResponsiveTextHandler

class MapsAlertDialog:
    def __init__(self, page, state_manager=None, translation_service=None, handle_location_toggle=None, handle_theme_toggle=None, text_color=None):
        self.page = page
        self.state_manager = state_manager
        self.translation_service = translation_service or (page.session.get('translation_service') if page else None)
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.text_color = text_color if text_color else (DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"])
        self.language_dropdown = DropdownLanguage(state_manager)
        self.measurement_dropdown = DropdownMeasurement(state_manager)
        self.location_toggle = None
        self.theme_toggle = None
        self.dialog = None
        
        # Initialize ResponsiveTextHandler
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
        
        # Register as observer for responsive updates
        self.text_handler.add_observer(self.update_text_controls)
        
        # Register for theme change events if state_manager is available
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_event)

    def update_text_controls(self):
        """Update text sizes for all registered controls"""
        for control, size_category in self.text_controls.items():
            if size_category == 'icon':
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
            else:
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
        
        # Request page update
        if self.page and self.dialog and self.dialog.page:
            self.dialog.update()

    def _get_translation(self, key):
        """Helper method to get translation with fallback"""
        if self.translation_service and hasattr(self.translation_service, 'translate'):
            current_language = self.state_manager.get_state("language") if self.state_manager else "en"
            return self.translation_service.translate(key, current_language)
        return key  # Fallback to key if no translation service

    def create_location_toggle(self):
        # Ottieni il valore corrente dallo state manager, se disponibile
        using_location = False
        if self.state_manager:
            using_location = self.state_manager.get_state('using_location') or False
            
        # Determina i colori in base al tema corrente
        is_dark = False
        if self.state_manager and hasattr(self.state_manager, 'page'):
            is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME
        
        from layout.frontend.sidebar.popmenu.alertdialogs.settings.location_toggle import LocationToggle
        
        self.location_toggle = LocationToggle(
            on_change=self.handle_location_toggle,
            value=using_location,
            page=self.page  # Pass page for ResponsiveTextHandler
        )
        
        return ft.Row([
            ft.Text(self._get_translation("use_current_location_setting"), size=self.text_handler.get_size('body'), color=self.text_color),
            self.location_toggle.build()
        ])
    
    def create_theme_toggle(self):
        # Ottieni il valore corrente dallo state manager, se disponibile
        using_dark_theme = False
        if self.state_manager:
            using_dark_theme = (self.state_manager.get_state('theme') == "dark") or False
            
        # Determina i colori in base al tema corrente
        is_dark = False
        if self.state_manager and hasattr(self.state_manager, 'page'):
            is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME

        from layout.frontend.sidebar.popmenu.alertdialogs.settings.theme_toggle import ThemeToggle
        
        self.theme_toggle = ThemeToggle(
            on_change=self.handle_theme_toggle,
            value=using_dark_theme,
            page=self.page  # Pass page for ResponsiveTextHandler
        )
        
        return ft.Row([
            ft.Text(self._get_translation("dark_theme_setting"), size=self.text_handler.get_size('body'), color=self.text_color),
            self.theme_toggle.build()
        ])

    def update_location_toggle(self, value):
        """Update the value of the location toggle"""
        if self.location_toggle:
            self.location_toggle._value = value
            if hasattr(self.location_toggle, 'switch') and self.location_toggle.switch:
                self.location_toggle.switch.value = value
                if self.location_toggle.switch.page:
                    self.location_toggle.switch.update()

    def update_theme_toggle(self, value):
        """Update the value of the theme toggle"""
        if self.theme_toggle:
            self.theme_toggle._value = value
            if hasattr(self.theme_toggle, 'switch') and self.theme_toggle.switch:
                self.theme_toggle.switch.value = value
                if self.theme_toggle.switch.page:
                    self.theme_toggle.switch.update()

    def handle_theme_event(self, event_data=None):
        """Handle theme change events by updating colors"""
        if not hasattr(self, 'page') or not self.page:
            return
            
        # Update text color
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        self.text_color = DARK_THEME["TEXT"] if is_dark else LIGHT_THEME["TEXT"]
        
        # Force a rebuild of the dialog if it exists
        if self.dialog:
            self.dialog.bgcolor = DARK_THEME["DIALOG_BACKGROUND"] if is_dark else LIGHT_THEME["DIALOG_BACKGROUND"]
            
            # Update dialog title if present
            if hasattr(self.dialog, 'title') and self.dialog.title:
                if hasattr(self.dialog.title, 'color'):
                    self.dialog.title.color = self.text_color
                    
            self.dialog.update()

    def createAlertDialog(self, page):
        """Create the maps alert dialog"""
        # Reset text controls dictionary before rebuilding
        self.text_controls = {}
        
        # Determina i colori in base al tema corrente
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        self.text_color = current_theme["TEXT"]
        
        # Utilizza i colori dal tema corrente
        bg_color = current_theme["DIALOG_BACKGROUND"]
        
        # Creare i controlli di testo con dimensioni responsive
        title_text = ft.Text(
            self._get_translation("maps"),
            size=self.text_handler.get_size('title'),
            weight=ft.FontWeight.BOLD, 
            color=self.text_color
        )
        
        # Register controls in text_controls dictionary
        self.text_controls[title_text] = 'title'

        # Dialog per le impostazioni
        self.dialog = ft.AlertDialog(
            title=title_text,
            bgcolor=bg_color,
            content=ft.Container(
                width=400,
                content=ft.Column(
                    controls=[
                        ft.Text("Maps content goes here", size=self.text_handler.get_size('body'), color=self.text_color),
                    ],
                    spacing=20,
                    height=200,
                ),
            ),
            actions=[
                ft.TextButton(
                    self._get_translation("close_button"),
                    on_click=lambda e: page.close(self.dialog)
                ),
            ],
            on_dismiss=lambda e: print("Maps dialog closed"),
        )
        
        return self.dialog
        
    def cleanup(self):
        """Cleanup method to remove observers"""
        if hasattr(self, 'text_handler') and self.text_handler:
            self.text_handler.remove_observer(self.update_text_controls)
        
        if self.state_manager:
            self.state_manager.unregister_observer("theme_event", self.handle_theme_event)
