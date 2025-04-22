import networkx as nx
from collections import defaultdict
from itertools import combinations
import pandas as pd


def build_graph(product_df, review_df):
    G = nx.Graph()

    for _, row in product_df.iterrows():
        G.add_node(
            row["product_id"],
            name=row.get("product_name", "Unnamed"),
            price=row.get("price", "N/A"),
            category=row.get("category", ""),
            brand=row.get("brand", ""),
            link=row.get("link", ""),
        )

    user_to_products = defaultdict(set)
    for _, row in review_df.iterrows():
        if pd.notna(row["user_id"]) and pd.notna(row["product_id"]):
            user_to_products[row["user_id"]].add(row["product_id"])

    for products in user_to_products.values():
        for p1, p2 in combinations(products, 2):
            if G.has_node(p1) and G.has_node(p2):
                if G.has_edge(p1, p2):
                    G[p1][p2]["weight"] += 1
                else:
                    G.add_edge(p1, p2, weight=1)

    print(
        f"[INFO] Constructed graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges."
    )
    return G

