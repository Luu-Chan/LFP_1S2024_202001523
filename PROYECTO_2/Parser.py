from token_1 import Token
from error_s import Error
import graphviz
import os
import subprocess

class Parser():
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.errors = []

        #Controlar fin de tokens
        if self.tokens[0].tipo.isdigit():
            self.tokens.pop(0)
        self.tokens.append(Token("EOF", "EOF", -1, -1))
        #End of file = EOF

    def recuperar(self, nombreTokenSincronizacion):
        while self.tokens[0].tipo != "EOF":
            tk = self.tokens.pop(0)
            if tk.tipo == nombreTokenSincronizacion:
                break

    def parse(self):
        self.inicio()

    #<inicio> ::= <elemento> <otro_elemento>
    def inicio(self):
        self.elemento()
        self.otro_elemento()
        print("Análisis sintáctico exitoso")

    #<elemento> ::= tk_llaveA <instruccionID> <instruccionER> <instruccionCadenas> tk_llaveC
    def elemento(self):
        if self.tokens[0].tipo == '{':
            self.tokens.pop(0) #Se extrae el token validado

            self.instruccionID()
            self.instruccionER()
            self.instruccionCadenas()

            if self.tokens[0].tipo == '}':
                self.tokens.pop(0)
            else:
                print("error, Se esperaba una llave de cierre")
                fila = self.tokens[0].linea
                columna = self.tokens[0].columna
                self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
                self.recuperar("}")
        else:
            print("Error, se esperaba una llave de apertura")
            self.recuperar("{")

    # <otro_elemento> ::= tk_coma <elemento> <otro_elemento>
    #                  | epsilon
    def otro_elemento(self):
        if self.tokens[0].tipo == ",":
            self.tokens.pop(0)
            self.elemento()
            self.otro_elemento()
        else:
            pass #Se acepta épsilon

    #<instruccionID> ::= tk_id tk_dosPuntos tk_entero tk_PyC
    def instruccionID(self):
        if self.tokens[0].tipo == "ID":
            self.tokens.pop(0)
            if self.tokens[0].tipo == ":":
                self.tokens.pop(0)
                if self.tokens[0].tipo.isdigit():
                    self.tokens.pop(0)
                    if self.tokens[0].tipo == ";":
                        self.tokens.pop(0)
                    else:
                        print("Error, se esperaba ';'")
                        fila = self.tokens[0].linea
                        columna = self.tokens[0].columna
                        self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
                else:
                    print("Error, se esperaba un entero")
                    fila = self.tokens[0].linea
                    columna = self.tokens[0].columna
                    self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
                    self.recuperar(";")
            else:
                print("Error, se esperaba ':'")
                fila = self.tokens[0].linea
                columna = self.tokens[0].columna
                self.errors.append(Error(self.tokens[0].tipo, "Sintactico",fila, columna))
                self.recuperar(";")
        else:
            print("Error, se esperaba la palabra reservada 'ID'")
            fila = self.tokens[0].linea
            columna = self.tokens[0].columna
            self.errors.append(Error(self.tokens[0].tipo, "Sintactico",fila, columna))
            self.recuperar(";")

    #<instruccionER> ::= tk_ER tk_dosPuntos <expresion> <otraExpresion> tk_PyC
    def instruccionER(self):
        if self.tokens[0].tipo == "ER":
            self.tokens.pop(0)
            if self.tokens[0].tipo == ":":
                self.tokens.pop(0)

                self.expresion()
                self.otraExpresion()

                if self.tokens[0].tipo == ";":
                    self.tokens.pop(0)
                else:
                    print("Error, se esperaba ';' y se obtuvo" + self.tokens[0].tipo)
                    fila = self.tokens[0].linea
                    columna = self.tokens[0].columna
                    self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
                    self.recuperar(";")

            else:
                print("Error, se esperaba ':'")
                fila = self.tokens[0].linea
                columna = self.tokens[0].columna
                self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
                self.recuperar(";")

        else:
            print("Error, se esperaba la palabra reservada 'ER'")
            fila = self.tokens[0].linea
            columna = self.tokens[0].columna
            self.errors.append(Error(self.tokens[0].tipo, "Sintactico",fila, columna))
            self.recuperar(";")


    #<expresion> ::= parA <expresion> parC <operador>
    #              | <elementoER> <operador>
    def expresion(self):
        if self.tokens[0].tipo == "(":
            self.tokens.pop(0)

            self.expresion()

            if self.tokens[0].tipo == ")":
                self.tokens.pop(0)

                self.operador()
            else:
                print("Error, se esperaba un parentesis de cierre")
                fila = self.tokens[0].linea
                columna = self.tokens[0].columna
                self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
                self.recuperar(";")

        else:
            self.elementoER()
            self.operador()

    #<otraExpresion> ::= <expresion> <otraExpresion>
    #                  | epsilon
    def otraExpresion(self):
        if self.tokens[0].tipo == "(" or self.tokens[0].valor == "String" or self.tokens[0].valor == "Numero" or self.tokens[0].tipo == '.':
            self.expresion()
            self.otraExpresion()
        else:
            pass #Se acepta épsilon

    #<operador> ::= <operadorUnario>
    #             | tk_Or <expresion>
    #             | epsilon
    def operador(self):
        if self.tokens[0].tipo == '+' or self.tokens[0].tipo == '*' or self.tokens[0].tipo == '?':
            self.operadorUnario()
        elif self.tokens[0].tipo == '|':
            self.tokens.pop(0)
            self.expresion()
        else:
            pass# Se acepta épsilon

    # <operadorUnario> ::= tk_Mas
    #                    | tk_Asterisco
    #                    | tk_interrogacion
    def operadorUnario(self):
        if self.tokens[0].tipo == '+' or self.tokens[0].tipo == '*' or self.tokens[0].tipo == '?':
            self.tokens.pop(0)
        else:
            print("Error, se esperaba un operador unario")
            fila = self.tokens[0].linea
            columna = self.tokens[0].columna
            self.errors.append(Error( self.tokens[0].tipo, "Sintactico", fila, columna))
            self.recuperar(";")


    # <elementoER> ::= tk_cadena
    #                | tk_entero
    #                | tk_decimal
    def elementoER(self):
        if self.tokens[0].valor == "String" or self.tokens[0].valor == "Numero" or self.tokens[0].tipo == '.':
            self.tokens.pop(0)
        else:
            print("Error, se esperaba cadena, entero o decimal")
            fila = self.tokens[0].linea
            columna = self.tokens[0].columna
            self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
            self.recuperar(";")


    #<instruccionCadenas> ::= tk_Cadenas tk_dosPuntos tk_cadena <otraCadena> tk_PyC
    def instruccionCadenas(self):
        if self.tokens[0].tipo == "CADENAS":
            self.tokens.pop(0)
            if self.tokens[0].tipo == ':':
                self.tokens.pop(0)
                if self.tokens[0].valor == "String":
                    self.tokens.pop(0)

                    self.otraCadena()

                    if self.tokens[0].tipo == ';':
                        self.tokens.pop(0)
                    else:
                        print("Error, se esperaba ';' y se obtuvo " + self.tokens[0].tipo)
                        fila = self.tokens[0].linea
                        columna = self.tokens[0].columna
                        self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
                        self.recuperar(";")

                else:
                    print("Error, se esperaba una cadena")
                    fila = self.tokens[0].linea
                    columna = self.tokens[0].columna
                    self.errors.append(Error("", self.tokens[0].tipo, "Sintactico",fila, columna))
                    self.recuperar(";")

            else:
                print("Error, se esperaba ':'")
                fila = self.tokens[0].linea
                columna = self.tokens[0].columna
                self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
                self.recuperar(";")

        else:
            print("Error, se esperaba la palabra reservada 'Cadenas'")
            fila = self.tokens[0].linea
            columna = self.tokens[0].columna
            self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
            self.recuperar(";")


    # <otraCadena> ::= tk_coma tk_cadena <otraCadena>
    #                | epsilon
    def otraCadena(self):
        if self.tokens[0].tipo == ',':
            self.tokens.pop(0)
            if self.tokens[0].valor == "String":
                self.tokens.pop(0)
                self.otraCadena()
            else:
                print("Error, se esperaba una cadena y se obtuvo" + self.tokens[0].tipo)
                fila = self.tokens[0].linea
                columna = self.tokens[0].columna
                self.errors.append(Error( self.tokens[0].tipo, "Sintactico",fila, columna))
                self.recuperar(";")

        else:
            pass #Se acepta épsilon
        
    def generate_html(self):
        with open("Informe_Sintactico.html", "w") as file:
            file.write("<!DOCTYPE html>\n")
            file.write("<html>\n")
            file.write("<head>\n")
            file.write("<title>Errores</title>\n")
            file.write("</head>\n")
            file.write("<body>\n")
            file.write("<h1><p align='center' style='color: red;'> Errores Sintacticos </p></h1>")
            file.write("<table border='1' align='center' >\n")
            file.write("<tr>\n")
            file.write("<th>Caracter</th>\n")
            file.write("<th>Fila</th>\n")
            file.write("<th>Columna</th>\n")
            file.write("</tr>\n")
            for error in self.errors:
                file.write("<tr>\n")
                file.write(f"<td>{error.errorChar}</td>\n")
                file.write(f"<td>{error.line}</td>\n")
                file.write(f"<td>{error.column}</td>\n")
                file.write("</tr>\n")
            file.write("</body>\n")
            file.write("</html>\n")
            file.close()