
class Estudiante:
    def __init__(self, carnet, nombre):
        self.carnet = carnet
        self.nombre = nombre
        self.notas = []

    def agregarNota(self, nota):
        self.notas.extend(nota)

    def calcularPromedio(self):
        suma = 0
        for nota in self.notas:
            suma += int(nota)
        return int((suma / len(self.notas))*100)/100