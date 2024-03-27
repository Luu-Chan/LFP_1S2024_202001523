with open('estudiantes.est', 'r') as archivo:
    # Leer todas las líneas del archivo
    lineas = archivo.readlines()

# Inicializar una lista para almacenar los datos
datos = []

# Iterar sobre cada línea leída del archivo
for linea in lineas:
    # Dividir la línea en carnet y nombre utilizando el carácter :
    carnet, nombre = linea.strip().split(':')
    # Eliminar las comillas del nombre
    nombre = nombre.strip('"')
    # Agregar los datos a la lista
    datos.append((int(carnet), nombre))

print(datos)
