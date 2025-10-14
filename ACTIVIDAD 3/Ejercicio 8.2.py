from math import sqrt
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    tk = None
    messagebox = None


class Notas:
    def __init__(self, tamanio=5):
        self.lista_notas = [0.0] * tamanio

    def calcular_promedio(self):
        return sum(self.lista_notas) / len(self.lista_notas) if self.lista_notas else 0.0

    def calcular_desviacion(self):
        if not self.lista_notas:
            return 0.0
        promedio = self.calcular_promedio()
        suma_cuadrados = sum((n - promedio) ** 2 for n in self.lista_notas)
        return sqrt(suma_cuadrados / len(self.lista_notas))

    def calcular_menor(self):
        return min(self.lista_notas) if self.lista_notas else 0.0

    def calcular_mayor(self):
        return max(self.lista_notas) if self.lista_notas else 0.0


class VentanaPrincipal(tk.Tk if tk is not None else object):
    def __init__(self):
        if tk is None:
            raise RuntimeError("Tkinter no esta disponible en este entorno.")
        super().__init__()
        self.title("Notas")
        self.geometry("320x440")
        self.resizable(False, False)
        self.notas = Notas()
        self.campos_notas = []
        self._crear_componentes()

    def _crear_componentes(self):
        for i in range(5):
            etiqueta = tk.Label(self, text=f"Nota {i + 1}:")
            etiqueta.place(x=20, y=20 + i * 40)
            campo = tk.Entry(self, width=15)
            campo.place(x=100, y=20 + i * 40)
            self.campos_notas.append(campo)
        # Botones
        tk.Button(self, text="Calcular", command=self._calcular_resultados).place(x=30, y=250)
        tk.Button(self, text="Limpiar", command=self._limpiar_campos).place(x=160, y=250)
        # Etiquetas de salida
        self.etiqueta_promedio = tk.Label(self, text="Promedio = ")
        self.etiqueta_promedio.place(x=20, y=300)
        self.etiqueta_desviacion = tk.Label(self, text="Desviacion = ")
        self.etiqueta_desviacion.place(x=20, y=330)
        self.etiqueta_mayor = tk.Label(self, text="Nota mayor = ")
        self.etiqueta_mayor.place(x=20, y=360)
        self.etiqueta_menor = tk.Label(self, text="Nota menor = ")
        self.etiqueta_menor.place(x=20, y=390)

    def _obtener_notas(self):
        try:
            for i, campo in enumerate(self.campos_notas):
                valor = float(campo.get().strip())
                self.notas.lista_notas[i] = valor
            return True
        except ValueError:
            if messagebox:
                messagebox.showerror("Error", "Todos los campos deben contener numeros validos.")
            return False

    def _calcular_resultados(self):
        if not self._obtener_notas():
            return
        self.etiqueta_promedio.config(text=f"Promedio = {self.notas.calcular_promedio():.2f}")
        self.etiqueta_desviacion.config(text=f"Desviacion = {self.notas.calcular_desviacion():.2f}")
        self.etiqueta_mayor.config(text=f"Nota mayor = {self.notas.calcular_mayor():.2f}")
        self.etiqueta_menor.config(text=f"Nota menor = {self.notas.calcular_menor():.2f}")

    def _limpiar_campos(self):
        for campo in self.campos_notas:
            campo.delete(0, tk.END)
        for etiqueta in [
            self.etiqueta_promedio,
            self.etiqueta_desviacion,
            self.etiqueta_mayor,
            self.etiqueta_menor,
        ]:
            etiqueta.config(text=etiqueta.cget("text").split("=")[0].strip() + " = ")


# Para ejecutar la aplicacion (si tkinter esta disponible):
if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
