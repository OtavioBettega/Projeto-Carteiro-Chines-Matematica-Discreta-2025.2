# -*- coding: utf-8 -*-
# main.py — Interface principal para os Casos 1.1, 1.2 e 3
# Autor: Otavio Bettega — 2025.2

import networkx as nx
from projeto1 import ler_grafo_txt, chinese_postman_unweighted, desenhar_grafo
from projeto2 import chinese_postman_weighted
from projeto3 import chinese_postman_max_edges_under_cost


def ler_grafo_txt_generico(caminho_arquivo):
    """Detecta automaticamente se o grafo é ponderado ou não"""
    G = nx.Graph()
    is_weighted = False
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.strip() == "" or linha.strip().startswith("#"):
                continue
            partes = linha.strip().split()
            if len(partes) == 2:
                u, v = partes
                G.add_edge(u, v)
            elif len(partes) == 3:
                u, v, w = partes
                G.add_edge(u, v, weight=float(w))
                is_weighted = True
            else:
                raise ValueError("Formato inválido de linha: " + linha)
    return G, is_weighted


def main():
    print("=" * 60)
    print(" PROJETO — Problema do Carteiro Chinês (Casos 1.1, 1.2, 3) ")
    print("=" * 60)

    arquivo = input("\nDigite o caminho do arquivo .txt do grafo: ").strip()
    try:
        G, ponderado = ler_grafo_txt_generico(arquivo)
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return

    print("\nGrafo carregado com sucesso!")
    print(f" - Número de vértices: {G.number_of_nodes()}")
    print(f" - Número de arestas: {G.number_of_edges()}")
    print(f" - Tipo detectado: {'Ponderado' if ponderado else 'Não ponderado'}")

    print("\nEscolha o caso a executar:")
    print(" 1 — Caso 1.1 (não ponderado)")
    print(" 2 — Caso 1.2 (ponderado, ciclo euleriano mínimo)")
    print(" 3 — Caso 3 (ponderado, max arestas distintas sob custo ≤ k)")

    escolha = input("\nDigite 1, 2 ou 3: ").strip()

    if escolha == "1":
        if ponderado:
            print("\nAviso: o arquivo contém pesos, mas você escolheu Caso 1.1.")
            print("Usando apenas estrutura não ponderada.")
        print("\nExecutando Caso 1.1 (não ponderado)...")
        tours, stats = chinese_postman_unweighted(G)
        titulo = "Carteiro Chinês - Caso 1.1 (Não Ponderado)"

    elif escolha == "2":
        if not ponderado:
            print("\nErro: Caso 1.2 exige um grafo ponderado.")
            return
        print("\nExecutando Caso 1.2 (ponderado)...")
        tours, stats = chinese_postman_weighted(G)
        titulo = "Carteiro Chinês - Caso 1.2 (Ponderado)"

    elif escolha == "3":
        if not ponderado:
            print("\nErro: Caso 3 exige um grafo ponderado.")
            return
        k = float(input("\nDigite o custo máximo K permitido: ").strip())
        print("\nExecutando Caso 3 (maximizar número de arestas distintas sob custo ≤ K)...")
        tours, stats = chinese_postman_max_edges_under_cost(G, k)
        titulo = "Carteiro Chinês - Caso 3 (Max edges under cost K)"

    else:
        print("Opção inválida.")
        return

    print("\nResultado(s) encontrado(s):")
    for i, t in enumerate(tours, 1):
        print(f"  Caminho {i}: {' -> '.join(t)}")

    print("\nEstatísticas:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    if tours:
        desenhar_grafo(G, tours[0], titulo=titulo)




if __name__ == "__main__":
    main()
