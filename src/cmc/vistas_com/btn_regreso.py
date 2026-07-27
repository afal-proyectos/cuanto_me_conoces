import flet as ft


class BotonRegreso(ft.ElevatedButton):
    def __init__(
        self,
        text: str,
        on_click=None,
        width: int = 220,
        height: int = 45,
    ):

        super().__init__(
            content=ft.Text(text),
            width=width,
            height=height,
            bgcolor=ft.Colors.BLUE,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
            ),
            on_click=on_click,
        )
