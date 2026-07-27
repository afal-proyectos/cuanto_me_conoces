import flet as ft


class PreguntaItem(ft.ListTile):
    def __init__(
        self,
        text,
        on_click=None,
    ):

        super().__init__(
            title=ft.Text(text),
            on_click=on_click,
        )
