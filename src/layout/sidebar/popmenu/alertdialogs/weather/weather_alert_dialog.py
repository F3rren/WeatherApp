import logging
import flet as ft
from services.translation_service import TranslationService

class WeatherAlertDialog:

    def __init__(self, page: ft.Page, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None, 
                 theme_handler=None, language: str = "en"):
        self.page = page
        self.state_manager = state_manager
        self.handle_location_toggle = handle_location_toggle
        self.handle_theme_toggle = handle_theme_toggle
        self.current_language = language
        self.theme_handler = theme_handler
        self.dialog = None
        self.update_ui()

    def update_ui(self, event_data=None):
        # Always update theme and language using theme_handler
        if self.theme_handler:
            self.text_color = self.theme_handler.get_text_color()
            if isinstance(self.text_color, str):
                # If theme_handler returns a string, wrap as dict for compatibility
                self.text_color = {"TEXT": self.text_color, "DIALOG_BACKGROUND": "#fff", "ACCENT": "#0078d4"}
        else:
            self.text_color = {"TEXT": "#000000", "DIALOG_BACKGROUND": "#fff", "ACCENT": "#0078d4"}
        # Optionally update language from state_manager
        if self.state_manager:
            self.current_language = self.state_manager.get_state('language') or self.current_language
        self.dialog = self.build()

    def build(self):
        def get_size(k):
            if k == 'title':
                return 20
            elif k == 'body':
                return 14
            elif k == 'icon':
                return 20
            return 14
        dialog_text_color = self.text_color["TEXT"]
        accent_color = self.text_color.get("ACCENT", "#0078d4")
        title_size = get_size('title')
        body_size = get_size('body')
        icon_size = get_size('icon')
        # Supporto dark mode per il background del dialog
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        dialog_bg = "#161b22" if is_dark else "#ffffff"
        title_text_control = ft.Text(
            self._get_translation("weather"), 
            size=title_size, 
            weight=ft.FontWeight.BOLD, 
            color=dialog_text_color
        )
        language_icon_control = ft.Icon(ft.Icons.LANGUAGE, size=icon_size, color="#ff6b35")
        measurement_icon_control = ft.Icon(ft.Icons.STRAIGHTEN, size=icon_size, color="#22c55e")
        location_icon_control = ft.Icon(ft.Icons.LOCATION_ON, size=icon_size, color="#ef4444")
        theme_icon_control = ft.Icon(ft.Icons.DARK_MODE, size=icon_size, color="#3b82f6")
        language_text_control = ft.Text(self._get_translation("language_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        measurement_text_control = ft.Text(self._get_translation("measurement_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        location_text_control = ft.Text(self._get_translation("use_current_location_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        theme_text_control = ft.Text(self._get_translation("dark_theme_setting"), size=body_size, weight=ft.FontWeight.W_500, color=dialog_text_color)
        close_button_text_control = ft.Text(self._get_translation("close_button"), color=accent_color, size=body_size)
        dialog = ft.AlertDialog(
            title=title_text_control,
            bgcolor=dialog_bg,
            content=ft.Container(
                width=400,
                bgcolor=dialog_bg,
                opacity=1.0,
                content=ft.Column(
                    controls=[
                        # Language selector row
                        ft.Row(
                            controls=[
                                ft.Row(controls=[language_icon_control, language_text_control], spacing=10),
                                self._build_language_dropdown(),
                            ],
                            spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        # Unit system selector row
                        ft.Row(
                            controls=[
                                ft.Row(controls=[measurement_icon_control, measurement_text_control], spacing=10),
                                self._build_unit_dropdown(),
                            ],
                            spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        # Location toggle row
                        ft.Row(
                            controls=[
                                ft.Row(controls=[location_icon_control, location_text_control], spacing=10),
                                self._build_location_switch(),
                            ],
                            spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        # Theme toggle row
                        ft.Row(
                            controls=[
                                ft.Row(controls=[theme_icon_control, theme_text_control], spacing=10),
                                self._build_theme_switch(),
                            ],
                            spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        # Divider
                        ft.Divider(color=ft.Colors.with_opacity(0.2, dialog_text_color)),
                        # Current weather info section
                        self._build_current_weather_info(),
                        # Quick actions section
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text=self._get_translation("refresh_data"),
                                    icon=ft.Icons.REFRESH,
                                    on_click=self._refresh_weather_data,
                                    bgcolor=accent_color,
                                    color="#ffffff",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    )
                                ),
                                ft.OutlinedButton(
                                    text=self._get_translation("view_forecast"),
                                    icon=ft.Icons.CALENDAR_VIEW_WEEK,
                                    on_click=self._show_forecast_summary,
                                    style=ft.ButtonStyle(
                                        color=accent_color,
                                        side=ft.BorderSide(1, accent_color),
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    )
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ],
                    height=450,  # Increased height for more content
                    spacing=20,
                ),
            ),
            actions=[
                ft.TextButton(
                    content=close_button_text_control,
                    style=ft.ButtonStyle(
                        color=accent_color,
                        overlay_color=ft.Colors.with_opacity(0.1, accent_color),
                    ),
                    on_click=lambda e: self.close_dialog()
                ),
            ],
            on_dismiss=lambda e: logging.info("Weather Dialog dismissed"),
            modal=True
        )
        return dialog

    def _get_translation(self, key):
        """Get translation with fallback for new keys not yet in translation files."""
        try:
            # First try the standard translation service
            result = TranslationService.translate(key, str(self.current_language))
            
            # If the result is the same as the key, it means no translation was found
            if result == key:
                # Use our local fallback translations
                local_translations = {
                    "en": {
                        "weather": "Weather Settings",
                        "language_setting": "Language",
                        "measurement_setting": "Units",
                        "use_current_location_setting": "Use GPS Location",
                        "dark_theme_setting": "Dark Theme",
                        "close_button": "Close",
                        "current_weather": "Current Weather",
                        "weather_info_unavailable": "Weather info unavailable",
                        "refresh_data": "Refresh",
                        "view_forecast": "Forecast",
                        "refreshing_data": "Refreshing weather data...",
                        "forecast_summary": "Quick Forecast",
                        "next_hours_forecast": "Next hours",
                        "no_forecast_data": "No forecast data available"
                    },
                    "it": {
                        "weather": "Impostazioni Meteo",
                        "language_setting": "Lingua",
                        "measurement_setting": "Unità",
                        "use_current_location_setting": "Usa Posizione GPS",
                        "dark_theme_setting": "Tema Scuro", 
                        "close_button": "Chiudi",
                        "current_weather": "Meteo Attuale",
                        "weather_info_unavailable": "Info meteo non disponibili",
                        "refresh_data": "Aggiorna",
                        "view_forecast": "Previsioni",
                        "refreshing_data": "Aggiornamento dati meteo...",
                        "forecast_summary": "Previsioni Rapide",
                        "next_hours_forecast": "Prossime ore",
                        "no_forecast_data": "Nessun dato previsione disponibile"
                    },
                    "es": {
                        "weather": "Configuración del Clima",
                        "language_setting": "Idioma",
                        "measurement_setting": "Unidades",
                        "use_current_location_setting": "Usar GPS",
                        "dark_theme_setting": "Tema Oscuro",
                        "close_button": "Cerrar",
                        "current_weather": "Clima Actual",
                        "weather_info_unavailable": "Info clima no disponible",
                        "refresh_data": "Actualizar",
                        "view_forecast": "Pronóstico",
                        "refreshing_data": "Actualizando datos...",
                        "forecast_summary": "Pronóstico Rápido",
                        "next_hours_forecast": "Próximas horas",
                        "no_forecast_data": "Sin datos de pronóstico"
                    },
                    "fr": {
                        "weather": "Paramètres Météo",
                        "language_setting": "Langue",
                        "measurement_setting": "Unités",
                        "use_current_location_setting": "Utiliser GPS",
                        "dark_theme_setting": "Thème Sombre",
                        "close_button": "Fermer",
                        "current_weather": "Météo Actuelle",
                        "weather_info_unavailable": "Info météo indisponible",
                        "refresh_data": "Actualiser",
                        "view_forecast": "Prévisions",
                        "refreshing_data": "Actualisation des données...",
                        "forecast_summary": "Prévisions Rapides",
                        "next_hours_forecast": "Prochaines heures",
                        "no_forecast_data": "Aucune donnée de prévision"
                    },
                    "de": {
                        "weather": "Wetter Einstellungen",
                        "language_setting": "Sprache",
                        "measurement_setting": "Einheiten",
                        "use_current_location_setting": "GPS verwenden",
                        "dark_theme_setting": "Dunkles Design",
                        "close_button": "Schließen",
                        "current_weather": "Aktuelles Wetter",
                        "weather_info_unavailable": "Wetter-Info nicht verfügbar",
                        "refresh_data": "Aktualisieren",
                        "view_forecast": "Vorhersage",
                        "refreshing_data": "Daten werden aktualisiert...",
                        "forecast_summary": "Kurze Vorhersage",
                        "next_hours_forecast": "Nächste Stunden",
                        "no_forecast_data": "Keine Vorhersagedaten verfügbar"
                    }
                }
                
                lang = str(self.current_language).lower()
                if lang in local_translations and key in local_translations[lang]:
                    return local_translations[lang][key]
                elif key in local_translations.get("en", {}):
                    return local_translations["en"][key]
            
            return result
        except Exception as e:
            logging.warning(f"Translation error for key '{key}': {e}")
            return key

    def open_dialog(self):
        if not self.dialog:
            self.dialog = self.build()
        if self.page and self.dialog:
            if self.dialog not in self.page.controls:
                self.page.controls.append(self.dialog)
            self.page.dialog = self.dialog
            self.page.dialog.open = True
            self.page.update()

    def close_dialog(self):
        if self.dialog:
            self.dialog.open = False
            if self.page:
                 self.page.update()

    def _build_language_dropdown(self):
        """Build language selection dropdown."""
        current_language = self.state_manager.get_state('language') if self.state_manager else 'en'
        
        language_options = [
            ft.dropdown.Option("en", "English"),
            ft.dropdown.Option("it", "Italiano"),
            ft.dropdown.Option("es", "Español"),
            ft.dropdown.Option("fr", "Français"),
            ft.dropdown.Option("de", "Deutsch"),
            ft.dropdown.Option("pt", "Português"),
            ft.dropdown.Option("ru", "Русский"),
            ft.dropdown.Option("zh", "中文"),
            ft.dropdown.Option("ja", "日本語"),
            ft.dropdown.Option("ar", "العربية"),
            ft.dropdown.Option("hi", "हिन्दी"),
            ft.dropdown.Option("ko", "한국어"),
        ]
        
        return ft.Dropdown(
            width=120,
            value=current_language,
            options=language_options,
            on_change=self._on_language_change,
            text_size=12,
            dense=True,
        )

    def _build_unit_dropdown(self):
        """Build unit system selection dropdown."""
        current_unit = self.state_manager.get_state('unit') if self.state_manager else 'metric'
        
        unit_options = [
            ft.dropdown.Option("metric", "Metric (°C)"),
            ft.dropdown.Option("imperial", "Imperial (°F)"),
            ft.dropdown.Option("standard", "Standard (K)"),
        ]
        
        return ft.Dropdown(
            width=120,
            value=current_unit,
            options=unit_options,
            on_change=self._on_unit_change,
            text_size=12,
            dense=True,
        )

    def _build_location_switch(self):
        """Build location toggle switch."""
        using_location = self.state_manager.get_state('using_location') if self.state_manager else False
        
        return ft.Switch(
            value=using_location,
            on_change=self._on_location_toggle,
            thumb_color=self.text_color.get("ACCENT", "#0078d4"),
        )

    def _build_theme_switch(self):
        """Build theme toggle switch."""
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        return ft.Switch(
            value=is_dark,
            on_change=self._on_theme_toggle,
            thumb_color=self.text_color.get("ACCENT", "#0078d4"),
        )

    def _build_current_weather_info(self):
        """Build current weather information section."""
        try:
            current_city = self.state_manager.get_state('city') if self.state_manager else "Unknown"
            current_temp = "N/A"
            current_condition = "N/A"
            
            # Try to get current weather from session or state
            main_app = self.page.session.get('main_app') if self.page else None
            if main_app and hasattr(main_app, 'weather_view_instance') and main_app.weather_view_instance:
                weather_data = main_app.weather_view_instance.weather_data
                if weather_data and 'list' in weather_data and len(weather_data['list']) > 0:
                    current_data = weather_data['list'][0]
                    temp_data = current_data.get('main', {})
                    current_temp = f"{int(temp_data.get('temp', 0))}°"
                    weather_info = current_data.get('weather', [{}])[0]
                    current_condition = weather_info.get('description', 'N/A').title()
            
            info_color = self.text_color["TEXT"]
            
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            self._get_translation("current_weather"),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=info_color
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.LOCATION_CITY, size=16, color="#f59e0b"),
                                ft.Text(f"{current_city}", size=12, color=info_color),
                            ],
                            spacing=5
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.THERMOSTAT, size=16, color="#ef4444"),
                                ft.Text(f"{current_temp}", size=12, color=info_color),
                                ft.Text(f"({current_condition})", size=10, color=ft.Colors.with_opacity(0.7, info_color)),
                            ],
                            spacing=5
                        ),
                    ],
                    spacing=5
                ),
                padding=ft.padding.all(8),
                bgcolor=ft.Colors.with_opacity(0.05, self.text_color["TEXT"]),
                border_radius=8,
            )
        except Exception as e:
            logging.warning(f"Error building weather info: {e}")
            return ft.Container(
                content=ft.Text(
                    self._get_translation("weather_info_unavailable"),
                    size=12,
                    color=ft.Colors.with_opacity(0.6, self.text_color["TEXT"])
                ),
                padding=8
            )

    def _on_language_change(self, e):
        """Handle language change."""
        if self.state_manager and e.control.value:
            import asyncio
            if hasattr(self.page, 'run_task'):
                self.page.run_task(self.state_manager.set_state, "language", e.control.value)
            else:
                asyncio.create_task(self.state_manager.set_state("language", e.control.value))

    def _on_unit_change(self, e):
        """Handle unit system change."""
        if self.state_manager and e.control.value:
            import asyncio
            if hasattr(self.page, 'run_task'):
                self.page.run_task(self.state_manager.set_state, "unit", e.control.value)
            else:
                asyncio.create_task(self.state_manager.set_state("unit", e.control.value))

    def _on_location_toggle(self, e):
        """Handle location toggle."""
        if self.handle_location_toggle:
            self.handle_location_toggle(e)

    def _on_theme_toggle(self, e):
        """Handle theme toggle."""
        if self.handle_theme_toggle:
            self.handle_theme_toggle(e)

    def _refresh_weather_data(self, e):
        """Refresh weather data."""
        try:
            main_app = self.page.session.get('main_app') if self.page else None
            if main_app and self.state_manager:
                city = self.state_manager.get_state('city')
                language = self.state_manager.get_state('language')
                unit = self.state_manager.get_state('unit')
                
                if city and language and unit:
                    if hasattr(self.page, 'run_task'):
                        self.page.run_task(main_app.update_weather_with_sidebar, city, language, unit)
                    
                    # Show temporary feedback
                    self.page.show_snack_bar(
                        ft.SnackBar(
                            content=ft.Text(self._get_translation("refreshing_data")),
                            duration=2000
                        )
                    )
        except Exception as ex:
            logging.error(f"Error refreshing weather data: {ex}")

    def _show_forecast_summary(self, e):
        """Show a quick forecast summary."""
        try:
            main_app = self.page.session.get('main_app') if self.page else None
            if main_app and hasattr(main_app, 'weather_view_instance') and main_app.weather_view_instance:
                weather_data = main_app.weather_view_instance.weather_data
                if weather_data and 'list' in weather_data:
                    forecast_items = weather_data['list'][:5]  # Next 5 forecasts
                    
                    forecast_text = self._get_translation("next_hours_forecast") + ":\n"
                    for i, item in enumerate(forecast_items):
                        time_str = item.get('dt_txt', '').split(' ')[1][:5] if 'dt_txt' in item else f"{i*3}h"
                        temp = int(item.get('main', {}).get('temp', 0))
                        condition = item.get('weather', [{}])[0].get('main', 'N/A')
                        forecast_text += f"• {time_str}: {temp}° - {condition}\n"
                    
                    forecast_dialog = ft.AlertDialog(
                        title=ft.Text(self._get_translation("forecast_summary")),
                        content=ft.Text(forecast_text, size=12),
                        actions=[
                            ft.TextButton(
                                self._get_translation("close_button"),
                                on_click=lambda e: self._close_forecast_dialog(forecast_dialog)
                            )
                        ]
                    )
                    
                    self.page.dialog = forecast_dialog
                    forecast_dialog.open = True
                    self.page.update()
                else:
                    self.page.show_snack_bar(
                        ft.SnackBar(
                            content=ft.Text(self._get_translation("no_forecast_data")),
                            duration=2000
                        )
                    )
        except Exception as ex:
            logging.error(f"Error showing forecast summary: {ex}")

    def _close_forecast_dialog(self, dialog):
        """Close forecast dialog."""
        dialog.open = False
        self.page.update()
