# -*- coding: utf-8 -*-
# Caso 1.1 - Carteiro Chinês (grafo não ponderado, repetições mínimas)
# Autor: Otavio Bettega - 2025.2

import networkx as nx
import matplotlib.pyplot as plt

def ler_grafo_txt(caminho_arquivo):
    """Lê um grafo não dirigido a partir de um arquivo .txt"""
    G = nx.Graph()
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.strip() == "" or linha.strip().startswith("#"):
                continue
            u, v = linha.strip().split()
            G.add_edge(u, v)
    return G


def chinese_postman_unweighted(G):
    """Resolve o problema do carteiro chinês para grafos não ponderados."""
    original_edges = G.number_of_edges()
    tours = []
    total_traversed = 0

    for comp_nodes in nx.connected_components(G):
        sub = G.subgraph(comp_nodes).copy()
        if sub.number_of_edges() == 0:
            continue

        M = nx.MultiGraph()
        M.add_nodes_from(sub.nodes())
        M.add_edges_from(sub.edges())

        odd = [n for n, d in sub.degree() if d % 2 == 1]

        if len(odd) > 0:
            dist = {}
            paths = {}
            for u in odd:
                lengths = dict(nx.single_source_shortest_path_length(sub, u))
                spaths = dict(nx.single_source_shortest_path(sub, u))
                for v in odd:
                    if u < v:
                        d = lengths.get(v, float('inf'))
                        dist[(u, v)] = d
                        paths[(u, v)] = spaths.get(v)

            K = nx.Graph()
            K.add_nodes_from(odd)
            for (u, v), d in dist.items():
                K.add_edge(u, v, weight=-d)

            matching = nx.max_weight_matching(K, maxcardinality=True)
            for a, b in matching:
                key = (a, b) if (a, b) in paths else (b, a)
                sp = paths[key]
                for i in range(len(sp) - 1):
                    M.add_edge(sp[i], sp[i + 1])

        euler_circuit = list(nx.eulerian_circuit(M))
        if euler_circuit:
            start = euler_circuit[0][0]
            tour = [start]
            for u, v in euler_circuit:
                tour.append(v)
        else:
            tour = []
        tours.append(tour)
        total_traversed += len(euler_circuit)

    stats = {
        'original_edges': original_edges,
        'total_traversed_edges': total_traversed,
        'repeated_edges': total_traversed - original_edges
    }
    return tours, stats


def desenhar_grafo(G, tour=None, titulo="Grafo"):
    """Desenha o grafo e opcionalmente destaca o caminho Euleriano."""
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6, 5))
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=800, font_size=10)
    if tour:
        edges_tour = list(zip(tour, tour[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges_tour, edge_color="red", width=2)
    plt.title(titulo)
    plt.show()


if __name__ == "__main__":
    arquivo = input("Digite o caminho do arquivo .txt do grafo: ").strip()
    G = ler_grafo_txt(arquivo)

    tours, stats = chinese_postman_unweighted(G)
    print("\nCircuito(s) encontrado(s):")
    for i, t in enumerate(tours, 1):
        print(f"  Componente {i}: {' -> '.join(t)}")

    print("\nEstatísticas:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    desenhar_grafo(G, tours[0] if tours else None, titulo="Carteiro Chinês - Caso 1.1")
