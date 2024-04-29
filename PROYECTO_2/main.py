from analyzer import Analyzer
from token_1 import Token
from Parser import Parser
import tkinter as tk
from tkinter import filedialog
import webbrowser

analyzer = None
tex = None
file_path = None
Lista_t = Token

def load_file():
    global analyzer
    global text
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Archivo de Entrada", "")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            analyzer = Analyzer(text)
            analyzer.analyze()
            analyzer.generate_html()
            print("====================== Tokens ======================")
            for token in analyzer.tokens:
                print(token)
            print("===================== Errores ======================")
            for error in analyzer.errors:
                print(error)
            parser = Parser(analyzer.tokens)
            parser.parse()
            print("===================== Errores Sintacticos =====================")
            for error in parser.errors:
                print(error)
            parser.generate_html()
            
            textbox.config(state=tk.NORMAL)
            textbox.delete("1.0", tk.END)
            textbox.insert(tk.END, text)
            tk.messagebox.showinfo("Mensaje", "¡Se ha cargado el archivo de entrada!")


def save_file():
    global analyzer
    global text
    global file_path
    if analyzer:
        if not file_path:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de Salida", "")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as file:
                text = textbox.get("1.0", tk.END)
                file.write(text)
                tk.messagebox.showinfo("Mensaje", "¡Se ha guardado el archivo de entrada!")

def save():
    global file_path
    with open(file_path, "w", encoding="utf-8") as file:
        text = textbox.get("1.0", tk.END)
        file.write(text)
        file.close()
        print("Se ha guardado el archivo de entrada!")
        tk.messagebox.showinfo("Mensaje", "¡Se ha guardado el archivo de entrada!")

def abrir_lexico():
    webbrowser.open_new_tab("Informe_Lexico.html")

def abrir_sintactico():
    webbrowser.open_new_tab("Informe_Sintactico.html")


def generarTexto():
    with open("html.html", "r", encoding="utf-8") as html_file:
        html_text = html_file.read()
        html_textbox.insert(tk.END, html_text)
        


root = tk.Tk()
root.title("PROYECTO 2 LFP")
root.resizable(False,False)
root.config(cursor="hand2")
root.geometry("1200x720")
root.config(bg="SlateBlue1")
root.config(bd="30")
root.config(relief="groove")



menu_principal = tk.Menu(root)

# Crear un menú desplegable
menu_desplegable = tk.Menu(menu_principal, tearoff=0)
menu_desplegable.add_command(label="Informe Lexico", command=abrir_lexico)
menu_desplegable.add_command(label="Informe Sintactico", command=abrir_sintactico)

# Añadir el menú desplegable al menú principal
menu_principal.add_cascade(label="Reportes", menu=menu_desplegable)

# Configurar la ventana para usar el menú principal
root.config(menu=menu_principal)

html_textbox = tk.Text(root, height=30, width=60)
html_textbox.pack(side=tk.RIGHT)

textbox = tk.Text(root, height=30, width=60)
textbox.pack(side=tk.LEFT)


button1 = tk.Button(root, text="Guardar Como", command= save_file , font=("Arial", 13))
button2 = tk.Button(root, text="Guardar", command= save , font=("Arial", 13))
button3 = tk.Button(root, text="Salir", command=root.quit, font=("Arial", 13))
button3.pack(side=tk.BOTTOM)
button = tk.Button(root, text="Cargar archivo", command=load_file, font=("Arial", 13))


button.place(x=10, y=10)  
button1.place(x=200, y=10)
button2.place(x=350, y=10)
textbox.pack()
html_textbox.pack()
root.mainloop()

