import math
import tkinter as tk
from tkinter import ttk, messagebox


class FiguraGeometrica:
    """Clase base que almacena el volumen y la superficie de una figura."""

    def __init__(self) -> None:
        self.volumen: float = 0.0
        self.superficie: float = 0.0

    def set_volumen(self, volumen: float) -> None:
        self.volumen = volumen

    def set_superficie(self, superficie: float) -> None:
        self.superficie = superficie

    def get_volumen(self) -> float:
        return self.volumen

    def get_superficie(self) -> float:
        return self.superficie


class Cilindro(FiguraGeometrica):
    """Representa un cilindro definido por su radio y altura."""

    def __init__(self, radio: float, altura: float) -> None:
        super().__init__()
        self.radio = radio
        self.altura = altura
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self) -> float:
        return math.pi * self.altura * self.radio ** 2

    def calcular_superficie(self) -> float:
        area_lateral = 2 * math.pi * self.radio * self.altura
        area_bases = 2 * math.pi * self.radio ** 2
        return area_lateral + area_bases


class Esfera(FiguraGeometrica):
    """Representa una esfera definida unicamente por su radio."""

    def __init__(self, radio: float) -> None:
        super().__init__()
        self.radio = radio
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self) -> float:
        return (4.0 / 3.0) * math.pi * self.radio ** 3

    def calcular_superficie(self) -> float:
        return 4.0 * math.pi * self.radio ** 2


class Piramide(FiguraGeometrica):
    """Representa una piramide de base cuadrada con apotema."""

    def __init__(self, base: float, altura: float, apotema: float) -> None:
        super().__init__()
        self.base = base
        self.altura = altura
        self.apotema = apotema
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self) -> float:
        return (self.base ** 2) * self.altura / 3.0

    def calcular_superficie(self) -> float:
        area_base = self.base ** 2
        area_lados = 2.0 * self.base * self.apotema
        return area_base + area_lados


class FiguraApp:
    """Interfaz grafica para calcular volumen y superficie de figuras geometricas."""

    FIGURAS = ("Cilindro", "Esfera", "Piramide")

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Figuras geometricas")
        self.root.configure(padx=24, pady=24)

        self._construir_interfaz()

    def _construir_interfaz(self) -> None:
        titulo = ttk.Label(self.root, text="Figuras geometricas", font=("Segoe UI", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(self.root, text="Seleccione la figura:").grid(row=1, column=0, sticky="w", pady=(12, 4))
        self.figura_var = tk.StringVar(value=self.FIGURAS[0])
        self.figura_selector = ttk.Combobox(
            self.root,
            textvariable=self.figura_var,
            values=self.FIGURAS,
            state="readonly",
            width=22,
        )
        self.figura_selector.grid(row=1, column=1, sticky="ew", pady=(12, 4))
        self.figura_selector.bind("<<ComboboxSelected>>", lambda _: self._actualizar_campos())

        self.campos: dict[str, tuple[tk.StringVar, ttk.Entry]] = {}
        etiquetas = ("Radio (cm):", "Altura (cm):", "Base (cm):", "Apotema (cm):")
        for index, etiqueta in enumerate(etiquetas, start=2):
            ttk.Label(self.root, text=etiqueta).grid(row=index, column=0, sticky="w", pady=3)
            var = tk.StringVar()
            entry = ttk.Entry(self.root, textvariable=var)
            entry.grid(row=index, column=1, sticky="ew", pady=3)
            self.campos[etiqueta] = (var, entry)

        botones_frame = ttk.Frame(self.root)
        botones_frame.grid(row=6, column=0, columnspan=2, pady=(12, 8), sticky="w")

        self.boton_calcular = tk.Button(
            botones_frame,
            text="Calcular",
            command=self._calcular,
            bg="#c9d6ff",
            activebackground="#b3c4ff",
            width=12,
        )
        self.boton_calcular.pack(side="left", padx=(0, 8))

        self.boton_limpiar = tk.Button(
            botones_frame,
            text="Limpiar",
            command=self._limpiar,
            bg="#f8caca",
            activebackground="#f7b6b6",
            width=12,
        )
        self.boton_limpiar.pack(side="left")

        self.resultado_volumen = tk.StringVar(value="Volumen =")
        self.resultado_superficie = tk.StringVar(value="Superficie =")

        ttk.Label(self.root, textvariable=self.resultado_volumen, font=("Segoe UI", 11)).grid(
            row=7, column=0, columnspan=2, sticky="w", pady=(4, 0)
        )
        ttk.Label(self.root, textvariable=self.resultado_superficie, font=("Segoe UI", 11)).grid(
            row=8, column=0, columnspan=2, sticky="w"
        )

        self.root.columnconfigure(1, weight=1)
        self._actualizar_campos()

    def _actualizar_campos(self) -> None:
        figura = self.figura_var.get()
        campos_activos = {
            "Cilindro": ("Radio (cm):", "Altura (cm):"),
            "Esfera": ("Radio (cm):",),
            "Piramide": ("Base (cm):", "Altura (cm):", "Apotema (cm):"),
        }

        for etiqueta, (var, entry) in self.campos.items():
            if etiqueta in campos_activos[figura]:
                entry.configure(state="normal")
            else:
                var.set("")
                entry.configure(state="disabled")

    def _tomar_float(self, etiqueta: str) -> float:
        valor = self.campos[etiqueta][0].get().strip()
        if not valor:
            raise ValueError(f"Ingrese un valor para {etiqueta}")
        return float(valor)

    def _calcular(self) -> None:
        figura = self.figura_var.get()

        try:
            if figura == "Cilindro":
                radio = self._tomar_float("Radio (cm):")
                altura = self._tomar_float("Altura (cm):")
                figura_obj = Cilindro(radio, altura)
            elif figura == "Esfera":
                radio = self._tomar_float("Radio (cm):")
                figura_obj = Esfera(radio)
            else:
                base = self._tomar_float("Base (cm):")
                altura = self._tomar_float("Altura (cm):")
                apotema = self._tomar_float("Apotema (cm):")
                figura_obj = Piramide(base, altura, apotema)
        except ValueError as error:
            messagebox.showerror("Datos invalidos", str(error))
            return

        self.resultado_volumen.set(f"Volumen = {figura_obj.get_volumen():.2f} cm^3")
        self.resultado_superficie.set(f"Superficie = {figura_obj.get_superficie():.2f} cm^2")

    def _limpiar(self) -> None:
        for var, entry in self.campos.values():
            entry.configure(state="normal")
            var.set("")

        self.resultado_volumen.set("Volumen =")
        self.resultado_superficie.set("Superficie =")
        self._actualizar_campos()


def main() -> None:
    root = tk.Tk()
    FiguraApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
