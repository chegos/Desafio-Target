import json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP


def calcular_comissao(valor: Decimal) -> Decimal:
    """Aplica a regra de comissão a uma única venda."""
    if valor < 100:
        return Decimal("0")
    if valor < 500:
        return valor * Decimal("0.01")
    return valor * Decimal("0.05")


def main():
    # parse_float=Decimal evita erros de arredondamento do float
    with open("vendas.json", encoding="utf-8") as arquivo:
        dados = json.load(arquivo, parse_float=Decimal)

    comissoes = defaultdict(Decimal)
    for venda in dados["vendas"]:
        comissoes[venda["vendedor"]] += calcular_comissao(venda["valor"])

    print("COMISSÃO POR VENDEDOR")
    print("-" * 35)
    for vendedor, total in comissoes.items():
        total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        print(f"{vendedor:<18} R$ {total:>10,.2f}")


if __name__ == "__main__":
    main()