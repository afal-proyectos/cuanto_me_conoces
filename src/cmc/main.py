import flet as ft

# from vistas.crear_quizz_flet import crear_quizz
from vistas.app import App


def main(page: ft.Page):
    print("hola")
    App(page)


if __name__ == "__main__":
    ft.run(main)
