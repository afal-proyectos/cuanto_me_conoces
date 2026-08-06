import flet as ft


class InicioView(ft.View):
    def __init__(
        self,
        on_nuevo_quiz=None,
        on_seguir_editando=None,
        on_ver_ranking=None,
        textos=None,
    ):
        self.textos = textos
        self.on_nuevo_quiz = on_nuevo_quiz
        self.on_seguir_editando = on_seguir_editando
        self.on_ver_ranking = on_ver_ranking

        self._crear_controles()
        self._crear_vista()

    def _crear_controles(self):
        self.ibl_titulo = ft.Text(
            self.textos["nombre"],
            # padding=5,
            text_align=ft.TextAlign.CENTER,
            size=50,
            weight=ft.FontWeight.BOLD,
        )

        self.btn_nuevo = ft.ElevatedButton(
            content="Crear nuevo Quiz",
            width=320,
            height=45,
            bgcolor="#FF0000",
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE  # Aquí defines el color del texto
            ),
            on_click=self._on_nuevo_quiz_click,
        )

        self.btn_continuar = ft.ElevatedButton(
            content="Seguir editando",
            width=320,
            height=45,
            bgcolor="BLUE",
            style=ft.ButtonStyle(color=ft.Colors.WHITE),
            on_click=self._on_seguir_editando_click,
        )

        self.btn_ver_ranking = ft.ElevatedButton(
            content="Ver Ranking y QR",
            width=320,
            height=45,
            bgcolor="GREEN",
            style=ft.ButtonStyle(color=ft.Colors.WHITE),
            on_click=self._on_ver_ranking_click,
        )

    def _crear_vista(self):
        super().__init__(
            route="/",
            controls=[
                ft.Container(  # contenedor "base", sobre él esta todo lo demás
                    expand=True,  # se "expoande" para ocupar toda la pantalla posible
                    padding=10,
                    alignment=ft.Alignment.CENTER,  # siempre estará centrado
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=30,  # paramtro de separación vertical de los elementos
                        controls=[
                            self.ibl_titulo,
                            self.btn_nuevo,
                            self.btn_continuar,
                            self.btn_ver_ranking,
                        ],
                    ),
                )
            ],
        )

    # Eventos privados:
    def _on_nuevo_quiz_click(self, e):
        if self.on_nuevo_quiz:
            self.on_nuevo_quiz()

    def _on_seguir_editando_click(self, e):
        if self.on_seguir_editando:
            self.on_seguir_editando()

    def _on_ver_ranking_click(self, e):
        if self.on_ver_ranking:
            self.on_ver_ranking()


if __name__ == "__main__":
    tex = {"nombre": "¿Cuánto me Conoces?"}

    def main(page: ft.Page):

        page.title = "Prueba Inicio"
        page.views.clear()
        page.views.append(
            InicioView(
                textos=tex,
                on_nuevo_quiz=lambda: print("Nuevo Quiz"),
                on_seguir_editando=lambda: print("Seguir editando"),
                on_ver_ranking=lambda: print("Ver el ranking y el código QR"),
            )
        )

        page.update()

    ft.app(main)
