import flet as ft
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
import logging

class AirConditionInfo(ft.Container):
    """
    Air condition information display.
    """

    def __init__(self, feels_like: int, humidity: int, wind_speed: int,
                 pressure: int, page: ft.Page = None, **kwargs):
        super().__init__(**kwargs)
        self._feels_like_data = feels_like
        self._humidity_data = humidity
        self._wind_speed_data = wind_speed
        self._pressure_data = pressure
        self.page = page
        self.state_manager = None
        self._language = DEFAULT_LANGUAGE
        self._unit_system = DEFAULT_UNIT_SYSTEM
        self._text_color = LIGHT_THEME["TEXT"] # Default to light theme text color
        self.padding = 20 # Moved from build method

        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 24,
                'label': 16,
                'value': 16,
                'icon': 20,
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        self.text_controls = {} # To store controls for responsive updates
        self._ui_elements_initialized = False

    def did_mount(self):
        """
        Called when the control is added to the page.
        """
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self.state_manager = self.page.session.get('state_manager')
            self._language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            self._unit_system = self.state_manager.get_state('unit') or "metric"
            current_theme = self.state_manager.get_state('theme') or "light"
            self._text_color = DARK_THEME["TEXT"] if current_theme == "dark" else LIGHT_THEME["TEXT"]
            
            self.state_manager.register_observer("language_event", self._handle_language_or_unit_change)
            self.state_manager.register_observer("unit_event", self._handle_language_or_unit_change)
            self.state_manager.register_observer("unit_text_change", self._handle_language_or_unit_change)
            self.state_manager.register_observer("theme_event", self._handle_theme_change)
        
        if self.page:
            self._original_on_resize = self.page.on_resize
            self.page.on_resize = self._combined_resize_handler
        
        self._request_ui_rebuild()

    def will_unmount(self):
        """
        Called when the control is removed from the page.
        """
        if self.state_manager:
            self.state_manager.unregister_observer("theme_event", self._handle_theme_change)
            self.state_manager.unregister_observer("language_event", self._handle_language_or_unit_change)
            self.state_manager.unregister_observer("unit_event", self._handle_language_or_unit_change)
        
        if self.page and hasattr(self, '_original_on_resize'):
            self.page.on_resize = self._original_on_resize

    def _determine_text_color_from_theme(self):
        """Determines text color based on the current page theme."""
        if self.page and self.page.theme_mode:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            return current_theme_config.get("TEXT", LIGHT_THEME["TEXT"]) # Fallback to light theme text
        return LIGHT_THEME["TEXT"] # Default if page or theme_mode not set

    def _build_ui_elements(self):
        """
        Constructs the Flet UI elements for air condition information.
        """
        self.text_controls = {} # Reset for rebuild

        title_text = ft.Text(
            value=TranslationService.translate("air_condition_title", self._language),
            size=self.text_handler.get_size('title'),
            weight="bold",
            color=self._text_color
        )
        self.text_controls[title_text] = 'title'
        divider = ft.Divider(height=1, color=self._text_color)

        # Feels Like
        feels_like_icon = ft.Icon(ft.Icons.THERMOSTAT, size=self.text_handler.get_size('icon'), color=self._text_color)
        self.text_controls[feels_like_icon] = 'icon'
        
        feels_like_label_text = ft.Text(
            value=TranslationService.translate("feels_like", self._language),
            size=self.text_handler.get_size('label'),
            weight=ft.FontWeight.BOLD,
            color=self._text_color
        )
        self.text_controls[feels_like_label_text] = 'label'
        feels_like_label = ft.Row(controls=[feels_like_icon, feels_like_label_text])
        
        temp_unit_symbol = TranslationService.get_unit_symbol("temperature", self._unit_system)
        feels_like_value = ft.Text(
            value=f"{self._feels_like_data}{temp_unit_symbol}",
            size=self.text_handler.get_size('value'),
            italic=True,
            color=self._text_color
        )
        self.text_controls[feels_like_value] = 'value'

        # Humidity
        humidity_icon = ft.Icon(ft.Icons.WATER_DROP, size=self.text_handler.get_size('icon'), color=self._text_color)
        self.text_controls[humidity_icon] = 'icon'
        humidity_label_text = ft.Text(
            value=TranslationService.translate("humidity", self._language),
            size=self.text_handler.get_size('label'),
            weight=ft.FontWeight.BOLD,
            color=self._text_color
        )
        self.text_controls[humidity_label_text] = 'label'
        humidity_label = ft.Row(controls=[humidity_icon, humidity_label_text])
        humidity_value = ft.Text(
            value=f"{self._humidity_data}%",
            size=self.text_handler.get_size('value'),
            italic=True,
            color=self._text_color
        )
        self.text_controls[humidity_value] = 'value'

        # Wind
        wind_icon = ft.Icon(ft.Icons.WIND_POWER, size=self.text_handler.get_size('icon'), color=self._text_color)
        self.text_controls[wind_icon] = 'icon'
        wind_label_text = ft.Text(
            value=TranslationService.translate("wind", self._language),
            size=self.text_handler.get_size('label'),
            weight=ft.FontWeight.BOLD,
            color=self._text_color
        )
        self.text_controls[wind_label_text] = 'label'
        wind_label = ft.Row(controls=[wind_icon, wind_label_text])
        
        wind_unit_symbol = TranslationService.get_unit_symbol("wind", self._unit_system)
        wind_value = ft.Text(
            value=f"{self._wind_speed_data} {wind_unit_symbol}",
            size=self.text_handler.get_size('value'),
            italic=True,
            color=self._text_color
        )
        self.text_controls[wind_value] = 'value'

        # Pressure
        pressure_icon = ft.Icon(ft.Icons.COMPRESS, size=self.text_handler.get_size('icon'), color=self._text_color)
        self.text_controls[pressure_icon] = 'icon'
        pressure_label_text = ft.Text(
            value=TranslationService.translate("pressure", self._language),
            size=self.text_handler.get_size('label'),
            weight=ft.FontWeight.BOLD,
            color=self._text_color
        )
        self.text_controls[pressure_label_text] = 'label'
        pressure_label = ft.Row(controls=[pressure_icon, pressure_label_text])

        pressure_unit_symbol = TranslationService.get_unit_symbol("pressure", self._unit_system)
        pressure_value = ft.Text(
            value=f"{self._pressure_data} {pressure_unit_symbol}",
            size=self.text_handler.get_size('value'),
            italic=True,
            color=self._text_color
        )
        self.text_controls[pressure_value] = 'value'
        
        self._ui_elements_initialized = True

        return ft.Column(
            controls=[
                title_text,
                divider,
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                feels_like_label,
                                feels_like_value,
                                humidity_label,
                                humidity_value,
                            ],
                            expand=True,
                        ),
                        ft.Column(
                            controls=[
                                wind_label,
                                wind_value,
                                pressure_label,
                                pressure_value,
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )

    def _safe_update(self):
        if getattr(self, "page", None) and getattr(self, "visible", True):
            self.update()
            

    def _request_ui_rebuild(self):
        """
        Rebuilds the UI content and updates the control.
        """
        self._text_color = self._determine_text_color_from_theme() # Update text color before rebuilding
        new_content = self._build_ui_elements()
        self.content = new_content
        self._safe_update()

    def _update_text_and_icon_sizes(self):
        if not self._ui_elements_initialized:
            return
        for control, size_category in self.text_controls.items():
            new_size = self.text_handler.get_size(size_category)
            if hasattr(control, 'size'):
                control.size = new_size
            elif hasattr(control, 'style') and hasattr(control.style, 'size'): # For TextSpans
                control.style.size = new_size
        self._safe_update()

    def _update_text_elements(self, event_type=None, data=None):
        """Updates all text elements without comparing current values."""
        if not self._ui_elements_initialized or not self.content:
            return

        if event_type == "unit_text_change" and data:
            self._unit_system = data
        elif event_type == "language_change" and data:
            self._language = data

        # Update title
        if self.content.controls and isinstance(self.content.controls[0], ft.Text):
            title = self.content.controls[0]
            title.value = TranslationService.translate("air_condition_title", self._language)
            title.update()

        # Update data columns
        if len(self.content.controls) >= 3 and isinstance(self.content.controls[2], ft.Row):
            data_row = self.content.controls[2]
            for column in data_row.controls:
                if isinstance(column, ft.Column):
                    for control in column.controls:
                        if isinstance(control, ft.Row):  # Labels with icons
                            for text in control.controls:
                                if isinstance(text, ft.Text):
                                    if text.value in [
                                        TranslationService.translate("feels_like", self._language),
                                        TranslationService.translate("humidity", self._language),
                                        TranslationService.translate("wind", self._language),
                                        TranslationService.translate("pressure", self._language)
                                    ]:
                                        text.value = TranslationService.translate(text.value, self._language)
                                        text.update()
                        elif isinstance(control, ft.Text):  # Values
                            if "°" in control.value:  # Temperature
                                unit = TranslationService.get_unit_symbol("temperature", self._unit_system)
                                control.value = f"{self._feels_like_data}{unit}"
                            elif "%" in control.value:  # Humidity
                                control.value = f"{self._humidity_data}%"
                            elif "m/s" in control.value or "mph" in control.value:  # Wind
                                unit = TranslationService.get_unit_symbol("wind", self._unit_system)
                                control.value = f"{self._wind_speed_data} {unit}"
                            elif "hPa" in control.value:  # Pressure
                                unit = TranslationService.get_unit_symbol("pressure", self._unit_system)
                                control.value = f"{self._pressure_data} {unit}"
                            control.update()

        self._safe_update()

    def _handle_language_or_unit_change(self, event_data=None):
        """Handles language or unit changes."""
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_language_or_unit_change received unexpected event_data type: {type(event_data)}")

        if self.state_manager:
            new_language = self.state_manager.get_state('language') or DEFAULT_LANGUAGE
            new_unit_system = self.state_manager.get_state('unit') or "metric"

            # Update language and unit system
            language_changed = self._language != new_language
            unit_changed = self._unit_system != new_unit_system

            self._language = new_language
            self._unit_system = new_unit_system

            # Rebuild UI if language or unit system changes
            if language_changed or unit_changed:
                self._request_ui_rebuild()

    def _handle_theme_change(self, event_data=None):
        if event_data is not None and not isinstance(event_data, dict):
            logging.warning(f"_handle_theme_change received unexpected event_data type: {type(event_data)}")
        self._request_ui_rebuild() # Rebuild UI with new colors

    def _combined_resize_handler(self, e):
        self.text_handler._handle_resize(e) # Update base sizes in handler
        self._update_text_and_icon_sizes() # Apply new sizes to controls
        if hasattr(self, '_original_on_resize') and self._original_on_resize:
            self._original_on_resize(e)

    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati"""
        for control, size_category in self.text_controls.items():
            if size_category == 'icon':
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
            else:
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
                elif hasattr(control, 'style') and hasattr(control.style, 'size'):
                    control.style.size = self.text_handler.get_size(size_category)
                if hasattr(control, 'spans'):
                    for span in control.spans:
                        span.style.size = self.text_handler.get_size(size_category)

    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text and divider colors."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]
            for control, _ in self.text_controls.items():
                if hasattr(control, 'color'):
                    control.color = self.text_color
            if hasattr(self.divider, 'color'):
                self.divider.color = self.text_color
            self._update_all_text_elements()
