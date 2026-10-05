# Desafio Target

Repositório com os 3 projetos desenvolvidos no desafio da Target, todos feitos em **Python**, sem dependências externas.

## Projetos

| Pasta | Projeto | Descrição |
|-------|---------|-----------|
| [Desafio Target 1](./Desafio%20Target%201) | [Cálculo de Comissão de Vendas](#projeto-1--cálculo-de-comissão-de-vendas) | Calcula a comissão de cada vendedor a partir de um JSON de vendas |
| [Desafio Target 2](./Desafio%20Target%202) | [Controle de Estoque](#projeto-2--controle-de-estoque) | Lançamento de entradas e saídas de mercadorias com validações e histórico |
| [Desafio Target 3](./Desafio%20Target%203) | [Cálculo de Juros](#projeto-3--cálculo-de-juros) | Calcula juros por atraso de uma conta usando JSON |

## Tecnologias

- Python 3.8+
- JSON
- Visual Studio Code

## Como executar

1. Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
```

2. Entre na pasta do projeto desejado:

```bash
cd "Desafio Target 1"
```

3. Execute o programa:

```bash
python comissao.py
```

> No Mac/Linux, use `python3`. É necessário ter o [Python 3](https://www.python.org/downloads/) instalado. Também é possível abrir o arquivo no VS Code (com a extensão **Python** da Microsoft) e clicar no botão ▶.

---

## Projeto 1 · Cálculo de Comissão de Vendas

Programa que lê um arquivo JSON com registros de vendas e calcula a comissão de cada vendedor.

### Regra de comissão

A regra é aplicada **a cada venda individualmente**:

| Valor da venda | Comissão |
|---|---|
| Abaixo de R$ 100,00 | Sem comissão |
| De R$ 100,00 até abaixo de R$ 500,00 | 1% |
| A partir de R$ 500,00 | 5% |

### Estrutura

```
Desafio Target 1/
├── comissao.py
└── vendas.json
```

### Como executar

```bash
cd "Desafio Target 1"
python comissao.py
```

### Formato do arquivo de entrada

```json
{
  "vendas": [
    { "vendedor": "Nome do Vendedor", "valor": 1200.50 }
  ]
}
```

### Resultado esperado

| Vendedor | Comissão |
|---|---|
| João Silva | R$ 495,68 |
| Maria Souza | R$ 465,95 |
| Carlos Oliveira | R$ 379,37 |
| Ana Lima | R$ 404,98 |

> O Python exibe os valores com ponto decimal (ex.: `495.68`).

### Decisões técnicas

- **`Decimal` em vez de `float`:** evita erros de arredondamento em cálculos monetários. O JSON é lido com `parse_float=Decimal`.
- **Arredondamento apenas no total final:** a comissão de cada venda é somada sem arredondar, e o total de cada vendedor é arredondado para 2 casas (`ROUND_HALF_UP`).
- **Limites da regra:** exatamente R$ 100,00 gera 1% e exatamente R$ 500,00 gera 5%.
- **Agrupamento:** as comissões são acumuladas por vendedor com `defaultdict`.

### Exemplo de cálculo (João Silva)

- Vendas de 5%: soma de R$ 9.703,25, que gera R$ 485,16
- Vendas de 1%: soma de R$ 1.051,45, que gera R$ 10,51
- **Total: R$ 495,68** (o arredondamento é feito sobre a soma exata, por isso não é a soma dos dois valores arredondados)

---

## Projeto 2 · Controle de Estoque

Programa de terminal para lançar movimentações de **entrada** e **saída** de mercadorias no depósito, a partir de um arquivo JSON de produtos.

### Funcionalidades

- Lançamento de movimentações de entrada e saída
- Número identificador **único e sequencial** para cada movimentação
- Descrição do tipo da movimentação (ex.: Compra, Venda, Devolução)
- Exibição da **quantidade final em estoque** do produto movimentado
- Validações: produto inexistente, quantidade inválida e saída maior que o estoque
- Consulta do estoque atual e histórico de movimentações
- Dados persistidos em JSON (o saldo é mantido entre execuções)

### Estrutura

```
Desafio Target 2/
├── main.py              # Código do programa
├── estoque.json         # Produtos e saldos de estoque
└── movimentacoes.json   # Histórico (criado automaticamente)
```

### Como executar

```bash
cd "Desafio Target 2"
python main.py
```

### Como usar

Ao iniciar, o menu é exibido:

```
===== CONTROLE DE ESTOQUE =====
1 - Lançar movimentação
2 - Consultar estoque
3 - Histórico de movimentações
0 - Sair
```

Para lançar uma movimentação (opção `1`), informe o **código do produto**, o **tipo** (`E` = Entrada / `S` = Saída), a **quantidade** e a **descrição**.

**Exemplo:**

```
Código do produto: 101
Tipo (E = Entrada / S = Saída): S
Quantidade: 20
Descrição da movimentação: Venda balcão

✔ Movimentação registrada!
  Nº da movimentação : 1
  Tipo               : SAÍDA - Venda balcão
  Produto            : Caneta Azul
  Quantidade         : 20
  ESTOQUE FINAL      : 130
```

### Formato dos dados

**estoque.json**

```json
{
  "estoque": [
    { "codigoProduto": 101, "descricaoProduto": "Caneta Azul", "estoque": 150 }
  ]
}
```

**movimentacoes.json** (gerado automaticamente)

```json
[
  {
    "id": 1,
    "data": "05/10/2026 14:30:00",
    "codigoProduto": 101,
    "tipo": "SAÍDA",
    "quantidade": 20,
    "descricao": "Venda balcão",
    "estoqueFinal": 130
  }
]
```

### Regras de negócio

- Cada movimentação recebe um ID único, que continua de onde parou mesmo após fechar o programa.
- A quantidade deve ser maior que zero.
- Não é permitida saída maior que o saldo disponível (o estoque nunca fica negativo).
- A cada lançamento, o `estoque.json` é atualizado com o novo saldo.

### Reiniciar os dados

1. Apague o arquivo `movimentacoes.json`.
2. Restaure os saldos originais no `estoque.json`.

---

## Projeto 3 · Cálculo de Juros

O programa recebe o **valor** de uma conta e a **data de vencimento**, e calcula os juros acumulados até a data de hoje, considerando **2,5% ao dia** (juros simples).

### Fórmula

```
juros = valor × 0,025 × dias em atraso
```

### Entrada e saída

Os dados são gravados em `dados.json` e o resultado em `resultado.json`.

### Como executar

```bash
cd "Desafio Target 3"
python calculo_juros.py
```

### Exemplo de uso

```
Valor da conta (R$): 100,00
Data de vencimento (DD/MM/AAAA): 25/09/2026

--- RESULTADO ---
Valor original : R$ 100.00
Vencimento     : 25/09/2026
Dias em atraso : 10
Juros          : R$ 25.00
Total a pagar  : R$ 125.00
```

---

## Autor

**[Luis Rodrigues]**
[GitHub](https://github.com/chegos) | [LinkedIn](https://www.linkedin.com/in/luis-rodrigues-03a169161)
