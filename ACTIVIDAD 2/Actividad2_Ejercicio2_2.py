from enum import Enum

class TipoPlaneta(Enum):
    GASEOSO = 1
    TERRESTRE = 2
    ENANO = 3

class Planeta:
    def __init__(self, nombre: str = None, num_satelites: int = 0, masa: float = 0.0, volumen: float = 0.0,
                 diametro: int = 0, distancia_sol: int = 0, tipo: TipoPlaneta = None, observable: bool = False):
        # Constructor que inicializa los atributos
        self.nombre = nombre
        self.num_satelites = num_satelites
        self.masa = masa
        self.volumen = volumen
        self.diametro = diametro
        self.distancia_sol = distancia_sol
        self.tipo = tipo
        self.observable = observable

    def mostrar_info(self):
        # Método que imprime los valores de los atributos
        print(f"Nombre del planeta = {self.nombre}")
        print(f"Cantidad de satélites = {self.num_satelites}")
        print(f"Masa del planeta (kg) = {self.masa}")
        print(f"Volumen del planeta (km³) = {self.volumen}")
        print(f"Diámetro del planeta (km) = {self.diametro}")
        print(f"Distancia media al sol (km) = {self.distancia_sol}")
        print(f"Tipo de planeta = {self.tipo.name if self.tipo else 'No definido'}")
        print(f"Es observable a simple vista = {self.observable}")

    def densidad(self):
        # Cálculo de la densidad
        if self.volumen > 0:
            return self.masa / self.volumen
        return 0

    def es_exterior(self):
        UA = 149597870
        # Es exterior si está más allá de 3.4 UA
        return self.distancia_sol > 3.4 * UA



if __name__ == "__main__":
    # Crear dos planetas
    planeta1 = Planeta("Tierra", 1, 5.9736E24, 1.08321E12, 12742, 150000000, TipoPlaneta.TERRESTRE, True)
    planeta2 = Planeta("Júpiter", 79, 1.898E27, 1.4313E15, 139820, 778500000, TipoPlaneta.GASEOSO, True)

    # Mostrar info
    planeta1.mostrar_info()
    print(f"Densidad de {planeta1.nombre} = {planeta1.densidad()} kg/km³")
    print(f"¿Es exterior? {planeta1.es_exterior()}\n")

    planeta2.mostrar_info()
    print(f"Densidad de {planeta2.nombre} = {planeta2.densidad()} kg/km³")
    print(f"¿Es exterior? {planeta2.es_exterior()}")