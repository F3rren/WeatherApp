#!/usr/bin/env python3
"""
Push Notifications Dialog for MeteoApp.
Dialog semplificato per gestire le notifiche push.
"""

import flet as ft
from translations import translation_manager
from utils.responsive_utils import ResponsiveTextFactory


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
    
    def _get_translation(self, key: str) -> str:
        """Get translation for the given key using the modular translation system."""
        try:
            return translation_manager.get_translation("weather", "push_notifications_dialog", key, self.language)
        except Exception as e:
            print(f"Translation error for key 'push_notifications_dialog.{key}': {e}")
            return key.replace('_', ' ').title()  # Fallback
    
    def update_theme_colors(self):
        """Update and return theme colors based on current theme."""
        is_dark = (self.page and hasattr(self.page, 'theme_mode') and 
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
        
        # Create scrollable content
        scrollable_content = ft.Column([
            ft.Icon(ft.Icons.NOTIFICATIONS, size=24, color=self.colors["accent"]),
            ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=f"{self._get_translation('title')}",
                text_type="title_small",
                color=self.colors["text"],
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Divider(color=ft.Colors.with_opacity(0.3, self.colors["text"])),
            ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=self._get_translation('description'),
                text_type="body_primary",
                color=self.colors["text_secondary"],
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=15),
            
            # Notification settings
            ResponsiveTextFactory.create_adaptive_text(
                page=self.page,
                text=self._get_translation('notification_types'),
                text_type="title_small",
                color=self.colors["text"],
                weight=ft.FontWeight.BOLD
            ),
            ft.Container(height=5),
            
            self.create_notification_settings(),
            
            ft.Container(height=15),
            ft.Divider(color=ft.Colors.with_opacity(0.3, self.colors["text"])),
            
            # Time settings
            ft.Row([
                ResponsiveTextFactory.create_adaptive_text(
                    page=self.page,
                    text=self._get_translation('notification_time'),
                    text_type="body_primary",
                    color=self.colors["text"],
                    weight=ft.FontWeight.BOLD
                ),
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
                    icon=ft.Icons.SAVE,
                    text=f"{self._get_translation('save_settings')}", 
                    on_click=lambda _: self.save_settings(),
                    bgcolor=ft.Colors.with_opacity(0.1, self.colors["accent"]), 
                    color=self.colors["accent"],
                    width=200, 
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
            
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        content = ft.Container(
            content=ft.Column([
                scrollable_content
            ], tight=True),
            padding=20, width=min(400, self.page.width * 0.9), bgcolor=self.colors["bg"]
        )
        
        return ft.AlertDialog(
            modal=False, scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.NOTIFICATIONS, color=self.colors["accent"], size=24),
                ResponsiveTextFactory.create_adaptive_text(
                    page=self.page,
                    text=self._get_translation('dialog_title'),
                    text_type="title_small",
                    color=self.colors["text"],
                    weight=ft.FontWeight.BOLD
                )
            ], spacing=10),
            content=content,
            actions=[ft.FilledButton(
                icon=ft.Icons.CLOSE, text=translation_manager.get_translation("weather", "dialog_buttons", "close", self.language), on_click=self.close_dialog,
                style=ft.ButtonStyle(bgcolor=self.colors["accent"], color=ft.Colors.WHITE,
                                   shape=ft.RoundedRectangleBorder(radius=8))
            )],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=self.colors["bg"],
            title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
            content_text_style=ft.TextStyle(size=14, color=self.colors["text"]),
            inset_padding=ft.padding.all(20)
        )
    
    def create_notification_settings(self):
        """Create notification settings checkboxes."""
        return ft.Column([
            ft.Checkbox(
                label=self._get_translation('severe_alerts'), 
                value=self.notification_settings["severe_alerts"],
                on_change=lambda e: self.update_setting("severe_alerts", e.control.value),
                active_color=self.colors["accent"],
                label_style=ft.TextStyle(size=14)
            ),
            ft.Checkbox(
                label=self._get_translation('morning_forecast'), 
                value=self.notification_settings["morning_forecast"],
                on_change=lambda e: self.update_setting("morning_forecast", e.control.value),
                active_color=self.colors["accent"],
                label_style=ft.TextStyle(size=14)
            ),
            ft.Checkbox(
                label=self._get_translation('hourly_updates'), 
                value=self.notification_settings["hourly_updates"],
                on_change=lambda e: self.update_setting("hourly_updates", e.control.value),
                active_color=self.colors["accent"],
                label_style=ft.TextStyle(size=14)
            ),
            ft.Checkbox(
                label=self._get_translation('temperature_changes'), 
                value=self.notification_settings["temperature_changes"],
                on_change=lambda e: self.update_setting("temperature_changes", e.control.value),
                active_color=self.colors["accent"],
                label_style=ft.TextStyle(size=14)
            ),
            ft.Checkbox(
                label=self._get_translation('rain_probability'), 
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
    
    def save_settings(self):
        """Save notification settings."""
        if self.page:
            # TODO: Implement actual settings save to state manager or preferences
            active_count = sum(1 for key, value in self.notification_settings.items() 
                             if key != "notification_time" and value)
            
            message = self._get_translation('settings_saved').format(
                count=active_count, 
                time=self.notification_settings['notification_time']
            )
            
            self.page.snack_bar = ft.SnackBar(
                content=ResponsiveTextFactory.create_adaptive_text(
                    page=self.page,
                    text=message,
                    text_type="body_primary",
                    color=ft.Colors.WHITE
                ),
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
