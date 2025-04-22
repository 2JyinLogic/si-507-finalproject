import networkx as nx


def recommend_similar(G, pid, topn=5):
    if pid not in G.nodes:
        return []

    neighbors = G[pid]
    sorted_neighbors = sorted(
        neighbors.items(), key=lambda x: x[1]["weight"], reverse=True
    )

    return sorted_neighbors[:topn]


def find_shortest_path(G, prod1, prod2):
    try:
        return nx.shortest_path(G, source=prod1, target=prod2)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None


def most_connected_product(G):
    if len(G.nodes) == 0:
        return None, 0
    return max(G.degree(), key=lambda x: x[1])


def get_product_stats(G, product_id):
    if product_id not in G:
        return None
    return G.nodes[product_id]
