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
        One MST algorithm works as follows:
        1. Find the MST
        2. For each edge NOT in MST, try adding it (creates a cycle)
        3. Remove the heaviest edge in that cycle (other than the added edge)
        4. This gives a candidate spanning tree.
        5. Return the candidate with minimum weight.

        NOTE: This is just a hint, you may implement it differently.
        NOTE: Naive implementations may be too slow for large graphs.
    """
    # TODO: Implement second-best spanning tree algorithm
    pass
