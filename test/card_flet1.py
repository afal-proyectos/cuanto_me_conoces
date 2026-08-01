import flet as ft


class EditorQuiz(ft.View):
    def __init__(
        self,
        pregunta,
        on_agregar,
        on_editar,
        on_eliminar_pregunta,
        on_cambiar,
        on_eliminar_quiz,
        on_terminar,
    ):
        self.on_terminar = on_terminar
        self.on_eliminar_quiz = on_eliminar_quiz
        self.on_cambiar = on_cambiar
        self.on_eliminar_pregunta = on_eliminar_pregunta
        self.on_editar = on_editar
        self.on_agregar = on_agregar
        self.pregunta = pregunta

        self._controles()
        self._vista()

    def _controles(self):
        self.cantidad_preguntas = ft.Text(self.contador_pregunta())

        self.titulo = ft.Text(
            "Editor de Quiz",
            align=ft.Alignment.CENTER,
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        self.agregar_nueva_pregunta = ft.Button(
            "Agregar Pregunta", align=ft.Alignment.CENTER, on_click=self._on_agregar
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
            "Terminar Quiz", align=ft.Alignment.CENTER, on_click=self._on_terminar
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
                            scroll=ft.ScrollMode.AUTO,
                            expand=True,
                        ),
                        ft.Row(
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            controls=[self.cambiar_quiz, self.eliminar_quiz],
                        ),
                    ],
                    expand=True,
                )
            ],
        )

    def _agregar_pregunta(self):  # devuelve la lista de elementos que necesitaremos
        return [
            ft.ExpansionTile(
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
            for dato in self.pregunta.values()
        ]

    def contador_pregunta(self, total=10):
        agregadas = len(self.pregunta.values())
        contador = f"Preguntas: {agregadas} / {total}"
        return contador

    def _agregar_opciones(self, opciones):
        return [ft.Text(op) for op in opciones.values()]

    def _agregar_puntaje(self, puntaje):
        return [ft.Text(f"{p} puntos.") for p in puntaje.values()]

    def _on_agregar(self):
        if self.on_agregar:
            self.on_agregar()

    def _on_editar(self):
        if self.on_editar:
            self.on_editar()

    def _on_eliminar_pregunta(self):
        if self.on_eliminar_pregunta:
            self.on_eliminar_pregunta()

    def _on_eliminar_quiz(self):
        if self.on_eliminar_quiz:
            self.on_eliminar_quiz()

    def _on_cambiar(self):
        if self.on_cambiar:
            self.on_cambiar()

    def _on_terminar(self):
        if self.on_terminar:
            self.on_terminar()

    def _on_terminar(self):
        if self.on_terminar:
            self.on_terminar()


if __name__ == "__main__":
    data = {
        1: {
            "pregunta": "¿Color favorito?",
            "opciones": {"1": "rojo", "2": "verde", "3": "amarillo"},
            "puntaje": {"1": 4, "2": -2, "3": 0},
        },
        2: {
            "pregunta": "¿Comida favorita",
            "opciones": {"1": "pizza", "2": "casuela", "3": "pollo asado"},
            "puntaje": {"1": 4, "2": -2, "3": 0},
        },
    }

    def pantalla(vista: ft.Page):
        page = vista
        page.title = "Quiz Editor"
        page.page.window.width = 350
        page.page.window.height = 685
        page.theme_mode = ft.ThemeMode.LIGHT

        ventana = EditorQuiz(
            pregunta=data,
            on_agregar=lambda: print("Agregar pregunta"),
            on_editar=lambda: print("editar Pregunta"),
            on_cambiar=lambda: print("Cambiar Quiz"),
            on_eliminar_pregunta=lambda: print("Eliminar Pregunta"),
            on_eliminar_quiz=lambda: print("Eliminar Quiz"),
            on_terminar=lambda: print("Terminar"),
        )

        page.views.append(ventana)
        page.update()

    ft.run(pantalla)


"""

def _agregar_pregunta(self):
        lista = []

        dor id, dato in self.pregunta.items():
            elemento = ft.ExpansionTile(title=ft.Text(dato["pregunta"]))
            lista.append(elemento)
        
        return lista
"""
