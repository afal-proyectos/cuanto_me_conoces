from src.models.preguntas import Question


def calculate_score(questions: list[Question], respuestas: list[dict]) -> dict:
    """
    Calcula el puntaje total de un jugador.

    questions: lista de objetos Question (ya cargados desde Supabase)
    respuestas:   lista de dicts con la forma
               [{"question_id": "...", "answer": "Azul"}, ...]
               (esto es lo que la vista del jugador junta mientras
               responde, y lo que se guarda tal cual en results.answers)

    Devuelve un dict con el score total y el detalle de cada pregunta,
    util tanto para persistir en Supabase como para mostrarle al
    jugador cuales acerto y cuales no.
    """
    # Indexamos las respuestas por question_id para acceso O(1)
    respuestas_por_pregunta = {a["question_id"]: a["answer"] for a in respuestas}

    detail = []
    total_score = 0

    for question in questions:
        obtener_respuesta = respuestas_por_pregunta.get(question.id)
        correct = question.is_correct(obtener_respuesta)
        points_earned = question.points if correct else 0
        total_score += points_earned

        detail.append(
            {
                "question_id": question.id,
                "given_answer": obtener_respuesta,
                "correct": correct,
                "points_earned": points_earned,
            }
        )

    return {
        "score": total_score,
        "detail": detail,
    }
