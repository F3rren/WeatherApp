import logging
from fastapi import params
import flet as ft
import requests
from datetime import datetime, timedelta
from babel.dates import format_datetime

class APIOperation:

    logger = logging.getLogger(__name__)

    def __init__(self, page, city, language, unit):
        logging.basicConfig(filename='logapp.log', level=logging.INFO, filemode='w')
        self.logger.info('Started')
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",
        
        self.city = city
        self.unit = unit
        self.lang = language
    
    def getApiKey(self):
        return "ef054c6def10c2df7b266ba83513133a"   
    
    def getStateInformation(self, city):
        try:
            url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {"q": city, "limit": 5, "appid": self.getApiKey()}
            response = requests.get(url, params=params)
            data = response.json()
            print(data)
            #return data
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero delle informazioni dello stato: {e}")
            return None

    def getInformation(self):
        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {"q": self.city, "appid": self.getApiKey(), "units": self.unit, "lang": self.lang}
            response = requests.get(url, params=params)
            data = response.json()
            return data
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero delle informazioni: {e}")
            return None

    #SEZIONE TEMPERATURE
    def getTemperatureByCity(self):
        try:
            response = self.getInformation()
            logging.info("Temperatura per citta' recuperata")
            return round(response["list"][0]["main"]["temp"])
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero della temperatura per citta': {e}")
            return None
        
    def getRealFeelByCity(self, city):
        try:
            response = self.getInformation()
            logging.info("Temperatura ipotetica per citta' recuperata")
            return round(response["list"][0]["main"]["feels_like"])   
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero della temperatura ipotetica per citta': {e}")
            return None
        
    def getMinMaxTemperatureByCity(self):
        try:
            response = self.getInformation()
            logging.info("Temperatura minima e max per citta' recuperata")
            return round(response["list"][0]["main"]["temp_min"]), round(response["list"][0]["main"]["temp_max"])
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero della temperatura minima e max per citta': {e}")
            return None 
    
    #SEZIONE PIOGGIA/VENTO/UMIDITA'
    def getWindInformation(self):
        try:
            response = self.getInformation()
            logging.info("Informazioni vento recuperato")
            return round(response["list"][0]["wind"]["speed"])   
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero del vento ipotetico: {e}")
            return None 
        
    def getHumidityInformation(self):
        try:
            response = self.getInformation()
            logging.info("Informazioni umidita' recuperato")
            return response["list"][0]["main"]["humidity"]
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero dell'umidita' : {e}")
            return None 

    def getPressureInformation(self):
        try:
            response = self.getInformation()
            logging.info("Informazioni pressione recuperato")
            return round(response["list"][0]["main"]["pressure"])   
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero della pressione : {e}")
            return None 
        
    def getImageByWeather(self):
        try:
            response = self.getInformation()
            icon_code= response["list"][0]["weather"][0]["icon"]
            logging.info("Informazioni immagine meteo recuperata")
            return ft.Image(src=f"https://openweathermap.org/img/wn/{icon_code}@4x.png")
        except (KeyError, IndexError, TypeError) as e:
            print(f"Errore durante il recupero dell'immagine meteo: {e}")
            return ft.Image(src="https://openweathermap.org/img/wn/01d@2x.png", width=100, height=100)
        
    def getVisibilityPercentage(self):
        try:
            response = self.getInformation()
            logging.info("Informazioni visibilita' recuperata")
            return response["list"][0]["visibility"] / 1000  
        except (KeyError, TypeError) as e:
            print(f"Errore nel recupero della visibilita': {e}")
            return None

    def getCurrentPressure(self):
        try:
            response = self.getInformation()
            logging.info("Informazioni pressione attuale recuperata")
            return response.json()["list"][0]["main"]["pressure"]
        except (KeyError, TypeError) as e:
            print(f"Errore nel recupero della pressione: {e}")
            return None

    
    def get_upcoming_days(self, n):
        today = datetime.now()
        return [(today + timedelta(days=i)).strftime("%a") for i in range(n)]

    #SEZIONE PREVISIONI METEO GIORNALIERE/SETTIMANALI
    def getDailyForecast(self, city):
        forecast_cards = []
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.getApiKey()}&units=metric&lang=it"
            response = requests.get(url)
            data = response.json()
            for i, item in enumerate(data["list"][:6]):
                time = item["dt_txt"]
                dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                orario = dt.strftime("%H:%M")
                
                card = ft.Column(
                            controls=[
                                ft.Text(orario, size=20, weight=ft.FontWeight.BOLD),
                                ft.Image(
                                    src=f"https://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png",
                                    width=100,
                                    height=100,
                                ),
                                ft.Text(f"{round(item["main"]["temp"])}°", size=20, weight=ft.FontWeight.BOLD)
                            ],
                            expand=True,
                            spacing=0,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                
                forecast_cards.append(card)

                if i < 5:
                     forecast_cards.append(
                         ft.Container(
                             content=ft.VerticalDivider(width=1, thickness=1, color="white", opacity=0.5),
                             height=100,
                             alignment=ft.alignment.center,
                         )
                     )

            return ft.Row(controls=forecast_cards)

        except Exception as e:
            logging.error(f"Errore nel parsing della previsione: {e}")
            return ft.Text("Errore nel caricamento della previsione.")


    def getWeeklyForecast(self):
        try:
            response = self.getInformation()
            items = response["list"]
            daily_data = {}

            # Raggruppa tutti gli item per giorno
            for item in items:
                dt_txt = item["dt_txt"]
                date_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
                day_key = date_obj.strftime("%Y-%m-%d")

                if day_key not in daily_data:
                    daily_data[day_key] = []
                daily_data[day_key].append(item)

            forecast_cards = []
            for i, (day_key, items_in_day) in enumerate(sorted(daily_data.items())[:5]):
                date_obj = datetime.strptime(day_key, "%Y-%m-%d")
                label = format_datetime(date_obj, "EEEE", locale="it").capitalize()

                # Calcola min e max su tutti i valori della giornata
                temp_min = min([x["main"]["temp_min"] for x in items_in_day])
                temp_max = max([x["main"]["temp_max"] for x in items_in_day])

                # Prendi l'icona dal primo elemento delle 12:00 se c'è, altrimenti qualsiasi
                icon_item = next((x for x in items_in_day if "12:00:00" in x["dt_txt"]), items_in_day[0])
                icon = icon_item["weather"][0]["icon"]

                row = ft.Row(
                    controls=[
                        ft.Text(label, 
                                size=20, 
                                color=self.txtcolor, 
                                weight="bold", 
                                width=100,
                                text_align=ft.TextAlign.START
                            ),
                        ft.Container(
                            content=ft.Image(
                                src=f"https://openweathermap.org/img/wn/{icon}@4x.png",
                                width=80,
                                height=80,
                            ),
                            expand=True,
                            alignment=ft.alignment.center
                        ),
                        ft.Text(
                            item["weather"][0]["description"].capitalize()
                        ),
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    f"{round(temp_min)}°",
                                    ft.TextStyle(
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE,
                                    )
                                ),
                                ft.TextSpan(" / ",
                                    ft.TextStyle(
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                    )),
                                ft.TextSpan(
                                    f"{round(temp_max)}°",
                                    ft.TextStyle(
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.RED,
                                    )
                                ),
                            ],
                            expand=True,
                            text_align=ft.TextAlign.END
                        )
                    ],
                    expand=True,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )

                forecast_cards.append(ft.Container(content=row))

                if i < 4:
                    forecast_cards.append(
                        ft.Container(
                            content=ft.Divider(thickness=0.5, color="white", opacity=1),
                        )
                    )

            return ft.Column(controls=forecast_cards, expand=True)

        except Exception as e:
            print(f"Errore durante l'elaborazione della previsione: {e}")
            return ft.Text("Errore nella previsione meteo.")
