import tkinter as tk
from tkinter import ttk


class PruebaExcepcionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Demostración de Máquina de Estados")
        self.root.configure(padx=20, pady=20)
        self.root.geometry("450x350")

        # Creación de los elementos  de la ventana

        # Un marco para agrupar los botones
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(pady=10)
        
        # El botón que inicia la demostración
        ttk.Button(frame_botones, text="Ejecutar Demostración", command=self.ejecutar_logica).pack(side="left", padx=10)
        
        # El botón para limpiar la pantalla de resultados
        ttk.Button(frame_botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=10)

        self.resultado_text = tk.Text(self.root, height=12, width=50, font=("Courier", 11))
        self.resultado_text.pack(pady=10)
   
        self.resultado_text.config(state="disabled")

    def _agregar_linea_resultado(self, texto):

        self.resultado_text.config(state="normal")
        self.resultado_text.insert(tk.END, texto + "\n")
        self.resultado_text.config(state="disabled")
        self.resultado_text.see(tk.END)

    def ejecutar_logica(self):
   
        self.limpiar() 
        try:
            self._agregar_linea_resultado("Ingresando al primer try")
            _ = 10000 / 0 
            self._agregar_linea_resultado("Después de la división") # Esta línea nunca se ejecuta

        except ZeroDivisionError:
            # Capturamos la excepción específica
            self._agregar_linea_resultado("División por cero")

        finally:
            self._agregar_linea_resultado("Ingresando al primer finally")

        self._agregar_linea_resultado("") 
        try:
            self._agregar_linea_resultado("Ingresando al segundo try")
  
            objeto = None
            objeto.toString() 
            self._agregar_linea_resultado("Imprimiendo objeto")

        except Exception:
    
            self._agregar_linea_resultado("Ocurrió una excepción")

        finally:
            self._agregar_linea_resultado("Ingresando al segundo finally")

    def limpiar(self):
        self.resultado_text.config(state="normal")
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.config(state="disabled")

# Clase de entrada principal del programa
class Principal:
    @staticmethod
    def main():
        root = tk.Tk()
        app = PruebaExcepcionesApp(root) 
        root.mainloop()

# Puerta de entrada que ejecuta el método main de la clase Principal
if __name__ == "__main__":
    Principal.main()