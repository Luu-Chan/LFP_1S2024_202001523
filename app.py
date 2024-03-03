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
        carne, notas = linea.strip().split(':')
        # Eliminar las coma de las notas
        nota = notas.split(",")
        #Verifica si la ubicacion ya existe
        if carne in estudiantes:
            estudiantes[carne].agregarNota(nota)
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
        informe.write("<th>Notas</th>")
        informe.write("</tr>")
        #Escribir los datos
        for estudiante in estudiantes.values():
            informe.write("<tr>")
            informe.write(f"<td>{estudiante.carnet}</td>")
            informe.write(f"<td>{estudiante.nombre}</td>")
            informe.write(f"<td>{', '.join(estudiante.notas)}</td>")
            informe.write("</tr>")
        #Escribir el pie
        informe.write("</table>") 
        informe.write("</body>")
        informe.write("</html>")
        #Cerrar el informe
    informe.close()

def reporteAprobacion():
    global estudiantes
    #Crear el archivo
    with open("reporte.html", "w", encoding="utf-8") as reporte:
    #Escribir el encabezado
        reporte.write("<html>")
        reporte.write("<head>")
        reporte.write("<title>Reporte de Aprobacion</title>")
        reporte.write("</head>")
        reporte.write("<body>")
        reporte.write("<h1>Reporte de Aprobacion</h1>")
        reporte.write("<table>")
        reporte.write("<tr>")
        reporte.write("<th>Carne</th>")
        reporte.write("<th>Nombre</th>")
        reporte.write("<th>Promedio</th>")
        reporte.write("<th>Estado</th>")
        reporte.write("</tr>")
        #Escribir los datos
        for estudiante in estudiantes.values():
            promedio = estudiante.calcularPromedio()
            estado = "Aprobado" if promedio >= 61 else "Reprobado"
            stilo = "style = 'color: green'" if promedio >= 61 else "style = 'color: red'"
            reporte.write(f"<tr {stilo}>")
            reporte.write(f"<td>{estudiante.carnet}</td>")
            reporte.write(f"<td>{estudiante.nombre}</td>")
            reporte.write(f"<td>{promedio}</td>")
            reporte.write(f"<td>{estado}</td>")
            reporte.write("</tr>")
        #Escribir el pie
        reporte.write("</table>") 
        reporte.write("</body>")
        reporte.write("</html>")
        #Cerrar el informe
    reporte.close()

def bubbleSort(estudiantes):
    n = len(estudiantes)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if estudiantes[j].calcularPromedio() < estudiantes[j+1].calcularPromedio():
                estudiantes[j], estudiantes[j+1] = estudiantes[j+1], estudiantes[j]
    return estudiantes[:3]


def top3Estudiantes():
    global estudiantes
    #Crear el archivo
    with open("top3.html", "w", encoding="utf-8") as top3:
    #Escribir el encabezado
        top3.write("<html>")
        top3.write("<head>")
        top3.write("<title>Top 3 Estudiantes</title>")
        top3.write("</head>")
        top3.write("<body>")
        top3.write("<h1>Top 3 Estudiantes</h1>")
        top3.write("<table>")
        top3.write("<tr>")
        top3.write("<th>Carne</th>")
        top3.write("<th>Nombre</th>")
        top3.write("<th>Promedio</th>")
        top3.write("</tr>")
        #Escribir los datos
        for estudiante in bubbleSort(list(estudiantes.values())):
            promedio = estudiante.calcularPromedio()
            top3.write(f"<tr>")
            top3.write(f"<td>{estudiante.carnet}</td>")
            top3.write(f"<td>{estudiante.nombre}</td>")
            top3.write(f"<td>{promedio}</td>")
            top3.write("</tr>")
        #Escribir el pie
        top3.write("</table>") 
        top3.write("</body>")
        top3.write("</html>")
        #Cerrar el informe
    top3.close()

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
        reporteAprobacion()
        print("Revise el archivo .html" + "\n")
    elif opcion == "5":
        print("Creando informe, espere...." + "\n")
        top3Estudiantes()
        print("Revise el archivo .html" + "\n")
    elif opcion == "6":
        print("Saliendo..." + "\n")
        break
    else:
        print("Opción inválida. Por favor, elige una opción del menú." + "\n")

#Todo los derechos reservados 2024©