import flet as ft

from vistas.p1_inicio_flet import InicioView
from vistas.p2_crear_quiz import DatosQuizView
from vistas.p3_crear_preguntas import CrearPreguntas
from vistas.p5_editar_quiz import QuizEditor
from vistas.p7_seleccion_quiz import SeleccionQuizView

from vistas.p4_crear_opciones import CrearOpciones
from vistas.p6_enviar_quiz import Enviar

# from textos.txt import TextosVistas as tx
from models.quiz_model import QuizM
from servicios.bd_local_ser import BDLocal


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self._configurar_page()  # titulo, tamaño ventana, padding, mode
        self._crear_views()  # contruir todas las vistas cons sus parametros
        self._mostrar_inicio()  # mostrar la primera vista

    def _configurar_page(self):
        self.page.title = "¿Cuánto me Conoces"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window_width = 200
        self.page.window_height = 400

    # clase + señales (callbacks)
    def _crear_views(self):
        # p1
        self.inicio_view = InicioView(
            on_nuevo_quiz=self._seleccion_quiz,
            # on_seguir_editando=self._continuar_editando,
        )
        # p2
        # self.datos_quiz_view = DatosQuizView(
        #    on_continuar=self._crear_preguntas,
        #    on_volver=self._mostrar_inicio,
        # )
        # p7
        self.seleccion_quiz_view = SeleccionQuizView(
            on_nuevo=self._abrir_crear_quiz,
            on_volver=self._mostrar_inicio,
            on_editar=self._mostrar_editor,
            # id_quiz="",
        )

        # p3
        self.crear_preguntas_view = CrearPreguntas(
            on_question_selected=self._abrir_editor_opciones,
            on_finish=self._mostrar_editor,
            # on_back=self._seleccion_quiz,
        )
        # p5
        self.editor_view = QuizEditor(
            on_edit_question=self._edit_question,  # (flotante) es la misma pantalla que _abrir_editor_opciones, pero, con datos ya impresos
            on_delete_question=self._delete_question,  # (accion en la misma pantalla)
            on_enviar_quiz=self._enviar_quiz,  # flotante
            on_back=self._seleccion_quiz,
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
    def _seleccion_quiz(self, e):
        if e.control.data:
            self.id = e.control.data
            bdl = BDLocal()
            bdl.deshabilitar_quiz(self.id)
        self._elegir_view(self.seleccion_quiz_view)  # se elije mostrar p7

    # ir a p3
    def _crear_preguntas(self, *args, **kwargs):
        self.datos_creacion_quiz = kwargs
        q = QuizM()
        datos_entrada = self.datos_creacion_quiz
        print(f"Datos para crear quiz -->{datos_entrada}")
        id = q.crear(datos=datos_entrada)
        print(f"ID Quiz -->{id}")
        self._elegir_view(self.crear_preguntas_view)
        # el id debe ser el unico quiz editable

    # ir a p5
    def _mostrar_editor(self, e):
        self.id = e.control.data
        bdl = BDLocal()
        bdl.habilitar_quiz(
            self.id
        )  # Esta función debe asegurarce de que solo 1 quizz sea "editable"
        self._elegir_view(self.editor_view)
        self.editor_view.add_question(
            question_id=self.id,
            question="¿Cuál es mi color favorito?",
            options=["Azul", "Rojo", "Verde", "Negro"],
            score=10,
        )

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
            on_continuar=self._crear_preguntas, on_volver=lambda: self.page.pop_dialog()
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
    # abrir la p4, pero con los datos correspondientes
    def _edit_question(self, question_id):
        print(f"Editar {question_id}")

    def _delete_question(self, question_id):
        print(f"Eliminar {question_id}")


if __name__ == "__main__":

    def main(page: ft.Page):
        App(page)

    ft.run(main)
