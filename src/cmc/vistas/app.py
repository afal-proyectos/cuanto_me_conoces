import flet as ft
from models.quiz_model import QuizM
from servicios.bd_local_ser import BDLocal
from vistas.p1_inicio_flet import InicioView
from vistas.p2_crear_quiz import DatosQuizView
from vistas.p3_crear_preguntas import CrearPreguntas
from vistas.p4_crear_opciones import CrearOpciones
from vistas.p5_editar_quiz import EditorQuiz
from vistas.p6_enviar_quiz import Enviar
from vistas.p7_seleccion_quiz import SeleccionQuizView


class App:
    def __init__(self, page: ft.Page):
        self.page = page

        self.bdl = BDLocal()
        self.quizzes_cache = self.bdl.mostrar_quiz_local()  # todos los quiz en local
        self.quiz_seleccionado_id = None
        self._configurar_page()  # titulo, tamaño ventana, padding, mode
        self._crear_views()  # contruir todas las vistas cons sus parametros
        self._mostrar_inicio()  # mostrar la primera vista

    def _configurar_page(self):
        self.page.title = "¿Cuánto me Conoces"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window.width = 350
        self.page.window.height = 685

    # clase + señales (callbacks)
    def _crear_views(self):
        # p1
        self.inicio_view = InicioView(on_nuevo_quiz=self._seleccion_quiz)

        # p7
        self.seleccion_quiz_view = SeleccionQuizView(
            dict_quiz=self.quizzes_cache,
            on_nuevo=self._abrir_crear_quiz,
            on_volver=self._mostrar_inicio,
            on_editar=self._mostrar_editor,
        )

        # p3
        self.crear_preguntas_view = CrearPreguntas(
            on_question_selected=self._abrir_editor_opciones,
            on_finish=self._mostrar_editor,
        )

    # Navegación
    # Seleccionar ventana : parametro, la ventana, limpia, agrega y actualiza
    def _elegir_view(self, view):
        self.page.views.clear()
        self.page.views.append(view)
        self.page.update()

    # invocada la primera vista
    def _mostrar_inicio(self):
        self._elegir_view(self.inicio_view)  # se elije mostrar p1

    # opción de ir a p7
    def _seleccion_quiz(self, e=None):
        self.quizzes_cache = self.bdl.mostrar_quiz_local()
        self._elegir_view(self.seleccion_quiz_view)  # se elije mostrar p7
        self.seleccion_quiz_view.actualizar_datos(
            self.quizzes_cache
        )  # primero elijo la pantalla, luego actuaizo.

    # ir a p7, desde la verntana flotante p2
    def _crear_quiz(self, *args, **kwargs):
        self.page.pop_dialog()
        self.datos_creacion_quiz = kwargs
        q = QuizM()
        datos_entrada = self.datos_creacion_quiz
        q.crear(datos=datos_entrada)

        self.quizzes_cache = q.lista_actual()

        self.seleccion_quiz_view.actualizar_datos(self.quizzes_cache)

    # ir a p5
    def _mostrar_editor(
        self,
        e,
    ):

        self.quiz_seleccionado_id = e.control.data
        quiz_data = self.quizzes_cache.get(self.quiz_seleccionado_id, {})

        # p5
        self.editor_view = EditorQuiz(
            quiz_preguntas=quiz_data,
            on_agregar=None,
            on_editar=self._editar_pregunta,
            on_eliminar_pregunta=self._eliminar_pregunta,
            on_cambiar=self._seleccion_quiz,
            on_eliminar_quiz=None,
            on_terminar=None,
        )

        self._elegir_view(self.editor_view)

    # ir a p4 (flotante):
    def _abrir_editor_opciones(self, pregunta, tipo):
        dialog = CrearOpciones(
            tipo_pregunta=tipo,
            question_text=pregunta,
            on_save=self._save_question,
            on_cancel=lambda: self.page.pop_dialog(),
        )
        self.page.show_dialog(dialog)

    # ir a p2 (flotante)
    def _abrir_crear_quiz(self):
        dialog = DatosQuizView(
            on_continuar=self._crear_quiz,
            on_volver=lambda: self.page.pop_dialog(),
        )

        self.page.show_dialog(dialog)

    # ir a p6 (flotante)
    def _enviar_quiz(self):
        dialog = Enviar(
            advertencia="¡Atención!",
            on_save=self._terminar_quiz,
            on_cancel=lambda: self.page.pop_dialog(),
        )
        self.page.show_dialog(dialog)

    # Acción al enviar el quiz en p6
    def _terminar_quiz(self):
        print("crear quiz")
        self.page.pop_dialog()
        # mandar a la pantalla (aún no creada), de quiz terminados.

    # guardar en p4
    def _save_question(self, **data):
        print(f"Info pregunta:{data}")
        self.page.pop_dialog()
        # agregar función para guardar las preguntas, en el unico quiz editable

    # Acciones de la p5
    # def _cargar_quiz_habilitado(self):
    # print("Ahora estoy pasando por aquí")
    #    if self.id_habilitado:
    #        id = self.id_habilitado
    #        bdl = BDLocal()
    #         return bdl.mostrar_quiz_habilitado(id)
    #    else:
    #        print("Aquí estoy")
    #        return {}

    # abrir la p4, pero con los datos correspondientes
    def _editar_pregunta(self, question_id):
        print(f"Editar {question_id}")

    def _eliminar_pregunta(self, question_id):
        print(f"Eliminar {question_id}")


if __name__ == "__main__":

    def main(page: ft.Page):
        App(page)

    ft.run(main)
