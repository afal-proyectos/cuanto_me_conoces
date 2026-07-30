import flet as ft

n = "Alejandro"


def main(page: ft.Page):
    page.title = "Card Example"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.START,
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Card(
                    expand=True,
                    content=ft.Container(
                        width=400,
                        expand=True,
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    bgcolor=ft.Colors.BLUE_50,
                                    title=ft.Text(
                                        "Título de la tarjeta",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    subtitle=ft.Text(
                                        f"Este es un texto descriptivo dentro del card.\nHola: {n}"
                                    ),
                                ),
                            ],
                        ),
                    ),
                ),
                ft.ElevatedButton(
                    "Aceptar",
                    # align=ft.MainAxisAlignment.,
                    on_click=lambda e: print("Botón presionado"),
                ),
            ],
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.START,
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Card(
                    expand=True,
                    content=ft.Container(
                        width=400,
                        expand=True,
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    bgcolor=ft.Colors.BLUE_50,
                                    title=ft.Text(
                                        "Título de la tarjeta",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    subtitle=ft.Text(
                                        f"Este es un texto descriptivo dentro del card.\nHola: {n}"
                                    ),
                                ),
                            ],
                        ),
                    ),
                ),
                ft.ElevatedButton(
                    "Edit",
                    expand_loose=True,
                    on_click=lambda e: print("Botón presionado"),
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
