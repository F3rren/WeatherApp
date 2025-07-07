import logging
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
        windy_url = f"https://embed.windy.com/embed2.html?lat={self.latitude}&lon={self.longitude}&zoom=16&overlay=temp"
        return ft.WebView(
                url=windy_url,
                on_page_started=lambda _: logging.info("Page started"),
                on_page_ended=lambda _: logging.info("Page ended"),
                on_web_resource_error=lambda e: logging.error("Page error:", e.data),
                expand=True,
            )

    def _open_fullscreen_map_fallback(self, e=None):
        """Apre la mappa a schermo intero nel browser (usato solo nel fallback)."""
        fullscreen_url = f"https://www.windy.com/?{self.latitude},{self.longitude},8"
        webbrowser.open(fullscreen_url)
