import flet as ft
from config import LIGHT_THEME, DARK_THEME

class WeatherAlertDialog:
        
    def __init__(self, page, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, text_color=None):
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.text_color = text_color if text_color else (DARK_THEME["TEXT"] if page.theme_mode == ft.ThemeMode.DARK else LIGHT_THEME["TEXT"])
        self.dialog = None  # Changed from self.dlg to self.dialog for consistency

 
    def createAlertDialog(self, page):
        # Determina i colori in base al tema corrente
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        current_theme = DARK_THEME if is_dark else LIGHT_THEME
        self.text_color = current_theme["TEXT"] # Ensure text_color is set based on initial theme
        
        # Utilizza i colori dal tema corrente
        bg_color = current_theme["DIALOG_BACKGROUND"]

        # Dialog semplificato per test
        self.dialog = ft.AlertDialog( # Changed from self.dlg to self.dialog
            title=ft.Text("Weather", size=20, weight=ft.FontWeight.BOLD, color=self.text_color),
            bgcolor=bg_color,
            content=ft.Container(
                width=400,  # Imposta una larghezza fissa per il dialogo
                content=ft.Column(
                controls=[
                    # Sezione lingua
                    ft.Row(
                        controls=[
                            ft.Row(                                controls=[
                                    ft.Icon(ft.Icons.LANGUAGE, size=20, color="#ff6b35"),  # Arancione personalizzato
                                    ft.Text("Language:", size=14, weight=ft.FontWeight.W_500, color=self.text_color),
                                ],
                                spacing=10,
                            ),
                            #self.language_dropdown.build(),
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
                            #self.measurement_dropdown.build(),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    # Sezione posizione attuale
                    ft.Row(
                        controls=[
                            ft.Row(                                controls=[
                                    ft.Icon(ft.Icons.LOCATION_ON, size=20, color="#ef4444"),  # Rosso personalizzato
                                    ft.Text("Use current location:", size=14, weight=ft.FontWeight.W_500, color=self.text_color),
                                ],
                                spacing=10,
                            ),
                            #self.create_location_toggle(),
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
                            #self.create_theme_toggle(),
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