# Amazon Product Network Analysis

A final project for **SI 507** exploring graph-based analysis and interactive visualization of real-world Amazon product data.

## Project Overview

This project builds a network of Amazon products based on shared user reviews. Each product is represented as a node, and an edge is formed between two products if the same user has reviewed both. The resulting product graph enables:

-  **Product similarity detection** based on user overlap  
- **Shortest paths** between products via shared user activity  
- **Identification of highly connected (popular) products**  
- **Access to key product statistics** (rating, price, etc.)  
- **Interactive graph visualizations** (full and filtered views)


## Project Structure

```
finalproj/
├── app.py                   # Flask app entry point
├── build_graph.py           # Graph construction logic
├── load_and_clean.py        # Data loading and preprocessing
├── recommend_core.py        # Recommendation & analysis utilities
│
├── templates/               
│   ├── index.html
│   ├── stats.html
│   ├── recommend.html
│   ├── shortest.html
│   ├── popular.html
│   ├── data_summary.html
│   └── graph_view.html
│
├── static/
│   ├── graphs/              # Auto-generated Pyvis visualizations
│   │   ├── full_network.html
│   │   ├── shortest_path.html
│   │   └── static_network.png
│   └── style.css            # UI styles
│
└── data/
    ├── Electronics.json           # User reviews
    └── meta_Electronics.json      # Product metadata
```


## Setup Instructions

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd finalproj
```

### 2. Install dependencies

```bash
pip install flask pandas networkx pyvis
```

### 3. Run the application

```bash
python app.py
```

### 4. Open in your browser

Visit [http://localhost:5000](http://localhost:5000)


## Features & Functionality

| Feature                        | Description                                                  |
| ------------------------------ | ------------------------------------------------------------ |
| **Check Product Stats**        | View product name, price, rating, category, and product link |
| **Recommend Similar Products** | Based on co-reviewed products (graph neighbors)              |
| **Find Shortest Path**         | Shows the connection path between two products               |
| **Most Popular Product**       | Highlights the product with the highest degree (most co-reviewed) |
| **Full Graph Visualization**   | Interactive Pyvis graph of up to 500 nodes                   |
| **Hover Tooltips**             | Product name, rating, and price                              |
| **Edge Scaling**               | Log-scaled edge thickness based on weight                    |
| **Visual Highlights**          | Red = shortest path, Orange = most popular                   |


## Data Sources

This project uses **two related datasets** from the [UCSD Amazon Product Dataset Repository](https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/):

- **`meta_Electronics.json`**:  
  Product metadata (title, category, price, ratings, links)

- **`Electronics.json`**:  
  User reviews with reviewer IDs and product ratings

### Key Fields Used

- `asin` / `product_id`
- `title` / `product_name`
- `price`
- `category`
- `overall` (rating)
- `reviewerID` / `user_id`
- `product_link`


## Graph Construction

- Each product is a **node**
- Two products are connected by an **edge** if they were reviewed by the same user
- **Edge weight** = number of users who reviewed both
- Implemented using **NetworkX**
- Visualized using **Pyvis** with Barnes-Hut layout physics for readability


## Visual Demonstrations

- **View Full Network**: Explore the entire graph of product connections  
- **Shortest Path View**: See how one product is connected to another  
- **Popular Product Highlight**: Find products with high degree centrality  
