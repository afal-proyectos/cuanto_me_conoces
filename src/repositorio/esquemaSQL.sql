CREATE TABLE "Quizz"(
    "id_quizz" UUID NOT NULL,
    "id_creador" INTEGER NOT NULL,
    "id_evento" INTEGER NOT NULL,
    "hora_creacion" TIMESTAMPTZ WITHOUT TIME ZONE NOT NULL,
    "estado" BOOLEAN NOT NULL DEFAULT TRUE,
    "completado" BOOLEAN NOT NULL DEFAULT FALSE,
    "total_preguntas" INTEGER NOT NULL,

    CONSTRAINT "pk_quizz" PRIMARY KEY("id_quizz")
);

CREATE TABLE "Preguntas"(
    "id_pregunta" UUID NOT NULL,
    "texto_pregunta" TEXT NOT NULL,
    "id_tipo_pregunta" INTEGER NOT NULL,

    CONSTRAINT "pk_preguntas" PRIMARY KEY("id_pregunta")
);

CREATE TABLE "Quizz_Preguntas"(
    "id_quizz" UUID NOT NULL,
    "id_pregunta" UUID NOT NULL,
    "index_pregunta" INTEGER NOT NULL,

    CONSTRAINT "pk_quizz_preguntas" PRIMARY KEY("id_quizz", "id_pregunta"),
    CONSTRAINT "fk_quizz_preguntas_quizz" FOREIGN KEY("id_quizz") 
        REFERENCES "Quizz"("id_quizz"),
    CONSTRAINT "fk_quizz_preguntas_preguntas" FOREIGN KEY("id_pregunta") 
        REFERENCES "Preguntas"("id_pregunta")
);


CREATE TABLE "Jugadores"(
    "id_jugador" UUID NOT NULL,
    "nombre_jugador" TEXT NOT NULL,
    "hora_creacion" TIMESTAMPTZ WITHOUT TIME ZONE NOT NULL,

    CONSTRAINT "pk_jugadores" PRIMARY KEY("id_jugador")
);

CREATE TABLE "Respuestas"(
    "id_quizz" UUID NOT NULL,
    "id_jugador" UUID NOT NULL,
    "hora_envio" TIMESTAMPTZ WITHOUT TIME ZONE NOT NULL,
    "lista_respuesta" jsonb NOT NULL,

    CONSTRAINT "pk_respuestas" PRIMARY KEY("id_quizz", "id_jugador"),
    CONSTRAINT "fk_respuestas_quizz" FOREIGN KEY("id_quizz")
        REFERENCES "Quizz"("id_quizz"),
    CONSTRAINT "fk_respuestas_jugadores" FOREIGN KEY("id_jugador") 
        REFERENCES "Jugadores"("id_jugador")
);

CREATE TABLE "Opciones"(
    "id_opcion" UUID NOT NULL,
    "texto_opcion" TEXT NOT NULL,
    "puntaje" INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT "pk_opciones" PRIMARY KEY("id_opcion")
);

CREATE TABLE "Preguntas_Opciones"(
    "id_pregunta" UUID NOT NULL,
    "id_opcion" UUID NOT NULL,
    "index_opcion" INTEGER NOT NULL,

    CONSTRAINT "pk_preguntas_opciones" PRIMARY KEY("id_pregunta", "id_opciones"),
    CONSTRAINT "fk_preguntas_opciones_preguntas" FOREIGN KEY("id_pregunta") 
        REFERENCES "Preguntas"("id_pregunta"),
    CONSTRAINT "fk_preguntas_opciones_opciones" FOREIGN KEY("id_opciones") 
        REFERENCES "Opciones"("id_opcion")  
);



--------las porlitixas están desactivadas en esta etapa de prueba-----------------
ALTER TABLE "Quizz" ENABLE ROW LEVEL SECURITY;

CREATE POLICY modificar_quizz ON "Quizz" 
FOR UPDATE
USING (estado = FALSE)       -- Solo te deja tocarlo si HOY su estado es FALSE
WITH CHECK (estado = FALSE);  -- Tampoco te deja cambiar el estado a TRUE mediante un update común