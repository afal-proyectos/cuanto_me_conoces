import flet as ft


class QuizTerminados(ft.View):
    def __init__(self, on_comenzar=None, on_regresar=None, on_seguir_editando=None):
        super().__init__(route="/quiz_terminados", padding=20, controls=[])

        self.on_comenzar = on_comenzar
        self.on_regresar = on_regresar
        self.on_seguir_editando = on_seguir_editando

        self._crear_controles()
        self._crear_vista()

    def _crear_controles(self):
        self.btn_comenzar = ft.Button("Comenzar", on_click=self._on_comenzar_click)
        self.btn_regresar = ft.Button("Regresar", on_click=self._on_regresar)
        self.btn_editar = ft.Button(
            "Seguir Editando", on_click=self._on_seguir_editando
        )
        self.list_quiz_terminados = ft.Column(controls=[self._crear_lista_terminada()])

    def _crear_vista(self):
        self.controls = ft.Container(
            expand=True,
            padding=2,
            content=ft.Column(
                controls=[self.btn_comenzar, self.btn_regresar, self.btn_editar]
            ),
        )

    def _crear_lista_terminada(self):
        lista = []
        return lista

    def _on_comenzar_click(self, e):
        if self.on_comenzar:
            self.on_comenzar()

    def _on_regresar(self, e):
        if self.on_regresar:
            self.on_regresar()

    def _on_seguir_editando(self, e):
        if self.on_seguir_editando:
            self.on_seguir_editando()


if __name__ == "__main__":

    def app(vista: ft.Page):
        page = vista
        page.title = "Quiz Terminados"
        page.page.window.width = 350
        page.page.window.height = 685
        ventana = QuizTerminados(
            on_comenzar=lambda: print("¡Comenzar!"),
            on_seguir_editando=lambda: print("Seguir Editando"),
            on_regresar=lambda: print("Ir a inicio"),
        )
        page.views.append(ventana)
        page.update()

    ft.run(app)
