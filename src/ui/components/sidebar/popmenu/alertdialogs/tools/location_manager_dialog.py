import flet as ft
from core.state_manager import StateManager
from services.location.location_manager_service import LocationManagerService
from services.location.geocoding_service import GeocodingService
from services.ui.translation_service import TranslationService
import logging

logger = logging.getLogger(__name__)


class LocationManagerDialog:
    def __init__(self, page: ft.Page, update_weather_callback=None):
        self.page = page
        self.state_manager = StateManager(page)
        self.location_service = LocationManagerService()
        self.geocoding_service = GeocodingService()
        self.update_weather_callback = update_weather_callback
        
        theme_mode = self.state_manager.get_state("theme_mode")
        self.theme = "dark" if theme_mode == ft.ThemeMode.DARK else "light"
        self.language = self.state_manager.get_state("language") or "italian"
        
        # Centralized color management  
        self.Colors = {}
        self.update_theme_Colors()
        
        # Register observers
        self.state_manager.register_observer("language_event", self.update_ui)
        self.state_manager.register_observer("theme_event", self.update_ui)
        
        # Dialog components
        self.dialog = None
        self.locations_list = None
        
        # Search components
        self.city_field = None
        self.state_field = None
        self.country_field = None
        self.search_button = None
        self.search_results_container = None
        self.is_searching = False
        
        # Stats dialog components
        self.stats_dialog = None
        
        logger.info("LocationManagerDialog inizializzato con input strutturato professionale")
    
    def update_theme_Colors(self):
        """Update theme Colors based on current theme."""
        if self.theme == "dark":
            self.Colors.update({
                "bg": "#1E1E1E", "surface": "#2D2D2D", "text": "#FFFFFF", 
                "text_secondary": "#B0B0B0", "border": "#404040", "accent": "#2196F3"
            })
        else:  # light
            self.Colors.update({
                "bg": "#FFFFFF", "surface": "#F5F5F5", "text": "#212121", 
                "text_secondary": "#757575", "border": "#E0E0E0", "accent": "#2196F3"
            })
    
    def update_ui(self, event=None):
        """Update UI when theme or language changes."""
        if event and event.get("type") == "theme_event":
            theme_mode = event.get("data")
            self.theme = "dark" if theme_mode == ft.ThemeMode.DARK else "light"
            self.update_theme_Colors()
        elif event and event.get("type") == "language_event":
            self.language = event.get("data", "italian")
        
        if self.page and self.dialog and self.dialog.open:
            self.show_dialog()  # Refresh dialog with new settings
    
    def show_dialog(self):
        """Show the location manager dialog."""
        try:
            # Chiudi eventuali dialog esistenti usando il metodo corretto
            if self.dialog:
                self.page.close(self.dialog)
                self.dialog = None
            
            # Crea e mostra il nuovo dialog usando page.open()
            self.dialog = self.create_dialog()
            self.page.open(self.dialog)
            
        except Exception as ex:
            logger.error(f"Errore durante la visualizzazione del dialog: {ex}")
    
    def create_dialog(self):
        """Create the unified location manager dialog with integrated search."""
        texts = self.get_texts()
        
        # Crea i campi di input per la ricerca
        self.city_field = ft.TextField(
            label="Città *",
            hint_text="Es. Milano, Roma, Tokyo...",
            border_color=self.Colors["border"],
            focused_border_color=self.Colors["accent"],
            color=self.Colors["text"],
            bgcolor=self.Colors["surface"],
            width=150
        )
        
        self.state_field = ft.TextField(
            label="Regione/Stato",
            hint_text="Opzionale",
            border_color=self.Colors["border"],
            focused_border_color=self.Colors["accent"],
            color=self.Colors["text"],
            bgcolor=self.Colors["surface"],
            width=130
        )
        
        self.country_field = ft.TextField(
            label="Paese",
            hint_text="Opzionale",
            border_color=self.Colors["border"],
            focused_border_color=self.Colors["accent"],
            color=self.Colors["text"],
            bgcolor=self.Colors["surface"],
            width=120
        )
        
        self.search_button = ft.ElevatedButton(
            text="🔍 Cerca",
            icon=ft.Icons.SEARCH,
            on_click=self.search_locations,
            bgcolor=ft.Colors.with_opacity(0.1, self.Colors["accent"]),
            color=self.Colors["accent"],
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            width=100
        )
        
        # Container per i risultati di ricerca
        self.search_results_container = ft.Container(
            content=ft.Column([], spacing=5),
            visible=False,
            height=0,
            bgcolor=ft.Colors.with_opacity(0.02, self.Colors["text"]),
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.Colors["text"])),
            border_radius=8,
            padding=10,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )
        
        return ft.AlertDialog(
            modal=False,
            title=ft.Row([
                ft.Icon(ft.Icons.LOCATION_ON, color=self.Colors["accent"], size=24),
                ft.Text(texts['dialog_title'], weight=ft.FontWeight.BOLD, color=self.Colors["text"])
            ], spacing=10),
            bgcolor=self.Colors["bg"],
            content=ft.Container(
                width=min(600, self.page.width * 0.95) if self.page else 600,
                bgcolor=self.Colors["bg"],
                padding=20,
                content=ft.Column([
                    # Sezione ricerca integrata
                    ft.Row([
                        ft.Icon(ft.Icons.SEARCH, size=20, color="#ff6b35"),
                        ft.Text("Cerca Nuova Località", weight=ft.FontWeight.W_600, 
                               color=self.Colors["text"], size=15),
                    ], spacing=10),
                    
                    # Campi di input per la ricerca
                    ft.Row([
                        self.city_field,
                        self.state_field,
                        self.country_field,
                        self.search_button
                    ], spacing=10, scroll=ft.ScrollMode.AUTO),
                    
                    # Container per risultati di ricerca
                    self.search_results_container,
                    
                    ft.Divider(color=ft.Colors.with_opacity(0.2, self.Colors["text"])),
                    
                    # Sezione località salvate con azioni
                    ft.Row([
                        ft.Icon(ft.Icons.BOOKMARK, size=20, color="#22c55e"),
                        ft.Text(texts['saved_locations'], weight=ft.FontWeight.W_600, 
                               color=self.Colors["text"], size=15),
                        ft.Container(expand=True),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.BAR_CHART,
                                tooltip=texts['stats'],
                                on_click=lambda e: self.show_statistics(),
                                icon_color=self.Colors["accent"],
                                icon_size=18
                            ),
                            ft.IconButton(
                                icon=ft.Icons.GPS_FIXED,
                                tooltip=texts['use_current'],
                                on_click=lambda e: self.use_current_location(),
                                icon_color=self.Colors["accent"],
                                icon_size=18
                            )
                        ], spacing=0)
                    ], spacing=10),
                    
                    # Lista località salvate
                    self.create_locations_list(),
                    
                    ft.Container(height=15),

                ], spacing=20, scroll=ft.ScrollMode.AUTO)
            ),
            actions=[
                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=TranslationService.translate_from_dict("settings_alert_dialog_items", "close", self.language),
                    on_click=lambda e: self.close_dialog(e),
                    style=ft.ButtonStyle(
                        bgcolor="#3F51B5",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=24, vertical=12)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content_padding=ft.padding.all(8),
            title_padding=ft.padding.all(16),
            open=False,
        )
    
    def create_locations_list(self):
        """Create the list of saved locations using the professional service."""
        locations_column = ft.Column([], spacing=5, scroll=ft.ScrollMode.AUTO)
        
        # Ottieni le località dal servizio professionale
        all_locations = self.location_service.get_all_locations()
        logger.info(f"create_locations_list: Trovate {len(all_locations)} località")
        
        if not all_locations:
            # Nessuna località salvata
            no_locations_msg = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.LOCATION_OFF, size=48, color=self.Colors["text_secondary"]),
                    ft.Text("Nessuna località salvata", 
                           weight=ft.FontWeight.BOLD, 
                           color=self.Colors["text_secondary"],
                           text_align=ft.TextAlign.CENTER),
                    ft.Text("Aggiungi una località per iniziare", 
                           size=12, 
                           color=self.Colors["text_secondary"],
                           text_align=ft.TextAlign.CENTER)
                ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                alignment=ft.alignment.center
            )
            locations_column.controls.append(no_locations_msg)
            
        else:
            # Ordina le località: prima i preferiti, poi per data aggiunta
            sorted_locations = sorted(all_locations, 
                                    key=lambda x: (not x.get('favorite', False), 
                                                  x.get('added_date', '')))
            
            for location in sorted_locations:
                # Indicatori di stato
                status_icons = []
                if location.get("last_selected", False):
                    status_icons.append(ft.Icon(ft.Icons.MY_LOCATION, 
                                              color=self.Colors["accent"], size=16))
                if location.get("favorite", False):
                    status_icons.append(ft.Icon(ft.Icons.STAR, 
                                              color="#FFD700", size=16))
                
                # Informazioni aggiuntive
                location_info = [
                    ft.Text(location["name"], weight=ft.FontWeight.BOLD, size=13, 
                           color=self.Colors["text"]),
                    ft.Text(f"{location['lat']:.4f}, {location['lon']:.4f}", 
                           size=11, color=self.Colors["text_secondary"])
                ]
                
                # Aggiungi paese se disponibile
                if location.get("country") and location["country"] != "Unknown":
                    location_info.insert(1, 
                        ft.Text(f"🏳️ {location['country']}", 
                               size=11, color=self.Colors["text_secondary"]))
                
                location_row = ft.Container(
                    content=ft.Row([
                        # Status indicators e info località
                        ft.Row([
                            # Status icons
                            ft.Container(
                                content=ft.Row(status_icons, spacing=2),
                                width=40,
                            ),
                            # Location info
                            ft.Column(location_info, spacing=2, expand=True),
                        ], spacing=8, expand=True),
                        
                        # Action buttons con design coerente
                        ft.Row([
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.STAR if location.get("favorite") else ft.Icons.STAR_BORDER,
                                    icon_color="#FFD700" if location.get("favorite") else self.Colors["text_secondary"],
                                    tooltip="Toggle Preferito",
                                    on_click=lambda e, loc_id=location["id"]: self.toggle_favorite(loc_id),
                                    icon_size=18
                                ),
                                width=40, height=40,
                                border_radius=20,
                                bgcolor=ft.Colors.with_opacity(0.05, self.Colors["text"]) if not location.get("favorite") else ft.Colors.with_opacity(0.1, "#FFD700")
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.LOCATION_ON,
                                    icon_color=self.Colors["accent"],
                                    tooltip="Usa Località",
                                    on_click=lambda e, loc=location: self.use_location(loc),
                                    icon_size=18
                                ),
                                width=40, height=40,
                                border_radius=20,
                                bgcolor=ft.Colors.with_opacity(0.1, self.Colors["accent"])
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.SETTINGS,
                                    icon_color=self.Colors["text_secondary"],
                                    tooltip="Configurazioni",
                                    on_click=lambda e, loc=location: self.show_location_settings(loc),
                                    icon_size=18
                                ),
                                width=40, height=40,
                                border_radius=20,
                                bgcolor=ft.Colors.with_opacity(0.05, self.Colors["text"])
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="#F44336",
                                    tooltip="Rimuovi",
                                    on_click=lambda e, loc_id=location["id"]: self.remove_location(loc_id),
                                    icon_size=18
                                ),
                                width=40, height=40,
                                border_radius=20,
                                bgcolor=ft.Colors.with_opacity(0.1, "#F44336")
                            ),
                        ], spacing=8)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=16,
                    margin=ft.margin.symmetric(vertical=4),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.Colors["text"])),
                    border_radius=12,
                    bgcolor=self.Colors["surface"] if not location.get("last_selected") else ft.Colors.with_opacity(0.1, self.Colors["accent"]),
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
                )
                locations_column.controls.append(location_row)
        
        return ft.Container(
            content=locations_column,
            height=220,
            padding=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.Colors["text"])),
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.02, self.Colors["text"])
        )
    
    def get_texts(self):
        """Get localized texts based on current language."""
        if self.language == "en":
            return {
                "title": "Location Manager", "dialog_title": "Professional Location Manager",
                "description": "Manage your saved weather locations with professional features",
                "add_location": "Add New Location", "saved_locations": "Saved Locations",
                "open_location_input": "Add New Location",
                "add": "Add", "use_current": "Use Current Location", "close": "Close",
                "stats": "Statistics", "export": "Export", "import": "Import"
            }
        else:  # Italian (default)
            return {
                "title": "Gestione Località", "dialog_title": "Gestione Professionale Località",
                "description": "Gestisci le tue località meteo con funzionalità avanzate",
                "add_location": "Aggiungi Nuova Località", "saved_locations": "Località Salvate",
                "open_location_input": "Inserisci Località",
                "add": "Aggiungi", "use_current": "Usa Posizione Attuale", "close": "Chiudi",
                "stats": "Statistiche", "export": "Esporta", "import": "Importa"
            }
    
    async def search_locations(self, e=None):
        """Search for locations using the integrated search."""
        if self.is_searching:
            return
            
        city = self.city_field.value.strip()
        if not city:
            self.show_snackbar("Inserisci almeno il nome della città", "#FF9800")
            return
        
        self.is_searching = True
        self.search_button.text = "🔍 Ricerca..."
        self.search_button.disabled = True
        self.page.update()
        
        try:
            # Prepara query di ricerca strutturata
            state = self.state_field.value.strip() if self.state_field.value else None
            country = self.country_field.value.strip() if self.country_field.value else None
            
            # Esegui ricerca
            results = await self.geocoding_service.search_by_structured_input(city, state, country)
            
            if results:
                self.display_search_results(results)
            else:
                self.show_search_message("Nessuna località trovata", "#FF9800")
                
        except Exception as ex:
            logger.error(f"Errore durante la ricerca: {ex}")
            self.show_search_message(f"Errore nella ricerca: {str(ex)}", "#F44336")
        finally:
            self.is_searching = False
            self.search_button.text = "🔍 Cerca"
            self.search_button.disabled = False
            self.page.update()
    
    def display_search_results(self, results):
        """Display search results in the integrated container."""
        if not self.search_results_container:
            return
            
        results_column = ft.Column([], spacing=5)
        
        # Header risultati
        results_column.controls.append(
            ft.Text(f"🔍 Trovate {len(results)} località:", 
                   weight=ft.FontWeight.BOLD, color=self.Colors["text"], size=14)
        )
        
        # Lista risultati
        for i, candidate in enumerate(results[:10]):  # Limita a 10 risultati
            result_card = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(candidate.full_name, weight=ft.FontWeight.BOLD, 
                               size=13, color=self.Colors["text"]),
                        ft.Text(f"📍 {candidate.lat:.4f}, {candidate.lon:.4f}", 
                               size=11, color=self.Colors["text_secondary"]),
                        ft.Text(f"🏳️ {candidate.country_code}", 
                               size=11, color=self.Colors["text_secondary"])
                    ], spacing=2, expand=True),
                    ft.ElevatedButton(
                        "✅ Aggiungi",
                        on_click=lambda e, loc=candidate: self.add_location_from_search(loc),
                        bgcolor=ft.Colors.with_opacity(0.1, self.Colors["accent"]),
                        color=self.Colors["accent"],
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
                        height=35
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=8,
                border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.Colors["text"])),
                border_radius=8,
                bgcolor=self.Colors["surface"],
                animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT)
            )
            results_column.controls.append(result_card)
        
        # Aggiorna container risultati
        self.search_results_container.content = results_column
        self.search_results_container.visible = True
        self.search_results_container.height = min(300, len(results) * 70 + 50)
        self.page.update()
    
    def show_search_message(self, message, color):
        """Show a message in the search results container."""
        message_content = ft.Column([
            ft.Icon(ft.Icons.INFO_OUTLINE, size=32, color=color),
            ft.Text(message, text_align=ft.TextAlign.CENTER, color=color)
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.search_results_container.content = message_content
        self.search_results_container.visible = True
        self.search_results_container.height = 100
        self.page.update()
    
    def add_location_from_search(self, candidate):
        """Add a location from search results."""
        try:
            result = self.location_service.add_location(
                name=candidate.full_name,
                lat=candidate.lat,
                lon=candidate.lon,
                country=candidate.country_code
            )
            
            if result:
                logger.info(f"Posizione aggiunta con successo: {candidate.full_name}")
                
                # Ricarica le località
                self.location_service.load_locations()
                
                # Nascondi risultati ricerca
                self.clear_search()
                
                # Refresh lista località
                self.refresh_locations_list()
                
                # Snackbar di successo
                self.show_snackbar(f"✅ Aggiunta: {candidate.full_name}", "#4CAF50")
                
                # Callback per aggiornare UI principale
                if self.update_weather_callback:
                    self.update_weather_callback()
                    
            else:
                self.show_snackbar("⚠️ Località già esistente", "#FF9800")
                
        except Exception as e:
            logger.error(f"Errore durante l'aggiunta: {e}")
            self.show_snackbar(f"Errore: {str(e)}", "#F44336")
    
    def clear_search(self):
        """Clear search results and reset form."""
        self.search_results_container.visible = False
        self.search_results_container.height = 0
        self.city_field.value = ""
        self.state_field.value = ""
        self.country_field.value = ""
        self.page.update()
    
    def refresh_locations_list(self):
        """Refresh only the locations list without recreating the entire dialog."""
        try:
            # Trova il container della lista località nel dialog
            if self.dialog and self.dialog.content and hasattr(self.dialog.content, 'content'):
                column = self.dialog.content.content
                if hasattr(column, 'controls'):
                    # Trova l'indice del container delle località (dovrebbe essere l'ultimo prima del Container(height=15))
                    for i, control in enumerate(column.controls):
                        if hasattr(control, 'content') and hasattr(control.content, 'controls'):
                            # Sostituisci con la nuova lista
                            column.controls[i] = self.create_locations_list()
                            break
                    
                    self.page.update()
                    
        except Exception as ex:
            logger.error(f"Errore durante il refresh della lista: {ex}")
            # Fallback: ricrea tutto il dialog
            self.show_dialog()
    
    def toggle_favorite(self, location_id: str):
        """Toggle favorite status using professional service."""
        try:
            location = self.location_service.get_location_by_id(location_id)
            if not location:
                return
                
            # Usa il metodo toggle_favorite del servizio invece di set_favorite
            success = self.location_service.toggle_favorite(location_id)
            
            if success and self.page:
                # Ottieni lo stato aggiornato dopo il toggle
                updated_location = self.location_service.get_location_by_id(location_id)
                is_favorite = updated_location.get("favorite", False) if updated_location else False
                status_text = "aggiunto ai" if is_favorite else "rimosso dai"
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Località {status_text} preferiti"),
                    bgcolor=self.Colors["accent"]
                )
                self.page.snack_bar.open = True
                self.page.update()
                
                # Refresh dialog - usa il nuovo metodo di refresh sicuro
                self.refresh_dialog_safely()
            
        except Exception as ex:
            logger.error(f"Errore nel toggle favorite: {ex}")
    
    def refresh_dialog_safely(self):
        """Safely refresh the dialog without causing overlay issues."""
        try:
            if self.dialog and self.page:
                # Chiudi il dialog corrente usando page.close()
                self.page.close(self.dialog)
                    
                # Ricrea il dialog
                self.dialog = self.create_dialog()
                self.page.open(self.dialog)
                
        except Exception as ex:
            logger.error(f"Errore durante il refresh sicuro del dialog: {ex}")
            # Se c'è un errore, prova a mostrare il dialog da zero
            self.show_dialog()
    
    def use_location(self, location):
        """Use selected location as current location."""
        try:
            # Seleziona la località nel servizio
            success = self.location_service.select_location(location['id'])
            
            if success:
                # Aggiorna lo stato nell'app principale usando il metodo sincrono
                if self.state_manager:
                    self.state_manager.set_state_sync('current_lat', location['lat'])
                    self.state_manager.set_state_sync('current_lon', location['lon'])
                    self.state_manager.set_state_sync('current_city', location['name'])
                
                # Triggerare l'aggiornamento completo dell'UI
                if self.update_weather_callback:
                    # Ottieni impostazioni correnti
                    language = self.state_manager.get_state("language") or "it"
                    unit = self.state_manager.get_state("unit") or "metric"
                    
                    # Chiama il callback per aggiornare l'UI usando run_task di Flet
                    self.page.run_task(self._update_ui_async, location['name'], language, unit)
                
                if self.page:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Aggiornando meteo per: {location['name']}"),
                        bgcolor=self.Colors["accent"]
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                
                # Close dialog after selection
                self.close_dialog()
                
        except Exception as ex:
            logger.error(f"Errore nell'uso della località: {ex}")
    
    async def _update_ui_async(self, city_name, language, unit):
        """Aggiorna l'UI in modo asincrono."""
        try:
            if self.update_weather_callback:
                result = await self.update_weather_callback(city_name, language, unit)
                if result:
                    logger.info(f"UI aggiornata con successo per: {city_name}")
                else:
                    logger.warning(f"Errore nell'aggiornamento UI per: {city_name}")
        except Exception as ex:
            logger.error(f"Errore nell'aggiornamento asincrono: {ex}")
    
    def remove_location(self, location_id: str):
        """Remove a location using professional service."""
        try:
            location = self.location_service.get_location_by_id(location_id)
            if not location:
                return
                
            location_name = location['name']
            success = self.location_service.remove_location(location_id)
            
            if success and self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Località '{location_name}' rimossa"),
                    bgcolor="#F44336"
                )
                self.page.snack_bar.open = True
                self.page.update()
                
            # Refresh dialog
            self.show_dialog()
            
        except Exception as ex:
            logger.error(f"Errore nella rimozione della località: {ex}")
    
    def show_location_settings(self, location):
        """Show location-specific settings dialog."""
        # Per ora mostra solo un messaggio, in futuro implementeremo il dialog completo
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Configurazioni per {location['name']} (in sviluppo)"),
                bgcolor=self.Colors["accent"]
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def show_statistics(self):
        """Show location statistics dialog."""
        try:
            stats = self.location_service.get_statistics()
            
            stats_content = ft.Column([
                ft.Text("Statistiche Località", weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(),
                ft.Text(f"📍 Totale località: {stats['total_locations']}"),
                ft.Text(f"⭐ Località preferite: {stats['favorite_locations']}"),
                ft.Text(f"🗂️ File storage: {stats['storage_size_bytes']} bytes"),
                
                ft.Text("📊 Paesi rappresentati:", weight=ft.FontWeight.BOLD, size=14),
                *[ft.Text(f"  🏳️ {country}: {count}") 
                  for country, count in stats['countries'].items()],
                
            ], spacing=8)
            
            self.stats_dialog = ft.AlertDialog(
                title=ft.Text("Statistiche"),
                content=ft.Container(content=stats_content, width=300),
                actions=[ft.TextButton("Chiudi", on_click=lambda e: self.close_stats_dialog())]
            )
            
            self.page.open(self.stats_dialog)
            
        except Exception as e:
            logger.error(f"Errore durante la visualizzazione delle statistiche: {e}")
            self.show_snackbar("Errore durante il caricamento delle statistiche")
    
    def refresh_locations(self):
        """Refresh the locations list."""
        try:
            logger.info("Refreshing locations list")
            self.show_dialog()  # Ricarica completamente il dialog
            self.show_snackbar("Lista località aggiornata!", "#4CAF50")
        except Exception as e:
            logger.error(f"Errore durante l'aggiornamento: {e}")
            self.show_snackbar("Errore durante l'aggiornamento")
    
    def export_locations(self):
        """Export locations to a file."""
        try:
            all_locations = self.location_service.get_all_locations()
            if not all_locations:
                self.show_snackbar("Nessuna località da esportare")
                return
            
            # Simulazione esportazione (in futuro potresti implementare il salvataggio file)
            export_count = len(all_locations)
            logger.info(f"Exported {export_count} locations")
            self.show_snackbar(f"Esportate {export_count} località!", "#4CAF50")
            
        except Exception as e:
            logger.error(f"Errore durante l'esportazione: {e}")
            self.show_snackbar("Errore durante l'esportazione")
    
    def close_stats_dialog(self):
        """Close statistics dialog properly."""
        try:
            if self.stats_dialog and self.page:
                self.page.close(self.stats_dialog)
                self.stats_dialog = None
                
        except Exception as ex:
            logger.error(f"Errore durante la chiusura del stats dialog: {ex}")
    
    def use_current_location(self):
        """Use current GPS location."""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Funzionalità GPS in sviluppo"),
                bgcolor=self.Colors["accent"]
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def close_dialog(self, e=None):
        """Close the dialog properly using page.close()."""
        try:
            logger.info("Iniziando chiusura LocationManagerDialog")
            
            # Chiudi prima eventuali dialog secondari (stats)
            if self.stats_dialog and self.page:
                self.page.close(self.stats_dialog)
                self.stats_dialog = None
            
            # Poi chiudi il dialog principale usando page.close()
            if self.dialog and self.page:
                self.page.close(self.dialog)
                self.dialog = None
            
            logger.info("LocationManagerDialog chiuso correttamente")
            
        except Exception as ex:
            logger.error(f"Errore durante la chiusura del dialog: {ex}")
            # Fallback: prova a chiudere forzatamente
            if self.dialog and self.page:
                try:
                    self.page.close(self.dialog)
                    self.dialog = None
                except Exception:
                    pass

    def show_snackbar(self, message, color="#4CAF50"):
        """Helper per mostrare notifiche snackbar."""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=color
            )
            self.page.snack_bar.open = True
            self.page.update()

    def cleanup(self):
        """Cleanup method to unregister observers and close dialogs."""
        try:
            # Chiudi tutti i dialog aperti usando page.close()
            if self.dialog and self.page:
                self.page.close(self.dialog)
                self.dialog = None
                
            if self.stats_dialog and self.page:
                self.page.close(self.stats_dialog)
                self.stats_dialog = None
            
            # Unregister observers
            if self.state_manager:
                self.state_manager.unregister_observer("language_event", self.update_ui)
                self.state_manager.unregister_observer("theme_event", self.update_ui)
                
            logger.info("LocationManagerDialog cleanup completato")
            
        except Exception as ex:
            logger.error(f"Errore durante il cleanup: {ex}")
