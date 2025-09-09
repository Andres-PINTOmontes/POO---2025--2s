from dataclasses import dataclass


def _fmt_money(v: float) -> str:
    return (f"${v:,.2f}"  # 1,234.56
            .replace(",", "_")
            .replace(".", ",")
            .replace("_", "."))


def _read_float(prompt: str, default: float) -> float:
    raw = input(f"{prompt} [{default}]: ").strip()
    return default if raw == "" else float(raw)


@dataclass
class Nomina:
    horas: float
    tarifa_hora: float
    retencion_pct: float  # porcentaje, ej. 12.5

    @property
    def salario_bruto(self) -> float:
        return self.horas * self.tarifa_hora

    @property
    def retencion_fuente(self) -> float:
        return self.salario_bruto * (self.retencion_pct / 100.0)

    @property
    def salario_neto(self) -> float:
        return self.salario_bruto - self.retencion_fuente


def main():
    try:
        horas = _read_float("Horas trabajadas", 48)
        tarifa = _read_float("Tarifa por hora ($)", 5000)
        pct = _read_float("% Retención en la fuente", 12.5)
    except ValueError:
        print("Entrada inválida. Use números.")
        return

    if horas < 0 or tarifa < 0 or not (0 <= pct <= 100):
        print("Valores fuera de rango: horas/tarifa no negativas y % entre 0 y 100.")
        return

    n = Nomina(horas, tarifa, pct)

    print("Resultados:")
    print(f"Salario bruto: {_fmt_money(n.salario_bruto)}")
    print(f"Retención en la fuente: {_fmt_money(n.retencion_fuente)}")
    print(f"Salario neto: {_fmt_money(n.salario_neto)}")


if __name__ == "__main__":
    main()

