class Deporte:
    def __init__(self, nombre, precio_hora):
        self.nombre = nombre
        self.precio_hora = precio_hora

    def __deportes__(self):
        return "Deporte: " + self.nombre + " Precio por hora: " + str(self.precio_hora)


