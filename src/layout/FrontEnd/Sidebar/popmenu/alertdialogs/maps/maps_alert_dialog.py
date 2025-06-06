import flet as ft
from utils.config import DARK_THEME, LIGHT_THEME

from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_language import DropdownLanguage
from layout.frontend.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_measurement import DropdownMeasurement

class MapsAlertDialog:
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
        bg_color = current_theme["DIALOG_BACKGROUND"]        # Dialog semplificato per test
        self.dialog = ft.AlertDialog( # Changed from self.dlg to self.dialog
            title=ft.Text("Maps", size=20, weight=ft.FontWeight.BOLD, color=self.text_color),
            bgcolor=bg_color,
            content=ft.Container(
                width=400,  # Imposta una larghezza fissa per il dialogo
                content=ft.Column(
                controls=[                    # Sezione lingua
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.LANGUAGE, size=20, color="#ff6b35"),  # Arancione personalizzato
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
                                    ft.Icon(ft.Icons.STRAIGHTEN, size=20, color="#22c55e"),  # Verde personalizzato
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
                                    ft.Icon(ft.Icons.LOCATION_ON, size=20, color="#ef4444"),  # Rosso personalizzato
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
                                    ft.Icon(ft.Icons.DARK_MODE, size=20, color="#3b82f6"),  # Blu personalizzato
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