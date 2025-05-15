import flet as ft

def create_geolocator(page, on_position_change, on_error):
    gl = ft.Geolocator(
        location_settings=ft.GeolocatorSettings(
            accuracy=ft.GeolocatorPositionAccuracy.LOW
        ),
        on_position_change=on_position_change,
        on_error=on_error,
    )
    page.overlay.append(gl)
    return gl
