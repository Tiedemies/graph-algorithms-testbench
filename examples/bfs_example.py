"""
Example: Breadth-First Search (BFS)

This is a reference implementation for educational purposes.
Students should read this to understand how to use the Graph API.

DO NOT COPY THIS CODE DIRECTLY INTO YOUR ASSIGNMENTS.
"""

from graph import Graph
from collections import deque


def bfs_traversal(graph: Graph, start: str) -> list:
    """
    Perform a breadth-first search traversal starting from a given vertex.
    
    Args:
        graph: The graph to traverse
        start: The starting vertex
        
    Returns:
        A list of vertices in the order they were visited
    """
    # Check if start vertex exists
    if start not in graph.vertices():
        raise KeyError(f"Start vertex {start} not found in graph")
    
    visited = set()
    queue = deque([start])
    traversal_order = []
    
    visited.add(start)
    
    while queue:
        # Dequeue a vertex
        vertex = queue.popleft()
        traversal_order.append(vertex)
        
        # Enqueue all unvisited neighbors
        for neighbor in graph.neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return traversal_order


def bfs_shortest_path(graph: Graph, start: str, goal: str) -> list:
    """
    Find the shortest path between two vertices using BFS.
    
    Args:
        graph: The graph to search
        start: The starting vertex
        goal: The goal vertex
        
    Returns:
        A list representing the path from start to goal.
        Returns empty list if no path exists.
    """
    if start not in graph.vertices() or goal not in graph.vertices():
        return []
    
    if start == goal:
        return [start]
    
    visited = set()
    queue = deque([(start, [start])])
    visited.add(start)
    
    while queue:
        vertex, path = queue.popleft()
        
        for neighbor in graph.neighbors(vertex):
            if neighbor == goal:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []


if __name__ == "__main__":
    # Example usage
    print("BFS Example")
    print("-" * 50)
    
    # Create a simple graph
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    g.add_edge("D", "E")
    
    print(f"Graph: {g}")
    print()
    
    # BFS traversal
    print("BFS Traversal from A:")
    order = bfs_traversal(g, "A")
    print(" -> ".join(order))
    print()
    
    # Shortest path
    print("Shortest path from A to E:")
    path = bfs_shortest_path(g, "A", "E")
    print(" -> ".join(path))
