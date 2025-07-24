import os
from services.api.api_service import load_dotenv
from translations import translation_manager
from services.ui.theme_handler import ThemeHandler
from ui.components.sidebar.popmenu.alertdialogs.settings.settings_alert_dialog import SettingsAlertDialog
from ui.components.sidebar.popmenu.alertdialogs.maps.radar_live_dialog import RadarLiveDialog
from ui.components.sidebar.popmenu.alertdialogs.weather.weather_alert_dialog import WeatherAlertDialog
from ui.components.sidebar.popmenu.alertdialogs.alerts.push_notifications_dialog import PushNotificationsDialog
from ui.components.sidebar.popmenu.alertdialogs.tools.location_manager_dialog import LocationManagerDialog
from ui.components.sidebar.popmenu.alertdialogs.tools.export_data_dialog import ExportDataDialog
import flet as ft
import webbrowser


class PopMenu(ft.Container):
    def __init__(self, page: ft.Page = None, state_manager=None, 
                 handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_toggle_value=False, location_toggle_value=False, 
                 language: str = None, theme_handler: ThemeHandler = None,
                 update_weather_callback=None, **kwargs):
        super().__init__(**kwargs)
        load_dotenv()
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.theme_toggle_value = theme_toggle_value
        self.location_toggle_value = location_toggle_value
        self.theme_handler = theme_handler or ThemeHandler(page)
        self.language = language if language else os.getenv("DEFAULT_LANGUAGE")
        self.update_weather_callback = update_weather_callback
        self.weather_alert = None
        # Dialog rimossi - ora apriamo direttamente servizi esterni:
        # - advanced_maps_alert (sostituito da apertura diretta)
        # - interactive_maps_alert (sostituito da apertura diretta)  
        # - satellite_view_dialog (sostituito da apertura diretta Windy)
        # - weather_trends_dialog (sostituito da Climate Data Online)
        # - historical_data_dialog (sostituito da Weather History)
        self.radar_live_dialog = None
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
        self.language = self.state_manager.get_state('language') if self.state_manager else os.getenv("DEFAULT_LANGUAGE")

        # Update child dialogs, passing theme_handler for color logic
        self.weather_alert = WeatherAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        
        # Initialize dialogs (alcuni dialog rimossi - ora apriamo direttamente servizi esterni)
        self.radar_live_dialog = RadarLiveDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.push_notifications_dialog = PushNotificationsDialog(page=self.page, state_manager=self.state_manager, language=self.language)
        self.location_manager_dialog = LocationManagerDialog(
            page=self.page, 
            update_weather_callback=self.update_weather_callback,
            state_manager=self.state_manager,
            language=self.language
        )
        self.export_data_dialog = ExportDataDialog(page=self.page)
        self.setting_alert = SettingsAlertDialog(page=self.page, state_manager=self.state_manager, language=self.language, theme_handler=self.theme_handler, handle_location_toggle=self.handle_location_toggle, handle_theme_toggle=self.handle_theme_toggle)

        # Create popup menu items text
        self.pop_menu_items = {
            "weather": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "weather", self.language), color=self._current_text_color),
            "maps": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "maps", self.language), color=self._current_text_color),
            "advanced_maps": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "advanced_maps", self.language), color=self._current_text_color),
            "interactive_maps": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "interactive_maps", self.language), color=self._current_text_color),
            "satellite_view": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "satellite_view", self.language), color=self._current_text_color),
            "radar_live": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "radar_live", self.language), color=self._current_text_color),
            "analytics": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "analytics", self.language), color=self._current_text_color),
            "weather_trends": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "weather_trends", self.language), color=self._current_text_color),
            "historical_data": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "historical_data", self.language), color=self._current_text_color),
            "alerts": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "alerts", self.language), color=self._current_text_color),
            "push_notifications": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "push_notifications", self.language), color=self._current_text_color),
            "tools": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "tools", self.language), color=self._current_text_color),
            "location_manager": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "location_manager", self.language), color=self._current_text_color),
            "export_data": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "export_data", self.language), color=self._current_text_color),
            "settings": ft.Text(value=translation_manager.get_translation("popup_menu", "items", "settings", self.language), color=self._current_text_color)
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
                            content=ft.Text(translation_manager.get_translation("popup_menu", "items", "weather", self.language)),
                            leading=ft.Icon(ft.Icons.SUNNY, color="#FF8C00", size=20),
                            on_click=lambda _: self.weather_alert.show_dialog() if self.weather_alert else None,
                        ),
                # Mappe - sottomenu
                ft.SubmenuButton(
                    content=ft.Text(translation_manager.get_translation("popup_menu", "items", "maps", self.language)),
                    leading=ft.Icon(ft.Icons.MAP, color="#2196F3", size=20),
                    controls=[
                        # Mappe Avanzate - sottomenu
                        ft.SubmenuButton(
                            content=ft.Text(translation_manager.get_translation("popup_menu", "items", "advanced_maps", self.language)),
                            leading=ft.Icon(ft.Icons.LAYERS_OUTLINED, color="#4CAF50", size=20),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text("Earth Nullschool"),
                                    leading=ft.Icon(ft.Icons.PUBLIC, color="#FF5722", size=20),
                                    on_click=lambda _: self._open_nasa_worldview(),
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Ventusky Weather"),
                                    leading=ft.Icon(ft.Icons.CLOUD, color="#2196F3", size=20),
                                    on_click=lambda _: self._open_noaa_weather(),
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Windy Advanced Maps"),
                                    leading=ft.Icon(ft.Icons.LAYERS, color="#4CAF50", size=20),
                                    on_click=lambda _: self._open_ecmwf_maps(),
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Weather Radar Live"),
                                    leading=ft.Icon(ft.Icons.RADAR, color="#E91E63", size=20),
                                    on_click=lambda _: self._open_radar_italia(),
                                ),
                            ],
                        ),
                        # Mappe Interattive - sottomenu  
                        ft.SubmenuButton(
                            content=ft.Text(translation_manager.get_translation("popup_menu", "items", "interactive_maps", self.language)),
                            leading=ft.Icon(ft.Icons.MAP, color="#2196F3", size=20),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text("Weather.com Maps"),
                                    leading=ft.Icon(ft.Icons.CLOUD_QUEUE, color="#4285F4", size=20),
                                    on_click=lambda _: self._open_google_weather_maps(),
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("OpenWeatherMap"),
                                    leading=ft.Icon(ft.Icons.MAP_OUTLINED, color="#FF8C00", size=20),
                                    on_click=lambda _: self._open_openweather_maps(),
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Weather Underground"),
                                    leading=ft.Icon(ft.Icons.THUNDERSTORM, color="#9C27B0", size=20),
                                    on_click=lambda _: self._open_weather_underground(),
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("AccuWeather Radar"),
                                    leading=ft.Icon(ft.Icons.THERMOSTAT, color="#FF5722", size=20),
                                    on_click=lambda _: self._open_accuweather_maps(),
                                ),
                            ],
                        ),
                        ft.MenuItemButton(
                            content=ft.Text(translation_manager.get_translation("popup_menu", "items", "satellite_view", self.language)),
                            leading=ft.Icon(ft.Icons.SATELLITE_ALT, color="#607D8B", size=20),
                            on_click=lambda _: self._open_satellite_view(),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text(translation_manager.get_translation("popup_menu", "items", "radar_live", self.language)),
                            leading=ft.Icon(ft.Icons.RADAR, color="#E91E63", size=20),
                            on_click=lambda _: self._open_radar_live(),
                        ),
                    ],
                ),
                        # Analisi - sottomenu
                        ft.SubmenuButton(
                            content=ft.Text(translation_manager.get_translation("popup_menu", "items", "analytics", self.language)),
                            leading=ft.Icon(ft.Icons.ANALYTICS, color="#9C27B0", size=20),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text("Climate Data Online"),
                                    leading=ft.Icon(ft.Icons.TRENDING_UP, color="#4CAF50", size=20),
                                    on_click=lambda _: self._open_climate_data(),
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Weather History"),
                                    leading=ft.Icon(ft.Icons.HISTORY, color="#795548", size=20),
                                    on_click=lambda _: self._open_weather_history(),
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Weather Analytics"),
                                    leading=ft.Icon(ft.Icons.ANALYTICS_OUTLINED, color="#FF9800", size=20),
                                    on_click=lambda _: self._open_weather_analytics(),
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Climate Explorer"),
                                    leading=ft.Icon(ft.Icons.EXPLORE, color="#2196F3", size=20),
                                    on_click=lambda _: self._open_climate_explorer(),
                                ),
                            ],
                        ),
                        # Avvisi - sottomenu
                        ft.SubmenuButton(
                            content=ft.Text(translation_manager.get_translation("popup_menu", "items", "alerts", self.language)),
                            leading=ft.Icon(ft.Icons.WARNING, color="#FF5722", size=20),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text(translation_manager.get_translation("popup_menu", "items", "push_notifications", self.language)),
                                    leading=ft.Icon(ft.Icons.NOTIFICATIONS, color="#FF9800", size=20),
                                    on_click=lambda _: self.push_notifications_dialog.show_dialog() if self.push_notifications_dialog else None,
                                ),
                            ],
                        ),
                        # Strumenti - sottomenu
                        ft.SubmenuButton(
                            content=ft.Text(translation_manager.get_translation("popup_menu", "items", "tools", self.language)),
                            leading=ft.Icon(ft.Icons.BUILD, color="#607D8B", size=20),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text(translation_manager.get_translation("popup_menu", "items", "location_manager", self.language)),
                                    leading=ft.Icon(ft.Icons.LOCATION_ON, color="#E91E63", size=20),
                                    on_click=lambda _: self.location_manager_dialog.show_dialog() if self.location_manager_dialog else None,
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text(translation_manager.get_translation("popup_menu", "items", "export_data", self.language)),
                                    leading=ft.Icon(ft.Icons.DOWNLOAD, color="#3F51B5", size=20),
                                    on_click=lambda _: self.export_data_dialog.show_dialog() if self.export_data_dialog else None,
                                ),
                            ],
                        ),
                        # Impostazioni - item diretto
                        ft.MenuItemButton(
                            content=ft.Text(translation_manager.get_translation("popup_menu", "items", "settings", self.language)),
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
    
    def _get_current_latitude(self) -> float:
        """Ottiene la latitudine corrente dal state manager"""
        if self.state_manager:
            lat = self.state_manager.get_state('current_lat')
            if lat is not None:
                return float(lat)
        return 45.4642  # Default Milano
    
    def _get_current_longitude(self) -> float:
        """Ottiene la longitudine corrente dal state manager"""
        if self.state_manager:
            lon = self.state_manager.get_state('current_lon')
            if lon is not None:
                return float(lon)
        return 9.1900  # Default Milano
    
    def _open_satellite_view(self):
        """Apre direttamente la vista satellitare Windy nel browser"""
        print("DEBUG: _open_satellite_view chiamato - apertura diretta")
        
        try:
            import webbrowser
            
            # Ottiene le coordinate correnti
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            print(f"DEBUG: Coordinate trovate - Lat: {lat}, Lon: {lon}")
            
            # Costruisce l'URL di Windy con le coordinate
            url = f"https://www.windy.com/?satellite,{lat},{lon},8"
            print(f"DEBUG: Aprendo URL direttamente: {url}")
            
            # Apre il browser
            webbrowser.open(url)
            
            # Mostra notifica di conferma
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Vista satellitare Windy aperta nel browser"),
                    bgcolor=ft.colors.BLUE_400
                )
                self.page.snack_bar.open = True
                self.page.update()
                
            print("DEBUG: Vista satellitare aperta con successo!")
            
        except Exception as e:
            print(f"ERROR: Errore nell'apertura della vista satellitare: {e}")
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Errore nell'apertura della vista satellitare"),
                    bgcolor=ft.colors.RED_400
                )
                self.page.snack_bar.open = True
                self.page.update()

    # === MAPPE AVANZATE ===
    def _open_nasa_worldview(self):
        """Apre Earth Nullschool (alternative a NASA) con vista globale"""
        try:
            import webbrowser
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            # Earth Nullschool - molto più affidabile e accessibile
            url = f"https://earth.nullschool.net/#{lat},{lon},1024"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Earth Nullschool aperto nel browser"),
                    bgcolor=ft.colors.ORANGE_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _open_noaa_weather(self):
        """Apre Ventusky Maps (alternativa più accessibile)"""
        try:
            import webbrowser
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            # Ventusky - molto affidabile per mappe meteo
            url = f"https://www.ventusky.com/?p={lat};{lon};8&l=temperature-2m"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Ventusky Weather Maps aperto nel browser"),
                    bgcolor=ft.colors.BLUE_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _open_ecmwf_maps(self):
        """Apre Windy Advanced Maps (servizio internazionale premium)"""
        try:
            import webbrowser
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            # Windy Advanced - servizio internazionale molto professionale
            url = f"https://www.windy.com/?{lat},{lon},8,m:eyadhpa"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Windy Advanced Maps aperto nel browser"),
                    bgcolor=ft.colors.GREEN_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _open_radar_italia(self):
        """Apre Weather Radar Live (servizio internazionale)"""
        try:
            import webbrowser
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            # Weather Radar Live - servizio internazionale con coordinate
            url = f"https://www.weather.gov/radar/?lat={lat}&lon={lon}"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Weather Radar Live aperto nel browser"),
                    bgcolor=ft.colors.RED_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    # === MAPPE INTERATTIVE ===
    def _open_google_weather_maps(self):
        """Apre Weather.com Interactive Maps"""
        try:
            import webbrowser
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            # Weather.com interactive map - servizio internazionale molto affidabile
            url = f"https://weather.com/maps/currentconditions?lat={lat}&lon={lon}&zoom=8"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Weather.com Maps aperto nel browser"),
                    bgcolor=ft.colors.BLUE_600
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _open_openweather_maps(self):
        """Apre OpenWeatherMap interactive"""
        try:
            import webbrowser
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            url = f"https://openweathermap.org/weathermap?basemap=map&cities=true&layer=temperature&lat={lat}&lon={lon}&zoom=8"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("OpenWeatherMap aperto nel browser"),
                    bgcolor=ft.colors.ORANGE_600
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _open_weather_underground(self):
        """Apre Weather Underground Maps"""
        try:
            import webbrowser
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            url = f"https://www.wunderground.com/wundermap?lat={lat}&lon={lon}&zoom=8&pin={lat}%2C{lon}&rad=1&wxsn=0"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Weather Underground aperto nel browser"),
                    bgcolor=ft.colors.PURPLE_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _open_accuweather_maps(self):
        """Apre AccuWeather Radar Maps"""
        try:
            import webbrowser
            
            # AccuWeather Radar - più diretto
            url = "https://www.accuweather.com/en/us/national/satellite"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("AccuWeather Radar aperto nel browser"),
                    bgcolor=ft.colors.RED_600
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _open_radar_live(self):
        """Apre radar meteorologico live (Rain Viewer)"""
        try:
            import webbrowser
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            url = f"https://www.rainviewer.com/map.html?loc={lat},{lon},8"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Radar Live aperto nel browser"),
                    bgcolor=ft.colors.PINK_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    # === SERVIZI DI ANALISI METEOROLOGICA ===
    def _open_climate_data(self):
        """Apre Weather Underground Historical per dati climatici storici"""
        try:
            # Ottieni le coordinate correnti usando i metodi esistenti
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            # Weather Underground Historical - supporta coordinate e fornisce dati climatici storici
            url = f"https://www.wunderground.com/history/daily/{lat},{lon}/date/2024-1-1"
            
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Dati climatici storici aperti nel browser"),
                    bgcolor=ft.colors.GREEN_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")
            print(f"ERROR: {e}")

    def _open_weather_history(self):
        """Apre Weather History per dati storici meteorologici"""
        try:
            import webbrowser
            lat = self._get_current_latitude()
            lon = self._get_current_longitude()
            
            # Weather Underground Historical Weather
            url = f"https://www.wunderground.com/history/daily/{lat},{lon}/date/2024-1-1"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Weather History aperto nel browser"),
                    bgcolor=ft.colors.BROWN_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _open_weather_analytics(self):
        """Apre Climate.gov per analisi e grafici meteorologici"""
        try:
            import webbrowser
            
            # Climate.gov Maps and Data - servizio ufficiale USA per analisi climatiche
            url = "https://www.climate.gov/maps-data"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Weather Analytics aperto nel browser"),
                    bgcolor=ft.colors.ORANGE_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _open_climate_explorer(self):
        """Apre Climate Explorer per analisi climatiche avanzate"""
        try:
            import webbrowser
            
            # NOAA Climate Explorer - strumento professionale per analisi climatiche
            url = "https://www.ncdc.noaa.gov/climate-explorer/"
            webbrowser.open(url)
            
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Climate Explorer aperto nel browser"),
                    bgcolor=ft.colors.BLUE_400
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            print(f"ERROR: {e}")

    def _determine_text_color_from_theme(self):
        """Returns the full theme dictionary based on the current page theme."""
        if not self.page:
            return "black"
        return "white" if self.page.theme_mode == ft.ThemeMode.DARK else "black"
