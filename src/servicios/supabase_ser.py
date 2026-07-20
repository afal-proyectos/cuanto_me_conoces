import os
from dotenv import load_dotenv
from supabase import create_client, Client


class SupabaseServicio:
    load_dotenv()
    """
    Capa de acceso a datos (Repository/CRUD) para la v1.
    Todos los metodos son sincronos y devuelven estructuras
    simples (dict / list[dict]) listas para usar en models/servicios.
    """

    def __init__(self):
        self.url: str = os.getenv("SUPABASE_URL")
        self.key: str = os.getenv("SUPABASE_ANON_KEY")
        self.client: Client = create_client(self.url, self.key)

    # ------------------------------------------------------------------
    # Métodos de la tabla quizz
    # ------------------------------------------------------------------
    def crear_quizz(
        self, id_quizz: str, id_creador: int, id_evento: int, total_preguntas: int
    ):
        """Inserta un nuevo Quizz en la base de datos."""
        try:
            datos = {
                "id_quizz": id_quizz,
                "id_creador": id_creador,
                "id_evento": id_evento,
                "total_preguntas": total_preguntas,
                # 'hora_creacion' la puedes manejar desde Python o dejar que Supabase la ponga con now() si lo configuraste así.
                # 'estado' y 'completado' toman sus valores por defecto automáticamente.
            }
            respuesta = self.client.table("Quizz").insert(datos).execute()
            return respuesta.data
        except Exception as e:
            print(f"Error al crear quizz: {e}")
            return None

    def obtener_quizz(self, id_quizz: str):
        """Consulta y devuelve los datos de un quizz específico."""
        try:
            respuesta = (
                self.client.table("Quizz")
                .select("*")
                .eq("id_quizz", id_quizz)
                .execute()
            )
            # Retorna el primer resultado si existe, o None si no encuentra nada
            return respuesta.data[0] if respuesta.data else None
        except Exception as e:
            print(f"Error al obtener quizz: {e}")
            return None

    def actualizar_estado_quizz(self, id_quizz: str, estado: bool, completado: bool):
        """Permite editar el estado del juego (por ejemplo, cerrarlo o marcarlo como terminado)."""
        try:
            datos_actualizados = {"estado": estado, "completado": completado}
            respuesta = (
                self.client.table("Quizz")
                .update(datos_actualizados)
                .eq("id_quizz", id_quizz)
                .execute()
            )
            return respuesta.data
        except Exception as e:
            print(f"Error al actualizar quizz: {e}")
            return None

    def eliminar_quizz(self, id_quizz: str):
        """Elimina un quizz por completo."""
        try:
            respuesta = (
                self.client.table("Quizz").delete().eq("id_quizz", id_quizz).execute()
            )
            return respuesta.data
        except Exception as e:
            print(f"Error al eliminar quizz: {e}")
            return None

    # =========================================================================
    # SECCIÓN: PREGUNTAS Y OPCIONES (CONSTRUCCIÓN INTEGRAL)
    # =========================================================================

    def agregar_pregunta_completa(
        self,
        id_quizz: str,
        id_pregunta: str,
        texto_pregunta: str,
        id_tipo_pregunta: int,
        index_pregunta: int,
        lista_opciones: list,
    ):
        """
        Inserta una pregunta, sus opciones y amarra todas las relaciones intermedias.

        'lista_opciones' debe ser una lista de diccionarios con este formato:
        [
            {"id_opcion": 101, "texto_opcion": "Azul", "puntaje": 10, "index_opcion": 1},
            {"id_opcion": 102, "texto_opcion": "Rojo", "puntaje": -5, "index_opcion": 2},
            ...
        ]
        """
        try:
            # 1. Insertar la Pregunta base
            self.client.table("Preguntas").insert(
                {
                    "id_pregunta": id_pregunta,
                    "texto_pregunta": texto_pregunta,
                    "id_tipo_pregunta": id_tipo_pregunta,
                }
            ).execute()

            # 2. Relacionar la Pregunta con el Quizz (Tabla intermedia Quizz/Preguntas)
            self.client.table("Quizz/Preguntas").insert(
                {
                    "id_quizz": id_quizz,
                    "id_pregunta": id_pregunta,
                    "index_pregunta": index_pregunta,
                }
            ).execute()

            # 3. Iterar por cada opción que envió el creador
            for opc in lista_opciones:
                # 3a. Insertar la Opción con su puntaje juguetón
                self.client.table("Opciones").insert(
                    {
                        "id_opcion": opc["id_opcion"],
                        "texto_opcion": opc["texto_opcion"],
                        "puntaje": opc["puntaje"],
                    }
                ).execute()

                # 3b. Relacionar la Opción con la Pregunta (Tabla intermedia Preguntas/Opciones)
                self.client.table("Preguntas/Opciones").insert(
                    {
                        "id_pregunta": id_pregunta,
                        "id_opciones": opc["id_opcion"],
                        "index_opcion": opc["index_opcion"],
                    }
                ).execute()

            print(f"Pregunta {id_pregunta} y sus opciones creadas con éxito.")
            return True

        except Exception as e:
            print(f"Error al construir la pregunta completa: {e}")
            return False

    # =========================================================================
    # SECCIÓN: JUGADORES, RESPUESTAS Y RANKING
    # =========================================================================

    def registrar_respuesta_jugador(
        self,
        id_quizz: str,
        id_jugador: str,
        nombre_jugador: str,
        lista_respuesta_json: dict,
    ):
        """
        Registra a un jugador y guarda sus respuestas en formato JSONB.
        Como es un juego de fiesta sin registro previo, este método crea ambos registros seguidos.
        """
        try:
            # 1. Crear al jugador en la tabla 'Jugadores'
            # 'hora_creacion' se puede manejar con el default de la BD o pasando el timestamp actual
            self.client.table("Jugadores").insert(
                {
                    "id_jugador": id_jugador,
                    "nombre_jugador": nombre_jugador,
                    "hora_creacion": "now()",  # O un string de timestamp desde Python
                }
            ).execute()

            # 2. Guardar su mapa de respuestas en la tabla 'Respuestas'
            # Aquí es donde 'lista_respuesta_json' recibe el diccionario {"id_pregunta": "id_opcion"}
            self.client.table("Respuestas").insert(
                {
                    "id_quizz": id_quizz,
                    "id_jugador": id_jugador,
                    "lista_respuesta": lista_respuesta_json,
                }
            ).execute()

            print(f"Respuestas de {nombre_jugador} guardadas con éxito.")
            return True
        except Exception as e:
            print(f"Error al registrar respuestas del jugador: {e}")
            return False

    def obtener_respuestas_para_ranking(self, id_quizz: str):
        """
        Trae todas las respuestas de un Quizz específico.
        Ideal para que tu App local procese los JSON y calcule el ranking en tiempo real.
        """
        try:
            respuesta = (
                self.client.table("Respuestas")
                .select("id_jugador, lista_respuesta, hora_envio")
                .eq("id_quizz", id_quizz)
                .execute()
            )
            return respuesta.data
        except Exception as e:
            print(f"Error al obtener respuestas para ranking: {e}")
            return None

    def eliminar_jugador_travieso(self, id_jugador: str):
        """
        El 'botón de pánico' del creador. Elimina al jugador de la base de datos.
        Gracias al ON DELETE CASCADE, esto borrará automáticamente su fila en la tabla Respuestas.
        """
        try:
            respuesta = (
                self.client.table("Jugadores")
                .delete()
                .eq("id_jugador", id_jugador)
                .execute()
            )
            print(f"Jugador {id_jugador} eliminado por el administrador.")
            return respuesta.data
        except Exception as e:
            print(f"Error al eliminar jugador: {e}")
            return None
