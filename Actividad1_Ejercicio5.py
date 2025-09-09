from dataclasses import dataclass


def _fmt(n: float) -> str:
    return str(int(n)) if float(n).is_integer() else f"{n:.2f}"


@dataclass
class Estado:
    paso: str
    suma: float
    x: float
    y: float


def ejecutar(x: float, y: float) -> tuple[float, list[Estado]]:
    pasos: list[Estado] = []
    suma = 0.0
    pasos.append(Estado("Inicio", suma, x, y))

    suma += x
    pasos.append(Estado("suma = suma + x", suma, x, y))

    x = x + y ** 2
    pasos.append(Estado("x = x + y**2", suma, x, y))

    suma += x / y
    pasos.append(Estado("suma = suma + x/y", suma, x, y))

    return suma, pasos


def main():
    try:
        x = float(input("Ingrese X: ").strip())
        y = float(input("Ingrese Y: ").strip())
    except ValueError:
        print("Entrada inválida. Deben ser números.")
        return

    if y == 0:
        print("Y no puede ser 0 (división por cero).")
        return

    resultado, pasos = ejecutar(x, y)

    print("Prueba de escritorio")
    for p in pasos:
        print(f"{p.paso:22} -> SUMA={_fmt(p.suma)} X={_fmt(p.x)} Y={_fmt(p.y)}")

    print(f"\nEL VALOR DE LA SUMA ES: {_fmt(resultado)}")


if __name__ == "__main__":
    main()
