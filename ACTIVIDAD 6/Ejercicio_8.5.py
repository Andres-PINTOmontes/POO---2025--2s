"""
Aplicación de gestión de huéspedes de un hotel.

Enunciado:
- 10 habitaciones simples.
- Habitaciones 1 a 5: 120000 por día.
- Habitaciones 6 a 10: 160000 por día.

Menú:
    * Consultar habitaciones (y registrar ingreso)
    * Salida de huéspedes (y calcular valor a pagar)
    * Salir

Fechas en formato: AAAA-MM-DD (ejemplo: 2025-11-27)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from dataclasses import dataclass
from typing import Optional, List


# ==========================
#  MODELO
# ==========================

@dataclass
class Huesped:
    nombre: str
    apellidos: str
    documento: str


class Habitacion:
    def __init__(self, numero: int, precio_dia: float):
        self.numero: int = numero
        self.precio_dia: float = precio_dia
        self.disponible: bool = True
        self.huesped: Optional[Huesped] = None
        self.fecha_ingreso: Optional[date] = None

    def ocupar(self, huesped: Huesped, fecha_ingreso: date) -> None:
        if not self.disponible:
            raise ValueError("La habitación ya está ocupada.")
        self.huesped = huesped
        self.fecha_ingreso = fecha_ingreso
        self.disponible = False

    def liberar(self, fecha_salida: date) -> float:
        """
        Libera la habitación y devuelve el valor total a pagar.
        """
        if self.disponible or self.fecha_ingreso is None or self.huesped is None:
            raise ValueError("La habitación no está ocupada.")

        if fecha_salida <= self.fecha_ingreso:
            raise ValueError("La fecha de salida debe ser posterior a la de ingreso.")

        dias = (fecha_salida - self.fecha_ingreso).days
        total = dias * self.precio_dia

        # Resetear estado
        self.disponible = True
        self.huesped = None
        self.fecha_ingreso = None

        return total

    def estado_str(self) -> str:
        return "Disponible" if self.disponible else "No disponible"


class Hotel:
    def __init__(self) -> None:
        self.habitaciones: List[Habitacion] = []
        self._crear_habitaciones()

    def _crear_habitaciones(self) -> None:
        # Habitaciones 1-5: 120000; 6-10: 160000
        for n in range(1, 11):
            precio = 120000 if n <= 5 else 160000
            self.habitaciones.append(Habitacion(n, precio))

    def buscar_habitacion(self, numero: int) -> Optional[Habitacion]:
        for h in self.habitaciones:
            if h.numero == numero:
                return h
        return None


# ==========================
#  APLICACIÓN TKINTER
# ==========================

class HotelApp:
    FORMATO_FECHA = "%Y-%m-%d"  # AAAA-MM-DD

    def __init__(self) -> None:
        self.hotel = Hotel()

        self.root = tk.Tk()
        self.root.title("Gestión de Hotel")
        self.root.geometry("800x400")

        self._crear_menu()
        self._crear_estado()

    # ---------- UI base ----------

    def _crear_menu(self) -> None:
        menubar = tk.Menu(self.root)

        menu_opciones = tk.Menu(menubar, tearoff=0)
        menu_opciones.add_command(
            label="Consultar habitaciones", command=self.ventana_consultar_habitaciones
        )
        menu_opciones.add_command(
            label="Salida de huéspedes", command=self.ventana_salida_huesped
        )
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Salir", command=self.root.quit)

        menubar.add_cascade(label="Opciones", menu=menu_opciones)
        self.root.config(menu=menubar)

    def _crear_estado(self) -> None:
        self.estado_var = tk.StringVar()
        self._actualizar_estado()

        barra_estado = tk.Label(
            self.root,
            textvariable=self.estado_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor="w",
        )
        barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

    def _actualizar_estado(self) -> None:
        ocupadas = sum(1 for h in self.hotel.habitaciones if not h.disponible)
        self.estado_var.set(f"Habitaciones ocupadas: {ocupadas} / 10")

    # ---------- Utilidades ----------

    @staticmethod
    def _parsear_fecha(texto: str) -> date:
        try:
            return datetime.strptime(texto, HotelApp.FORMATO_FECHA).date()
        except ValueError:
            raise ValueError(
                f"Fecha inválida. Use el formato AAAA-MM-DD, por ejemplo 2025-11-27."
            )

    # ---------- Ventana: Consultar y ocupar ----------

    def ventana_consultar_habitaciones(self) -> None:
        ventana = tk.Toplevel(self.root)
        ventana.title("Consultar habitaciones")
        ventana.geometry("750x350")
        ventana.grab_set()

        columnas = ("numero", "precio", "estado", "huesped", "fecha_ingreso")
        tree = ttk.Treeview(ventana, columns=columnas, show="headings")
        encabezados = [
            "Número",
            "Precio por día",
            "Estado",
            "Huésped",
            "Fecha ingreso",
        ]
        for col, txt in zip(columnas, encabezados):
            tree.heading(col, text=txt)
            tree.column(col, width=120, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def poblar_tree():
            tree.delete(*tree.get_children())
            for h in self.hotel.habitaciones:
                nombre_huesped = ""
                fecha_ingreso = ""
                if not h.disponible and h.huesped is not None and h.fecha_ingreso:
                    nombre_huesped = f"{h.huesped.nombre} {h.huesped.apellidos}"
                    fecha_ingreso = h.fecha_ingreso.strftime(self.FORMATO_FECHA)

                tree.insert(
                    "",
                    tk.END,
                    values=(
                        h.numero,
                        f"{h.precio_dia:.0f}",
                        h.estado_str(),
                        nombre_huesped,
                        fecha_ingreso,
                    ),
                )

        poblar_tree()

        # Botón para ocupar habitación seleccionada
        def ocupar_habitacion():
            seleccionado = tree.selection()
            if not seleccionado:
                messagebox.showwarning(
                    "Selección requerida",
                    "Debe seleccionar una habitación de la tabla.",
                    parent=ventana,
                )
                return

            item = tree.item(seleccionado[0])
            numero = int(item["values"][0])

            habitacion = self.hotel.buscar_habitacion(numero)
            if habitacion is None:
                messagebox.showerror(
                    "Error", "La habitación seleccionada no existe.", parent=ventana
                )
                return

            if not habitacion.disponible:
                messagebox.showerror(
                    "No disponible",
                    "La habitación seleccionada ya está ocupada.",
                    parent=ventana,
                )
                return

            self._ventana_registro_ingreso(habitacion, poblar_tree, ventana)

        btn_frame = tk.Frame(ventana)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(
            btn_frame, text="Ocupar habitación", command=ocupar_habitacion
        ).pack(side=tk.LEFT)

        tk.Button(
            btn_frame, text="Cerrar", command=ventana.destroy
        ).pack(side=tk.RIGHT)

    def _ventana_registro_ingreso(
        self,
        habitacion: Habitacion,
        callback_refrescar,
        ventana_padre,
    ) -> None:
        win = tk.Toplevel(ventana_padre)
        win.title(f"Registrar ingreso - Habitación {habitacion.numero}")
        win.geometry("420x260")
        win.grab_set()

        tk.Label(
            win,
            text=f"Habitación {habitacion.numero} - Precio por día: {habitacion.precio_dia:.0f}",
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=8, padx=8)

        etiquetas = [
            "Fecha de ingreso (AAAA-MM-DD):",
            "Nombre:",
            "Apellidos:",
            "Documento de identidad:",
        ]
        entradas = []
        for i, txt in enumerate(etiquetas, start=1):
            tk.Label(win, text=txt).grid(row=i, column=0, sticky="w", padx=8, pady=4)
            e = tk.Entry(win, width=25)
            e.grid(row=i, column=1, padx=8, pady=4)
            entradas.append(e)

        entry_fecha, entry_nombre, entry_apellidos, entry_doc = entradas

        def registrar():
            try:
                fecha = self._parsear_fecha(entry_fecha.get().strip())
                nombre = entry_nombre.get().strip()
                apellidos = entry_apellidos.get().strip()
                documento = entry_doc.get().strip()

                if not nombre or not apellidos or not documento:
                    raise ValueError("Todos los campos son obligatorios.")

                if not documento.isdigit():
                    raise ValueError("El documento debe contener solo dígitos.")

                huesped = Huesped(nombre, apellidos, documento)
                habitacion.ocupar(huesped, fecha)

                messagebox.showinfo(
                    "Ingreso registrado",
                    f"Huésped {nombre} {apellidos} ocupado la "
                    f"habitación {habitacion.numero}.",
                    parent=win,
                )
                self._actualizar_estado()
                callback_refrescar()
                win.destroy()

            except ValueError as e:
                messagebox.showerror("Datos inválidos", str(e), parent=win)

        tk.Button(win, text="Registrar ingreso", command=registrar).grid(
            row=5, column=0, pady=10
        )
        tk.Button(win, text="Cancelar", command=win.destroy).grid(
            row=5, column=1, pady=10
        )

    # ---------- Ventana: Salida de huéspedes ----------

    def ventana_salida_huesped(self) -> None:
        ventana = tk.Toplevel(self.root)
        ventana.title("Salida de huéspedes")
        ventana.geometry("420x260")
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Salida de huéspedes",
            font=("Arial", 11, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=8)

        tk.Label(ventana, text="Número de habitación (1-10):").grid(
            row=1, column=0, sticky="w", padx=8, pady=4
        )
        spin_num = tk.Spinbox(ventana, from_=1, to=10, width=5)
        spin_num.grid(row=1, column=1, padx=8, pady=4, sticky="w")

        # Frame para info y registro de salida
        frame_info = tk.LabelFrame(ventana, text="Datos de la estancia")
        frame_info.grid(row=2, column=0, columnspan=2, padx=8, pady=8, sticky="ew")

        lbl_detalle = tk.Label(frame_info, text="(Seleccione habitación y pulse 'Buscar')")
        lbl_detalle.grid(row=0, column=0, columnspan=2, sticky="w", padx=4, pady=2)

        tk.Label(frame_info, text="Fecha de salida (AAAA-MM-DD):").grid(
            row=1, column=0, sticky="w", padx=4, pady=4
        )
        entry_fecha_salida = tk.Entry(frame_info, width=20, state="disabled")
        entry_fecha_salida.grid(row=1, column=1, padx=4, pady=4, sticky="w")

        habitacion_seleccionada: dict = {"hab": None}

        def buscar_habitacion():
            try:
                numero = int(spin_num.get())
            except ValueError:
                messagebox.showerror(
                    "Número inválido", "Debe ingresar un número de habitación válido."
                )
                return

            hab = self.hotel.buscar_habitacion(numero)
            if hab is None:
                messagebox.showerror("Error", "La habitación no existe.", parent=ventana)
                return

            if hab.disponible or hab.huesped is None or hab.fecha_ingreso is None:
                messagebox.showerror(
                    "No ocupada",
                    "La habitación seleccionada no está ocupada.",
                    parent=ventana,
                )
                return

            habitacion_seleccionada["hab"] = hab
            lbl_detalle.config(
                text=(
                    f"Habitación {hab.numero} | Precio día: {hab.precio_dia:.0f}\n"
                    f"Huésped: {hab.huesped.nombre} {hab.huesped.apellidos}\n"
                    f"Fecha ingreso: {hab.fecha_ingreso.strftime(self.FORMATO_FECHA)}"
                )
            )
            entry_fecha_salida.config(state="normal")

        def registrar_salida():
            hab = habitacion_seleccionada["hab"]
            if hab is None:
                messagebox.showwarning(
                    "Sin habitación",
                    "Primero debe buscar una habitación ocupada.",
                    parent=ventana,
                )
                return
            try:
                fecha_salida = self._parsear_fecha(entry_fecha_salida.get().strip())
                total = hab.liberar(fecha_salida)
                self._actualizar_estado()

                messagebox.showinfo(
                    "Salida registrada",
                    f"Estancia registrada correctamente.\n"
                    f"Días de alojamiento: {(fecha_salida - hab.fecha_ingreso).days if hab.fecha_ingreso else '?'}\n"
                    f"Total a pagar: {total:.0f}",
                    parent=ventana,
                )
                ventana.destroy()
            except ValueError as e:
                messagebox.showerror("Error en datos", str(e), parent=ventana)

        btn_buscar = tk.Button(ventana, text="Buscar habitación", command=buscar_habitacion)
        btn_buscar.grid(row=3, column=0, pady=8)

        btn_registrar = tk.Button(
            ventana, text="Registrar salida", command=registrar_salida
        )
        btn_registrar.grid(row=3, column=1, pady=8)

    # ---------- Bucle principal ----------

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = HotelApp()
    app.run()
