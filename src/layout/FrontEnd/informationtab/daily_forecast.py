import flet as ft
from services.api_service import ApiService
from components.responsive_text_handler import ResponsiveTextHandler

class DailyForecast:    
    def __init__(self, page, city, language, unit):
        self.page = page  
        self.city = city
        self.language = language
        self.unit = unit
        self.api = ApiService(page, self.city, self.language, self.unit)
        self.daily_forecast_items = []  # Inizializza la lista per memorizzare i riferimenti agli item
        
        # Inizializzazione del ResponsiveTextHandler per gestire il testo responsive
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'title': 24,
                'subtitle': 18,
                'label': 14,
                'value': 16,
                'icon': 200
            },
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Dizionario per memorizzare i controlli di testo da aggiornare
        self.text_controls = {}

        # This Row will hold the dynamically loaded forecast items.
        # self.api.getDailyForecast() is expected to return a single ft.Control (e.g., another ft.Row)
        # that contains the actual hourly forecast elements.
        self.forecast_items_row = ft.Row(scroll=ft.ScrollMode.AUTO)
        
        # This is the main column for the hourly forecast content.
        # Its structure is static; only the controls of self.forecast_items_row will change.
        self.hourly_forecast_content_column = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                self.forecast_items_row,
            ],
        )
        
        # Initial population of the forecast items
        self._populate_forecast_items()
        
        # Aggiungiamo un observer per il ridimensionamento
        self.text_handler.add_observer(self._handle_text_resize)

    def _populate_forecast_items(self):
        """
        Fetches new forecast data from the ApiService and updates 
        the content of self.forecast_items_row.
        """
        new_forecast_display_control = self.api.getDailyForecast()
        
        self.forecast_items_row.controls.clear()
        if isinstance(new_forecast_display_control, ft.Control):
            self.forecast_items_row.controls.append(new_forecast_display_control)
        elif isinstance(new_forecast_display_control, list): # Handle if it's a list of controls
            self.forecast_items_row.controls.extend(new_forecast_display_control)

        if self.forecast_items_row.page:  # Check if the control is part of the page
            self.forecast_items_row.update()
        elif self.hourly_forecast_content_column.page: # Fallback to update parent if direct child not updated
             self.hourly_forecast_content_column.update()

    def update_city(self, new_city):
        self.city = new_city
        self.update_data(new_city, self.language, self.unit)
        self._populate_forecast_items() 
        
    def update_by_coordinates(self, lat, lon):
        """Aggiorna le informazioni meteo usando le coordinate geografiche"""
        self.api.update_coordinates(lat, lon, self.language, self.unit)
        self.city = self.api.city  
        self._populate_forecast_items() 
        
    def update_data(self, city, language, unit):
        self.city = city
        self.language = language
        self.unit = unit
        self.api = ApiService(self.page, self.city, self.language, self.unit)
        self._populate_forecast_items() 
        
    def createHourlyForecast(self):
        return ft.Container(
            alignment=ft.alignment.center,
            content=self.hourly_forecast_content_column,
            expand=True
        )

    def build(self):
        return ft.Container(
            border_radius=15,
            padding=20,
            content=self.createHourlyForecast(),
            expand=True,
        )

    def cleanup(self):
        """Release resources and perform cleanup."""
        # Rimuove l'observer del text_handler
        if hasattr(self, 'text_handler'):
            self.text_handler.remove_observer(self._handle_text_resize)
        
        # Rimuove gli handler dello StateManager
        self.unregister_state_handlers()
            
        if self.forecast_items_row:
            # Call cleanup on each DailyForecastItems instance
            if self.daily_forecast_items:
                for item in self.daily_forecast_items:
                    if hasattr(item, 'cleanup') and callable(item.cleanup):
                        item.cleanup() # Call cleanup on each DailyForecastItems instance
                self.daily_forecast_items.clear()
            self.forecast_items_row.controls.clear()
            self.forecast_items_row.update()

    def _handle_text_resize(self):
        """
        Aggiorna le dimensioni del testo quando cambia la dimensione della finestra.
        Chiamato come observer dal ResponsiveTextHandler.
        """
        if self.text_controls:
            self.text_handler.update_text_controls(self.text_controls)
            
        # Aggiorniamo anche i DailyForecastItems che potrebbero avere il proprio text_handler
        for item in self.daily_forecast_items:
            if hasattr(item, 'text_handler') and hasattr(item, '_update_text_elements'):
                item._update_text_elements()
                
        # Forza l'aggiornamento dell'interfaccia
        if self.hourly_forecast_content_column.page:
            self.hourly_forecast_content_column.update()

