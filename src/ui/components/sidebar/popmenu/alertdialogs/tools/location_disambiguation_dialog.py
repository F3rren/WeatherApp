#!/usr/bin/env python3

import flet as ft
from typing import List, Callable
from services.location.geocoding_service import LocationCandidate
from utils.responsive_utils import ResponsiveTextFactory
import logging

logger = logging.getLogger(__name__)


class LocationDisambiguationDialog:
    """Dialog per la disambiguazione quando ci sono più località con lo stesso nome."""
    
    def __init__(self, page: ft.Page, candidates: List[LocationCandidate], 
                 on_selection: Callable[[LocationCandidate], None]):
        self.page = page
        self.candidates = candidates
        self.on_selection = on_selection
        self.dialog = None
        
        # Get theme colors
        self.is_dark = page.theme_mode == ft.ThemeMode.DARK
        self.colors = self._get_theme_colors()
    
    def _get_theme_colors(self):
        """Get theme-appropriate colors."""
        if self.is_dark:
            return {
                "bg": "#1E1E1E", "surface": "#2D2D2D", "text": "#FFFFFF",
                "text_secondary": "#B0B0B0", "border": "#404040", "accent": "#2196F3",
                "hover": "#3A3A3A", "selected": "#2196F320"
            }
        else:
            return {
                "bg": "#FFFFFF", "surface": "#F5F5F5", "text": "#212121",
                "text_secondary": "#757575", "border": "#E0E0E0", "accent": "#2196F3",
                "hover": "#F0F0F0", "selected": "#2196F320"
            }
    
    def show(self):
        """Mostra il dialog di disambiguazione."""
        if not self.candidates:
            return
        
        self.dialog = self._create_dialog()
        self.page.open(self.dialog)
    
    def _create_dialog(self):
        """Crea il dialog di disambiguazione."""
        # Header con informazioni
        header_text = "Sono state trovate più località con questo nome. Seleziona quella corretta:"
        if len(self.candidates) > 5:
            header_text += f" (mostrate le prime 5 di {len(self.candidates)} risultati)"
        
        # Lista delle opzioni
        options_column = ft.Column([], spacing=5, scroll=ft.ScrollMode.AUTO)
        
        # Mostra massimo 5 risultati per non sovraccaricare l'UI
        display_candidates = self.candidates[:5]
        
        for i, candidate in enumerate(display_candidates):
            # Crea il contenuto per ogni opzione
            option_content = self._create_option_content(candidate, i)
            options_column.controls.append(option_content)
        
        # Contenuto principale
        content = ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LOCATION_SEARCHING, 
                               color=self.colors["accent"], size=24),
                        ResponsiveTextFactory.create_adaptive_text(
                            page=self.page,
                            text="Seleziona Località",
                            text_type="title_small",
                            color=self.colors["text"],
                            weight=ft.FontWeight.BOLD
                        )
                    ], spacing=10),
                    padding=ft.padding.only(bottom=10)
                ),
                
                # Descrizione
                ResponsiveTextFactory.create_adaptive_text(
                    page=self.page,
                    text=header_text,
                    text_type="body_primary",
                    color=self.colors["text_secondary"],
                    text_align=ft.TextAlign.LEFT
                ),
                
                ft.Divider(color=self.colors["border"]),
                
                # Opzioni
                options_column,
                
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            width=600, height=400, padding=20, bgcolor=self.colors["bg"]
        )
        
        return ft.AlertDialog(
            modal=True, scrollable=True,
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
    
    def _create_option_content(self, candidate: LocationCandidate, index: int):
        """Crea il contenuto per una singola opzione."""
        # Icona bandiera paese (emoji semplificata)
        flag_emoji = self._get_country_flag(candidate.country_code)
        
        # Informazioni principali
        main_info = ft.Column([
            ResponsiveTextFactory.create_adaptive_text(
                text=candidate.name,
                text_type="body_primary",
                color=self.colors["text"],
                weight=ft.FontWeight.BOLD
            ),
            ResponsiveTextFactory.create_adaptive_text(
                text=f"{flag_emoji} {candidate.country}" + 
                     (f", {candidate.state}" if candidate.state else ""),
                text_type="label_small",
                color=self.colors["text_secondary"]
            ),
            ResponsiveTextFactory.create_adaptive_text(
                text=f"📍 {candidate.lat:.4f}, {candidate.lon:.4f}",
                text_type="label_small",
                color=self.colors["text_secondary"]
            ),
        ], spacing=2, expand=True)
        
        # Informazioni aggiuntive
        additional_info = ft.Column([
            ResponsiveTextFactory.create_adaptive_text(
                text=f"👥 {candidate.population:,} ab." if candidate.population > 0 else "👥 N/A",
                text_type="label_small",
                color=self.colors["text_secondary"]
            ),
            ResponsiveTextFactory.create_adaptive_text(
                text=f"🎯 {candidate.relevance_score:.1f}%" if candidate.relevance_score > 0 else "",
                text_type="label_small",
                color=self.colors["accent"]
            ),
        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END)
        
        # Container principale
        option_container = ft.Container(
            content=ft.Row([
                # Numero opzione
                ft.Container(
                    content=ResponsiveTextFactory.create_adaptive_text(
                        text=str(index + 1),
                        text_type="label_small",
                        color=self.colors["accent"],
                        weight=ft.FontWeight.BOLD
                    ),
                    width=30, height=30, 
                    border_radius=15,
                    bgcolor=f"{self.colors['accent']}20",
                    alignment=ft.alignment.center
                ),
                
                # Informazioni principali
                main_info,
                
                # Informazioni aggiuntive
                additional_info,
                
                # Pulsante selezione
                ft.IconButton(
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    icon_color=self.colors["accent"],
                    tooltip="Seleziona questa località",
                    on_click=lambda e, c=candidate: self._select_candidate(c)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
            padding=15,
            border=ft.border.all(1, self.colors["border"]),
            border_radius=10,
            bgcolor=self.colors["surface"],
            on_click=lambda e, c=candidate: self._select_candidate(c),
            ink=True,
            on_hover=lambda e: self._on_hover(e, option_container)
        )
        
        return option_container
    
    def _get_country_flag(self, country_code: str) -> str:
        """Ottieni emoji bandiera per codice paese."""
        flags = {
            "IT": "🇮🇹", "FR": "🇫🇷", "US": "🇺🇸", "ES": "🇪🇸", 
            "DE": "🇩🇪", "GB": "🇬🇧", "UK": "🇬🇧"
        }
        return flags.get(country_code.upper(), "🏳️")
    
    def _on_hover(self, e, container):
        """Gestisci hover effect."""
        if e.data == "true":  # Mouse enter
            container.bgcolor = self.colors["hover"]
        else:  # Mouse leave
            container.bgcolor = self.colors["surface"]
        container.update()
    
    def _select_candidate(self, candidate: LocationCandidate):
        """Gestisci selezione di un candidato."""
        self._close_dialog()
        if self.on_selection:
            self.on_selection(candidate)
    
    def _close_dialog(self, e=None):
        """Chiudi il dialog."""
        if self.dialog:
            self.page.close(self.dialog)
