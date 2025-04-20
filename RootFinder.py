import tkinter as tk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import PhotoImage
from PIL import Image, ImageTk

ejemploEcuacion = "x**2 - 3*x - 2"
entry_function = None

def on_entry_focus_in(event):
    if entry_function.get() == ejemploEcuacion:
        entry_function.delete(0, tk.END)
        entry_function.config(fg="black")

def on_entry_focus_out(event):
    if entry_function.get().strip() == "":
        entry_function.insert(0, ejemploEcuacion)
        entry_function.config(fg="gray")

def encontrarRaices():
    global entry_function
    limpiarFrame()
    for widget in canvasFrame.winfo_children():
        widget.destroy()
    
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="CALCULA LA RAÍZ DE UNA ECUACIÓN POLINÓMICA NO LINEAL", font=("Arial", 14, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="Ingrese la función f(x):", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()

    entry_function = tk.Entry(frameContenido, font=("Arial", 12), fg="#00008B", bg="whitesmoke")
    entry_function.insert(0, ejemploEcuacion)  # Muestra una ecuación como ejemplo de ingreso
    entry_function.bind("<FocusIn>", on_entry_focus_in)
    entry_function.bind("<FocusOut>", on_entry_focus_out)
    entry_function.pack()

    def calcular():
        try:
            expr_str = entry_function.get()
            x = sp.symbols('x')
            expr = sp.sympify(expr_str)

            f_lambdified = sp.lambdify(x, expr, 'numpy')

            x_vals = np.linspace(-10, 10, 400)
            y_vals = f_lambdified(x_vals)

            roots = []
            for i in range(len(x_vals) - 1):
                if y_vals[i] * y_vals[i + 1] < 0:
                    root_approx = (x_vals[i] + x_vals[i + 1]) / 2
                    roots.append(root_approx)

            if roots:
                rootLabel.config(text=f"Raíces encontradas: {', '.join(map(lambda r: f'{r:.4f}', roots))}", font=("Arial", 12, "bold"))
            else:
                rootLabel.config(text="No se encontraron raíces en el intervalo.")

            funcionPlot(expr, roots)

        except Exception as e:
            rootLabel.config(text=f"Error: Ingrese la ecuación correctamente", font=("Arial"),fg="red")

    def borrarGrafico():
        entry_function.delete(0, tk.END)
        rootLabel.config(text="")
        infoLabel.config(text="")
        for widget in canvasFrame.winfo_children():
            widget.destroy()
    # Botón 1
    tk.Button(
        frameContenido, text="Encontrar Raíces", command=calcular,
        fg="white", bg="orange", font=("Arial", 12, "bold"),
        height=2, width=20
    ).pack(side="left", padx=50, pady = 20)

    # Botón 2
    tk.Button(
        frameContenido, text="Borrar Gráfico", command=borrarGrafico,
        fg="white", bg="orange", font=("Arial", 12, "bold"),
        height=2, width=20
    ).pack(side="left", padx=50, pady = 20)

def funcionPlot(expr, roots):
    x = sp.symbols('x')
    f_lambdified = sp.lambdify(x, expr, 'numpy')

    x_vals = np.linspace(-10, 10, 400)
    y_vals = f_lambdified(x_vals)

    fig, eje = plt.subplots(figsize=(8, 6))
    eje.plot(x_vals, y_vals, label=f'f(x) = {expr}')
    # Color de ejes
    eje.axhline(0, color='darkgray', linewidth=1.5)
    eje.axvline(0, color='darkgray', linewidth=1.5)
    #Color de etiqueta en el eje
    eje.set_xlabel("Eje X", color ='blue')
    eje.set_ylabel("Eje Y", color ='blue')
    #Color de fondo
    fig.patch.set_facecolor("whitesmoke")
    eje.set_facecolor("whitesmoke")
    #Color de numeros en los ejes
    eje.tick_params(axis='x', colors='black')
    eje.tick_params(axis='y', colors='black')
    
    for root in roots:
        eje.axvline(root, color='red', linestyle='--')
        eje.plot(root, 0, 'ro', markersize=8)

    eje.set_xlim([-10, 10])
    eje.set_ylim([-10, 10])
    eje.grid(True, linestyle='--', linewidth=1)
    eje.legend()

    for widget in canvasFrame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvasFrame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def limpiarFrame():
    for widget in frameContenido.winfo_children():
        widget.destroy()

def Presentacion():
    limpiarFrame()
    for widget in canvasFrame.winfo_children():
        widget.destroy()

    rootLabel.config(text="")
    infoLabel.config(text="")

    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack() 
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack() 
    tk.Label(frameContenido, text="BIENVENIDOS A LA APLICACIÓN", font=("Comic Sans MS", 14, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="RAÍCES DE UNA ECUACIÓN POLINÓMICA NO LINEAL", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()

    try:
        image = Image.open("RootFinder.png")  
        image = image.resize((400, 400))  
        image_tk = ImageTk.PhotoImage(image)
        imageLabel = tk.Label(frameContenido, image=image_tk, bg="whitesmoke")
        imageLabel.image = image_tk
        imageLabel.pack(pady=20)
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="RootFinder v1.0", font=("Comic Sans MS", 20, "bold"), fg="#00008B", bg="whitesmoke").pack()

def Ayuda():
    limpiarFrame()
    for widget in canvasFrame.winfo_children():
        widget.destroy()
        
    rootLabel.config(text="")
    infoLabel.config(text="")

    tk.Label(frameContenido, text="\n\nINSTRUCCIONES DE USO", bg="whitesmoke", font=("Comic Sans MS", 14,"bold"), fg="#00008B").pack(pady=20)
    tk.Label(frameContenido, text="RootFinder v1.0:\n\n", bg="whitesmoke", font=("Comic Sans MS", 14,"bold"), fg="#00008B").pack(pady=20)
    tk.Label(frameContenido, text="\n1. Ingresar la función en el cuadro correspondiente"
             f"\nEjemplos de Funciones validas\nx**3 - 2*x + 1\nsin(x) - x/2\n"
             f"2. Hacer un click en el boton 'Encontrar raíces'"
             f"\n3. Visualización gráfica\n4. Hacer un click en el botón Borrar gráfico",bg="whitesmoke", font=("Comic Sans MS", 14)).pack(pady=20)

def Acercade():
    limpiarFrame()
    for widget in canvasFrame.winfo_children():
        widget.destroy()
        
    rootLabel.config(text="")
    infoLabel.config(text="")

    tk.Label(frameContenido, text="\n\n\n\nCálculo de racíces de ecuciones no lineales."
             f"\nRootFinder v1.0", bg="whitesmoke", font=("Comic Sans MS", 14,"bold"), fg="#00008B").pack(pady=20)
    
    textos = [
        "\nDesarrollado por: Leonel Coyla Idme",
        "Alfredo Mamani Canqui",
        "Elqui Yeye Pari Condori",
        "Juan Reynaldo Paredes Quispe",
        "José Pánfilo Tito Lipa",
    ]

    for texto in textos:
        tk.Label(frameContenido, text=texto, bg="whitesmoke", font=("Comic Sans MS", 14)).pack(pady=4)

    labelAcerca_de = tk.Label(frameContenido, text= "\n\nLanzamiento : 11 de abril  2025", font=("Comic Sans MS", 14),fg="#003366",bg="whitesmoke")
    labelAcerca_de.pack(pady=(1,10))
    labelAcerca_de = tk.Label(frameContenido, text= "Contacto: lcoyla@unap.edu.pe", font=("Comic Sans MSl", 14),fg="#003366",bg="whitesmoke")
    labelAcerca_de.pack(pady=(1,10))

def crearInterfaz():
    global frameContenido, rootLabel, infoLabel, canvasFrame

    root = tk.Tk()
    root.title("Busca Raíces")
    root.geometry("900x900")
    root.config(bg="whitesmoke")

    menuBar = tk.Menu(root)
    root.config(menu=menuBar)

    menuBar.add_command(label="Presentación", command=Presentacion)
    menuBar.add_command(label="Encontrar raíces", command=encontrarRaices)
    menuBar.add_command(label="Ayuda", command=Ayuda)
    menuBar.add_command(label="Acerca de", command=Acercade)

    mainFrame = tk.Frame(root, bg="whitesmoke")
    mainFrame.pack(pady=10)

    frameContenido = tk.Frame(mainFrame, bg="whitesmoke")
    frameContenido.pack()

    rootLabel = tk.Label(mainFrame, text="", bg="whitesmoke")
    rootLabel.pack()

    infoLabel = tk.Label(mainFrame, text="", fg="blue", bg="whitesmoke")
    infoLabel.pack()

    canvasFrame = tk.Frame(mainFrame, bg="whitesmoke")
    canvasFrame.pack()
    
    encontrarRaices()

    root.mainloop()

def main():
    crearInterfaz()

if __name__ == "__main__":
    main()
