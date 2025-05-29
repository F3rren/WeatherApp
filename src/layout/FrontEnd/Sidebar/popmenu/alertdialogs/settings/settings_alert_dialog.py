import flet as ft
from config import LIGHT_THEME, DARK_THEME

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
        self.dialog = None  # Changed from self.dlg to self.dialog for consistency
        
        # Register for theme change events if state_manager is available
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_event) # Renamed for clarity

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
            self.dialog.bgcolor = current_theme.get("DIALOG_BACKGROUND", ft.colors.WHITE)
            if isinstance(self.dialog.title, ft.Text):
                self.dialog.title.color = self.text_color 
            
            # Aggiorna i pulsanti nel dialogo
            if self.dialog.actions:
                for action_button in self.dialog.actions:
                    if isinstance(action_button, ft.TextButton):
                        action_button.style.color = current_theme.get("ACCENT", ft.colors.BLUE)
                        if action_button.content and isinstance(action_button.content, ft.Text):
                             action_button.content.color = current_theme.get("ACCENT", ft.colors.BLUE)
                    elif isinstance(action_button, ft.ElevatedButton):
                        action_button.bgcolor = current_theme.get("BUTTON_BACKGROUND", ft.colors.BLUE)
                        if action_button.content and isinstance(action_button.content, ft.Text):
                            action_button.content.color = current_theme.get("BUTTON_TEXT", ft.colors.WHITE)
            
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
                                        sub_item.color = current_theme.get("ICON")
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

            self.dialog.update()

    def createAlertDialog(self, page):
        # Determina i colori in base al tema corrente
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        self.text_color = current_theme["TEXT"] # Ensure text_color is set based on initial theme
        
        # Utilizza i colori dal tema corrente
        bg_color = current_theme["DIALOG_BACKGROUND"]

        # Dialog semplificato per test
        self.dialog = ft.AlertDialog( # Changed from self.dlg to self.dialog
            title=ft.Text("Settings", size=20, weight=ft.FontWeight.BOLD, color=self.text_color),
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
                                    ft.Icon(ft.Icons.LANGUAGE, size=20, color=current_theme["ICON"]),
                                    ft.Text("Language:", size=14, weight=ft.FontWeight.W_500, color=self.text_color),
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
                                    ft.Icon(ft.Icons.STRAIGHTEN, size=20, color=current_theme["ICON"]),
                                    ft.Text("Measurement:", size=14, weight=ft.FontWeight.W_500, color=self.text_color),
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
                                    ft.Icon(ft.Icons.LOCATION_ON, size=20, color=current_theme["ICON"]),
                                    ft.Text("Use current location:", size=14, weight=ft.FontWeight.W_500, color=self.text_color),
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
                                    ft.Icon(ft.Icons.DARK_MODE, size=20, color=current_theme["ICON"]),
                                    ft.Text("Dark theme:", size=14, weight=ft.FontWeight.W_500, color=self.text_color),
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
                    content=ft.Text("Close", color=current_theme["ACCENT"]), # Ensure text color is applied
                    style=ft.ButtonStyle(
                        color=current_theme["ACCENT"],
                        overlay_color=ft.Colors.with_opacity(0.1, current_theme["ACCENT"]),
                    ),
                    on_click=lambda e: page.close(self.dialog) # Changed from self.dlg to self.dialog
                ),
            ],
            on_dismiss=lambda e: print("Dialog closed"),
        )
        
        # Pulsante semplificato per aprire il dialog
        return ft.ElevatedButton( 
            text="Settings",
            icon=ft.Icons.SETTINGS,
            icon_color=current_theme["ICON"], # Uncommented and uses current_theme
            bgcolor=current_theme["BUTTON_BACKGROUND"], # Uncommented and uses current_theme
            color=current_theme["BUTTON_TEXT"], # Uncommented and uses current_theme
            on_click=lambda e: page.open(self.dialog), 
        )