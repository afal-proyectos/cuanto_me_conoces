import json
import os
from pathlib import Path


class BDLocal:
    def __init__(self):
        # Ruta base: carpeta raíz del proyecto
        self.base_dir = Path(__file__).resolve().parents[3]

        self.local = self.base_dir / "data_local" / "quiz.json"

    def guardar_quiz_local(self, id_quiz_actual: str, quiz_actual: dict):
        self.id = id_quiz_actual
        self.quiz = quiz_actual
        quiz_local = {}

        if os.path.exists(self.local):
            try:
                with open(self.local, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()
                    if contenido:
                        quiz_local = json.loads(contenido)
            except FileNotFoundError as e:
                print(f"Error al obtener quizz: {e}")

        quiz_local[self.id] = self.quiz

        try:
            with open(self.local, "w", encoding="utf-8") as archivo:
                json.dump(quiz_local, archivo, indent=4, ensure_ascii=False)
        except FileNotFoundError as e:
            print(f"Error al guardar el Quiz: {e}")

    def mostrar_quiz_local(self):
        try:
            with open(self.local, "r", encoding="utf-8") as archivo:
                quiz_local = json.load(archivo)
        except FileNotFoundError:
            print("No hay datos guardados")

        return quiz_local

    def mostrar_quiz_habilitado(self, id):
        if id:
            try:
                with open(self.local, "r", encoding="utf-8") as archivo:
                    quiz_local = json.load(archivo)
            except FileNotFoundError:
                print("No hay datos guardados")

            return quiz_local[id]

    def agregar_pregunta(self, id, pregunta):
        quiz_local = {}
        try:
            with open(self.local, "r", encoding="utf-8") as archivo:
                quiz_local = json.load(archivo)
        except FileNotFoundError:
            print("No hay datos guardados")

        quiz_actualizar = quiz_local.get(id)
        preguntas_lista = quiz_actualizar.get(
            "data_preguntas", []
        )  # pregunta_data es una lista
        preguntas_lista.append(pregunta)  # la lista con preguntas se actualiza
        quiz_actualizar["data_preguntas"] = preguntas_lista
        quiz_local[id] = quiz_actualizar

        try:
            with open(self.local, "w", encoding="utf-8") as archivo:
                json.dump(quiz_local, archivo, indent=4, ensure_ascii=False)
        except FileNotFoundError as e:
            print(f"Error al guardar el Quiz: {e}")
        print(f"Quiz {id} -->Actualizado con la ultima pregunta")

    def eliminar_pregunta(self, id_quiz, id_pregunta):
        try:
            with open(self.local, "r", encoding="utf-8") as archivo:
                quiz_local = json.load(archivo)
        except FileNotFoundError:
            print("No hay datos guardados")
            return

        quiz = quiz_local.get(id_quiz)
        if not quiz:
            return

        preguntas = quiz.get("data_preguntas", [])
        quiz["data_preguntas"] = [
            p for p in preguntas if p["id_pregunta"] != id_pregunta
        ]

        try:
            with open(self.local, "w", encoding="utf-8") as archivo:
                json.dump(quiz_local, archivo, indent=4, ensure_ascii=False)
        except FileNotFoundError as e:
            print(f"Error al guardar el Quiz: {e}")

    def eliminar_quiz(self, id_quiz):
        try:
            with open(self.local, "r", encoding="utf-8") as archivo:
                quiz_local = json.load(archivo)
        except FileNotFoundError:
            print("No hay datos guardados")
            return

        quiz_local.pop(id_quiz, None)

        try:
            with open(self.local, "w", encoding="utf-8") as archivo:
                json.dump(quiz_local, archivo, indent=4, ensure_ascii=False)
        except FileNotFoundError as e:
            print(f"Error al guardar el Quiz: {e}")

    def actualizar_pregunta(self, id_quiz, id_pregunta, pregunta_actualizada):
        try:
            with open(self.local, "r", encoding="utf-8") as archivo:
                quiz_local = json.load(archivo)
        except FileNotFoundError:
            print("No hay datos guardados")
            return

        quiz = quiz_local.get(id_quiz)
        if not quiz:
            return

        preguntas = quiz.get("data_preguntas", [])
        for i, p in enumerate(preguntas):
            if p["id_pregunta"] == id_pregunta:
                preguntas[i] = pregunta_actualizada  # reemplaza manteniendo la posición
                break

        try:
            with open(self.local, "w", encoding="utf-8") as archivo:
                json.dump(quiz_local, archivo, indent=4, ensure_ascii=False)
        except FileNotFoundError as e:
            print(f"Error al guardar el Quiz: {e}")


if __name__ == "__main__":
    bdl = BDLocal()

    bdl.mostrar_quiz_local()
