import flet as ft

from servicios.bd_local_ser import BDLocal


class SeleccionQuizView(ft.View):
    def __init__(self, on_continuar=None, on_volver=None):

        self.on_continuar = on_continuar
        self.on_volver = on_volver

        self._crear_controles()
        self._crear_vista()

    def _crear_controles(
        self,
    ):
        self.titulo = ft.Text(
            "Elije un Quiz para terminarlo",
            size=18,
            expand=True,
            weight=ft.FontWeight.BOLD,
        )
        self.lista_quiz = ft.Column(controls=self.crear_tarjetas())

        self.btn_crear_nuevo_quiz = ft.Button(
            "Crear nuevo Quiz",
            height=50,
            expand=True,
            bgcolor=ft.Colors.RED,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=2)
            ),
            on_click=self._on_crear_quiz,
        )
        self.btn_volver = ft.Button(
            "Regresar",
            bgcolor=ft.Colors.RED,
            expand=True,
            on_click=self._on_volver,
            style=ft.ButtonStyle(color=ft.Colors.WHITE),
        )

    def _crear_vista(self):
        super().__init__(
            route="/quiz",
            controls=[
                ft.Container(
                    expand=True,
                    padding=2,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Divider(),
                            self.btn_crear_nuevo_quiz,
                            ft.Divider(),
                            self.titulo,
                            self.lista_quiz,
                            self.btn_volver,
                        ],
                    ),
                )
            ],
        )

    def crear_tarjetas(self):
        bdl = BDLocal()
        lista = bdl.mostrar_quiz_local()

        return [
            ft.Row(
                # alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Card(
                        expand=True,
                        content=ft.Container(
                            width=400,
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        bgcolor=ft.Colors.BLACK,
                                        title=ft.Text(
                                            item["nombre_evento"],
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        subtitle=ft.Text(
                                            f"Para: {item['nombre_creador']}\n{item['comentario']}\n{item['cantidad_preguntas']} preguntas."
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ),
                    ft.Button(
                        "Edit",
                        # expand_loose=True,
                        data=id,
                        on_click=self._on_editar_quiz,
                    ),
                ],
            )
            for id, item in lista.items()
        ]

    def _on_editar_quiz(self, e):
        id = e.control.data
        print("id: ", id)
        if self.on_continuar:
            self._on_continuar(id)

    def _on_volver(self, e):
        print("volver")
        if self.on_volver:
            self.on_volver()

    def _on_crear_quiz(self):
        print("abrir ventana de creador")


if __name__ == "__main__":

    def main(page: ft.Page):
        page.title = "Prueba QuestionSelectorView"
        ventana = SeleccionQuizView()
        page.views.append(ventana)
        page.update()

    ft.run(main)
