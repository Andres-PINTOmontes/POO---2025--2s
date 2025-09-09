from dataclasses import dataclass


def _fmt(n: float) -> str:
    return str(int(n)) if float(n).is_integer() else f"{n:.2f}"


@dataclass
class Persona:
    nombre: str
    edad: float


class FamiliaJuan:
    def __init__(self, edad_juan: float):
        self.juan = Persona("Juan", edad_juan)
        self.alberto = Persona("Alberto", 2 * (edad_juan / 3))
        self.ana = Persona("Ana", 4 * (edad_juan / 3))
        self.mama = Persona("Mamá", self.juan.edad + self.alberto.edad + self.ana.edad)

    def resumen(self) -> list[str]:
        return [
            f"Juan: {_fmt(self.juan.edad)}",
            f"Ana: {_fmt(self.ana.edad)}",
            f"Alberto: {_fmt(self.alberto.edad)}",
            f"Mamá: {_fmt(self.mama.edad)}",
        ]


def main():
    try:
        edjuan = float(input("Ingrese la edad de Juan: ").strip())
    except ValueError:
        print("Entrada inválida. Debe ser un número.")
        return

    if not (0 < edjuan <= 120):
        print("La edad debe estar entre 1 y 120 años.")
        return

    familia = FamiliaJuan(edjuan)
    print("LAS EDADES SON:")
    for linea in familia.resumen():
        print(linea)


if __name__ == "__main__":
    main()
