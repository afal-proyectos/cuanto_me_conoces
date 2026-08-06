import flet as ft


class CrearPreguntas(ft.View):
    def __init__(
        self,
        tex_pregunta=None,
        on_selec_pregunta=None,
        on_regresar=None,
    ):
        self.on_select_pregunta = on_selec_pregunta
        self.on_regresar = on_regresar
        self.tex_pregunta = tex_pregunta
        self._crear_controls()
        self._crear_vista()

    def _crear_vista(self):
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
                        ],
                    ),
                )
            ],
        )

    def _crear_controls(self):

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
            "Ver Quiz",
            on_click=self._on_finish_click,
        )

    def cambiar_lista(self, clave_boton):
        self.tipo_pregunta = clave_boton
        lista = self.tex_pregunta.get(self.tipo_pregunta, [])
        self.lista_preguntas.controls = [
            ft.ListTile(
                title=ft.Text(pregunta),
                on_click=lambda e, t=pregunta: self._on_select_pregunta(
                    e, t, self.tipo_pregunta
                ),
            )
            for pregunta in lista
        ]
        self.lista_preguntas.update()

    def _on_select_pregunta(self, e, pregunta, tipo):
        if self.on_select_pregunta:
            self.on_select_pregunta(pregunta, tipo)

    def _on_finish_click(self, e):
        if self.on_regresar:
            self.on_regresar(e)


if __name__ == "__main__":
    opciones = {
        "multiple": [
            "¿Cuál es mi color favorito?",
            "¿Cuál es mi lugar favorito?",
            "¿Cuál es mi pelicula favorita?",
            "¿Cuál es mi comida favorita?",
            "¿Cuál es mi superhéroe favorito?",
        ],
        "vof": [
            "Amo a los animales",
            "Me encantaría vivir en el campo",
            "Mi comida favorita es la pizza",
        ],
    }

    def main(page: ft.Page):

        page.title = "Prueba QuestionSelectorView"

        vista = CrearPreguntas(
            on_selec_pregunta=lambda pregunta, tipo: print(
                f"Tipo: {tipo}\nPregunta: {pregunta}"
            ),
            on_regresar=lambda: print("Terminar Quiz"),
            tex_pregunta=opciones,
        )

        page.views.append(vista)
        page.update()

    ft.run(main)
