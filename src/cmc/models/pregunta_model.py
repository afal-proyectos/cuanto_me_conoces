import uuid


class PreguntasM:
    def formato_pregunta(self, data: dict):
        self.data = data
        self.id = str(uuid.uuid4())
        self.pregunta = {self.id: self.data}
