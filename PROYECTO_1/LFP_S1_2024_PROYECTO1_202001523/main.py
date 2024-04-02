from analyzer import Analyzer
import tkinter as tk
from tkinter import filedialog
from generador import leer_documento, crear_html, formatear
import webbrowser

analyzer = None
tex = None
filepath = None

def load_file():
    global analyzer
    global text
    global filepath
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            analyzer = Analyzer(text)
            analyzer.analyze()
            print("====================== Tokens ======================")
            for token in analyzer.tokens:
                print(token)
            print("===================== Errores ======================")
            for error in analyzer.errors:
                print(error)
            textbox.delete("1.0", tk.END)
            textbox.insert(tk.END, text)

def traducir():
    analyzer.getTokens()
    leer_documento(text)
    crear_html("html.html")
    generarTexto()
    abrir_archivos()


def abrir_archivos():
    webbrowser.open_new_tab("html.html")
    webbrowser.open_new_tab("tokens.html")

def reiniciar():
    global analyzer
    global text
    global filepath
    analyzer = None
    text = None
    filepath = None
    formatear()
    textbox.delete("1.0", tk.END)
    html_textbox.delete("1.0", tk.END)
    

def generarTexto():
    with open("html.html", "r", encoding="utf-8") as html_file:
        html_text = html_file.read()
        html_textbox.insert(tk.END, html_text)


root = tk.Tk()
root.title("Traductor HTML")
root.resizable(False,False)
root.config(cursor="hand2")
root.geometry("1200x720")
root.config(bg="SlateBlue1")
root.config(bd="30")
root.config(relief="groove")


html_textbox = tk.Text(root, height=30, width=60)
html_textbox.pack(side=tk.RIGHT)

textbox = tk.Text(root, height=30, width=60)
textbox.pack(side=tk.LEFT)



button2 = tk.Button(root, text="Traducir", command=traducir,font=("Arial", 15))

button3 = tk.Button(root, text="Salir", command=root.quit, font=("Arial", 15))
button3.pack(side=tk.BOTTOM)
button4 = tk.Button(root, text="Reiniciar", command=reiniciar, font=("Arial", 15))

button = tk.Button(root, text="Cargar archivo", command=load_file, font=("Arial", 15))

button4.pack()
button.pack()
button2.pack()
button3.pack()  
textbox.pack()
html_textbox.pack()
root.mainloop()

