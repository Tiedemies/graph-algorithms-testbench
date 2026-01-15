"""
# ============================================
# STUDENT IMPLEMENTATION FILE - TASK 1
# You may edit this file.
# Do NOT modify function signatures.
# ============================================

TASK 1: Shortest Paths with Maximal Blue Nodes

Given a graph where some vertices are marked as "blue", find a shortest path
from s to t that goes through the maximum number of blue vertices.

In other words:
1. Find all shortest paths from s to t (paths with minimum number of edges)
2. Among those shortest paths, return the maximum number of blue vertices
   that can be visited on any single shortest path

The graph will have a "blue" attribute on vertices (a set of vertex names).
"""

from graph import Graph
from typing import Set


def max_blue_path(graph: Graph, s: str, t: str) -> int:
    """
    Find the maximum number of blue vertices on any shortest path from s to t.
    
    Args:
        graph: The input graph with a 'blue' attribute (set of blue vertex names)
        s: Source vertex
        t: Target vertex
        
    Returns:
        The maximum number of blue vertices that can be visited on any 
        shortest path from s to t. Returns 0 if no path exists.
        
    Raises:
        KeyError: If source or target vertex does not exist in graph
        
    Note:
        - Blue vertices are stored in graph.blue (a set)
        - You need to find shortest paths first, then count blue vertices
        - Only consider paths with minimum edge count (shortest paths)
    """
    # TODO: Implement maximal blue nodes on shortest paths
    # Hints:
    # 1. Use BFS to find distance from s to all vertices
    # 2. Use BFS from t to find distance to all vertices (reverse direction)
    # 3. A vertex v is on a shortest path if dist[s][v] + dist[v][t] == dist[s][t]
    # 4. Use dynamic programming or BFS to track max blue count along paths
    pass
