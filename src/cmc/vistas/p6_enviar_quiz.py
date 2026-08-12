import flet as ft


class Enviar(ft.AlertDialog):
    def __init__(
        self,
        advertencia="",
        on_save=None,
        on_cancel=None,
    ):
        super().__init__(
            modal=True,
        )

        self.on_save = on_save
        self.on_cancel = on_cancel

        self._create_controls()

        self.title = ft.Text(advertencia)
        self.content = self._build_content()

    def _create_controls(self):

        self.advertencia = ft.Text("¿Estás Seguro de enviar el quizz?")

        self.btn_save = ft.Button(
            "Enviar",
            expand=True,
            on_click=self._on_save_click,
        )

        self.btn_cancel = ft.Button(
            "Seguir Editando",
            expand=True,
            on_click=self._on_cancel_click,
        )

    # =====================================================
    # Layout
    # =====================================================

    def _build_content(self):

        return ft.Column(
            tight=True,
            width=400,
            controls=[
                self.advertencia,
                ft.Divider(),
                ft.Row(controls=[self.btn_cancel, self.btn_save]),
            ],
        )

    # =====================================================
    # Eventos
    # =====================================================

    def _on_save_click(self, e):

        if self.on_save:
            self.on_save()

    def _on_cancel_click(self, e):

        if self.on_cancel:
            self.on_cancel()


if __name__ == "__main__":

    def main(page: ft.Page):
        page.title = "Prueba Enviar"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def cerrar_dialogo(e=None):
            page.pop_dialog()
            page.update()

        # Instanciamos el diálogo
        dlg = Enviar(
            advertencia="¡Atención!",
            on_save=lambda: print("guardar datos"),
            on_cancel=cerrar_dialogo,
        )

        # Botón para mostrar el diálogo
        btn_abrir = ft.Button(
            "Configurar Opciones",
            on_click=lambda _: page.show_dialog(dlg),
        )

        page.add(
            ft.Text("Haz clic para ver el diálogo de opciones", size=20), btn_abrir
        )

    ft.run(main)
