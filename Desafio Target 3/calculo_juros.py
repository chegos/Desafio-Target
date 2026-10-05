import json
from datetime import datetime, date

TAXA_DIARIA = 0.025  # 2,5% ao dia
ARQUIVO_ENTRADA = "dados.json"
ARQUIVO_SAIDA = "resultado.json"


def pedir_dados():
    """Pede o valor e o vencimento ao usuário e salva em JSON."""
    valor = float(input("Valor da conta (R$): ").replace(",", "."))
    vencimento = input("Data de vencimento (DD/MM/AAAA): ")
    # valida o formato da data
    datetime.strptime(vencimento, "%d/%m/%Y")

    dados = {"valor": valor, "vencimento": vencimento}
    with open(ARQUIVO_ENTRADA, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def calcular():
    """Lê o JSON de entrada, calcula os juros e salva o resultado em JSON."""
    with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
        dados = json.load(f)

    valor = dados["valor"]
    vencimento = datetime.strptime(dados["vencimento"], "%d/%m/%Y").date()
    hoje = date.today()

    dias_atraso = (hoje - vencimento).days
    if dias_atraso < 0:
        dias_atraso = 0  # ainda não venceu

    juros = valor * TAXA_DIARIA * dias_atraso
    total = valor + juros

    resultado = {
        "valor_original": round(valor, 2),
        "vencimento": dados["vencimento"],
        "data_calculo": hoje.strftime("%d/%m/%Y"),
        "dias_em_atraso": dias_atraso,
        "taxa_diaria": "2,5%",
        "juros": round(juros, 2),
        "valor_total": round(total, 2),
    }

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    return resultado


def main():
    try:
        pedir_dados()
        r = calcular()
    except ValueError:
        print("Valor ou data inválidos. Use números e a data no formato DD/MM/AAAA.")
        return

    print("\n--- RESULTADO ---")
    print(f"Valor original : R$ {r['valor_original']:.2f}")
    print(f"Vencimento     : {r['vencimento']}")
    print(f"Dias em atraso : {r['dias_em_atraso']}")
    print(f"Juros          : R$ {r['juros']:.2f}")
    print(f"Total a pagar  : R$ {r['valor_total']:.2f}")
    print(f"\nResultado salvo em '{ARQUIVO_SAIDA}'.")


if __name__ == "__main__":
    main()