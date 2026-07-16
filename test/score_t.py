import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.preguntas import Question
from src.servicios.puntos_ser import calculate_score


def _preguntas_de_prueba() -> list[Question]:
    return [
        Question(
            id="q1",
            order_index=1,
            question_text="¿Mi color favorito?",
            options=["Rojo", "Azul", "Verde"],
            correct_answer="Azul",
            points=10,
        ),
        Question(
            id="q2",
            order_index=2,
            question_text="¿Mi comida favorita?",
            options=["Pizza", "Sushi", "Tacos"],
            correct_answer="Sushi",
            points=10,
        ),
    ]


def test_todas_correctas():
    preguntas = _preguntas_de_prueba()
    respuestas = [
        {"question_id": "q1", "answer": "Azul"},
        {"question_id": "q2", "answer": "Sushi"},
    ]
    resultado = calculate_score(preguntas, respuestas)
    assert resultado["score"] == 20


def test_una_incorrecta():
    preguntas = _preguntas_de_prueba()
    respuestas = [
        {"question_id": "q1", "answer": "Rojo"},  # incorrecta
        {"question_id": "q2", "answer": "Sushi"},  # correcta
    ]
    resultado = calculate_score(preguntas, respuestas)
    assert resultado["score"] == 10
    assert resultado["detail"][0]["correct"] is False
    assert resultado["detail"][1]["correct"] is True


def test_respuesta_no_enviada():
    """Simula que el jugador no alcanzo a responder una pregunta
    (por ejemplo, se acabo el tiempo)."""
    preguntas = _preguntas_de_prueba()
    respuestas = [
        {"question_id": "q1", "answer": "Azul"},
        # q2 no aparece en la lista de respuestas
    ]
    resultado = calculate_score(preguntas, respuestas)
    assert resultado["score"] == 10


def test_case_insensitive_y_espacios():
    """La comparacion no deberia ser quisquillosa con mayusculas
    o espacios accidentales."""
    preguntas = _preguntas_de_prueba()
    respuestas = [
        {"question_id": "q1", "answer": "  azul  "},
        {"question_id": "q2", "answer": "sushi"},
    ]
    resultado = calculate_score(preguntas, respuestas)
    assert resultado["score"] == 20


if __name__ == "__main__":
    print("Iniciando pruebas unitarias de la lógica de puntuación...")
    print("-" * 50)

    test_todas_correctas()
    test_una_incorrecta()
    test_respuesta_no_enviada()
    test_case_insensitive_y_espacios()

    print("-" * 50)
    print("¡Felicidades! Todos los tests pasaron correctamente.")
