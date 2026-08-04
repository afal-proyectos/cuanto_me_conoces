pregunta = {
    "2a43ab4e-11eb-4ba9-98cc-74c6436e3279": {
        "nombre_creador": "as",
        "nombre_evento": "as",
        "comentario": "as",
        "cantidad_preguntas": 5,
        "data_preguntas": [
            {
                "id_pregunta": "2a43ab4e-11eb-4ba9-98cc-74c6436e3201",
                "index": 1,
                "pregunta": "¿Anime Favorito?",
                "opciones": {
                    "1": "Dragon Ball Z",
                    "2": "Demon Slayers",
                    "3": "Bako no Hero",
                },
                "puntaje": {"1": 4, "2": -2, "3": 0},
            },
            {
                "id_pregunta": "2a43ab4e-11eb-4ba9-98cc-74c6436e3202",
                "index": 1,
                "pregunta": "¿Superhéroe favorito?",
                "opciones": {"1": "Batman", "2": "Superman", "3": "WonderWoman"},
                "puntaje": {"1": 4, "2": -2, "3": 0},
            },
        ],
    }
}
# print("Prueba 1: ", pregunta["data_preguntas"][0]["pregunta"])
print(list(pregunta.keys())[0])
for dato in list(pregunta.values())[0]["data_preguntas"]:
    print(f"Hola : {dato['pregunta']}")
