import tkinter as tk
import sympy as sp
import scipy.optimize as opt
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
    tk.Label(frameContenido, text="CALCULA RAÍCES DE FUNCIONES NO LINEALES",
             font=("Arial", 14, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="Ingrese la función f(x):", font=("Arial", 12, "bold"),
             fg="#00008B", bg="whitesmoke").pack()

    entry_function = tk.Entry(frameContenido, font=("Arial", 12), fg="#00008B", bg="whitesmoke")
    entry_function.insert(0, ejemploEcuacion)  # Muestra una ecuación como ejemplo de ingreso
    entry_function.bind("<FocusIn>", on_entry_focus_in)
    entry_function.bind("<FocusOut>", on_entry_focus_out)
    entry_function.pack()

    def newtonRaices():
        try:

            exprCadena = entry_function.get()
            x = sp.symbols('x')
            expr = sp.sympify(exprCadena)

            funcionlamdified = sp.lambdify(x, expr, 'numpy')
            primerad = sp.lambdify(x, sp.diff(expr, x), 'numpy')  # primera derivada

            # Para detectar logaritmos
            if 'log' in exprCadena or 'ln' in exprCadena:
                valoresx = np.linspace(0.01, 2, 10000)
            else:
                valoresx = np.linspace(-10, 10, 4000)

            # Evaluacción f(x)
            valoresy = funcionlamdified(valoresx)

            # Filtrado de valores válidos
            mascara_valida = np.isfinite(valoresy)
            valoresx = valoresx[mascara_valida]
            valoresy = valoresy[mascara_valida]

            ventanas = []
            #*****
            for x1, x2, y1, y2 in zip(valoresx[:-1], valoresx[1:], valoresy[:-1], valoresy[1:]):
                if y1 == 0:
                    ventanas.append(x1)
                elif y1 * y2 < 0:
                    x0 = (x1 + x2) / 2
                    try:
                        raiz = opt.newton(funcionlamdified, x0, fprime=primerad, tol=1e-10, maxiter=50)
                    except Exception:
                        raiz = x0  # En caso de error, usar punto medio
                    ventanas.append(raiz)

            # Revisamos el último valor
            if valoresy[-1] == 0:
                ventanas.append(valoresx[-1])

            # Eliminar raíces muy cercanas
            listav= []
            tol = 1e-5

            listav += [r for r in ventanas if not any(abs(r - existente) < tol for existente in listav)]

            if listav:
                resultados = " Raíces:\n" + "  ".join(f"{r:.6f}" for r in listav)
                ventanaLabel.config(text=resultados.strip(), font=("Arial", 12, "bold"))
            else:
                ventanaLabel.config(text="No tiene raíces")

            muestraPlot(expr, listav)

        except Exception as e:
            ventanaLabel.config(text=f"Error: Ingrese la ecuación correctamente", font=("Arial"),fg="red")

    def borrarGrafico():
        entry_function.delete(0, tk.END)
        ventanaLabel.config(text="")
        infoLabel.config(text="")
        for widget in canvasFrame.winfo_children():
            widget.destroy()

    # Botón Encontrar raíces
    tk.Button(
        frameContenido, text="Calcular raíces", command=newtonRaices,
        fg="white", bg="orange", font=("Arial", 12, "bold"),
        height=2, width=20
    ).pack(side="left", padx=50, pady = 20)

    # Botón Borrar grafico
    tk.Button(
        frameContenido, text="Borrar gráfico", command=borrarGrafico,
        fg="white", bg="orange", font=("Arial", 12, "bold"),
        height=2, width=20
    ).pack(side="left", padx=50, pady = 20)

def muestraPlot(exprFunc, ventanas):
    x = sp.symbols('x')
    funcionlamdified = sp.lambdify(x, exprFunc, 'numpy')

    valoresx = np.linspace(-10, 10, 400)
    valoresx_validos = valoresx[valoresx > 0]    # positivo
    valoresy = funcionlamdified(valoresx)

    fig, eje = plt.subplots(figsize=(10, 8))
    eje.plot(valoresx, valoresy, label=f'f(x) = {exprFunc}')

    eje.set_xticks(np.arange(-10, 11, 1))
    eje.set_yticks(np.arange(-10, 11, 1))

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
    
    for ventana in ventanas:
        eje.axvline(ventana, color='red', linestyle='--')
        eje.plot(ventana, 0, 'ro', markersize=8)

    eje.set_xlim([-10, 10])
    eje.set_ylim([-10, 10])
    eje.grid(True, linestyle='-', linewidth=0.5)
    #eje.grid(True)
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
    global frameContenido, ventanaLabel, infoLabel, canvasFrame
    limpiarFrame()
    for widget in canvasFrame.winfo_children():
        widget.destroy()

    ventanaLabel.config(text="")
    infoLabel.config(text="")

    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack() 
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack() 
    tk.Label(frameContenido, text="BIENVENIDOS A LA APLICACIÓN", font=("Comic Sans MS", 18, "bold"),
             fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="RAÍCES DE FUNCIONES NO LINEALES",
             font=("Arial", 14, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()

    try:
        image = Image.open("RootFinder.png")  
        image = image.resize((550, 400))  
        image_tk = ImageTk.PhotoImage(image)
        imageLabel = tk.Label(frameContenido, image=image_tk, bg="whitesmoke")
        imageLabel.image = image_tk
        imageLabel.pack(pady=20)
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="", font=("Arial", 12, "bold"), fg="#00008B", bg="whitesmoke").pack()
    tk.Label(frameContenido, text="RootFinder v1.0", font=("Comic Sans MS", 20, "bold"),
             fg="#00008B", bg="whitesmoke").pack()

def Ayuda():
    limpiarFrame()
    for widget in canvasFrame.winfo_children():
        widget.destroy()
        
    ventanaLabel.config(text="")
    infoLabel.config(text="")

    tk.Label(frameContenido, text="\n\nINSTRUCCIONES DE USO", bg="whitesmoke",
             font=("Comic Sans MS", 14,"bold"), fg="#00008B").pack(pady=20)
    tk.Label(frameContenido, text="RootFinder v1.0:\n\n", bg="whitesmoke",
             font=("Comic Sans MS", 14,"bold"), fg="#00008B").pack(pady=20)
    tk.Label(frameContenido, text="\n1. Ingresar la función en el cuadro correspondiente"
             f"\nEjemplos de Funciones validas\nx**3 - 2*x + 1\nsin(x) - x/2\n"
             f"2. Hacer un click en el boton 'Encontrar raíces'"
             f"\n3. Visualización gráfica\n4. Hacer un click en el botón Borrar gráfico",bg="whitesmoke",
             font=("Comic Sans MS", 14)).pack(pady=20)

def Acercade():
    limpiarFrame()
    for widget in canvasFrame.winfo_children():
        widget.destroy()
        
    ventanaLabel.config(text="")
    infoLabel.config(text="")

    tk.Label(frameContenido, text="\n\n\n\nCalcula raíces de funciones no lineales."
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

    labelAcercade = tk.Label(frameContenido, text= "\n\nLanzamiento : 1 de mayo  2025",
                              font=("Comic Sans MS", 14),fg="#003366",bg="whitesmoke")
    labelAcercade.pack(pady=(1,10))
    labelAcercade = tk.Label(frameContenido, text= "Contacto: lcoyla@unap.edu.pe",
                              font=("Comic Sans MSl", 14),fg="#003366",bg="whitesmoke")
    labelAcercade.pack(pady=(1,10))

def crearInterfaz():
    global frameContenido, ventanaLabel, infoLabel, canvasFrame

    ventana = tk.Tk()
    ventana.title("Busca raíces")
    ventana.geometry("1000x1000")
    ventana.config(bg="whitesmoke")

    menuBar = tk.Menu(ventana)
    ventana.config(menu=menuBar)

    menuBar.add_command(label="Presentación", command=Presentacion)
    menuBar.add_command(label="Encontrar raíces", command=encontrarRaices)
    menuBar.add_command(label="Ayuda", command=Ayuda)
    menuBar.add_command(label="Acerca de", command=Acercade)

    mainFrame = tk.Frame(ventana, bg="whitesmoke")
    mainFrame.pack(pady=10)

    frameContenido = tk.Frame(mainFrame, bg="whitesmoke")
    frameContenido.pack()

    ventanaLabel = tk.Label(mainFrame, text="", bg="whitesmoke")
    ventanaLabel.pack()

    infoLabel = tk.Label(mainFrame, text="", fg="blue", bg="whitesmoke")
    infoLabel.pack()

    canvasFrame = tk.Frame(mainFrame, bg="whitesmoke")
    canvasFrame.pack()
    
    encontrarRaices()

    ventana.mainloop()

def main():
    crearInterfaz()
    
if __name__ == "__main__":
    main()
