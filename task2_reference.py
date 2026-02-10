"""
# ============================================
# Teacher implementation for Task 2
# You may not edit this file.
# ============================================
TASK 2: Minimum Spanning Trees

Implement two functions:
1. MST(graph) - Find a minimum spanning tree
2. second_best_ST(graph) - Find the second-best spanning tree

You may implement Union-Find in this file or use the example from examples/union_find_example.py
"""

from graph import Graph
from typing import List, Tuple, Optional


def MST(graph: Graph) -> List[Tuple[str, str, float]]:
    """
    Find a minimum spanning tree.
    
    Args:
        graph: An undirected, weighted graph
        
    Returns:
        A list of edges (u, v, weight) that form the MST.
        
    Raises:
        ValueError: If graph is directed
    
    Note: Uses Prims' algorithm.
    """
    if graph.directed:
        raise ValueError("MST is not defined for directed graphs")
    ## Import a priority queue that can be updated easily.
    from pq import PQ
    ## we use the heapq as our priority queue
    Q = PQ()
    k = {}
    pi = {}
    for v in graph.vertices():
        k[v] = float('inf')
        pi[v] = None
    ## Start from an arbitrary vertex
    s = next(iter(graph.vertices()))
    k[s] = 0
    for v in graph.vertices():
        Q.push(v, k[v])
    mst_edges = []
    while Q:
        u, key_u = Q.extract_min()
        if pi[u] is not None:
            assert graph.weight(pi[u], u) == key_u
            mst_edges.append((pi[u], u, k[u]))
        for v in graph._adjacency[u]:
            w = min(graph.weight(u, v), graph.weight(v, u))
            if v in Q.items and w < k[v]:
                k[v] = w
                pi[v] = u
                # Update priority queue NOTE: This is the Update operation
                Q.update(v, w)
    return mst_edges

## A helper function to find the cycle and the maximum edge in it
def find_cycle_and_max_edge(graph: Graph, tree_edges: List[Tuple[str, str, float]], added_edge: Tuple[str, str, float]) -> Tuple[str, str, float]:
    s = added_edge[0]
    t = added_edge[1]
    parent = {}
    visited = set()
    ## Define DFS to find path from s to t along treen edges
    def dfs(u) -> bool:
        visited.add(u)
        for v in graph._adjacency[u]:
            if (u, v, graph.weight(u, v)) in tree_edges or (v, u, graph.weight(u, v)) in tree_edges:
                if v == t:
                    parent[v] = u
                    return True
                if v not in visited:
                    parent[v] = u
                    found = dfs(v)
                    if found:
                        return True
        return False
    dfs(s)
    # Reconstruct path from s to t and find max edge
    path = []
    current = t
    max_edge = (None, None, -1)
    while current != s:
        p = parent[current]
        edge_weight = graph.weight(p, current)
        path.append((p, current, edge_weight))
        if edge_weight > max_edge[2]:
            max_edge = (p, current, edge_weight)
        current = p
    return max_edge
                


def second_best_ST(graph: Graph) -> Optional[List[Tuple[str, str, float]]]:
    """
    Find the second-best spanning tree.
    
    The second-best spanning tree is a spanning tree with weight > MST weight,
    but the smallest weight possible among all spanning trees.
    
    Args:
        graph: An undirected, weighted graph
        
    Returns:
        A list of edges forming the second-best spanning tree,
        or None if no second-best spanning tree exists.
        
    Raises:
        ValueError: If graph is directed
        
    Hint:
        One MST algorithm works as follows:
        1. Find the MST
        2. For each edge NOT in MST, try adding it (creates a cycle)
        3. Remove the heaviest edge in that cycle (other than the added edge)
        4. This gives a candidate spanning tree.
        5. Return the candidate with minimum weight.

        NOTE: This is just a hint, you may implement it differently.
        NOTE: Naive implementations may be too slow for large graphs.
    """
    assert not graph.directed, "second_best_ST does not support directed graphs"
    mst = MST(graph)
    mst_weight = sum(weight for u, v, weight in mst)
    edges_in_graph = [ (u, v, graph.weight(u, v)) for u in graph.vertices() for v in graph._adjacency[u] if u < v and (u, v, graph.weight(u, v)) not in mst and (v, u, graph.weight(u, v)) not in mst ]
    edges_in_graph.sort(key=lambda x: x[2])
    ## We dtart with infinity as the second best
    second_best = float('inf') 
    candidate_tree = None
    for u, v, weight in edges_in_graph:
        max_edge = find_cycle_and_max_edge(graph, mst, (u, v, weight))
        ## THe max edge should not be heavier than weight; if it is, then the tree was not mst
        assert max_edge[2] <= weight, "MST property violated, a lighter tree found!!"
        if max_edge[2] < weight:
            candidate_weight = mst_weight - max_edge[2] + weight
            if candidate_weight < second_best:
                second_best = candidate_weight
                # Construct the new tree edges - remove max_edge (check both directions)
                candidate_tree = []
                for edge in mst:
                    # Check if this edge matches max_edge (either direction)
                    if edge == max_edge or edge == (max_edge[1], max_edge[0], max_edge[2]):
                        continue  # Skip this edge
                    candidate_tree.append(edge)
                candidate_tree.append((u, v, weight))
    return candidate_tree
               





