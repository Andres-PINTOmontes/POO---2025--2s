"""
Aplicación de agenda de contactos en una sola ventana.

Campos de un contacto:
- Nombres
- Apellidos
- Fecha de nacimiento (formato AAAA-MM-DD)
- Dirección
- Teléfono
- Correo

Al oprimir el botón "Agregar":
- Se valida que no haya campos vacíos.
- Se crea un contacto y se guarda en memoria.
- Se añade una representación de texto a una Listbox en la parte inferior.
- Se limpian los campos para ingresar un nuevo contacto.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import datetime
from typing import List


# ==========================
#  MODELO
# ==========================

@dataclass
class Contacto:
    nombres: str
    apellidos: str
    fecha_nacimiento: datetime.date
    direccion: str
    telefono: str
    correo: str

    def resumen(self) -> str:
        """Cadena que se mostrará en la lista gráfica."""
        fecha_str = self.fecha_nacimiento.strftime("%Y-%m-%d")
        return (
            f"{self.nombres} {self.apellidos} | "
            f"Fecha nac.: {fecha_str} | "
            f"Tel: {self.telefono} | "
            f"Correo: {self.correo}"
        )


# ==========================
#  APLICACIÓN (GUI)
# ==========================

class VentanaContactoApp:
    FORMATO_FECHA = "%Y-%m-%d"  # AAAA-MM-DD

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Agenda de contactos")
        self.root.geometry("650x420")

        self.contactos: List[Contacto] = []

        self._crear_componentes()

    # ---------- GUI ----------

    def _crear_componentes(self) -> None:
        # Contenedor principal (como VBox en JavaFX)
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Grid para etiquetas y campos
        grid = ttk.Frame(main_frame)
        grid.pack(fill=tk.X, pady=5)

        # Etiquetas
        ttk.Label(grid, text="Nombres:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        ttk.Label(grid, text="Apellidos:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        ttk.Label(grid, text="Fecha nacimiento (AAAA-MM-DD):").grid(
            row=2, column=0, sticky="e", padx=5, pady=3
        )
        ttk.Label(grid, text="Dirección:").grid(row=3, column=0, sticky="e", padx=5, pady=3)
        ttk.Label(grid, text="Teléfono:").grid(row=4, column=0, sticky="e", padx=5, pady=3)
        ttk.Label(grid, text="Correo:").grid(row=5, column=0, sticky="e", padx=5, pady=3)

        # Campos de texto
        self.entry_nombres = ttk.Entry(grid, width=40)
        self.entry_apellidos = ttk.Entry(grid, width=40)
        self.entry_fecha = ttk.Entry(grid, width=20)
        self.entry_direccion = ttk.Entry(grid, width=40)
        self.entry_telefono = ttk.Entry(grid, width=25)
        self.entry_correo = ttk.Entry(grid, width=40)

        self.entry_nombres.grid(row=0, column=1, sticky="w", padx=5, pady=3)
        self.entry_apellidos.grid(row=1, column=1, sticky="w", padx=5, pady=3)
        self.entry_fecha.grid(row=2, column=1, sticky="w", padx=5, pady=3)
        self.entry_direccion.grid(row=3, column=1, sticky="w", padx=5, pady=3)
        self.entry_telefono.grid(row=4, column=1, sticky="w", padx=5, pady=3)
        self.entry_correo.grid(row=5, column=1, sticky="w", padx=5, pady=3)

        # Botón Agregar
        btn_agregar = ttk.Button(main_frame, text="Agregar", command=self._agregar_contacto)
        btn_agregar.pack(pady=10)

        # Listbox (equivalente a ListView) para mostrar contactos
        lista_frame = ttk.LabelFrame(main_frame, text="Contactos")
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.listbox_contactos = tk.Listbox(lista_frame, height=10)
        self.listbox_contactos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.listbox_contactos.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        self.listbox_contactos.config(yscrollcommand=scrollbar.set)

    # ---------- LÓGICA ----------

    def _parsear_fecha(self, texto: str):
        try:
            return datetime.strptime(texto, self.FORMATO_FECHA).date()
        except ValueError:
            raise ValueError(
                "Fecha de nacimiento inválida. "
                "Use el formato AAAA-MM-DD, por ejemplo 2003-05-21."
            )

    def _agregar_contacto(self) -> None:
        try:
            nombres = self.entry_nombres.get().strip()
            apellidos = self.entry_apellidos.get().strip()
            fecha_txt = self.entry_fecha.get().strip()
            direccion = self.entry_direccion.get().strip()
            telefono = self.entry_telefono.get().strip()
            correo = self.entry_correo.get().strip()

            # Validaciones básicas
            if not (nombres and apellidos and fecha_txt and direccion and telefono and correo):
                raise ValueError("No se permiten campos vacíos.")

            fecha_nacimiento = self._parsear_fecha(fecha_txt)

            contacto = Contacto(
                nombres=nombres,
                apellidos=apellidos,
                fecha_nacimiento=fecha_nacimiento,
                direccion=direccion,
                telefono=telefono,
                correo=correo,
            )
            self.contactos.append(contacto)

            # Añadir a la lista gráfica
            self.listbox_contactos.insert(tk.END, contacto.resumen())

            # Limpiar campos
            self.entry_nombres.delete(0, tk.END)
            self.entry_apellidos.delete(0, tk.END)
            self.entry_fecha.delete(0, tk.END)
            self.entry_direccion.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
            self.entry_correo.delete(0, tk.END)

            messagebox.showinfo(
                "Contacto agregado",
                "Los datos del contacto se han registrado correctamente.",
            )

        except ValueError as e:
            messagebox.showerror("Error en los datos", str(e))

    # ---------- Bucle principal ----------

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = VentanaContactoApp()
    app.run()
