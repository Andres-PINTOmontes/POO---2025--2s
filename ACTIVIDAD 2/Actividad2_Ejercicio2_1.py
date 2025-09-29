class Persona:
    def __init__(self, nombre: str, apellido: str, documento: int, nacimiento: int):
        # Constructor que inicializa los atributos
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.nacimiento = nacimiento

    def imprimir(self):
        # Método que imprime los valores de los atributos
        print(f"Nombre: {self.nombre}")
        print(f"Apellido: {self.apellido}")
        print(f"Documento: {self.documento}")
        print(f"Año de Nacimiento: {self.nacimiento}")

def main():
    # Crear dos personas
    persona1 = Persona("Pedro", "Pérez", 1053121010, 1998)
    persona2 = Persona("Luis", "León", 1053223344, 2001)

    # Imprimir los valores de los atributos de las personas
    print("PERSONA #1")
    persona1.imprimir()
    print()  # Espacio entre las personas
    print("PERSONA #2")
    persona2.imprimir()

# Llamada a la función main
if __name__ == "__main__":
    main()