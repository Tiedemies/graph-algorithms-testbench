"""
Example: Depth-First Search (DFS)

This is a reference implementation for educational purposes.
Students should read this to understand how to use the Graph API.

DO NOT COPY THIS CODE DIRECTLY INTO YOUR ASSIGNMENTS.
"""

from graph import Graph


def dfs_traversal(graph: Graph, start: str) -> list:
    """
    Perform a depth-first search traversal starting from a given vertex.
    
    Args:
        graph: The graph to traverse
        start: The starting vertex
        
    Returns:
        A list of vertices in the order they were visited
    """
    if start not in graph.vertices():
        raise KeyError(f"Start vertex {start} not found in graph")
    
    visited = set()
    traversal_order = []
    
    def dfs_recursive(vertex):
        """Helper function for recursive DFS."""
        visited.add(vertex)
        traversal_order.append(vertex)
        
        for neighbor in graph.neighbors(vertex):
            if neighbor not in visited:
                dfs_recursive(neighbor)
    
    dfs_recursive(start)
    return traversal_order


def dfs_iterative(graph: Graph, start: str) -> list:
    """
    Perform DFS using an explicit stack (iterative approach).
    
    Args:
        graph: The graph to traverse
        start: The starting vertex
        
    Returns:
        A list of vertices in the order they were visited
    """
    if start not in graph.vertices():
        raise KeyError(f"Start vertex {start} not found in graph")
    
    visited = set()
    stack = [start]
    traversal_order = []
    
    while stack:
        vertex = stack.pop()
        
        if vertex not in visited:
            visited.add(vertex)
            traversal_order.append(vertex)
            
            # Add neighbors to stack in reverse order
            # (to maintain similar order to recursive version)
            neighbors = graph.neighbors(vertex)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return traversal_order


def has_path_dfs(graph: Graph, start: str, goal: str) -> bool:
    """
    Check if a path exists between two vertices using DFS.
    
    Args:
        graph: The graph to search
        start: The starting vertex
        goal: The goal vertex
        
    Returns:
        True if a path exists, False otherwise
    """
    if start not in graph.vertices() or goal not in graph.vertices():
        return False
    
    if start == goal:
        return True
    
    visited = set()
    
    def dfs_search(vertex):
        if vertex == goal:
            return True
        
        visited.add(vertex)
        
        for neighbor in graph.neighbors(vertex):
            if neighbor not in visited:
                if dfs_search(neighbor):
                    return True
        
        return False
    
    return dfs_search(start)


if __name__ == "__main__":
    # Example usage
    print("DFS Example")
    print("-" * 50)
    
    # Create a simple graph
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "E")
    g.add_edge("D", "F")
    
    print(f"Graph: {g}")
    print()
    
    # DFS traversal (recursive)
    print("DFS Traversal (Recursive) from A:")
    order = dfs_traversal(g, "A")
    print(" -> ".join(order))
    print()
    
    # DFS traversal (iterative)
    print("DFS Traversal (Iterative) from A:")
    order = dfs_iterative(g, "A")
    print(" -> ".join(order))
    print()
    
    # Path checking
    print("Path exists from A to F?", has_path_dfs(g, "A", "F"))
    print("Path exists from A to Z?", has_path_dfs(g, "A", "Z"))
