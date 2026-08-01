import flet as ft
from textos.txt import TxPreguntas as tx


class CrearPreguntas(ft.View):
    def __init__(
        self,
        on_question_selected=None,
        on_finish=None,
        # on_back=None,
    ):

        self.on_question_selected = on_question_selected
        self.on_finish = on_finish
        # self.on_back = on_back

        self._create_controls()

        super().__init__(
            route="/questions",
            controls=[
                ft.Container(
                    expand=True,
                    padding=20,
                    content=ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.lbl_title,
                            ft.Row(
                                height=100,
                                controls=[
                                    self.opciones,
                                    self.verdad_mentira,
                                ],
                            ),
                            ft.Row(
                                height=100,
                                controls=[
                                    self.ranking_10,
                                    self.trio,
                                ],
                            ),
                            ft.Divider(),
                            self.lista_preguntas,
                            ft.Divider(),
                            self.btn_finish,
                            # self.btn_back,
                        ],
                    ),
                )
            ],
        )

    def _create_controls(self):

        self.lbl_title = ft.Text(
            "Crear Pregunta",
            size=30,
            weight=ft.FontWeight.BOLD,
        )

        self.lista_preguntas = ft.Column(
            expand=True,
            spacing=5,
            scroll=ft.ScrollMode.AUTO,
        )

        self.opciones = ft.Button(
            "Seleccion Multiple",
            expand=True,
            height=100,
            bgcolor=ft.Colors.RED,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=2)
            ),
            on_click=lambda e: self.cambiar_lista("multiple"),
        )
        self.verdad_mentira = ft.Button(
            "Verdad o Mentira",
            expand=True,
            height=100,
            bgcolor=ft.Colors.GREEN,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=2)
            ),
            on_click=lambda e: self.cambiar_lista("vof"),
        )
        self.ranking_10 = ft.Button(
            "Del 1 al 10",
            expand=True,
            height=100,
            bgcolor=ft.Colors.BLUE,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=2)
            ),
            on_click=lambda e: self.cambiar_lista("btn_3"),
        )
        self.trio = ft.Button(
            "Encuentra el trio",
            expand=True,
            height=100,
            bgcolor="#ffc800",
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=2)
            ),
            on_click=lambda e: self.cambiar_lista("btn_4"),
        )
        self.btn_finish = ft.Button(
            "Terminar Quiz",
            on_click=self._on_finish_click,
        )

        # self.btn_back = ft.Button(
        #    "Volver",
        #    on_click=self._on_back_click,
        # )

    def cambiar_lista(self, clave_boton):
        self.tipo_pregunta = clave_boton
        alternativas = tx.opciones.get(self.tipo_pregunta, [])
        self.lista_preguntas.controls = [
            ft.ListTile(
                title=ft.Text(text),
                on_click=lambda e, t=text: self._on_question_click(
                    t, self.tipo_pregunta
                ),
            )
            for text in alternativas
        ]
        self.lista_preguntas.update()

    # def clear_questions(self):
    #    self.lst_questions.controls.clear()
    #    self.update()
    def _on_question_click(self, pregunta, tipo):
        if self.on_question_selected:
            self.on_question_selected(pregunta, tipo)
            print(f"Seleccionado:{tipo}={pregunta}")

    def _on_finish_click(self, e):
        if self.on_finish:
            self.on_finish()

    # def _on_back_click(self, e):
    #    if self.on_back:
    #       self.on_back()


if __name__ == "__main__":

    def main(page: ft.Page):

        page.title = "Prueba QuestionSelectorView"

        view = CrearPreguntas(
            on_question_selected=lambda q: print(f"Pregunta {q}"),
            on_finish=lambda: print("Terminar Quiz"),
            # on_back=lambda: print("Volver"),
        )

        page.views.append(view)
        page.update()
        # Datos de prueba
        ft.run(main)


"""
        view.add_question(1, "¿Cuál es mi color favorito?")
        view.add_question(2, "¿Cuál es mi película favorita?")
        view.add_question(3, "¿Cuál es mi comida favorita?")
        view.add_question(4, "¿Cuál es mi canción favorita?")
        view.add_question(5, "¿Cuál es mi equipo favorito?")
        view.add_question(6, "¿Cuál es mi mascota favorita?")
        view.add_question(7, "¿Cuál es mi bebida favorita?")
        view.add_question(8, "¿Cuál es mi libro favorito?")
"""
