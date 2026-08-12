import flet as ft
from models.quiz_model import QuizM
from servicios.bd_local_ser import BDLocal
from textos.txt import TxtApp
from vistas.p1_inicio_flet import InicioView
from vistas.p2_crear_quiz import DatosQuizView
from vistas.p3_crear_preguntas import CrearPreguntas
from vistas.p4_crear_opciones import CrearOpciones
from vistas.p5_editar_quiz import EditorQuiz
from vistas.p6_enviar_quiz import Enviar
from vistas.p7_seleccion_quiz import SeleccionQuizView
from vistas.p8_quiz_terminados import QuizTerminados


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tx = TxtApp()
        self.bdl = BDLocal()
        self.q = QuizM()
        self.quizzes_cache = self.bdl.mostrar_quiz_local()  # todos los quiz en local
        self.quiz_seleccionado_id = None
        self._configurar_page()  # titulo, tamaño ventana, padding, mode
        self._crear_views()  # contruir todas las vistas cons sus parametros
        self._mostrar_inicio()  # mostrar la primera vista

    def _configurar_page(self):
        self.page.title = self.tx.info()["nombre"]
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window.width = 350
        self.page.window.height = 685

    # clase + señales (callbacks)
    def _crear_views(self):
        # p1
        self.inicio_view = InicioView(
            on_nuevo_quiz=self._seleccion_quiz,
            on_quiz_terminados=self._abrir_quiz_terminados_view,
            on_ver_ranking=None,
            textos=self.tx.info(),
        )

        # p7
        self.seleccion_quiz_view = SeleccionQuizView(
            dict_quiz=self.quizzes_cache,
            on_nuevo=self._abrir_crear_quiz,
            on_volver=self._mostrar_inicio,
            on_editar=self._abrir_editor,
        )

        # p3
        self.crear_preguntas_view = CrearPreguntas(
            tex_pregunta=self.tx.preguntas(),
            on_selec_pregunta=self._abrir_editor_opciones,
            on_regresar=self._abrir_editor,
        )
        # p8
        self.quiz_terminados = QuizTerminados(
            on_comenzar=None,
            on_regresar=self._mostrar_inicio,
            on_revisar=None,
            on_seguir_editando=None,
            quiz_terminados=self._quiz_terminados(),
        )
        # p4 — una sola instancia reutilizada para crear y editar preguntas
        self.dialog_opciones = CrearOpciones(
            on_save=self._save_question,
            on_cancel=lambda: self.page.pop_dialog(),
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
        self._elegir_view(self.seleccion_quiz_view)
        self.seleccion_quiz_view.actualizar_datos(self.quizzes_cache)

    # ir a p7, desde la verntana flotante p2
    def _crear_quiz(self, *args, **kwargs):
        self.page.pop_dialog()
        datos_entrada = kwargs
        self.q.crear(datos=datos_entrada)
        self.quizzes_cache = self.bdl.mostrar_quiz_local()
        # self.quizzes_cache = self.q.lista_actual()
        self.seleccion_quiz_view.actualizar_datos(self.quizzes_cache)

    # ir a p5
    def _abrir_editor(self, e=None):
        if e is not None and getattr(e.control, "data", None):
            self.quiz_seleccionado_id = e.control.data

        self.quizzes_cache = (
            self.bdl.mostrar_quiz_local()
        )  # refrescar la cacche con nuevos datos en local
        quiz_data = self.quizzes_cache.get(self.quiz_seleccionado_id, {})

        self.editor_view = EditorQuiz(
            quiz_preguntas=quiz_data,
            on_agregar=self._arbir_crear_preguntas_view,
            on_editar=self._editar_pregunta,
            on_eliminar_pregunta=self._eliminar_pregunta,
            on_cambiar=self._seleccion_quiz,
            on_eliminar_quiz=self._eliminar_quiz,
            on_terminar=self._enviar_quiz,
        )

        self._elegir_view(self.editor_view)

    # ir a p3
    def _arbir_crear_preguntas_view(self):
        self._elegir_view(self.crear_preguntas_view)

    # ir a p8 (quiz terminados)
    def _abrir_quiz_terminados_view(self):
        self._elegir_view(self.quiz_terminados)

    # ir a p4 (flotante):
    def _abrir_editor_opciones(self, pregunta, tipo):
        self.dialog_opciones.configurar(
            tipo_pregunta=tipo,
            pregunta_text=pregunta,
            # on_save=self._save_question,
            # on_cancel=lambda: self.page.pop_dialog(),
            id_pregunta=None,
            valores_iniciales=None,
        )
        self.page.show_dialog(self.dialog_opciones)

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
        self.page.pop_dialog()
        print("Quiz terminado")
        self.q.guardar_quiz_terminado(idq=self.quiz_seleccionado_id)
        self._elegir_view(self.inicio_view)

    # guardar en p4
    def _save_question(self, **data):
        id_pregunta = data.pop("id_pregunta", None)
        self.page.pop_dialog()
        self.page.update()
        if id_pregunta:
            print("Guardar pregunta con id...")
            self.q.actualizar_pregunta(self.quiz_seleccionado_id, id_pregunta, data)
            self.quizzes_cache = self.q.lista_actual()
            # time.sleep(0.9)
            self.editor_view.update()
            self._abrir_editor()  # refresca p5 con los datos ya editados

        else:
            self.q.ordenar(self.quiz_seleccionado_id, data)
            self.quizzes_cache = self.q.lista_actual()

    # abrir la p4, pero con los datos correspondientes
    def _editar_pregunta(self, question_id):
        quiz = self.quizzes_cache.get(self.quiz_seleccionado_id, {})
        preguntas = quiz.get("data_preguntas", [])
        pregunta_data = next(
            (p for p in preguntas if p["id_pregunta"] == question_id), None
        )
        if not pregunta_data:
            return

        self.dialog_opciones.configurar(
            tipo_pregunta=pregunta_data.get("tipo"),
            pregunta_text=pregunta_data.get("pregunta"),
            id_pregunta=question_id,
            valores_iniciales=pregunta_data,
            # on_save=self._save_question,
            # on_cancel=lambda: self.page.pop_dialog(),
        )
        self.page.show_dialog(self.dialog_opciones)

    def _eliminar_pregunta(self, question_id):
        self.q.eliminar_pregunta(self.quiz_seleccionado_id, question_id)
        self.quizzes_cache = self.q.lista_actual()
        # se abre, aunque estemos en la mima pantalla, para recargarla con info actualizada
        self._abrir_editor()

    def _eliminar_quiz(self):
        if not self.quiz_seleccionado_id:
            return
        self.q.eliminar_quiz(self.quiz_seleccionado_id)
        self.quiz_seleccionado_id = None  # actualiza la memoria volatil del programa
        self.quizzes_cache = self.q.lista_actual()
        # abrimos una pantalla para no quedar en la "nada"
        self._seleccion_quiz()

    def _quiz_terminados(self):
        lista_quiz_terminados = {}
        lista_quiz_terminados = self.bdl.mostrar_quiz_terminados()
        return lista_quiz_terminados


if __name__ == "__main__":

    def main(page: ft.Page):
        App(page)

    ft.run(main)
