# -*- coding: utf-8 -*-
# Caso 1.2 - Carteiro Chinês (grafo ponderado, minimizando custo total)
# Autor: Otavio Bettega - 2025.2

import networkx as nx
from projeto1 import desenhar_grafo


def chinese_postman_weighted(G):
    """
    Resolve o Problema do Carteiro Chinês (Caso 1.2)
    - Grafo ponderado (pesos positivos)
    - Minimiza o custo total de percorrer todas as arestas ao menos uma vez

    Supõe que G é um grafo simples, não direcionado (networkx.Graph).
    Um MultiGraph é usado apenas internamente para representar arestas duplicadas.
    """
    if not isinstance(G, nx.Graph):
        raise TypeError("G deve ser um networkx.Graph não direcionado e simples")

    original_edges = G.number_of_edges()
    total_original_cost = sum(d.get("weight", 1) for _, _, d in G.edges(data=True))
    tours = []
    total_cost = 0.0

    # Trabalhamos componente por componente
    for comp_nodes in nx.connected_components(G):
        sub = G.subgraph(comp_nodes).copy()
        if sub.number_of_edges() == 0:
            continue

        # MultiGraph para permitir duplicações
        M = nx.MultiGraph()
        for u, v, data in sub.edges(data=True):
            w = data.get("weight", 1)
            M.add_edge(u, v, weight=w)

        # Vértices de grau ímpar na componente
        odd = [n for n, d in sub.degree() if d % 2 == 1]

        if len(odd) > 0:
            dist, paths = {}, {}

            # Distâncias e caminhos mínimos entre vértices ímpares (Dijkstra)
            for u in odd:
                lengths, paths_u = nx.single_source_dijkstra(sub, u, weight="weight")
                for v in odd:
                    if u < v:
                        d = lengths.get(v, float("inf"))
                        if d < float("inf"):
                            dist[(u, v)] = d
                            paths[(u, v)] = paths_u.get(v)

            # Grafo completo auxiliar sobre os vértices ímpares, com pesos -d(u,v)
            if dist:
                K = nx.Graph()
                K.add_nodes_from(odd)
                for (u, v), d in dist.items():
                    K.add_edge(u, v, weight=-d)

                # Emparelhamento perfeito de peso máximo em K
                # (equivalente a emparelhamento de menor custo nas distâncias reais)
                matching = nx.max_weight_matching(K, maxcardinality=True)

                # Duplicação dos caminhos mínimos correspondentes ao emparelhamento
                for a, b in matching:
                    key = (a, b) if (a, b) in paths else (b, a)
                    sp = paths.get(key)
                    if sp:
                        for i in range(len(sp) - 1):
                            w = sub[sp[i]][sp[i + 1]]["weight"]
                            M.add_edge(sp[i], sp[i + 1], weight=w)

        # Extração do circuito Euleriano no multigrafo M
        euler_circuit = list(nx.eulerian_circuit(M, keys=True))
        if euler_circuit:
            start = euler_circuit[0][0]
            tour = [start]
            cost = 0.0
            for u, v, edge_key in euler_circuit:
                w = M[u][v][edge_key]["weight"]
                tour.append(v)
                cost += w
        else:
            tour, cost = [], 0.0

        tours.append(tour)
        total_cost += cost

    stats = {
        "original_edges": original_edges,
        "original_cost": total_original_cost,
        "total_cost": total_cost,
        "extra_cost": total_cost - total_original_cost,
    }
    return tours, stats
