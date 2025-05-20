import json
import os


class SidebarOperations:

    def getCapitalCities(self):
        cities = []
        try:
            cartella_corrente = os.path.dirname(__file__)
            percorso_file = os.path.join(cartella_corrente, 'capital.json')

            with open(percorso_file, 'r', encoding='utf-8') as f:
                dati = json.load(f)  # <-- parsing corretto

                items = sorted(dati["countries"], key=lambda x: x["capital"])
                for paese in items:
                    capitale = paese.get("capital")
                    if capitale:
                        cities.append(capitale)
            return cities

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Errore durante l'apertura o la lettura del file JSON: {e}")
            return []
        
