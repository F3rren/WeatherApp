from services.ui.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE
from services.ui.theme_handler import ThemeHandler
from ui.components.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from ui.components.sidebar.popmenu.alertdialogs.maps.advanced_maps_alert_dialog import AdvancedMapsAlertDialog
from ui.components.sidebar.popmenu.alertdialogs.maps.interactive.interactive_maps_alert_dialog import InteractiveMapAlertDialog
from ui.components.sidebar.popmenu.alertdialogs.maps.satellite_view_dialog import SatelliteViewDialog
from ui.components.sidebar.popmenu.alertdialogs.maps.radar_live_dialog import RadarLiveDialog
from ui.components.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog
from ui.components.sidebar.popmenu.alertdialogs.analytics.weather_trends_dialog import WeatherTrendsDialog
from ui.components.sidebar.popmenu.alertdialogs.analytics.historical_data_dialog import HistoricalDataDialog
from ui.components.sidebar.popmenu.alertdialogs.alerts.push_notifications_dialog import PushNotificationsDialog
from ui.components.sidebar.popmenu.alertdialogs.tools.location_manager_dialog import LocationManagerDialog
from ui.components.sidebar.popmenu.alertdialogs.tools.export_data_dialog import ExportDataDialog
import flet as ft


class PopMenu(ft.Container):
    def __init__(self, page: ft.Page = None, state_manager=None, 
                 handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_toggle_value=False, location_toggle_value=False, 
                 language: str = None, theme_handler: ThemeHandler = None, **kwargs):
        super().__init__(**kwargs)
        print(f"DEBUG: PopMenu.__init__ chiamato con page={page}")
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.location_toggle_value = location_toggle_value
        self.theme_handler = theme_handler or ThemeHandler(page)
        self.language = language if language else DEFAULT_LANGUAGE
        self.weather_alert = None
        self.advanced_maps_alert = None
        self.interactive_maps_alert = None
        self.satellite_view_dialog = None
        self.radar_live_dialog = None
        self.weather_trends_dialog = None
        self.historical_data_dialog = None
        self.push_notifications_dialog = None
        self.location_manager_dialog = None
        self.export_data_dialog = None
        self.setting_alert = None
        self.pop_menu_items = None
        self.popup_menu_button_icon = None
        print(f"DEBUG: Prima di update_ui, self.page={self.page}")
        self.update_ui()
        # NON rimuovere la creazione dell'icona del menu!
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)
        
        # Imposta il contenuto del container con l'icona del menu
        self.content = self.build()

    def update_ui(self, event_data=None):
        """Update theme, language, text sizes, and rebuild UI."""
        print(f"DEBUG: update_ui chiamato, self.page={self.page}")
        self._current_text_color = self.theme_handler.get_text_color() if self.theme_handler else "black"
        self.language = self.state_manager.get_state('language') if self.state_manager else DEFAULT_LANGUAGE

        # Update child dialogs, passing theme_handler for color logic
        self.weather_alert = WeatherAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        
        self.advanced_maps_alert = AdvancedMapsAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language, theme_handler=self.theme_handler)
        
        self.interactive_maps_alert = InteractiveMapAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language, theme_handler=self.theme_handler)
        
        # Initialize all dialogs
        self.satellite_view_dialog = SatelliteViewDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.radar_live_dialog = RadarLiveDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.weather_trends_dialog = WeatherTrendsDialog(page=self.page)
        self.historical_data_dialog = HistoricalDataDialog(page=self.page)
        self.push_notifications_dialog = PushNotificationsDialog(page=self.page)
        self.location_manager_dialog = LocationManagerDialog(page=self.page)
        self.export_data_dialog = ExportDataDialog(page=self.page)
        self.setting_alert = SettingsAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language, theme_handler=self.theme_handler, handle_location_toggle=self.handle_location_toggle, handle_theme_toggle=self.handle_theme_toggle)

        # Create popup menu items text
        self.pop_menu_items = {
            "weather": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "weather", self.language), color=self._current_text_color),
            "maps": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "maps", self.language), color=self._current_text_color),
            "advanced_maps": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "advanced_maps", self.language), color=self._current_text_color),
            "interactive_maps": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "interactive_maps", self.language), color=self._current_text_color),
            "satellite_view": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "satellite_view", self.language), color=self._current_text_color),
            "radar_live": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "radar_live", self.language), color=self._current_text_color),
            "analytics": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "analytics", self.language), color=self._current_text_color),
            "weather_trends": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "weather_trends", self.language), color=self._current_text_color),
            "historical_data": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "historical_data", self.language), color=self._current_text_color),
            "alerts": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "alerts", self.language), color=self._current_text_color),
            "push_notifications": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "push_notifications", self.language), color=self._current_text_color),
            "tools": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "tools", self.language), color=self._current_text_color),
            "location_manager": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "location_manager", self.language), color=self._current_text_color),
            "export_data": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "export_data", self.language), color=self._current_text_color),
            "settings": ft.Text(value=TranslationService.translate_from_dict("popup_menu_items", "settings", self.language), color=self._current_text_color)
        }
        
        # Aggiorna il contenuto del container se già inizializzato
        if hasattr(self, 'content') and self.content is not None:
            self.content = self.build()
            if self.page:
                self.page.update()

    def build(self):
        """Build the frontend component using MenuBar with native SubmenuButton."""
        
        # IMPORTANTE: Creazione MenuBar con sottomenu nativi
        menubar = ft.MenuBar(
            expand=True,
            controls=[
                ft.SubmenuButton(
                    content=ft.Icon(ft.Icons.MENU, color=self._current_text_color, size=24),
                    controls=[
                        # Meteo - item diretto
                        ft.MenuItemButton(
                            content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "weather", self.language)),
                            leading=ft.Icon(ft.Icons.SUNNY, color="#FF8C00", size=20),
                            on_click=lambda _: self.weather_alert.show_dialog() if self.weather_alert else None,
                        ),
                        # Mappe - sottomenu
                        ft.SubmenuButton(
                            content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "maps", self.language)),
                            leading=ft.Icon(ft.Icons.MAP, color="#2196F3", size=20),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "advanced_maps", self.language)),
                                    leading=ft.Icon(ft.Icons.LAYERS_OUTLINED, color="#4CAF50", size=20),
                                    on_click=lambda _: self.advanced_maps_alert.open_dialog() if self.advanced_maps_alert else None,
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "interactive_maps", self.language)),
                                    leading=ft.Icon(ft.Icons.MAP, color="#2196F3", size=20),
                                    on_click=lambda _: self.interactive_maps_alert.open_dialog() if self.interactive_maps_alert else None,
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "satellite_view", self.language)),
                                    leading=ft.Icon(ft.Icons.SATELLITE_ALT, color="#607D8B", size=20),
                                    on_click=lambda _: self.satellite_view_dialog.show_dialog() if self.satellite_view_dialog else None,
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "radar_live", self.language)),
                                    leading=ft.Icon(ft.Icons.RADAR, color="#E91E63", size=20),
                                    on_click=lambda _: self.radar_live_dialog.show_dialog() if self.radar_live_dialog else None,
                                ),
                            ],
                        ),
                        # Analisi - sottomenu
                        ft.SubmenuButton(
                            content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "analytics", self.language)),
                            leading=ft.Icon(ft.Icons.ANALYTICS, color="#9C27B0", size=20),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "weather_trends", self.language)),
                                    leading=ft.Icon(ft.Icons.TRENDING_UP, color="#4CAF50", size=20),
                                    on_click=lambda _: self.weather_trends_dialog.show_dialog() if self.weather_trends_dialog else None,
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "historical_data", self.language)),
                                    leading=ft.Icon(ft.Icons.HISTORY, color="#795548", size=20),
                                    on_click=lambda _: self.historical_data_dialog.show_dialog() if self.historical_data_dialog else None,
                                ),
                            ],
                        ),
                        # Avvisi - sottomenu
                        ft.SubmenuButton(
                            content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "alerts", self.language)),
                            leading=ft.Icon(ft.Icons.WARNING, color="#FF5722", size=20),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "push_notifications", self.language)),
                                    leading=ft.Icon(ft.Icons.NOTIFICATIONS, color="#FF9800", size=20),
                                    on_click=lambda _: self.push_notifications_dialog.show_dialog() if self.push_notifications_dialog else None,
                                ),
                            ],
                        ),
                        # Strumenti - sottomenu
                        ft.SubmenuButton(
                            content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "tools", self.language)),
                            leading=ft.Icon(ft.Icons.BUILD, color="#607D8B", size=20),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "location_manager", self.language)),
                                    leading=ft.Icon(ft.Icons.LOCATION_ON, color="#E91E63", size=20),
                                    on_click=lambda _: self.location_manager_dialog.show_dialog() if self.location_manager_dialog else None,
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "export_data", self.language)),
                                    leading=ft.Icon(ft.Icons.DOWNLOAD, color="#3F51B5", size=20),
                                    on_click=lambda _: self.export_data_dialog.show_dialog() if self.export_data_dialog else None,
                                ),
                            ],
                        ),
                        # Impostazioni - item diretto
                        ft.MenuItemButton(
                            content=ft.Text(TranslationService.translate_from_dict("popup_menu_items", "settings", self.language)),
                            leading=ft.Icon(ft.Icons.SETTINGS, color="#808080", size=20),
                            on_click=lambda _: self.setting_alert.open_dialog() if self.setting_alert else None,
                        ),
                    ],
                )
            ],
        )
        
        return menubar

    def cleanup(self):
        """Cleanup observers and resources."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
            self.state_manager.unregister_observer("theme_event", self.update_ui)

    def _determine_text_color_from_theme(self):
        """Returns the full theme dictionary based on the current page theme."""
        if not self.page:
            return "black"
        return "white" if self.page.theme_mode == ft.ThemeMode.DARK else "black"
