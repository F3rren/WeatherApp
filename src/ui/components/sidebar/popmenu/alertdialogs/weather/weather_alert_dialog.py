import asyncio
import flet as ft
from services.alerts.weather_alerts_service import AlertSeverity, AlertType
from services.ui.translation_service import TranslationService

class WeatherAlertDialog:
    """Dialog dedicato esclusivamente alla gestione delle allerte meteo."""

    def __init__(self, page: ft.Page, state_manager=None, language: str = "en"):
        self.page = page
        self.state_manager = state_manager
        self.language = language
        self.dialog = None
        self._original_on_click = None
        
        # Get weather alerts service from session
        self.weather_alerts_service = self.page.session.get('weather_alerts_service') if self.page else None
        
        # Theme colors
        self._update_theme_colors()

    def _update_theme_colors(self):
        """Update theme colors based on current theme."""
        is_dark = False
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        
        if is_dark:
            self.colors = {
                "bg": "#161b22",
                "surface": "#21262d", 
                "text": "#f0f6fc",
                "text_secondary": "#8b949e",
                "accent": "#58a6ff",
                "border": "#30363d",
                "success": "#238636",
                "warning": "#d29922",
                "error": "#f85149",
                "purple": "#a5a2ff"
            }
        else:
            self.colors = {
                "bg": "#ffffff",
                "surface": "#f6f8fa",
                "text": "#24292f",
                "text_secondary": "#656d76", 
                "accent": "#0969da",
                "border": "#d1d9e0",
                "success": "#1a7f37",
                "warning": "#bf8700",
                "error": "#cf222e",
                "purple": "#8250df"
            }

    def build(self):
        """Build the weather alerts dialog."""
        self._update_theme_colors()
        
        # Ensure weather alerts service is available
        if not self.weather_alerts_service:
            # Try to get it from session again
            self.weather_alerts_service = self.page.session.get('weather_alerts_service') if self.page and self.page.session else None
        
        # If still not available, show error dialog
        if not self.weather_alerts_service:
            return self._build_error_dialog(TranslationService.translate_from_dict("weather_alert_dialog_items", "service_unavailable", self.language))
        
        try:
            return ft.AlertDialog(
                modal=False,
                title=self._build_header(),
                #scrollable=True,  # Make dialog scrollable
                bgcolor=self.colors["bg"],
                content=ft.Container(
                    width=600,
                    height=500,
                    bgcolor=self.colors["bg"],
                    content=ft.Column(
                        controls=[
                            # Alert statistics
                            self._build_alert_statistics(),
                            ft.Divider(color=self.colors["border"], height=1),
                            
                            # Active alerts list
                            self._build_alerts_list(),
                            ft.Divider(color=self.colors["border"], height=1),
                            
                            # Alert configuration
                            self._build_alert_configuration(),
                        ],
                        spacing=15,
                        scroll=ft.ScrollMode.AUTO
                    )
                ),
                actions=[
                    ft.Row(
                        controls=[
                            ft.FilledButton(
                                icon=ft.Icons.SENSORS,
                                text=TranslationService.translate_from_dict("weather_alert_dialog_items", "test_real_data", self.language),
                                on_click=self._test_real_data,
                                style=ft.ButtonStyle(
                                    bgcolor=self.colors["accent"],
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                )
                            ),
                            ft.FilledButton(
                                icon=ft.Icons.CLEAR_ALL,
                                text=TranslationService.translate_from_dict("weather_alert_dialog_items", "clear_all", self.language),
                                on_click=self._clear_all_alerts,                               
                                style=ft.ButtonStyle(
                                    bgcolor=self.colors["warning"],
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                )
                            ),
                            ft.FilledButton(
                                icon=ft.Icons.CLOSE,
                                text=TranslationService.translate_from_dict("dialog_buttons", "close", self.language),
                                on_click=lambda e: self.close_dialog(),
                                style=ft.ButtonStyle(
                                    bgcolor=self.colors["accent"],
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ],
            )
        except Exception as e:
            print(f"Error building weather alert dialog: {e}")
            return self._build_error_dialog(f"Errore nella creazione del dialogo: {str(e)}")

    def _build_error_dialog(self, message: str):
        """Build an error dialog when the main dialog cannot be created."""
        return ft.AlertDialog(
            modal=False,
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ERROR_OUTLINE, color=self.colors["error"], size=24),
                    ft.Text(
                        "Errore Allerte Meteo",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=self.colors["text"]
                    )
                ],
                spacing=10
            ),
            #scrollable=True,  # Make dialog scrollable
            bgcolor=self.colors["bg"],
            content=ft.Container(
                width=400,
                height=200,
                bgcolor=self.colors["bg"],
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=48, color=self.colors["warning"]),
                        ft.Text(
                            message,
                            size=14,
                            color=self.colors["text"],
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Riprova più tardi o riavvia l'applicazione",
                            size=12,
                            color=self.colors["text_secondary"],
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ),
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            text=TranslationService.translate_from_dict("dialog_buttons", "retry", self.language),
                            icon=ft.Icons.REFRESH,
                            on_click=lambda e: self._retry_dialog(),
                            style=ft.ButtonStyle(color=self.colors["accent"])
                        ),
                        ft.FilledButton(
                            text=TranslationService.translate_from_dict("dialog_buttons", "close", self.language),
                            on_click=lambda e: self.close_dialog(),
                            style=ft.ButtonStyle(
                                bgcolor=self.colors.get("accent", ft.Colors.BLUE),
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
        )

    def _retry_dialog(self):
        """Retry building and showing the dialog."""
        try:
            # Try to get weather alerts service again
            self.weather_alerts_service = self.page.session.get('weather_alerts_service') if self.page and self.page.session else None
            
            if self.weather_alerts_service:
                # Close current error dialog
                self.close_dialog()
                # Show the proper dialog
                self.show_dialog()
            else:
                # Show snackbar message
                self._show_snackbar(TranslationService.translate_from_dict("weather_alert_dialog_items", "service_unavailable", self.language), self.colors["error"])
        except Exception as e:
            print(f"Error retrying dialog: {e}")
            self._show_snackbar(f"Errore nel riprovare: {str(e)}", self.colors["error"])

    def _build_header(self):
        """Build dialog header with title and status."""
        active_count = len(self.weather_alerts_service.get_active_alerts()) if self.weather_alerts_service else 0
        
        return ft.Row(
            controls=[
                ft.Icon(ft.Icons.WARNING_ROUNDED, color=self.colors["warning"], size=24),
                ft.Column(
                    controls=[
                        ft.Text(
                            TranslationService.translate_from_dict("weather_alert_dialog_items", "weather_alerts", self.language),
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=self.colors["text"]
                        ),
                        ft.Text(
                            f"{active_count} " + TranslationService.translate_from_dict("weather_alert_dialog_items", "active_alerts_count", self.language),
                            size=12,
                            color=self.colors["text_secondary"]
                        )
                    ],
                    spacing=2,
                    expand=True
                ),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    tooltip=TranslationService.translate_from_dict("weather_alert_dialog_items", "refresh", self.language),
                    on_click=self._refresh_alerts,
                    icon_color=self.colors["accent"]
                )
            ],
            spacing=10
        )

    def _build_alert_statistics(self):
        """Build alert statistics section."""
        if not self.weather_alerts_service:
            return ft.Container()
        
        active_alerts = self.weather_alerts_service.get_active_alerts()
        
        # Count by severity
        severity_counts = {
            AlertSeverity.LOW: 0,
            AlertSeverity.MODERATE: 0, 
            AlertSeverity.HIGH: 0,
            AlertSeverity.EXTREME: 0
        }
        
        for alert in active_alerts:
            severity_counts[alert.severity] += 1
        
        severity_cards = []
        severity_info = [
            (AlertSeverity.LOW, self._get_translation("severity_low"), self.colors["success"]),
            (AlertSeverity.MODERATE, self._get_translation("severity_moderate"), self.colors["warning"]),
            (AlertSeverity.HIGH, self._get_translation("severity_high"), self.colors["error"]),
            (AlertSeverity.EXTREME, self._get_translation("severity_extreme"), self.colors["purple"])
        ]
        
        for severity, label, color in severity_info:
            count = severity_counts[severity]
            severity_cards.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(str(count), size=20, weight=ft.FontWeight.BOLD, color=color),
                            ft.Text(label, size=10, color=self.colors["text_secondary"])
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(8),
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    border_radius=8,
                    width=80
                )
            )
        
        return ft.Column(
            controls=[
                ft.Text(
                    self._get_translation("alert_statistics"),
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=self.colors["text"]
                ),
                ft.Row(
                    controls=severity_cards,
                    spacing=10,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                )
            ],
            spacing=8
        )

    def _build_alerts_list(self):
        """Build active alerts list."""
        if not self.weather_alerts_service:
            return ft.Container(
                content=ft.Text(
                    self._get_translation("service_unavailable"),
                    color=self.colors["text_secondary"]
                ),
                padding=20
            )
        
        active_alerts = self.weather_alerts_service.get_active_alerts()
        
        if not active_alerts:
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=48, color=self.colors["success"]),
                        ft.Text(
                            self._get_translation("no_active_alerts"),
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=self.colors["success"]
                        ),
                        ft.Text(
                            self._get_translation("all_clear"),
                            size=12,
                            color=self.colors["text_secondary"]
                        )
                    ],
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20
            )
        
        alert_cards = []
        for alert in active_alerts[:10]:  # Show max 10 alerts
            alert_cards.append(self._build_alert_card(alert))
        
        if len(active_alerts) > 10:
            alert_cards.append(
                ft.Container(
                    content=ft.Text(
                        f"+{len(active_alerts) - 10} " + self._get_translation("more_alerts"),
                        color=self.colors["text_secondary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=10
                )
            )
        
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            self._get_translation("active_alerts"),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=self.colors["text"]
                        ),
                        ft.TextButton(
                            text=self._get_translation("acknowledge_all"),
                            icon=ft.Icons.DONE_ALL,
                            on_click=self._acknowledge_all_alerts,
                            style=ft.ButtonStyle(color=self.colors["accent"])
                        ) if active_alerts else ft.Container()
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Column(
                    controls=alert_cards,
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                    height=200
                )
            ],
            spacing=8
        )

    def _build_alert_card(self, alert):
        """Build individual alert card."""
        severity_color = self._get_severity_color(alert.severity)
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Severity indicator
                    ft.Container(
                        width=4,
                        height=60,
                        bgcolor=severity_color,
                        border_radius=ft.border_radius.only(
                            top_left=4, bottom_left=4
                        )
                    ),
                    # Alert content
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            alert.title,
                                            size=13,
                                            weight=ft.FontWeight.W_600,
                                            color=self.colors["text"],
                                            expand=True
                                        ),
                                        ft.Container(
                                            content=ft.Text(
                                                self._get_translation(f"severity_{alert.severity.value}"),
                                                size=9,
                                                color=severity_color,
                                                weight=ft.FontWeight.W_500
                                            ),
                                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                            bgcolor=ft.Colors.with_opacity(0.1, severity_color),
                                            border_radius=10
                                        )
                                    ]
                                ),
                                ft.Text(
                                    alert.message[:100] + "..." if len(alert.message) > 100 else alert.message,
                                    size=11,
                                    color=self.colors["text_secondary"],
                                    max_lines=2
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            alert.created_at.strftime("%H:%M"),
                                            size=9,
                                            color=self.colors["text_secondary"]
                                        ),
                                        ft.Text(
                                            f"{alert.value:.1f} {alert.unit}" if alert.value and alert.unit else "",
                                            size=9,
                                            color=self.colors["text_secondary"]
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.CHECK,
                                            icon_size=16,
                                            tooltip=self._get_translation("acknowledge"),
                                            on_click=lambda e, alert_id=alert.id: self._acknowledge_alert(alert_id),
                                            icon_color=self.colors["accent"]
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ],
                            spacing=4
                        ),
                        padding=ft.padding.all(10),
                        expand=True
                    )
                ]
            ),
            bgcolor=self.colors["surface"],
            border_radius=8,
            border=ft.border.all(1, self.colors["border"])
        )

    def _build_alert_configuration(self):
        """Build alert configuration section."""
        if not self.weather_alerts_service:
            return ft.Container()
        
        enabled_alerts = self.weather_alerts_service.enabled_alerts
        alert_types = [
            (AlertType.TEMPERATURE_HIGH, self._get_translation("temp_high"), ft.Icons.THERMOSTAT),
            (AlertType.TEMPERATURE_LOW, self._get_translation("temp_low"), ft.Icons.AC_UNIT),
            (AlertType.WIND_STRONG, self._get_translation("wind_strong"), ft.Icons.AIR),
            (AlertType.RAIN_HEAVY, self._get_translation("rain_heavy"), ft.Icons.WATER_DROP),
            (AlertType.UV_HIGH, self._get_translation("uv_high"), ft.Icons.WB_SUNNY),
            (AlertType.AIR_QUALITY_POOR, self._get_translation("air_quality"), ft.Icons.MASKS)
        ]
        
        config_switches = []
        for alert_type, label, icon in alert_types:
            is_enabled = alert_type in enabled_alerts
            config_switches.append(
                ft.Row(
                    controls=[
                        ft.Icon(icon, size=16, color=self.colors["accent"]),
                        ft.Text(
                            label,
                            size=12,
                            color=self.colors["text"],
                            expand=True
                        ),
                        ft.Switch(
                            value=is_enabled,
                            on_change=lambda e, at=alert_type: self._toggle_alert_type(at, e.control.value),
                            active_color=self.colors["accent"]
                        )
                    ],
                    spacing=8
                )
            )
        
        return ft.Column(
            controls=[
                ft.Text(
                    self._get_translation("alert_types"),
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=self.colors["text"]
                ),
                ft.Column(
                    controls=config_switches,
                    spacing=5
                )
            ],
            spacing=8
        )

    def _get_translation(self, key: str) -> str:
        """Get translation for a key using the centralized translation service."""
        return TranslationService.translate_from_dict("weather_alert_dialog_items", key, self.language)

    def _show_snackbar(self, message: str, bgcolor: str = None):
        """Helper method to show snackbar with proper error handling."""
        try:
            snackbar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=bgcolor or self.colors["success"]
            )
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()
        except Exception:
            # Fallback: just print to console if snackbar fails
            print(f"Message: {message}")

    def _get_severity_color(self, severity: AlertSeverity) -> str:
        """Get color for alert severity."""
        color_map = {
            AlertSeverity.LOW: self.colors["success"],
            AlertSeverity.MODERATE: self.colors["warning"],
            AlertSeverity.HIGH: self.colors["error"],
            AlertSeverity.EXTREME: self.colors["purple"]
        }
        return color_map.get(severity, self.colors["warning"])

    async def _test_real_data(self, e):
        """Test alerts with real weather data."""
        if self.weather_alerts_service:
            try:
                print("Testing alerts with real weather data...")
                
                # Get the API service and current weather data from the main app
                main_app = self.page.session.get('main_app')
                if not main_app:
                    self._show_snackbar(
                        TranslationService.translate_from_dict("weather_alert_dialog_items", "error_test_data", self.language),
                        self.colors["error"]
                    )
                    return
                
                api_service = main_app.api_service
                weather_view = main_app.weather_view_instance
                
                if not weather_view or not hasattr(weather_view, 'current_weather_data'):
                    self._show_snackbar(
                        TranslationService.translate_from_dict("weather_alert_dialog_items", "no_weather_data", self.language),
                        self.colors["error"]
                    )
                    return
                
                weather_data = weather_view.current_weather_data
                if not weather_data:
                    self._show_snackbar(
                        TranslationService.translate_from_dict("weather_alert_dialog_items", "weather_data_not_loaded", self.language),
                        self.colors["error"]
                    )
                    return
                
                # Test with real weather data
                alerts = await self.weather_alerts_service.check_real_weather_conditions(
                    weather_data, api_service
                )
                
                print(f"Generated {len(alerts)} alerts from real data")
                
                if len(alerts) == 0:
                    self._show_snackbar(
                        TranslationService.translate_from_dict("weather_alert_dialog_items", "no_alerts_generated", self.language),
                        self.colors["success"]
                    )
                else:
                    self._show_snackbar(
                        f"{len(alerts)} " + TranslationService.translate_from_dict("weather_alert_dialog_items", "alerts_generated", self.language),
                        self.colors["warning"]
                    )
                
                # Refresh the display immediately
                await self._refresh_alerts(None)
                print("Dialog refreshed successfully")
                
            except Exception as ex:
                print(f"Error in test_real_data: {ex}")
                self._show_snackbar(
                    TranslationService.translate_from_dict("weather_alert_dialog_items", "error_real_data", self.language) + f": {str(ex)}",
                    self.colors["error"]
                )

    async def _clear_all_alerts(self, e):
        """Clear all active alerts."""
        if self.weather_alerts_service:
            active_alerts = self.weather_alerts_service.get_active_alerts()
            for alert in active_alerts:
                self.weather_alerts_service.acknowledge_alert(alert.id)
            
            self._show_snackbar(
                TranslationService.translate_from_dict("weather_alert_dialog_items", "all_alerts_cleared", self.language),
                self.colors["success"]
            )
            await self._refresh_alerts(None)

    async def _refresh_alerts(self, e):
        """Refresh alerts display."""
        if self.dialog and hasattr(self.dialog, 'content'):
            # Update theme colors first
            self._update_theme_colors()
            
            # Rebuild dialog title (header)
            self.dialog.title = self._build_header()
            
            # Rebuild dialog content
            self.dialog.content = ft.Container(
                width=600,
                height=500,
                bgcolor=self.colors["bg"],
                content=ft.Column(
                    controls=[
                        self._build_alert_statistics(),
                        ft.Divider(color=self.colors["border"], height=1),
                        self._build_alerts_list(),
                        ft.Divider(color=self.colors["border"], height=1),
                        self._build_alert_configuration(),
                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO
                )
            )
            
            # Force update the entire dialog
            self.page.update()

    def _acknowledge_alert(self, alert_id: str):
        """Acknowledge a specific alert."""
        if self.weather_alerts_service:
            success = self.weather_alerts_service.acknowledge_alert(alert_id)
            if success:
                self._show_snackbar(
                    TranslationService.translate_from_dict("weather_alert_dialog_items", "alert_acknowledged", self.language),
                    self.colors["success"]
                )
                # Refresh the display
                asyncio.create_task(self._refresh_alerts(None))

    async def _acknowledge_all_alerts(self, e):
        """Acknowledge all active alerts."""
        if self.weather_alerts_service:
            active_alerts = self.weather_alerts_service.get_active_alerts()
            for alert in active_alerts:
                self.weather_alerts_service.acknowledge_alert(alert.id)
            
            self._show_snackbar(
                f"{len(active_alerts)} " + TranslationService.translate_from_dict("weather_alert_dialog_items", "alerts_acknowledged", self.language),
                self.colors["success"]
            )
            await self._refresh_alerts(None)

    def _toggle_alert_type(self, alert_type: AlertType, enabled: bool):
        """Toggle an alert type on/off."""
        if self.weather_alerts_service:
            self.weather_alerts_service.toggle_alert_type(alert_type, enabled)
            status_key = "alert_type_enabled" if enabled else "alert_type_disabled"
            self._show_snackbar(
                f"{alert_type.value} - " + TranslationService.translate_from_dict("weather_alert_dialog_items", status_key, self.language),
                self.colors["success"] if enabled else self.colors["warning"]
            )

    def show_dialog(self):
        """Show the weather alerts dialog."""
        try:
            # Build new dialog
            self.dialog = self.build()
            
            # Add to overlay only if not already present
            if self.dialog not in self.page.overlay:
                self.page.overlay.append(self.dialog)
                
            # Store original page click handler
            self._original_on_click = getattr(self.page, 'on_click', None)
            
            # Add click outside handler
            def handle_page_click(e):
                # Close dialog when clicking outside
                self.close_dialog()
            
            self.page.on_click = handle_page_click
                
            self.dialog.open = True
            self.page.update()
        except Exception as e:
            print(f"Error showing dialog: {e}")

    def close_dialog(self):
        """Close the weather alerts dialog."""
        try:
            if self.dialog:
                self.dialog.open = False
                
                # Restore original page click handler
                if hasattr(self, '_original_on_click'):
                    self.page.on_click = self._original_on_click
                    delattr(self, '_original_on_click')
                else:
                    self.page.on_click = None
                
                self.page.update()
                
                # Optional: Remove from overlay after a short delay to ensure proper cleanup
                if hasattr(self.page, 'run_task'):
                    async def cleanup_overlay():
                        await asyncio.sleep(0.1)
                        try:
                            if self.dialog in self.page.overlay:
                                self.page.overlay.remove(self.dialog)
                                self.page.update()
                        except Exception as e:
                            print(f"Overlay cleanup warning: {e}")
                    
                    self.page.run_task(cleanup_overlay)
        except Exception as e:
            print(f"Error closing dialog: {e}")
