import flet as ft
from src.vistas.creador_flet import mostrar_pantalla_qr


def main(page: ft.Page):
    # Aquí simulas la URL que tendrá tu GitHub Pages en el futuro
    URL_PROVISIONAL = "https://afal-proyectos.io/cuanto_me_conoces/?quiz_id=123"

    # Llamamos a la vista de la capa de interfaz
    mostrar_pantalla_qr(page, URL_PROVISIONAL)


if __name__ == "__main__":
    ft.app(target=main)
