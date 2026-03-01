"""
# ============================================
# Teacher Reference Implementation - Task 3
# Community Detection (Spectral Clustering)
# ============================================

This is a reference implementation demonstrating spectral clustering
for community detection in graphs.

Spectral clustering uses the eigenvalues and eigenvectors of matrices
(typically the Laplacian matrix) derived from the graph to identify
communities.

The method is based on graph cut theory and provides a principled
approach to partitioning graphs into communities.
"""

from graph import Graph
from typing import List, Set, Dict
import numpy as np


def communities(graph: Graph, num_communities: int = None) -> List[Set[str]]:
    """
    Detect communities in an undirected graph using spectral clustering.
    
    Algorithm Overview:
        1. Construct the graph Laplacian matrix
        2. Compute eigenvalues and eigenvectors
        3. Use k smallest non-zero eigenvectors for embedding
        4. Apply k-means clustering to the embedded points
        5. Map clusters back to vertices
    
    Time Complexity: O(V^3) for eigendecomposition, O(k * V * iterations) for k-means
    Space Complexity: O(V^2) for the Laplacian matrix
    
    Args:
        graph: An undirected graph (directed graphs not supported)
        num_communities: Number of communities to detect. If None, uses heuristic.
        
    Returns:
        A list of sets, where each set contains vertices in one community.
        
    References:
        - Von Luxburg, U. (2007). A tutorial on spectral clustering.
          Statistics and computing, 17(4), 395-416.
        - Ng, A., Jordan, M., & Weiss, Y. (2001). On spectral clustering.
    """
    
    if graph.directed:
        raise ValueError("Spectral clustering requires an undirected graph")
    
    vertices = graph.vertices()
    n = len(vertices)
    
    if n == 0:
        return []
    
    if n == 1:
        return [{vertices[0]}]
    
    # ============================================
    # Step 1: Create vertex index mapping
    # ============================================
    # Map vertex names to indices for matrix operations
    vertex_to_idx = {v: i for i, v in enumerate(vertices)}
    idx_to_vertex = {i: v for v, i in vertex_to_idx.items()}
    
    # ============================================
    # Step 2: Construct the Adjacency Matrix (A)
    # ============================================
    # A[i,j] = 1 if there's an edge between vertex i and vertex j
    # For weighted graphs, A[i,j] = weight of edge
    A = np.zeros((n, n))
    for u in vertices:
        i = vertex_to_idx[u]
        for v in graph.neighbors(u):
            j = vertex_to_idx[v]
            # Use edge weight (or 1 for unweighted graphs)
            weight = graph.weight(u, v) if graph.weighted else 1.0
            A[i, j] = weight
    
    # ============================================
    # Step 3: Construct the Degree Matrix (D)
    # ============================================
    # D is a diagonal matrix where D[i,i] = degree of vertex i
    # (sum of weights of edges incident to vertex i)
    degrees = np.sum(A, axis=1)
    D = np.diag(degrees)
    
    # ============================================
    # Step 4: Construct the Laplacian Matrix (L)
    # ============================================
    # Several variants of Laplacian exist:
    #
    # 1. Unnormalized Laplacian: L = D - A
    #    - Simple but sensitive to graph structure
    #
    # 2. Normalized Symmetric Laplacian: L_sym = D^(-1/2) L D^(-1/2) = I - D^(-1/2) A D^(-1/2)
    #    - Better for graphs with varying degree distributions
    #
    # 3. Random Walk Laplacian: L_rw = D^(-1) L = I - D^(-1) A
    #    - Interpretable as random walk transition matrix
    #
    # We use the normalized symmetric Laplacian (option 2) as it's
    # generally more robust and theoretically well-founded.
    
    # Compute D^(-1/2), handling zero degrees
    D_inv_sqrt = np.zeros((n, n))
    for i in range(n):
        if degrees[i] > 0:
            D_inv_sqrt[i, i] = 1.0 / np.sqrt(degrees[i])
    
    # L_sym = I - D^(-1/2) A D^(-1/2)
    L_sym = np.eye(n) - D_inv_sqrt @ A @ D_inv_sqrt
    
    # ============================================
    # Step 5: Compute Eigenvalues and Eigenvectors
    # ============================================
    # We need the k smallest eigenvalues and their corresponding eigenvectors
    # The smallest eigenvalue is always 0 (with eigenvector of all 1s)
    # For k communities, we use eigenvectors corresponding to k smallest eigenvalues
    
    eigenvalues, eigenvectors = np.linalg.eigh(L_sym)
    
    # Sort by eigenvalue (should already be sorted, but ensure it)
    idx_sorted = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx_sorted]
    eigenvectors = eigenvectors[:, idx_sorted]
    
    # ============================================
    # Step 6: Determine Number of Communities
    # ============================================
    if num_communities is None:
        # Heuristic: Use the eigengap to estimate k
        # The eigengap is the difference between consecutive eigenvalues
        # A large eigengap suggests a natural number of clusters
        num_communities = _estimate_num_communities(eigenvalues, n)
    
    # Ensure num_communities is valid
    num_communities = max(1, min(num_communities, n))
    
    # ============================================
    # Step 7: Extract k smallest eigenvectors
    # ============================================
    # Take the first k eigenvectors (corresponding to k smallest eigenvalues)
    # This gives us a k-dimensional embedding of the graph vertices
    k = num_communities
    U = eigenvectors[:, :k]
    
    # ============================================
    # Step 8: Normalize rows (optional but recommended)
    # ============================================
    # Normalize each row of U to have unit length
    # This puts all points on the unit sphere, which helps k-means
    row_norms = np.linalg.norm(U, axis=1, keepdims=True)
    row_norms[row_norms == 0] = 1  # Avoid division by zero
    U_normalized = U / row_norms
    
    # ============================================
    # Step 9: Apply k-means clustering
    # ============================================
    # Cluster the rows of U_normalized using k-means
    # Each row represents a vertex in the k-dimensional spectral space
    labels = _kmeans_clustering(U_normalized, k)
    
    # ============================================
    # Step 10: Map clusters back to vertices
    # ============================================
    communities_list = [set() for _ in range(k)]
    for i, label in enumerate(labels):
        vertex = idx_to_vertex[i]
        communities_list[label].add(vertex)
    
    # Remove empty communities (shouldn't happen, but be safe)
    communities_list = [c for c in communities_list if len(c) > 0]
    
    return communities_list


def _estimate_num_communities(eigenvalues: np.ndarray, max_k: int) -> int:
    """
    Estimate the number of communities using the eigengap heuristic.
    
    The eigengap is the difference between consecutive eigenvalues.
    A large eigengap suggests a natural partition of the graph.
    
    Args:
        eigenvalues: Sorted array of eigenvalues from the Laplacian matrix
        max_k: Maximum number of communities to consider
        
    Returns:
        Estimated number of communities
    """
    # Look at eigenvalues up to max_k (or sqrt(n) as a heuristic)
    n = len(eigenvalues)
    search_limit = min(max_k or int(np.sqrt(n)) + 1, n - 1)
    
    if search_limit < 2:
        return 2  # Default to 2 communities
    
    # Find the largest eigengap
    eigengaps = np.diff(eigenvalues[:search_limit + 1])
    
    # The optimal k is where the largest gap occurs
    # Add 1 because we're looking at gaps, not eigenvalues
    optimal_k = np.argmax(eigengaps) + 1
    
    # Ensure at least 1 community
    return max(1, optimal_k)


def _kmeans_clustering(X: np.ndarray, k: int, max_iterations: int = 100, 
                       n_init: int = 10) -> np.ndarray:
    """
    Perform k-means clustering on the data matrix X.
    
    This is a simple implementation of Lloyd's algorithm for k-means.
    For production use, consider using sklearn.cluster.KMeans.
    
    Args:
        X: Data matrix (n_samples x n_features)
        k: Number of clusters
        max_iterations: Maximum number of iterations
        n_init: Number of times to run k-means with different initializations
        
    Returns:
        Array of cluster labels (integers 0 to k-1)
    """
    n_samples = X.shape[0]
    
    if k >= n_samples:
        # Each point is its own cluster
        return np.arange(n_samples)
    
    best_labels = None
    best_inertia = float('inf')
    
    # Run k-means multiple times with different initializations
    # and keep the best result (lowest inertia)
    for _ in range(n_init):
        # ============================================
        # Initialize: Random selection of centroids
        # ============================================
        # Use k-means++ initialization for better results
        centroids = _kmeans_plusplus_init(X, k)
        
        labels = np.zeros(n_samples, dtype=int)
        
        # ============================================
        # Lloyd's Algorithm: Iterate until convergence
        # ============================================
        for iteration in range(max_iterations):
            # E-step: Assign each point to nearest centroid
            distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
            new_labels = np.argmin(distances, axis=1)
            
            # Check for convergence
            if np.array_equal(labels, new_labels):
                break
            
            labels = new_labels
            
            # M-step: Update centroids as mean of assigned points
            for j in range(k):
                cluster_points = X[labels == j]
                if len(cluster_points) > 0:
                    centroids[j] = cluster_points.mean(axis=0)
        
        # Compute inertia (sum of squared distances to centroids)
        inertia = 0
        for j in range(k):
            cluster_points = X[labels == j]
            if len(cluster_points) > 0:
                inertia += np.sum((cluster_points - centroids[j]) ** 2)
        
        # Keep best result
        if inertia < best_inertia:
            best_inertia = inertia
            best_labels = labels
    
    return best_labels


def _kmeans_plusplus_init(X: np.ndarray, k: int) -> np.ndarray:
    """
    Initialize k-means centroids using the k-means++ algorithm.
    
    k-means++ selects initial centroids that are far apart, which
    leads to better and more consistent clustering results.
    
    Args:
        X: Data matrix (n_samples x n_features)
        k: Number of clusters
        
    Returns:
        Initial centroids (k x n_features)
    """
    n_samples, n_features = X.shape
    centroids = np.zeros((k, n_features))
    
    # Choose first centroid uniformly at random
    centroids[0] = X[np.random.randint(n_samples)]
    
    # Choose remaining centroids
    for i in range(1, k):
        # Compute distance from each point to nearest existing centroid
        distances = np.min(np.linalg.norm(X[:, np.newaxis] - centroids[:i], axis=2), axis=1)
        
        # Square the distances (D(x)^2 weighting)
        distances_squared = distances ** 2
        
        # Choose next centroid with probability proportional to D(x)^2
        probabilities = distances_squared / distances_squared.sum()
        cumulative_probs = np.cumsum(probabilities)
        r = np.random.random()
        next_centroid_idx = np.searchsorted(cumulative_probs, r)
        centroids[i] = X[next_centroid_idx]
    
    return centroids


# ============================================
# Utility Functions
# ============================================

def compute_modularity(graph: Graph, communities_list: List[Set[str]]) -> float:
    """
    Compute the modularity of a community partition.
    
    Modularity measures the quality of a network partition by comparing
    the actual number of edges within communities to the expected number
    in a random graph with the same degree distribution.
    
    Q = (1/2m) * sum_ij [A_ij - (k_i * k_j)/(2m)] * delta(c_i, c_j)
    
    where:
    - m = total number of edges
    - A_ij = adjacency matrix
    - k_i = degree of vertex i
    - delta(c_i, c_j) = 1 if i and j are in same community, 0 otherwise
    
    Args:
        graph: The graph
        communities_list: List of communities (sets of vertices)
        
    Returns:
        Modularity value (typically between -0.5 and 1.0)
        Higher values indicate better community structure
    """
    # Create community membership mapping
    vertex_to_community = {}
    for comm_id, community in enumerate(communities_list):
        for vertex in community:
            vertex_to_community[vertex] = comm_id
    
    # Compute total number of edges (2m for undirected graphs)
    edges = graph.edges()
    m = len(edges)
    
    if m == 0:
        return 0.0
    
    two_m = 2 * m
    
    # Compute degrees
    degrees = {}
    for v in graph.vertices():
        degrees[v] = len(graph.neighbors(v))
    
    # Compute modularity
    modularity = 0.0
    for u in graph.vertices():
        for v in graph.vertices():
            # Check if in same community
            if vertex_to_community.get(u) == vertex_to_community.get(v):
                # Actual edges
                A_uv = 1 if graph.has_edge(u, v) else 0
                
                # Expected edges under null model
                expected = (degrees[u] * degrees[v]) / two_m
                
                modularity += A_uv - expected
    
    modularity /= two_m
    
    return modularity


# ============================================
# Example Usage (for demonstration)
# ============================================
if __name__ == "__main__":
    # Create a simple graph with two obvious communities
    g = Graph(directed=False)
    
    # Community 1: a-b-c forming a triangle
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("c", "a")
    
    # Community 2: x-y-z forming a triangle
    g.add_edge("x", "y")
    g.add_edge("y", "z")
    g.add_edge("z", "x")
    
    # Bridge: weak connection between communities
    g.add_edge("c", "x")
    
    # Detect communities
    communities_list = communities(g, num_communities=2)
    
    print(f"Found {len(communities_list)} communities:")
    for i, community in enumerate(communities_list, 1):
        print(f"  Community {i}: {sorted(community)}")
    
    # Compute modularity
    mod = compute_modularity(g, communities_list)
    print(f"\nModularity: {mod:.3f}")
