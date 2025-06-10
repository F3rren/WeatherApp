import flet as ft
from datetime import datetime
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM # Added DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService # Added TranslationService

class HourlyForecastDisplay:
    """
    Manages the display of the entire hourly forecast section, 
    including generating each item and arranging them in a scrollable row.
    """
    def __init__(self, hourly_data: list, text_color: str, page: ft.Page):
        self.hourly_data_list = hourly_data
        self.initial_text_color = text_color # Store initial text color
        self.page = page
        self.built_item_containers = [] 
        self.main_container_ref = None 
        self._state_manager = None
        
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes= {
                'icon': 70,
                'title': 16,
                'value': 20,
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        self.text_controls_map = {} # Stores {control_instance: {type: 'text/icon', category: 'title/value/icon', original_data: {}}}

        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self.language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
            self.unit_system = self._state_manager.get_state('unit_system') or DEFAULT_UNIT_SYSTEM
            self.text_color = self._determine_text_color()

            self._state_manager.register_observer("theme_event", self._handle_state_change)
            self._state_manager.register_observer("language_event", self._handle_state_change) # Added
            self._state_manager.register_observer("unit_event", self._handle_state_change)   # Added
            
            original_resize_handler = self.page.on_resize
            
            def combined_resize_handler(e):
                self.text_handler._handle_resize(e)
                self._update_all_item_visuals() # Update visuals on resize
                if original_resize_handler:
                    original_resize_handler(e)
            self.page.on_resize = combined_resize_handler
        else:
            self.language = DEFAULT_LANGUAGE
            self.unit_system = DEFAULT_UNIT_SYSTEM
            self.text_color = self.initial_text_color

    def _determine_text_color(self):
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config["TEXT"]
        return self.initial_text_color

    def _handle_state_change(self, event_data=None):
        """Handles theme, language, or unit changes."""
        if self._state_manager:
            self.language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
            self.unit_system = self._state_manager.get_state('unit_system') or DEFAULT_UNIT_SYSTEM
        self.text_color = self._determine_text_color()
        self._update_all_item_visuals()

    def _update_all_item_visuals(self):
        """Updates text, color, and size for all items based on current state."""
        for item_container in self.built_item_containers:
            if hasattr(item_container, "original_data"):
                original_data = item_container.original_data
                # item_container.content is the ft.Column
                column_controls = item_container.content.controls
                weather_icon_control = column_controls[0]
                time_text_control = column_controls[1]
                temp_text_control = column_controls[2]

                # Update icon size
                weather_icon_control.width = self.text_handler.get_size('icon')
                weather_icon_control.height = self.text_handler.get_size('icon')

                # Update time text (no translation needed for HH:MM)
                time_text_control.size = self.text_handler.get_size('title')
                time_text_control.color = self.text_color

                # Update temperature text with unit
                temp_value = round(original_data["main"]["temp"])
                unit_symbol = TranslationService.get_unit_symbol("temperature", self.unit_system, self.language)
                temp_text_control.value = f"{temp_value}{unit_symbol}"
                temp_text_control.size = self.text_handler.get_size('value')
                temp_text_control.color = self.text_color
                
                if hasattr(item_container, 'page') and item_container.page: # Guard update
                    item_container.update()

    def _create_item_column(self, item_data: dict) -> ft.Container:
        """Helper method to create a single forecast item's visual representation."""
        time_str = datetime.strptime(item_data["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
        icon_code = item_data["weather"][0]["icon"]
        temp_value = round(item_data["main"]["temp"])
        unit_symbol = TranslationService.get_unit_symbol("temperature", self.unit_system, self.language)

        weather_icon = ft.Image(
            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
            width=self.text_handler.get_size('icon'),
            height=self.text_handler.get_size('icon'),
            fit=ft.ImageFit.CONTAIN
        )
        time_text = ft.Text(
            time_str, 
            size=self.text_handler.get_size('title'), 
            weight=ft.FontWeight.BOLD, 
            color=self.text_color
        )
        temp_text = ft.Text(
            f"{temp_value}{unit_symbol}", 
            size=self.text_handler.get_size('value'), 
            weight=ft.FontWeight.BOLD, 
            color=self.text_color
        )

        container = ft.Container(
            content=ft.Column(
                controls=[
                    weather_icon,
                    time_text,
                    temp_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border_radius=20,
            expand=True,
        )
        # Store original data with the container for updates
        container.original_data = item_data 
        return container

    def build(self) -> ft.Container:
        """Builds the hourly forecast container with a scrollable row of items."""
        self.built_item_containers.clear()
        if self.hourly_data_list:
            for item_data in self.hourly_data_list:
                item_container = self._create_item_column(item_data) # Sets initial visuals
                self.built_item_containers.append(item_container)
        
        self.main_container_ref = ft.Container(
            content=ft.Row(
                controls=self.built_item_containers,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            expand=True,
            padding=ft.padding.symmetric(vertical=10),
        )
        return self.main_container_ref

    def cleanup(self):
        """Unregister observers."""
        if self._state_manager:
            self._state_manager.unregister_observer("theme_event", self._handle_state_change)
            self._state_manager.unregister_observer("language_event", self._handle_state_change)
            self._state_manager.unregister_observer("unit_event", self._handle_state_change)
        # print("HourlyForecastDisplay cleaned up") # For debugging

    # Remove update_text_controls and handle_theme_change as their logic is now in _handle_state_change and _update_all_item_visuals

