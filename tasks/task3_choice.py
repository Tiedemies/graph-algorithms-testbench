"""
# ============================================
# STUDENT IMPLEMENTATION FILE - TASK 3
# You may edit this file.
# Do NOT modify function signatures.
# ============================================

TASK 3: Algorithm of Your Choice

Choose ONE of the following algorithms to implement:

Option A: Betweenness Centrality
Option B: Community Detection

Indicate your choice by setting the ALGORITHM_CHOICE variable below.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from graph import Graph
from typing import Dict, Set, List

# ============================================
# SET YOUR CHOICE HERE (required)
# Valid values: "centrality", "community"
# ============================================
ALGORITHM_CHOICE = "centrality"  # TODO: Change this to your choice


# ============================================
# Option A: Betweenness Centrality
# ============================================

def centralities(graph: Graph) -> Dict[str, float]:
    """
    Compute betweenness centrality for all vertices in the graph.
    
    Betweenness centrality of a vertex v is the sum over all pairs (s,t) of
    the fraction of shortest paths from s to t that pass through v.
    
    Args:
        graph: An unweighted graph (may be directed or undirected)
        
    Returns:
        A dictionary mapping each vertex to its betweenness centrality value.
        
    Note:
        Only implement this if ALGORITHM_CHOICE = "centrality"
        
    Algorithm hint:
        - For each vertex s, run BFS to find all shortest paths from s
        - Track how many shortest paths pass through each vertex
        - Brandes' algorithm is efficient for this
    """
    if ALGORITHM_CHOICE != "centrality":
        raise NotImplementedError(f"This function is not implemented. Current choice: {ALGORITHM_CHOICE}")
    
    # TODO: Implement betweenness centrality
    # Hint: Use Brandes' algorithm or all-pairs shortest paths
    pass


# ============================================
# Option B: Community Detection
# ============================================

def communities(graph: Graph) -> List[Set[str]]:
    """
    Detect communities in the graph.
    
    A community is a set of vertices that are more densely connected to each
    other than to the rest of the graph.
    
    Args:
        graph: An undirected graph
        
    Returns:
        A list of sets, where each set contains vertices in one community.
        Each vertex should belong to exactly one community.
        
    Note:
        Only implement this if ALGORITHM_CHOICE = "community"
        There is no single "correct" answer - different algorithms may find
        different communities. You will be evaluated on the quality of
        communities found (measured by modularity or overlap with other methods).
        
    Algorithm options:
        - Girvan-Newman (edge betweenness)
        - Louvain method
        - Label propagation
        - Spectral clustering
    """
    if ALGORITHM_CHOICE != "community":
        raise NotImplementedError(f"This function is not implemented. Current choice: {ALGORITHM_CHOICE}")
    
    # TODO: Implement community detection
    # Hint: Girvan-Newman is conceptually simple - iteratively remove edges
    # with highest betweenness until communities emerge
    pass
