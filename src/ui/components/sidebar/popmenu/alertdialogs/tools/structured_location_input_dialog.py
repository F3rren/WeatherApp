#!/usr/bin/env python3

import flet as ft
from typing import Callable
from services.location.geocoding_service import LocationCandidate
import logging

logger = logging.getLogger(__name__)


class StructuredLocationInputDialog:
    """Dialog per input strutturato di località (Città, Regione/Stato, Paese)."""
    
    def __init__(self, page: ft.Page, on_location_selected: Callable[[LocationCandidate], None], on_close_callback: Callable[[], None] = None):
        self.page = page
        self.on_location_selected = on_location_selected
        self.on_close_callback = on_close_callback
        self.dialog = None
        
        # Input fields
        self.city_field = None
        self.state_field = None
        self.country_field = None
        self.search_button = None
        self.results_container = None
        
        # Get theme colors
        self.is_dark = page.theme_mode == ft.ThemeMode.DARK
        self.colors = self._get_theme_colors()
    
    def _get_theme_colors(self):
        """Get theme-appropriate colors."""
        if self.is_dark:
            return {
                "bg": "#1E1E1E", "surface": "#2D2D2D", "text": "#FFFFFF",
                "text_secondary": "#B0B0B0", "border": "#404040", "accent": "#2196F3",
                "success": "#4CAF50", "warning": "#FF9800", "error": "#F44336"
            }
        else:
            return {
                "bg": "#FFFFFF", "surface": "#F5F5F5", "text": "#212121",
                "text_secondary": "#757575", "border": "#E0E0E0", "accent": "#2196F3",
                "success": "#4CAF50", "warning": "#FF9800", "error": "#F44336"
            }
    
    def show(self):
        """Mostra il dialog di input strutturato."""
        self.dialog = self._create_dialog()
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def _create_dialog(self):
        """Crea il dialog di input strutturato."""
        # Campi di input
        self.city_field = ft.TextField(
            label="Città *",
            hint_text="Es: Milano, London, New York, Tokyo",
            prefix_icon=ft.Icons.LOCATION_CITY,
            bgcolor=self.colors["surface"],
            color=self.colors["text"],
            label_style=ft.TextStyle(color=self.colors["text"]),
            hint_style=ft.TextStyle(color=self.colors["text_secondary"]),
            border_radius=8,
            on_change=self._on_input_change,
            autofocus=True
        )
        
        self.state_field = ft.TextField(
            label="Regione/Stato",
            hint_text="Es: Lombardia, Texas, Bavaria",
            prefix_icon=ft.Icons.MAP,
            bgcolor=self.colors["surface"],
            color=self.colors["text"],
            label_style=ft.TextStyle(color=self.colors["text"]),
            hint_style=ft.TextStyle(color=self.colors["text_secondary"]),
            border_radius=8,
            on_change=self._on_input_change
        )
        
        self.country_field = ft.TextField(
            label="Paese",
            hint_text="Es: Italia, Francia, Germania",
            prefix_icon=ft.Icons.PUBLIC,
            bgcolor=self.colors["surface"],
            color=self.colors["text"],
            label_style=ft.TextStyle(color=self.colors["text"]),
            hint_style=ft.TextStyle(color=self.colors["text_secondary"]),
            border_radius=8,
            on_change=self._on_input_change
        )
        
        # Pulsante di ricerca
        self.search_button = ft.ElevatedButton(
            text="🔍 Cerca Località",
            icon=ft.Icons.SEARCH,
            style=ft.ButtonStyle(
                bgcolor=self.colors["accent"],
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=8)
            ),
            on_click=self._search_location,
            disabled=True
        )
        
        # Container per i risultati
        # Container dei risultati
        self.results_container = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO)
        
        # Layout principale
        content = ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD_LOCATION, color=self.colors["accent"], size=24),
                        ft.Text("Aggiungi Nuova Località", 
                               weight=ft.FontWeight.BOLD, 
                               color=self.colors["text"], size=18)
                    ], spacing=10),
                    padding=ft.padding.only(bottom=10)
                ),
                
                # Descrizione
                ft.Text(
                    "🔍 Cerca città da tutto il mondo usando l'API di OpenWeatherMap!\n"
                    "Digita il nome di una città e ottieni risultati precisi con coordinate geografiche.\n"
                    "I campi Regione/Stato e Paese sono opzionali ma aiutano a restringere la ricerca.",
                    color=self.colors["text_secondary"], 
                    size=13, 
                    text_align=ft.TextAlign.LEFT
                ),
                
                ft.Divider(color=self.colors["border"]),
                
                # Campi di input
                ft.Text("Informazioni Località", 
                       weight=ft.FontWeight.BOLD, 
                       color=self.colors["text"], size=16),
                
                self.city_field,
                self.state_field,
                self.country_field,
                
                # Pulsante ricerca
                ft.Container(
                    content=self.search_button,
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(vertical=10)
                ),
                
                ft.Divider(color=self.colors["border"]),
                
                # Risultati con indicatore scroll
                ft.Row([
                    ft.Text("Risultati Ricerca", 
                           weight=ft.FontWeight.BOLD, 
                           color=self.colors["text"], size=16),
                    ft.Icon(ft.Icons.SWIPE_VERTICAL, 
                           color=self.colors["text_secondary"], 
                           size=16,
                           tooltip="Scorri per vedere tutti i risultati")
                ], spacing=8),
                
                ft.Container(
                    content=self.results_container,
                    height=250,  # Aumentato da 200 a 250 per più spazio
                    bgcolor=self.colors["surface"],
                    border=ft.border.all(1, self.colors["border"]),
                    border_radius=8,
                    padding=8,  # Ridotto da 10 a 8 per più spazio interno
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Assicura che il contenuto non esca dal container
                    # Aggiungiamo un'ombra interna per rendere più evidente che è un'area scorrevole
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=3,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                        blur_style=ft.ShadowBlurStyle.INNER
                    )
                ),
                
            ], spacing=15, scroll=ft.ScrollMode.AUTO),
            width=550, height=500, padding=20, bgcolor=self.colors["bg"]
        )
        
        return ft.AlertDialog(
            modal=True,
            content=content,
            actions=[
                ft.TextButton(
                    icon=ft.Icons.CANCEL, 
                    text="Annulla", 
                    on_click=self._close_dialog,
                    style=ft.ButtonStyle(color=self.colors["text_secondary"])
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=self.colors["bg"],
            inset_padding=ft.padding.all(20)
        )
    
    def _on_input_change(self, e):
        """Gestisce il cambio di input per abilitare/disabilitare il pulsante."""
        city_filled = bool(self.city_field.value and self.city_field.value.strip())
        self.search_button.disabled = not city_filled
        self.search_button.update()
    
    def _search_location(self, e):
        """Esegue la ricerca della località."""
        self.results_container.controls.clear()
        
        # Ottieni valori dai campi
        city = self.city_field.value.strip()
        state = self.state_field.value.strip() if self.state_field.value else ""
        country = self.country_field.value.strip() if self.country_field.value else ""
        
        if not city:
            self._show_error("Il campo Città è obbligatorio")
            return
        
        # Mostra indicatore di caricamento
        loading = ft.Container(
            content=ft.Column([
                ft.ProgressRing(width=32, height=32, stroke_width=3, color=self.colors["accent"]),
                ft.Text("🌐 Ricerca tramite OpenWeatherMap API...", color=self.colors["text"], size=12),
                ft.Text("Interrogazione database globale città", color=self.colors["text_secondary"], size=10)
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            padding=20
        )
        self.results_container.controls.append(loading)
        self.page.update()
        
        # Usa la vera API per la ricerca
        self.page.run_task(self._search_with_api, city, state, country)
    
    async def _search_with_api(self, city: str, state: str, country: str):
        """Ricerca asincrona con API."""
        try:
            from services.location.geocoding_service import GeocodingService
            geocoding_service = GeocodingService()
            
            # Crea query strutturata  
            query_parts = [city]
            if state:
                query_parts.append(state)
            if country:
                query_parts.append(country)
            query = ", ".join(query_parts)
            
            # Effettua la ricerca
            results = await geocoding_service.search_by_structured_input(city, state, country)
            
            # Aggiorna l'UI nel thread principale
            self.results_container.controls.clear()
            
            if not results:
                # Nessun risultato
                no_results = ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SEARCH_OFF, size=48, color=self.colors["text_secondary"]),
                        ft.Text("Nessun risultato trovato", 
                               color=self.colors["text_secondary"],
                               weight=ft.FontWeight.BOLD),
                        ft.Text(f"📍 Nessuna località trovata per: {query}", 
                               color=self.colors["text_secondary"], size=12),
                        ft.Text("🌐 Ricerca effettuata tramite OpenWeatherMap Geocoding API", 
                               color=self.colors["text_secondary"], size=10)
                    ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=20
                )
                self.results_container.controls.append(no_results)
            else:
                # Mostra risultati
                for i, candidate in enumerate(results):
                    result_card = self._create_result_card(candidate, i + 1)
                    self.results_container.controls.append(result_card)
            
            self.page.update()
            logger.info(f"Ricerca completata: {len(results) if results else 0} risultati per '{query}'")
            
        except Exception as ex:
            logger.error(f"Errore nella ricerca API: {ex}")
            self.results_container.controls.clear()
            error_msg = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, size=48, color="#F44336"),
                    ft.Text("Errore nella ricerca", 
                           color="#F44336",
                           weight=ft.FontWeight.BOLD),
                    ft.Text(f"Dettaglio: {str(ex)}", 
                           color=self.colors["text_secondary"], size=11)
                ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                padding=20
            )
            self.results_container.controls.append(error_msg)
            self.page.update()
    

    
    def _display_results(self, results: list):
        """Mostra i risultati della ricerca."""
        self.results_container.controls.clear()
        
        if not results:
            # Nessun risultato
            no_results = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.SEARCH_OFF, size=48, color=self.colors["text_secondary"]),
                    ft.Text("Nessun risultato trovato", 
                           color=self.colors["text_secondary"],
                           weight=ft.FontWeight.BOLD),
                    ft.Text("Prova a modificare i termini di ricerca", 
                           color=self.colors["text_secondary"], size=12)
                ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                padding=20
            )
            self.results_container.controls.append(no_results)
        else:
            # Mostra risultati
            for i, candidate in enumerate(results):
                result_card = self._create_result_card(candidate, i + 1)
                self.results_container.controls.append(result_card)
        
        self.results_container.update()
    
    def _create_result_card(self, candidate: LocationCandidate, index: int):
        """Crea una card per un risultato di ricerca."""
        # Flag emoji
        flag_emoji = self._get_country_flag(candidate.country_code)
        
        # Informazioni principali
        main_info = ft.Column([
            ft.Text(candidate.name, 
                   weight=ft.FontWeight.BOLD, 
                   color=self.colors["text"], size=15),
            ft.Text(f"{flag_emoji} {candidate.state}, {candidate.country}" if candidate.state 
                   else f"{flag_emoji} {candidate.country}",
                   color=self.colors["text_secondary"], size=12),
            ft.Text(f"📍 {candidate.lat:.4f}, {candidate.lon:.4f}",
                   color=self.colors["text_secondary"], size=10)
        ], spacing=2, expand=True)
        
        # Card container - più compatta per migliorare lo scroll
        card = ft.Container(
            content=ft.Row([
                # Numero
                ft.Container(
                    content=ft.Text(str(index), 
                                   weight=ft.FontWeight.BOLD, 
                                   color=self.colors["accent"], size=14),
                    width=28, height=28, 
                    border_radius=14,
                    bgcolor=f"{self.colors['accent']}20",
                    alignment=ft.alignment.center
                ),
                
                # Info
                main_info,
                
                # Pulsante selezione
                ft.IconButton(
                    icon=ft.Icons.CHECK_CIRCLE,
                    icon_color=self.colors["success"],
                    tooltip="Seleziona questa località",
                    on_click=lambda e, c=candidate: self._select_location(c),
                    icon_size=20  # Icona più piccola per compattezza
                )
            ], spacing=8),  # Ridotto da 10 a 8
            padding=8,  # Ridotto da 12 a 8 per compattezza
            margin=ft.margin.only(bottom=4),  # Margine tra le card
            border=ft.border.all(1, self.colors["border"]),
            border_radius=6,  # Ridotto da 8 a 6
            bgcolor=self.colors["bg"],
            on_click=lambda e, c=candidate: self._select_location(c),
            ink=True,
            # Hover effect per migliorare l'interazione
            animate=ft.Animation(100, ft.AnimationCurve.EASE_IN_OUT)
        )
        
        return card
    
    def _get_country_flag(self, country_code: str) -> str:
        """Ottieni emoji bandiera per codice paese."""
        flags = {
            "IT": "🇮🇹", "FR": "🇫🇷", "US": "🇺🇸", "ES": "🇪🇸", 
            "DE": "🇩🇪", "GB": "🇬🇧", "UK": "🇬🇧"
        }
        return flags.get(country_code.upper(), "🏳️")
    
    def _select_location(self, candidate: LocationCandidate):
        """Gestisci selezione di una località."""
        self._close_dialog(call_callback=False)  # Non chiamare il callback di chiusura
        if self.on_location_selected:
            self.on_location_selected(candidate)
    
    def _show_error(self, message: str):
        """Mostra messaggio di errore."""
        if self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=self.colors["error"]
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _close_dialog(self, e=None, call_callback=True):
        """Chiudi il dialog."""
        try:
            if self.dialog:
                self.dialog.open = False
                if self.dialog in self.page.overlay:
                    self.page.overlay.remove(self.dialog)
                self.page.update()
                logger.info("Dialog di input strutturato chiuso correttamente")
                
                # Chiama il callback di chiusura solo se richiesto
                if call_callback and self.on_close_callback:
                    self.on_close_callback()
                    
        except Exception as ex:
            logger.error(f"Errore nella chiusura del dialog: {ex}")
            # Tentativo di recovery
            try:
                if self.dialog and hasattr(self.dialog, 'open'):
                    self.dialog.open = False
                self.page.update()
                    
                # Chiama il callback anche in caso di errore, ma solo se richiesto
                if call_callback and self.on_close_callback:
                    self.on_close_callback()
                    
            except Exception as recovery_ex:
                logger.error(f"Errore nel recovery della chiusura: {recovery_ex}")
