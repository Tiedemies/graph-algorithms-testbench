"""
# ============================================
# STUDENT IMPLEMENTATION FILE - TASK 2
# You may edit this file.
# Do NOT modify function signatures.
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
        
    Note:
        If the graph is disconnected, returns a minimum spanning forest.
        You may use Kruskal's, Prim's, or any other MST algorithm.
    """
    # TODO: Implement MST algorithm (Kruskal's recommended)
    # Hint: Sort edges by weight, use Union-Find to detect cycles
    pass


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
        One approach is to:
        1. Find the MST
        2. For each edge NOT in MST, try adding it (creates a cycle)
        3. Remove the heaviest edge in that cycle (other than the added edge)
        4. This gives a candidate spanning tree
        5. Return the candidate with minimum weight
    """
    # TODO: Implement second-best spanning tree algorithm
    pass


# ============================================
# OPTIONAL: Union-Find Helper Class
# You may implement Union-Find here or import from examples/
# ============================================

class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure.
    
    Optional helper for Kruskal's algorithm.
    You may implement this or use the example from examples/union_find_example.py
    """
    
    def __init__(self, vertices: List[str]):
        """Initialize Union-Find structure with given vertices."""
        # TODO: Implement initialization
        pass
    
    def find(self, x: str) -> str:
        """Find the root/representative of the set containing x."""
        # TODO: Implement find with path compression
        pass
    
    def union(self, x: str, y: str) -> bool:
        """
        Unite the sets containing x and y.
        
        Returns:
            True if x and y were in different sets (union performed)
            False if x and y were already in the same set
        """
        # TODO: Implement union with rank
        pass
