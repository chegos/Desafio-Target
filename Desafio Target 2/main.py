import json
import os
from datetime import datetime

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQ_ESTOQUE = os.path.join(PASTA, "estoque.json")
ARQ_MOVIMENTOS = os.path.join(PASTA, "movimentacoes.json")


# ---------- Persistência ----------
def carregar_estoque():
    with open(ARQ_ESTOQUE, "r", encoding="utf-8") as f:
        return json.load(f)["estoque"]


def salvar_estoque(produtos):
    with open(ARQ_ESTOQUE, "w", encoding="utf-8") as f:
        json.dump({"estoque": produtos}, f, ensure_ascii=False, indent=2)


def carregar_movimentos():
    if not os.path.exists(ARQ_MOVIMENTOS):
        return []
    with open(ARQ_MOVIMENTOS, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_movimentos(movimentos):
    with open(ARQ_MOVIMENTOS, "w", encoding="utf-8") as f:
        json.dump(movimentos, f, ensure_ascii=False, indent=2)


# ---------- Regras de negócio ----------
def buscar_produto(produtos, codigo):
    for p in produtos:
        if p["codigoProduto"] == codigo:
            return p
    return None


def proximo_id(movimentos):
    """Identificador único e sequencial (continua de onde parou)."""
    return max((m["id"] for m in movimentos), default=0) + 1


def lancar_movimentacao(produtos, movimentos, codigo, tipo, quantidade, descricao):
    produto = buscar_produto(produtos, codigo)
    if produto is None:
        raise ValueError("Produto não encontrado.")
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")
    if tipo == "S" and quantidade > produto["estoque"]:
        raise ValueError(
            f"Estoque insuficiente. Disponível: {produto['estoque']}."
        )

    produto["estoque"] += quantidade if tipo == "E" else -quantidade

    mov = {
        "id": proximo_id(movimentos),
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "codigoProduto": codigo,
        "tipo": "ENTRADA" if tipo == "E" else "SAÍDA",
        "quantidade": quantidade,
        "descricao": descricao,
        "estoqueFinal": produto["estoque"],
    }
    movimentos.append(mov)
    salvar_estoque(produtos)
    salvar_movimentos(movimentos)
    return mov


# ---------- Interface (terminal) ----------
def listar_produtos(produtos):
    print("\nCÓDIGO | PRODUTO                       | ESTOQUE")
    print("-" * 52)
    for p in produtos:
        print(f"{p['codigoProduto']:<6} | {p['descricaoProduto']:<29} | {p['estoque']}")


def ler_inteiro(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro válido.")


def tela_movimentacao(produtos, movimentos):
    listar_produtos(produtos)
    codigo = ler_inteiro("\nCódigo do produto: ")
    produto = buscar_produto(produtos, codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    tipo = ""
    while tipo not in ("E", "S"):
        tipo = input("Tipo (E = Entrada / S = Saída): ").strip().upper()

    quantidade = ler_inteiro("Quantidade: ")
    descricao = input("Descrição da movimentação (ex: Compra, Venda, Devolução): ").strip()
    if not descricao:
        descricao = "Entrada de mercadoria" if tipo == "E" else "Saída de mercadoria"

    try:
        mov = lancar_movimentacao(produtos, movimentos, codigo, tipo, quantidade, descricao)
    except ValueError as erro:
        print(f"\n[ERRO] {erro}")
        return

    print("\n✔ Movimentação registrada!")
    print(f"  Nº da movimentação : {mov['id']}")
    print(f"  Tipo               : {mov['tipo']} - {mov['descricao']}")
    print(f"  Produto            : {produto['descricaoProduto']}")
    print(f"  Quantidade         : {mov['quantidade']}")
    print(f"  ESTOQUE FINAL      : {mov['estoqueFinal']}")


def tela_historico(movimentos):
    if not movimentos:
        print("\nNenhuma movimentação registrada.")
        return
    print("\nID  | DATA                | PROD | TIPO    | QTDE | FINAL | DESCRIÇÃO")
    print("-" * 80)
    for m in movimentos:
        print(
            f"{m['id']:<3} | {m['data']} | {m['codigoProduto']:<4} | "
            f"{m['tipo']:<7} | {m['quantidade']:<4} | {m['estoqueFinal']:<5} | {m['descricao']}"
        )


def main():
    produtos = carregar_estoque()
    movimentos = carregar_movimentos()

    while True:
        print("\n===== CONTROLE DE ESTOQUE =====")
        print("1 - Lançar movimentação")
        print("2 - Consultar estoque")
        print("3 - Histórico de movimentações")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            tela_movimentacao(produtos, movimentos)
        elif opcao == "2":
            listar_produtos(produtos)
        elif opcao == "3":
            tela_historico(movimentos)
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()