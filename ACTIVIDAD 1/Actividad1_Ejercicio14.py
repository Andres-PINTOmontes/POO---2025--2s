def main():
    try:
        n = float(input("Ingrese un número: ").strip())
    except ValueError:
        print("Entrada inválida. Debe ser un número.")
        return

    cuadrado = n ** 2
    cubo = n ** 3

    print(f"Cuadrado: {cuadrado}")
    print(f"Cubo: {cubo}")


if __name__ == "__main__":
    main()

