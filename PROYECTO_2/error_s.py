class Error():
    def __init__(self, errorChar, type, line, column):

        self.errorChar = errorChar
        self.type = type
        self.line = line
        self.column = column

    def __str__(self):
        return f"Error Sintactico({self.errorChar}, {self.type}, {self.line}, {self.column})"