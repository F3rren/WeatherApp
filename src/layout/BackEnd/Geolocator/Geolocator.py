import flet as ft
import threading
import time

class Geolocator:
    def __init__(self):
        self.gl = None
        self.location_callback = None
        self.is_tracking = False
        self.current_lat = None
        self.current_lon = None
        self.update_thread = None
        self.stop_thread = False
        
    async def get_current_location(self, page: ft.Page):
        """Ottiene la posizione corrente una sola volta"""
        self.gl = ft.Geolocator(
            location_settings=ft.GeolocatorSettings(
                accuracy=ft.GeolocatorPositionAccuracy.HIGH
            ),
            on_error=lambda e: page.add(ft.Text(f"Errore: {e.data}")),
        )

        # Aggiunta del controllo alla pagina PRIMA di usarlo
        page.overlay.append(self.gl)
        page.update()

        # Chiedi il permesso se necessario
        permission = await self.gl.request_permission_async()
        if permission != "granted":
            page.add(ft.Text("Permessi per la posizione non concessi"))
            return None, None

        # Ottieni posizione attuale
        position = await self.gl.get_current_position_async()
        return position.latitude, position.longitude
    
    async def start_location_tracking(self, page: ft.Page, on_location_change=None):
        """Inizia il tracciamento continuo della posizione"""
        self.location_callback = on_location_change
        
        # Definisci la funzione di callback per i cambiamenti di posizione
        def handle_position_change(e):
            if e.latitude and e.longitude:
                # Memorizza le coordinate più recenti
                self.current_lat = e.latitude
                self.current_lon = e.longitude
                
                # Aggiorna l'interfaccia utente
                try:
                    # Aggiorna solo le etichette di stato
                    page.update()
                except Exception as e:
                    print(f"Errore nell'aggiornamento dell'UI: {e}")
        
        self.gl = ft.Geolocator(
            location_settings=ft.GeolocatorSettings(
                accuracy=ft.GeolocatorPositionAccuracy.HIGH,
                distance_filter=500  # Aggiorna solo se ci si sposta di almeno 500 metri
            ),
            on_position_change=handle_position_change,
            on_error=lambda e: page.add(ft.Text(f"Errore: {e.data}")),
        )
        
        # Aggiunta del controllo alla pagina
        page.overlay.append(self.gl)
        page.update()
        
        # Chiedi il permesso se necessario
        permission = await self.gl.request_permission_async()
        if permission != "granted":
            page.add(ft.Text("Permessi per la posizione non concessi"))
            return False
        
        # Inizia il tracciamento
        await self.gl.start_position_watcher_async()
        self.is_tracking = True
        
        # Avvia un thread separato per aggiornare l'UI
        self.stop_thread = False
        self.update_thread = threading.Thread(target=self._update_ui_thread, args=(page,))
        self.update_thread.daemon = True
        self.update_thread.start()
        
        return True
    
    def _update_ui_thread(self, page):
        """Thread che aggiorna periodicamente l'UI con le nuove coordinate"""
        while not self.stop_thread:
            if self.current_lat and self.current_lon and self.location_callback:
                try:
                    # Aggiorna l'UI con le coordinate più recenti solo se il callback è attivo
                    # (cioè quando lo switch è attivato)
                    lat, lon = self.current_lat, self.current_lon
                    
                    # Non resettiamo più le coordinate dopo l'uso, così rimangono disponibili
                    # self.current_lat = None
                    # self.current_lon = None
                    
                    # Usa il metodo update_async per aggiornare l'UI
                    page.invoke_async(lambda: self.location_callback(lat, lon))
                except Exception as e:
                    print(f"Errore nell'aggiornamento dell'UI dal thread: {e}")
            
            # Attendi 5 secondi prima del prossimo controllo
            time.sleep(5)
    
    async def stop_location_tracking(self):
        """Ferma il tracciamento della posizione"""
        if self.gl and self.is_tracking:
            await self.gl.stop_position_watcher_async()
            self.is_tracking = False
            
        # Ferma il thread di aggiornamento
        self.stop_thread = True
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(1)  # Attendi al massimo 1 secondo
