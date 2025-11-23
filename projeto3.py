# projeto3.py — Caso 3: Maximizar nº de arestas distintas sob custo ≤ K
# Autor: Otavio Bettega — 2025.2

import networkx as nx

def chinese_postman_max_edges_under_cost(G, K):
    """
    Retorna um caminho que maximiza o número de arestas distintas percorridas
    mantendo o custo total ≤ K.
    Estratégia gulosa: sempre pega a melhor aresta ainda não usada com menor custo.
    """
    if not nx.is_connected(G):
        raise ValueError("O grafo precisa ser conectado para este caso.")

    # Verifica se ponderado
    for u, v, d in G.edges(data=True):
        if "weight" not in d:
            raise ValueError("Caso 3 exige grafo com pesos.")

    best_path = []
    best_cost = 0.0
    best_edges_used = 0

    # Tentamos começar de cada vértice
    for start in G.nodes():
        used_edges = set()
        total_cost = 0.0
        path = [start]
        current = start

        while True:
            # Escolher entre TODAS as arestas não usadas
            candidatos = []
            for u, v, data in G.edges(data=True):
                if (u, v) not in used_edges and (v, u) not in used_edges:
                    candidatos.append((u, v, data["weight"]))

            # Ordenar por menor peso → maximiza nº de arestas dentro do orçamento
            candidatos.sort(key=lambda x: x[2])

            found = False
            for u, v, w in candidatos:
                # achar vizinho acessível a partir de "current"
                if u == current or v == current:
                    if total_cost + w <= K:
                        # Pegar essa aresta
                        used_edges.add((u, v))
                        total_cost += w
                        nxt = v if u == current else u
                        path.append(nxt)
                        current = nxt
                        found = True
                        break

            if not found:
                break

        if len(used_edges) > best_edges_used:
            best_edges_used = len(used_edges)
            best_cost = total_cost
            best_path = path

    stats = {
        "arestas_distintas": best_edges_used,
        "custo_total": best_cost,
        "K_limite": K
    }

    return [best_path], stats
