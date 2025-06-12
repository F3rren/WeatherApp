import flet as ft
from datetime import datetime
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService

class HourlyForecastDisplay(ft.Container):
    """
    Manages the display of the entire hourly forecast section,
    including generating each item and arranging them in a scrollable row.
    Inherits from ft.Container to be a self-contained Flet component.
    """
    def __init__(self, hourly_data: list, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self._hourly_data_list = hourly_data
        self.page = page
        self._state_manager = None
        self._language = DEFAULT_LANGUAGE
        self._unit_system = DEFAULT_UNIT_SYSTEM
        self._text_color = LIGHT_THEME["TEXT"] # Default

        # Configure the container itself (e.g., expand)
        self.expand = True 
        # self.padding = ft.padding.all(5) # Example: if padding is desired for the main container

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'icon': 60, # Adjusted for a more compact hourly view
                'time': 20, # Smaller text for time
                'temp': 25, # Slightly larger for temperature
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        self._ui_elements_built = False # Flag to check if UI elements are ready for size updates

    def did_mount(self):
        """Called when the control is added to the page."""
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
            self._unit_system = self._state_manager.get_state('unit') or DEFAULT_UNIT_SYSTEM
            current_theme = self._state_manager.get_state('theme') or "light"
            self._text_color = DARK_THEME["TEXT"] if current_theme == "dark" else LIGHT_THEME["TEXT"]

            self._state_manager.register_observer("theme_event", self._handle_theme_change)
            self._state_manager.register_observer("language_event", self._handle_language_or_unit_change)
            self._state_manager.register_observer("unit_event", self._handle_language_or_unit_change)
        
        if self.page:
            self._original_on_resize = self.page.on_resize
            self.page.on_resize = self._combined_resize_handler
        
        self._request_ui_rebuild()

    def will_unmount(self):
        """Called when the control is removed from the page."""
        if self._state_manager:
            self._state_manager.unregister_observer("theme_event", self._handle_theme_change)
            self._state_manager.unregister_observer("language_event", self._handle_language_or_unit_change)
            self._state_manager.unregister_observer("unit_event", self._handle_language_or_unit_change)
        
        if self.page and hasattr(self, '_original_on_resize'):
            self.page.on_resize = self._original_on_resize

    def _build_ui_elements(self):
        """Constructs the Flet UI elements for the hourly forecast."""
        forecast_item_controls = []
        if self._hourly_data_list:
            for item_data in self._hourly_data_list:
                try:
                    time_str = datetime.strptime(item_data["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
                    icon_code = item_data["weather"][0]["icon"]
                    temp_value = round(item_data["main"]["temp"])
                    unit_symbol = TranslationService.get_unit_symbol("temperature", self._unit_system)

                    icon_image = ft.Image(
                        src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                        width=self.text_handler.get_size('icon'),
                        height=self.text_handler.get_size('icon'),
                        fit=ft.ImageFit.CONTAIN,
                        # Store category for resize updates
                        data={'type': 'icon', 'category': 'icon'} 
                    )
                    
                    time_text = ft.Text(
                        time_str,
                        size=self.text_handler.get_size('time'),
                        color=self._text_color,
                        # Store category for resize updates
                        data={'type': 'text', 'category': 'time'}
                    )
                    
                    temp_text_val = ft.Text(
                        f"{temp_value}{unit_symbol}",
                        size=self.text_handler.get_size('temp'),
                        weight=ft.FontWeight.BOLD,
                        color=self._text_color,
                        # Store category for resize updates
                        data={'type': 'text', 'category': 'temp'}
                    )

                    item_column = ft.Column(
                        controls=[icon_image, time_text, temp_text_val],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND, # Adjusted for better spacing
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5, # Spacing between elements in a single forecast item
                        # expand=True # Each item column should not expand, the Row will scroll
                    )
                    
                    # Each item is wrapped in its own container for padding/margin if needed
                    item_container = ft.Container(
                        content=item_column,
                        padding=ft.padding.symmetric(horizontal=5, vertical=10), # Padding for each item
                        margin=ft.margin.only(right=5), # Margin between items
                        # border_radius=ft.border_radius.all(10), # Optional: if items need rounded corners
                        # bgcolor=ft.colors.with_opacity(0.05, ft.colors.BLACK), # Optional: subtle background
                    )
                    forecast_item_controls.append(item_container)
                except Exception as e:
                    print(f"Error processing hourly item: {item_data}, Error: {e}")
                    # Optionally add a placeholder or error message for this item
                    forecast_item_controls.append(ft.Text("Error", color=ft.colors.RED))


        self._ui_elements_built = True # Mark UI as built
        return ft.Row(
            controls=forecast_item_controls,
            scroll=ft.ScrollMode.ADAPTIVE,
            vertical_alignment=ft.CrossAxisAlignment.START, # Align items to the top of the row
            spacing=0, # Spacing is handled by item_container margin
            # expand=True # The Row itself can expand
        )

    def _request_ui_rebuild(self):
        """Rebuilds the UI content and updates the control."""
        new_content = self._build_ui_elements()
        self.content = new_content
        if self.page:
            self.update()

    def _update_text_and_icon_sizes(self):
        """Updates sizes of text and icon elements within the content."""
        if not self._ui_elements_built or not self.content or not isinstance(self.content, ft.Row):
            return

        for item_container in self.content.controls: # ft.Row -> list of ft.Container (items)
            if isinstance(item_container, ft.Container) and isinstance(item_container.content, ft.Column):
                item_column = item_container.content
                for control in item_column.controls: # ft.Column -> list of ft.Image, ft.Text
                    if hasattr(control, 'data') and isinstance(control.data, dict):
                        category = control.data.get('category')
                        control_type = control.data.get('type')
                        if category:
                            new_size = self.text_handler.get_size(category)
                            if control_type == 'icon' and hasattr(control, 'width') and hasattr(control, 'height'):
                                control.width = new_size
                                control.height = new_size
                            elif control_type == 'text' and hasattr(control, 'size'):
                                control.size = new_size
        if self.page:
            self.update()
            
    def _handle_language_or_unit_change(self, event_data=None):
        """Handles language or unit system changes."""
        if self._state_manager:
            new_language = self._state_manager.get_state('language') or DEFAULT_LANGUAGE
            new_unit_system = self._state_manager.get_state('unit') or DEFAULT_UNIT_SYSTEM
            
            changed = False
            if self._language != new_language:
                self._language = new_language
                changed = True
            if self._unit_system != new_unit_system:
                self._unit_system = new_unit_system
                changed = True
            
            if changed:
                self._request_ui_rebuild()

    def _handle_theme_change(self, event_data=None):
        """Handles theme changes."""
        if self._state_manager:
            current_theme = self._state_manager.get_state('theme') or "light"
            new_text_color = DARK_THEME["TEXT"] if current_theme == "dark" else LIGHT_THEME["TEXT"]
            if self._text_color != new_text_color:
                self._text_color = new_text_color
                self._request_ui_rebuild() # Rebuild to apply new colors

    def _combined_resize_handler(self, e):
        """Handles page resize events."""
        self.text_handler._handle_resize(e) 
        self._update_text_and_icon_sizes() 
        if hasattr(self, '_original_on_resize') and self._original_on_resize:
            self._original_on_resize(e)

    # The old build method is no longer needed as the class itself is a container.
    # Old _update_all_item_visuals is replaced by _request_ui_rebuild and specific updates.
    # Old _determine_text_color is integrated into theme handling.
    # Old _handle_state_change is split into more specific handlers.

