import flet as ft
from layout.frontend.layout_manager_fixed import LayoutManager
import time

def test_layout(page: ft.Page):
    # Inizializza il layout manager
    manager = LayoutManager(page)
    
    # Crea container semplici per test con testi descrittivi
    sidebar = ft.Container(
        ft.Text("Sidebar", size=20, weight="bold", color="white"),
        alignment=ft.alignment.center, 
        bgcolor="red",
        padding=20
    )
    
    info = ft.Container(
        ft.Text("Info Section", size=20, weight="bold", color="white"),
        alignment=ft.alignment.center, 
        bgcolor="blue",
        padding=20
    )
    
    weekly = ft.Container(
        ft.Text("Weekly Weather", size=20, weight="bold", color="white"),
        alignment=ft.alignment.center, 
        bgcolor="green",
        padding=20
    )
    
    air_pollution = ft.Container(
        ft.Text("Air Pollution Info", size=20, weight="bold", color="white"),
        alignment=ft.alignment.center, 
        bgcolor="yellow",
        padding=20
    )
    
    chart = ft.Container(
        ft.Text("Temperature Chart", size=20, weight="bold", color="white"),
        alignment=ft.alignment.center, 
        bgcolor="purple",
        padding=20
    )
    
    air_pollution_chart = ft.Container(
        ft.Text("Air Pollution Chart", size=20, weight="bold", color="white"),
        alignment=ft.alignment.center, 
        bgcolor="orange",
        padding=20
    )
    
    # Crea i container nel layout manager
    manager.create_containers(
        sidebar_content=sidebar,
        info_content=info,
        weekly_content=weekly,
        chart_content=chart,
        air_pollution_chart_content=air_pollution_chart,
        air_pollution_content=air_pollution
    )
    
    # Costruisci il layout
    layout = manager.build_layout()
    page.add(layout)
    
    # Debug prima della modifica
    manager.debug_column_sizes()
    
    # Aggiungi un pulsante per cambiare layout
    def change_layout(e):
        # Modifica le dimensioni delle colonne
        manager.update_column_sizes({
            'weekly': {"xs": 6, "md": 6, "lg": 6},
            'air_pollution': {"xs": 6, "md": 6, "lg": 6},
            'chart': {"xs": 6, "md": 6, "lg": 6},
            'air_pollution_chart': {"xs": 6, "md": 6, "lg": 6}
        })
        
        # Forza l'aggiornamento completo del layout
        manager.force_layout_update()
        
        # Debug dopo la modifica
        manager.debug_column_sizes()
    
    # Aggiungi pulsante in fondo alla pagina
    button = ft.ElevatedButton("Cambia Layout", on_click=change_layout)
    page.add(button)
    page.update()

# Avvia l'applicazione
ft.app(target=test_layout)
