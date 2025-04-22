import pandas as pd
import json


def parse_json(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def load_reviews(path="data/Electronics.json", max_lines=2_000_000):
    rows = []
    for i, r in enumerate(parse_json(path)):
        if "reviewerID" in r and "asin" in r and "overall" in r:
            rows.append(
                {
                    "user_id": r["reviewerID"],
                    "product_id": r["asin"],
                    "rating": r["overall"],
                }
            )
        if i + 1 >= max_lines:
            break
        if (i + 1) % 500_000 == 0:
            print(f"[INFO] Parsed {i + 1} review lines...")

    df = pd.DataFrame(rows)
    df = df.dropna(subset=["user_id", "product_id", "rating"])
    df["product_id"] = df["product_id"].astype(str)
    print(f"[INFO] Loaded {len(df)} reviews (subset)")
    return df


def load_metadata(path="data/meta_Electronics.json", max_lines=500_000):
    rows = []
    for i, r in enumerate(parse_json(path)):
        if not isinstance(r, dict):
            continue

        asin = r.get("asin")
        if not asin:
            continue

        rows.append(
            {
                "product_id": asin,
                "product_name": r.get("title", ""),
                "price": r.get("price"),
                "category": "|".join(r.get("category", []))
                if isinstance(r.get("category"), list)
                else "",
                "brand": r.get("brand", ""),
                "link": f"https://www.amazon.com/dp/{asin}",  
            }
        )

        if i + 1 >= max_lines:
            break
        if (i + 1) % 200_000 == 0:
            print(f"[INFO] Parsed {i + 1} metadata lines...")

    df = pd.DataFrame(rows)
    df = df.dropna(subset=["product_id", "product_name"])
    df["product_id"] = df["product_id"].astype(str)
    print(f"[INFO] Loaded {len(df)} metadata entries (subset)")
    return df
