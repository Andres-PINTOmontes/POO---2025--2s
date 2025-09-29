from enum import Enum

class TipoCombustible(Enum):
    GASOLINA= 1
    BIOETANOL = 2
    DIESEL = 3
    BIODIESEL = 4
    GAS_NATURAL = 5

class TipoAutomovil(Enum):
    CARRO_CUIDAD = 1
    SUBCOMPACTO = 2
    COMPACTO = 3
    FAMILIAR = 4
    EJECUTIVO = 5
    SUV = 6

class TipoColor(Enum):
    BLANCO = 1
    NEGRO = 2
    ROJO = 3
    NARANJA = 4
    AMARILLO = 5
    VERDE = 6
    AZUL = 7
    VIOLETA = 8

class Automovil:
    def __init__(self,
                 marca: str,
                 modelo: int,
                 motor: int ,
                 tipo_combustible: TipoCombustible,
                 tipo_automovil: TipoAutomovil,
                 numero_puertas: int ,
                 cantidad_asientos: int,
                 velocidad_maxima: int,
                 color: TipoColor):

        self.marca = marca
        self.modelo = modelo
        self.motor = motor
        self.tipo_combustible = tipo_combustible
        self.tipo_automovil = tipo_automovil
        self.numero_puertas = numero_puertas
        self.cantidad_asientos = cantidad_asientos
        self.velocidad_maxima = velocidad_maxima
        self.color = color

        self.velocidad_actual = 0

    # Lectura o tener el valor del atributo de un objeto
    def get_marca(self):
      return self.marca

    def get_modelo(self):
      return self.modelo

    def get_motor(self):
      return self.motor

    def get_tipo_combustible(self):
      return self.tipo_combustible

    def get_tipo_automovil(self):
      return self.tipo_automovil

    def get_numero_puertas(self):
      return self.numero_puertas

    def get_cantidad_asientos(self):
      return self.cantidad_asientos

    def get_velocidad_maxima(self):
      return self.velocidad_maxima

    def get_color(self):
      return self.color

    def get_velocidad_actual(self):
      return self.velocidad_actual

    # Escritura o asignar o cambiar el valor de un atributo de un objeto
    def set_marca(self, marca):
        self.marca = marca

    def set_modelo(self, modelo):
        self.modelo = modelo

    def set_motor(self, motor):
        self.motor = motor

    def set_tipo_combustible(self, tipo_combustible):
        self.tipo_combustible = tipo_combustible

    def set_tipo_automovil(self, tipo_automovil):
        self.tipo_automovil = tipo_automovil

    def set_numero_puertas(self, numero_puertas):
        self.numero_puertas = numero_puertas

    def set_cantidad_asientos(self, cantidad_asientos):
        self.cantidad_asientos = cantidad_asientos

    def set_velocidad_maxima(self, velocidad_maxima):
        self.velocidad_maxima = velocidad_maxima

    def set_color(self, color):
        self.color = color

    def set_velocidad_actual(self, velocidad_actual):
        self.velocidad_actual = velocidad_actual



    def acelerar(self, aceleracion):
        if self.velocidad_actual + aceleracion > self.velocidad_maxima:
            self.velocidad_actual = self.velocidad_maxima
            print(f"No se puede superar la velocidad máxima")
        else:
            self.velocidad_actual += aceleracion

    def desacelerar(self, desaceleracion):
        if self.velocidad_actual - desaceleracion < 0:
            self.velocidad_actual = 0
            print(f"No se puede decrementar a una velocidad negativa.")
        else:
            self.velocidad_actual -= desaceleracion

    def frenar(self):
        self.velocidad_actual = 0

    def calcular_tiempo_llegada(self, distancia):
        return distancia / self.velocidad_actual



    def imprimir(self):
        print(f"Marca = {self.marca}")
        print(f"Modelo = {self.modelo}")
        print(f"Motor = {self.motor}")
        print(f"Tipo de combustible = {self.tipo_combustible.name}")
        print(f"Tipo de automóvil = {self.tipo_automovil.name}")
        print(f"Número de puertas = {self.numero_puertas}")
        print(f"Cantidad de asientos = {self.cantidad_asientos}")
        print(f"Velocida máxima = {self.velocidad_maxima}")
        print(f"Color = {self.color.name}")

    def imprimir_velocidad_actual(self):
        print(f"Velocidad actual = {self.velocidad_actual}")


class Prueba_Automovil:

  def main():

  #Objeto
    auto1 = Automovil(
        "Ford",
        2018,
        3,
        TipoCombustible.DIESEL,
        TipoAutomovil.EJECUTIVO,
        5,
        6,
        250,
        TipoColor.NEGRO
    )

    auto1.imprimir()

    auto1.set_velocidad_actual(100)
    auto1.imprimir_velocidad_actual()


    auto1.acelerar(20)
    auto1.imprimir_velocidad_actual()

    auto1.desacelerar(50)
    auto1.imprimir_velocidad_actual()


    auto1.frenar()
    auto1.imprimir_velocidad_actual()

    auto1.desacelerar(20)

if __name__ == "__main__":
      Prueba_Automovil.main()