class TxInfoApp:
    nombre_app = "¿Cúanto Me conoces?"


class TxPreguntas:
    opciones = {
        "multiple": [
            "¿Cuál es mi color favorito?",
            "¿Cuál es mi lugar favorito?",
            "¿Cuál es mi pelicula favorita?",
            "¿Cuál es mi comida favorita?",
            "¿Cuál es mi superhéroe favorito?",
        ],
        "vof": [
            "Amo a los animales",
            "Me encantaría vivir en el campo",
            "Mi comida favorita es la pizza",
        ],
    }

    """

    class PreguntasQuiz:
        def __init__(self):
            self.nombre = ""
            self.preguntas_list = []

    class SM(PreguntasQuiz):
        def __init__(self):
            super().__init__()
            self.tipo = "Multiple"
            self.preguntas_list = [
                "¿Cuál es mi color favorito?",
                "¿Cuál es mi lugar favorito?",
                "¿Cuál es mi pelicula favorita?",
                "¿Cuál es mi comida favorita?",
                "¿Cuál es mi supehéroe favorito?",
            ]

    class Vof(PreguntasQuiz):
        def __init__(self):
            super().__init__()
            self.tipo = "VoF"
            self.preguntas_list = [
                "Amo a los animales",
                "Me encantaría vivir en el campo",
                "Mi comida favorita es la pizza",
            ]


if __name__ == "__main__":
    ej = TextosApp.SM()
    print(f"tipo: {ej.tipo}")
    print(f"Lista de preguntas {ej.preguntas_list}")
"""
