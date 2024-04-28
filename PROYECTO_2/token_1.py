class Token:
    def __init__(self, valor, tipo, linea, columna):
        self.valor = valor
        self.tipo = tipo
        self.linea = linea
        self.columna = columna


        
    def __str__(self):
        return f"Token({self.valor}, {self.tipo}, {self.linea}, {self.columna})"
    
