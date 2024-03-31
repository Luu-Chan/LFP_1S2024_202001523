from token_1 import Token
from error import Error
import os
import os
import subprocess

TOKENS = []

class Analyzer():
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.errors = []
        self.palabrasReservada = ["Inicio" , "Titulo", "Encabezado", "Cuerpo", "Fondo", "Parrafo", "Texto","Codigo","Negrita",
                                "Subrayado","Tachado","Cursiva","Salto", "texto", "fuente", "color", "tamaño", "posicion","cantidad"]

    def isValidSymbol(self, char):
        return char in [":", "{", "}", ";", ",", "[", "]", "="]
    
    def state0(self, char, line, column, lexema):
        if self.isValidSymbol(char):
            return 10
        elif char == '"':
            return 1
        elif char.isalpha():
            return 2
        else:
            #Omitir espacios, tabulaciones y saltos de línea
            if ord(char) == 10 or ord(char) == 32 or ord(char) == 9:
                pass
            else:# Es un error
                self.errors.append(Error(lexema, char, "Léxico", line, column))
            return 0

    def analyze(self):
        line = 1
        column = 1
        lexema = ""

        state = 0
        previousState = -1
        self.tokens.clear()
        self.errors.clear()

        for char in self.text:
            if state == 0:
                state = self.state0(char, line, column, lexema)
                if state == 0:
                    #Se reinicia el lexema
                    lexema = ""
                    previousState = -1
                elif state == 10:
                    lexema += char
                    previousState = 0
                    self.tokens.append(Token("Signo", lexema, line, column))
                    state = 0
                    lexema = ""
                else:
                    lexema += char
                    previousState = 0

            
            elif state == 1:
                if char == '"':
                    lexema += char
                    state = 10
                    previousState = 1
                elif char != "\n":
                    lexema += char
                    state = 1
                else:#Error
                    self.errors.append(Error(lexema, char, "Léxico", line, column))

                    #Se reinicia el lexema
                    lexema = ""
                    state = 0
            
            elif state == 2:
                if char.isalpha():
                    lexema += char
                    state = 2
                else: #Es un estado de aceptación, se guarda el token
                    #Se verifica si es una palabra reservada valida
                    for palabraReservada in self.palabrasReservada:
                        if lexema == palabraReservada:
                            self.tokens.append(Token("Palabra Reservada", lexema, line, column - len(lexema)))
                            
                        
                            #Se reinicia el lexema
                            lexema = ""
                            state = 0

                        #Actúa como si estuviera en el estado 0 de nuevo
                            state = self.state0(char, line, column, lexema)
                            if state == 0:
                        #Se reinicia el lexema
                                lexema = ""
                                previousState = -1
                            else:
                                lexema += char
                                previousState = 0
                    else: #Es un error
                        self.errors.append(Error(lexema, char, "Léxico", line, column))
                        #Se reinicia el lexema
                        lexema = ""
                        state = 0

            elif state == 10:
                if previousState == 0:
                    self.tokens.append(Token("Signo", lexema, line, column - len(lexema)))
                elif previousState == 1:
                    self.tokens.append(Token("String", lexema, line, column - len(lexema)))
                
                lexema = "" #Se limpia el lexema porque ya fue almacenado

                state = self.state0(char, line, column, lexema)
                if state == 0:
                    #Se reinicia el lexema
                    lexema = ""
                    previousState = -1
                else:
                    lexema += char
                    previousState = 0


            # Control de líneas y columnas
            
            #Salto de línea
            if ord(char) == 10:
                line += 1
                column = 1
            #Tabulación
            elif ord(char) == 9:
                column += 4

            #Espacio
            elif ord(char) == 32:
                column += 1

            else:
                column += 1

    def generarTokens(self):
        for token in self.tokens:
            if token.name == "Palabra Reservada" or token.name == "String":
                TOKENS.append(token)

    def getTokens(self):
        with open("tokens.html", "w") as file:
            file.write("<!DOCTYPE html>\n")
            file.write("<html>\n")
            file.write("<head>\n")
            file.write("<title>Tokens</title>\n")
            file.write("</head>\n")
            file.write("<body>\n")
            file.write("<h1><p align='center' style='color: red;'> Tokens y Errores</p></h1>")
            file.write("<table border='1'>\n")
            file.write("<tr>\n")
            file.write("<th>Token</th>\n")
            file.write("<th>Lexema</th>\n")
            file.write("<th>Fila</th>\n")
            file.write("<th>Columna</th>\n")
            file.write("</tr>\n")
            for token in self.tokens:
                file.write("<tr>\n")
                file.write(f"<td>{token.name}</td>\n")
                file.write(f"<td>{token.value}</td>\n")
                file.write(f"<td>{token.line}</td>\n")
                file.write(f"<td>{token.column}</td>\n")
                file.write("</tr>\n")
            #file.write("table border='2'>\n")
            file.write("<tr>\n")
            file.write("<th>Caracter Invalido</th>\n")
            file.write("<th>Linea</th>\n")
            file.write("<th>Colunma</th>\n")
            file.write("</tr>\n")
            for error in self.errors:
                if error.errorChar != ';' or error.lexema != '=':
                    file.write("<tr>\n")
                    file.write(f"<td>{error.errorChar}</td>\n")
                    file.write(f"<td>{error.line}</td>\n")
                    file.write(f"<td>{error.column}</td>\n")
                    file.write("</tr>\n")
            file.write("</body>\n")
            file.write("</html>\n")
            file.close()

    def generate_dot_code(self):
        """dot_code = "digraph G {\n"
        
        # Add nodes for tokens
        for token in self.tokens:
            dot_code += f'    {token.name}_{token.line}_{token.column} [label="{token.name}: {token.value}"];\n'
        
        # Add edges between tokens
        for i in range(len(self.tokens) - 1):
            dot_code += f'    {self.tokens[i].name}_{self.tokens[i].line}_{self.tokens[i].column} -> {self.tokens[i+1].name}_{self.tokens[i+1].line}_{self.tokens[i+1].column};\n'
        
        dot_code += "}"
                    
        with open("code_graph.dot", "w") as file:
            file.write(dot_code)
            file.close()"""
        
        # Add the path to Graphviz bin directory to the PATH environment variable
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        
        # Use subprocess to execute the dot command
        subprocess.run(["dot", "-Tpng", "code_graph.dot", "-o", "Automata.png"])
