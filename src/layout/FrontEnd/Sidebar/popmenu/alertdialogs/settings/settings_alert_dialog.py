import flet as ft
from config import LIGHT_THEME, DARK_THEME

from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_language import DropdownLanguage
from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_measurement import DropdownMeasurement

class SettingsAlertDialog:
    """
    Versione semplificata per test dell'alert dialog delle impostazioni.
    """
    def __init__(self, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None):
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.language_dropdown = DropdownLanguage(state_manager)
        self.measurement_dropdown = DropdownMeasurement(state_manager)
        self.location_toggle = None
        self.theme_toggle = None
        self.dlg = None
        
        # Register for theme change events if state_manager is available
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_toggle)

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

    def handle_theme_toggle(self, event_data=None):
        # Determina lo stato del tema dai dati dell'evento o dallo state_manager
        is_dark = False
        if event_data and "is_dark" in event_data:
            is_dark = event_data["is_dark"]
        elif self.state_manager and hasattr(self.state_manager, 'page'):
            is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
        
        theme = DARK_THEME if is_dark else LIGHT_THEME

        # Aggiorna l'aspetto del dialogo
        if self.dialog:
            self.dialog.bgcolor = theme.get("DIALOG_BACKGROUND", ft.colors.WHITE)
            # Assicurati che title sia un ft.Text per poter impostare il colore
            if isinstance(self.dialog.title, ft.Text):
                self.dialog.title.color = theme.get("DIALOG_TEXT", ft.colors.BLACK)
            
            # Aggiorna i pulsanti nel dialogo
            if self.dialog.actions:
                for action_button in self.dialog.actions:
                    if isinstance(action_button, ft.TextButton):
                        # Per TextButton, potresti voler cambiare il colore del testo
                        if action_button.content and isinstance(action_button.content, ft.Text):
                            action_button.content.color = theme.get("ACCENT", ft.colors.BLUE) # Esempio
                    elif isinstance(action_button, ft.ElevatedButton):
                        action_button.bgcolor = theme.get("BUTTON_BACKGROUND", ft.colors.BLUE)
                        if action_button.content and isinstance(action_button.content, ft.Text):
                            action_button.content.color = theme.get("BUTTON_TEXT", ft.colors.WHITE)
            self.dialog.update()

    def createAlertDialog(self, page):
        # Determina i colori in base al tema corrente
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME
        
        # Utilizza i colori dal tema corrente
        bg_color = theme["DIALOG_BACKGROUND"]
        text_color = theme["TEXT"]

        # Dialog semplificato per test
        self.dlg = ft.AlertDialog(
            title=ft.Text("Settings", size=20, weight=ft.FontWeight.BOLD, color=text_color),
            bgcolor=bg_color,
            content=ft.Container(
                width=400,  # Imposta una larghezza fissa per il dialogo
                content=ft.Column(
                controls=[
                    # Sezione lingua
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.LANGUAGE, size=20, color=theme["ICON"]),
                                    ft.Text("Language:", size=14, weight=ft.FontWeight.W_500, color=text_color),
                                ],
                                spacing=10,
                            ),
                            self.language_dropdown.build(),
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
                                    ft.Icon(ft.Icons.STRAIGHTEN, size=20, color=theme["ICON"]),
                                    ft.Text("Measurement:", size=14, weight=ft.FontWeight.W_500, color=text_color),
                                ],
                                spacing=10,
                            ),
                            self.measurement_dropdown.build(),
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
                                    ft.Icon(ft.Icons.LOCATION_ON, size=20, color=theme["ICON"]),
                                    ft.Text("Use current location:", size=14, weight=ft.FontWeight.W_500, color=text_color),
                                ],
                                spacing=10,
                            ),
                            self.create_location_toggle(),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.DARK_MODE, size=20, color=theme["ICON"]),
                                    ft.Text("Dark theme:", size=14, weight=ft.FontWeight.W_500, color=text_color),
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
                height=280,  # Aumentata per ospitare comodamente i quattro controlli
                expand=True,
                spacing=20,
            ),
            ),
            actions=[
                ft.TextButton(
                    "Close",
                    style=ft.ButtonStyle(
                        color=theme["ACCENT"],
                        overlay_color=ft.Colors.with_opacity(0.1, theme["ACCENT"]),
                    ),
                    on_click=lambda e: page.close(self.dlg)
                ),
            ],
            on_dismiss=lambda e: print("Dialog closed"),
        )
        
        # Pulsante semplificato per aprire il dialog
        return ft.ElevatedButton(
            text="Settings",
            icon=ft.Icons.SETTINGS,
            icon_color=theme["ICON"],
            bgcolor=theme["BUTTON_BACKGROUND"],
            color=theme["BUTTON_TEXT"],
            on_click=lambda e: page.open(self.dlg),
        )