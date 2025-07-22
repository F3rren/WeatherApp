import flet as ft
from src.core.state_manager import StateManager


class ExportDataDialog:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state_manager = StateManager()
        self.theme = self.state_manager.get_state("theme", "light")
        self.language = self.state_manager.get_state("language", "italian")
        
        # Centralized color management  
        self.colors = {}
        self.update_theme_colors()
        
        # Register observers
        self.state_manager.register_observer("language_event", self.update_ui)
        self.state_manager.register_observer("theme_event", self.update_ui)
        
        # Dialog components
        self.dialog = None
        self.period_radio = None
        self.data_checkboxes = {}
        self.format_dropdown = None
    
    def update_theme_colors(self):
        """Update theme colors based on current theme."""
        if self.theme == "dark":
            self.colors.update({
                "bg": "#1E1E1E", "surface": "#2D2D2D", "text": "#FFFFFF", 
                "text_secondary": "#B0B0B0", "border": "#404040", "accent": "#3F51B5"
            })
        else:  # light
            self.colors.update({
                "bg": "#FFFFFF", "surface": "#F5F5F5", "text": "#212121", 
                "text_secondary": "#757575", "border": "#E0E0E0", "accent": "#3F51B5"
            })
    
    def update_ui(self, event=None):
        """Update UI when theme or language changes."""
        if event and event.get("type") == "theme_event":
            self.theme = event.get("data", "light")
            self.update_theme_colors()
        elif event and event.get("type") == "language_event":
            self.language = event.get("data", "italian")
        
        if self.page and self.dialog and self.dialog.open:
            self.show_dialog()  # Refresh dialog with new settings
    
    def show_dialog(self):
        """Show the export data dialog."""
        if self.dialog and self.dialog in self.page.overlay:
            self.page.overlay.remove(self.dialog)
        
        self.dialog = self.create_dialog()
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def create_dialog(self):
        """Create the export data dialog."""
        texts = self.get_texts()
        
        # Period selection
        self.period_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="week", label=texts['week']),
                ft.Radio(value="month", label=texts['month']),
                ft.Radio(value="year", label=texts['year']),
                ft.Radio(value="custom", label=texts['custom']),
            ]),
            value="week"
        )
        
        # Data type checkboxes
        self.data_checkboxes = {
            "temperature": ft.Checkbox(label=texts['temperature'], value=True),
            "humidity": ft.Checkbox(label=texts['humidity'], value=True),
            "precipitation": ft.Checkbox(label=texts['precipitation'], value=False),
            "wind": ft.Checkbox(label=texts['wind'], value=False),
            "pressure": ft.Checkbox(label=texts['pressure'], value=False),
        }
        
        # Format dropdown
        self.format_dropdown = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("csv", "CSV"),
                ft.dropdown.Option("excel", "Excel (.xlsx)"),
                ft.dropdown.Option("json", "JSON"),
                ft.dropdown.Option("pdf", "PDF Report"),
            ],
            value="csv",
            bgcolor=self.colors["surface"],
            color=self.colors["text"],
            border_color=self.colors["border"]
        )
        
        # Main content
        content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.DOWNLOAD, size=48, color=self.colors["accent"]),
                ft.Text(texts['description'], text_align=ft.TextAlign.CENTER, 
                       size=14, color=self.colors["text_secondary"]),
                
                ft.Divider(color=self.colors["border"]),
                
                # Period selection section
                ft.Text(texts['select_period'], weight=ft.FontWeight.BOLD, 
                       color=self.colors["text"], size=16),
                self.period_radio,
                
                ft.Divider(color=self.colors["border"]),
                
                # Data selection section
                ft.Text(texts['select_data'], weight=ft.FontWeight.BOLD, 
                       color=self.colors["text"], size=16),
                ft.Column([checkbox for checkbox in self.data_checkboxes.values()], spacing=5),
                
                ft.Divider(color=self.colors["border"]),
                
                # Format selection section  
                ft.Text(texts['select_format'], weight=ft.FontWeight.BOLD, 
                       color=self.colors["text"], size=16),
                self.format_dropdown,
                
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            width=400, height=500, padding=20, bgcolor=self.colors["bg"]
        )
        
        return ft.AlertDialog(
            modal=False, scrollable=True,
            title=ft.Row([
                ft.Icon(ft.Icons.DOWNLOAD, color=self.colors["accent"], size=24),
                ft.Text(texts['dialog_title'], weight=ft.FontWeight.BOLD, color=self.colors["text"])
            ], spacing=10),
            content=content,
            actions=[
                ft.TextButton(
                    icon=ft.Icons.SAVE, text=texts['export'], on_click=self.export_data,
                    style=ft.ButtonStyle(bgcolor="#4CAF50", color=ft.Colors.WHITE,
                                       shape=ft.RoundedRectangleBorder(radius=8))
                ),
                ft.FilledButton(
                    icon=ft.Icons.CLOSE, text=texts['close'], on_click=self.close_dialog,
                    style=ft.ButtonStyle(bgcolor=self.colors["accent"], color=ft.Colors.WHITE,
                                       shape=ft.RoundedRectangleBorder(radius=8))
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END, bgcolor=self.colors["bg"],
            title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
            content_text_style=ft.TextStyle(size=14, color=self.colors["text"]),
            inset_padding=ft.padding.all(20)
        )
    
    def get_texts(self):
        """Get localized texts based on current language."""
        if self.language == "en":
            return {
                "title": "Export Data", "dialog_title": "Export Data",
                "description": "Export weather data in various formats",
                "select_period": "Select Period:", "select_data": "Select Data:",
                "select_format": "Export Format:", "week": "Last Week",
                "month": "Last Month", "year": "Last Year", "custom": "Custom Period",
                "temperature": "Temperature", "humidity": "Humidity",
                "precipitation": "Precipitation", "wind": "Wind", "pressure": "Pressure",
                "export": "Export", "close": "Close"
            }
        else:  # Italian (default)
            return {
                "title": "Esporta Dati", "dialog_title": "Esporta Dati",
                "description": "Esporta i dati meteorologici in diversi formati",
                "select_period": "Seleziona Periodo:", "select_data": "Seleziona Dati:",
                "select_format": "Formato Esportazione:", "week": "Ultima Settimana",
                "month": "Ultimo Mese", "year": "Ultimo Anno", "custom": "Periodo Personalizzato",
                "temperature": "Temperature", "humidity": "Umidità",
                "precipitation": "Precipitazioni", "wind": "Vento", "pressure": "Pressione",
                "export": "Esporta", "close": "Chiudi"
            }
    
    def export_data(self, e=None):
        """Export the selected data."""
        # Simulate export process (in real app would actually export the data)
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Esportazione dati completata!"),
                bgcolor="#4CAF50"
            )
            self.page.snack_bar.open = True
            self.page.update()
        
        # Close dialog after export
        self.close_dialog()
    
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
