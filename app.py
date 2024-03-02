from tkinter.filedialog import askopenfilename

def cargarEstudiantes():
    ruta =askopenfilename()
    archivo= open(ruta,"r")
    archivo.close()
    print("========Archivo Cargado exitosamente!!========== \n")

def cargarCali():    
    ruta =askopenfilename()
    archivo= open(ruta,"r")
    archivo.close()
    print("========Archivo Cargado exitosamente!!========== \n")


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
        #informeInventario()
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
        print("Opción inválida. Por favor, elige una opción del menú.")

#Todo los derechos reservados 2024©