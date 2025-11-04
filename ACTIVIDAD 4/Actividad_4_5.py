
import io
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

APP_TITLE = "Lector de archivos — Tkinter"
ENCODINGS = ("utf-8", "latin-1", "cp1252")

def leer_archivo_bytes_a_texto(path: Path, encoding: str) -> str:
    """Lee el archivo en binario -> buffer -> texto y devuelve el contenido."""
    with path.open("rb") as fb:                     # flujo de bytes
        with io.BufferedReader(fb) as buf:          # buffer de bytes
            with io.TextIOWrapper(buf, encoding=encoding, errors="replace") as txt:
                return txt.read()

class App(tk.Tk):
    def __init__(self, ruta_inicial: Path | None = None):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x560")
        self.minsize(720, 420)

        # --- Barra superior (botones + encoding)
        top = tk.Frame(self, padx=8, pady=6)
        top.pack(side=tk.TOP, fill=tk.X)

        self.encoding_var = tk.StringVar(value=ENCODINGS[0])
        tk.Button(top, text="Abrir archivo…", command=self.abrir).pack(side=tk.LEFT)
        tk.Button(top, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=(8,0))
        tk.Label(top, text="Encoding:").pack(side=tk.RIGHT)
        tk.OptionMenu(top, self.encoding_var, *ENCODINGS).pack(side=tk.RIGHT, padx=(4,8))

        # --- Área de texto con scroll
        wrap = tk.Frame(self, padx=8, pady=8)
        wrap.pack(fill=tk.BOTH, expand=True)

        self.txt = tk.Text(wrap, wrap=tk.NONE, undo=True)
        sx = tk.Scrollbar(wrap, orient=tk.HORIZONTAL, command=self.txt.xview)
        sy = tk.Scrollbar(wrap, orient=tk.VERTICAL, command=self.txt.yview)
        self.txt.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)

        self.txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sy.pack(side=tk.RIGHT, fill=tk.Y)
        sx.pack(side=tk.BOTTOM, fill=tk.X)

        # --- Barra de estado
        self.status = tk.StringVar(value="Listo")
        tk.Label(self, textvariable=self.status, anchor="w", relief=tk.SUNKEN, padx=8)\
            .pack(side=tk.BOTTOM, fill=tk.X)

        # Carga inicial (si se pasó una ruta por argumento)
        if ruta_inicial:
            self.cargar_desde_ruta(ruta_inicial)

    def abrir(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo de texto",
            filetypes=[("Texto", "*.txt *.csv *.log *.md *.json *.xml *.yml *.yaml *.py *.java"),
                       ("Todos", "*.*")]
        )
        if ruta:
            self.cargar_desde_ruta(Path(ruta))

    def cargar_desde_ruta(self, path: Path):
        try:
            contenido = leer_archivo_bytes_a_texto(path, self.encoding_var.get())
        except FileNotFoundError:
            messagebox.showerror("Error", f"Archivo no encontrado:\n{path}")
            return
        except PermissionError:
            messagebox.showerror("Error", f"Permiso denegado:\n{path}")
            return
        except OSError as e:
            messagebox.showerror("Error de lectura", f"{e}")
            return

        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, contenido)
        self.status.set(f"Leído: {path} — {len(contenido.splitlines())} líneas")

    def limpiar(self):
        self.txt.delete("1.0", tk.END)
        self.status.set("Listo")

def main():
    # Permite pasar una ruta como argumento opcional: python leer_gui.py prueba.txt
    ruta = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else None
    app = App(ruta)
    app.mainloop()

if __name__ == "__main__":
    main()
