from services.ui.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE
from services.ui.theme_handler import ThemeHandler
from ui.components.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from ui.components.sidebar.popmenu.alertdialogs.maps.advanced_maps_alert_dialog import AdvancedMapsAlertDialog
from ui.components.sidebar.popmenu.alertdialogs.maps.interactive.interactive_maps_alert_dialog import InteractiveMapAlertDialog
from ui.components.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog
from ui.components.sidebar.popmenu.placeholders.placeholder_dialogs import (
    SatelliteViewDialog, RadarLiveDialog, WeatherTrendsDialog, 
    HistoricalDataDialog, PushNotificationsDialog, LocationManagerDialog, ExportDataDialog
)
import flet as ft


class PopMenu(ft.Container):
    def __init__(self, page: ft.Page = None, state_manager=None, 
                 handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_toggle_value=False, location_toggle_value=False, 
                 language: str = None, theme_handler: ThemeHandler = None, **kwargs):
        super().__init__(**kwargs)
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
        self.popup_menu_button_control = None
        self.update_ui()
        self.content = self.build()
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)

    def update_ui(self, event_data=None):
        """Update theme, language, text sizes, and rebuild UI."""
        self._current_text_color = self.theme_handler.get_text_color() if self.theme_handler else "black"
        self.language = self.state_manager.get_state('language') if self.state_manager else DEFAULT_LANGUAGE

        # Update child dialogs, passing theme_handler for color logic
        self.weather_alert = WeatherAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        
        self.advanced_maps_alert = AdvancedMapsAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language, theme_handler=self.theme_handler)
        
        self.interactive_maps_alert = InteractiveMapAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language, theme_handler=self.theme_handler)
        
        # Initialize placeholder dialogs
        self.satellite_view_dialog = SatelliteViewDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.radar_live_dialog = RadarLiveDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.weather_trends_dialog = WeatherTrendsDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.historical_data_dialog = HistoricalDataDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.push_notifications_dialog = PushNotificationsDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.location_manager_dialog = LocationManagerDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.export_data_dialog = ExportDataDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        
        self.setting_alert = SettingsAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language, 
                                                 handle_location_toggle=self.handle_location_toggle, handle_theme_toggle=self.handle_theme_toggle, 
                                                 theme_toggle_value=self.theme_toggle_value, location_toggle_value=self.location_toggle_value)

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
        self.popup_menu_button_icon = ft.Icon(ft.Icons.FILTER_ALT_OUTLINED, color=self._current_text_color)

    def build(self):
        """Build the frontend component."""
        def build_popup_menu_items():
            return [
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SUNNY, color="#FF8C00", size=20),
                        self.pop_menu_items["weather"]
                    ]),
                    on_click=lambda _, al=self.weather_alert: self.weather_alert.show_dialog(),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.MAP, color="#2196F3", size=20),
                        ft.Text(f"{TranslationService.translate_from_dict('popup_menu_items', 'maps', self.language)} ▶", color=self._current_text_color)
                    ]),
                    on_click=self._show_maps_submenu,
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ANALYTICS, color="#9C27B0", size=20),
                        ft.Text(f"{TranslationService.translate_from_dict('popup_menu_items', 'analytics', self.language)} ▶", color=self._current_text_color)
                    ]),
                    on_click=self._show_analytics_submenu,
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.WARNING, color="#FF5722", size=20),
                        ft.Text(f"{TranslationService.translate_from_dict('popup_menu_items', 'alerts', self.language)} ▶", color=self._current_text_color)
                    ]),
                    on_click=self._show_alerts_submenu,
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.BUILD, color="#607D8B", size=20),
                        ft.Text(f"{TranslationService.translate_from_dict('popup_menu_items', 'tools', self.language)} ▶", color=self._current_text_color)
                    ]),
                    on_click=self._show_tools_submenu,
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SETTINGS, color="#808080", size=20),
                        self.pop_menu_items["settings"]
                    ]),
                    on_click=lambda _, al=self.setting_alert: self.setting_alert.show_dialog(),
                ),
            ]
        
        self.popup_menu_button_control = ft.PopupMenuButton(
            content=ft.Icon(ft.Icons.MENU, color=self._current_text_color, size=20),
            items=build_popup_menu_items(),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )
        return self.popup_menu_button_control

    def _show_maps_submenu(self, e):
        """Show maps submenu dialog."""
        if not self.page:
            return
        
        # Chiudi il menu principale
        if hasattr(self, 'popup_menu_button_control'):
            self.popup_menu_button_control.open = False
            self.page.update()
        
        # Crea dialog semplice per le mappe
        maps_dialog = ft.AlertDialog(
            modal=True,
            scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.MAP, color="#2196F3", size=24),
                ft.Text(TranslationService.translate_from_dict("popup_menu_items", "maps", self.language), 
                       weight=ft.FontWeight.BOLD, size=18, color=self._current_text_color)
            ], spacing=10),
            content=ft.Container(
                width=350,
                height=200,
                content=ft.Column([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.LAYERS_OUTLINED, color="#4CAF50"),
                            ft.Text(TranslationService.translate_from_dict("popup_menu_items", "advanced_maps", self.language), size=14)
                        ], spacing=10),
                        on_click=lambda _: self._handle_maps_choice("advanced"),
                        width=300,
                        height=45
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.MAP, color="#2196F3"),
                            ft.Text(TranslationService.translate_from_dict("popup_menu_items", "interactive_maps", self.language), size=14)
                        ], spacing=10),
                        on_click=lambda _: self._handle_maps_choice("interactive"),
                        width=300,
                        height=45
                    ),
                ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
            ),
            actions=[
                ft.TextButton(TranslationService.translate_from_dict("general", "cancel", self.language), 
                            on_click=lambda _: self._close_submenu_dialog(),
                            style=ft.ButtonStyle(color=self._current_text_color))
            ]
        )
        
        self.page.dialog = maps_dialog
        maps_dialog.open = True
        self.page.update()

    def _handle_maps_choice(self, choice):
        """Gestisce la scelta del tipo di mappa."""
        self._close_submenu_dialog()
        
        if choice == "advanced":
            if self.advanced_maps_alert:
                self.advanced_maps_alert.open_dialog()
        elif choice == "interactive":
            if self.interactive_maps_alert:
                self.interactive_maps_alert.open_dialog()

    def _show_analytics_submenu(self, e):
        """Show analytics submenu dialog."""
        if not self.page:
            return
        
        # Chiudi il menu principale
        if hasattr(self, 'popup_menu_button_control'):
            self.popup_menu_button_control.open = False
            self.page.update()
        
        # Crea dialog per analytics
        analytics_dialog = ft.AlertDialog(
            modal=True,
            scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ANALYTICS, color="#9C27B0", size=24),
                ft.Text(TranslationService.translate_from_dict("popup_menu_items", "analytics", self.language), 
                       weight=ft.FontWeight.BOLD, size=18, color=self._current_text_color)
            ], spacing=10),
            content=ft.Container(
                width=350,
                height=200,
                content=ft.Column([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.TRENDING_UP, color="#4CAF50"),
                            ft.Text(TranslationService.translate_from_dict("popup_menu_items", "weather_trends", self.language), size=14)
                        ], spacing=10),
                        on_click=lambda _: self._handle_submenu_choice("weather_trends"),
                        width=300,
                        height=45
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.HISTORY, color="#795548"),
                            ft.Text(TranslationService.translate_from_dict("popup_menu_items", "historical_data", self.language), size=14)
                        ], spacing=10),
                        on_click=lambda _: self._handle_submenu_choice("historical_data"),
                        width=300,
                        height=45
                    ),
                ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
            ),
            actions=[
                ft.TextButton(TranslationService.translate_from_dict("general", "cancel", self.language), 
                            on_click=lambda _: self._close_submenu_dialog(),
                            style=ft.ButtonStyle(color=self._current_text_color))
            ]
        )
        
        self.page.dialog = analytics_dialog
        analytics_dialog.open = True
        self.page.update()

    def _show_alerts_submenu(self, e):
        """Show alerts submenu dialog."""
        if not self.page:
            return
        
        # Chiudi il menu principale
        if hasattr(self, 'popup_menu_button_control'):
            self.popup_menu_button_control.open = False
            self.page.update()
        
        # Crea dialog per alerts
        alerts_dialog = ft.AlertDialog(
            modal=True,
            scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING, color="#FF5722", size=24),
                ft.Text(TranslationService.translate_from_dict("popup_menu_items", "alerts", self.language), 
                       weight=ft.FontWeight.BOLD, size=18, color=self._current_text_color)
            ], spacing=10),
            content=ft.Container(
                width=350,
                height=150,
                content=ft.Column([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.NOTIFICATIONS, color="#FF9800"),
                            ft.Text(TranslationService.translate_from_dict("popup_menu_items", "push_notifications", self.language), size=14)
                        ], spacing=10),
                        on_click=lambda _: self._handle_submenu_choice("push_notifications"),
                        width=300,
                        height=45
                    ),
                ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
            ),
            actions=[
                ft.TextButton(TranslationService.translate_from_dict("general", "cancel", self.language), 
                            on_click=lambda _: self._close_submenu_dialog(),
                            style=ft.ButtonStyle(color=self._current_text_color))
            ]
        )
        
        self.page.dialog = alerts_dialog
        alerts_dialog.open = True
        self.page.update()

    def _show_tools_submenu(self, e):
        """Show tools submenu dialog."""
        if not self.page:
            return
        
        # Chiudi il menu principale
        if hasattr(self, 'popup_menu_button_control'):
            self.popup_menu_button_control.open = False
            self.page.update()
        
        # Crea dialog per tools
        tools_dialog = ft.AlertDialog(
            modal=True,
            scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.BUILD, color="#607D8B", size=24),
                ft.Text(TranslationService.translate_from_dict("popup_menu_items", "tools", self.language), 
                       weight=ft.FontWeight.BOLD, size=18, color=self._current_text_color)
            ], spacing=10),
            content=ft.Container(
                width=350,
                height=200,
                content=ft.Column([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON, color="#E91E63"),
                            ft.Text(TranslationService.translate_from_dict("popup_menu_items", "location_manager", self.language), size=14)
                        ], spacing=10),
                        on_click=lambda _: self._handle_submenu_choice("location_manager"),
                        width=300,
                        height=45
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DOWNLOAD, color="#3F51B5"),
                            ft.Text(TranslationService.translate_from_dict("popup_menu_items", "export_data", self.language), size=14)
                        ], spacing=10),
                        on_click=lambda _: self._handle_submenu_choice("export_data"),
                        width=300,
                        height=45
                    ),
                ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
            ),
            actions=[
                ft.TextButton(TranslationService.translate_from_dict("general", "cancel", self.language), 
                            on_click=lambda _: self._close_submenu_dialog(),
                            style=ft.ButtonStyle(color=self._current_text_color))
            ]
        )
        
        self.page.dialog = tools_dialog
        tools_dialog.open = True
        self.page.update()

    def _handle_submenu_choice(self, choice):
        """Handle submenu item selection."""
        self._close_submenu_dialog()
        
        # Handle different submenu choices
        if choice == "weather_trends":
            if self.weather_trends_dialog:
                self.weather_trends_dialog.show_dialog()
        elif choice == "historical_data":
            if self.historical_data_dialog:
                self.historical_data_dialog.show_dialog()
        elif choice == "push_notifications":
            if self.push_notifications_dialog:
                self.push_notifications_dialog.show_dialog()
        elif choice == "location_manager":
            if self.location_manager_dialog:
                self.location_manager_dialog.show_dialog()
        elif choice == "export_data":
            if self.export_data_dialog:
                self.export_data_dialog.show_dialog()

    def _close_submenu_dialog(self):
        """Close any open submenu dialog."""
        if self.page and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

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
