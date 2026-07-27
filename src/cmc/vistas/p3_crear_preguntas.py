import flet as ft


class CrearPreguntas(ft.View):
    def __init__(
        self,
        on_question_selected=None,
        on_finish=None,
        on_back=None,
    ):

        self.on_question_selected = on_question_selected
        self.on_finish = on_finish
        self.on_back = on_back

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
                            self.cmb_question_type,
                            self.opciones,
                            ft.Divider(),
                            self.lst_questions,
                            ft.Divider(),
                            self.btn_finish,
                            self.btn_back,
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

        self.cmb_question_type = ft.Dropdown(
            width=300,
            label="Tipo de pregunta",
            value="multiple",
            options=[
                ft.dropdown.Option(
                    key="SM",
                    text="Selección múltiple",
                ),
                ft.dropdown.Option(
                    key="VoF",
                    text="Verdadero o Falso",
                ),
                ft.dropdown.Option(
                    key="L3",
                    text="Lista de 10",
                ),
            ],
        )

        self.lst_questions = ft.ListView(
            expand=True,
            spacing=5,
            auto_scroll=False,
        )

        self.opciones = ft.Card(
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,
            content=ft.Container(
                width=400,
                padding=10,
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            bgcolor=ft.Colors.GREY_400,
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text("Javiera"),
                        )
                    ]
                ),
            ),
        )

        self.btn_finish = ft.Button(
            "Terminar Quiz",
            on_click=self._on_finish_click,
        )

        self.btn_back = ft.Button(
            "Volver",
            on_click=self._on_back_click,
        )

    def add_question(self, question_id, text):
        self.lst_questions.controls.append(
            ft.ListTile(
                title=ft.Text(text),
                on_click=lambda e: self._on_question_click(question_id),
            )
        )
        self.update()

    def clear_questions(self):
        self.lst_questions.controls.clear()
        self.update()

    def _on_question_click(self, question_id):

        if self.on_question_selected:
            self.on_question_selected(question_id)

    def _on_finish_click(self, e):
        if self.on_finish:
            self.on_finish()

    def _on_back_click(self, e):
        if self.on_back:
            self.on_back()


if __name__ == "__main__":

    def main(page: ft.Page):

        page.title = "Prueba QuestionSelectorView"

        view = CrearPreguntas(
            on_question_selected=lambda q: print(f"Pregunta {q}"),
            on_finish=lambda: print("Terminar Quiz"),
            on_back=lambda: print("Volver"),
        )

        page.views.append(view)
        page.update()
        # Datos de prueba

        view.add_question(1, "¿Cuál es mi color favorito?")
        view.add_question(2, "¿Cuál es mi película favorita?")
        view.add_question(3, "¿Cuál es mi comida favorita?")
        view.add_question(4, "¿Cuál es mi canción favorita?")
        view.add_question(5, "¿Cuál es mi equipo favorito?")
        view.add_question(6, "¿Cuál es mi mascota favorita?")
        view.add_question(7, "¿Cuál es mi bebida favorita?")
        view.add_question(8, "¿Cuál es mi libro favorito?")

    ft.run(main)
