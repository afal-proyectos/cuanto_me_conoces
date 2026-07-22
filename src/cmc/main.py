import flet as ft
from vistas.crear_quizz_flet import crear_quizz


def main(page: ft.Page):
    page.title = "Sistema de Quizz - Panel del Creador"

    # Configuramos el tamaño de la ventana para que sea cómodo en PC
    page.window_width = 500
    page.window_height = 700
    page.window_resizable = False

    # Obtenemos la vista que creamos
    instancia_vista = crear_quizz(page)

    # Agregamos los controles de esa vista a la página principal
    page.add(*instancia_vista.controls)


if __name__ == "__main__":
    ft.app(target=main)
