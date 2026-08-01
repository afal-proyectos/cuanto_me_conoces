import flet as ft


class DatosQuizView(ft.AlertDialog):
    def __init__(
        self,
        on_continuar=None,
        on_volver=None,
    ):
        super().__init__(
            modal=True,
        )
        # callbacks
        self.on_continuar = on_continuar
        self.on_volver = on_volver

        self.crear_controles()

        self.title = self.lbl_titulo
        self.content = self._build_content()

    def crear_controles(self):
        self.lbl_titulo = ft.Container(
            content=ft.Text("Crear Nuevo", size=30, weight=ft.FontWeight.BOLD),
            margin=ft.Margin.only(bottom=5),
            padding=5,
            expand=True,
        )

        self.txt_nombre = ft.TextField(
            label="Ingresa tu nombre", width=320, on_change=self._validar_campos
        )

        self.txt_evento = ft.TextField(
            label="Nombre del evento donde jugarás",
            width=320,
            on_change=self._validar_campos,
        )
        self.txt_comentario = ft.TextField(
            label="Breve comentario de este Quiz", width=320
        )
        self.cmb_cantidad = ft.Dropdown(
            label="Cantidad de preguntas",
            width=320,
            value="5",
            expand=True,
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

    def _build_content(self):
        return ft.Column(
            tight=True,
            expand=True,
            controls=[
                self.lbl_titulo,
                self.txt_nombre,
                self.txt_evento,
                self.txt_comentario,
                self.cmb_cantidad,
                ft.Row(
                    controls=[
                        self.btn_continuar,
                        self.btn_volver,
                    ]
                ),
            ],
        )

        """    
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
                            self.txt_comentario,
                            self.cmb_cantidad,
                            ft.Row(
                                controls=[
                                    self.btn_continuar,
                                    self.btn_volver,
                                ]
                            ),
                        ],
                    ),
                )
            ],
        )
    """

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
                comentario=self.txt_comentario.value,
                cantidad_preguntas=int(self.cmb_cantidad.value),
            )

    def _on_volver_click(self, e):
        if self.on_volver:
            self.on_volver()


if __name__ == "__main__":

    def main(page: ft.Page):
        page.title = "Prueba de Crear quiz"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def cerrar_dialogo(e=None):
            page.pop_dialog()
            page.update()

        def guardar_datos():
            print("Datos guardados:")
            cerrar_dialogo()

        # Instanciamos el diálogo
        dlg = DatosQuizView(
            # question_text="¿Cuál es tu lenguaje favorito?",
            on_continuar=guardar_datos,
            on_volver=cerrar_dialogo,
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
