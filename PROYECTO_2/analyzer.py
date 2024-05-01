from token_1 import Token
from error import Error
import os
import subprocess
import graphviz

class Analyzer():
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.errors = []
        self.palabrasReservada = ["ID","ER", "CADENAS"]

    def isValidSymbol(self, char):
        return char in [":", "{", "}", ";", ",", "+", "*", "?", "|","(", ")", "-"]
    
    def isnumber(self, char):
        return char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    
    def state0(self, char, line, column, lexema):
        if self.isValidSymbol(char):
            return 10
        elif char == '"':
            return 1
        elif char.isalpha():
            return 2
        elif self.isnumber(char):
            return 8
        elif char == "'":
            return 3
        elif char == "#":
            return 9
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
                    if lexema in self.palabrasReservada:
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
            
            elif state == 3:
                if char == "'":
                    state = 4
                else:
                    self.errors.append(Error(lexema, char, "Léxico", line, column))
                    lexema = ""
                    state = 0
            
            elif state == 4:    
                if char == "'":
                    state = 5
                else:
                    self.errors.append(Error(lexema, char, "Léxico", line, column))
                    lexema = ""
                    state = 10
            
            #Se acepta lo que hay dentro del comentario
            elif state == 5:
                if char == "'":
                    state = 6
                else:
                    pass
            
            elif state == 6:
                if char == "'":
                    state = 7
                else:
                    pass
            
            elif state == 7:
                if char == "'":
                    #se termina el comentario
                    
                    state = 0
                    lexema = ""
                else:
                    state = 5

            elif state == 8:
                if self.isnumber(char):
                    lexema += char
                    state = 8
                elif self.isnumber(char) == False:
                    self.tokens.append(Token("Numero", lexema, line, column - len(lexema)))
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
                else:
                    self.errors.append(Error(lexema, char, "Léxico", line, column))
                    lexema = ""
                    state = 0
            
            elif state == 9:
                if char == "\n":
                    state = 0
                    lexema = ""
                else:
                    pass
            
            elif state == 10:
                if previousState == 0:
                    self.tokens.append(Token("Signo", lexema, line, column - len(lexema)))
                elif previousState == 1:
                    self.tokens.append(Token("String", lexema, line, column - len(lexema)))
                elif previousState == 2:
                    self.tokens.append(Token("Numero", lexema, line, column - len(lexema)))
                
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

    def get_tokens(self):
        texto = ""
        for token in self.tokens:
            if token.valor == "Palabra Reservada"  or token.valor == "Numero" or token.valor == "String":
                if token.tipo == "ID" or token.tipo == "ER" or token.tipo == "CADENAS":
                    texto += "\n" + token.tipo + ": \n"
                
                else:    
                    texto += "\n" + token.tipo + "\n"
                
                
            elif token.tipo == "(" or token.tipo == ")" or token.tipo == "+" or token.tipo == "|" or token.tipo == "?" or token.tipo == "*":
                texto += token.tipo
        return texto
            
    
    def generate_html(self):
        if self.tokens[0].valor == "Numero":
            self.tokens.pop(0)
        with open("Informe_Lexico.html", "w") as file:
            file.write("<!DOCTYPE html>\n")
            file.write("<html>\n")
            file.write("<head>\n")
            file.write("<title>Tokens</title>\n")
            file.write("</head>\n")
            file.write("<body>\n")
            file.write("<h1><p align='center' style='color: red;'> Tokens y Errores Lexicos</p></h1>")
            file.write("<table border='1' align='center' >\n")
            file.write("<tr>\n")
            file.write("<th>Token</th>\n")
            file.write("<th>Lexema</th>\n")
            file.write("<th>Fila</th>\n")
            file.write("<th>Columna</th>\n")
            file.write("</tr>\n")
            for token in self.tokens:
                file.write("<tr>\n")
                file.write(f"<td>{token.valor}</td>\n")
                file.write(f"<td>{token.tipo}</td>\n")
                file.write(f"<td>{token.linea}</td>\n")
                file.write(f"<td>{token.columna}</td>\n")
                file.write("</tr>\n")
            file.write("<tr>\n")
            file.write("<th>Caracter Invalido</th>\n")
            file.write("<th>Linea</th>\n")
            file.write("<th>Colunma</th>\n")
            file.write("</tr>\n")
            for error in self.errors:
                file.write("<tr>\n")
                file.write(f"<td>{error.lexema}{error.errorChar}</td>\n")
                file.write(f"<td>{error.line}</td>\n")
                file.write(f"<td>{error.column}</td>\n")
                file.write("</tr>\n")
            file.write("</body>\n")
            file.write("</html>\n")
            file.close()

    def generate_afd_graph(self):
        dot = graphviz.Digraph(comment='AFD Diagram')
            
        dot.node('0', '0', shape='doublecircle')
        dot.node('1', '1', shape='circle')
        dot.node('2', '2', shape='circle')
        dot.node('3', '3', shape='circle')
        dot.node('4', '4', shape='circle')
        dot.node('5', '5', shape='circle')
        dot.node('6', '6', shape='circle')
        dot.node('7', '7', shape='circle')
        dot.node('8', '8', shape='circle')
        dot.node('9', '9', shape='circle')
        dot.node('10', '10', shape='circle')
            
        dot.edge('0', '10', label=': { } ; , + * ? | . ( ) -')
        dot.edge('0', '1', label='"')
        dot.edge('0', '2', label='a-z A-Z')
        dot.edge('0', '8', label='0-9')
        dot.edge('0', '3', label="'")
        dot.edge('0', '9', label='#')
            
        dot.edge('1', '10', label='"')
        dot.edge('1', '1', label='any')
            
        dot.edge('2', '2', label='a-z A-Z')
        dot.edge('2', '10', label='any')
            
        dot.edge('3', '4', label="'")
        dot.edge('3', '10', label='any')
            
        dot.edge('4', '5', label="'")
        dot.edge('4', '10', label='any')
            
        dot.edge('5', '6', label="'")
        dot.edge('5', '5', label='any')
            
        dot.edge('6', '7', label="'")
        dot.edge('6', '5', label='any')
            
        dot.edge('7', '10', label="'")
        dot.edge('7', '5', label='any')
            
        dot.edge('8', '8', label='0-9 .')
        dot.edge('8', '10', label='any')
            
        dot.edge('9', '10', label='any')
            
        dot.edge('10', '10', label='any')
            
        dot.render('afd_graph.gv', view=True)
                    
        with open("code_graph.dot", "w") as file:
            file.write(dot.source)
            file.close()
        
        # Add the path to Graphviz bin directory to the PATH environment variable
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        
        # Use subprocess to execute the dot command
        subprocess.run(["dot", "-Tpng", "code_graph.dot", "-o", "Arbol.png"])