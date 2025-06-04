import flet as ft
from typing import List
from config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class TemperatureChart:
    """
    Temperature chart display.
    """
    
    def __init__(self, page: ft.Page, days: List[str], temp_min: List[int], 
                 temp_max: List[int], text_color: str):
        self.page = page
        self.days = days
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.text_color = text_color # Initial text color

        # Inizializzazione del ResponsiveTextHandler
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'label': 12,      # Etichette degli assi
                'legend': 14,     # Testo legenda
                'icon': 20,       # Dimensione icone
            },
            breakpoints=[600, 900, 1200, 1600]  # Breakpoint per il ridimensionamento
        )

        # Dizionario dei controlli di testo per aggiornamento facile
        self.text_controls = {}
        
        # Sovrascrivi il gestore di ridimensionamento della pagina
        if self.page:
            # Salva l'handler originale se presente
            original_resize_handler = self.page.on_resize
            
            def combined_resize_handler(e):
                # Aggiorna le dimensioni del testo
                self.text_handler._handle_resize(e)
                # Aggiorna i controlli di testo
                self.update_text_controls()
                # Chiama anche l'handler originale se esiste
                if original_resize_handler:
                    original_resize_handler(e)
            
            self.page.on_resize = combined_resize_handler
            
        # Rimuoviamo la chiamata a add_load_complete_callback che non esiste
        # Le dimensioni iniziali verranno applicate quando build() viene chiamato
        
        # Store references to text elements that need color updates - ora con dimensioni responsive
        self.legend_max_text = ft.Text("Max", color=self.text_color, size=self.text_handler.get_size('legend'))
        self.legend_min_text = ft.Text("Min", color=self.text_color, size=self.text_handler.get_size('legend'))
        
        # Aggiungi i controlli al dizionario per l'aggiornamento dinamico
        self.text_controls[self.legend_max_text] = 'legend'
        self.text_controls[self.legend_min_text] = 'legend'

        # Register for theme change events
        state_manager = self.page.session.get('state_manager')
        if state_manager:
            state_manager.register_observer("theme_event", self.handle_theme_change)
    
    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati"""
        for control, size_category in self.text_controls.items():
            if size_category == 'icon':
                # Per le icone, aggiorna size
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
            else:
                # Per i testi, aggiorna size
                if hasattr(control, 'size'):
                    control.size = self.text_handler.get_size(size_category)
                elif hasattr(control, 'style') and hasattr(control.style, 'size'):
                    control.style.size = self.text_handler.get_size(size_category)
                # Aggiorna anche i TextSpan se presenti
                if hasattr(control, 'spans'):
                    for span in control.spans:
                        span.style.size = self.text_handler.get_size(size_category)
        
        # Richiedi l'aggiornamento della pagina
        if self.page:
            self.page.update()
    
    def handle_theme_change(self, event_data=None):
        """Handles theme change events by updating text color and chart elements."""
        if self.page:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            current_theme_config = DARK_THEME if is_dark else LIGHT_THEME
            self.text_color = current_theme_config["TEXT"]

            # Update legend text colors
            if hasattr(self, 'legend_max_text'):
                self.legend_max_text.color = self.text_color
                if self.legend_max_text.page:
                    self.legend_max_text.update()
            
            if hasattr(self, 'legend_min_text'):
                self.legend_min_text.color = self.text_color
                if self.legend_min_text.page:
                    self.legend_min_text.update()

            # For axis labels, the chart might need to be rebuilt
            if hasattr(self, 'chart_control') and self.chart_control.page:
                 # Update axis label colors directly
                 self._update_chart_axis_colors()
                 self.chart_control.update()

    def _update_chart_axis_colors(self):
        """Updates the colors of chart axis labels."""
        if hasattr(self, 'chart_control'):
            # Update X-axis labels
            if self.chart_control.bottom_axis and self.chart_control.bottom_axis.labels:
                for label in self.chart_control.bottom_axis.labels:
                    if isinstance(label.label, ft.Container) and isinstance(label.label.content, ft.Text):
                        label.label.content.color = self.text_color
                        
                        # Aggiorna il dizionario dei controlli di testo
                        self.text_controls[label.label.content] = 'label'
            
            # Update Y-axis labels
            if self.chart_control.left_axis and self.chart_control.left_axis.labels:
                for label in self.chart_control.left_axis.labels:
                    if isinstance(label.label, ft.Text):
                        label.label.color = self.text_color
                        
                        # Aggiorna il dizionario dei controlli di testo
                        self.text_controls[label.label] = 'label'
            
            # Aggiorna le dimensioni dopo aver cambiato colore
            self.update_text_controls()

    def build(self) -> ft.Column:
        """Build the temperature chart"""
        # Calculate dynamic range with margin
        min_temp = min(self.temp_min) if self.temp_min else 0
        max_temp = max(self.temp_max) if self.temp_max else 30
        min_y = int((min_temp - 5) // 5 * 5)
        max_y = int((max_temp + 5) // 5 * 5)
        min_y = max(min_y, 0)
        
        # Data series
        data_series = [
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i + 1, t) for i, t in enumerate(self.temp_min)],
                stroke_width=5,
                color=ft.Colors.BLUE,
                curved=True,
                stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i + 1, t) for i, t in enumerate(self.temp_max)],
                stroke_width=5,
                color=ft.Colors.RED,
                curved=True,
                stroke_cap_round=True,
            ),
        ]
        
        # X-axis labels with responsive text size
        x_labels = [
            ft.ChartAxisLabel(
                value=i + 1,
                label=ft.Container(
                    ft.Text(
                        day,
                        size=self.text_handler.get_size('label'),
                        weight=ft.FontWeight.BOLD,
                        color=self.text_color
                    ),
                    margin=ft.margin.only(top=10),
                )
            )
            for i, day in enumerate(self.days)
        ]
        
        # Y-axis labels with responsive text size
        y_labels = [
            ft.ChartAxisLabel(
                value=y,
                label=ft.Text(str(y), size=self.text_handler.get_size('label'), color=self.text_color)
            )
            for y in range(min_y, max_y + 1, 5)
        ]
        
        # Chart
        self.chart_control = ft.LineChart(
            data_series=data_series,
            border=ft.border.all(3, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
                width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
                width=1
            ),
            left_axis=ft.ChartAxis(labels=y_labels, labels_size=40),
            bottom_axis=ft.ChartAxis(labels=x_labels, labels_size=40),
            min_y=min_y,
            max_y=max_y,
            min_x=0,
            max_x=6,
            expand=True,
        )
        
        # Registra i controlli di testo per il grafico
        self._register_chart_text_controls()
        
        return ft.Column([
            ft.Row(
                [
                    ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.RED, size=self.text_handler.get_size('icon')),
                    self.legend_max_text,
                    ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.BLUE, size=self.text_handler.get_size('icon')),
                    self.legend_min_text,
                ], 
                spacing=20
            ),
            self.chart_control
        ])
    
    def _register_chart_text_controls(self):
        """Registra tutti i controlli di testo del grafico per l'aggiornamento responsive."""
        if hasattr(self, 'chart_control'):
            # Registra le etichette dell'asse X
            if self.chart_control.bottom_axis and self.chart_control.bottom_axis.labels:
                for label in self.chart_control.bottom_axis.labels:
                    if isinstance(label.label, ft.Container) and isinstance(label.label.content, ft.Text):
                        self.text_controls[label.label.content] = 'label'
            
            # Registra le etichette dell'asse Y
            if self.chart_control.left_axis and self.chart_control.left_axis.labels:
                for label in self.chart_control.left_axis.labels:
                    if isinstance(label.label, ft.Text):
                        self.text_controls[label.label] = 'label'
