import logging
import flet as ft
               
from services.api.api_service import load_dotenv
from translations import translation_manager  # New modular translation system
from ui.components.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_language import DropdownLanguage
from ui.components.sidebar.popmenu.alertdialogs.settings.dropdowns.dropdown_measurement import DropdownMeasurement


class SettingsAlertDialog:
    """
    Versione semplificata per test dell'alert dialog delle impostazioni.
    Refactored: exposes only __init__, update_ui, build as public methods.
    """    
    def __init__(self, page, theme_handler, language, state_manager=None, handle_location_toggle=None, handle_theme_toggle=None):
        load_dotenv()
        self.page = page
        self.theme_handler = theme_handler
        self.language = language
        self.state_manager = state_manager
        self.handle_location_toggle_callback = handle_location_toggle
        self.handle_theme_toggle_callback = handle_theme_toggle

        self.language_dropdown = None
        self.measurement_dropdown = None
        self.theme_toggle_control = None
        self.dialog = None  # Initialize dialog attribute
        if self.state_manager:
            self.state_manager.register_observer("language_event", self.update_ui)
            self.state_manager.register_observer("theme_event", self.update_ui)

    def _init_dropdowns(self):
        # Usa la nuova architettura di colori
        colors = self._get_current_colors()
        # Converte il nuovo formato in quello legacy per i dropdown
        text_color = {
            "TEXT": colors["text"],
            "ACCENT": colors["accent"],
            "SECONDARY_TEXT": ft.Colors.with_opacity(0.6, colors["text"])
        }
        self.language_dropdown = DropdownLanguage(
            page=self.page,
            state_manager=self.state_manager,
            text_color=text_color,
            language=self.language,
        )
        self.measurement_dropdown = DropdownMeasurement(
            state_manager=self.state_manager,
            page=self.page, 
            text_color=text_color,
            language=self.language,
        )
        self.language_dropdown.register_child_observer(self.measurement_dropdown)
        self.language_dropdown.register_child_observer(self)

    def on_language_change(self, new_language_code):
        """Called when language changes from the dropdown."""
        logging.info(f"Settings dialog received language change notification: {new_language_code}")
        self.language = new_language_code
        
        # Update UI to reflect the language change using new architecture
        if self.dialog:
            self._update_dialog_theme_colors()

    def _get_current_colors(self):
        """Ottiene i colori del tema corrente usando la stessa logica del test funzionante."""
        is_dark = False
        
        # Determina se il tema è scuro
        if hasattr(self.page, 'theme_mode') and self.page.theme_mode is not None:
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        elif self.state_manager:
            theme_mode = self.state_manager.get_state('theme_mode')
            if theme_mode is not None:
                is_dark = theme_mode == 'dark'
        
        # Restituisce i colori come nel test funzionante
        if is_dark:
            return {
                "bg": "#161b22",
                "text": "#ffffff", 
                "accent": "#60a5fa"
            }
        else:
            return {
                "bg": "#ffffff",
                "text": "#000000",
                "accent": "#3b82f6"
            }

    def _update_dialog_theme_colors(self):
        """Aggiorna i colori del dialog usando la logica del test funzionante."""
        if not self.dialog:
            return
            
        colors = self._get_current_colors()
        
        logging.info(f"Aggiornamento colori dialog - BG: {colors['bg']}, Text: {colors['text']}")
        
        # AGGIORNA BACKGROUND DIALOG
        self.dialog.bgcolor = colors["bg"]
        
        # AGGIORNA BACKGROUND CONTENUTO
        if self.dialog.content:
            self.dialog.content.bgcolor = colors["bg"]
        
        # AGGIORNA TITOLO
        if hasattr(self.dialog, 'title') and isinstance(self.dialog.title, ft.Row):
            for control in self.dialog.title.controls:
                if isinstance(control, ft.Text):
                    control.color = colors["text"]
                elif isinstance(control, ft.Icon):
                    control.color = colors["accent"]
        
        # AGGIORNA CONTENUTO RICORSIVAMENTE
        if self.dialog.content and hasattr(self.dialog.content, 'content'):
            self._update_content_colors_recursive(self.dialog.content.content, colors)
        
        # AGGIORNA DROPDOWN CON NUOVA ARCHITETTURA
        if self.language_dropdown or self.measurement_dropdown:
            # Converte il nuovo formato in quello legacy per i dropdown
            text_color = {
                "TEXT": colors["text"],
                "ACCENT": colors["accent"],
                "SECONDARY_TEXT": ft.Colors.with_opacity(0.6, colors["text"])
            }
            is_dark = colors["bg"] == "#161b22"
            
            logging.info(f"🔄 Aggiornamento dropdown con tema: {('SCURO' if is_dark else 'CHIARO')}")
            
            if self.language_dropdown:
                try:
                    self.language_dropdown.update_text_sizes(text_color, self.language)
                    self.language_dropdown.update_theme_colors(text_color, is_dark)
                    logging.info("✅ Language dropdown aggiornato")
                except Exception as e:
                    logging.debug(f"Error updating language dropdown: {e}")
            
            if self.measurement_dropdown:
                try:
                    self.measurement_dropdown.update_text_sizes(text_color, self.language)
                    self.measurement_dropdown.update_theme_colors(text_color, is_dark)
                    logging.info("✅ Measurement dropdown aggiornato")
                except Exception as e:
                    logging.debug(f"Error updating measurement dropdown: {e}")
        
        # AGGIORNA PULSANTI DI AZIONE
        if hasattr(self.dialog, 'actions'):
            for action in self.dialog.actions:
                if isinstance(action, ft.TextButton):
                    action.style = ft.ButtonStyle(color=colors["accent"])
                elif isinstance(action, ft.ElevatedButton):
                    action.bgcolor = colors["accent"]
                elif isinstance(action, ft.FilledButton):
                    action.style = ft.ButtonStyle(
                        bgcolor=colors["accent"],
                        color="#FFFFFF"
                    )
        
        # FORZA UPDATE
        try:
            self.dialog.update()
            logging.info("✅ Dialog theme aggiornato con successo!")
        except Exception as ex:
            logging.error(f"❌ Errore update dialog theme: {ex}")

    def _update_content_colors_recursive(self, content, colors):
        """Aggiorna ricorsivamente tutti i controlli con i nuovi colori."""
        if isinstance(content, ft.Text):
            content.color = colors["text"]
        elif isinstance(content, ft.Icon):
            # Mantieni i colori fissi per le icone delle sezioni principali
            # Solo le icone del titolo e altre azioni usano colors["accent"]
            if hasattr(content, 'name'):
                # Colori fissi per le icone delle sezioni
                if content.name == ft.Icons.LANGUAGE:
                    content.color = "#ff6b35"  # Arancione per lingua
                elif content.name == ft.Icons.STRAIGHTEN:
                    content.color = "#22c55e"  # Verde per misure  
                elif content.name == ft.Icons.LOCATION_ON:
                    content.color = "#ef4444"  # Rosso per posizione
                elif content.name == ft.Icons.DARK_MODE:
                    content.color = "#8b5cf6"  # Viola per tema
                else:
                    # Per tutte le altre icone (titolo, pulsanti, ecc.)
                    content.color = colors["accent"]
            else:
                content.color = colors["accent"]
        elif isinstance(content, ft.Switch):
            content.active_color = colors["accent"]
            content.active_track_color = ft.Colors.with_opacity(0.5, colors["accent"])
        elif isinstance(content, ft.Divider):
            content.color = ft.Colors.with_opacity(0.3, colors["text"])
        elif isinstance(content, ft.Dropdown):
            # Aggiorna i dropdown con i nuovi colori
            is_dark = colors["bg"] == "#161b22"
            if is_dark:
                content.bgcolor = "#2d3748"
                content.border_color = "#4a5568" 
                content.focused_border_color = colors["accent"]
                content.color = colors["text"]
            else:
                content.bgcolor = "#ffffff"
                content.border_color = "#e2e8f0"
                content.focused_border_color = colors["accent"]
                content.color = colors["text"]
            
            # Update hint style
            secondary_color = ft.Colors.with_opacity(0.6, colors["text"])
            if content.hint_style:
                content.hint_style.color = secondary_color
            else:
                content.hint_style = ft.TextStyle(color=secondary_color)
            
            # Update label style if present
            if content.label_style:
                content.label_style.color = secondary_color
            else:
                content.label_style = ft.TextStyle(color=secondary_color)
        elif isinstance(content, ft.Container):
            if hasattr(content, 'content'):
                self._update_content_colors_recursive(content.content, colors)
            # Aggiorna background dei container se necessario
            if hasattr(content, 'bgcolor') and content.bgcolor:
                # Mantieni solo i container con background specifici
                if str(content.bgcolor).startswith("#") or "opacity" in str(content.bgcolor):
                    content.bgcolor = ft.Colors.with_opacity(0.1, colors["accent"])
        elif isinstance(content, (ft.ElevatedButton, ft.OutlinedButton)):
            # Aggiorna i pulsanti nel contenuto
            if "refresh" in str(content.text).lower():
                content.bgcolor = ft.Colors.with_opacity(0.1, colors["accent"])
                content.color = colors["accent"]
            elif "reset" in str(content.text).lower():
                content.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.ORANGE)
                content.color = ft.Colors.ORANGE_700
        elif hasattr(content, 'controls'):
            for child in content.controls:
                self._update_content_colors_recursive(child, colors)

    def update_ui(self, event_data=None):
        """Update UI based on current state with instant theme application usando la nuova architettura."""
        logging.debug(f"Settings dialog update_ui called with event_data: {event_data}")
        
        # Update language from state manager
        if self.state_manager:
            current_language = self.state_manager.get_state('language')
            if current_language and current_language != self.language:
                self.language = current_language
                logging.info(f"Settings dialog language updated to: {self.language}")
        
        # Force reinitialize dropdowns with new state
        self._init_dropdowns()
        
        # Update theme switch to reflect current theme usando i nuovi colori
        if self.theme_toggle_control:
            colors = self._get_current_colors()
            is_dark = colors["bg"] == "#161b22"  # Determina tema dall'background
            
            self.theme_toggle_control.value = is_dark
            self.theme_toggle_control.active_color = colors["accent"]
            self.theme_toggle_control.active_track_color = ft.Colors.with_opacity(0.5, colors["accent"])
            
            try:
                if hasattr(self.theme_toggle_control, 'page') and self.theme_toggle_control.page:
                    self.theme_toggle_control.update()
            except Exception:
                pass
        
        # Applica i nuovi colori del tema al dialog se esiste
        if self.dialog:
            self._update_dialog_theme_colors()
            
            # Force update if dialog is open
            if hasattr(self.dialog, 'open') and self.dialog.open:
                try:
                    if self.page:
                        self.page.update()
                except Exception as e:
                    logging.debug(f"Error updating page: {e}")
        
        logging.debug("Settings dialog update_ui completed")

    def build(self):
        self._init_dropdowns()
        return self.createAlertDialog(self.page)

    # --- Internal helpers and dialog logic remain private ---
    def createAlertDialog(self, page):
        # Usa la nuova architettura per i colori
        colors = self._get_current_colors()
        
        logging.info(f"Creazione dialog con colori: BG={colors['bg']}, Text={colors['text']}, Accent={colors['accent']}")

        language_dropdown_control = self.language_dropdown.build()
        measurement_dropdown_control = self.measurement_dropdown.build()

        self.dialog = ft.AlertDialog(

            modal=False,  # Cambiato da False a True per miglior visibilità
            title=ft.Row([
                ft.Icon(ft.Icons.SETTINGS, size=24, color=colors["accent"]),
                ft.Text(
                    translation_manager.get_translation("weather", "settings_alert_dialog_items", "settings_alert_dialog_title", self.language),
                    size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=colors["text"]
                ),
            ], spacing=2, expand=True),
            scrollable=True,
            bgcolor=colors["bg"],  # Usa il background del nuovo tema
            content=ft.Container(
                width=min(450, self.page.width * 0.9) if self.page else 400,
                bgcolor=colors["bg"],  # Assicura che anche il contenuto abbia il background corretto
                content=ft.Column(
                    controls=[
                        # Language settings section
                        ft.Row([
                            ft.Icon(ft.Icons.LANGUAGE, size=20, color="#ff6b35"),  # Arancione per lingua
                            ft.Text(
                                translation_manager.get_translation("weather", "settings_alert_dialog_items", "language", self.language), 
                                size=15, weight=ft.FontWeight.W_600, color=colors["text"]
                            ),
                            ft.Container(expand=True),
                            ft.Container(
                                content=language_dropdown_control,
                                width=120,  # Fixed smaller width
                            ),
                        ], spacing=10),
                        
                        # Unit measurement section
                        ft.Row([
                            ft.Icon(ft.Icons.STRAIGHTEN, size=20, color="#22c55e"),  # Verde per misure
                            ft.Text(
                                translation_manager.get_translation("weather", "settings_alert_dialog_items", "measurement", self.language), 
                                size=15, weight=ft.FontWeight.W_600, color=colors["text"]
                            ),
                            ft.Container(expand=True),
                            ft.Container(
                                content=measurement_dropdown_control,
                                width=120,  # Fixed smaller width
                            ),
                        ], spacing=10),
                        
                        # Location toggle section
                        ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON, size=20, color="#ef4444"),  # Rosso per posizione
                            ft.Text(
                                translation_manager.get_translation("weather", "settings_alert_dialog_items", "use_current_location", self.language), 
                                size=15, weight=ft.FontWeight.W_600, color=colors["text"]
                            ),
                            ft.Container(expand=True),
                            ft.Container(
                                content=self._create_location_button_instance(colors),
                                width=80,  # Fixed smaller width for button
                            ),
                        ], spacing=10),
                        
                        # Theme toggle section
                        ft.Row([
                            ft.Icon(ft.Icons.DARK_MODE, size=20, color="#8b5cf6"),  # Viola per tema
                            ft.Text(
                                translation_manager.get_translation("weather", "settings_alert_dialog_items", "dark_theme", self.language), 
                                size=15, weight=ft.FontWeight.W_600, color=colors["text"]
                            ),
                            ft.Container(expand=True),
                            ft.Container(
                                content=self._create_theme_toggle_instance(),
                                width=80,  # Fixed smaller width for toggle
                            ),
                        ], spacing=10),
                        
                    ],
                    spacing=24,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=ft.padding.all(16),
            ),
            actions=[                
                ft.FilledButton(
                    icon=ft.Icons.CLOSE,
                    text=translation_manager.get_translation("weather", "dialog_buttons", "close", self.language),
                    on_click=lambda e: self._close_dialog(e),
                    style=ft.ButtonStyle(
                        bgcolor=colors["accent"],
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=24, vertical=12)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            title_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=colors["text"]),
            content_text_style=ft.TextStyle(size=14, color=colors["text"]),
            inset_padding=ft.padding.all(20)
        )
        return self.dialog

    def _force_update_all_components(self):
        """Force update all dialog components."""
        if not self.dialog or not self.page:
            return
            
        try:
            logging.debug("Force updating all dialog components")
            
            # Update individual controls if dialog is open and connected
            if hasattr(self.page, 'dialog') and self.page.dialog == self.dialog and self.dialog.open:
                # Update dropdown controls
                if self.language_dropdown and hasattr(self.language_dropdown, 'dropdown'):
                    try:
                        self.language_dropdown.dropdown.update()
                    except Exception:
                        pass
                        
                if self.measurement_dropdown and hasattr(self.measurement_dropdown, 'dropdown'):
                    try:
                        self.measurement_dropdown.dropdown.update()
                    except Exception:
                        pass
                        
                # Update theme toggle control
                if self.theme_toggle_control:
                    try:
                        self.theme_toggle_control.update()
                    except Exception:
                        pass
                
                # Update all text controls recursively
                self._update_text_controls_recursive(self.dialog.content)
                
                # Update the dialog itself
                self.dialog.update()
                
        except Exception as e:
            logging.debug(f"Error in force update: {e}")

    def _update_text_controls_recursive(self, control):
        """Recursively update all text controls within a container."""
        if not control:
            return
            
        try:
            # Update if it's a text control
            if isinstance(control, ft.Text):
                control.update()
            elif isinstance(control, ft.Icon):
                control.update()
            elif isinstance(control, ft.Button):
                control.update()
            elif isinstance(control, ft.ElevatedButton):
                control.update()
            elif isinstance(control, ft.OutlinedButton):
                control.update()
            elif isinstance(control, ft.TextButton):
                control.update()
            elif isinstance(control, ft.Switch):
                control.update()
            elif isinstance(control, ft.Dropdown):
                control.update()
            
            # Recursively update child controls
            if hasattr(control, 'controls') and control.controls:
                for child in control.controls:
                    self._update_text_controls_recursive(child)
            elif hasattr(control, 'content') and control.content:
                self._update_text_controls_recursive(control.content)
                
        except Exception as e:
            logging.debug(f"Error updating control {type(control)}: {e}")

    def _get_translation(self, key, dict_key=None):
        if dict_key:
            return translation_manager.get_translation("weather", dict_key, key, self.language)
        # For simple translations, use weather module with a general section
        return translation_manager.get_translation("weather", "general", key, self.language)

    def _close_dialog(self, e=None):
        """Close the dialog when close button is clicked"""
        if self.dialog and hasattr(self.dialog, 'open'):
            self.dialog.open = False
            self.page.update()

    def open_dialog(self):
        """Apre l'alert dialog usando l'architettura funzionante del test."""
        if not self.page:
            logging.error("Error: Page context not available for SettingsAlertDialog.")
            return
            
        logging.info("Opening settings dialog con nuova architettura tema")
        
        # Build the dialog first
        dialog = self.build()
        
        # Apply immediate theme and language updates
        self.update_ui()
        
        # Usa page.open() come nel test funzionante
        self.page.open(dialog)
        
        logging.info("Settings dialog opened successfully usando page.open()")

    def close_dialog(self):
        """Closes the alert dialog."""
        if self.page and hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def _create_location_button_instance(self, colors):
        """Create location button with current state indication and theme awareness using new color system."""
        # Get current location state
        using_location = False
        if self.state_manager:
            using_location = self.state_manager.get_state('using_location') or False
        
        # Determine button style based on state and theme
        is_dark = colors["bg"] == "#161b22"
        
        if using_location:
            button_icon = ft.Icons.GPS_FIXED
            button_color = ft.Colors.GREEN_700 if not is_dark else ft.Colors.GREEN_400
            button_bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.GREEN)
        else:
            button_icon = ft.Icons.GPS_OFF
            button_color = ft.Colors.GREY_700 if not is_dark else ft.Colors.GREY_400
            button_bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.GREY)
        
        async def on_location_click(e):
            """Handle location button click."""
            try:
                new_state = not using_location
                if self.state_manager:
                    await self.state_manager.set_state('using_location', new_state)
                
                # Call the callback if provided
                if self.handle_location_toggle_callback:
                    # Create a mock event for compatibility
                    mock_event = type('MockEvent', (), {
                        'control': type('MockControl', (), {'value': new_state})()
                    })()
                    await self.handle_location_toggle_callback(mock_event)
                
                # Update the dialog to reflect the new state
                self.update_ui()
                
            except Exception as ex:
                logging.error(f"Error toggling location: {ex}")
        
        return ft.IconButton(
            icon=button_icon,
            on_click=on_location_click,
            bgcolor=button_bgcolor,
            #color=button_color,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                overlay_color=ft.Colors.with_opacity(0.1, button_color)
            ),
            width=140,
            height=36
        )

    def _create_theme_toggle_instance(self):
        """Create theme toggle switch con la nuova architettura tema."""
        colors = self._get_current_colors()
        is_dark = colors["bg"] == "#161b22"

        async def on_theme_toggle(e):
            logging.info(f"🔄 THEME TOGGLE: {'SCURO' if e.control.value else 'CHIARO'}")
            
            # Aggiorna immediatamente i colori del dialog usando la nuova architettura
            self._update_dialog_theme_colors()
            
            # Chiama il callback originale per aggiornare il tema globale
            if self.handle_theme_toggle_callback:
                if hasattr(self.page, 'run_task'):
                    self.page.run_task(self.handle_theme_toggle_callback, e)
                else:
                    await self.handle_theme_toggle_callback(e)

        if self.theme_toggle_control is None:
            self.theme_toggle_control = ft.Switch(
                value=is_dark,
                on_change=on_theme_toggle,
                active_color=colors["accent"],
                active_track_color=ft.Colors.with_opacity(0.5, colors["accent"]),
                inactive_thumb_color="#cccccc" if not is_dark else "#666666",
                inactive_track_color="#eeeeee" if not is_dark else "#333333",
            )
        else:
            # Update existing switch con nuovi colori
            self.theme_toggle_control.value = is_dark
            self.theme_toggle_control.active_color = colors["accent"]
            self.theme_toggle_control.active_track_color = ft.Colors.with_opacity(0.5, colors["accent"])
            self.theme_toggle_control.inactive_thumb_color = "#cccccc" if not is_dark else "#666666"
            self.theme_toggle_control.inactive_track_color = "#eeeeee" if not is_dark else "#333333"
            
        return self.theme_toggle_control

    def _get_translation_local(self, key):
        """Get translation using the new modular translation system."""
        try:
            return translation_manager.get_translation("weather", "settings_dialog", key, self.language)
        except Exception as e:
            logging.warning(f"Translation error for key '{key}': {e}")
            return key

    def cleanup(self):
        if self.state_manager:
            self.state_manager.unregister_observer("language_event", self.update_ui)
            self.state_manager.unregister_observer("theme_event", self.update_ui)
