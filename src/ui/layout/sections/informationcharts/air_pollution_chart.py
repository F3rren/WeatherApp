import flet as ft
import math
import logging
from services.api.api_service import ApiService
from services.ui.translation_service import TranslationService
from utils.config import LIGHT_THEME, DARK_THEME, DEFAULT_LANGUAGE

from typing import Optional

class AirPollutionChartDisplay(ft.Container):
    """
    Air Pollution chart display component.
    Manages its own UI construction, updates, and state observers.
    """
    
    def __init__(self, page: ft.Page, lat: Optional[float] = None, lon: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self._lat = lat
        self._lon = lon
        
        self._api_service = ApiService()
        self._state_manager = None
        self._current_language = DEFAULT_LANGUAGE
        self._current_text_color = LIGHT_THEME.get("TEXT", ft.Colors.BLACK)
        self._pollution_data = {}
        self._cached_header = None  # Cache for header to prevent unnecessary rebuilds
        self._header_language = None  # Track which language the header was built for
        self._last_theme_mode = None  # Track theme changes for header cache invalidation


        
        if 'expand' not in kwargs:
            self.expand = True
        if 'padding' not in kwargs:
            self.padding = ft.padding.all(10)
        
        if self.page and hasattr(self.page, 'session') and self.page.session.get('state_manager'):
            self._state_manager = self.page.session.get('state_manager')
            self._state_manager.register_observer("language_event", self._safe_language_update)
            self._state_manager.register_observer("theme_event", self._safe_theme_update)
          
        self.content = self.build()
        if self.page:
            self.page.run_task(self.update_ui)

    async def update_ui(self, event_data=None):
        """Updates the UI based on state changes, fetching new data if necessary."""
        if not self.page or not self.visible:
            return

        try:
            data_changed = False
            if self._state_manager:
                new_language = self._state_manager.get_state('language') or self._current_language
                language_changed = self._current_language != new_language
                
                # Invalidate header cache when language changes
                if language_changed:
                    self._cached_header = None
                    self._header_language = None
                
                self._current_language = new_language
                data_changed = language_changed

            if not self._pollution_data or data_changed:
                if self._lat is not None and self._lon is not None:
                    self._pollution_data = await self._api_service.get_air_pollution_async(self._lat, self._lon) or {}
                else:
                    self._pollution_data = {}

            # Safe theme detection
            if self.page and hasattr(self.page, 'theme_mode'):
                is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            else:
                is_dark = False
            
            # Also invalidate header cache when theme changes
            if hasattr(self, '_last_theme_mode') and self._last_theme_mode != is_dark:
                self._cached_header = None
                self._header_language = None
            self._last_theme_mode = is_dark
            
            theme = DARK_THEME if is_dark else LIGHT_THEME
            self._current_text_color = theme.get("TEXT", ft.Colors.BLACK)

            self.content = self.build()
            # Only update if this control is already in the page
            try:
                if self.page and hasattr(self, 'page') and self.page is not None:
                    self.update()
            except Exception:
                # Control not yet added to page, update will happen when added
                pass
        except Exception as e:
            logging.error(f"AirPollutionChartDisplay: Error updating UI: {e}")

    def build(self):
        """Constructs the UI for the air pollution chart."""
        if not self._pollution_data or "co" not in self._pollution_data:
            return ft.Column([
                self._build_header(),
                ft.Container(
                    content=ft.Text(
                        TranslationService.translate_from_dict("air_pollution_chart_items", "no_air_pollution_data", self._current_language),
                        color=self._current_text_color,
                        size=14,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20),
                    expand=True,
                )
            ], spacing=0, expand=True)

        components_data = {
            "co": float(self._pollution_data.get("co", 0.0)),
            "no": float(self._pollution_data.get("no", 0.0)),
            "no2": float(self._pollution_data.get("no2", 0.0)),
            "o3": float(self._pollution_data.get("o3", 0.0)),
            "so2": float(self._pollution_data.get("so2", 0.0)),
            "pm2_5": float(self._pollution_data.get("pm2_5", 0.0)),
            "pm10": float(self._pollution_data.get("pm10", 0.0)),
            "nh3": float(self._pollution_data.get("nh3", 0.0)),
        }

        all_metrics = list(components_data.values())
        max_val = max(all_metrics) if all_metrics else 0.0
        
        raw_dynamic_max_y = 0.0
        if max_val == 0.0:
            raw_dynamic_max_y = 50.0
        else:
            buffered_max_percentage = max_val * 1.2
            buffered_max_fixed = max_val + 10.0
            raw_dynamic_max_y = max(buffered_max_percentage, buffered_max_fixed, 20.0)

        if raw_dynamic_max_y <= 0:
            final_max_y = 50.0
        elif raw_dynamic_max_y <= 50:
            final_max_y = math.ceil(raw_dynamic_max_y / 10) * 10
        elif raw_dynamic_max_y <= 200:
            final_max_y = math.ceil(raw_dynamic_max_y / 20) * 20
        else:
            final_max_y = math.ceil(raw_dynamic_max_y / 50) * 50
        final_max_y = max(final_max_y, 10.0)

        unit_text = TranslationService.translate_from_dict("air_pollution_chart_items", "micrograms_per_cubic_meter_short", self._current_language)

        bar_groups = []
        component_keys = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
        # Colori moderni e vivaci per le barre, con gradiente e opacità
        component_colors = [
            ft.Colors.with_opacity(0.85, "#FF5252"),  # CO - Rosso vivace
            ft.Colors.with_opacity(0.85, "#FF9800"),  # NO - Arancione vibrante
            ft.Colors.with_opacity(0.85, "#FFC107"),  # NO2 - Ambra brillante
            ft.Colors.with_opacity(0.85, "#8BC34A"),  # O3 - Verde lime
            ft.Colors.with_opacity(0.85, "#03A9F4"),  # SO2 - Blu cielo
            ft.Colors.with_opacity(0.85, "#9C27B0"),  # PM2.5 - Viola
            ft.Colors.with_opacity(0.85, "#673AB7"),  # PM10 - Indaco
            ft.Colors.with_opacity(0.85, "#607D8B"),  # NH3 - Blu grigio
        ]

        # Creo le barre con tooltips tradotti
        for i, key in enumerate(component_keys):
            value = components_data[key]
            # Ottieni il nome tradotto dell'inquinante
            pollutant_name = TranslationService.translate_from_dict(
                "air_pollution_chart_items", f"{key}_name", self._current_language
            )
            
            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0, to_y=value, width=32,
                            color=component_colors[i],
                            tooltip=f"{pollutant_name}: {round(value, 1)} {unit_text}",
                            border_radius=6,  # Angoli arrotondati moderni
                            border_side=ft.BorderSide(width=0),  # Rimuovi bordo
                        )
                    ]
                )
            )
        
        bottom_axis_labels_text = {
            "co": "CO", "no": "NO", "no2": "NO₂", "o3": "O₃", 
            "so2": "SO₂", "pm2_5": "PM₂.₅", "pm10": "PM₁₀", "nh3": "NH₃"
        }
        bottom_axis_labels = []
        for i, key in enumerate(component_keys):
            label_text = bottom_axis_labels_text.get(key, key.upper())
            bottom_axis_labels.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(
                        label_text, 
                        color=self._current_text_color, 
                        size=14
                    )
                )
            )

        # Determina il tema e i colori del background
        # Safe theme detection
        if self.page and hasattr(self.page, 'theme_mode'):
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        else:
            is_dark = False
        
        # Background moderno simile al temperature chart
        if is_dark:
            chart_bg_color = "#2A3441"  # Blu-grigio scuro moderno
            grid_color = ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
            border_color = ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
        else:
            chart_bg_color = "#F8FAFC"  # Blu-grigio chiaro moderno
            grid_color = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)
            border_color = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)

        # Crea il grafico con stile moderno
        chart = ft.BarChart(
            bar_groups=bar_groups,
            bgcolor=chart_bg_color,  # Background moderno
            border=ft.border.all(1, border_color),  # Bordo più delicato
            bottom_axis=ft.ChartAxis(
                labels=bottom_axis_labels,
                labels_size=14 * 3.5,
                labels_interval=1,  # Mostra tutte le etichette
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=grid_color, width=1, dash_pattern=[8, 4]  # Griglia più delicata
            ),
            vertical_grid_lines=ft.ChartGridLines(
                color=grid_color, width=0.5, dash_pattern=[8, 4]  # Linee verticali sottili
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.95, "#1E293B" if is_dark else "#FFFFFF"),
            max_y=final_max_y,
            interactive=False,  # Abilita interattività per migliore UX
            expand=True,
        )

        # Ritorna la struttura completa con header + grafico diretto
        return ft.Column([
            self._build_header(),
            chart
        ], spacing=0, expand=True)

    def _build_header(self):
        """Builds a modern header for air pollution chart section with caching."""
        # Check if we need to rebuild the header
        if self._cached_header is not None and self._header_language == self._current_language:
            return self._cached_header
        
        header_text = TranslationService.translate_from_dict("air_pollution_chart_items", "air_pollution_title", self._current_language)
        
        # Safe theme detection
        if self.page and hasattr(self.page, 'theme_mode'):
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        else:
            is_dark = False
        
        header = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.AIR_OUTLINED,  # Icona per la qualità dell'aria
                    color=ft.Colors.RED_400 if not is_dark else ft.Colors.RED_300,
                    size=24
                ),
                ft.Container(width=12),  # Spacer
                ft.Text(
                    f"{header_text}" " (μg/m3)",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color=self._current_text_color
                ),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.only(left=20, top=16, bottom=8)
        )
        
        # Cache the header and language
        self._cached_header = header
        self._header_language = self._current_language
        
        return header

    def update_location(self, lat: float, lon: float):
        """Allows updating the location and refreshing the air pollution chart data."""
        if self._lat != lat or self._lon != lon:
            self._lat = lat
            self._lon = lon
            if self.page:
                self.page.run_task(self.update_ui)
    
    def _safe_language_update(self, e=None):
        """Safely handle language change event."""
        if self.page and hasattr(self.page, 'run_task'):
            self.page.run_task(self.update_ui, e)
    
    def _safe_theme_update(self, e=None):
        """Safely handle theme change event."""
        if self.page and hasattr(self.page, 'run_task'):
            self.page.run_task(self.update_ui, e)