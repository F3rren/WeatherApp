import flet as ft
from theme_handler import ThemeHandler

def main(page: ft.Page):
    theme_handler = ThemeHandler(page)
    page.theme_mode = ft.ThemeMode.LIGHT

    # Questi controlli verranno aggiornati al cambio tema
    text_main = ft.Text("Testo principale", color=theme_handler.get_color("TEXT"))
    text_secondary = ft.Text("Testo secondario", color=theme_handler.get_color("SECONDARY_TEXT"))

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        # Aggiorna i colori dei testi
        text_main.color = theme_handler.get_color("TEXT")
        text_secondary.color = theme_handler.get_color("SECONDARY_TEXT")
        page.update()

    col = ft.Column([
        text_main,
        text_secondary,
        ft.ElevatedButton("Cambia tema", on_click=toggle_theme)
    ])
    page.add(col)


if __name__ == "__main__":
    ft.app(target=main)
