import tkinter as tk
from tkinter import messagebox


# ==========================================================
# Clase Programador
# ==========================================================
class Programador:
    def __init__(self, nombre, apellido):
        
        self.nombre = nombre
        self.apellido = apellido


# ==========================================================
# Clase EquipoProgramadores
# ==========================================================
class EquipoProgramadores:

    def __init__(self, nombre_equipo, universidad, lenguaje, tamano):
        
        self.nombre_equipo = nombre_equipo
        self.universidad = universidad
        self.lenguaje = lenguaje
        self.tamano = tamano
        self.programadores = []  # Lista que almacenará objetos Programador

    def equipo_completo(self):
        
        return len(self.programadores) >= self.tamano

    def validar_nombre(self, texto):
       
        if not texto.isalpha():
            raise ValueError("El nombre o apellido solo puede contener letras.")
        if len(texto) >= 20:
            raise ValueError("El texto no puede tener 20 caracteres o más.")

    def agregar_programador(self, nombre, apellido):
        
        if self.equipo_completo():
            raise OverflowError("El equipo ya tiene el número máximo de programadores.")
        self.validar_nombre(nombre)
        self.validar_nombre(apellido)
        self.programadores.append(Programador(nombre, apellido))


# ==========================================================
# Clase que maneja la GUI con Tkinter (equivalente a main)
# ==========================================================
class InterfazGrafica:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Registro de Equipo - Maratón")
        self.ventana.geometry("350x450")

        # Campos del equipo
        tk.Label(self.ventana, text="Nombre del equipo:").pack()
        self.entry_equipo = tk.Entry(self.ventana)
        self.entry_equipo.pack()

        tk.Label(self.ventana, text="Universidad:").pack()
        self.entry_universidad = tk.Entry(self.ventana)
        self.entry_universidad.pack()

        tk.Label(self.ventana, text="Lenguaje que usarán:").pack()
        self.entry_lenguaje = tk.Entry(self.ventana)
        self.entry_lenguaje.pack()

        tk.Label(self.ventana, text="Tamaño del equipo (2-3):").pack()
        self.entry_tamano = tk.Entry(self.ventana)
        self.entry_tamano.pack()

        tk.Button(self.ventana, text="Crear equipo", command=self.crear_equipo).pack(pady=8)

        # Campos para programadores
        tk.Label(self.ventana, text="Nombre programador:").pack()
        self.entry_nombre_prog = tk.Entry(self.ventana)
        self.entry_nombre_prog.pack()

        tk.Label(self.ventana, text="Apellido programador:").pack()
        self.entry_apellido_prog = tk.Entry(self.ventana)
        self.entry_apellido_prog.pack()

        tk.Button(self.ventana, text="Añadir programador", command=self.agregar_programador).pack(pady=8)
        tk.Button(self.ventana, text="Salir", command=self.ventana.destroy).pack(pady=8)

        self.equipo = None  # Aún no existe hasta que el usuario lo cree

    # ======================================================
    def crear_equipo(self):
        
        try:
            nombre = self.entry_equipo.get()
            uni = self.entry_universidad.get()
            lenguaje = self.entry_lenguaje.get()
            tamano = int(self.entry_tamano.get())

            if tamano < 2 or tamano > 3:
                raise ValueError("El tamaño del equipo debe ser 2 o 3.")

            self.equipo = EquipoProgramadores(nombre, uni, lenguaje, tamano)
            messagebox.showinfo("Éxito", "¡Equipo creado correctamente!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ======================================================
    def agregar_programador(self):
        
        if self.equipo is None:
            messagebox.showerror("Error", "Primero debe crear el equipo.")
            return

        try:
            nombre = self.entry_nombre_prog.get()
            apellido = self.entry_apellido_prog.get()
            self.equipo.agregar_programador(nombre, apellido)
            messagebox.showinfo("OK", f"Programador añadido ({len(self.equipo.programadores)}/{self.equipo.tamano})")

            # Limpia campos
            self.entry_nombre_prog.delete(0, tk.END)
            self.entry_apellido_prog.delete(0, tk.END)

            if self.equipo.equipo_completo():
                messagebox.showinfo("Equipo completo", "Ya no se pueden agregar más programadores.")
                self.mostrar_resumen_equipo()

        except (ValueError, OverflowError) as e:
            messagebox.showerror("Error", str(e))

    # ======================================================
    def mostrar_resumen_equipo(self):
        
        resumen = tk.Toplevel(self.ventana)
        resumen.title("Resumen del equipo")
        resumen.geometry("350x300")

        tk.Label(resumen, text="✅ EQUIPO REGISTRADO", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(resumen, text=f"Nombre del equipo: {self.equipo.nombre_equipo}").pack()
        tk.Label(resumen, text=f"Universidad: {self.equipo.universidad}").pack()
        tk.Label(resumen, text=f"Lenguaje: {self.equipo.lenguaje}").pack()
        tk.Label(resumen, text=f"Tamaño: {self.equipo.tamano} programadores").pack(pady=5)

        tk.Label(resumen, text="👨‍💻 Integrantes:", font=("Arial", 10, "bold")).pack()
        for idx, prog in enumerate(self.equipo.programadores, start=1):
            tk.Label(resumen, text=f"{idx}. {prog.nombre} {prog.apellido}").pack()

        tk.Button(resumen, text="Cerrar", command=resumen.destroy).pack(pady=10)

    # ======================================================
    def ejecutar(self):
        
        self.ventana.mainloop()


# ==========================================================
# Punto de entrada principal (main)
# ==========================================================
if __name__ == "__main__":
    app = InterfazGrafica()
    app.ejecutar()
