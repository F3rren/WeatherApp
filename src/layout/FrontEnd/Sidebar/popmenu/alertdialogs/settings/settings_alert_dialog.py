import flet as ft
from utils.config import LIGHT_THEME, DARK_THEME
from services.translation_service import TranslationService

from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_language import DropdownLanguage
from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_measurement import DropdownMeasurement

class SettingsAlertDialog:
    """
    Versione semplificata per test dell'alert dialog delle impostazioni.
    """
    def __init__(self, page, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, text_color=None):
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.text_color = text_color if text_color else (DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"])
        self.language_dropdown = DropdownLanguage(state_manager)
        self.measurement_dropdown = DropdownMeasurement(state_manager)
        self.location_toggle = None
        self.theme_toggle = None
        self.dialog = None  # Changed from self.dlg to self.dialog
        
        # Register for theme change events if state_manager is available
        if state_manager:
            # Rimuovi eventuali registrazioni errate
            try:
                state_manager.unregister_observer("theme_event", self.handle_theme_change)
            except Exception:
                pass
            state_manager.register_observer("theme_event", self.handle_theme_event) # Correct method name

        # Language initialization
        self.language = None
        if state_manager:
            self.language = state_manager.get_state('language') or 'en'
            state_manager.register_observer("language_event", self.handle_language_change)
        else:
            self.language = 'en'

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

        # Crea il toggle switch con stile consistente con theme toggle
        self.location_toggle = ft.Switch(
            value=using_location,
            active_color=theme["ACCENT"],
            inactive_thumb_color=ft.Colors.GREY_400,
            active_track_color=ft.Colors.with_opacity(0.5, theme["ACCENT"]),
            inactive_track_color=ft.Colors.with_opacity(0.3, ft.Colors.GREY),
            on_change=self.handle_location_toggle
        )
        
        return self.location_toggle
    
    def create_theme_toggle(self):
        # Ottieni il valore corrente dallo state manager, se disponibile
        using_theme = False
        if self.state_manager:
            using_theme = self.state_manager.get_state('using_theme') or False
            
        # Determina i colori in base al tema corrente
        is_dark = False
        if self.state_manager and hasattr(self.state_manager, 'page'):
            is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME

        # Crea il toggle switch con colori migliorati che utilizzano il tema
        self.theme_toggle = ft.Switch(
            value=using_theme,
            active_color=theme["ACCENT"],
            inactive_thumb_color=ft.Colors.GREY_400,
            active_track_color=ft.Colors.with_opacity(0.5, theme["ACCENT"]),
            inactive_track_color=ft.Colors.with_opacity(0.3, ft.Colors.GREY),
            on_change=self.handle_theme_toggle
        )

        return self.theme_toggle


    def update_location_toggle(self, value):
        """Aggiorna il valore del toggle di posizione"""
        if self.location_toggle:
            self.location_toggle.value = value
            self.location_toggle.update()

    def update_theme_toggle(self, value):
        """Aggiorna il valore del toggle di tema"""
        if self.theme_toggle:
            self.theme_toggle.value = value
            self.theme_toggle.update()

    def handle_theme_event(self, event_data=None): # Renamed from handle_theme_toggle
        # Determina lo stato del tema dai dati dell'evento o dallo state_manager
        is_dark = False
        if event_data and "is_dark" in event_data:
            is_dark = event_data["is_dark"]
        elif self.state_manager and hasattr(self.state_manager, 'page'): # Ensure page attribute exists
            is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
        
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        self.text_color = current_theme["TEXT"]

        # Aggiorna l'aspetto del dialogo
        if self.dialog:
            self.dialog.bgcolor = current_theme.get("DIALOG_BACKGROUND", ft.Colors.WHITE)
            if isinstance(self.dialog.title, ft.Text):
                self.dialog.title.color = self.text_color 
            
            # Aggiorna i pulsanti nel dialogo
            if self.dialog.actions:
                for action_button in self.dialog.actions:
                    if isinstance(action_button, ft.TextButton):
                        action_button.style.color = current_theme.get("ACCENT", ft.Colors.BLUE)
                        if action_button.content and isinstance(action_button.content, ft.Text):
                             action_button.content.color = current_theme.get("ACCENT", ft.Colors.BLUE)
                    elif isinstance(action_button, ft.ElevatedButton):
                        action_button.bgcolor = current_theme.get("BUTTON_BACKGROUND", ft.Colors.BLUE)
                        if action_button.content and isinstance(action_button.content, ft.Text):
                            action_button.content.color = current_theme.get("BUTTON_TEXT", ft.Colors.WHITE)
            
            # Update text colors in the content
            if self.dialog.content and hasattr(self.dialog.content, 'content') and isinstance(self.dialog.content.content, ft.Column):
                for row in self.dialog.content.content.controls:
                    if isinstance(row, ft.Row):
                        for item in row.controls:
                            if isinstance(item, ft.Row): # Inner row with icon and text
                                for sub_item in item.controls:
                                    if isinstance(sub_item, ft.Text):
                                        sub_item.color = self.text_color
                                    elif isinstance(sub_item, ft.Icon):
                                        # Icons have custom colors, don't change them
                                        pass
                            elif isinstance(item, ft.Text): # Direct text in a row (should not happen with current structure)
                                item.color = self.text_color
            
            # Update toggles
            if self.location_toggle:
                self.location_toggle.active_color=current_theme["ACCENT"]
                self.location_toggle.active_track_color=ft.Colors.with_opacity(0.5, current_theme["ACCENT"])
                self.location_toggle.update()
            if self.theme_toggle:
                self.theme_toggle.active_color=current_theme["ACCENT"]
                self.theme_toggle.active_track_color=ft.Colors.with_opacity(0.5, current_theme["ACCENT"])
                self.theme_toggle.update()

            # Aggiorna il colore di sfondo dei dropdown
            if self.language_dropdown and hasattr(self.language_dropdown, 'dropdown'):
                if hasattr(self.language_dropdown.dropdown, 'bgcolor'):
                    self.language_dropdown.dropdown.bgcolor = current_theme.get("DIALOG_BACKGROUND", ft.Colors.WHITE)
                    self.language_dropdown.dropdown.update()
            if self.measurement_dropdown and hasattr(self.measurement_dropdown, 'dropdown'):
                if hasattr(self.measurement_dropdown.dropdown, 'bgcolor'):
                    self.measurement_dropdown.dropdown.bgcolor = current_theme.get("DIALOG_BACKGROUND", ft.Colors.WHITE)
                    self.measurement_dropdown.dropdown.update()

            self.dialog.update()

    def handle_language_change(self, event_data=None):
        if self.state_manager:
            self.language = self.state_manager.get_state('language') or 'en'
        # Aggiorna le label del dialogo
        if self.dialog:
            if isinstance(self.dialog.title, ft.Text):
                self.dialog.title.value = TranslationService.get_text("settings", self.language)
                self.dialog.title.update()
            # Aggiorna le label delle sezioni
            if self.dialog.content and hasattr(self.dialog.content, 'content') and isinstance(self.dialog.content.content, ft.Column):
                rows = self.dialog.content.content.controls
                # Language
                if len(rows) > 0 and isinstance(rows[0].controls[0].controls[1], ft.Text):
                    rows[0].controls[0].controls[1].value = TranslationService.get_text("language", self.language)
                    rows[0].controls[0].controls[1].update()
                # Measurement
                if len(rows) > 1 and isinstance(rows[1].controls[0].controls[1], ft.Text):
                    rows[1].controls[0].controls[1].value = TranslationService.get_text("measurement", self.language)
                    rows[1].controls[0].controls[1].update()
                # Use current location
                if len(rows) > 2 and isinstance(rows[2].controls[0].controls[1], ft.Text):
                    rows[2].controls[0].controls[1].value = TranslationService.get_text("use_current_location", self.language)
                    rows[2].controls[0].controls[1].update()
                # Dark theme
                if len(rows) > 3 and isinstance(rows[3].controls[0].controls[1], ft.Text):
                    rows[3].controls[0].controls[1].value = TranslationService.get_text("dark_theme", self.language)
                    rows[3].controls[0].controls[1].update()
            # Aggiorna il testo del pulsante Close
            if self.dialog.actions and len(self.dialog.actions) > 0:
                btn = self.dialog.actions[0]
                if hasattr(btn, 'content') and isinstance(btn.content, ft.Text):
                    btn.content.value = TranslationService.get_text("close", self.language)
                    btn.content.update()
        if self.dialog:
            self.dialog.update()

    def createAlertDialog(self, page):
        # Determina i colori in base al tema corrente
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        self.text_color = current_theme["TEXT"] # Ensure text_color is set based on initial theme
        # Imposta il colore di sfondo dei dropdown
        language_dropdown_control = self.language_dropdown.build()
        measurement_dropdown_control = self.measurement_dropdown.build()
        if hasattr(language_dropdown_control, 'bgcolor'):
            language_dropdown_control.bgcolor = current_theme.get("CARD_BACKGROUND", ft.Colors.WHITE)
        if hasattr(measurement_dropdown_control, 'bgcolor'):
            measurement_dropdown_control.bgcolor = current_theme.get("CARD_BACKGROUND", ft.Colors.WHITE)
        # Utilizza i colori dal tema corrente
        bg_color = current_theme["DIALOG_BACKGROUND"]

        # Dialog semplificato per test
        self.dialog = ft.AlertDialog(
            title=ft.Text(TranslationService.get_text("settings", self.language), size=20, weight=ft.FontWeight.BOLD, color=self.text_color),
            scrollable=True,
            bgcolor=bg_color,
            content=ft.Container(
                width=500,
                content=ft.Column(
                    controls=[
                        # Sezione lingua
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LANGUAGE, size=20, color="#ff6b35"),
                                        ft.Text(TranslationService.get_text("language", self.language), size=14, weight=ft.FontWeight.W_500, color=self.text_color),
                                    ],
                                    spacing=10,
                                ),
                                language_dropdown_control,
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        # Sezione unità di misura
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.STRAIGHTEN, size=20, color="#22c55e"),
                                        ft.Text(TranslationService.get_text("measurement", self.language), size=14, weight=ft.FontWeight.W_500, color=self.text_color),
                                    ],
                                    spacing=10,
                                ),
                                measurement_dropdown_control,
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        # Sezione posizione attuale
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.LOCATION_ON, size=20, color="#ef4444"),
                                        ft.Text(TranslationService.get_text("use_current_location", self.language), size=14, weight=ft.FontWeight.W_500, color=self.text_color),
                                    ],
                                    spacing=10,
                                ),
                                self.create_location_toggle(),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        # Sezione tema
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.DARK_MODE, size=20, color="#3b82f6"),
                                        ft.Text(TranslationService.get_text("dark_theme", self.language), size=14, weight=ft.FontWeight.W_500, color=self.text_color),
                                    ],
                                    spacing=10,
                                ),
                                self.create_theme_toggle(),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    height=280,
                    expand=True,
                    spacing=20,
                ),
            ),
            actions=[
                ft.TextButton(
                    TranslationService.get_text("close", self.language),
                    content=ft.Text(TranslationService.get_text("close", self.language), color=current_theme["ACCENT"]),
                    style=ft.ButtonStyle(
                        color=current_theme["ACCENT"],
                        overlay_color=ft.Colors.with_opacity(0.1, current_theme["ACCENT"]),
                    ),
                    on_click=lambda e: page.close(self.dialog)
                ),
            ],
        )
        
        # Rimosso: return ft.ElevatedButton(...)

    def build(self):
        return self.createAlertDialog(self.page)