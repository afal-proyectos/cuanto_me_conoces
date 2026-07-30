import uuid

from servicios.bd_local_ser import BDLocal


class QuizM:
    def __init__(self):
        pass

    def ordenar_datos(
        self,
        fecha,
        creador,
        evento,
        estado,
        cantidad,
        preguntas,
    ):
        datos = [
            fecha,
            creador,
            evento,
            estado,
            cantidad,
            preguntas,
        ]
        return datos

    def crear(self, datos: dict):
        id = str(uuid.uuid4())
        datos_ok = datos
        bdl = BDLocal()
        bdl.guardar_quiz_local(id, datos_ok)
        return id

    def actualizar(self, id_quiz: str, nuevos_datos: dict):
        id = id_quiz
        datos = nuevos_datos
        bdl = BDLocal()
        bdl.guardar_quiz_local(id, datos)

    def quiz_ordenados(self):
        bdl = BDLocal()
        quiz = bdl.mostrar_quiz_local()
