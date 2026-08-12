import flet as ft


class QuizTerminados(ft.View):
    def __init__(
        self,
        on_comenzar=None,
        on_regresar=None,
        on_revisar=None,
        on_seguir_editando=None,
        quiz_terminados=None,
    ):
        super().__init__(route="/quiz_terminados", padding=20, controls=[])
        self.on_revisar = on_revisar
        self.on_comenzar = on_comenzar
        self.on_regresar = on_regresar
        self.on_seguir_editando = on_seguir_editando
        self.quiz_terminados = quiz_terminados

        self._crear_controles()
        self._crear_vista()

    def _crear_controles(self):
        self.btn_comenzar = ft.Button("Comenzar", on_click=self._on_comenzar_click)
        self.btn_regresar = ft.Button("Regresar", on_click=self._on_regresar)
        self.list_quiz_terminados = ft.Column(
            controls=self._crear_lista_terminada(),
        )
        self.todas_las_preguntas = ft.Column()

    def _crear_vista(self):
        self.controls = ft.Container(
            expand=True,
            padding=2,
            content=ft.Column(
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        controls=self.list_quiz_terminados,
                    ),
                    ft.Divider(),
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        controls=self.todas_las_preguntas,
                    ),
                    self.btn_comenzar,
                    self.btn_regresar,
                ]
            ),
        )

    def _crear_lista_terminada(self):
        lista = []
        terminados = self.quiz_terminados

        for id_quiz, dato in terminados.items():
            # t = id_quiz
            terminados = ft.Row(
                controls=[
                    ft.Card(
                        expand=True,
                        key=f"card_{id}",
                        content=ft.Container(
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    ft.ListTile(title=ft.Text(dato["nombre_creador"])),
                                ],
                            ),
                        ),
                    ),
                    ft.Button(
                        "Revisar",
                        expand_loose=True,
                        data=id_quiz,
                        on_click=lambda e: self._mostrar_lista_quiz(e),
                    ),
                ]
            )
            lista.append(terminados)

        return lista

    def _mostrar_lista_quiz(self, e):
        id_q = e.control.data
        self.todas_las_preguntas.controls.clear()
        try:
            preguntas = self.quiz_terminados[id_q]
            for pregunta in preguntas["data_preguntas"]:
                a = ft.ExpansionTile(
                    title=ft.Text(pregunta["pregunta"]),
                    controls=ft.ListTile(
                        title=ft.Text(pregunta["pregunta"]),
                        on_click=lambda _: print(id_q),
                    ),
                )

                self.todas_las_preguntas.controls.append(a)

            self.todas_las_preguntas.update()
        except KeyError:
            pass

    def _on_comenzar_click(self, e):
        if self.on_comenzar:
            self.on_comenzar()

    def _on_regresar(self, e):
        if self.on_regresar:
            self.on_regresar()

    def _on_revisar(self, e):
        if self.on_revisar:
            self.on_revisar()

    def _on_seguir_editando(self, e):
        if self.on_seguir_editando:
            self.on_seguir_editando()


if __name__ == "__main__":
    datos = {
        "b7b52d35-fcd0-41ef-8d20-d74a1aebd16d": {
            "nombre_creador": "Alejandro",
            "nombre_evento": "Cerro Alegre",
            "comentario": "Prueba 1",
            "cantidad_preguntas": 5,
            "data_preguntas": [
                {
                    "id_pregunta": "97ff64d7-1d25-4ca8-921f-543b681ea718",
                    "tipo": "multiple",
                    "pregunta": "¿Cuál es mi color favorito?",
                    "opciones": {"1": "Rojo", "2": "verde", "3": "azul", "4": "morado"},
                    "puntaje": {"1": 4, "2": 0, "3": 0, "4": 4},
                },
                {
                    "id_pregunta": "f4293458-2767-4f2c-a10b-ad3e57761e8f",
                    "tipo": "multiple",
                    "pregunta": "¿Cuál es mi color favorito?",
                    "opciones": {
                        "1": "Rojo",
                        "2": "Verde",
                        "3": "Azul",
                        "4": "Amarillo",
                    },
                    "puntaje": {"1": 0, "2": 0, "3": 0, "4": 4},
                },
            ],
        },
        "123456-1": {
            "nombre_creador": "Ale",
            "edad": 23,
            "ciudad": "Santiago",
            "data_preguntas": [
                {
                    "pregunta": "¿mi color favorito?",
                },
                {
                    "pregunta": "¿mi super heroe favorito?",
                },
            ],
        },
        "789456-2": {
            "nombre_creador": "Feña",
            "edad": 20,
            "ciudad": "Santiago",
            "data_preguntas": [
                {
                    "pregunta": "¿mi lugar favorito?",
                }
            ],
        },
    }

    def app(vista: ft.Page):
        page = vista
        page.title = "Quiz Terminados"
        page.page.window.width = 350
        page.page.window.height = 685
        ventana = QuizTerminados(
            on_comenzar=lambda: print("¡Comenzar!"),
            on_seguir_editando=lambda: print("Seguir Editando"),
            on_regresar=lambda: print("Ir a inicio"),
            on_revisar=lambda: print("Revisar"),
            quiz_terminados=datos,
        )
        page.views.append(ventana)
        page.update()

    ft.run(app)
