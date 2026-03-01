"""
# ============================================
# Teacher Reference Implementation - Task 3
# Betweenness Centrality (Brandes Algorithm)
# ============================================

This is a reference implementation demonstrating Brandes' algorithm
for efficiently computing betweenness centrality for all vertices.

Betweenness centrality measures the extent to which a vertex lies on
paths between other vertices. It's useful for identifying "bridge" nodes
in networks.
"""

from graph import Graph
from typing import Dict, List, Set
from collections import deque, defaultdict


def centralities(graph: Graph) -> Dict[str, float]:
    """
    Compute betweenness centrality for all vertices using Brandes' algorithm.
    
    The algorithm is based on:
    Brandes, U. (2001). A faster algorithm for betweenness centrality.
    Journal of Mathematical Sociology, 25(2), 163-177.
    
    Time Complexity: O(V * E) for unweighted graphs, O(V * E + V^2 * log V) for weighted
    Space Complexity: O(V + E)
    
    Args:
        graph: An unweighted graph (may be directed or undirected)
        
    Returns:
        A dictionary mapping each vertex to its betweenness centrality value.
        
    Algorithm Overview:
        For each vertex s:
        1. Forward Phase (BFS): Find all shortest paths from s
           - Track distance to each vertex
           - Track number of shortest paths to each vertex
           - Track predecessors on shortest paths
        2. Backward Phase (Accumulation): Compute dependencies
           - Process vertices in non-increasing distance order
           - Accumulate contribution to betweenness centrality
    """
    
    # Initialize betweenness centrality to 0 for all vertices
    CB = {v: 0.0 for v in graph.vertices()}
    
    # ============================================
    # Main Loop: Process each vertex as a source
    # ============================================
    for s in graph.vertices():
        # ============================================
        # FORWARD PHASE: Single-Source Shortest Paths
        # ============================================
        # We use BFS to find shortest paths from source s
        
        # S: Stack to store vertices in order of non-increasing distance from s
        # This will be used in the backward phase
        S = []
        
        # P: Dictionary of predecessors on shortest paths
        # P[w] contains all vertices v such that there's a shortest path s -> ... -> v -> w
        P = defaultdict(list)
        
        # sigma: Number of shortest paths from s to each vertex
        # sigma[s] = 1 (one path from s to itself: the empty path)
        sigma = defaultdict(int)
        sigma[s] = 1
        
        # d: Distance from s to each vertex (-1 means infinity/unvisited)
        d = {v: -1 for v in graph.vertices()}
        d[s] = 0
        
        # Q: Queue for BFS traversal
        Q = deque([s])
        
        # ============================================
        # BFS: Discover shortest paths from s
        # ============================================
        while Q:
            v = Q.popleft()
            # Add v to stack for later backward traversal
            S.append(v)
            
            # Explore all neighbors of v
            for w in graph.neighbors(v):
                # ============================================
                # Case 1: w found for the first time
                # ============================================
                if d[w] < 0:  # w has not been visited yet
                    Q.append(w)
                    d[w] = d[v] + 1
                
                # ============================================
                # Case 2: Shortest path to w via v?
                # ============================================
                if d[w] == d[v] + 1:
                    # This means v is a predecessor of w on a shortest path
                    sigma[w] += sigma[v]  # Add number of shortest paths through v
                    P[w].append(v)  # v is a predecessor of w
        
        # ============================================
        # BACKWARD PHASE: Accumulation of Dependencies
        # ============================================
        # delta[v] represents the "pair-dependency" of s on v
        # It measures how much betweenness credit v gets from paths starting at s
        delta = {v: 0.0 for v in graph.vertices()}
        
        # Process vertices in order of non-increasing distance from s
        # (This is why we stored them in stack S during BFS)
        while S:
            w = S.pop()
            
            # For each predecessor v of w on shortest paths from s
            for v in P[w]:
                # ============================================
                # Key Formula: Dependency Accumulation
                # ============================================
                # The pair-dependency formula:
                # delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                #
                # Intuition:
                # - sigma[v] / sigma[w]: Fraction of shortest s-w paths that go through v
                # - (1 + delta[w]): Credit for s-w pair plus credit w gets from pairs beyond w
                # - This credit is back-propagated to v in proportion to path counts
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            
            # ============================================
            # Update Betweenness Centrality
            # ============================================
            # Add the dependency to the betweenness centrality
            # (but not for the source vertex s itself)
            if w != s:
                CB[w] += delta[w]
    
    # ============================================
    # Normalization (optional, but conventional)
    # ============================================
    # For undirected graphs, each shortest path is counted twice
    # (once from each direction), so we divide by 2
    if not graph.directed:
        for v in CB:
            CB[v] /= 2.0
    
    # Note: Further normalization by (n-1)(n-2) is sometimes applied
    # to make values comparable across different graph sizes, but
    # we return the raw betweenness centrality values here.
    
    return CB


# ============================================
# Additional Utilities (for testing/debugging)
# ============================================

def top_k_central_vertices(centrality: Dict[str, float], k: int) -> List[tuple]:
    """
    Get the k vertices with highest betweenness centrality.
    
    Args:
        centrality: Dictionary mapping vertices to centrality values
        k: Number of top vertices to return
        
    Returns:
        List of (vertex, centrality) tuples in descending order
    """
    sorted_vertices = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    return sorted_vertices[:k]


def normalize_centrality(centrality: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize centrality values to [0, 1] range.
    
    This normalization divides by the maximum possible betweenness centrality
    in a graph with n vertices: (n-1)(n-2)/2 for undirected, (n-1)(n-2) for directed.
    
    Args:
        centrality: Dictionary mapping vertices to centrality values
        
    Returns:
        Dictionary with normalized centrality values
    """
    n = len(centrality)
    if n <= 2:
        return {v: 0.0 for v in centrality}
    
    # Maximum possible betweenness in a graph with n vertices
    # For undirected: (n-1)(n-2)/2 (each vertex could be on all shortest paths)
    # For directed: (n-1)(n-2)
    # Note: This assumes undirected; adjust if needed
    max_centrality = (n - 1) * (n - 2) / 2
    
    return {v: c / max_centrality for v, c in centrality.items()}


# ============================================
# Example Usage (for demonstration)
# ============================================
if __name__ == "__main__":
    # Create a simple example graph
    g = Graph(directed=False)
    
    # Star graph: center connected to 4 outer vertices
    # The center should have highest betweenness
    g.add_edge("center", "a")
    g.add_edge("center", "b")
    g.add_edge("center", "c")
    g.add_edge("center", "d")
    g.add_edge("a", "b")  # Add one more edge
    
    centrality = centralities(g)
    
    print("Betweenness Centrality:")
    for vertex, value in sorted(centrality.items(), key=lambda x: x[1], reverse=True):
        print(f"  {vertex}: {value:.2f}")
    
    print("\nTop 3 most central vertices:")
    for vertex, value in top_k_central_vertices(centrality, 3):
        print(f"  {vertex}: {value:.2f}")
