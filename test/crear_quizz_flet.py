import flet as ft
import uuid
from servicios.supabase_ser import SupabaseServicio
import qrcode
import os


def crear_quizz(page: ft.Page):
    supabase = SupabaseServicio()

    input_creador = ft.TextField(label="ID del Creador (Número)", value="1")
    input_evento = ft.TextField(label="ID del Evento (Número)", value="2026")
    text_estado = ft.Text(value="", color=ft.Colors.GREEN)
    componente_qr = ft.Image(src="", visible=False, width=200, height=200)

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
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Todas las Carnes",
                    "puntaje": 0,
                    "index_opcion": 1,
                },
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "No me gustan la pizza",
                    "puntaje": -2,
                    "index_opcion": 2,
                },
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Me gustan todas",
                    "puntaje": 2,
                    "index_opcion": 3,
                },
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Pepperoni",
                    "puntaje": 4,
                    "index_opcion": 4,
                },
            ]
            supabase.agregar_pregunta_completa(
                id_nuevo_quizz,
                id_p1,
                "¿Cuál es mi pizza favorita?",
                1,
                1,
                opciones_p1,
            )

            # Pregunta 2
            id_p2 = str(uuid.uuid4())
            opciones_p2 = [
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Gata loca",
                    "puntaje": 0,
                    "index_opcion": 1,
                },
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Gusano Pincel",
                    "puntaje": 2,
                    "index_opcion": 2,
                },
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Agente del Caos",
                    "puntaje": 2,
                    "index_opcion": 3,
                },
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Alma",
                    "puntaje": 4,
                    "index_opcion": 4,
                },
            ]
            supabase.agregar_pregunta_completa(
                id_nuevo_quizz, id_p2, "¿Cómo se llama mi gato?", 1, 2, opciones_p2
            )
            # ---------------------------------------------------------------------
            id_p3 = str(uuid.uuid4())
            opciones_p2 = [
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Trasero Loco",
                    "puntaje": 2,
                    "index_opcion": 1,
                },
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Javi",
                    "puntaje": -2,
                    "index_opcion": 2,
                },
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "Popita",
                    "puntaje": 0,
                    "index_opcion": 3,
                },
                {
                    "id_opcion": str(uuid.uuid4()),
                    "texto_opcion": "ChikiPopi",
                    "puntaje": 4,
                    "index_opcion": 4,
                },
            ]
            supabase.agregar_pregunta_completa(
                id_nuevo_quizz,
                id_p3,
                "¿Cómo me gusta llamar a mi hija?",
                1,
                2,
                opciones_p2,
            )
            text_estado.value = f"¡Quizz creado con éxito!\nID: {id_nuevo_quizz}\n¡Ya puedes generar tu QR!"
            text_estado.color = ft.Colors.GREEN
            quizz_listo = True
        else:
            text_estado.value = "Hubo un error al crear el Quizz base."
            text_estado.color = ft.Colors.RED

        page.update()

        if quizz_listo:
            # 1. Definimos la URL real apuntando a tu otro mini-proyecto + el ID dinámico
            url_jugador = f"https://afal-proyectos.github.io/cuanto_me_conoces_web/?id={id_nuevo_quizz}"

            # 2. Generamos el QR con la librería de Python
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(url_jugador)
            qr.make(fit=True)

            # 3. Lo guardamos temporalmente como imagen en tu computadora
            ruta_qr = os.path.join(os.path.dirname(__file__), "qr_actual.png")
            img_qr = qr.make_image(fill_color="black", back_color="white")
            img_qr.save(ruta_qr)

            # 4. Le decimos a Flet que cargue esa imagen y la haga visible
            componente_qr.src = ruta_qr
            componente_qr.visible = True

            text_estado.value = f"¡Quizz creado con éxito!\nID: {id_nuevo_quizz}"
            text_estado.color = ft.Colors.GREEN

        else:
            text_estado.value = "Error al crear el Quizz."
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
                        componente_qr,
                    ],
                    spacing=20,
                ),
                padding=30,
            ),
        ],
    )
