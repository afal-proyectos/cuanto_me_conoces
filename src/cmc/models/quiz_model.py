import uuid

from servicios.bd_local_ser import BDLocal


class QuizM:
    def __init__(self):
        self.bdl = BDLocal()

    def ordenar(self, idq, datos):
        id = str(uuid.uuid4())
        opciones_ok = {
            1: datos["option1"],
            2: datos["option2"],
            3: datos["option3"],
            4: datos["option4"],
        }
        puntajes_ok = {
            1: datos["score1"],
            2: datos["score2"],
            3: datos["score3"],
            4: datos["score4"],
        }
        pregunta_ok = {
            "id_pregunta": id,
            "tipo": datos["tipo"],
            "pregunta": datos["pregunta"],
            "opciones": opciones_ok,
            "puntaje": puntajes_ok,
        }

        id = idq
        self.bdl.agregar_pregunta(id, pregunta_ok)

    def crear(self, datos: dict):
        id = str(uuid.uuid4())
        datos_ok = dict(datos)
        datos_ok["data_preguntas"] = []
        self.bdl.guardar_quiz_local(id, datos_ok)
        return id

    def actualizar(self, id_quiz: str, nuevos_datos: dict):
        id = id_quiz
        datos = nuevos_datos
        self.bdl.guardar_quiz_local(id, datos)

    def lista_actual(self):
        lista = self.bdl.mostrar_quiz_local()
        return lista

    def eliminar_pregunta(self, id_quiz, id_pregunta):
        self.bdl.eliminar_pregunta(id_quiz, id_pregunta)

    def eliminar_quiz(self, id_quiz):
        self.bdl.eliminar_quiz(id_quiz)

    def actualizar_pregunta(self, idq, id_pregunta, datos):
        opciones_ok = {
            1: datos["option1"],
            2: datos["option2"],
            3: datos["option3"],
            4: datos["option4"],
        }
        puntajes_ok = {
            1: datos["score1"],
            2: datos["score2"],
            3: datos["score3"],
            4: datos["score4"],
        }
        pregunta_ok = {
            "id_pregunta": id_pregunta,
            "tipo": datos["tipo"],
            "pregunta": datos["pregunta"],
            "opciones": opciones_ok,
            "puntaje": puntajes_ok,
        }
        self.bdl.actualizar_pregunta(idq, id_pregunta, pregunta_ok)


if __name__ == "__main__":
    QuizM.ordenar()
