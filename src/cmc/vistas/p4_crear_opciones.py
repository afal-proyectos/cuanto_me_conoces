import flet as ft


class CrearOpciones(ft.AlertDialog):
    def __init__(
        self,
        tipo_pregunta=None,
        question_text=None,
        on_save=None,
        on_cancel=None,
    ):
        super().__init__(
            modal=True,
            # actions_alignment=ft.MainAxisAlignment.END,
        )

        self.on_save = on_save
        self.on_cancel = on_cancel

        self._create_controls()
        self.tipo = tipo_pregunta
        self.title = ft.Text(question_text)
        self.content = self._build_content()
        # self.actions = [self.btn_cancel, self.btn_save]

    # =====================================================
    # Controles
    # =====================================================

    def _create_controls(self):

        self.txt_option1 = ft.TextField(label="Opción 1")
        self.txt_option2 = ft.TextField(label="Opción 2")
        self.txt_option3 = ft.TextField(label="Opción 3")
        self.txt_option4 = ft.TextField(label="Opción 4")

        self.score1 = ft.Dropdown(
            label="Puntos",
            expand=True,
            value="0",
            options=[ft.dropdown.Option(str(i)) for i in range(-5, 6)],
        )
        self.score2 = ft.Dropdown(
            label="Puntos",
            expand=True,
            value="0",
            options=[ft.dropdown.Option(str(i)) for i in range(-5, 6)],
        )
        self.score3 = ft.Dropdown(
            label="Puntos",
            expand=True,
            value="0",
            options=[ft.dropdown.Option(str(i)) for i in range(-5, 6)],
        )
        self.score4 = ft.Dropdown(
            label="Puntos",
            expand=True,
            value="0",
            options=[ft.dropdown.Option(str(i)) for i in range(-5, 6)],
        )

        self.btn_save = ft.Button(
            "Guardar",
            expand=True,
            on_click=self._on_save_click,
        )

        self.btn_cancel = ft.Button(
            "Cancelar",
            expand=True,
            on_click=self._on_cancel_click,
        )

    # =====================================================
    # Layout
    # =====================================================

    def _build_content(self):

        return ft.Column(
            tight=True,
            expand=True,
            controls=[
                ft.Row(controls=[self.txt_option1, self.score1]),
                ft.Row(controls=[self.txt_option2, self.score2]),
                ft.Row(controls=[self.txt_option3, self.score3]),
                ft.Row(controls=[self.txt_option4, self.score4]),
                ft.Divider(),
                ft.Row(controls=[self.btn_cancel, self.btn_save]),
            ],
        )

    # =====================================================
    # API pública
    # =====================================================

    def clear(self):

        self.txt_option1.value = ""
        self.txt_option2.value = ""
        self.txt_option3.value = ""
        self.txt_option4.value = ""
        self.score1.value = "0"
        self.score2.value = "0"
        self.score3.value = "0"
        self.score4.value = "0"

        self.update()

    def load_question(
        self,
        option1="",
        option2="",
        option3="",
        option4="",
        score1=0,
        score2=0,
        score3=0,
        score4=0,
    ):

        self.txt_option1.value = option1
        self.txt_option2.value = option2
        self.txt_option3.value = option3
        self.txt_option4.value = option4
        self.score1.value = str(score1)
        self.score2.value = str(score2)
        self.score3.value = str(score3)
        self.score4.value = str(score4)

        self.update()

    # =====================================================
    # Eventos
    # =====================================================

    def _on_save_click(self, e):
        # print(f"prueba de tipo:{self.tipo}")
        if self.on_save:
            self.on_save(
                tipo=self.tipo,
                pregunta=self.title.value,
                option1=self.txt_option1.value,
                option2=self.txt_option2.value,
                option3=self.txt_option3.value,
                option4=self.txt_option4.value,
                score1=int(self.score1.value),
                score2=int(self.score2.value),
                score3=int(self.score3.value),
                score4=int(self.score4.value),
            )

    def _on_cancel_click(self, e):

        if self.on_cancel:
            self.on_cancel()


if __name__ == "__main__":

    def main(page: ft.Page):
        page.title = "Prueba de CrearOpciones"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def cerrar_dialogo(e=None):
            page.pop_dialog()
            page.update()

        def guardar_datos(**kwargs):
            print(f"Datos guardados: {kwargs}")
            cerrar_dialogo()

        # Instanciamos el diálogo
        dlg = CrearOpciones(
            question_text="¿Cuál es tu lenguaje favorito?",
            on_save=guardar_datos,
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
