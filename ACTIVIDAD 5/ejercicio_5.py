import tkinter as tk
from tkinter import messagebox
import os

#crea el contacto
nombre_archivo = "contacto.txt"

def crear_contacto(nombre_nuevo, telefono):
    with open(nombre_archivo, "a+") as archivo:
        archivo.seek(0)
        lineas = archivo.readlines()
        for linea in lineas:
            if "!" in linea:
                nombre_existente, telefono_existente = linea.strip().split("!")
                if nombre_nuevo == nombre_existente or telefono_existente == telefono:
                    return "El nombre o número introducido ya existe."
        archivo.write(f"{nombre_nuevo}!{telefono}\n")
    return "Contacto creado exitosamente."

#lea el contacto donde abre el archivo y lee su contenido
def buscar_contacto_en_archivo(nombre_a_buscar):
    try:
        with open(nombre_archivo, "r") as archivo:
            for linea in archivo:
                if "!" in linea:
                    nombre_en_archivo, telefono_en_archivo = linea.strip().split("!")
                    if nombre_en_archivo == nombre_a_buscar:
                        return f"Nombre: {nombre_en_archivo}\nTeléfono: {telefono_en_archivo}"
    except FileNotFoundError:
        return None
    return None

#para actualizar contacto
def actualizar_contacto(nombre_a_actualizar, nuevo_telefono):
    archivo_temporal = nombre_archivo + ".tmp"
    contacto_encontrado = False
    try:
        with open(nombre_archivo, "r") as archivo_original, open(archivo_temporal, "w") as archivo_temp:
            for linea in archivo_original:
                if "!" in linea:
                    nombre_en_archivo, _ = linea.strip().split("!")
                    if nombre_en_archivo == nombre_a_actualizar:
                        archivo_temp.write(f"{nombre_a_actualizar}!{nuevo_telefono}\n")
                        contacto_encontrado = True
                    else:
                        archivo_temp.write(linea)
    except FileNotFoundError:
        return False
    
    if contacto_encontrado:
        os.remove(nombre_archivo)
        os.rename(archivo_temporal, nombre_archivo)
    else:
        os.remove(archivo_temporal)
    return contacto_encontrado

#para eliminar un contacto
def eliminar_contacto(nombre_a_eliminar):
    archivo_temporal = nombre_archivo + ".tmp"
    contacto_encontrado = False
    try:
        #abrir el arcihvo original pra leer y el temporal para escribir
        with open(nombre_archivo, "r") as archivo_original, open(archivo_temporal, "w") as archivo_temp:
            for linea in archivo_original:
                if "!" in linea:
                    nombre_en_archivo, _ = linea.strip().split("!")
                    if nombre_en_archivo != nombre_a_eliminar:
                        archivo_temp.write(linea)
                    else:
                        contacto_encontrado = True
    except FileNotFoundError:
        return False
    
    if contacto_encontrado:
        os.remove(nombre_archivo) #borrar el arcivo viejo
        os.rename(archivo_temporal, nombre_archivo)
    else:
        os.remove(archivo_temporal)
    return contacto_encontrado

#clase de la ventana principal

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        #Configuracion de la ventana
        self.title("Contactos")
        self.geometry("360x160")
        self.resizable(False, False)
        
        self.crear_widgets()

    def crear_widgets(self):
        #nombre
        label_nombre = tk.Label(self, text="Nombre:")
        label_nombre.grid(row=0, column=0, padx=10, pady=10)
        #campo de texto para nombre
        self.entry_nombre = tk.Entry(self, width=35)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        #telefono
        label_telefono = tk.Label(self, text="Teléfono:")
        label_telefono.grid(row=1, column=0, padx=10, pady=10)
        #campo de texto para telefono
        self.entry_telefono = tk.Entry(self, width=35)
        self.entry_telefono.grid(row=1, column=1, padx=10, pady=10)

        frame_boton = tk.Frame(self)
        frame_boton.grid(row=2, column=0, columnspan=2, pady=10)

        #boton para crear contacto
        boton_crear = tk.Button(frame_boton, text="Crear", command=self.accion_crear_contacto)
        boton_crear.pack(side="left", padx=5)

        #boton para contacto
        boton_buscar = tk.Button(frame_boton, text="Leer", command=self.accion_leer_contacto)
        boton_buscar.pack(side="left", padx=5)

        #boton para actualizar contacto
        boton_actualizar = tk.Button(frame_boton, text="Actualizar", command=self.accion_actualizar_contacto)
        boton_actualizar.pack(side="left", padx=5)

        #boton de eliminar 
        boton_eliminar = tk.Button(frame_boton, text="Eliminar", command=self.accion_eliminar_contacto)
        boton_eliminar.pack(side="left", padx=5)

        #boton para limpiar
        boton_limpiar = tk.Button(frame_boton, text="Limpiar", command=self.accion_limpiar_campos)
        boton_limpiar.pack(side="left", padx=5)

    def accion_crear_contacto(self):
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        
        #validamos que el campo no este vacio
        if nombre == "" or telefono == "":
            messagebox.showerror("Campos vacíos", "Por favor, complete todos los campos.")
            return
            
        resultado = crear_contacto(nombre, telefono)
        messagebox.showinfo("Resultado", resultado)

        if "exitosamente" in resultado:
            self.accion_limpiar_campos()

    def accion_leer_contacto(self):
        nombre_a_buscar = self.entry_nombre.get()
        if not nombre_a_buscar:
            messagebox.showerror("Campo vacío", "Por favor, ingrese un nombre para buscar.")
            return

        inf_contacto = buscar_contacto_en_archivo(nombre_a_buscar)
        if inf_contacto:
            messagebox.showinfo("Contacto encontrado", inf_contacto)
        else:
            messagebox.showinfo("No encontrado", "El contacto no fue encontrado.")

    def accion_actualizar_contacto(self):
        nombre = self.entry_nombre.get()
        nuevo_telefono = self.entry_telefono.get()

        if nombre == "" or nuevo_telefono == "":
            messagebox.showerror("Campos vacíos", "Para actulizar, ingrese el nombre del contacto y el nuevo teléfono.")
            return
        
        fue_actualizado = actualizar_contacto(nombre, nuevo_telefono)

        if fue_actualizado:
            messagebox.showinfo("Éxito", "Contacto actualizado exitosamente.")
            self.accion_limpiar_campos()
        else:
            messagebox.showinfo("No encontrado", "El contacto no fue encontrado para actualizar.")

    def accion_eliminar_contacto(self):
        nombre = self.entry_nombre.get()

        if nombre == "":
            messagebox.showerror("Campo vacío", "Ingrese el nombre del contacto a eliminar.")
            return
        
        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de que desea eliminar el contacto '{nombre}'?")

        if confirmacion:
            fue_eliminado = eliminar_contacto(nombre)

            if fue_eliminado:
                messagebox.showinfo("Éxito", "Contacto eliminado exitosamente.")
                self.accion_limpiar_campos()
            else:
                messagebox.showinfo("No encontrado", "El contacto no fue encontrado para eliminar.")

    #limpiar los campos
    def accion_limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)




class Principal:
    @staticmethod
    def main():
        app = VentanaPrincipal()
        app.mainloop()

if __name__ == "__main__":
    Principal.main()



