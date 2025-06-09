# filepath: c:\Users\Utente\Desktop\Progetti\Python\MeteoApp\src\layout\frontend\sidebar\popmenu\alertdialogs\settings\dropdowns\dropdown_measurement.py
import flet as ft
from utils.config import MEASUREMENT_UNITS, LIGHT_THEME, DARK_THEME

class DropdownMeasurement:

    def __init__(self, state_manager=None):
        self.selected_unit = None
        self.state_manager = state_manager
        self.dropdown = None
        # Sistemi di misura disponibili
        self.units = MEASUREMENT_UNITS
        # Mappiamo i nomi ai codici per l'API
        self.unit_labels = {unit["code"]: unit["name"] for unit in MEASUREMENT_UNITS}
        
        # Register for theme change events if state_manager is available
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_change)

    def get_options(self, theme=None):
        # Accept theme so we can set the correct color for option content
        if theme is None:
            is_dark = False
            if self.state_manager and hasattr(self.state_manager, 'page'):
                is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
        options = []
        for unit in self.units:
            code = unit["code"]
            name = unit["name"]
            options.append(
                ft.dropdown.Option(
                    key=code,
                    text=name,
                    content=ft.Text(
                        value=name,
                        color=theme["TEXT"]
                    ),
                )
            )
        return options
    
    def createDropdown(self):
        def dropdown_changed(e):
            unit_code = e.control.value
            self.set_unit(unit_code)
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        current_unit = "metric"
        if self.state_manager:
            current_unit = self.state_manager.get_state('unit') or "metric"
            self.selected_unit = current_unit

        is_dark = False
        if self.state_manager and hasattr(self.state_manager, 'page'):
            is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
        theme = DARK_THEME if is_dark else LIGHT_THEME

        dropdown = ft.Dropdown(
            autofocus=True,
            hint_text="Select measurement system",
            options=self.get_options(theme),
            on_change=dropdown_changed,
            expand=True,
            value=current_unit,
            border_width=2,
            border_color=theme["BORDER"],
            focused_border_color=theme["ACCENT"],
            focused_border_width=2,
            bgcolor=theme["CARD_BACKGROUND"],
            color=theme["TEXT"],
            content_padding=ft.padding.all(8),
        )
        # Imposta label_style e hint_style come nel dropdown lingua
        if dropdown.hint_style is None:
            dropdown.hint_style = ft.TextStyle()
        dropdown.hint_style.color = theme.get("SECONDARY_TEXT", ft.Colors.GREY_700)
        if dropdown.label_style is None:
            dropdown.label_style = ft.TextStyle()
        dropdown.label_style.color = theme.get("SECONDARY_TEXT", ft.Colors.GREY_700)
        self.dropdown = dropdown
        return dropdown

    def set_unit(self, unit_code):
        self.selected_unit = unit_code
        
        # Aggiorna lo stato dell'applicazione se state_manager è disponibile
        if self.state_manager:
            import asyncio
            
            # Funzione wrapper per gestire chiamate asincrone in modo sicuro
            def call_async_safely(coro):
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                if not loop.is_running():
                    return loop.run_until_complete(coro)
                else:
                    return asyncio.create_task(coro)
            
            # Aggiorna lo stato con la nuova unità di misura
            call_async_safely(self.state_manager.set_state("unit", unit_code))
            print(f"State updated with unit: {unit_code}")

    def handle_theme_change(self, event_data=None):
        """Handle theme change events by updating the dropdown appearance"""
        if self.dropdown and self.state_manager:
            is_dark = False
            if event_data and "is_dark" in event_data:
                is_dark = event_data["is_dark"]
            elif hasattr(self.state_manager, 'page'):  # Fallback
                is_dark = self.state_manager.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self.dropdown.border_color = theme.get("BORDER", ft.Colors.BLACK)
            self.dropdown.focused_border_color = theme.get("ACCENT", ft.Colors.BLUE)
            self.dropdown.bgcolor = theme.get("CARD_BACKGROUND", ft.Colors.WHITE)
            self.dropdown.color = theme.get("TEXT", ft.Colors.BLACK)
            # Imposta label_style e hint_style come nel dropdown lingua
            if self.dropdown.hint_style is None:
                self.dropdown.hint_style = ft.TextStyle()
            self.dropdown.hint_style.color = theme.get("SECONDARY_TEXT", ft.Colors.GREY_700)
            if self.dropdown.label_style is None:
                self.dropdown.label_style = ft.TextStyle()
            self.dropdown.label_style.color = theme.get("SECONDARY_TEXT", ft.Colors.GREY_700)
            self.dropdown.options = self.get_options(theme)
            self.dropdown.update()

    def get_selected_unit(self):
        return self.selected_unit

    def build(self):
        self.dropdown = self.createDropdown()
        return self.dropdown
