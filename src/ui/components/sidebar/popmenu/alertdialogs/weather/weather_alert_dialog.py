import asyncio
import flet as ft
from services.alerts.weather_alerts_service import AlertSeverity, AlertType
from translations import translation_manager  # New modular translation system

class WeatherAlertDialog:
    """Dialog semplificato per la gestione delle allerte meteo."""

    def __init__(self, page: ft.Page, state_manager=None, language: str = "en"):
        self.page = page
        self.state_manager = state_manager
        self.language = language
        self.dialog = None
        
        # Get weather alerts service from session
        self.weather_alerts_service = self.page.session.get('weather_alerts_service') if self.page else None
        
        # Initialize colors
        self.update_theme_colors()

    def update_theme_colors(self):
        """Update theme colors based on current theme."""
        is_dark = (hasattr(self.page, 'theme_mode') and 
                  self.page.theme_mode == ft.ThemeMode.DARK)
        
        if is_dark:
            self.colors = {
                "bg": "#161b22", "surface": "#21262d", "text": "#f0f6fc",
                "text_secondary": "#8b949e", "accent": "#58a6ff", "border": "#30363d",
                "success": "#238636", "warning": "#d29922", "error": "#f85149", "purple": "#a5a2ff"
            }
        else:
            self.colors = {
                "bg": "#ffffff", "surface": "#f6f8fa", "text": "#24292f",
                "text_secondary": "#656d76", "accent": "#0969da", "border": "#d1d9e0",
                "success": "#1a7f37", "warning": "#bf8700", "error": "#cf222e", "purple": "#8250df"
            }

    def get_translation(self, key: str) -> str:
        """Get translation for a key using new modular translation system."""
        return translation_manager.get_translation(
            'weather', 'weather_alert_dialog_items', key, 
            language=self.language
        )

    def create_dialog(self):
        """Create the weather alerts dialog."""
        self.update_theme_colors()
        
        if not self.weather_alerts_service:
            return self.create_error_dialog(self.get_translation("service_unavailable"))
        
        try:
            return ft.AlertDialog(
                modal=False,
                title=self.create_header(),
                bgcolor=self.colors["bg"],
                content=ft.Container(
                    width=min(400, self.page.width * 0.9),
                    bgcolor=self.colors["bg"],
                    padding=20,
                    content=ft.Column([
                        # Statistiche compatte
                        self.create_compact_statistics(),
                        #ft.Container(height=15),
                        # Lista allerte semplificata
                        self.create_compact_alerts_list(),
                        #ft.Container(height=15),
                    ], spacing=10, tight=True)
                ),
                actions=[self.create_actions()],
                actions_alignment=ft.MainAxisAlignment.END,
                title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
                content_text_style=ft.TextStyle(size=14, color=self.colors["text"]),
                inset_padding=ft.padding.all(20)
            )
        except Exception as e:
            print(f"Error building weather alert dialog: {e}")
            return self.create_error_dialog(f"Errore nella creazione del dialogo: {str(e)}")

    def create_error_dialog(self, message: str):
        """Create error dialog when main dialog fails."""
        return ft.AlertDialog(
            modal=False,
            title=ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=self.colors["error"], size=24),
                ft.Text(self.get_translation("weather_alert_error"), size=18, weight=ft.FontWeight.BOLD, color=self.colors["text"])
            ], spacing=10),
            bgcolor=self.colors["bg"],
            content=ft.Container(
                width=min(400, self.page.width * 0.9), bgcolor=self.colors["bg"],
                padding=ft.padding.all(20),
                content=ft.Column([
                    ft.Text(message, size=14, color=self.colors["text"], text_align=ft.TextAlign.CENTER),
                    ft.Text(self.get_translation("error_retry_message"), size=12, 
                           color=self.colors["text_secondary"], text_align=ft.TextAlign.CENTER)
                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                alignment=ft.MainAxisAlignment.CENTER)
            ),
            actions=[ft.Row([
                ft.TextButton(
                    text=translation_manager.get_translation(
                        'weather', 'dialog_buttons', 'retry', 
                        language=self.language
                    ),
                    icon=ft.Icons.REFRESH, on_click=lambda e: self.retry_dialog(),
                    style=ft.ButtonStyle(color=self.colors["accent"])
                ),
                ft.FilledButton(
                    text=translation_manager.get_translation(
                        'weather', 'dialog_buttons', 'close', 
                        language=self.language
                    ),
                    on_click=lambda e: self.close_dialog(),
                    style=ft.ButtonStyle(bgcolor=self.colors["accent"], color=ft.Colors.WHITE,
                                       shape=ft.RoundedRectangleBorder(radius=8))
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)]
        )

    def retry_dialog(self):
        """Retry building and showing the dialog."""
        try:
            self.weather_alerts_service = self.page.session.get('weather_alerts_service') if self.page and self.page.session else None
            if self.weather_alerts_service:
                self.close_dialog()
                self.show_dialog()
            else:
                self.show_snackbar(self.get_translation("service_unavailable"), self.colors["error"])
        except Exception as e:
            print(f"Error retrying dialog: {e}")
            self.show_snackbar(f"{self.get_translation('error_retrying')}: {str(e)}", self.colors["error"])

    def create_header(self):
        """Create dialog header with title and status."""
        active_count = len(self.weather_alerts_service.get_active_alerts()) if self.weather_alerts_service else 0
        
        return ft.Row([
            ft.Icon(ft.Icons.WARNING_ROUNDED, color=self.colors["warning"], size=24),
            ft.Column([
                ft.Text(self.get_translation("weather_alerts"), size=18, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
                ft.Text(f"{active_count} " + self.get_translation("active_alerts_count"), size=12, color=self.colors["text_secondary"])
            ], spacing=2, expand=True),
            ft.IconButton(icon=ft.Icons.REFRESH, tooltip=self.get_translation("refresh"), 
                         on_click=self.refresh_alerts, icon_color=self.colors["accent"])
        ], spacing=10)

    def create_statistics(self):
        """Create alert statistics section."""
        if not self.weather_alerts_service:
            return ft.Container()
        
        active_alerts = self.weather_alerts_service.get_active_alerts()
        severity_counts = {severity: 0 for severity in AlertSeverity}
        for alert in active_alerts:
            severity_counts[alert.severity] += 1
        
        severity_info = [
            (AlertSeverity.LOW, self.get_translation("severity_low"), self.colors["success"]),
            (AlertSeverity.MODERATE, self.get_translation("severity_moderate"), self.colors["warning"]),
            (AlertSeverity.HIGH, self.get_translation("severity_high"), self.colors["error"]),
            (AlertSeverity.EXTREME, self.get_translation("severity_extreme"), self.colors["purple"])
        ]
        
        cards = []
        for severity, label, color in severity_info:
            count = severity_counts[severity]
            cards.append(ft.Container(
                content=ft.Column([
                    ft.Text(str(count), size=20, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(label, size=10, color=self.colors["text_secondary"])
                ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(12), bgcolor=ft.Colors.with_opacity(0.1, color),
                border_radius=8, width=80
            ))
        
        return ft.Column([
            ft.Text(self.get_translation("alert_statistics"), size=14, weight=ft.FontWeight.W_600, color=self.colors["text"]),
            ft.Row(cards, spacing=10, alignment=ft.MainAxisAlignment.SPACE_AROUND)
        ], spacing=10)

    def create_alerts_list(self):
        """Create active alerts list."""
        if not self.weather_alerts_service:
            return ft.Container(content=ft.Text(self.get_translation("service_unavailable"), 
                                              color=self.colors["text_secondary"]), padding=20)
        
        active_alerts = self.weather_alerts_service.get_active_alerts()
        
        if not active_alerts:
            return ft.Container(
                content=ft.Column([
                    #ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=48, color=self.colors["success"]),
                    ft.Text(self.get_translation("no_active_alerts"), size=16, weight=ft.FontWeight.W_500, color=self.colors["success"]),
                    ft.Text(self.get_translation("all_clear"), size=12, color=self.colors["text_secondary"])
                ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20
            )
        
        alert_cards = [self.create_alert_card(alert) for alert in active_alerts]
        
        return ft.Column([
            ft.Row([
                ft.Text(self.get_translation("active_alerts"), size=14, weight=ft.FontWeight.W_600, color=self.colors["text"]),
                ft.TextButton(text=self.get_translation("acknowledge_all"), icon=ft.Icons.DONE_ALL,
                             on_click=self.acknowledge_all_alerts, style=ft.ButtonStyle(color=self.colors["accent"])) if active_alerts else ft.Container()
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.ListView(
                    controls=alert_cards,
                    spacing=8,
                    padding=ft.padding.symmetric(vertical=5),
                    auto_scroll=False
                ),
                height=min(400, max(200, len(alert_cards) * 80)),  # Dynamic height with min/max limits
                border=ft.border.all(1, self.colors["border"]),
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.02, self.colors["text"])
            )
        ], spacing=8)

    def create_alert_card(self, alert):
        """Create individual alert card."""
        severity_colors = {
            AlertSeverity.LOW: self.colors["success"], AlertSeverity.MODERATE: self.colors["warning"],
            AlertSeverity.HIGH: self.colors["error"], AlertSeverity.EXTREME: self.colors["purple"]
        }
        severity_color = severity_colors.get(alert.severity, self.colors["warning"])
        
        return ft.Container(
            content=ft.Row([
                ft.Container(width=4, height=60, bgcolor=severity_color, 
                           border_radius=ft.border_radius.only(top_left=4, bottom_left=4)),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(alert.title, size=13, weight=ft.FontWeight.W_600, color=self.colors["text"], expand=True),
                            ft.Container(
                                content=ft.Text(self.get_translation(f"severity_{alert.severity.value}"), 
                                               size=9, color=severity_color, weight=ft.FontWeight.W_500),
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                bgcolor=ft.Colors.with_opacity(0.1, severity_color), border_radius=10
                            )
                        ]),
                        ft.Text(alert.message[:100] + "..." if len(alert.message) > 100 else alert.message,
                               size=11, color=self.colors["text_secondary"], max_lines=2),
                        ft.Row([
                            ft.Text(alert.created_at.strftime("%H:%M"), size=9, color=self.colors["text_secondary"]),
                            ft.Text(f"{alert.value:.1f} {alert.unit}" if alert.value and alert.unit else "", 
                                   size=9, color=self.colors["text_secondary"]),
                            ft.IconButton(icon=ft.Icons.CHECK, icon_size=16, tooltip=self.get_translation("acknowledge"),
                                        on_click=lambda e, alert_id=alert.id: self.acknowledge_alert(alert_id),
                                        icon_color=self.colors["accent"])
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ], spacing=4), padding=ft.padding.all(10), expand=True
                )
            ]),
            bgcolor=self.colors["surface"], border_radius=8, border=ft.border.all(1, self.colors["border"])
        )

    def create_configuration(self):
        """Create alert configuration section."""
        if not self.weather_alerts_service:
            return ft.Container()
        
        enabled_alerts = self.weather_alerts_service.enabled_alerts
        alert_types = [
            (AlertType.TEMPERATURE_HIGH, self.get_translation("temp_high"), ft.Icons.THERMOSTAT),
            (AlertType.TEMPERATURE_LOW, self.get_translation("temp_low"), ft.Icons.AC_UNIT),
            (AlertType.WIND_STRONG, self.get_translation("wind_strong"), ft.Icons.AIR),
            (AlertType.RAIN_HEAVY, self.get_translation("rain_heavy"), ft.Icons.WATER_DROP),
            (AlertType.UV_HIGH, self.get_translation("uv_high"), ft.Icons.WB_SUNNY),
            (AlertType.AIR_QUALITY_POOR, self.get_translation("air_quality"), ft.Icons.MASKS)
        ]
        
        config_switches = []
        for alert_type, label, icon in alert_types:
            is_enabled = alert_type in enabled_alerts
            config_switches.append(ft.Row([
                ft.Icon(icon, size=16, color=self.colors["accent"]),
                ft.Text(label, size=12, color=self.colors["text"], expand=True),
                ft.Switch(value=is_enabled, on_change=lambda e, at=alert_type: self.toggle_alert_type(at, e.control.value),
                         active_color=self.colors["accent"])
            ], spacing=8))
        
        return ft.Column([
            ft.Text(self.get_translation("alert_types"), size=14, weight=ft.FontWeight.W_600, color=self.colors["text"]),
            ft.Column(config_switches, spacing=5)
        ], spacing=8)

    def create_actions(self):
        """Create dialog actions row."""
        return ft.Row([
            ft.FilledButton(
                icon=ft.Icons.SENSORS, text=self.get_translation("test_real_data"),
                on_click=self.test_real_data,
                style=ft.ButtonStyle(bgcolor=self.colors["accent"], color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=8))
            ),
            ft.FilledButton(
                icon=ft.Icons.CLEAR_ALL, text=self.get_translation("clear_all"),
                on_click=self.clear_all_alerts,
                style=ft.ButtonStyle(bgcolor=self.colors["warning"], color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=8))
            ),
            ft.FilledButton(
                icon=ft.Icons.CLOSE, text=translation_manager.get_translation(
                    'weather', 'dialog_buttons', 'close', 
                    language=self.language
                ),
                on_click=lambda e: self.close_dialog(),
                style=ft.ButtonStyle(bgcolor=self.colors["accent"], color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=8))
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def show_snackbar(self, message: str, bgcolor: str = None):
        """Show snackbar with proper error handling."""
        try:
            snackbar = ft.SnackBar(content=ft.Text(message), bgcolor=bgcolor or self.colors["success"])
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()
        except Exception:
            print(f"Message: {message}")

    async def test_real_data(self, e):
        """Test alerts with real weather data."""
        if not self.weather_alerts_service:
            return
        
        try:
            main_app = self.page.session.get('main_app')
            if not main_app:
                self.show_snackbar(self.get_translation("error_test_data"), self.colors["error"])
                return
            
            weather_view = main_app.weather_view_instance
            if not weather_view or not hasattr(weather_view, 'current_weather_data') or not weather_view.current_weather_data:
                self.show_snackbar(self.get_translation("no_weather_data"), self.colors["error"])
                return
            
            alerts = await self.weather_alerts_service.check_real_weather_conditions(
                weather_view.current_weather_data, main_app.api_service
            )
            
            if len(alerts) == 0:
                self.show_snackbar(self.get_translation("no_alerts_generated"), self.colors["success"])
            else:
                self.show_snackbar(f"{len(alerts)} " + self.get_translation("alerts_generated"), self.colors["warning"])
            
            await self.refresh_alerts(None)
            
        except Exception as ex:
            print(f"Error in test_real_data: {ex}")
            self.show_snackbar(self.get_translation("error_real_data") + f": {str(ex)}", self.colors["error"])

    async def clear_all_alerts(self, e):
        """Clear all active alerts."""
        if self.weather_alerts_service:
            active_alerts = self.weather_alerts_service.get_active_alerts()
            for alert in active_alerts:
                self.weather_alerts_service.acknowledge_alert(alert.id)
            
            self.show_snackbar(self.get_translation("all_alerts_cleared"), self.colors["success"])
            await self.refresh_alerts(None)

    async def refresh_alerts(self, e):
        """Refresh alerts display."""
        if self.dialog and hasattr(self.dialog, 'content'):
            self.update_theme_colors()
            self.dialog.title = self.create_header()
            self.dialog.content = ft.Container(
                width=min(400, self.page.width * 0.9), 
                bgcolor=self.colors["bg"],
                padding=20,
                content=ft.Column([
                    # Header migliorato con icona e stile
                    # Statistiche compatte
                    self.create_compact_statistics(),
                    # Lista allerte semplificata
                    self.create_compact_alerts_list(),
                    
                ], spacing=10, tight=True)
            )

            self.page.update()

    def create_compact_statistics(self):
        """Create compact statistics display."""
        if not self.weather_alerts_service:
            return ft.Text(self.get_translation("service_unavailable"), color=self.colors["text_secondary"], text_align=ft.TextAlign.CENTER)
        
        active_alerts = self.weather_alerts_service.get_active_alerts()
        total_alerts = len(active_alerts)
        
        if total_alerts == 0:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=self.colors["success"], size=36),
                    ft.Text(
                        self.get_translation("no_active_alerts"), 
                        size=14, color=self.colors["success"], 
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=ft.padding.all(20),
                border_radius=12,
                bgcolor=ft.Colors.with_opacity(0.05, self.colors["success"])
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color=self.colors["warning"], size=24),
                    ft.Text(
                        f"{total_alerts} {self.get_translation('alerts_active')}", 
                        size=16, weight=ft.FontWeight.W_600, 
                        color=self.colors["warning"]
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                ft.Text(
                    self.get_translation("check_details_info"), 
                    size=11, color=self.colors["text_secondary"], 
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            padding=ft.padding.all(16),
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(0.03, self.colors["warning"]),
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.colors["warning"]))
        )

    def create_compact_alerts_list(self):
        """Create compact alerts list."""
        if not self.weather_alerts_service:
            return ft.Container()
        
        active_alerts = self.weather_alerts_service.get_active_alerts()
        if not active_alerts:
            return ft.Container()
        
        # Ordina le allerte per severità
        sorted_alerts = sorted(active_alerts, key=lambda x: x.severity.value, reverse=True)
        
        alert_items = []
        for alert in sorted_alerts:
            # Mappa dei colori per severità
            severity_colors = {
                AlertSeverity.LOW: self.colors["success"], 
                AlertSeverity.MODERATE: self.colors["warning"],
                AlertSeverity.HIGH: self.colors["error"], 
                AlertSeverity.EXTREME: "#9C27B0"
            }
            
            # Icone per tipo di alert usando Flet Icons
            alert_icons = {
                AlertType.STORM: ft.Icons.THUNDERSTORM,
                AlertType.RAIN_HEAVY: ft.Icons.WATER_DROP,
                AlertType.SNOW_HEAVY: ft.Icons.AC_UNIT,
                AlertType.WIND_STRONG: ft.Icons.AIR,
                AlertType.TEMPERATURE_HIGH: ft.Icons.WB_SUNNY,
                AlertType.TEMPERATURE_LOW: ft.Icons.AC_UNIT,
                AlertType.FOG: ft.Icons.CLOUD,
                AlertType.UV_HIGH: ft.Icons.WB_SUNNY,
                AlertType.AIR_QUALITY_POOR: ft.Icons.MASKS,
                AlertType.HUMIDITY_HIGH: ft.Icons.WATER_DROP,
                AlertType.PRESSURE_LOW: ft.Icons.COMPRESS
            }
            
            color = severity_colors.get(alert.severity, self.colors["warning"])
            icon = alert_icons.get(alert.alert_type, ft.Icons.WARNING)
            
            # Traduzione del tipo di severità
            severity_key = f"alert_severity_{alert.severity.name.lower()}"
            severity_text = self.get_translation(severity_key)
            
            alert_items.append(
                ft.Container(
                    content=ft.Column([
                        # Header con icona e severità
                        ft.Row([
                            ft.Icon(icon, size=20, color=color),
                            ft.Column([
                                ft.Text(alert.title, size=13, weight=ft.FontWeight.W_600, color=self.colors["text"]),
                                ft.Row([
                                    ft.Icon(ft.Icons.KEYBOARD_ARROW_UP, size=12, color=color),
                                    ft.Text(severity_text, size=10, color=color, weight=ft.FontWeight.W_500)
                                ], spacing=2)
                            ], spacing=2, expand=True),
                            ft.Container(width=4, height=40, bgcolor=color, border_radius=2)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        # Messaggio dell'alert
                        ft.Container(
                            content=ft.Text(
                                alert.message[:80] + "..." if len(alert.message) > 80 else alert.message, 
                                size=11, color=self.colors["text_secondary"],
                                text_align=ft.TextAlign.LEFT
                            ),
                            padding=ft.padding.only(left=28)
                        )
                    ], spacing=4),
                    padding=ft.padding.all(12),
                    bgcolor=ft.Colors.with_opacity(0.03, color),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
                    border_radius=10,
                    margin=ft.margin.only(bottom=6)
                )
            )
        
        # Calcola l'altezza dinamica basata sul numero di allerte
        alert_count = len(alert_items)
        if alert_count == 0:
            return ft.Container()
        
        # Altezza minima per 1-2 allerte, massima per molte allerte
        min_height = 120
        max_height = 300
        calculated_height = min(max_height, max(min_height, alert_count * 80))
        
        return ft.Container(
            content=ft.ListView(
                controls=alert_items,
                spacing=8,
                padding=ft.padding.symmetric(vertical=4),
                auto_scroll=False
            ),
            height=calculated_height,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.colors["text"])),
            border_radius=12
        )

    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a specific alert."""
        if self.weather_alerts_service:
            success = self.weather_alerts_service.acknowledge_alert(alert_id)
            if success:
                self.show_snackbar(self.get_translation("alert_acknowledged"), self.colors["success"])
                asyncio.create_task(self.refresh_alerts(None))

    async def acknowledge_all_alerts(self, e):
        """Acknowledge all active alerts."""
        if self.weather_alerts_service:
            active_alerts = self.weather_alerts_service.get_active_alerts()
            for alert in active_alerts:
                self.weather_alerts_service.acknowledge_alert(alert.id)
            
            self.show_snackbar(f"{len(active_alerts)} " + self.get_translation("alerts_acknowledged"), self.colors["success"])
            await self.refresh_alerts(None)

    def toggle_alert_type(self, alert_type: AlertType, enabled: bool):
        """Toggle an alert type on/off."""
        if self.weather_alerts_service:
            self.weather_alerts_service.toggle_alert_type(alert_type, enabled)
            status_key = "alert_type_enabled" if enabled else "alert_type_disabled"
            self.show_snackbar(f"{alert_type.value} - " + self.get_translation(status_key),
                             self.colors["success"] if enabled else self.colors["warning"])

    def show_dialog(self):
        """Show the weather alerts dialog."""
        try:
            # Chiudi eventuali dialog esistenti usando il metodo corretto
            if self.dialog:
                self.page.close(self.dialog)
                self.dialog = None
            
            # Crea e mostra il nuovo dialog usando page.open()
            self.dialog = self.create_dialog()
            self.page.open(self.dialog)
            
        except Exception as e:
            print(f"Error showing dialog: {e}")

    def close_dialog(self):
        """Close the weather alerts dialog using page.close()."""
        try:
            if self.dialog and self.page:
                self.page.close(self.dialog)
                self.dialog = None
                
        except Exception as e:
            print(f"Error closing dialog: {e}")
            # Fallback: prova a chiudere forzatamente
            if self.dialog and self.page:
                try:
                    self.page.close(self.dialog)
                    self.dialog = None
                except Exception:
                    pass
