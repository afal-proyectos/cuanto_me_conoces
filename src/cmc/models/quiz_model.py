import uuid

from servicios.bd_local_ser import BDLocal


class QuizM:
    def __init__(self):

        self.bdl = BDLocal()

    def crear(self, datos: dict):
        id = str(uuid.uuid4())
        datos_ok = datos
        self.bdl.guardar_quiz_local(id, datos_ok)
        return id

    def actualizar(self, id_quiz: str, nuevos_datos: dict):
        id = id_quiz
        datos = nuevos_datos
        self.bdl.guardar_quiz_local(id, datos)

    def lista_actual(self):
        lista = self.bdl.mostrar_quiz_local()
        return lista
