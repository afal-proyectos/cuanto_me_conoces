import json
import os
from pathlib import Path


class BDLocal:
    def __init__(self):
        # Ruta base: carpeta raíz del proyecto
        self.base_dir = Path(__file__).resolve().parents[3]
        # → sube dos niveles desde bd_local_ser.py hasta cuanto_me_conoces/

        # Ruta al archivo JSON
        self.local = self.base_dir / "data_local" / "quiz.json"

    def guardar_quiz_local(self, id_quiz_actual: str, quiz_actual: dict):
        self.id = id_quiz_actual
        self.quiz = quiz_actual

        quiz_local = {}

        if os.path.exists(self.local):
            # self.local.parent.mkdir(parents=True, exist_ok=True)

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


if __name__ == "__main__":
    bdl = BDLocal()
    # print(f"ruta:{bdl.local}")
    # bdl.guardar_quiz_local("2", ("hola", "chao"))
    bdl.mostrar_quiz_local()
