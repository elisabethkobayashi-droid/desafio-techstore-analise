"""
Desafio de Análise de Dados - TechStore
Análise exploratória, cálculos de métricas de negócio e visualizações.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# 1. CARREGAMENTO DOS DADOS
# ==========================================================
caminho_arquivo = "vendas.csv" if os.path.exists("vendas.csv") else "dados/vendas.csv"
df = pd.read_csv(caminho_arquivo)

# Converter a coluna de data para datetime
df["data_venda"] = pd.to_datetime(df["data_venda"])

# ==========================================================
# 2. EXIBIR INFORMAÇÕES BÁSICAS
# ==========================================================
print("=" * 60)
print("INFORMAÇÕES BÁSICAS DO DATASET")
print("=" * 60)

# Mostrar as 5 primeiras linhas
print("\n--- Primeiras 5 linhas do dataset ---")
print(df.head())

# Exibir o número total de registos (linhas)
total_linhas = len(df)
print(f"\nNúmero total de registos (linhas): {total_linhas}")

# Calcular a receita total (quantidade * preco_unitario)
df["receita_item"] = df["quantidade"] * df["preco_unitario"]
receita_total = df["receita_item"].sum()
print(f"Receita Total Gerada: R$ {receita_total:,.2f}")

# ==========================================================
# 3. CONSULTAS ESPECÍFICAS
# ==========================================================
print("\n" + "=" * 60)
print("CONSULTAS ESPECÍFICAS DO NEGÓCIO")
print("=" * 60)

# Filtrar e exibir as vendas da categoria 'Eletrônicos'
vendas_eletronicos = df[df["categoria"] == "Eletrônicos"]
print(f"\n--- Vendas da categoria 'Eletrônicos' ({len(vendas_eletronicos)} registos) ---")
print(vendas_eletronicos.head())

# Identificar e exibir o produto mais vendido (em quantidade)
vendas_por_produto = df.groupby("produto")["quantidade"].sum()
produto_mais_vendido = vendas_por_produto.idxmax()
total_qtd_mais_vendido = vendas_por_produto.max()
print(f"\nProduto mais vendido (em quantidade): {produto_mais_vendido} ({total_qtd_mais_vendido} unidades)")

# Descobrir e exibir a região com maior valor de compras (maior receita)
receita_por_regiao = df.groupby("regiao")["receita_item"].sum()
regiao_maior_compras = receita_por_regiao.idxmax()
total_valor_regiao = receita_por_regiao.max()
print(f"Região com maior valor de compras: {regiao_maior_compras} (R$ {total_valor_regiao:,.2f})")

# ==========================================================
# 4. DESAFIOS EXTRA (OPCIONAIS)
# ==========================================================
print("\n" + "=" * 60)
print("DESAFIO EXTRA: TABELA DINÂMICA E EXPORTAÇÃO")
print("=" * 60)

# Tabela dinâmica com receita por regiao x categoria
tabela_dinamica = df.pivot_table(
    values="receita_item",
    index="regiao",
    columns="categoria",
    aggfunc="sum",
    fill_value=0
)
print("\nTabela Dinâmica (Receita por Região x Categoria):")
print(tabela_dinamica)

# ==========================================================
# 5. GERAÇÃO DE VISUALIZAÇÕES GRÁFICAS
# ==========================================================
# 1. Gráfico de barras: Receita por categoria
receita_categoria = df.groupby("categoria")["receita_item"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 4.5))
receita_categoria.plot(kind="bar", color="#4C72B0", edgecolor="black")
plt.title("Receita Total por Categoria de Produto")
plt.xlabel("Categoria")
plt.ylabel("Receita (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("receita_por_categoria.png")
plt.close()

# 2. Gráfico de linha: Evolução das vendas por mês
df["mes_ano"] = df["data_venda"].dt.to_period("M").astype(str)
evolucao_mensal = df.groupby("mes_ano")["receita_item"].sum()

plt.figure(figsize=(9, 4.5))
evolucao_mensal.plot(kind="line", marker="o", color="#55A868", linewidth=2)
plt.title("Evolução Temporal das Vendas por Mês")
plt.xlabel("Mês")
plt.ylabel("Receita (R$)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("evolucao_vendas_mes.png")
plt.close()

print("\nGráficos gerados e guardados: 'receita_por_categoria.png' e 'evolucao_vendas_mes.png'")
