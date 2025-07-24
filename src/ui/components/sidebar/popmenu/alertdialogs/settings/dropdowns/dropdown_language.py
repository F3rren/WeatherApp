import os
from dotenv import load_dotenv
import flet as ft
import logging

from utils.translations_data import LANGUAGES 
from translations import translation_manager  # New modular translation system
from ui.themes.themes import DARK_THEME, LIGHT_THEME

class DropdownLanguage:
    
    def __init__(self, page: ft.Page, state_manager, text_color: dict, language: str):
        load_dotenv()
        self.page = page
        self.state_manager = state_manager
        self.text_color = text_color
        self.current_language_display = language # For potential future use if this component had its own translatable text
        
        self.selected_language = None # This will be set from state_manager or during selection
        self.dropdown = None

        # --- Observer pattern ---
        self.child_observers = []  # List of child components to notify
        if self.state_manager:
            self.state_manager.register_observer("language_event", self._handle_language_event)

    def register_child_observer(self, observer):
        if observer not in self.child_observers:
            self.child_observers.append(observer)

    def unregister_child_observer(self, observer):
        if observer in self.child_observers:
            self.child_observers.remove(observer)

    def notify_child_observers(self, new_language_code):
        for observer in self.child_observers:
            if hasattr(observer, "on_language_change"):
                observer.on_language_change(new_language_code)

    def _handle_language_event(self, event_data=None):
        """Called when language_event is received from state_manager"""
        new_language_code = None
        if event_data and isinstance(event_data, dict):
            new_language_code = event_data.get("language", None)
        elif self.state_manager:
            new_language_code = self.state_manager.get_state('language')
            
        if new_language_code and new_language_code != self.selected_language:
            logging.info(f"Language dropdown handling language event: {new_language_code}")
            self.selected_language = new_language_code
            self.current_language_display = new_language_code
            
            # Update dropdown value if it exists
            if self.dropdown and self.dropdown.value != new_language_code:
                self.dropdown.value = new_language_code
                try:
                    if self.dropdown.page:
                        self.dropdown.update()
                except Exception as e:
                    logging.debug(f"Error updating dropdown value: {e}")
            
            # Notify child observers
            self.notify_child_observers(new_language_code)

    def update_text_sizes(self, text_color: dict, language: str):
        """Update text sizes and colors for the dropdown."""
        self.text_color = text_color
        self.current_language_display = language
        
        # Update selected language from state manager if available
        if self.state_manager:
            current_state_language = self.state_manager.get_state('language')
            if current_state_language:
                self.selected_language = current_state_language
                self.current_language_display = current_state_language

        if self.dropdown:
            # Update hint text with current language
            translated_hint_text = translation_manager.get_translation("weather", "settings_alert_dialog_items", "language", self.current_language_display)
            self.dropdown.hint_text = translated_hint_text
            
            # Update dropdown value to match current language
            if self.selected_language and self.dropdown.value != self.selected_language:
                self.dropdown.value = self.selected_language
            
            # Safe access to text_color properties
            if isinstance(self.text_color, dict) and 'dropdown_text' in self.text_color:
                self.dropdown.text_size = self.text_color['dropdown_text']
            else:
                self.dropdown.text_size = 14  # Default size
                
            if isinstance(self.text_color, dict):
                self.dropdown.color = self.text_color.get("TEXT", ft.Colors.BLACK)
                self.dropdown.border_color = self.text_color.get("BORDER", ft.Colors.GREY)
                self.dropdown.focused_border_color = self.text_color.get("ACCENT", ft.Colors.BLUE)
                self.dropdown.bgcolor = self.text_color.get("CARD_BACKGROUND", ft.Colors.WHITE)
            else:
                # Fallback if text_color is not a dict
                self.dropdown.color = ft.Colors.BLACK
                self.dropdown.border_color = ft.Colors.GREY
                self.dropdown.focused_border_color = ft.Colors.BLUE
                self.dropdown.bgcolor = ft.Colors.WHITE

            if self.dropdown.hint_style:
                secondary_color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color.get("TEXT", ft.Colors.BLACK))) if isinstance(self.text_color, dict) else ft.Colors.GREY
                self.dropdown.hint_style.color = secondary_color
            else:
                secondary_color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color.get("TEXT", ft.Colors.BLACK))) if isinstance(self.text_color, dict) else ft.Colors.GREY
                self.dropdown.hint_style = ft.TextStyle(color=secondary_color)
            
            if self.dropdown.label_style: # Though label is not used in current createDropdown
                secondary_color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color.get("TEXT", ft.Colors.BLACK))) if isinstance(self.text_color, dict) else ft.Colors.GREY
                self.dropdown.label_style.color = secondary_color
            else: # Though label is not used
                secondary_color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color.get("TEXT", ft.Colors.BLACK))) if isinstance(self.text_color, dict) else ft.Colors.GREY
                self.dropdown.label_style = ft.TextStyle(color=secondary_color)

            # Options might need re-styling if their text color is static; however, ft.Text defaults to inheriting.
            # If options had complex styling that doesn't inherit, they'd need updating here.
            # For now, assume ft.Text within options inherits color or is handled by Flet's theme propagation.

            try:
                if self.dropdown.page:
                    self.dropdown.update()
                    if self.page:
                        self.page.update()
            except Exception as e:
                logging.debug(f"Error updating dropdown: {e}")
    
    def update_theme_colors(self, text_color: dict, is_dark: bool):
        """Update dropdown colors based on current theme."""
        self.text_color = text_color
        
        if self.dropdown:
            # Update dropdown background and border colors based on theme
            if is_dark:
                self.dropdown.bgcolor = "#2d3748"
                self.dropdown.border_color = "#4a5568" 
                self.dropdown.focused_border_color = text_color.get("ACCENT", "#3b82f6")
                self.dropdown.color = text_color.get("TEXT", "#ffffff")
            else:
                self.dropdown.bgcolor = "#ffffff"
                self.dropdown.border_color = "#e2e8f0"
                self.dropdown.focused_border_color = text_color.get("ACCENT", "#0078d4")
                self.dropdown.color = text_color.get("TEXT", "#000000")
                
            # Update hint style
            secondary_color = ft.Colors.with_opacity(0.6, text_color.get("TEXT", "#000000"))
            if self.dropdown.hint_style:
                self.dropdown.hint_style.color = secondary_color
            else:
                self.dropdown.hint_style = ft.TextStyle(color=secondary_color)
                
            try:
                if self.dropdown.page:
                    self.dropdown.update()
            except Exception as e:
                logging.debug(f"Error updating dropdown theme: {e}")

    def get_language_name_by_code(self, code):
        """Restituisce il nome della lingua dato il codice"""
        for language_item in LANGUAGES:
            if language_item["code"] == code:
                return language_item["name"]
        return "English"  # Default


    def get_options(self):
        options = []
        
        # Usa un percorso assoluto rispetto alla cartella assets dell'applicazione
        # Flet cerca le risorse nella cartella assets specificata nell'ft.app() in main.py
        base_path = "/flags/"
        
        for lang in LANGUAGES:
            code = lang["code"]
            name = lang["name"]
            flag = lang.get("flag", "")
            
            # Crea l'opzione con un'immagine per la bandiera e il nome della lingua
            option_content = ft.Row(
                controls=[],  # Inizia con una lista vuota
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            
            # Aggiungi l'immagine della bandiera, se disponibile
            if flag:
                try:
                    flag_path = f"{base_path}{flag}"
                    flag_image = ft.Image(
                        src=flag_path,
                        width=24,
                        height=16,
                        fit=ft.ImageFit.CONTAIN,
                    )
                    option_content.controls.append(flag_image)
                except Exception as e:
                    logging.error(f"Error loading flag for {code}: {e}")
                    # Aggiungi un placeholder se l'immagine non può essere caricata
                    option_content.controls.append(ft.Container(width=24, height=16))
            else:
                # Aggiungi un placeholder se non è specificata alcuna bandiera
                option_content.controls.append(ft.Container(width=24, height=16))
            
            # Aggiungi il testo del nome della lingua
            # Ensure text color for options is also dynamic if needed, though ft.Text usually inherits.
            # If not, explicitly set color: self.text_color["TEXT"]
            option_content.controls.append(ft.Text(name)) # Potentially: ft.Text(name, color=self.text_color["TEXT"])
            
            # Aggiungi l'opzione al dropdown
            options.append(
                ft.dropdown.Option(
                    key=code,
                    text=name,
                    content=option_content,
                )
            )
        
        return options

    def createDropdown(self):
        # Always set self.text_color based on current theme
        if self.page and hasattr(self.page, 'theme_mode'):
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            self.text_color = DARK_THEME if is_dark else LIGHT_THEME
        elif isinstance(self.text_color, str):
            if self.text_color.lower() in ("#fff", "#ffffff", "white"):
                self.text_color = LIGHT_THEME
            else:
                self.text_color = DARK_THEME

        def dropdown_changed(e):
            # Get the language code directly from the selection
            selected_code = e.control.value
            
            # Use the same pattern as weather_alert_dialog for consistency
            if self.state_manager and selected_code:
                import asyncio
                # Use page.run_task if available for better async handling
                if hasattr(self.page, 'run_task'):
                    # First update the state
                    self.page.run_task(self.state_manager.set_state, "language", selected_code)
                    # Then trigger the language_event to update the weather data
                    self.page.run_task(self.state_manager.notify_all, "language_event", {"language": selected_code})
                else:
                    # Fallback for older versions
                    asyncio.create_task(self.state_manager.set_state("language", selected_code))
                    asyncio.create_task(self.state_manager.notify_all("language_event", {"language": selected_code}))
                
                logging.info(f'Language updated via state manager and event triggered: {selected_code}')
            
            # Update local state
            self.set_language(selected_code)
            
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        # Ottieni il valore corrente della lingua dallo state manager, se disponibile
        current_language_code = os.getenv("DEFAULT_LANGUAGE")  # Valore predefinito
        if self.state_manager:
            current_language_code = self.state_manager.get_state('language') or os.getenv("DEFAULT_LANGUAGE")
            self.selected_language = current_language_code
            logging.info(f'Lingua corrente dallo state manager: {current_language_code}')

        
        translated_hint_text = translation_manager.get_translation("units", "unit_items", "language", self.current_language_display)
        self.dropdown = ft.Dropdown(
            hint_text=translated_hint_text,
            options=self.get_options(),
            on_change=dropdown_changed,
            width=120, 
            value=current_language_code,
            border_width=2,
            border_color=self.text_color["BORDER"],
            focused_border_color=self.text_color["ACCENT"],
            focused_border_width=2,
            bgcolor=self.text_color["CARD_BACKGROUND"],
            color=self.text_color["TEXT"],
            content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
            hint_style=ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
        )
        
        return self.dropdown # Return the created dropdown

    def get_language_code_by_name(self, name):
        """Restituisce il codice lingua dato il nome"""
        for language_item in LANGUAGES:
            if language_item["name"] == name:
                return language_item["code"]
        return "en"  # Default

    def set_language(self, language_code): # Renamed parameter for clarity
        """Set the selected language and update local state."""
        self.selected_language = language_code
        
        # Update the dropdown value if it exists and is different
        if self.dropdown and self.dropdown.value != language_code:
            self.dropdown.value = language_code
            if self.dropdown.page:
                self.dropdown.update()
        
        # Notify child observers
        self.notify_child_observers(language_code)
        
        logging.info(f'Language set successfully: {self.selected_language} - {self.get_language_name_by_code(self.selected_language)}')

    def handle_theme_change(self, event_data=None): # This method might be deprecated by direct calls to update_text_sizes
        """Handle theme change events by updating the dropdown appearance using stored text_color."""
        if self.dropdown:
            # The actual theme (dark/light) determination is now external,
            # self.text_color should be updated by the parent.
            # This method just re-applies the current self.text_color.
            self.dropdown.border_color = self.text_color.get("BORDER", ft.Colors.BLACK)
            self.dropdown.focused_border_color = self.text_color.get("ACCENT", ft.Colors.BLUE)
            self.dropdown.bgcolor = self.text_color.get("CARD_BACKGROUND", ft.Colors.WHITE)
            self.dropdown.color = self.text_color.get("TEXT", ft.Colors.BLACK)
            
            if self.dropdown.hint_style:
                self.dropdown.hint_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else:
                self.dropdown.hint_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))

            if self.dropdown.label_style: # Though label is not used
                self.dropdown.label_style.color = self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"]))
            else: # Though label is not used
                self.dropdown.label_style = ft.TextStyle(color=self.text_color.get("SECONDARY_TEXT", ft.Colors.with_opacity(0.5, self.text_color["TEXT"])))
            
            self.dropdown.update()
            
    def build(self):
        if not self.dropdown: # Create dropdown only if it doesn't exist
            self.dropdown = self.createDropdown()
        return self.dropdown
