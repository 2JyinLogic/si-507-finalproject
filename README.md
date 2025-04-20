# Amazon Product Network Analysis

A final project for **SI 507** showcasing graph-based analysis and interactive visualization of Amazon product data.


## Project Overview

This project explores connections between Amazon products based on shared user interactions (e.g., common reviewers). Using a graph data structure, we analyze and visualize:

- Product similarity and co-occurrence  
- The most "popular" or highly connected products  
- Shortest connection paths between two products  
- Product statistics (rating, price, etc.)  
- Interactive visualizations by category or full dataset  



## File Structure

```
finalproj/
│
├── app.py                   # Flask app entry point
├── build_graph.py           # Constructs graph from dataset
├── load_and_clean.py        # Loads and preprocesses raw data
├── recommend_core.py        # Core functions: recommend, stats, shortest path
│
├── templates/               # Jinja2 HTML templates
│   ├── index.html
│   ├── stats.html
│   ├── recommend.html
│   ├── shortest.html
│   └── graph_view.html
│
├── static/
│   ├── graphs/              # Auto-generated Pyvis graph HTML
│   └── style.css            # Optional custom CSS
│
└── amazon.csv               # Source data file
```


## Setup Instructions

1. **Clone the repo**

```bash
git clone <your-repo-url>
cd finalproj
```

2. **Install required packages**

```bash
pip install flask pandas networkx pyvis
```

3. **Run the app**

```bash
python app.py
```


4. **Open in browser**

Visit: [http://localhost:5000](http://localhost:5000)


## Features

| Function | Description |
|----------|-------------|
| `Check Product Stats` | Input a `product_id` to see its name, rating, price, and link |
| `Recommend Similar Products` | Based on user overlap (graph neighbors) |
| `Find Shortest Path` | Between two products (smallest co-review path) |
| `Most Popular Product` | Node with highest degree |
| `Graph Visualization` | Full graph or category-specific interactive network |
| `Tooltip Info` | On hover: product name, rating, price |
| `Highlighting` | Shortest path in red, most connected in orange |
| `Edge Scaling` | Weight visualized with logarithmic thickness |


## Data Description

- **Source**: `amazon.csv`  
- **Attributes used**:
  - `product_id`
  - `product_name`
  - `discounted_price`
  - `rating`
  - `user_id` (for co-purchase edges)
  - `category`
  - `product_link`


## Graph Details

- Undirected graph built via shared users:
  - Edge weight = number of users who interacted with both products
- `NetworkX` used for backend graph structure
- `Pyvis` used for interactive frontend rendering


## Visual Samples

- `View Full Product Network`  
  Displays entire dataset as a product co-review graph

- `View Category Network`  
  Filter by top-level category to focus graph view

- `Visualize Shortest Path`  
  Animates shortest connection between any two nodes

