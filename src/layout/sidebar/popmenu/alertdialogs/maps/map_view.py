import flet as ft
import webbrowser

class MapView:
    """
    A view component to display a map using WebView or a fallback button.
    """
    def __init__(self, page: ft.Page, lat: float = None, lon: float = None):
        super().__init__()
        self.page = page
        self.latitude = lat
        self.longitude = lon

    def build(self):
        windy_url = f"https://embed.windy.com/embed2.html?lat={self.latitude}&lon={self.longitude}&zoom=8&overlay=temp"
        return ft.WebView(
                url=windy_url,
                on_page_started=lambda _: print("Page started"),
                on_page_ended=lambda _: print("Page ended"),
                on_web_resource_error=lambda e: print("Page error:", e.data),
                expand=True,
            )

        try:
            # Prova a creare il componente WebView
            pass
        except Exception:
            # Fallback se WebView non è disponibile
            return ft.Column([
                ft.Text("Il componente mappa (WebView) non è supportato su questa piattaforma.", text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton(
                    text="Apri Mappa nel Browser",
                    on_click=self._open_fullscreen_map_fallback,
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            )

    def _open_fullscreen_map_fallback(self, e=None):
        """Apre la mappa a schermo intero nel browser (usato solo nel fallback)."""
        fullscreen_url = f"https://www.windy.com/?{self.latitude},{self.longitude},8"
        webbrowser.open(fullscreen_url)
