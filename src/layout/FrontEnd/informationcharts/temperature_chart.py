import flet as ft
from typing import List
from services.translation_service import TranslationService
from utils.config import DEFAULT_LANGUAGE, LIGHT_THEME, DARK_THEME, DEFAULT_UNIT_SYSTEM # Added DEFAULT_UNIT_SYSTEM
from components.responsive_text_handler import ResponsiveTextHandler
import logging # Added import for logging

class TemperatureChart:
    """
    Temperature chart display.
    """
    
    def __init__(self, page: ft.Page, days: List[str], temp_min: List[int], 
                 temp_max: List[int], text_color: str):
        self.page = page
        self.days = days # These are the keys for translation, e.g., "Mon", "Tue"
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.text_color = text_color # Initial text color

        state_manager = None
        if page and hasattr(page, 'session') and page.session.get('state_manager'):
            state_manager = page.session.get('state_manager')
            self.language = state_manager.get_state('language') or DEFAULT_LANGUAGE
            self.unit_system = state_manager.get_state('unit_system') or DEFAULT_UNIT_SYSTEM
            # Assuming theme is handled by page.theme_mode directly in handle_theme_change
            state_manager.register_observer("language_event", self.handle_language_change)
            state_manager.register_observer("theme_event", self.handle_theme_change)
            state_manager.register_observer("unit_event", self.handle_unit_change) # New observer
        else:
            self.language = DEFAULT_LANGUAGE
            self.unit_system = DEFAULT_UNIT_SYSTEM
        
        self.unit_symbol = TranslationService.get_unit_symbol(self.unit_system, "temperature")

        # Inizializzazione del ResponsiveTextHandler
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'icon': 20,       # Dimensione icone
                'label': 12,      # Dimensione per etichette assi
                'legend': 14,     # Dimensione per testo legenda
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
            
        # Store references to text elements that need color updates
        # Use TranslationService for legend text - Use lowercase keys "max" and "min"
        max_label = TranslationService.get_text("max", self.language)
        min_label = TranslationService.get_text("min", self.language)
        self.legend_max_text = ft.Text(f"{max_label} ({self.unit_symbol})", color=self.text_color, size=self.text_handler.get_size('legend'))
        self.legend_min_text = ft.Text(f"{min_label} ({self.unit_symbol})", color=self.text_color, size=self.text_handler.get_size('legend'))
        
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
            new_text_color = current_theme_config["TEXT"]

            if self.text_color != new_text_color:
                self.text_color = new_text_color

                # Update legend text colors
                if hasattr(self, 'legend_max_text'):
                    self.legend_max_text.color = self.text_color
                    if self.legend_max_text.page:
                        self.legend_max_text.update()
                
                if hasattr(self, 'legend_min_text'):
                    self.legend_min_text.color = self.text_color
                    if self.legend_min_text.page:
                        self.legend_min_text.update()

                # For axis labels, the chart might need to be rebuilt or colors updated
                if hasattr(self, 'chart_control') and self.chart_control.page:
                    self._update_chart_axis_colors() # This updates colors and calls update_text_controls
                    self.chart_control.update() # Ensure chart itself updates

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
                stroke_width=3,
                color=ft.Colors.BLUE,
                curved=True,
                stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i + 1, t) for i, t in enumerate(self.temp_max)],
                stroke_width=3,
                color=ft.Colors.RED,
                curved=True,
                stroke_cap_round=True,
            ),
        ]
        
        # X-axis labels with responsive text size
        self._x_axis_label_text_controls = [] # Store ft.Text objects for direct update
        x_labels_for_chart = []
        for i, day_key in enumerate(self.days): # self.days contains keys like "Mon", "Tue"
            day_text_obj = ft.Text(
                TranslationService.translate_weekday(day_key, self.language),
                size=self.text_handler.get_size('label'), # Use responsive size
                weight=ft.FontWeight.BOLD,
                color=self.text_color
            )
            self._x_axis_label_text_controls.append(day_text_obj)
            self.text_controls[day_text_obj] = 'label' # Register for responsive updates
            x_labels_for_chart.append(ft.ChartAxisLabel(
                value=i + 1, # Chart expects 1-based index for days if data points are 1-based
                label=ft.Container(
                    day_text_obj,
                    margin=ft.margin.only(top=10),
                )
            ))
        
        # Y-axis labels with responsive text size
        y_labels_for_chart = []
        for y_val_num in range(min_y, max_y + 1, 5):
            val_text_obj = ft.Text(
                str(y_val_num), 
                size=self.text_handler.get_size('label'), # Use responsive size
                color=self.text_color
            )
            self.text_controls[val_text_obj] = 'label' # Register for responsive updates
            y_labels_for_chart.append(ft.ChartAxisLabel(
                value=y_val_num,
                label=val_text_obj
            ))
        
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
            left_axis=ft.ChartAxis(labels=y_labels_for_chart, labels_size=40),
            bottom_axis=ft.ChartAxis(labels=x_labels_for_chart, labels_size=40),
            interactive=False,  # Correct way to disable hover/tooltips
            min_y=min_y,
            max_y=max_y,
            min_x=0,
            max_x=6,
            expand=True,
        )
        
        chart_column = ft.Column([ # Define chart_column here
            ft.Row(
                [
                    ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.RED, size=self.text_handler.get_size('icon')),
                    self.legend_max_text,
                    ft.Icon(name=ft.Icons.SQUARE, color=ft.Colors.BLUE, size=self.text_handler.get_size('icon')),
                    self.legend_min_text,
                ], 
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER # Center the legend
            ),
            self.chart_control
        ])

        # Apply initial responsive sizes
        self.update_text_controls()
        
        return chart_column

    def handle_language_change(self, event_data=None):
        """Handles language change events by updating chart x-axis labels and legend."""
        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                new_language = state_manager.get_state('language') or DEFAULT_LANGUAGE
                if new_language != self.language:
                    self.language = new_language
                    logging.info(f"TemperatureChart: Language changed to {self.language}")
                
                    # Update X-axis labels
                    if hasattr(self, '_x_axis_label_text_controls') and self._x_axis_label_text_controls:
                        for i, text_control in enumerate(self._x_axis_label_text_controls):
                            if i < len(self.days): # self.days stores the original day keys
                                translated_day = TranslationService.translate_weekday(self.days[i], self.language)
                                logging.info(f"TemperatureChart: Translating day {self.days[i]} to {translated_day}")
                                text_control.value = translated_day
                                if text_control.page: # Update if on page
                                     text_control.update()
                    
                    # Update legend texts
                    self._update_legend_display() # Call new method

                    if hasattr(self, 'chart_control') and self.chart_control.page:
                        self.chart_control.update()
                        logging.info("TemperatureChart: chart_control updated after language change.")

    def handle_unit_change(self, event_data=None):
        """Handles unit system change events by updating the legend."""
        if self.page:
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                new_unit_system = state_manager.get_state('unit_system') or DEFAULT_UNIT_SYSTEM
                if new_unit_system != self.unit_system:
                    self.unit_system = new_unit_system
                    self.unit_symbol = TranslationService.get_unit_symbol(self.unit_system, "temperature")
                    logging.info(f"TemperatureChart: Unit system changed to {self.unit_system}, symbol: {self.unit_symbol}")
                    
                    self._update_legend_display() # Call new method

                    if hasattr(self, 'chart_control') and self.chart_control.page:
                        self.chart_control.update()
                        logging.info("TemperatureChart: chart_control updated after unit change.")

    def _update_legend_display(self):
        """Updates the legend texts based on current language and unit symbol."""
        if not hasattr(self, 'legend_max_text') or not hasattr(self, 'legend_min_text'):
            return

        max_label = TranslationService.get_text("max", self.language)
        min_label = TranslationService.get_text("min", self.language)
        
        new_max_value = f"{max_label} ({self.unit_symbol})"
        new_min_value = f"{min_label} ({self.unit_symbol})"

        if self.legend_max_text.value != new_max_value:
            self.legend_max_text.value = new_max_value
            logging.info(f"TemperatureChart: Updating legend_max_text to {new_max_value}")
            if self.legend_max_text.page:
                self.legend_max_text.update()

        if self.legend_min_text.value != new_min_value:
            self.legend_min_text.value = new_min_value
            logging.info(f"TemperatureChart: Updating legend_min_text to {new_min_value}")
            if self.legend_min_text.page:
                self.legend_min_text.update()
    
    def cleanup(self):
        """Unregisters observers to prevent memory leaks."""
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            state_manager = self.page.session.get('state_manager')
            if state_manager:
                logging.info("TemperatureChart: Cleaning up observers.")
                state_manager.unregister_observer("language_event", self.handle_language_change)
                state_manager.unregister_observer("theme_event", self.handle_theme_change)
                state_manager.unregister_observer("unit_event", self.handle_unit_change)
        
        # Consider if page.on_resize needs specific cleanup if it was overridden
        # For now, assuming Flet handles it or it's not causing issues.
        # If self.page.on_resize was set to combined_resize_handler,
        # and original_resize_handler was stored, it might be good practice to restore it,
        # but only if this component's lifecycle is managed such that it's truly "destroyed"
        # and its on_resize should no longer be active.
        # Given Flet's declarative nature, simply not including it in a new page build might be enough.