import math
from flask import Flask, render_template, request
from load_and_clean import load_reviews, load_metadata
from build_graph import build_graph
from recommend_core import (
    get_product_stats,
    recommend_similar,
    find_shortest_path,
    most_connected_product,
)
from pyvis.network import Network

app = Flask(__name__)

# Load datasets
review_df = load_reviews("data/Electronics.json")
product_df = load_metadata("data/meta_Electronics.json")

common_ids = set(product_df["product_id"]) & set(review_df["product_id"])

product_df = product_df[product_df["product_id"].isin(common_ids)]
review_df = review_df[review_df["product_id"].isin(common_ids)]

print(
    "[INFO] Loaded {} products and {} reviews with common IDs.".format(
        len(product_df), len(review_df)
    )
)

G = build_graph(product_df, review_df)


@app.route("/")
def index():
    product_df["main_category"] = (
        product_df["category"].astype(str).str.split("|").str[0]
    )
    categories = sorted(set(product_df["main_category"].dropna()))
    return render_template("index.html", categories=categories)


@app.route("/stats", methods=["POST"])
def product_stats():
    pid = request.form.get("product_id")
    info = get_product_stats(G, pid)
    if info:
        return render_template("stats.html", info=info, pid=pid)
    return f"Product ID {pid} not found."


@app.route("/recommend", methods=["POST"])
def recommend():
    pid = request.form.get("product_id")
    results = recommend_similar(G, pid)
    if results:
        products = [
            (G.nodes[pid].get("name", "Unnamed"), pid, data["weight"])
            for pid, data in results
        ]
        return render_template("recommend.html", products=products, base_pid=pid)
    return f"No similar items found for product {pid}."


@app.route("/shortest", methods=["POST"])
def shortest():
    p1 = request.form.get("product1")
    p2 = request.form.get("product2")
    path = find_shortest_path(G, p1, p2)
    if path:
        named_path = [(pid, G.nodes[pid]["name"]) for pid in path]
        return render_template("shortest.html", path=named_path, p1=p1, p2=p2)
    return f"No path found between {p1} and {p2}."


@app.route("/popular")
def popular():
    pid, degree = most_connected_product(G)
    if not pid:
        return "No connected products found."
    info = G.nodes[pid]
    return render_template("popular.html", pid=pid, degree=degree, info=info)


@app.route("/data-summary")
def data_summary():
    # Top 10 rated products
    top_products = (
        product_df.sort_values(by="rating", ascending=False)
        .head(10)[["product_id", "name", "rating"]]
        .to_dict("records")
    )

    # Category distribution
    category_counts = product_df["category"].value_counts().to_dict()

    return render_template(
        "data_summary.html", top_products=top_products, category_counts=category_counts
    )


@app.route("/visual/network")
def visualize_network():
    category = request.args.get("category")
    net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")

    popular_id, _ = most_connected_product(G)

    max_nodes = 100
    selected_nodes = []

    for node, data in G.nodes(data=True):
        if "name" not in data:
            continue

        if category:
            raw_cat = str(data.get("category", ""))
            main_cat = raw_cat.split("|")[0]
            if category != main_cat:
                continue

        selected_nodes.append((node, data))
        if len(selected_nodes) >= max_nodes:
            break

    selected_ids = {n[0] for n in selected_nodes}

    for node, data in selected_nodes:
        title = f"{data['name']}<br>Rating: {data.get('rating', 'N/A')}<br>Price: {data.get('price', 'N/A')}"
        color = "orange" if node == popular_id else "lightblue"
        size = 30 if node == popular_id else 15

        net.add_node(
            node,
            label=node,
            title=title,
            color=color,
            size=size,
            url=f"/stats?product_id={node}",
        )

    edge_count = 0
    max_edges = 300
    for source, target, data in G.edges(data=True):
        if source in selected_ids and target in selected_ids:
            net.add_edge(source, target, value=math.log(data["weight"] + 1))
            edge_count += 1
            if edge_count >= max_edges:
                break

    print(f"[DEMO] Visualized {len(selected_ids)} nodes and {edge_count} edges.")

    net.save_graph("static/graphs/full_network.html")
    return render_template("graph_view.html", graph_file="graphs/full_network.html")


@app.route("/visual/path", methods=["POST"])
def visualize_shortest_path():
    p1 = request.form.get("product1")
    p2 = request.form.get("product2")

    path = find_shortest_path(G, p1, p2)

    if not path or len(path) > 15:
        return render_template(
            "graph_view.html",
            graph_file=None,
            error=f"No path found between {p1} and {p2}, or path too long to render.",
        )

    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    net.toggle_physics(False)

    path_edges = list(zip(path, path[1:]))

    for node in path:
        data = G.nodes[node]
        label = data.get("name", node)
        title = f"{label}<br>Price: {data.get('price', 'N/A')}"
        net.add_node(
            node,
            label=label,
            title=title,
            color="red",
            size=20,
            url=f"/stats?product_id={node}",
        )

    for src, tgt in path_edges:
        net.add_edge(src, tgt, color="red", width=3)

    output_path = "static/graphs/shortest_path.html"
    net.save_graph(output_path)

    return render_template("graph_view.html", graph_file="graphs/shortest_path.html")


@app.route("/connected", methods=["GET", "POST"])
def connected_products():
    if request.method == "POST":
        pid = request.form.get("product_id")
        if not G.has_node(pid):
            return render_template(
                "connected.html",
                base_pid=pid,
                neighbors=None,
                error="Product not found in graph.",
            )

        neighbors = []
        for neighbor in G.neighbors(pid):
            neighbors.append(
                {"id": neighbor, "name": G.nodes[neighbor].get("name", "Unnamed")}
            )

        return render_template("connected.html", base_pid=pid, neighbors=neighbors)

    return render_template("connected.html", base_pid=None, neighbors=None)


if __name__ == "__main__":
    print("Flask app is running at http://localhost:5000")
    app.run(debug=True, use_reloader=False)
