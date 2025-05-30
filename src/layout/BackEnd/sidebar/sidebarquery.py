import os
from supabase import create_client, Client
from dotenv import load_dotenv


class SidebarQuery:

    #dalla searchbar, i dati devono essere sputati fuori così:
    #nome città: regione (se possibile), stato, ma da dietro le quinte
    # verranno passate solamente latitudine e longitudine
    def __init__(self):
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)
    
    def loadAllCity(self):
        response = (
            self.supabase.table("italian_cities")
            .select("*")  
            .execute()
        )
        return response.data

    def loadCityAdmin(self): #carica i capoluoghi di regione
        response = (
            self.supabase.table("italian_cities")
            .select("*")
            .eq("capital", "admin")  
            .execute()
        )
        return response.data

    def loadCityCapital(self): #carica i capoluoghi di regione
        response = (
            self.supabase.table("italian_cities")
            .select("*")
            .eq("capital", "primary")  
            .execute()
        )

        return response.data


p = SidebarQuery()
#p.loadCityAdmin()
p.loadCityCapital()
    
