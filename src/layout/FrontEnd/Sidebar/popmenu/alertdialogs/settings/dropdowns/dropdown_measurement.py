# filepath: c:\Users\Utente\Desktop\Progetti\Python\MeteoApp\src\layout\frontend\sidebar\popmenu\alertdialogs\settings\dropdowns\dropdown_measurement.py
import flet as ft
from config import MEASUREMENT_UNITS

class DropdownMeasurement:

    def __init__(self, state_manager=None):
        self.selected_unit = None
        self.state_manager = state_manager
        # Sistemi di misura disponibili
        self.units = [unit["name"] for unit in MEASUREMENT_UNITS]
        self.unit_labels = {unit["name"]: unit["name"] for unit in MEASUREMENT_UNITS}

    def get_options(self):
        options = []
        for unit in self.units:
            options.append(
                ft.DropdownOption(
                    key=unit,
                    content=ft.Text(
                        value=self.unit_labels[unit],
                    ),
                )
            )
        return options
    
    def createDropdown(self):
        
        def dropdown_changed(e):
            self.set_unit(e.control.value)
            print(f"Unit set to: {e.control.value}")
            # Aggiornato solo se il parent è stato impostato
            if hasattr(self, 'parent') and self.parent:
                self.parent.update()

        # Ottieni il valore corrente dell'unità di misura dallo state manager, se disponibile
        current_unit = "metric"  # Valore predefinito
        if self.state_manager:
            current_unit = self.state_manager.get_state('unit') or "metric"
            self.selected_unit = current_unit

        return ft.Dropdown(
            autofocus=True,
            label="Measurement Unit",
            hint_text="Select measurement system",
            options=self.get_options(),
            on_change=dropdown_changed,
            expand=True,  # Usa tutto lo spazio disponibile
            value=current_unit,
            # text_size rimosso poiché non supportato in Flet 0.28.2
            border_width=2,
            border_color=ft.Colors.GREY_400,
            focused_border_color=ft.Colors.BLUE,
            focused_border_width=2,
            content_padding=ft.padding.all(8)
        )

    def set_unit(self, unit):
        self.selected_unit = unit
        
        # Aggiorna lo stato dell'applicazione se state_manager è disponibile
        if self.state_manager:
            import asyncio
            
            # Funzione wrapper per gestire chiamate asincrone in modo sicuro
            def call_async_safely(coro):
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                if not loop.is_running():
                    return loop.run_until_complete(coro)
                else:
                    return asyncio.create_task(coro)
            
            # Aggiorna lo stato con la nuova unità di misura
            call_async_safely(self.state_manager.set_state("unit", unit))
            
        print(f"Unit set to: {self.selected_unit}")

    def get_selected_unit(self):
        return self.selected_unit

    def build(self):
        return self.createDropdown()
