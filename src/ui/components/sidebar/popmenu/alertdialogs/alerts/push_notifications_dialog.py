#!/usr/bin/env python3
"""
Push Notifications Dialog for MeteoApp.
Dialog semplificato per gestire le notifiche push.
"""

import flet as ft


class PushNotificationsDialog:
    """Dialog semplificato per gestire le notifiche push."""
    
    def __init__(self, page: ft.Page = None, state_manager=None, language: str = "it", theme_handler=None):
        self.page = page
        self.state_manager = state_manager
        self.language = language
        self.theme_handler = theme_handler
        self.dialog = None
        self.colors = self.update_theme_colors()
        
        # Notification settings state
        self.notification_settings = {
            "severe_alerts": True,
            "morning_forecast": False,
            "hourly_updates": False,
            "temperature_changes": True,
            "rain_probability": True,
            "notification_time": "08:00"
        }
        
        # Register for theme and language updates if state_manager is available
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)
    
    def update_theme_colors(self):
        """Update and return theme colors based on current theme."""
        is_dark = (hasattr(self.page, 'theme_mode') and 
                  self.page.theme_mode == ft.ThemeMode.DARK)
        
        if is_dark:
            return {
                "bg": "#161b22", "surface": "#21262d", "text": "#f0f6fc",
                "text_secondary": "#8b949e", "accent": "#ff9800", "border": "#30363d"
            }
        else:
            return {
                "bg": "#ffffff", "surface": "#f6f8fa", "text": "#24292f",
                "text_secondary": "#656d76", "accent": "#ff9800", "border": "#d1d9e0"
            }
    
    def update_ui(self, event_data=None):
        """Update UI when theme or language changes."""
        if event_data and 'language' in event_data:
            self.language = event_data['language']
        
        self.colors = self.update_theme_colors()
        
        # If dialog is currently open, refresh it
        if self.dialog and hasattr(self.page, 'dialog') and self.page.dialog and self.page.dialog.open:
            self.show_dialog()
    
    def show_dialog(self):
        """Show the push notifications dialog."""
        if not self.page:
            print("ERROR: Page context not available for PushNotificationsDialog")
            return
        
        try:
            self.colors = self.update_theme_colors()
            dialog = self.create_dialog()
            
            if dialog not in self.page.controls:
                self.page.controls.append(dialog)
            
            self.page.dialog = dialog
            self.page.dialog.open = True
            self.page.update()
            
        except Exception as e:
            print(f"ERROR: Exception in show_dialog: {e}")
    
    def create_dialog(self) -> ft.AlertDialog:
        """Create the push notifications alert dialog."""
        texts = self.get_texts()
        
        # Create scrollable content
        scrollable_content = ft.Column([
            ft.Text(f"🔔 {texts['title']}", size=18, weight=ft.FontWeight.BOLD,
                   text_align=ft.TextAlign.CENTER, color=self.colors["text"]),
            ft.Divider(color=ft.Colors.with_opacity(0.3, self.colors["text"])),
            ft.Text(texts['description'], size=14, color=self.colors["text_secondary"], 
                   text_align=ft.TextAlign.CENTER),
            ft.Container(height=15),
            
            # Notification settings
            ft.Text(texts['notification_types'], size=16, weight=ft.FontWeight.BOLD, 
                   color=self.colors["text"]),
            ft.Container(height=5),
            
            self.create_notification_settings(texts),
            
            ft.Container(height=15),
            ft.Divider(color=ft.Colors.with_opacity(0.3, self.colors["text"])),
            
            # Time settings
            ft.Row([
                ft.Text(texts['notification_time'], size=14, weight=ft.FontWeight.BOLD, 
                       color=self.colors["text"]),
                ft.Dropdown(
                    width=120,
                    options=[
                        ft.dropdown.Option("07:00"),
                        ft.dropdown.Option("08:00"),
                        ft.dropdown.Option("09:00"),
                        ft.dropdown.Option("10:00")
                    ],
                    value=self.notification_settings["notification_time"],
                    on_change=self.on_time_change,
                    bgcolor=self.colors["surface"],
                    color=self.colors["text"],
                    text_size=14
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Container(height=20),
            
            # Action buttons
            ft.Row([
                ft.ElevatedButton(
                    f"💾 {texts['save_settings']}", on_click=lambda _: self.save_settings(),
                    bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]), color=self.colors["accent"],
                    width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
            
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        content = ft.Container(
            content=ft.Column([
                scrollable_content
            ], scroll=ft.ScrollMode.AUTO),
            padding=20, width=450, height=400, bgcolor=self.colors["bg"]
        )
        
        return ft.AlertDialog(
            modal=False, scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.NOTIFICATIONS, color=self.colors["accent"], size=24),
                ft.Text(texts['dialog_title'], weight=ft.FontWeight.BOLD, color=self.colors["text"], size=18)
            ], spacing=10),
            content=content,
            actions=[ft.FilledButton(
                icon=ft.Icons.CLOSE, text=texts['close'], on_click=self.close_dialog,
                style=ft.ButtonStyle(bgcolor=self.colors["accent"], color=ft.Colors.WHITE,
                                   shape=ft.RoundedRectangleBorder(radius=8))
            )],
            actions_alignment=ft.MainAxisAlignment.END, bgcolor=self.colors["bg"],
            title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
            content_text_style=ft.TextStyle(size=14, color=self.colors["text"]),
            inset_padding=ft.padding.all(20)
        )
    
    def create_notification_settings(self, texts):
        """Create notification settings checkboxes."""
        return ft.Column([
            ft.Checkbox(
                label=texts['severe_alerts'], 
                value=self.notification_settings["severe_alerts"],
                on_change=lambda e: self.update_setting("severe_alerts", e.control.value),
                active_color=self.colors["accent"],
                label_style=ft.TextStyle(size=14)
            ),
            ft.Checkbox(
                label=texts['morning_forecast'], 
                value=self.notification_settings["morning_forecast"],
                on_change=lambda e: self.update_setting("morning_forecast", e.control.value),
                active_color=self.colors["accent"],
                label_style=ft.TextStyle(size=14)
            ),
            ft.Checkbox(
                label=texts['hourly_updates'], 
                value=self.notification_settings["hourly_updates"],
                on_change=lambda e: self.update_setting("hourly_updates", e.control.value),
                active_color=self.colors["accent"],
                label_style=ft.TextStyle(size=14)
            ),
            ft.Checkbox(
                label=texts['temperature_changes'], 
                value=self.notification_settings["temperature_changes"],
                on_change=lambda e: self.update_setting("temperature_changes", e.control.value),
                active_color=self.colors["accent"],
                label_style=ft.TextStyle(size=14)
            ),
            ft.Checkbox(
                label=texts['rain_probability'], 
                value=self.notification_settings["rain_probability"],
                on_change=lambda e: self.update_setting("rain_probability", e.control.value),
                active_color=self.colors["accent"],
                label_style=ft.TextStyle(size=14)
            )
        ], spacing=5)
    
    def update_setting(self, setting_key: str, value: bool):
        """Update a notification setting."""
        self.notification_settings[setting_key] = value
    
    def on_time_change(self, e):
        """Handle notification time change."""
        self.notification_settings["notification_time"] = e.control.value
    
    def get_texts(self):
        """Get localized texts based on current language."""
        if self.language == "en":
            return {
                "title": "Push Notifications", "dialog_title": "Push Notifications",
                "description": "Configure push notifications to receive important weather updates",
                "notification_types": "Notification Types",
                "severe_alerts": "Severe weather alerts",
                "morning_forecast": "Morning forecasts",
                "hourly_updates": "Hourly updates",
                "temperature_changes": "Temperature changes",
                "rain_probability": "Rain probability",
                "notification_time": "Notification Time:",
                "save_settings": "Save Settings", "close": "Close"
            }
        else:  # Italian (default)
            return {
                "title": "Notifiche Push", "dialog_title": "Notifiche Push",
                "description": "Configura le notifiche push per ricevere aggiornamenti meteo importanti",
                "notification_types": "Tipi di Notifica",
                "severe_alerts": "Allerte meteo severe",
                "morning_forecast": "Previsioni mattutine",
                "hourly_updates": "Aggiornamenti orari",
                "temperature_changes": "Cambiamenti di temperatura",
                "rain_probability": "Probabilità di pioggia",
                "notification_time": "Orario Notifiche:",
                "save_settings": "Salva Impostazioni", "close": "Chiudi"
            }
    
    def save_settings(self):
        """Save notification settings."""
        if self.page:
            # TODO: Implement actual settings save to state manager or preferences
            active_count = sum(1 for key, value in self.notification_settings.items() 
                             if key != "notification_time" and value)
            
            message = f"Impostazioni salvate: {active_count} notifiche attive alle {self.notification_settings['notification_time']}"
            
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=self.colors["accent"]
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def close_dialog(self, e=None):
        """Close the dialog."""
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def cleanup(self):
        """Cleanup method to unregister observers."""
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
            self.state_manager.unregister_observer("theme_event", self.update_ui)
