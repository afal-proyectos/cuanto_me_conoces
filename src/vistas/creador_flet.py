import flet as ft


def mostrar_pantalla_qr(page: ft.Page, url_completa: str):
    """Construye y monta la interfaz del QR en la página actual."""
    page.title = "Creador - Generar QR"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    titulo = ft.Text(
        "¡Tu Quiz está listo!",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_700,
    )
    subtitulo = ft.Text(
        "Escanea este código QR para jugar", size=14, color=ft.colors.GREY_700
    )

    codigo_qr = ft.QrCode(
        value=url_completa,
        thickness=10,
        size=250,
    )

    # Limpiamos la pantalla por si acaso y agregamos los componentes
    page.clean()
    page.add(
        ft.Column(
            controls=[titulo, subtitulo, ft.Container(content=codigo_qr, margin=20)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
