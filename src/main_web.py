import flet as ft
from urllib.parse import urlparse, parse_qs

# Aquí importarías tu servicio real de Supabase
# from src.servicios.supabase_ser import obtener_pregunta_db


def main(page: ft.Page):
    page.title = "Responde el Quiz"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 1. CAPTURAR EL ID DESDE LA URL (page.route)
    url_actual = page.route
    parsed_url = urlparse(url_actual)
    parametros = parse_qs(parsed_url.query)
    quiz_id = parametros.get("quiz_id", [None])[0]

    # 2. SIMULAR DATOS DE SUPABASE (Para la prueba rápida)
    # En el futuro, aquí harás: fila = obtener_pregunta_db(quiz_id)
    # Y luego usarás tu modelo: pregunta = Question.from_row(fila)
    pregunta_texto = "¿Cuál es mi color favorito?"
    opciones = ["Rojo", "Azul", "Verde"]

    # 3. INTERFAZ VISUAL MÍNIMA
    titulo = ft.Text(value="Trivia de Cumpleaños", size=24, weight=ft.FontWeight.BOLD)

    texto_pregunta = ft.Text(value=pregunta_texto, size=18)

    # Creamos un grupo de opciones (Radio Group) para la selección múltiple
    opciones_usuario = ft.RadioGroup(
        content=ft.Column(controls=[ft.Radio(value=opt, label=opt) for opt in opciones])
    )

    def enviar_respuesta(e):
        respuesta_seleccionada = opciones_usuario.value
        if respuesta_seleccionada:
            # Aquí irá la lógica para guardar en Supabase:
            # guardar_resultado_en_supabase(quiz_id, respuesta_seleccionada)

            # Por ahora, solo mostramos una alerta de éxito en la web
            page.dialog = ft.AlertDialog(
                title=ft.Text("¡Enviado!"),
                content=ft.Text(
                    f"Respuesta '{respuesta_seleccionada}' registrada para el Quiz: {quiz_id}"
                ),
            )
            page.dialog.open = True
            page.update()

    boton_enviar = ft.ElevatedButton(text="Enviar respuesta", on_click=enviar_respuesta)

    # Si entramos sin código QR (sin ID), mostramos error. Si hay ID, cargamos el juego.
    if quiz_id:
        page.add(
            titulo,
            ft.Divider(),
            texto_pregunta,
            opciones_usuario,
            ft.Divider(),
            boton_enviar,
        )
    else:
        page.add(
            ft.Text(
                "Error: Escanea un código QR válido para jugar.", color=ft.colors.RED
            )
        )


if __name__ == "__main__":
    ft.app(target=main)
