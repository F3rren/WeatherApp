import flet as ft

def create_location_settings_dialog(handler):
    return ft.AlertDialog(
        adaptive=True,
        title=ft.Text("Opening Location Settings..."),
        content=ft.Text(
            "You are about to be redirected to the location/app settings. "
            "Please locate this app and grant it location permissions."
        ),
        actions=[ft.TextButton(text="Take me there", on_click=handler)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

def create_app_settings_dialog(handler):
    return ft.AlertDialog(
        adaptive=True,
        title=ft.Text("Opening App Settings..."),
        content=ft.Text(
            "You are about to be redirected to the app settings. "
            "Please locate this app and grant it location permissions."
        ),
        actions=[ft.TextButton(text="Take me there", on_click=handler)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
