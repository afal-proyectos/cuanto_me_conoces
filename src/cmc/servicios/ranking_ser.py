import flet as ft
from supabase_ser import SupabaseServicio

supabase = SupabaseServicio()


class RankingServicio:
    def __init__(self, supabase_client):
        self.client = supabase_client

    def obtener_jugadores(self):
        try:
            return self.client.table("Jugadores").select("*").excute()
        except Exception as e:
            print(f"Error al obtener jugadores: {e}")
            return None

    def obtener_ranking_quizz(self, id_quizz: str):
        """
        Descarga todas las respuestas de un Quizz, procesa los puntajes en lote
        y devuelve una lista ordenada de mayor a menor puntuación.
        """
        try:
            print(f"DEBUG: Consultando ranking para Quizz ID: {id_quizz}")
            # 1. Traer todos los jugadores y sus JSON de respuestas para este Quizz (Consulta 1)
            registros = (
                self.client.table("Respuestas")
                .select("id_jugador, lista_respuesta, Jugadores!inner(nombre_jugador)")
                .eq("id_quizz", id_quizz)
                .execute()
            )
            print(
                f"DEBUG: Registros encontrados: {len(registros.data) if registros.data else 0}"
            )

            if not registros.data:
                return []

            # 2. Recolectar TODOS los IDs de opciones que eligieron entre todos los jugadores
            todos_los_id_opciones = set()  # Usamos set para no duplicar IDs en la lista
            for reg in registros.data:
                votos = reg["lista_respuesta"] or {}  # {id_pregunta: id_opcion}
                todos_los_id_opciones.update(str(v) for v in votos.values())

            if not todos_los_id_opciones:
                print("DEBUG: El jugador no tiene votos en su JSON")
                return []

            # 3. Traer los puntajes de todas esas opciones de un solo golpe (Consulta 2)
            opciones_db = (
                self.client.table("Opciones")
                .select("id_opcion", "puntaje")
                .in_(
                    "id_opcion", list(todos_los_id_opciones)
                )  # solo trae las opciones seleccionadas por un id
                .execute()
            )
            print(
                f"DEBUG: Puntajes de opciones cargados: {len(opciones_db.data) if opciones_db.data else 0}"
            )
            # Creamos un diccionario rápido en memoria para buscar puntos: {id_opcion: puntaje}
            mapa_puntajes = {
                opc["id_opcion"]: opc.get("puntaje", 0) for opc in opciones_db.data
            }

            # 4. Calcular el puntaje total de cada jugador localmente en Python
            lista_ranking = []
            for reg in registros.data:
                datos_jugador = reg.get("Jugadores")
                if isinstance(datos_jugador, list):
                    datos_jugador = datos_jugador[0] if datos_jugador else {}

                nombre = datos_jugador.get("nombre_jugador", "Anónimo")
                votos = reg.get("lista_respuesta") or {}

                # Sumamos los puntos usando nuestro mapa en memoria
                puntos_totales = sum(
                    mapa_puntajes.get(str(id_opc), 0) for id_opc in votos.values()
                )

                lista_ranking.append({"nombre": nombre, "puntaje": puntos_totales})

            # 5. Ordenar la lista de mayor a menor puntaje
            # key=lambda x: x["puntaje"] le dice a Python que ordene por los puntos
            lista_ranking.sort(key=lambda x: x["puntaje"], reverse=True)

            return lista_ranking

        except Exception as e:
            print(f"Error al generar el ranking: {e}")
            return None

    def generar_componente_ranking(self, ranking_datos: list):
        if not ranking_datos:
            return [
                ft.Text(
                    "No hay participantes aún.", italic=True, color=ft.Colors.GREY_400
                )
            ]

        filas = []

        # Recorremos los datos ordenados y añadimos medallas a los 3 primeros
        for index, jugador in enumerate(ranking_datos):
            puesto = index + 1
            if puesto == 1:
                icono = "🥇"
            elif puesto == 2:
                icono = "🥈"
            elif puesto == 3:
                icono = "🥉"
            else:
                icono, color = f"  {puesto}. ", ft.Colors.WHITE

            filas.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(icono, size=24),
                            ft.Text(
                                jugador["nombre"], size=20, weight="bold", expand=True
                            ),
                            ft.Text(
                                f"{jugador['puntaje']} pts",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN,
                            ),
                        ]
                    ),
                    padding=10,
                    bgcolor=ft.Colors.WHITE10,
                    border_radius=10,
                )
            )
        return filas


if __name__ == "__main__":

    def main(page: ft.Page):
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 50

        servicio = RankingServicio(supabase.client)
        ID_QUIZZ_TEST = "40b68a3f-3aa7-4d24-a2b2-3cebca2c3466"

        datos = servicio.obtener_ranking_quizz(ID_QUIZZ_TEST)
        print(f"DEBUG FINAL: Datos procesados para UI: {datos}")

        page.add(
            ft.Column(
                [
                    ft.Text("🏆 RANKING", size=40, weight="bold"),
                    ft.Divider(),
                    *servicio.generar_componente_ranking(datos),
                ],
                scroll=ft.ScrollMode.ALWAYS,
            )
        )

    ft.app(target=main)
