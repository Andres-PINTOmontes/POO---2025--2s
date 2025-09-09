from math import pi


def main():
    try:
        r = float(input("Ingrese el radio del círculo: ").strip())
    except ValueError:
        print("Entrada inválida. Debe ser un número.")
        return

    if r < 0:
        print("El radio no puede ser negativo.")
        return

    area = pi * (r ** 2)
    longitud = 2 * pi * r

    print(f"Área del círculo: {area}")
    print(f"Longitud de la circunferencia: {longitud}")


if __name__ == "__main__":
    main()

