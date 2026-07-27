import flet as ft


class DatosQuizView(ft.View):
    def __init__(
        self,
        on_continuar=None,
        on_volver=None,
    ):
        # callbacks
        self.on_continuar = on_continuar
        self.on_volver = on_volver

        # Controles
        self.lbl_titulo = ft.Container(
            content=ft.Text("Datos del Quizz", size=30, weight=ft.FontWeight.BOLD),
            margin=ft.Margin.only(bottom=50),
            padding=50,
        )

        self.txt_nombre = ft.TextField(
            label="Nombre del creador", width=320, on_change=self._validar_campos
        )

        self.txt_evento = ft.TextField(
            label="Nombre del evento", width=320, on_change=self._validar_campos
        )

        self.cmb_cantidad = ft.Dropdown(
            label="Cantidad de preguntas",
            width=320,
            value="5",
            options=[
                ft.dropdown.Option("5"),
                ft.dropdown.Option("7"),
                ft.dropdown.Option("10"),
            ],
        )
        self.cmb_cantidad.on_change = self._validar_campos

        self.btn_continuar = ft.ElevatedButton(
            content=ft.Text("Continuar"),
            on_click=self._on_continuar_click,
            disabled=True,
        )

        self.btn_volver = ft.ElevatedButton(
            content=ft.Text("Volver"),
            on_click=self._on_volver_click,
        )

        # vista
        super().__init__(
            route="/datos",
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        width=350,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.lbl_titulo,
                            self.txt_nombre,
                            self.txt_evento,
                            self.cmb_cantidad,
                            self.btn_continuar,
                            self.btn_volver,
                        ],
                    ),
                )
            ],
        )

    def _validar_campos(self, e):
        nombre_ok = bool(self.txt_nombre.value and self.txt_nombre.value.strip())
        evento_ok = bool(self.txt_evento.value and self.txt_evento.value.strip())
        cantidad_ok = bool(self.cmb_cantidad.value)

        if nombre_ok and evento_ok and cantidad_ok:
            self.btn_continuar.disabled = False
        else:
            self.btn_continuar.disabled = True

        self.btn_continuar.update()

    def _on_continuar_click(self, e):
        if self.on_continuar:
            self.on_continuar(
                nombre_creador=self.txt_nombre.value,
                nombre_evento=self.txt_evento.value,
                cantidad_preguntas=int(self.cmb_cantidad.value),
            )

    def _on_volver_click(self, e):
        if self.on_volver:
            self.on_volver()


if __name__ == "__main__":

    def main(page: ft.Page):

        page.title = "Prueba dos"
        page.views.clear()
        page.views.append(
            DatosQuizView(
                on_continuar=lambda nombre_creador, nombre_evento, cantidad_preguntas: (
                    print(
                        f"Nombre: {nombre_creador}, Evento: {nombre_evento}, Cantidad: {cantidad_preguntas}"
                    )
                ),
                on_volver=lambda: print("Regresar"),
            )
        )

        page.update()

    ft.run(main)
