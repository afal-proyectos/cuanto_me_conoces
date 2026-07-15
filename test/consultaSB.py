import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.servicios.supabase_ser import SupabaseService

service = SupabaseService()

quiz = service.crear_quiz("Alejandro", "Quiz de prueba")
print("Quiz creado:", quiz["id"])

preguntas = [
    {
        "order_index": 1,
        "question_text": "¿Mi color favorito?",
        "options": ["Rojo", "Azul", "Verde"],
        "correct_answer": "Azul",
        "points": 10,
    },
]
service.add_preguntas(quiz["id"], preguntas)

datos = service.obtener_quiz_con_preguntas(quiz["id"])
print(datos)
