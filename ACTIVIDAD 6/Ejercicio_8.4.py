"""
Aplicación de nómina con interfaz gráfica (Tkinter).

- Menú:
    * Agregar empleado
    * Calcular nómina
    * Guardar archivo
    * Salir

- Usa diálogos de mensaje, advertencia, confirmación y selección de carpeta.
"""

import os
from enum import Enum
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# ==========================
#  MODELO
# ==========================

class TipoCargo(Enum):
    DIRECTIVO = "Directivo"
    ESTRATEGICO = "Estratégico"
    OPERATIVO = "Operativo"


class TipoGenero(Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


class Empleado:
    """Modelo de un empleado de la empresa."""

    def __init__(
        self,
        nombre: str,
        apellidos: str,
        cargo: TipoCargo,
        genero: TipoGenero,
        salario_dia: float,
        dias_trabajados: int,
        otros_ingresos: float,
        pagos_salud: float,
        aporte_pensiones: float,
    ):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pensiones = aporte_pensiones

    @property
    def salario_mensual(self) -> float:
        """
        Salario mensual = (días trabajados * sueldo por día)
                          + otros ingresos
                          - pagos por salud
                          - aporte pensiones
        """
        return (
            self.dias_trabajados * self.salario_dia
            + self.otros_ingresos
            - self.pagos_salud
            - self.aporte_pensiones
        )


class NominaApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nómina de empleados")
        self.root.geometry("700x400")

        self.empleados: list[Empleado] = []

        self._crear_menu()
        self._crear_estado()

    # ---------- Menú y barra de estado ----------

    def _crear_menu(self):
        menubar = tk.Menu(self.root)

        menu_principal = tk.Menu(menubar, tearoff=0)
        menu_principal.add_command(
            label="Agregar empleado", command=self.ventana_agregar_empleado
        )
        menu_principal.add_command(
            label="Calcular nómina", command=self.ventana_calcular_nomina
        )
        menu_principal.add_command(
            label="Guardar archivo", command=self.guardar_archivo_nomina
        )
        menu_principal.add_separator()
        menu_principal.add_command(label="Salir", command=self.root.quit)

        menubar.add_cascade(label="Opciones", menu=menu_principal)
        self.root.config(menu=menubar)

    def _crear_estado(self):
        self.estado_var = tk.StringVar()
        self.estado_var.set("Sin empleados registrados.")
        barra_estado = tk.Label(
            self.root,
            textvariable=self.estado_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor="w",
        )
        barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

    # ---------- Ventana: Agregar empleado ----------

    def ventana_agregar_empleado(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar empleado")
        ventana.grab_set()  # comportarse más modal

        # Campos de texto
        labels = [
            "Nombre:",
            "Apellidos:",
            "Salario por día:",
            "Días trabajados (1-31):",
            "Otros ingresos:",
            "Pagos por salud:",
            "Aporte pensiones:",
        ]

        entradas = []
        for i, texto in enumerate(labels):
            tk.Label(ventana, text=texto).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            entry = tk.Entry(ventana, width=25)
            entry.grid(row=i, column=1, padx=5, pady=3)
            entradas.append(entry)

        entry_nombre, entry_apellidos, entry_salario, entry_dias, \
            entry_otros, entry_salud, entry_pension = entradas

        # Cargo (Listbox)
        tk.Label(ventana, text="Cargo:").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        lista_cargos = tk.Listbox(ventana, height=3, exportselection=False)
        for c in TipoCargo:
            lista_cargos.insert(tk.END, c.value)
        lista_cargos.grid(row=0, column=3, rowspan=3, padx=5, pady=3)

        # Género (Radiobuttons, equivalente a JCheckBox del enunciado)
        tk.Label(ventana, text="Género:").grid(row=3, column=2, sticky="w", padx=5, pady=3)
        genero_var = tk.StringVar(value=TipoGenero.MASCULINO.value)
        tk.Radiobutton(
            ventana, text="Masculino", variable=genero_var,
            value=TipoGenero.MASCULINO.value
        ).grid(row=3, column=3, sticky="w")
        tk.Radiobutton(
            ventana, text="Femenino", variable=genero_var,
            value=TipoGenero.FEMENINO.value
        ).grid(row=4, column=3, sticky="w")

        # Botones
        def guardar_empleado():
            try:
                nombre = entry_nombre.get().strip()
                apellidos = entry_apellidos.get().strip()
                if not nombre or not apellidos:
                    raise ValueError("Debe ingresar nombre y apellidos.")

                salario_dia = float(entry_salario.get())
                dias_trabajados = int(entry_dias.get())
                if dias_trabajados < 1 or dias_trabajados > 31:
                    raise ValueError("Los días trabajados deben estar entre 1 y 31.")

                otros_ingresos = float(entry_otros.get() or 0.0)
                pagos_salud = float(entry_salud.get() or 0.0)
                aporte_pensiones = float(entry_pension.get() or 0.0)

                seleccion = lista_cargos.curselection()
                if not seleccion:
                    raise ValueError("Debe seleccionar un cargo.")
                nombre_cargo = lista_cargos.get(seleccion[0])
                cargo = next(c for c in TipoCargo if c.value == nombre_cargo)

                genero = next(
                    g for g in TipoGenero if g.value == genero_var.get()
                )

                empleado = Empleado(
                    nombre,
                    apellidos,
                    cargo,
                    genero,
                    salario_dia,
                    dias_trabajados,
                    otros_ingresos,
                    pagos_salud,
                    aporte_pensiones,
                )
                self.empleados.append(empleado)
                self.estado_var.set(
                    f"Empleados registrados: {len(self.empleados)}"
                )

                messagebox.showinfo(
                    "Empleado agregado",
                    f"Se agregó a {nombre} {apellidos} correctamente.",
                    parent=ventana,
                )
                ventana.destroy()

            except ValueError as e:
                messagebox.showerror("Datos inválidos", str(e), parent=ventana)

        btn_guardar = tk.Button(ventana, text="Guardar", command=guardar_empleado)
        btn_guardar.grid(row=7, column=0, columnspan=2, pady=10)

        btn_cancelar = tk.Button(ventana, text="Cancelar", command=ventana.destroy)
        btn_cancelar.grid(row=7, column=2, columnspan=2, pady=10)

    # ---------- Ventana: Calcular nómina ----------

    def ventana_calcular_nomina(self):
        if not self.empleados:
            messagebox.showwarning(
                "Sin empleados", "No hay empleados registrados para calcular la nómina."
            )
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Cálculo de nómina")
        ventana.geometry("900x400")
        ventana.grab_set()

        columnas = (
            "nombre", "apellidos", "cargo", "genero",
            "salario_dia", "dias", "otros", "salud",
            "pension", "salario_mensual",
        )

        tree = ttk.Treeview(ventana, columns=columnas, show="headings")
        encabezados = [
            "Nombre", "Apellidos", "Cargo", "Género",
            "Salario día", "Días", "Otros ingresos",
            "Salud", "Pensiones", "Salario mensual",
        ]
        for col, texto in zip(columnas, encabezados):
            tree.heading(col, text=texto)
            tree.column(col, width=90, anchor="center")

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        total_nomina = 0.0
        for emp in self.empleados:
            salario_m = emp.salario_mensual
            total_nomina += salario_m
            tree.insert(
                "",
                tk.END,
                values=(
                    emp.nombre,
                    emp.apellidos,
                    emp.cargo.value,
                    emp.genero.value,
                    f"{emp.salario_dia:.2f}",
                    emp.dias_trabajados,
                    f"{emp.otros_ingresos:.2f}",
                    f"{emp.pagos_salud:.2f}",
                    f"{emp.aporte_pensiones:.2f}",
                    f"{salario_m:.2f}",
                ),
            )

        etiqueta_total = tk.Label(
            ventana,
            text=f"Total nómina de la empresa: {total_nomina:.2f}",
            font=("Arial", 11, "bold"),
        )
        etiqueta_total.pack(pady=5)

    # ---------- Guardar archivo ----------

    def guardar_archivo_nomina(self):
        if not self.empleados:
            messagebox.showwarning(
                "Sin empleados", "No hay datos para guardar en el archivo."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmación",
            "Se generará el archivo 'Nomina.txt' con la información actual.\n"
            "¿Desea continuar?",
        )
        if not confirmar:
            return

        carpeta = filedialog.askdirectory(
            title="Seleccione la carpeta donde se guardará Nomina.txt"
        )
        if not carpeta:
            messagebox.showinfo("Cancelado", "No se seleccionó ninguna carpeta.")
            return

        ruta_archivo = os.path.join(carpeta, "Nomina.txt")

        try:
            total_nomina = 0.0
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write("NÓMINA DE EMPLEADOS\n")
                f.write("=" * 60 + "\n")
                for emp in self.empleados:
                    salario_m = emp.salario_mensual
                    total_nomina += salario_m
                    linea = (
                        f"{emp.nombre} {emp.apellidos} | "
                        f"Cargo: {emp.cargo.value} | "
                        f"Género: {emp.genero.value} | "
                        f"Salario mensual: {salario_m:.2f}\n"
                    )
                    f.write(linea)

                f.write("=" * 60 + "\n")
                f.write(f"TOTAL NÓMINA: {total_nomina:.2f}\n")

            messagebox.showinfo(
                "Archivo guardado",
                f"Se creó el archivo:\n{ruta_archivo}",
            )
        except OSError as e:
            messagebox.showerror(
                "Error al guardar",
                f"No fue posible escribir el archivo:\n{e}",
            )

    # ---------- Bucle principal ----------

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = NominaApp()
    app.run()
