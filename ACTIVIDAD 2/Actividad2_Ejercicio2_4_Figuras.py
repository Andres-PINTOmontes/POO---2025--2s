import math


class Circulo:
    def __init__(self, radio):
        self.radio = radio

    def calcular_area(self):
        return math.pi * self.radio ** 2

    def calcular_perimetro(self):
        return 2 * math.pi * self.radio

class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return self.base * self.altura

    def calcular_perimetro(self):
        return 2 * (self.base + self.altura)

class Cuadrado:
    def __init__(self, longitud):
        self.longitud = longitud

    def calcular_area(self):
        return self.longitud ** 2

    def calcular_perimetro(self):
        return 4 * self.longitud

class TrianguloRectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return (self.base * self.altura)/2


    def calcular_hipotenusa(self):
      return math.sqrt(self.base ** 2 + self.altura ** 2)

    def calcular_perimetro(self):
      return self.base + self.altura + self.calcular_hipotenusa()

    def determinar_tipo_triagunlo(self):
      hipotenusa = self.calcular_hipotenusa()

      if self.base == self.altura and self.base == hipotenusa and self.altura == hipotenusa:
        return " Es un triángulo Equilátero"

      elif self.base != self.altura and self.base != hipotenusa and self.altura != hipotenusa:
        return "Es un triángulo Escaleno"

      else:
        return "Es un triángulo Isósceles"

    #Clase principal
class Figuras_geometricas:
  def main():
    figura1 = Circulo(2.0)
    figura2 = Rectangulo(1, 2)
    figura3 = Cuadrado(3)
    figura4 = TrianguloRectangulo(3, 5)


    print(f"El área del círculo es = {figura1.calcular_area()}")
    print(f"El perímetro del círculo es = {figura1.calcular_perimetro()}")
    print(f"El área del rectángulo es = {figura2.calcular_area()}")
    print(f"El perímetro del rectángulo es = {figura2.calcular_perimetro()}")
    print(f"El área del cuadrado es = {figura3.calcular_area()}")
    print(f"El perímetro del cuadrado es = {figura3.calcular_perimetro()}")
    print(f"El área del triángulo rectángulo es = {figura4.calcular_area()}")
    print(f"El perímetro del triángulo rectángulo es = {figura4.calcular_perimetro()}")
    print(figura4.determinar_tipo_triagunlo())

if __name__ == "__main__":
  Figuras_geometricas.main()