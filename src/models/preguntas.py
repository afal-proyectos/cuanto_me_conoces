class Question:
    """
    Representa una sola pregunta del quiz.
    Se crea a partir de los datos individuales o desde una fila de Supabase.
    """

    def __init__(
        self,
        id,
        order_index,
        question_text,
        options,
        correct_answer,
        points=10,
    ):
        self.id = id
        self.order_index = order_index
        self.question_text = question_text
        self.options = options  # Una lista de strings, ej: ["Azul", "Rojo", "Verde"]
        self.correct_answer = correct_answer
        self.points = points

    @classmethod
    def from_row(cls, row):
        """
        Toma un diccionario (fila de Supabase) y crea un objeto Question.
        Ejemplo de uso: nueva_pregunta = Question.from_row(fila_supabase)
        """
        return cls(
            id_pregunta=row["id"],
            order_index=row["order_index"],
            question_text=row["question_text"],
            options=row["options"],
            correct_answer=row["correct_answer"],
            points=row.get(
                "points", 10
            ),  # Si no hay puntos en la BD, por defecto es 10
        )

    def is_correct(self, given_answer):
        """
        Compara la respuesta que dio el jugador con la respuesta correcta.
        """
        if given_answer is None:
            return False

        # .strip() quita espacios al inicio y final. .lower() lo pasa todo a minúsculas.
        # Así evitamos que "Azul " y "azul" se consideren diferentes.
        respuesta_limpia = given_answer.strip().lower()
        correcta_limpia = self.correct_answer.strip().lower()

        return respuesta_limpia == correcta_limpia


class Quiz:
    """
    Representa el cuestionario completo.
    Contiene la información del creador y la lista de preguntas asociadas.
    """

    def __init__(self, id_quiz, creator_name, title, status, questions=None):
        self.id = id_quiz
        self.creator_name = creator_name
        self.title = title
        self.status = status

        # Si no nos pasan preguntas al crear el Quiz, iniciamos con una lista vacía
        if questions is None:
            self.questions = []
        else:
            self.questions = questions

    @classmethod
    def from_service_data(cls, data):
        """
        Toma el diccionario combinado de Supabase y construye el Quiz con sus preguntas.
        """
        # Obtenemos los datos básicos del quiz
        quiz_row = data["quiz"]

        # Traducimos la lista de diccionarios de preguntas a objetos Question reales
        lista_preguntas_objetos = []
        for q in data["questions"]:
            objeto_pregunta = Question.from_row(q)
            lista_preguntas_objetos.append(objeto_pregunta)

        # Retornamos el objeto Quiz construido
        return cls(
            id_quiz=quiz_row["id"],
            creator_name=quiz_row["creator_name"],
            title=quiz_row["title"],
            status=quiz_row["status"],
            questions=lista_preguntas_objetos,
        )
