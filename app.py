from tkinter.filedialog import askopenfilename
from estudiantes import Estudiante

estudiantes = {}

def cargarEstudiantes():
    ruta =askopenfilename()
    archivo= open(ruta,"r")
    global estudiantes
    for linea in archivo:
            #Leer el archivo y omitir caracteres especificos
            carne, nombre = linea.strip().split(':')
            # Eliminar las comillas del nombre
            nombre = nombre.strip('"')
            #Verifica si la ubicacion ya existe
            if carne in estudiantes:
                    print("El estudiante ya existe")
            else:
                    
                    estudiantes[carne] = Estudiante(str(carne), str(nombre))
                    
    archivo.close()
    print("========Archivo Cargado exitosamente!!========== \n")



def cargarCali():    
    ruta =askopenfilename()
    archivo= open(ruta,"r")
    global estudiantes
    for linea in archivo:
        #Leer el archivo y omitir caracteres especificos
        carne, nota = linea.strip().split(':')
        # Eliminar las coma de las notas
        nota = nota.strip(",")
        #Verifica si la ubicacion ya existe
        if carne in estudiantes:
            estudiantes[carne].agregarNota(str(nota))
        else:
            print("El estudiante no existe")
    archivo.close()
    print("========Archivo Cargado exitosamente!!========== \n")


def informeInventario():
    global estudiantes
    #Crear el archivo
    with open("informe.html", "w", encoding="utf-8") as informe:
    #Escribir el encabezado
        informe.write("<html>")
        informe.write("<head>")
        informe.write("<title>Informe de Estudiantes</title>")
        informe.write("</head>")
        informe.write("<body>")
        informe.write("<h1>Informe de Estudiantes</h1>")
        informe.write("<table>")
        informe.write("<tr>")
        informe.write("<th>Carne</th>")
        informe.write("<th>Nombre</th>")
        informe.write("</tr>")
        #Escribir los datos
        for estudiantes in estudiantes.items():
            informe.write("<tr>")
            informe.write(f"<td>{estudiantes[0]}</td>")
            informe.write(f"<td>{estudiantes[1].nombre}</td>")
            informe.write("</tr>")
        #Escribir el pie
        informe.write("</table>")
        informe.write("</body>")
        informe.write("</html>")
        #Cerrar el informe
    informe.close()

def mostrar_menu():
    print("1. Cargar Estudiantes")
    print("2. Cargar Calificaciones")
    print("3. Crear Informe de General de Estudiantes")
    print("4. Reporte de aprobacion de estudiantes")
    print("5. Top 3 estudiantes con mejor promedio")
    print("6. Salir")
    print("")

#Hola aux
while True:
    mostrar_menu()
    opcion = input("Elige una opción: ")
    if opcion == "1":
        print("===== Cargando Estudiantes.... ========")
        print("")
        cargarEstudiantes()
    elif opcion == "2":
        print("========= Cargando Calificaciones..... ============")
        print("")
        cargarCali()
    elif opcion == "3": 
        print("Creando informe, espere...." + "\n")
        informeInventario()
        print("Revise el archivo .html" + "\n")
    elif opcion == "4":
        print("Creando informe, espere...." + "\n")
        #reporteAprobacion()
        print("Revise el archivo .html" + "\n")
    elif opcion == "5":
        print("Creando informe, espere...." + "\n")
        #top3Estudiantes()
        print("Revise el archivo .html" + "\n")
    elif opcion == "6":
        print("Saliendo..." + "\n")
        break
    else:
        print("Opción inválida. Por favor, elige una opción del menú." + "\n")

#Todo los derechos reservados 2024©