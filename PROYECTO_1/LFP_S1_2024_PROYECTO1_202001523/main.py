from analyzer import Analyzer
import tkinter as tk
from tkinter import filedialog
from generador import leer_documento, crear_html

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
    """leer_documento(text)
    crear_html("html.html")"""
    


root = tk.Tk()
root.title("Traducto HTML")
root.resizable(False,False)
root.config(cursor="hand2")
root.geometry("1200x600")
root.config(bg="SlateBlue1")
root.config(bd="30")
root.config(relief="groove")


textbox = tk.Text(root, height=10, width=50)
textbox.pack()

button2 = tk.Button(root, text="Traducir", command=traducir)

button = tk.Button(root, text="Cargar archivo", command=load_file)
button.pack()
button2.pack()

root.mainloop()

