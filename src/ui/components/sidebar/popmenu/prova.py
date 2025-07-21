import flet as ft


def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0

    bg_container = ft.Ref[ft.Container]()

    def handle_color_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    def handle_alignment_click(e):
        print("in handle alignment click method")
        print(
            f"bg_container.alignment: {bg_container.alignment}, bg_container.content: {bg_container.content}"
        )
        bg_container.current.alignment = e.control.data
        # page.update()
        # bg_container.alignment = e.control.data
        print(
            f"e.control.content.value: {e.control.content.value}, e.control.data: {e.control.data}"
        )
        page.update()

    def handle_on_hover(e):
        print(f"{e.control.content.value}.on_hover")

    bg_container = ft.Container(
        # ref=bg_container,
        expand=True,
        bgcolor=ft.Colors.SURFACE,
        content=ft.Text(
            "Choose a bgcolor from the menu",
            style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD),
        ),
        alignment=ft.alignment.center,
    )
    
    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.MENU, color=ft.Colors.ON_SURFACE),
                    ]
                ),
                controls=[
                    ft.SubmenuButton(
                        content=ft.Text("Meteo"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        controls=[
                        ],
                    ),
                    ft.SubmenuButton(
                        content=ft.Text("Mappe"),
                        leading=ft.Icon(ft.Icons.COLORIZE),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Mappe Avanzate"),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}
                                ),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Mappe Interattive"),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}
                                ),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            ),
                        ],
                    ),
                    ft.SubmenuButton(
                        content=ft.Text("Analisi"),
                        leading=ft.Icon(ft.Icons.LOCATION_PIN),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Tendenze Meteo"),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}
                                ),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Dati storici"),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}
                                ),
                                on_click=handle_color_click,
                                on_hover=handle_on_hover,
                            ),
                        ],
                    ),
                ],
            )
        ],
    )

    page.add(
        ft.Row([menubar]),
        ft.Container(
            ref=bg_container,
            expand=True,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Text(
                "Choose a bgcolor from the menu",
                style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD),
            ),
            alignment=ft.alignment.center,
        ),
    )


ft.app(main)