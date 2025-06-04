"""
Layout Manager per MeteoApp.
Centralizza la gestione del layout dell'applicazione.
"""

import flet as ft
import logging
from typing import Dict

from layout.frontend.layout_builder import LayoutBuilder
from config import LIGHT_THEME, DARK_THEME
from components.responsive_text_handler import ResponsiveTextHandler

class LayoutManager:
    """
    Layout manager class for the MeteoApp.
    Handles the construction and management of UI layout components.
    """
    
    def __init__(self, page: ft.Page):
        """
        Inizializza il gestore del layout.
        
        Args:
            page: Flet page object
        """
        self.page = page
        self.containers = {}
        self.layout = None
        
        # Nuovo - Dimensioni iniziali e proporzioni dei container
        self.container_heights = {
            'sidebar': 80,       # Altezza fissa per la sidebar
            'info': 180,         # Contenitore info principale
            'weekly': 320,       # Previsioni settimanali
            'air_pollution': 320,  # Informazioni inquinamento
            'chart': 350,        # Grafico temperature
            'air_pollution_chart': 350,  # Grafico inquinamento
        }
        
        # Configurazione delle colonne per diversi breakpoint
        self.column_sizes = {
            'sidebar': {"xs": 12},
            'info': {"xs": 12, "md": 12, "lg": 12},
            'weekly': {"xs": 12, "sm": 12, "md": 12, "lg": 8},
            'air_pollution': {"xs": 12, "md": 4, "lg": 4},
            'air_pollution_chart': {"xs": 12, "sm": 6, "md": 8, "lg": 6},
            'chart': {"xs": 12, "sm": 6, "md": 4, "lg": 6}
        }
        
        # Proporzioni per ridimensionamento responsive
        self.height_ratios = {
            'small': 0.7,     # Per schermi piccoli (<600px)
            'medium': 0.85,   # Per schermi medi (600-1200px)
            'large': 1.0      # Per schermi grandi (>1200px)
        }
        
        # Inizializzazione del ResponsiveHandler per il layout
        self.responsive_handler = ResponsiveTextHandler(
            page=self.page,
            base_sizes=self.container_heights,
            breakpoints=[600, 900, 1200, 1600]
        )
        
        # Gestione del ridimensionamento
        if self.page:
            original_resize_handler = self.page.on_resize
            
            def combined_resize_handler(e):
                # Aggiorna i container in base alla dimensione della finestra
                self._update_container_sizes()
                
                # Chiama anche l'handler originale se esiste
                if original_resize_handler:
                    original_resize_handler(e)
            
            self.page.on_resize = combined_resize_handler
    
    def create_containers(self,                         
                         sidebar_content,
                         info_content,
                         weekly_content,
                         chart_content,
                         air_pollution_chart_content,
                         air_pollution_content,
                         animation_duration=500,
                         animation_curve=ft.AnimationCurve.EASE_IN_OUT) -> None:
        """
        Crea tutti i contenitori per il layout dell'applicazione.
        
        Args:
            sidebar_content: Oggetto Sidebar da inserire nel container
            info_content: Contenuto del container info meteo
            weekly_content: Contenuto del container previsioni settimanali
            chart_content: Contenuto del container grafico
            air_pollution_chart_content: Contenuto del container grafico inquinamento
            air_pollution_content: Contenuto del container informazioni inquinamento
            animation_duration: Durata delle animazioni in millisecondi
            animation_curve: Curva di animazione
        """
        # Calcola le altezze iniziali in base alla dimensione della finestra
        self._update_container_sizes()
        
        self.containers['sidebar'] = LayoutBuilder.build_content_container(
            sidebar_content, 
            self.column_sizes['sidebar'],
            animation_duration,
            animation_curve,
            height=self.container_heights['sidebar']
        )
        
        self.containers['info'] = LayoutBuilder.build_content_container(
            info_content,
            self.column_sizes['info'],
            animation_duration,
            animation_curve,
            height=self.container_heights['info']
        )
        
        self.containers['weekly'] = LayoutBuilder.build_content_container(
            weekly_content,
            self.column_sizes['weekly'],
            animation_duration,
            animation_curve,
            height=self.container_heights['weekly']
        )
        
        self.containers['air_pollution'] = LayoutBuilder.build_content_container(
            air_pollution_content,
            self.column_sizes['air_pollution'],
            animation_duration,
            animation_curve,
            height=self.container_heights['air_pollution']
        )

        self.containers['air_pollution_chart'] = LayoutBuilder.build_content_container(
            air_pollution_chart_content,
            self.column_sizes['air_pollution_chart'],
            animation_duration,
            animation_curve,
            height=self.container_heights['air_pollution_chart']
        )

        self.containers['chart'] = LayoutBuilder.build_content_container(
            chart_content,
            self.column_sizes['chart'],
            animation_duration,
            animation_curve,
            height=self.container_heights['chart']
        )
    
    def _update_container_sizes(self):
        """
        Aggiorna le dimensioni dei container in base alla dimensione della finestra.
        """
        if not self.page:
            return
        
        # Determina il fattore di scala in base alla larghezza della finestra
        window_width = self.page.window_width if hasattr(self.page, 'window_width') else 1200
        
        if window_width < 600:
            scale_factor = self.height_ratios['small']
        elif window_width < 1200:
            scale_factor = self.height_ratios['medium']
        else:
            scale_factor = self.height_ratios['large']
        
        # Calcola la nuova altezza per ciascun container
        for container_key in self.container_heights.keys():
            base_height = self.container_heights[container_key]
            
            # La sidebar ha un'altezza fissa
            if container_key == 'sidebar':
                continue
                
            # Calcola l'altezza scalata
            new_height = base_height * scale_factor
            
            # Applica la nuova altezza se il container esiste
            if container_key in self.containers and self.containers[container_key]:
                self.containers[container_key].height = new_height
        
        # Aggiorna la pagina se necessario
        if hasattr(self.page, 'update'):
            self.page.update()
        
    def build_layout(self) -> ft.Control:
        """
        Costruisce il layout principale dell'applicazione.
        
        Returns:
            ft.Control: Il layout principale
        """
        self.layout = LayoutBuilder.build_main_layout(
            self.containers['sidebar'],
            self.containers['info'],
            self.containers['weekly'],
            self.containers['air_pollution'],
            self.containers['chart'],
            self.containers['air_pollution_chart']
        )
        return self.layout
    
    def get_all_containers(self) -> Dict[str, ft.Container]:
        """
        Restituisce tutti i contenitori del layout.
        
        Returns:
            Dict[str, ft.Container]: Dizionario dei contenitori
        """
        return self.containers
    
    def update_container_colors(self, theme_mode: ft.ThemeMode) -> None:
        """
        Aggiorna i colori dei contenitori in base al tema.
        
        Args:
            theme_mode: Modalità tema (chiaro/scuro)
        """
        if not self.containers:
            logging.warning("Containers not initialized. Cannot update colors.")
            return

        # Aggiorna i container con i gradienti
        self.update_container_gradients(theme_mode)
        
        # Aggiorna anche il colore di sfondo della pagina
        theme = LIGHT_THEME if theme_mode == ft.ThemeMode.LIGHT else DARK_THEME
        self.page.bgcolor = theme.get("BACKGROUND", "#f5f5f5" if theme_mode == ft.ThemeMode.LIGHT else "#1a1a1a")
        self.page.update()
    
    def update_column_sizes(self, new_sizes):
        """
        Aggiorna le dimensioni delle colonne dei container.
        
        Args:
            new_sizes (dict): Dizionario con le nuove dimensioni delle colonne
                              Es: {'weekly': {"xs": 12, "md": 6, "lg": 6}}
        """
        # Aggiorna le configurazioni delle colonne
        for container_name, col_config in new_sizes.items():
            if container_name in self.column_sizes:
                self.column_sizes[container_name] = col_config
                
                # Aggiorna anche il container esistente se presente
                if container_name in self.containers and self.containers[container_name]:
                    self.containers[container_name].col = col_config
        
        # Aggiorna la pagina se necessario
        if hasattr(self.page, 'update'):
            self.page.update()
    
    def debug_column_sizes(self):
        """
        Stampa le informazioni sulle dimensioni delle colonne per debugging.
        """
        print("==== COLUMN SIZES DEBUG ====")
        
        # Controlla le configurazioni
        print("CONFIGURAZIONI COLONNE:")
        for name, config in self.column_sizes.items():
            print(f"{name}: {config}")
        
        # Controlla i valori effettivamente applicati
        print("\nVALORI APPLICATI AI CONTAINER:")
        for name, container in self.containers.items():
            if container:
                print(f"{name}: col={container.col}")
        
        print("===========================")

    def force_layout_update(self):
        """
        Forza l'aggiornamento del layout ricreando i container con le dimensioni correnti.
        """
        # Memorizza i contenuti attuali
        contents = {}
        for name, container in self.containers.items():
            if container and hasattr(container, 'content'):
                contents[name] = container.content
        
        # Ricrea i container solo se abbiamo i contenuti
        if len(contents) >= 6:  # Verifichiamo di avere tutti i contenuti necessari
            self.create_containers(
                sidebar_content=contents.get('sidebar'),
                info_content=contents.get('info'),
                weekly_content=contents.get('weekly'),
                chart_content=contents.get('chart'),
                air_pollution_chart_content=contents.get('air_pollution_chart'),
                air_pollution_content=contents.get('air_pollution')
            )
            
            # Ricostruisci il layout
            self.build_layout()
            
            # Aggiorna la pagina
            if self.page:
                self.page.update()

