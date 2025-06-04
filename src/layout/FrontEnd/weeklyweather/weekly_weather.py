import flet as ft

from services.api_service import ApiService
from layout.frontend.informationtab.air_condition import AirConditionInfo
from layout.frontend.informationtab.daily_forecast import DailyForecast
from layout.frontend.informationtab.main_information import MainWeatherInfo
from components.responsive_text_handler import ResponsiveTextHandler

class WeeklyWeather:
    def __init__(self, page, city, language, unit):
        self.page = page
        self.language = language
        self.unit = unit
        self.city = city
        self.mainInformation = MainWeatherInfo(page, city, language, unit)
        self.dailyForecast = DailyForecast(page, city, language, unit)
        self.airCondition = AirConditionInfo(page, city, language, unit)
        self.api = ApiService(page, city, language, unit)
        
        self.text_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes={
                'label': 20,       # Etichette (dimensione base più piccola per mobile)
                'icon': 50,        # Icone (dimensione base)
                'body': 14,        # Testo normale
                'value': 16,       # Valori (es. temperature, percentuali)
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
            
    def update_city(self, new_city):
        self.city = new_city
        self.mainInformation.update_city(new_city)
        self.dailyForecast.update_city(new_city)
        self.airCondition.update_city(new_city)
        self.api.update_data(new_city, self.language, self.unit)
        
    def update_by_coordinates(self, lat, lon):
        """Aggiorna le informazioni meteo usando le coordinate geografiche"""
        self.api.update_coordinates(lat, lon, self.language, self.unit)
        self.city = self.api.city  # Aggiorna il nome della città dal geocoding inverso
        self.mainInformation.update_by_coordinates(lat, lon)
        self.dailyForecast.update_by_coordinates(lat, lon)
        self.airCondition.update_by_coordinates(lat, lon)

    def createWeeklyForecast(self):
        """Crea il componente per le previsioni settimanali"""
        # Ottieni prima i dati meteo generali
        weather_data = self.api.get_weather_data(self.city)
        
        # Poi ottieni i dati delle previsioni settimanali
        forecast_days = self.api.get_weekly_forecast_data(weather_data) if weather_data else []
        
        if not forecast_days:
            return ft.Text("Dati previsioni meteo non disponibili.")
        
        forecast_cards = []
        
        # Per ogni giorno, crea una riga con le relative informazioni
        for i, day_data in enumerate(forecast_days):
            # Crea i controlli di testo con dimensioni responsive
            day_text = ft.Text(
                day_data["day"],
                size=self.text_handler.get_size('label'),
                weight="bold", 
                text_align=ft.TextAlign.START
            )
            temp_text = ft.Text(
                spans=[
                    ft.TextSpan(
                        f"{day_data['temp_min']}°",
                        ft.TextStyle(
                            size=self.text_handler.get_size('value'),
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE,
                        )
                    ),
                    ft.TextSpan(" / ",
                        ft.TextStyle(
                            size=self.text_handler.get_size('value'),
                            weight=ft.FontWeight.BOLD,
                        )),
                    ft.TextSpan(
                        f"{day_data['temp_max']}°",
                        ft.TextStyle(
                            size=self.text_handler.get_size('value'),
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.RED,
                        )
                    ),
                ],
                expand=True,
                text_align=ft.TextAlign.END
            )
            
            # Crea l'icona meteo con dimensioni responsive
            weather_icon = ft.Image(
                src=f"https://openweathermap.org/img/wn/{day_data['icon']}@4x.png",
                width=self.text_handler.get_size('icon'),
                height=self.text_handler.get_size('icon'),
            )
            
            # Aggiungi i controlli al dizionario per l'aggiornamento dinamico
            self.text_controls[day_text] = 'label'
            self.text_controls[temp_text] = 'value'
            self.text_controls[weather_icon] = 'icon'
            
            row = ft.Row(
                controls=[
                    day_text,
                    ft.Container(
                        content=weather_icon,
                        expand=True,
                        alignment=ft.alignment.center
                    ),
                    temp_text
                ],
                expand=True,
                spacing=0,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

            forecast_cards.append(ft.Container(content=row))

            # Aggiungi un divisore tra le righe (tranne che dopo l'ultima)
            if i < len(forecast_days) - 1:
                forecast_cards.append(
                    ft.Container(
                        content=ft.Divider(thickness=0.5, color="white", opacity=1),
                    )
                )
                
        # Dopo aver creato tutti i controlli, aggiorna le dimensioni del testo
        self.update_text_controls()
        
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=forecast_cards,
                expand=True
            )
        )

    def update_text_controls(self):
        """Aggiorna le dimensioni del testo per tutti i controlli registrati"""
        for control, size_category in self.text_controls.items():
            if size_category == 'icon':
                # Per le icone, aggiorna width e height
                control.width = self.text_handler.get_size(size_category)
                control.height = self.text_handler.get_size(size_category)
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

    def build(self):
        return ft.Container(
            border_radius=15,
            padding=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.createWeeklyForecast()
                ],
            )
        )