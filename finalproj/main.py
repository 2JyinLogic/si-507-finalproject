from load_and_clean import load_reviews, load_metadata
from build_graph import build_graph
from recommend_core import (
    recommend_similar,
    find_shortest_path,
    most_connected_product,
    get_product_stats
)

def run_interface(G):
    print("Amazon Product Recommendation System")
    while True:
        print("\nChoose an option:")
        print("1. Recommend similar/complementary products")
        print("2. Find shortest path between two products")
        print("3. Find most connected (popular) product")
        print("4. Get stats for a product")
        print("5. Exit")
        choice = input("Enter choice number: ")

        if choice == '1':
            pid = input("Enter product ID: ")
            recs = recommend_similar(G, pid)
            if recs:
                print("Recommendations:")
                for rec_id, data in recs:
                    weight = data["weight"] if isinstance(data, dict) else data
                    print(f"- {G.nodes[rec_id].get('name', 'Unnamed')} (ID: {rec_id}, shared users: {weight})")
            else:
                print("Product not found or has no similar items.")

        elif choice == '2':
            p1 = input("Enter first product ID: ")
            p2 = input("Enter second product ID: ")
            path = find_shortest_path(G, p1, p2)
            if path:
                print("Shortest path:")
                for pid in path:
                    print(f"> {G.nodes[pid].get('name', 'Unnamed')} (ID: {pid})")
            else:
                print("No path found or product(s) invalid.")

        elif choice == '3':
            pid, degree = most_connected_product(G)
            info = G.nodes[pid]
            print(f"Most connected product: {info.get('name', 'Unnamed')} (ID: {pid}, connections: {degree})")

        elif choice == '4':
            pid = input("Enter product ID: ")
            info = get_product_stats(G, pid)
            if info:
                print(f"Name: {info.get('name', 'N/A')}")
                print(f"Rating: {info.get('rating', 'N/A')}")
                print(f"Price: ${info.get('price', 'N/A')}")
                print(f"Link: {info.get('link', 'N/A')}")
            else:
                print("Product not found.")

        elif choice == '5':
            print("Goodbye.")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    review_df = load_reviews("data/Electronics.json")
    product_df = load_metadata("data/meta_Electronics.json")

    common_ids = set(product_df["product_id"]) & set(review_df["product_id"])
    product_df = product_df[product_df["product_id"].isin(common_ids)]
    review_df = review_df[review_df["product_id"].isin(common_ids)]

    print(f"[INFO] Loaded {len(product_df)} products and {len(review_df)} reviews with common IDs.")

    G = build_graph(product_df, review_df)
    run_interface(G)
