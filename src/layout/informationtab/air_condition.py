import flet as ft
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME, DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
from services.translation_service import TranslationService
from services.api_service import ApiService
import asyncio
import logging
import traceback

def get_wind_direction_icon(wind_direction_deg):
    """
    Restituisce l'icona appropriata per la direzione del vento.
    
    Args:
        wind_direction_deg: Direzione del vento in gradi (0-360)
        
    Returns:
        Tupla (icona, descrizione) con l'icona ft.Icons e descrizione testuale
    """
    if wind_direction_deg is None:
        return ft.Icons.QUESTION_MARK, "N/A"
    
    # Normalizza i gradi a 0-360
    wind_direction_deg = wind_direction_deg % 360
    
    # Definisce le direzioni con le relative icone
    # N = 0°, NE = 45°, E = 90°, SE = 135°, S = 180°, SW = 225°, W = 270°, NW = 315°
    if wind_direction_deg >= 337.5 or wind_direction_deg < 22.5:
        return ft.Icons.NORTH, "N"
    elif 22.5 <= wind_direction_deg < 67.5:
        return ft.Icons.NORTH_EAST, "NE"
    elif 67.5 <= wind_direction_deg < 112.5:
        return ft.Icons.EAST, "E"
    elif 112.5 <= wind_direction_deg < 157.5:
        return ft.Icons.SOUTH_EAST, "SE"
    elif 157.5 <= wind_direction_deg < 202.5:
        return ft.Icons.SOUTH, "S"
    elif 202.5 <= wind_direction_deg < 247.5:
        return ft.Icons.SOUTH_WEST, "SW"
    elif 247.5 <= wind_direction_deg < 292.5:
        return ft.Icons.WEST, "W"
    elif 292.5 <= wind_direction_deg < 337.5:
        return ft.Icons.NORTH_WEST, "NW"
    else:
        return ft.Icons.QUESTION_MARK, "N/A"

class AirConditionComponent(ft.Container):
    """
    Individual air condition component for separated display.
    """
    
    def __init__(self, metric_type: str, value, unit: str = "", wind_direction: int = None, 
                 page: ft.Page = None, **kwargs):
        super().__init__(**kwargs)
        self.metric_type = metric_type
        self.value = value
        self.unit = unit
        self.wind_direction = wind_direction
        self.page = page
        
        self._state_manager = None
        self._language = DEFAULT_LANGUAGE
        self._text_color = LIGHT_THEME["TEXT"]
        
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={'title': 14, 'label': 10, 'value': 12, 'icon': 18},
            breakpoints=[600, 900, 1200, 1600]
        )
        
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._state_manager.register_observer("language_event", lambda e=None: self.page.run_task(self.update_ui, e))
            self._state_manager.register_observer("theme_event", lambda e=None: self.page.run_task(self.update_ui, e))
        
        self.content = self.build()
        # Don't auto-update on init - wait for page to be ready
    
    async def update_ui(self, event_data=None):
        """Update UI based on theme/language changes."""
        if not self.page or not self.visible:
            return
        
        try:
            if self._state_manager:
                self._language = self._state_manager.get_state('language') or self._language
            
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._text_color = theme.get("TEXT", ft.Colors.BLACK)
            
            self.content = self.build()
            try:
                self.update()
            except AssertionError:
                # Component not yet added to page, this is okay
                pass
        except Exception as e:
            logging.error(f"AirConditionComponent: Error updating UI: {e}")
    
    def build(self):
        """Build individual component based on metric type."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK if self.page else False
        
        # Get translation service
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        # Define component configurations
        components_config = {
            "feels_like": {
                "icon": ft.Icons.THERMOSTAT_OUTLINED,
                "color": ft.Colors.ORANGE_400,
                "light_bg": ft.Colors.ORANGE_50,
                "dark_bg": ft.Colors.ORANGE_900,
                "label_key": "feels_like"
            },
            "humidity": {
                "icon": ft.Icons.WATER_DROP_OUTLINED,
                "color": ft.Colors.BLUE_400,
                "light_bg": ft.Colors.BLUE_50,
                "dark_bg": ft.Colors.BLUE_900,
                "label_key": "humidity"
            },
            "wind": {
                "icon": ft.Icons.AIR,
                "color": ft.Colors.TEAL_400,
                "light_bg": ft.Colors.TEAL_50,
                "dark_bg": ft.Colors.TEAL_900,
                "label_key": "wind"
            },
            "pressure": {
                "icon": ft.Icons.COMPRESS_OUTLINED,
                "color": ft.Colors.PURPLE_400,
                "light_bg": ft.Colors.PURPLE_50,
                "dark_bg": ft.Colors.PURPLE_900,
                "label_key": "pressure"
            },
            "visibility": {
                "icon": ft.Icons.VISIBILITY_OUTLINED,
                "color": ft.Colors.CYAN_400,
                "light_bg": ft.Colors.CYAN_50,
                "dark_bg": ft.Colors.CYAN_900,
                "label_key": "visibility"
            },
            "uv_index": {
                "icon": ft.Icons.WB_SUNNY_OUTLINED,
                "color": ft.Colors.YELLOW_600,
                "light_bg": ft.Colors.YELLOW_50,
                "dark_bg": ft.Colors.YELLOW_900,
                "label_key": "uv_index"
            },
            "dew_point": {
                "icon": ft.Icons.WATER_OUTLINED,
                "color": ft.Colors.INDIGO_400,
                "light_bg": ft.Colors.INDIGO_50,
                "dark_bg": ft.Colors.INDIGO_900,
                "label_key": "dew_point"
            },
            "cloud_coverage": {
                "icon": ft.Icons.CLOUD_OUTLINED,
                "color": ft.Colors.GREY_600,
                "light_bg": ft.Colors.GREY_50,
                "dark_bg": ft.Colors.GREY_800,
                "label_key": "cloud_coverage"
            }
        }
        
        config = components_config.get(self.metric_type, components_config["feels_like"])
        
        # Get translated label
        label_text = self.metric_type
        if translation_service:
            label_text = translation_service.translate_from_dict(
                "air_condition_items", 
                config["label_key"],
                self._language
            ) or self.metric_type
        
        # Icon with background
        icon_container = ft.Container(
            content=ft.Icon(
                config["icon"],
                size=20,
                color=config["color"]
            ),
            bgcolor=config["light_bg"] if not is_dark else config["dark_bg"],
            padding=10,
            border_radius=10,
        )
        
        # Value and unit
        value_text = ft.Text(
            f"{self.value}{self.unit}",
            size=self._text_handler.get_size('value'),
            weight=ft.FontWeight.BOLD,
            color=self._text_color,
        )
        
        # Label
        label_text_widget = ft.Text(
            label_text.title(),
            size=self._text_handler.get_size('label'),
            color=ft.Colors.with_opacity(0.7, self._text_color),
            weight=ft.FontWeight.W_500,
        )
        
        # Special handling for wind direction
        additional_info = None
        if self.metric_type == "wind" and self.wind_direction is not None:
            wind_icon, wind_desc = get_wind_direction_icon(self.wind_direction)
            additional_info = ft.Row([
                ft.Icon(
                    wind_icon,
                    size=12,
                    color=config["color"]
                ),
                ft.Text(
                    f"{wind_desc} ({self.wind_direction}°)",
                    size=8,
                    color=ft.Colors.with_opacity(0.8, self._text_color),
                )
            ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)
        
        # Build content based on layout
        content_items = [
            ft.Row([
                icon_container,
                ft.Container(width=8),
                ft.Column([
                    value_text,
                    label_text_widget,
                ], spacing=1, alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.START)
        ]
        
        if additional_info:
            content_items.append(ft.Container(height=4))
            content_items.append(additional_info)
        
        return ft.Container(
            content=ft.Column(content_items, spacing=4),
            bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE if not is_dark else ft.Colors.BLACK),
            border=ft.border.all(
                1,
                ft.Colors.with_opacity(0.1, ft.Colors.GREY_400 if not is_dark else ft.Colors.GREY_600)
            ),
            border_radius=12,
            padding=12,
            margin=2,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            ink=True,
        )


class AirConditionInfo(ft.Container):
    """
    Air condition information display with separated components.
    """

    def __init__(self, city: str, feels_like: int, humidity: int, wind_speed: int,
                 pressure: int, wind_direction: int = None, wind_gust: float = None, 
                 visibility: int = None, uv_index: float = None, dew_point: int = None, 
                 cloud_coverage: int = None, page: ft.Page = None, **kwargs):
        super().__init__(**kwargs)
        self._city = city
        self._feels_like_data = feels_like
        self._humidity_data = humidity
        self._wind_speed_data = wind_speed
        self._wind_direction_data = wind_direction  # Aggiungiamo la direzione del vento
        self._wind_gust_data = wind_gust  # Aggiungiamo le raffiche di vento
        self._pressure_data = pressure
        self._visibility_data = visibility
        self._uv_index_data = uv_index
        self._dew_point_data = dew_point
        self._cloud_coverage_data = cloud_coverage
        self.page = page
        
        self._state_manager = None
        self._language = DEFAULT_LANGUAGE
        self._unit_system = DEFAULT_UNIT_SYSTEM
        self._text_color = LIGHT_THEME["TEXT"]
        self.padding = 20
        self._api_service = ApiService()

        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 24, 'label': 16, 'value': 16, 'icon': 20,
            },
            breakpoints=[600, 900, 1200, 1600]
        )

        if self.page:
            if hasattr(self.page, 'session') and self.page.session.get('state_manager'):
                self._state_manager = self.page.session.get('state_manager')
                self._state_manager.register_observer("language_event", lambda e=None: self.page.run_task(self.update_ui, e))
                self._state_manager.register_observer("unit_event", lambda e=None: self.page.run_task(self.update_ui, e))
                self._state_manager.register_observer("theme_event", lambda e=None: self.page.run_task(self.update_ui, e))

            original_on_resize = self.page.on_resize
            def resize_handler(e):
                if original_on_resize:
                    original_on_resize(e)
                if self._text_handler:
                    self._text_handler._handle_resize(e)
                if self.page:
                    self.page.run_task(self.update_ui)
            self.page.on_resize = resize_handler

        self.content = self.build()
        # Don't auto-update on init - wait for page to be ready

    async def update_ui(self, event_data=None):
        """Updates the UI based on state changes, fetching new data if necessary."""
        if not self.page or not self.visible:
            return

        try:
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._language
                new_unit_system = self._state_manager.get_state('unit') or self._unit_system
                
                unit_changed = self._unit_system != new_unit_system

                self._language = new_language
                self._unit_system = new_unit_system

                # Only fetch new data if unit system changed (language doesn't affect weather data)
                if unit_changed:
                    weather_data = await asyncio.to_thread(
                        self._api_service.get_weather_data,
                        city=self._city, language=self._language, unit=self._unit_system
                    )
                    if weather_data:
                        self._feels_like_data = self._api_service.get_feels_like_temperature(weather_data)
                        self._humidity_data = self._api_service.get_humidity(weather_data)
                        self._wind_speed_data = self._api_service.get_wind_speed(weather_data)
                        self._wind_direction_data = self._api_service.get_wind_direction(weather_data)
                        self._wind_gust_data = self._api_service.get_wind_gust(weather_data)
                        self._pressure_data = self._api_service.get_pressure(weather_data)
                        self._visibility_data = self._api_service.get_visibility(weather_data)
                        self._uv_index_data = self._api_service.get_uv_index(weather_data)
                        self._dew_point_data = self._api_service.get_dew_point(weather_data)
                        self._cloud_coverage_data = self._api_service.get_cloud_coverage(weather_data)

            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._text_color = theme.get("TEXT", ft.Colors.BLACK)

            # Always rebuild content for translations/theme changes
            self.content = self.build()
            try:
                self.update()
            except AssertionError:
                # Component not yet added to page, this is okay
                pass
        except Exception as e:
            logging.error(f"AirConditionInfo: Error updating UI: {e}\n{traceback.format_exc()}")

    def build(self):
        """Create individual air condition components for separated display."""
        # This method now returns None as we'll use get_separated_components()
        # to get individual components for the layout
        return ft.Container(visible=False)
    
    def get_separated_components(self):
        """
        Returns grouped air condition components as separate containers.
        Groups related metrics together for better organization.
        """
        # Get unit symbols
        temp_unit = TranslationService.get_unit_symbol("temperature", self._unit_system)
        wind_unit = TranslationService.get_unit_symbol("wind", self._unit_system)
        pressure_unit = TranslationService.get_unit_symbol("pressure", self._unit_system)
        
        # Get translation service
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        def get_translated_label(key):
            if translation_service:
                return translation_service.translate_from_dict(
                    "air_condition_items", key, self._language
                ) or key.replace('_', ' ').title()
            return key.replace('_', ' ').title()
        
        # Create grouped components
        components = {}
        
        # Temperature Group (Feels Like + Dew Point)
        temperature_metrics = []
        if self._feels_like_data is not None:
            temperature_metrics.append({
                'label': get_translated_label('feels_like'),
                'label_key': 'feels_like',  # Store the key for re-translation
                'value': self._feels_like_data,
                'unit': temp_unit
            })
        if self._dew_point_data is not None:
            temperature_metrics.append({
                'label': get_translated_label('dew_point'),
                'label_key': 'dew_point',  # Store the key for re-translation
                'value': self._dew_point_data,
                'unit': temp_unit
            })
        
        if temperature_metrics:
            components["temperature"] = AirConditionGroupComponent(
                group_type="temperature",
                metrics=temperature_metrics,
                page=self.page
            )
        
        # Humidity & Air Group (Humidity + Cloud Coverage)
        humidity_air_metrics = []
        if self._humidity_data is not None:
            humidity_air_metrics.append({
                'label': get_translated_label('humidity'),
                'label_key': 'humidity',  # Store the key for re-translation
                'value': self._humidity_data,
                'unit': '%'
            })
        if self._cloud_coverage_data is not None:
            humidity_air_metrics.append({
                'label': get_translated_label('cloud_coverage'),
                'label_key': 'cloud_coverage',  # Store the key for re-translation
                'value': self._cloud_coverage_data,
                'unit': '%'
            })
        
        if humidity_air_metrics:
            components["humidity_air"] = AirConditionGroupComponent(
                group_type="humidity_air",
                metrics=humidity_air_metrics,
                page=self.page
            )
        
        # Wind Group (Wind Speed + Direction + Gust)
        wind_metrics = []
        
        # 1. Wind Speed (Vento)
        if self._wind_speed_data is not None:
            wind_metrics.append({
                'label': get_translated_label('wind'),
                'label_key': 'wind',  # Store the key for re-translation
                'value': self._wind_speed_data,
                'unit': f' {wind_unit}'
            })
        
        # 2. Wind Direction (Angolazione)
        if self._wind_direction_data is not None:
            wind_icon, wind_desc = get_wind_direction_icon(self._wind_direction_data)
            wind_metrics.append({
                'label': get_translated_label('wind_direction'),
                'label_key': 'wind_direction',  # Store the key for re-translation
                'value': f"{wind_desc}",  # Show direction description
                'unit': f" {self._wind_direction_data}°",  # Show degrees as unit
                'wind_icon': wind_icon,  # Pass the wind direction icon
                'wind_desc': wind_desc,  # Pass the wind direction description
                'wind_direction': self._wind_direction_data  # Pass the wind direction degrees
            })
        
        # 3. Wind Gust (Raffica)
        if self._wind_gust_data is not None:
            wind_metrics.append({
                'label': get_translated_label('wind_gust'),
                'label_key': 'wind_gust',  # Store the key for re-translation
                'value': round(self._wind_gust_data, 1),  # Round to 1 decimal place
                'unit': f' {wind_unit}'
            })
        
        if wind_metrics:
            components["wind"] = AirConditionGroupComponent(
                group_type="wind",
                metrics=wind_metrics,
                page=self.page
            )
        
        # Atmospheric Group (Pressure + Visibility)
        atmospheric_metrics = []
        if self._pressure_data is not None:
            atmospheric_metrics.append({
                'label': get_translated_label('pressure'),
                'label_key': 'pressure',  # Store the key for re-translation
                'value': self._pressure_data,
                'unit': f' {pressure_unit}'
            })
        if self._visibility_data is not None:
            atmospheric_metrics.append({
                'label': get_translated_label('visibility'),
                'label_key': 'visibility',  # Store the key for re-translation
                'value': self._visibility_data,
                'unit': ' m'
            })
        
        if atmospheric_metrics:
            components["atmospheric"] = AirConditionGroupComponent(
                group_type="atmospheric",
                metrics=atmospheric_metrics,
                page=self.page
            )
        
        # Solar Group (UV Index)
        solar_metrics = []
        if self._uv_index_data is not None:
            solar_metrics.append({
                'label': get_translated_label('uv_index'),
                'label_key': 'uv_index',  # Store the key for re-translation
                'value': round(self._uv_index_data, 1),
                'unit': ''
            })
        
        if solar_metrics:
            components["solar"] = AirConditionGroupComponent(
                group_type="solar",
                metrics=solar_metrics,
                page=self.page
            )
        
        return components

class AirConditionGroupComponent(ft.Container):
    """
    Group component that contains multiple related air condition metrics.
    """
    
    def __init__(self, group_type: str, metrics: list, page: ft.Page = None, **kwargs):
        super().__init__(**kwargs)
        self.group_type = group_type
        self.metrics = metrics  # List of dictionaries with metric data
        self.page = page
        
        self._state_manager = None
        self._language = DEFAULT_LANGUAGE
        self._text_color = LIGHT_THEME["TEXT"]
        
        self._text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={'title': 14, 'label': 10, 'value': 12, 'icon': 18},
            breakpoints=[600, 900, 1200, 1600]
        )
        
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._state_manager.register_observer("language_event", lambda e=None: self.page.run_task(self.update_ui, e))
            self._state_manager.register_observer("theme_event", lambda e=None: self.page.run_task(self.update_ui, e))
        
        self.content = self.build()
        # Don't auto-update on init - wait for page to be ready
    
    async def update_ui(self, event_data=None):
        """Update UI based on theme/language changes."""
        if not self.page or not self.visible:
            return
        
        try:
            if self._state_manager:
                self._language = self._state_manager.get_state('language') or self._language
            
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._text_color = theme.get("TEXT", ft.Colors.BLACK)
            
            self.content = self.build()
            try:
                self.update()
            except AssertionError:
                # Component not yet added to page, this is okay
                pass
        except Exception as e:
            logging.error(f"AirConditionGroupComponent: Error updating UI: {e}")
    
    def build(self):
        """Build group component with multiple metrics."""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK if self.page else False
        
        # Get translation service
        translation_service = None
        if self.page and hasattr(self.page, 'session'):
            translation_service = self.page.session.get('translation_service')
        
        # Helper function to re-translate labels dynamically
        def get_translated_label(key):
            if translation_service:
                return translation_service.translate_from_dict(
                    "air_condition_items", key, self._language
                ) or key.replace('_', ' ').title()
            return key.replace('_', ' ').title()
        
        # Define group configurations
        group_configs = {
            "temperature": {
                "title": "Temperature",
                "icon": ft.Icons.THERMOSTAT_OUTLINED,
                "color": ft.Colors.ORANGE_400,
                "light_bg": ft.Colors.ORANGE_50,
                "dark_bg": ft.Colors.ORANGE_900,
            },
            "humidity_air": {
                "title": "Humidity & Air",
                "icon": ft.Icons.WATER_DROP_OUTLINED,
                "color": ft.Colors.BLUE_400,
                "light_bg": ft.Colors.BLUE_50,
                "dark_bg": ft.Colors.BLUE_900,
            },
            "wind": {
                "title": "Wind",
                "icon": ft.Icons.AIR,
                "color": ft.Colors.TEAL_400,
                "light_bg": ft.Colors.TEAL_50,
                "dark_bg": ft.Colors.TEAL_900,
            },
            "atmospheric": {
                "title": "Atmospheric",
                "icon": ft.Icons.COMPRESS_OUTLINED,
                "color": ft.Colors.PURPLE_400,
                "light_bg": ft.Colors.PURPLE_50,
                "dark_bg": ft.Colors.PURPLE_900,
            },
            "solar": {
                "title": "Solar",
                "icon": ft.Icons.WB_SUNNY_OUTLINED,
                "color": ft.Colors.YELLOW_600,
                "light_bg": ft.Colors.YELLOW_50,
                "dark_bg": ft.Colors.YELLOW_900,
            }
        }
        
        config = group_configs.get(self.group_type, group_configs["temperature"])
        
        # Build metrics list with dynamic label translation
        metrics_widgets = []
        for metric in self.metrics:
            if metric.get('value') is not None:
                # Re-translate label based on current language
                label_key = metric.get('label_key', metric.get('label', '').lower().replace(' ', '_'))
                
                # Get translated label directly using the stored label_key
                translated_label = get_translated_label(label_key)
                
                # Create value text and additional elements
                value_elements = [
                    ft.Text(
                        f"{metric['value']}{metric.get('unit', '')}",
                        size=self._text_handler.get_size('value'),
                        weight=ft.FontWeight.BOLD,
                        color=self._text_color,
                    )
                ]
                
                # Add wind direction icon and angle if available
                if metric.get('wind_icon') and metric.get('wind_desc'):
                    value_elements.append(
                        ft.Container(width=8)  # Small spacing
                    )
                    value_elements.append(
                        ft.Icon(
                            metric['wind_icon'],
                            size=16,
                            color=config.get("color", ft.Colors.TEAL_400),
                        )
                    )
                    
                
                # Create individual metric row
                metric_row = ft.Row([
                    ft.Text(
                        f"{translated_label}:",
                        size=self._text_handler.get_size('label'),
                        color=ft.Colors.with_opacity(0.7, self._text_color),
                        weight=ft.FontWeight.W_500,
                        width=80,
                    ),
                    ft.Row(
                        value_elements,
                        spacing=0,
                        alignment=ft.MainAxisAlignment.END
                    )
                ], spacing=8, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                
                metrics_widgets.append(metric_row)
        
        if not metrics_widgets:
            return ft.Container(
                content=ft.Text("No data available", size=12),
                height=80,
                alignment=ft.alignment.center
            )
        
        # Group title
        title_text = config["title"]
        if translation_service:
            try:
                translated_title = translation_service.translate_from_dict(
                    "air_condition_items", 
                    f"{self.group_type}_group",
                    self._language
                )
                if translated_title:
                    title_text = translated_title
                else:
                    # Debug: log if translation not found
                    logging.debug(f"Translation not found for {self.group_type}_group in language {self._language}")
            except Exception as e:
                logging.error(f"Error translating group title: {e}")
        else:
            logging.debug(f"Translation service not available for group {self.group_type}")
        
        return ft.Container(
            content=ft.Column([
                # Group header with icon
                ft.Container(
                    content=ft.Row([
                        ft.Icon(
                            config["icon"],
                            size=18,
                            color=config["color"]
                        ),
                        ft.Container(width=6),  # Small spacing
                        ft.Text(
                            title_text,
                            size=self._text_handler.get_size('title'),
                            weight=ft.FontWeight.BOLD,
                            color=config["color"],
                        )
                    ], alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.only(bottom=8),
                ),
                # Metrics
                ft.Column(
                    metrics_widgets,
                    spacing=6,
                )
            ], spacing=4),
            bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE if not is_dark else ft.Colors.BLACK),
            border=ft.border.all(
                1,
                ft.Colors.with_opacity(0.1, config["color"])
            ),
            border_radius=12,
            padding=16,
            margin=2,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
