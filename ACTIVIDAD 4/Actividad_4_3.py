import tkinter as tk
from tkinter import messagebox
import math


# =========================================================
# Clase que contiene los métodos estáticos solicitados
# =========================================================
class CalculosNumericos:

    @staticmethod
    def logaritmo_neperiano(valor):
        
        if valor <= 0:
            raise ArithmeticError("Error: El valor debe ser positivo para calcular el logaritmo.")
        return math.log(valor)

    @staticmethod
    def raiz_cuadrada(valor):
        
        if valor < 0:
            raise ArithmeticError("Error: El valor debe ser positivo para calcular la raíz cuadrada.")
        return math.sqrt(valor)


# =========================================================
# Clase que maneja la interfaz gráfica
# =========================================================
class InterfazGrafica:

    def __init__(self):
        """ Constructor: crea la ventana e inicializa los elementos gráficos. """
        self.ventana = tk.Tk()
        self.ventana.title("Cálculos Numéricos")
        self.ventana.geometry("300x260")

        # Etiqueta
        tk.Label(self.ventana, text="Ingrese un número:").pack(pady=10)

        # Campo de entrada
        self.campo_entrada = tk.Entry(self.ventana)
        self.campo_entrada.pack()

        # Botones de cálculo
        tk.Button(self.ventana, text="Calcular ln(x)", command=self.calcular_log).pack(pady=5)
        tk.Button(self.ventana, text="Calcular √x", command=self.calcular_raiz).pack(pady=5)

        # Botón para limpiar el campo
        tk.Button(self.ventana, text="Limpiar", command=self.limpiar_campo).pack(pady=10)

    def obtener_valor(self):
        
        return float(self.campo_entrada.get())

    def calcular_log(self):
        """ Llama al método estático para calcular logaritmo y muestra resultado. """
        try:
            numero = self.obtener_valor()
            resultado = CalculosNumericos.logaritmo_neperiano(numero)
            messagebox.showinfo("Resultado", f"Logaritmo neperiano: {resultado}")
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número válido.")
        except ArithmeticError as e:
            messagebox.showerror("Error", str(e))

    def calcular_raiz(self):
        """ Llama al método estático para calcular raíz cuadrada y muestra resultado. """
        try:
            numero = self.obtener_valor()
            resultado = CalculosNumericos.raiz_cuadrada(numero)
            messagebox.showinfo("Resultado", f"Raíz cuadrada: {resultado}")
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número válido.")
        except ArithmeticError as e:
            messagebox.showerror("Error", str(e))

    def limpiar_campo(self):
        """ Limpia el campo de entrada y coloca el cursor nuevamente en él. """
        self.campo_entrada.delete(0, tk.END)
        self.campo_entrada.focus()

    def ejecutar(self):
        """ Ejecuta el ciclo principal de la ventana (mainloop). """
        self.ventana.mainloop()


# =========================================================
# Punto de entrada del programa
# =========================================================
if __name__ == "__main__":
    app = InterfazGrafica()
    app.ejecutar()
