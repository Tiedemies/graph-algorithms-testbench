"""
# ============================================
# STUDENT IMPLEMENTATION FILE - TASK 1
# You may edit this file.
# Do NOT modify function signatures.
# ============================================

TASK 1: Shortest Paths with Maximal Blue Nodes

Given a graph where some vertices are marked as "blue", find the shortest path
from s to t that goes through the maximum number of blue vertices.

In other words:
1.  Among the shortest paths from s to t one has the highest number of blue vertices
2.  Return that number of blue vertices.

The graph will have a "blue" attribute on vertices (a set of vertex names).
"""

from graph import Graph
from collections import deque


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
        - Find the shorts path(s) using (single) BFS
        - Count blue vertices along the maximal blue the shortest path.
    """

    dist = {}
    blue_count = {}
    queue = deque([s])

    dist[s] = 0
    if s in graph.blue:
        blue_count[s] = 1
    else:
        blue_count[s] = 0

    while queue:
        vertex = queue.popleft()
        for v in graph.neighbors(vertex):
            new_dist = dist[vertex] + 1
            if v in graph.blue:
                new_blue = blue_count[vertex] + 1
            else:
                new_blue = blue_count[vertex]

            # Case 1: the vertex v hasn't been in dist
            if v not in dist:
                dist[v] = new_dist
                blue_count[v] = new_blue
                queue.append(v)

            # Case 2: the new distance is smaller than the current distance
            elif new_dist < dist[v]:
                dist[v] = new_dist
                blue_count[v] = new_blue
                queue.append(v)

            # Case 3: The distances are equal, but the new one has more
            # blue vertices than the current one
            elif new_dist == dist[v] and new_blue > blue_count[v]:
                blue_count[v] = new_blue
                queue.append(v)

    if t in dist:
        return blue_count[t]
    else:
        return 0

