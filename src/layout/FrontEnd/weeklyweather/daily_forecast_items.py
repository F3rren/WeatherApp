import flet as ft
from config import LIGHT_THEME, DARK_THEME

class DailyForecastItems:
    """
    An item displaying daily forecast information.
    """
    
    def __init__(self, day: str, icon_code: str, description: str, 
                 temp_min: int, temp_max: int, text_color: str, page: ft.Page = None):
        self.day = day
        self.icon_code = icon_code
        self.description = description
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.text_color = text_color
        self.page = page

        self.day_text = ft.Text(
            self.day, 
            size=20, 
            weight="bold", 
            width=100,
            text_align=ft.TextAlign.START,
            color=self.text_color
        )
        self.description_text = ft.Text(
            self.description.upper(), 
            size=20,
            weight="bold", 
            text_align=ft.TextAlign.START,
            color=self.text_color
        )
        self.temp_span_min = ft.TextSpan(
            f"{self.temp_min}°",
            ft.TextStyle(
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE, # Keep specific Colors for min/max temp for now
            )
        )
        self.temp_span_separator = ft.TextSpan(" / ",
            ft.TextStyle(
                size=20,
                weight=ft.FontWeight.BOLD,
                color=self.text_color # Separator should follow theme
            )
        )
        self.temp_span_max = ft.TextSpan(
            f"{self.temp_max}°",
            ft.TextStyle(
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED, # Keep specific Colors for min/max temp for now
            )
        )
        self.temperature_text = ft.Text(
            spans=[
                self.temp_span_min,
                self.temp_span_separator,
                self.temp_span_max,
            ],
            expand=True,
            text_align=ft.TextAlign.END
        )

        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                state_manager.register_observer("theme_event", self.handle_theme_change)

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]

            if hasattr(self, 'day_text'):
                self.day_text.color = self.text_color
                if self.day_text.page:
                    self.day_text.update()
            
            if hasattr(self, 'description_text'):
                self.description_text.color = self.text_color
                if self.description_text.page:
                    self.description_text.update()

            if hasattr(self, 'temp_span_separator'):
                 self.temp_span_separator.style.color = self.text_color
                 # We need to update the parent Text control for TextSpan changes to be visible
                 if hasattr(self, 'temperature_text') and self.temperature_text.page:
                     self.temperature_text.update()

    def build(self) -> ft.Row:
        """Build the daily forecast item"""
        return ft.Row(
            controls=[
                self.day_text,
                ft.Container(
                    content=ft.Image(
                        src=f"https://openweathermap.org/img/wn/{self.icon_code}@4x.png",
                        width=80,
                        height=80,
                    ),
                    expand=True,
                    alignment=ft.alignment.center
                ),
                self.description_text,
                self.temperature_text
            ],
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
