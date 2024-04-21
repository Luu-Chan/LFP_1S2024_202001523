from analyzer import Analyzer
import tkinter as tk
from tkinter import filedialog
import webbrowser

analyzer = None
tex = None
filepath = None

def load_file():
    global analyzer
    global text
    global filepath
    file_path = filedialog.askopenfilename(filetypes=[("Archivo de Entrada", "")])
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
            tk.messagebox.showinfo("Mensaje", "¡Se ha cargado el archivo de entrada!")



def abrir_archivos():
    webbrowser.open_new_tab("html.html")
    webbrowser.open_new_tab("tokens.html")


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


button3 = tk.Button(root, text="Salir", command=root.quit, font=("Arial", 15))
button3.pack(side=tk.BOTTOM)


button = tk.Button(root, text="Cargar archivo", command=load_file, font=("Arial", 15))

button.pack()
button3.pack()  
textbox.pack()
html_textbox.pack()
root.mainloop()

