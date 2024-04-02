from analyzer import Analyzer

class ElementoHTML:
    def __init__(self, instruccion, atributo):
        self.instruccion = instruccion
        self.atributos = atributo

    def __str__(self):
        atributos_html = " ".join([f'{key}="{value}"' for key, value in self.atributos.items()])
        return f"<{self.instruccion} {atributos_html}>{self.atributos.get('texto', '')}</{self.instruccion}>"

alineado_html = {"izquierda": "left", "derecha": "right", "centro": "center", "justificado": "justify"}

tamaño_html = {"t1": "h1", "t2": "h2", "t3": "h3", "t4": "h4", "t5": "h5","t6": "h6",}

colors_html = {"rojo": "red", "azul": "blue", "verde": "green"}

def procesar_bloque_encabezado(bloque):
    titulo_pagina = bloque.split('TituloPagina')[1].split('"')[1]
    return ElementoHTML('title', texto=titulo_pagina)


def generar_titulo(bloque):
    atributos = {}
    for linea in bloque.split(';'):
        if 'texto' in linea:
            atributos['texto'] = linea.split('"')[1]
        elif 'posicion' in linea:
            posicion = linea.split('"')[1]
            atributos['align'] = alineado_html.get(posicion, posicion)
        elif 'tamaño' in linea:
            tamaño = linea.split('"')[1]
            atributos['size'] = tamaño_html.get(tamaño, tamaño)
        elif 'color' in linea:
            color = linea.split('"')[1]
            atributos['color'] = colors_html.get(color, color)
    return ElementoHTML('h1', **atributos)


def procesar_bloque_fondo(bloque):
    color = bloque.split('color')[1].split('"')[1]
    color_html = colors_html.get(color, color)
    return ElementoHTML('style', texto=f"body{{background-color: {color_html};}}")


def procesar_bloque_parrafo(bloque):
    atributos = {}
    for linea in bloque.split(';'):
        if 'texto' in linea:
            atributos['texto'] = linea.split('"')[1]
        elif 'posicion' in linea:
            posicion = linea.split('"')[1]
            atributos['align'] = alineado_html.get(posicion, posicion)
    return ElementoHTML('p', **atributos)


def procesar_bloque_texto(bloque):
    atributos = {}
    for linea in bloque.split(';'):
        if 'fuente' in linea:
            atributos['font-family'] = linea.split('"')[1]
        elif 'color' in linea:
            color = linea.split('"')[1]
            atributos['color'] = colors_html.get(color, color)
        elif 'tamaño' in linea:
            tamaño = linea.split('"')[1]
            atributos['font-size'] = tamaño_html.get(tamaño, tamaño)
    return ElementoHTML('span', **atributos)


def procesar_bloque_codigo(bloque):
    atributos = {}
    for linea in bloque.split(';'):
        if 'texto' in linea:
            atributos['texto'] = linea.split('"')[1]
        elif 'posicion' in linea:
            posicion = linea.split('"')[1]
            atributos['text-align'] = alineado_html.get(posicion, posicion)
    return ElementoHTML('div', **atributos)


def procesar_bloque_negrita(bloque):
    texto = bloque.split('texto')[1].split('"')[1]
    return ElementoHTML('b', texto=texto)


def procesar_bloque_subrayado(bloque):
    texto = bloque.split('texto')[1].split('"')[1]
    return ElementoHTML('u', texto=texto)


def procesar_bloque_tachado(bloque):
    texto = bloque.split('texto')[1].split('"')[1]
    return ElementoHTML('s', texto=texto)


def procesar_bloque_cursiva(bloque):
    texto = bloque.split('texto')[1].split('"')[1]
    return ElementoHTML('i', texto=texto)


def procesar_bloque_salto(bloque):
    cantidad = int(bloque.split('cantidad')[1].split('"')[1])
    return ElementoHTML('br' * cantidad)


estructura = []

def leer_documento(ruta_archivo):
    contenido = ruta_archivo
    bloques_procesados = {
        'Encabezado': procesar_bloque_encabezado,
        'Titulo': generar_titulo,
        'Fondo': procesar_bloque_fondo,
        'Parrafo': procesar_bloque_parrafo,
        'Texto': procesar_bloque_texto,
        'Codigo': procesar_bloque_codigo,
        'Negrita': procesar_bloque_negrita,
        'Subrayado': procesar_bloque_subrayado,
        'Tachado': procesar_bloque_tachado,
        'Cursiva': procesar_bloque_cursiva,
        'Salto': procesar_bloque_salto,
    }

    for palabra_clave, funcion_procesar in bloques_procesados.items():

        if palabra_clave == 'Palabra clave':
            Analyzer.getTokens()
            for token in Analyzer.tokens:
                if token.lexema == palabra_clave:
                    indice_busquedas = 0
        indice_busqueda = 0
        while True:
            indice_palabra_clave = contenido.find(palabra_clave, indice_busqueda)
            if indice_palabra_clave != -1:
                inicio_bloque = contenido.find('{', indice_palabra_clave)
                fin_bloque = contenido.find('}', inicio_bloque)
                if inicio_bloque != -1 and fin_bloque != -1:
                    bloque = contenido[inicio_bloque + 1: fin_bloque]
                    estructura.append(funcion_procesar(bloque))
                    indice_busqueda = fin_bloque + 1
                else:
                    break
            else:
                break
    return estructura

def crear_html(html_salida):
    with open(html_salida, 'w', encoding='utf-8') as archivo:
        archivo.write('<!DOCTYPE html>\n<html>\n<head>\n')
        for elemento in estructura:
            if elemento.instruccion == 'title':
                archivo.write(str(elemento))
                archivo.write('\n')
        archivo.write('</head>\n<body>\n')
        for elemento in estructura:
            if elemento.instruccion != 'title':
                archivo.write(str(elemento))
                archivo.write('\n')
        archivo.write('</body>\n</html>\n')

    print(f"Se ha creado el archivo HTML '{html_salida}'")

def formatear():
    estructura.clear()
    
