class TxtApp:
    def info(self):
        self.app = {"nombre": "¿Cúanto me Conoces?"}
        return self.app

    def preguntas(self):
        self.opciones = {
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

        return self.opciones


if __name__ == "__main__":
    tx = TxtApp()
    print(f"Nombre de al app {tx.info()['nombre']}")
    print(f"Lista de preguntas: {tx.preguntas()['vof']}")
