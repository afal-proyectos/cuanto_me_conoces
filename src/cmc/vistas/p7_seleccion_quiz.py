import flet as ft


class SeleccionQuizView(ft.View):
    def __init__(
        self,
        dict_quiz=None,
        on_nuevo=None,
        on_volver=None,
        on_editar=None,
    ):

        self.on_nuevo = on_nuevo
        self.on_volver = on_volver
        self.on_editar = on_editar
        self.dict_quiz = dict_quiz

        self._crear_controles()
        self._crear_vista()

    def _crear_controles(
        self,
    ):
        self.titulo = ft.Text(
            "Elije un Quiz para terminarlo",
            size=18,
            # expand=True,
            weight=ft.FontWeight.BOLD,
        )
        self.lista_quiz = ft.Column(controls=self.crear_tarjetas())

        self.btn_crear_nuevo_quiz = ft.Button(
            "Crear nuevo Quiz",
            height=50,
            # expand=True,
            bgcolor=ft.Colors.RED,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=2)
            ),
            on_click=self._on_nuevo,
        )
        self.btn_volver = ft.Button(
            "Regresar",
            bgcolor=ft.Colors.RED,
            # expand=True,
            on_click=self._on_volver,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
            ),
        )

    def _crear_vista(self):
        super().__init__(
            route="/quiz",
            controls=[
                ft.Container(
                    expand=True,
                    padding=2,
                    content=ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Divider(),
                            self.btn_crear_nuevo_quiz,
                            ft.Divider(),
                            self.titulo,
                            ft.Column(
                                controls=[self.lista_quiz],
                                scroll=ft.ScrollMode.AUTO,
                                expand=True,  # Obligatorio para que ocupe el espacio disponible
                            ),
                            ft.Divider(),
                            self.btn_volver,
                        ],
                    ),
                )
            ],
        )

    def crear_tarjetas(self):
        return [
            ft.Row(
                key=f"quiz_row_{id}",
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Card(
                        key=f"quiz_card_{id}",
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
                                            color=ft.Colors.WHITE,
                                        ),
                                        subtitle=ft.Text(
                                            f"Para: {item['nombre_creador']}\n{item['comentario']}\n{item['cantidad_preguntas']} preguntas.",
                                            color=ft.Colors.WHITE,
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ),
                    ft.Button(
                        "Edit",
                        data=quiz_id,
                        on_click=self._on_editar,
                    ),
                ],
            )
            for quiz_id, item in reversed(self.dict_quiz.items())
        ]

    def actualizar_datos(self, nuevos_quizzes: dict):
        self.dict_quiz = nuevos_quizzes
        self.lista_quiz.controls = self.crear_tarjetas()
        try:
            if self.lista_quiz.page:
                self.lista_quiz.update()
        except RuntimeError:
            pass

    def _on_editar(self, e):
        if self.on_editar:
            self.on_editar(e)

    def _on_volver(self, e):
        if self.on_volver:
            self.on_volver()

    def _on_nuevo(self, e):
        if self.on_nuevo:
            self.on_nuevo()


if __name__ == "__main__":

    def main(page: ft.Page):
        page.title = "Prueba QuestionSelectorView"
        ventana = SeleccionQuizView()
        page.views.append(ventana)
        page.update()

    ft.run(main)
