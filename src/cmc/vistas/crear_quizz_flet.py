import flet as ft
import uuid
from servicios.supabase_ser import SupabaseServicio


def crear_quizz(page: ft.Page):
    supabase = SupabaseServicio()

    input_creador = ft.TextField(label="ID del Creador (Número)", value="1")
    input_evento = ft.TextField(label="ID del Evento (Número)", value="2026")
    text_estado = ft.Text(value="", color=ft.Colors.GREEN)

    def boton_crear_click(e):
        text_estado.value = "Generando Quizz y preguntas de prueba..."
        page.update()

        # 1. Generamos el UUID único para este Quizz desde Python
        id_nuevo_quizz = str(uuid.uuid4())

        # 2. Llamamos a tu método para crear el Quizz base
        quizz_creado = supabase.crear_quizz(
            id_quizz=id_nuevo_quizz,
            id_creador=int(input_creador.value),
            id_evento=int(input_evento.value),
            total_preguntas=2,  # Vamos a inyectar 2 preguntas de prueba
        )

        if quizz_creado:
            # 3. Datos de prueba quemados en el código (Tus preguntas de negocio)
            # Pregunta 1
            id_p1 = str(uuid.uuid4())
            opciones_p1 = [
                {
                    "id_opcion": 11,
                    "texto_opcion": "Python",
                    "puntaje": 10,
                    "index_opcion": 1,
                },
                {
                    "id_opcion": 12,
                    "texto_opcion": "SQL",
                    "puntaje": 5,
                    "index_opcion": 2,
                },
                {
                    "id_opcion": 13,
                    "texto_opcion": "Flet",
                    "puntaje": 8,
                    "index_opcion": 3,
                },
                {
                    "id_opcion": 14,
                    "texto_opcion": "Java",
                    "puntaje": -5,
                    "index_opcion": 4,
                },
            ]
            supabase.agregar_pregunta_completa(
                id_nuevo_quizz,
                id_p1,
                "¿Cuál es tu lenguaje favorito?",
                1,
                1,
                opciones_p1,
            )

            # Pregunta 2
            id_p2 = str(uuid.uuid4())
            opciones_p2 = [
                {
                    "id_opcion": 21,
                    "texto_opcion": "Mucho",
                    "puntaje": 10,
                    "index_opcion": 1,
                },
                {
                    "id_opcion": 22,
                    "texto_opcion": "Poco",
                    "puntaje": 2,
                    "index_opcion": 2,
                },
                {
                    "id_opcion": 23,
                    "texto_opcion": "Nada",
                    "puntaje": 0,
                    "index_opcion": 3,
                },
                {
                    "id_opcion": 24,
                    "texto_opcion": "Me rindo",
                    "puntaje": -10,
                    "index_opcion": 4,
                },
            ]
            supabase.agregar_pregunta_completa(
                id_nuevo_quizz, id_p2, "¿Cuánto te gusta programar?", 1, 2, opciones_p2
            )

            text_estado.value = f"¡Quizz creado con éxito!\nID: {id_nuevo_quizz}\n¡Ya puedes generar tu QR!"
            text_estado.color = ft.Colors.GREEN
        else:
            text_estado.value = "Hubo un error al crear el Quizz base."
            text_estado.color = ft.Colors.RED

        page.update()

    # Diseño visual de la interfaz del Creador
    return ft.View(
        route="/crear",
        controls=[
            ft.AppBar(title=ft.Text("Creador de Quizz - Configuración")),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Paso 1: Configurar Datos del Evento",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        input_creador,
                        input_evento,
                        ft.ElevatedButton(
                            "Crear Quizz y Cargar Preguntas", on_click=boton_crear_click
                        ),
                        text_estado,
                    ],
                    spacing=20,
                ),
                padding=30,
            ),
        ],
    )
