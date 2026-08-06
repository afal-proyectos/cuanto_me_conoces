import flet as ft


class EditorQuiz(ft.View):
    def __init__(
        self,
        quiz_preguntas=None,
        on_agregar=None,
        on_editar=None,
        on_eliminar_pregunta=None,
        on_cambiar=None,
        on_eliminar_quiz=None,
        on_terminar=None,
    ):

        self.on_terminar = on_terminar
        self.on_eliminar_quiz = on_eliminar_quiz
        self.on_cambiar = on_cambiar
        self.on_eliminar_pregunta = on_eliminar_pregunta
        self.on_editar = on_editar
        self.on_agregar = on_agregar
        self.data_quiz = (
            quiz_preguntas  # es la data de TODo el quiz, no solo las preguntas
        )

        self._info_quiz()
        self._controles()
        self._vista()

    # Metódo en contrucción, necesario para luego dibujar info en pantalla.
    # aquí "desempacaré" toda la info que viene en self.data_quiz", para los fines de esta versión de la app, 0.2 aún no es necesario.
    def _info_quiz(self):
        self.nombre_creado = "pregunta[]"

    def _controles(self):
        self.cantidad_preguntas = ft.Text(self.contador_pregunta())

        self.titulo = ft.Text(
            "Editor de Quiz",
            align=ft.Alignment.CENTER,
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        self.agregar_nueva_pregunta = ft.Button(
            "Agregar Pregunta",
            align=ft.Alignment.CENTER,
            on_click=self._on_agregar,
            visible=not self._limite_alcanzado(),
        )

        self.editar_pregunta = ft.IconButton(
            icon=ft.Icons.EDIT,
            tooltip="Editar",
            align=ft.Alignment.CENTER,
            expand=True,
            on_click=self._on_editar,
        )

        self.eliminar_pregunta = ft.IconButton(
            icon=ft.Icons.DELETE,
            tooltip="Eliminar",
            align=ft.Alignment.CENTER,
            on_click=self._on_eliminar_pregunta,
        )

        self.lista_pregunta = ft.Column(
            controls=self._agregar_pregunta()
        )  # "controls" es una lista de elementos.

        self.cambiar_quiz = ft.Button(
            "Cambiar de Quiz",
            align=ft.Alignment.CENTER,
            expand=True,
            on_click=self._on_cambiar,
        )

        self.eliminar_quiz = ft.Button(
            "Eliminar Quiz",
            align=ft.Alignment.CENTER,
            on_click=self._on_eliminar_quiz,
        )

        self.terminar = ft.Button(
            "Terminar Quiz",
            align=ft.Alignment.CENTER,
            on_click=self._on_terminar,
            visible=self._limite_alcanzado(),
        )

    def _vista(self):
        super().__init__(
            route="/editor_quiz",
            padding=20,
            controls=[
                ft.Column(
                    controls=[
                        self.titulo,
                        self.cantidad_preguntas,
                        self.lista_pregunta,
                        ft.Column(
                            controls=[self.agregar_nueva_pregunta, self.terminar],
                        ),
                        ft.Row(
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            controls=[self.cambiar_quiz, self.eliminar_quiz],
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                )
            ],
        )

    def _agregar_pregunta(self):  # devuelve la lista de elementos que necesitaremos
        lista = []
        # acceso a la lista de preguntas del diccionario
        preguntas = self.data_quiz.get("data_preguntas", [])
        for dato in preguntas:
            elemento = ft.ExpansionTile(
                expanded=True,
                title=ft.Text(dato["pregunta"]),
                controls=[
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=self._agregar_opciones(
                                            dato["opciones"]
                                        ),
                                        expand=True,
                                    ),
                                    ft.Column(
                                        controls=self._agregar_puntaje(dato["puntaje"]),
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ],
                            ),
                            ft.Row(
                                controls=[self.editar_pregunta, self.eliminar_pregunta],
                            ),
                        ]
                    )
                ],
            )

            lista.append(elemento)

        return lista

    def _limite_alcanzado(self):
        preguntas = self.data_quiz.get("data_preguntas", [])
        agre = len(preguntas)
        total = self.data_quiz.get("cantidad_preguntas", 0)
        return agre >= total

    def contador_pregunta(self):
        preguntas = self.data_quiz.get("data_preguntas", [])
        agregadas = len(preguntas)
        total_quiz = self.data_quiz.get("cantidad_preguntas", 0)
        contador = f"Preguntas: {agregadas} / {total_quiz}"

        return contador

    def _agregar_opciones(self, opciones):
        return [ft.Text(op) for op in opciones.values()]

    def _agregar_puntaje(self, puntaje):
        return [ft.Text(f"{p} puntos.") for p in puntaje.values()]

    def _on_agregar(self, e):
        if self.on_agregar:
            self.on_agregar()

    def _on_editar(self, e):
        if self.on_editar:
            self.on_editar()

    def _on_eliminar_pregunta(self, e):
        if self.on_eliminar_pregunta:
            self.on_eliminar_pregunta()

    def _on_eliminar_quiz(self, e):
        if self.on_eliminar_quiz:
            self.on_eliminar_quiz()

    def _on_cambiar(self, e):
        if self.on_cambiar:
            self.on_cambiar()

    def _on_terminar(self, e):
        if self.on_terminar:
            self.on_terminar()

    def _on_terminar(self, e):
        if self.on_terminar:
            self.on_terminar()

    def actualiazr_botones(self):
        limite = self._limite_alcanzado()
        self.agregar_nueva_pregunta.visible = not limite
        self.terminar.visible = limite
        try:
            if self.agregar_nueva_pregunta.page:
                self.agregar_nueva_pregunta.update()
                self.terminar.update()
        except RuntimeError:
            pass


if __name__ == "__main__":
    data = {
        "2a43ab4e-11eb-4ba9-98cc-74c6436e3279": {
            "nombre_creador": "as",
            "nombre_evento": "as",
            "comentario": "as",
            "cantidad_preguntas": 5,
            # "editable": true,
            "data_preguntas": [
                {
                    "id_pregunta": "2a43ab4e-11eb-4ba9-98cc-74c6436e3201",
                    "index": 1,
                    "pregunta": "¿Anime Favorito?",
                    "opciones": {
                        "1": "Dragon Ball Z",
                        "2": "Demon Slayers",
                        "3": "Bako no Hero",
                    },
                    "puntaje": {"1": 4, "2": -2, "3": 0},
                },
                {
                    "id_pregunta": "2a43ab4e-11eb-4ba9-98cc-74c6436e3202",
                    "index": 1,
                    "pregunta": "¿Superhéroe favorito?",
                    "opciones": {"1": "Batman", "2": "Superman", "3": "WonderWoman"},
                    "puntaje": {"1": 4, "2": -2, "3": 0},
                },
            ],
        },
    }

    def pantalla(vista: ft.Page):
        page = vista
        page.title = "Quiz Editor"
        page.page.window.width = 350
        page.page.window.height = 685
        page.theme_mode = ft.ThemeMode.LIGHT

        ventana = EditorQuiz(
            quiz_preguntas=data["2a43ab4e-11eb-4ba9-98cc-74c6436e3279"],
            on_agregar=lambda: print("Agregar pregunta"),
            on_editar=lambda: print("editar Pregunta"),
            on_cambiar=lambda: print("Cambiar Quiz"),
            on_eliminar_pregunta=lambda: print("Eliminar Pregunta"),
            on_eliminar_quiz=lambda: print("Eliminar Quiz"),
            on_terminar=lambda: print("Terminar"),
        )

        page.views.append(ventana)
        page.update()

    ft.run(pantalla)  # , view=ft.AppView.WEB_BROWSER)


"""

def _agregar_pregunta(self):
        lista = []

        dor id, dato in self.pregunta.items():
            elemento = ft.ExpansionTile(title=ft.Text(dato["pregunta"]))
            lista.append(elemento)
        
        return lista
"""
