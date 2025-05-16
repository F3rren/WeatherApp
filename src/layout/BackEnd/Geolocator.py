import flet as ft

async def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.appbar = ft.AppBar(title=ft.Text("Geolocator Test"))

    # Etichette da aggiornare
    lat_text = ft.Text()
    lon_text = ft.Text()

    def handle_position_change(e):
        lat_text.value = f"Latitude: {e.latitude}"
        lon_text.value = f"Longitude: {e.longitude}"
        lat_text.update()
        lon_text.update()

    gl = ft.Geolocator(
        location_settings=ft.GeolocatorSettings(
            accuracy=ft.GeolocatorPositionAccuracy.LOW
        ),
        on_position_change=handle_position_change,
        on_error=lambda e: page.add(ft.Text(f"Error: {e.data}")),
    )

    page.overlay.append(gl)

    async def handle_get_current_position(e):
        p = await gl.get_current_position_async()
        lat_text.value = f"Latitude: {p.latitude}"
        lon_text.value = f"Longitude: {p.longitude}"
        page.update()

    page.add(
        ft.Column([
            ft.Row([
                ft.OutlinedButton("Get Current Position", on_click=handle_get_current_position),
            ]),
            lat_text,
            lon_text,
        ])
    )
