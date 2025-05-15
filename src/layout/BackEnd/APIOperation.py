import logging
import flet as ft
import requests
from datetime import datetime, timedelta

class APIOperation:

    logger = logging.getLogger(__name__)

    def __init__(self, page):
        logging.basicConfig(filename='logapp.log', level=logging.INFO, filemode='w')
        self.logger.info('Started')
        self.bgcolor = "#ffff80" if page.theme_mode == ft.ThemeMode.LIGHT else "#262626" #"#262626",
        self.txtcolor= "#000000" if page.theme_mode == ft.ThemeMode.LIGHT else "#ffffff" #"#262626",

    def getApiKey(self):
        return "ef054c6def10c2df7b266ba83513133a"   
    
    def getInformation(self, city):
        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {"q": city, "appid": self.getApiKey(), "units": "metric", "lang": "it"}
            response = requests.get(url, params=params)
            data = response.json()
            return data
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero delle informazioni: {e}")
            return None

    #SEZIONE TEMPERATURE
    def getTemperatureByCity(self, city):
        try:
            response = self.getInformation(city)
            logging.info("Temperatura per citta' recuperata")
            return round(response["list"][0]["main"]["temp"])
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero della temperatura per citta': {e}")
            return None
        
    def getRealFeelByCity(self, city):
        try:
            response = self.getInformation(city)
            logging.info("Temperatura ipotetica per citta' recuperata")
            return round(response["list"][0]["main"]["feels_like"])   
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero della temperatura ipotetica per citta': {e}")
            return None
        
    def getMinMaxTemperatureByCity(self, city):
        try:
            response = self.getInformation(city)
            logging.info("Temperatura minima e max per citta' recuperata")
            return round(response["list"][0]["main"]["temp_min"]), round(response["list"][0]["main"]["temp_max"])
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero della temperatura minima e max per citta': {e}")
            return None 
    
    #SEZIONE PIOGGIA/VENTO/UMIDITA'
    def getWindInformation(self, city):
        try:
            response = self.getInformation(city)
            logging.info("Informazioni vento recuperato")
            return round(response["list"][0]["wind"]["speed"])   
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero del vento ipotetico: {e}")
            return None 
        
    def getHumidityInformation(self, city):
        try:
            response = self.getInformation(city)
            logging.info("Informazioni umidita' recuperato")
            return response["list"][0]["main"]["humidity"]
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero dell'umidita' : {e}")
            return None 

    def getPressureInformation(self, city):
        try:
            response = self.getInformation(city)
            logging.info("Informazioni pressione recuperato")
            return round(response["list"][0]["main"]["pressure"])   
        except (KeyError, TypeError) as e:
            logging.error(f"Errore nel recupero della pressione : {e}")
            return None 
        
    def getImageByWeather(self, city):
        try:
            response = self.getInformation(city)
            icon_code= response["list"][0]["weather"][0]["icon"]
            logging.info("Informazioni immagine meteo recuperata")
            return ft.Image(src=f"https://openweathermap.org/img/wn/{icon_code}@4x.png")
        except (KeyError, IndexError, TypeError) as e:
            print(f"Errore durante il recupero dell'immagine meteo: {e}")
            return ft.Image(src="https://openweathermap.org/img/wn/01d@2x.png", width=100, height=100)
        
    def getVisibilityPercentage(self, city):
        try:
            response = self.getInformation(city)
            logging.info("Informazioni visibilita' recuperata")
            return response["list"][0]["visibility"] / 1000  
        except (KeyError, TypeError) as e:
            print(f"Errore nel recupero della visibilita': {e}")
            return None

    def getCurrentPressure(self, city):
        try:
            response = self.getInformation(city)
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
                                ft.Text(f"{item["main"]["temp"]:.1f}°", size=20, weight=ft.FontWeight.BOLD)
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

    from datetime import datetime

    def getWeeklyForecast(self, city):
        try:
            days = self.get_upcoming_days(5)  # es. ["Mon", "Tue", ...]
            today_abbrev = datetime.now().strftime("%a")

            response = self.getInformation(city)
            items = response["list"]
            forecast_cards = []

            
            for item in items:
                dt_txt = item["dt_txt"]  # "2025-05-16 09:00:00"
                date_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
                abbrev = date_obj.strftime("%a")  # "Mon", "Tue", ...
                
                if abbrev not in days:
                    continue

                hour = dt_txt.split(" ")[1]
                if hour not in ["09:00:00", "15:00:00"]:
                    continue

                is_today = abbrev == today_abbrev
                label = "Today" if is_today else abbrev

                temp_min = round(item["main"]["temp_min"])
                temp_max = round(item["main"]["temp_max"])
                weather = item["weather"][0]["description"]
                icon = item["weather"][0]["icon"]

                card = ft.Row(
                        controls=[
                            ft.Text(
                                label,
                                size=15,
                                color=self.txtcolor,
                                weight="bold" if is_today else "normal",
                            ),
                            ft.Image(
                                src=f"https://openweathermap.org/img/wn/{icon}@4x.png",
                                width=100,
                                height=100,
                            ),
                            ft.Text(weather.capitalize(), size=12),
                            ft.Text(f"{temp_min}° / {temp_max}°")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        
                )

                forecast_cards.append(card)
                
            return ft.Column(controls=forecast_cards)

        except Exception as e:
            print(f"Errore durante l'elaborazione della previsione: {e}")
            return ft.Text("Errore nella previsione meteo.")
