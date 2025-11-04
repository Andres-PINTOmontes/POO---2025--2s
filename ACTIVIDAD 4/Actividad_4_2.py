import tkinter as tk
from tkinter import ttk

class Vendedor:
    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = None

    def verificacion_edad(self, edad):
        if edad < 18:
            raise ValueError("El vendedor debe ser mayor de 18 años.")
        if edad < 0 or edad > 120:
            raise ValueError("La edad no puede ser negativa ni mayor a 120.")
        self.edad = edad

    def imprimir(self):
        return f"Nombre: {self.nombre}\nApellidos: {self.apellidos}\nEdad: {self.edad}"

class VendedorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Vendedor")
        self.root.configure(padx=15, pady=15)

        ttk.Label(self.root, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self.root, width=25)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        self.entry_nombre.focus()

        ttk.Label(self.root, text="Apellidos:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_apellido = ttk.Entry(self.root, width=25)
        self.entry_apellido.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Edad:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_edad = ttk.Entry(self.root, width=25)
        self.entry_edad.grid(row=2, column=1, padx=5, pady=5)

        frame_botones = ttk.Frame(self.root)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(frame_botones, text="Registrar", command=self.registrar_vendedor).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=10)

        self.resultado_label = ttk.Label(self.root, text="", justify="left")
        self.resultado_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    def registrar_vendedor(self):
        self.resultado_label.config(text="")
        try:
            nombre = self.entry_nombre.get()
            apellidos = self.entry_apellido.get()
            edad_texto = self.entry_edad.get()

            if not nombre or not apellidos or not edad_texto:
                raise ValueError("Todos los campos son obligatorios.")

            edad = int(edad_texto)
            vendedor = Vendedor(nombre, apellidos)
            vendedor.verificacion_edad(edad)

            datos_vendedor = vendedor.imprimir()
            self.resultado_label.config(text=datos_vendedor)

        except ValueError as ve:
            self.resultado_label.config(text=f"Error: {ve}")

    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.resultado_label.config(text="")
        self.entry_nombre.focus()


# Clase que actúa como punto de entrada principal del programa
class Principal:
    @staticmethod
    def main():
  
        root = tk.Tk()
        app = VendedorApp(root) 
        root.mainloop()

# Puerta de entrada que ejecuta el método main de la clase Principal
if __name__ == "__main__":
    Principal.main()
    