import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


class SupabaseService:
    """
    Capa de acceso a datos (Repository/CRUD) para la v1.
    Todos los metodos son sincronos y devuelven estructuras
    simples (dict / list[dict]) listas para usar en models/servicios.
    """

    def __init__(self):
        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_ANON_KEY"]
        self.client: Client = create_client(url, key)

    # ------------------------------------------------------------------
    # CREADOR: crear quiz
    # ------------------------------------------------------------------
    def crear_quiz(self, creator_name: str, title: str) -> dict:
        """
        Paso 1 de 2. Crea el registro del quiz y devuelve la fila completa
        (incluye el id/uuid recien generado, necesario para el paso 2
        y para codificar el QR).
        """
        # Preparar los datos del quiz
        info_obtenida = {
            "creator_name": creator_name,
            "title": title,
        }

        # agregar el quiz a la tabla quizzes y ejecutar la consultaSQL
        insert_quizz = self.client.table("quizzes").insert(info_obtenida).execute()
        return insert_quizz.data[0]

    # ------------------------------------------------------------------
    # CREADOR: agregar preguntas a un quiz ya creado
    # ------------------------------------------------------------------
    def add_preguntas(self, quiz_id: str, questions: list[dict]) -> list[dict]:
        """
        Paso 2 de 2. Recibe una lista de preguntas ya con la forma de la
        tabla, por ejemplo:

        [
            {
                "order_index": 1,
                "question_text": "¿Cual es mi color favorito?",
                "options": ["Rojo", "Azul", "Verde"],
                "correct_answer": "Azul",
                "points": 10,
            },
            ...
        ]

        Se les inyecta el quiz_id y se insertan todas en una sola llamada.
        """
        info_obtenida = []
        # question es un diccionario, se hace una copia de cada pregunta y se le agrega el quiz_id
        # el diccionario, asocia los atributos de la tabla "preguntas"(keys), con sus valores(values)
        # cada pregunta tiene el id del quiz al que pertenece, para poder relacionarlas
        for q in questions:
            q_copy = dict(q)
            q_copy["quiz_id"] = quiz_id
            info_obtenida.append(q_copy)

        insert_preguntas = (
            self.client.table("questions").insert(info_obtenida).execute()
        )
        return insert_preguntas.data

    # ------------------------------------------------------------------
    # JUGADOR: cargar quiz + preguntas para responder
    # ------------------------------------------------------------------
    def obtener_quiz_con_preguntas(self, quiz_id: str) -> dict:
        """
        Usado por la vista del jugador despues de escanear/tipear el QR.
        Devuelve un dict con el quiz y su lista de preguntas ordenadas.
        """
        # obtener el quizz
        quiz_response = (
            self.client.table("quizzes")
            .select("*")
            .eq("id", quiz_id)
            .single()
            .execute()
        )
        # obtener las preguntas del quiz, filtrando por quiz_id y ordenando por order_index
        questions_response = (
            self.client.table("questions")
            .select("*")
            .eq("quiz_id", quiz_id)  # filtro
            .order("order_index")  # ordenamiento
            .execute()
        )
        # diccionario {"quiz": "questions"}
        return {
            "quiz": quiz_response.data,
            "questions": questions_response.data,
        }

    # ------------------------------------------------------------------
    # JUGADOR: registrarse en el quiz (antes de responder)
    # ------------------------------------------------------------------
    def registrar_jugador(self, quiz_id: str, player_name: str) -> dict:
        info_obtenida = {
            "quiz_id": quiz_id,
            "player_name": player_name,
        }
        insert_registro = self.client.table("players").insert(info_obtenida).execute()
        return insert_registro.data[0]

    # ------------------------------------------------------------------
    # JUGADOR: enviar resultado ya calculado (el calculo de score
    # vive en servicios/puntos_s.py, este metodo solo persiste)
    # ------------------------------------------------------------------
    def enviar_resultado(
        self, player_id: str, quiz_id: str, answers: list[dict], score: int
    ) -> dict:
        info_enviada = {
            "player_id": player_id,
            "quiz_id": quiz_id,
            "answers": answers,
            "score": score,
        }
        insert_resultado = self.client.table("results").insert(info_enviada).execute()
        return insert_resultado.data[0]

    # ------------------------------------------------------------------
    # CREADOR: obtener ranking de un quiz
    # ------------------------------------------------------------------
    def obtener_ranking(self, quiz_id: str) -> list[dict]:
        """
        v1: sin Realtime, se llama manualmente (boton "Ver ranking"
        o polling simple). Devuelve resultados ordenados de mayor a
        menor score. No trae el nombre del jugador directamente
        (results no lo tiene), eso se resuelve en la capa de servicio
        o con un join manual si prefieres mas adelante.
        """
        consulta_ranking = (
            self.client.table("results")
            .select("*")
            .eq("quiz_id", quiz_id)
            .order("score", desc=True)
            .execute()
        )
        return consulta_ranking.data
