import flet as ft


class CrearOpciones(ft.AlertDialog):
    def __init__(
        self,
        # tipo_pregunta=None,
        # pregunta_text=None,
        # id_pregunta=None,  # None = pregunta nueva; con valor = se está editando
        # valores_iniciales=None,  # dict -> "opciones" : "puntaje", solo si se edita
        on_save=None,
        on_cancel=None,
    ):
        super().__init__(
            modal=True,
        )
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.tipo = None
        self.pregunta = None
        self.id_pregunta = None
        # dic vacio en caso que sea una pregunta nueva
        self.valores_iniciales = {}
        self._crear_controles()
        self.content = self._crear_vista()

    def _valor_opcion(self, n):
        return self.valores_iniciales.get("opciones", {}).get(str(n), "")

    def _valor_puntaje(self, n):
        return str(self.valores_iniciales.get("puntaje", {}).get(str(n), 0))

    def _subtitulos(self, t):
        if t == "multiple":
            return "Selección Múltiple\n"

    def _crear_controles(self):
        self.title = ft.Text(
            self.pregunta,
            size=20,
            align=ft.Alignment.CENTER,
            weight=ft.FontWeight.BOLD,
            theme_style=ft.TextStyle(color=ft.Colors.BLACK),
        )
        self.sub_title = ft.Text(self._subtitulos(self.tipo), align=ft.Alignment.CENTER)

        self.txt_option1 = ft.TextField(
            expand=True, label="Opción 1", value=self._valor_opcion(1)
        )
        self.txt_option2 = ft.TextField(
            expand=True, label="Opción 2", value=self._valor_opcion(2)
        )
        self.txt_option3 = ft.TextField(
            expand=True, label="Opción 3", value=self._valor_opcion(3)
        )
        self.txt_option4 = ft.TextField(
            expand=True, label="Opción 4", value=self._valor_opcion(4)
        )

        self.score1 = ft.Dropdown(
            label="Puntos",
            expand=True,
            value=self._valor_puntaje(1),
            options=[ft.dropdown.Option(str(i)) for i in range(-5, 6)],
        )
        self.score2 = ft.Dropdown(
            label="Puntos",
            expand=True,
            value=self._valor_puntaje(2),
            options=[ft.dropdown.Option(str(i)) for i in range(-5, 6)],
        )
        self.score3 = ft.Dropdown(
            label="Puntos",
            expand=True,
            value=self._valor_puntaje(3),
            options=[ft.dropdown.Option(str(i)) for i in range(-5, 6)],
        )
        self.score4 = ft.Dropdown(
            label="Puntos",
            expand=True,
            value=self._valor_puntaje(4),
            options=[ft.dropdown.Option(str(i)) for i in range(-5, 6)],
        )

        self.btn_save = ft.Button(
            "Listar",
            expand=True,
            on_click=self._on_save_click,
        )

        self.btn_cancel = ft.Button(
            "Volver",
            expand=True,
            on_click=self._on_cancel_click,
        )

    def _crear_vista(self):
        return ft.Column(
            tight=True,
            expand=True,
            controls=[
                self.sub_title,
                ft.Row(controls=[self.txt_option1, self.score1]),
                ft.Row(controls=[self.txt_option2, self.score2]),
                ft.Row(controls=[self.txt_option3, self.score3]),
                ft.Row(controls=[self.txt_option4, self.score4]),
                ft.Divider(),
                ft.Row(controls=[self.btn_cancel, self.btn_save]),
            ],
        )

    def configurar(
        self, tipo_pregunta, pregunta_text, id_pregunta=None, valores_iniciales=None
    ):
        self.tipo = tipo_pregunta
        self.pregunta = pregunta_text
        self.id_pregunta = id_pregunta
        valores = valores_iniciales or {}

        self.title.value = pregunta_text
        self.sub_title.value = self._subtitulos(tipo_pregunta)

        self.load_question(
            option1=valores.get("opciones", {}).get("1", ""),
            option2=valores.get("opciones", {}).get("2", ""),
            option3=valores.get("opciones", {}).get("3", ""),
            option4=valores.get("opciones", {}).get("4", ""),
            score1=valores.get("puntaje", {}).get("1", 0),
            score2=valores.get("puntaje", {}).get("2", 0),
            score3=valores.get("puntaje", {}).get("3", 0),
            score4=valores.get("puntaje", {}).get("4", 0),
        )

    def _update_seguro(self):
        try:
            if self.page:
                self.update()
        except RuntimeError:
            pass

    def clear(self):

        self.txt_option1.value = ""
        self.txt_option2.value = ""
        self.txt_option3.value = ""
        self.txt_option4.value = ""
        self.score1.value = "0"
        self.score2.value = "0"
        self.score3.value = "0"
        self.score4.value = "0"

        self._update_seguro()

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

        self._update_seguro()

    def _on_save_click(self, e):
        if self.on_save:
            self.on_save(
                id_pregunta=self.id_pregunta,
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
            tipo_pregunta="multiple",
            pregunta_text="¿Cuál es tu lenguaje favorito?",
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
