"""
Example: Dijkstra's Shortest Path Algorithm

This is a reference implementation for educational purposes.
Students should read this to understand how to use the Graph API.

DO NOT COPY THIS CODE DIRECTLY INTO YOUR ASSIGNMENTS.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from graph import Graph
import heapq


def dijkstra(graph: Graph, source: str) -> dict:
    """
    Compute shortest path distances from source to all vertices using Dijkstra's algorithm.
    
    Args:
        graph: A weighted graph (directed or undirected)
        source: The source vertex
        
    Returns:
        A dictionary mapping each vertex to its shortest distance from source.
        Uses float('inf') for unreachable vertices.
        
    Raises:
        KeyError: If source does not exist
        ValueError: If graph has negative edge weights
    """
    if source not in graph.vertices():
        raise KeyError(f"Source vertex {source} not found in graph")
    
    # Check for negative weights
    for u, v, w in graph.edges():
        if w < 0:
            raise ValueError("Dijkstra's algorithm does not work with negative edge weights")
    
    # Initialize distances
    distances = {vertex: float('inf') for vertex in graph.vertices()}
    distances[source] = 0
    
    # Priority queue: (distance, vertex)
    pq = [(0, source)]
    visited = set()
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        # Skip if already visited
        if u in visited:
            continue
        
        visited.add(u)
        
        # Update distances to neighbors
        for v in graph.neighbors(u):
            if v in visited:
                continue
            
            weight = graph.weight(u, v)
            new_dist = current_dist + weight
            
            if new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))
    
    return distances


def dijkstra_with_path(graph: Graph, source: str, target: str) -> tuple:
    """
    Find shortest path and distance from source to target using Dijkstra's algorithm.
    
    Args:
        graph: A weighted graph
        source: The source vertex
        target: The target vertex
        
    Returns:
        A tuple (distance, path) where:
        - distance is the shortest distance from source to target
        - path is a list of vertices in the shortest path
        Returns (float('inf'), []) if no path exists.
    """
    if source not in graph.vertices() or target not in graph.vertices():
        return (float('inf'), [])
    
    if source == target:
        return (0, [source])
    
    # Initialize
    distances = {vertex: float('inf') for vertex in graph.vertices()}
    distances[source] = 0
    previous = {vertex: None for vertex in graph.vertices()}
    
    pq = [(0, source)]
    visited = set()
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if u == target:
            break
        
        if u in visited:
            continue
        
        visited.add(u)
        
        for v in graph.neighbors(u):
            if v in visited:
                continue
            
            weight = graph.weight(u, v)
            new_dist = current_dist + weight
            
            if new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heapq.heappush(pq, (new_dist, v))
    
    # Reconstruct path
    if distances[target] == float('inf'):
        return (float('inf'), [])
    
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return (distances[target], path)


if __name__ == "__main__":
    # Example usage
    print("Dijkstra's Algorithm Example")
    print("-" * 50)
    
    # Create a weighted graph
    g = Graph(directed=False, weighted=True)
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 8)
    g.add_edge("C", "E", 10)
    g.add_edge("D", "E", 2)
    
    print(f"Graph: {g}")
    print()
    
    # Compute all shortest distances from A
    source = "A"
    distances = dijkstra(g, source)
    print(f"Shortest distances from {source}:")
    for vertex, dist in sorted(distances.items()):
        print(f"  {source} -> {vertex}: {dist}")
    print()
    
    # Find shortest path from A to E
    dist, path = dijkstra_with_path(g, "A", "E")
    print(f"Shortest path from A to E:")
    print(f"  Path: {' -> '.join(path)}")
    print(f"  Distance: {dist}")
