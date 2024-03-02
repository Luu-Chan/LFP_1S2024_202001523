
class Estudiante:
    def __init__(self, carnet, nombre):
        self.carnet = carnet
        self.nombre = nombre
        self.notas = []

    def agregarNota(self, nota):
        self.notas.append(nota)

    def calcularPromedio(self):
        suma = 0
        for nota in self.notas:
            suma += nota
        return suma / len(self.notas)