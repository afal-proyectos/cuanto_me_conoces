import flet as ft


class QuizQuestionTile(ft.ExpansionTile):
    def __init__(
        self,
        question_id,
        question,
        options,
        score,
        on_edit=None,
        on_delete=None,
    ):
        super().__init__(
            title=ft.Text(question),
            subtitle=ft.Text(f"Puntaje: {score}"),
            controls=[
                ft.Text("Alternativas"),
                *[ft.Text(f"• {option}") for option in options],
                ft.Divider(),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar",
                            on_click=self._edit_click,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Eliminar",
                            on_click=self._delete_click,
                        ),
                    ],
                ),
            ],
        )

        self.question_id = question_id
        self.on_edit = on_edit
        self.on_delete = on_delete

    def _edit_click(self, e):
        if self.on_edit:
            self.on_edit(self.question_id)

    def _delete_click(self, e):
        if self.on_delete:
            self.on_delete(self.question_id)


# ==========================================================
# Vista
# ==========================================================


class QuizEditor(ft.View):
    def __init__(
        self,
        on_edit_question=None,
        on_delete_question=None,
        on_enviar_quiz=None,
        on_back=None,
    ):
        super().__init__(route="/editor")

        self.on_edit_question = on_edit_question
        self.on_delete_question = on_delete_question
        self.on_send_quiz = on_enviar_quiz
        self.on_back = on_back

        self._create_controls()
        self._build_layout()

    # ------------------------------------------------------

    def _create_controls(self):

        self.lbl_title = ft.Text(
            "Editar Quiz",
            size=32,
            weight=ft.FontWeight.BOLD,
        )

        self.lbl_counter = ft.Text("Preguntas: 0 / 10")

        self.lst_questions = ft.ListView(
            expand=True,
            spacing=8,
        )

        self.btn_send = ft.Button(
            "Enviar Quiz",
            on_click=self._send_click,
        )

        self.btn_back = ft.Button(
            "Volver",
            on_click=self._back_click,
        )

    # ------------------------------------------------------

    def _build_layout(self):

        self.controls = [
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.lbl_title,
                        ft.Divider(),
                        self.lst_questions,
                        ft.Divider(),
                        self.lbl_counter,
                        self.btn_send,
                        self.btn_back,
                    ],
                ),
            )
        ]

    # =====================================================
    # API pública
    # =====================================================

    def add_question(
        self,
        question_id,
        question,
        options,
        score,
    ):
        self.tile = QuizQuestionTile(
            question_id=question_id,
            question=question,
            options=options,
            score=score,
            on_edit=self.on_edit_question,
            on_delete=self.on_delete_question,
        )
        self.btn_back.data = question_id  # agrego a data, del botón volver, el id del quiz para deshabilarlo
        self.lst_questions.controls.append(self.tile)
        self.update_counter()
        self.update()

    # ------------------------------------------------------

    def clear_questions(self):
        self.lst_questions.controls.clear()
        self.update_counter()
        self.update()

    # ------------------------------------------------------

    def update_counter(self, total=10):
        current = len(self.lst_questions.controls)
        self.lbl_counter.value = f"Preguntas: {current} / {total}"

    # =====================================================
    # Eventos
    # =====================================================

    def _send_click(self, e):
        if self.on_send_quiz:
            self.on_send_quiz()

    # ------------------------------------------------------

    def _back_click(self, e):
        if self.on_back:
            self.on_back(e)


# ==========================================================
# Prueba
# ==========================================================

if __name__ == "__main__":

    def main(page: ft.Page):

        page.title = "Quiz Editor"

        view = QuizEditor(
            on_edit_question=lambda q: print(f"Editar {q}"),
            on_delete_question=lambda q: print(f"Eliminar {q}"),
            on_enviar_quiz=lambda: print("Enviar Quiz"),
            on_back=lambda: print("Volver"),
        )

        page.views.append(view)
        page.update()

        view.add_question(
            question_id=1,
            question="¿Cuál es mi color favorito?",
            options=["Azul", "Rojo", "Verde", "Negro"],
            score=10,
        )

        view.add_question(
            question_id=2,
            question="¿Cuál es mi película favorita?",
            options=["Matrix", "Titanic", "Avatar", "Rocky"],
            score=8,
        )

        view.add_question(
            question_id=3,
            question="¿Cuál es mi comida favorita?",
            options=["Pizza", "Sushi", "Pastas", "Asado"],
            score=5,
        )

        page.update()

    ft.run(main)
