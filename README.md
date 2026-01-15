# Graph Algorithms Test Bench

**Course Programming Assignments Repository**

This repository provides a complete testing and execution environment for graph algorithm programming assignments. Students implement core algorithms while the infrastructure handles graph loading, parsing, and testing.

---

## ⚠️ Important Rules

### **YOU SHOULD EDIT:**
- `tasks/task1_bfs.py` - Implement the maximal blue nodes on shortest paths algorithm
- `tasks/task2_mst.py` - Implement MST and 2nd MST algorithms
- `tasks/task3_choice.py` - Implement your chosen algorithm

### **YOU SHOULD NOT EDIT:**
- `graph/graph.py` - Graph class (instructor-provided)
- `graph/loaders.py` - Graph loading utilities
- `examples/` - Reference implementations (read-only)
- `test_task1.py`, `test_task2.py`, `test_task3.py` - Test scripts

**Violation of these rules may result in assignment rejection.**

---

## 📋 Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd GraphEdu
```

### 2. No External Dependencies Required
This project uses only Python standard library. No additional packages need to be installed.

### 3. Verify Setup
Run the example files to ensure everything works:
```bash
python examples/bfs_example.py
python examples/dfs_example.py
```

---

## 🎯 Your Tasks

### **Task 1: Shortest Paths with maximal blue nodes**
**File:** `tasks/task1_bfs.py`

Implement "max_blue_path(graph, s, t)" that returns the maximum number of "blue" vertices

**Test:** `python test_task1.py graphfile s t`

---

### **Task 2: Minimum Spanning Trees and second spanning tree **
**File:** `tasks/task2_mst.py`

Implement two functions:

1. MST(graph) -- returns the edges that form the MST
2. second_best_ST(graph)` - Find the second-best spanning tree, i.e., the set of edges that form a spanning tree with weight > than MST, but
smallest weight possible for all spanning trees. 

You may implement Union-Find in this file or use `examples/union_find_example.py`, if you think it is necessary 

**Test:** `python test_task2.py graphfile`

---

### **Task 3: Algorithm of Your Choice**
## Either an algorithm for betweenness centrality of vertices (A)
## OR an algorithm for community detection (B)

Implement one of two functions:
1. centralities(graph) -- returns a dictionary of the vertices of graph where the values are betweenness centralities
2. communities(graph) -- returns an iterable of iterables (sets) such that each vertex belongs to one set, these sets are communities

**File:** `tasks/task3_choice.py`


**Test (centrality):** `python test_task3.py -A graphfile`
**Test (community):** `python test_task3.py -B graphfile`
---

## 🧪 Testing Your Code

Each task has a standalone test script that takes a graph file as input.
For the community detection, we do not report correctenss, instead we report on overlap metric of the sets produced by other
methods; there is no strict correctness in that task. 

---

## 📚 Using the Graph API

All tasks use the same `Graph` class. Here's how to use it:

### Creating Graphs
```python
from graph import Graph

# Undirected, unweighted graph
g = Graph(directed=False, weighted=False)

# Directed, weighted graph
g = Graph(directed=True, weighted=True)
```

### Adding Vertices and Edges
```python
g.add_vertex("A")
g.add_edge("A", "B")  # Unweighted (weight = 1.0)
g.add_edge("A", "C", 5.0)  # Weighted
```

### Querying the Graph
```python
vertices = g.vertices()  # List of all vertices
neighbors = g.neighbors("A")  # List of A's neighbors
edges = g.edges()  # List of (u, v, weight) tuples
weight = g.weight("A", "B")  # Get edge weight
has_edge = g.has_edge("A", "B")  # Check if edge exists
```

### Loading Graphs from Files
```python
from graph import load_graph

g = load_graph("data/small_graph.json")
g = load_graph("data/weighted_graph.json")
```

**See `examples/` for complete usage examples.**

---

## 📖 Example Implementations

The `examples/` directory contains reference implementations:

- `bfs_example.py` - Breadth-first search
- `dfs_example.py` - Depth-first search
- `dijkstra_example.py` - Dijkstra's algorithm
- `union_find_example.py` - Union-Find data structure

**These are for learning purposes.** You may read and understand them, but:
- DO NOT copy-paste code directly
- DO use them to understand the Graph API
- DO use Union-Find from examples in Task 2 if needed

---

## 📊 Sample Data Files


---

## 📦 Submission Instructions

Submit **ONLY** the following files:
- `tasks/task1_bfs.py` for the first assignment
- `tasks/task2_mst.py` for the second assignment
- `tasks/task3_choice.py` for the third assignment

