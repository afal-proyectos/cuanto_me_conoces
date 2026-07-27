import flet as ft

from vistas.p1_inicio_flet import InicioView
from vistas.p2_craer_quiz import DatosQuizView
from vistas.p3_crear_preguntas import CrearPreguntas
from vistas.p5_editar_quiz import QuizEditor

from vistas.p4_crear_opciones import CrearOpciones
from vistas.p6_enviar_quiz import Enviar
# from textos.txt import TextosVistas as tx


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self._configurar_page()  # titulo, tamaño ventana, padding, mode
        self._crear_views()  # contruir todas las vistas cons sus parametros
        self._mostrar_inicio()  # mostrar la primera vista

    # =====================================================
    # Configuración
    # =====================================================

    def _configurar_page(self):
        self.page.title = "¿Cuánto me Conoces"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window_width = 400
        self.page.window_height = 800

    # =====================================================
    # Crear vistas
    # =====================================================
    # clase + señales (callbacks)
    def _crear_views(self):
        # p1
        self.inicio_view = InicioView(
            on_nuevo_quiz=self._datos_quiz,
            on_seguir_editando=self._continuar_editando,
        )
        # p2
        self.datos_quiz_view = DatosQuizView(
            on_continuar=self._crear_preguntas,
            on_volver=self._mostrar_inicio,
        )
        # p3
        self.crear_preguntas_view = CrearPreguntas(
            on_question_selected=self._abrir_editor_opciones,
            on_finish=self._mostrar_editor,
            on_back=self._datos_quiz,
        )
        # p5
        self.editor_view = QuizEditor(
            on_edit_question=self._edit_question,  # es la misma pantalla que _abrir_editor_opciones, pero, con datos ya impresos
            on_delete_question=self._delete_question,
            on_enviar_quiz=self._enviar_quiz,
            on_back=self._crear_preguntas,
        )

    # Navegación
    # Seleccionar ventana : parametro, la ventana, limpia, agrega y actualiza
    def _elegir_view(self, view):
        self.page.views.clear()
        self.page.views.append(view)
        self.page.update()

    # invocada al iniciar el programa (lo primero que se ve)
    def _mostrar_inicio(self):
        self._elegir_view(self.inicio_view)  # se elije mostrar p1

    # opción de ir a p2
    def _datos_quiz(self):
        self._elegir_view(self.datos_quiz_view)  # se elije mostrar p2

    # ir a p3
    def _crear_preguntas(self, *args, **kwargs):
        self._elegir_view(self.crear_preguntas_view)

    # ir a p5
    def _mostrar_editor(self):
        self._elegir_view(self.editor_view)

    # ir a p4 : necesitamos más información en los parametros
    def _abrir_editor_opciones(self, question_id):
        dialog = CrearOpciones(
            question_text=f"Pregunta {question_id}",
            on_save=self._save_question,
            on_cancel=lambda: self.page.pop_dialog(),
        )
        self.page.show_dialog(dialog)

    # ir a p6
    def _enviar_quiz(
        self,
    ):
        dialog = Enviar(
            question_text="¡Atención!",
            on_save=self._crear_quiz,
            on_cancel=lambda: self.page.pop_dialog(),
        )
        self.page.show_dialog(dialog)

    # =====================================================
    # Eventos temporales
    # =====================================================
    # Acción al enviar el quiz en p6
    def _crear_quiz(self):
        print("crear quiz")
        print("")
        self.page.pop_dialog()

    # guardar en p4
    def _save_question(self, **data):
        print("Guardar pregunta")
        print(data)
        self.page.pop_dialog()

    # abrir la p4, pero con los datos correspondientes
    def _edit_question(self, question_id):
        print(f"Editar {question_id}")

    # -----------------------------------------------------
    def _delete_question(self, question_id):
        print(f"Eliminar {question_id}")

    # vista aún no contruida, te debe mandar a los quizz guardados en local que aún no se terminan
    def _continuar_editando(self):
        print("Continuar edición")


if __name__ == "__main__":

    def main(page: ft.Page):
        App(page)

    ft.run(main)
