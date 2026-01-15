"""
Example: Union-Find (Disjoint Set Union) Data Structure

This is a reference implementation for educational purposes.
Students may use this implementation in their assignments.

Union-Find is commonly used for:
- Kruskal's MST algorithm 
- Finding connected components
- Dynamic connectivity problems
"""


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure.
    
    Supports two main operations:
    - find(x): Find which set x belongs to
    - union(x, y): Merge the sets containing x and y
    
    Uses two optimizations:
    - Path compression: Make trees flat during find()
    - Union by rank: Attach smaller tree under larger tree
    
    Time complexity: O(α(n)) per operation, where α is inverse Ackermann function
    (effectively constant time for practical purposes)
    """
    
    def __init__(self, elements):
        """
        Initialize Union-Find structure.
        
        Args:
            elements: A list or iterable of elemets 
        """
        # Each element starts as its own parent (its own set)
        self.parent = {elem: elem for elem in elements}
        
        # Rank is used for union by rank optimization
        # Initially all ranks are 0
        self.rank = {elem: 0 for elem in elements}
        
        # Optional: track size of each set
        self.size = {elem: 1 for elem in elements}
    
    def make_set(self, x):
        """
        Create a new set with a single element x.
        
        Args:
            x: Element to add
            
        Raises:
            ValueError: If x already exists in the structure
        """
        if x in self.parent:
            raise ValueError(f"Element {x} already exists in Union-Find structure")
        
        self.parent[x] = x
        self.rank[x] = 0
        self.size[x] = 1
    
    def find(self, x):
        """
        Find the root/representative of the set containing x.
        
        Uses path compression: all nodes on the path to root
        are made to point directly to the root.
        
        Args:
            x: Element to find
            
        Returns:
            The root/representative of x's set
        """
        if x not in self.parent:
            raise KeyError(f"Element {x} not in Union-Find structure")
        
        # Path compression: recursively find root and update parent
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        
        return self.parent[x]
    
    def union(self, x, y):
        """
        Unite the sets containing x and y.
        
        Uses union by rank: attach the tree with smaller rank
        under the tree with larger rank.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if x and y were in different sets (union performed)
            False if x and y were already in the same set
        """
        # Find roots of both elements
        root_x = self.find(x)
        root_y = self.find(y)
        
        # Already in same set
        if root_x == root_y:
            return False
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            # Attach x's tree under y's tree
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            # Attach y's tree under x's tree
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            # Same rank: attach y under x and increment x's rank
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            self.size[root_x] += self.size[root_y]
        
        return True
    
    def connected(self, x, y):
        """
        Check if x and y are in the same set.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if x and y are in the same set
        """
        return self.find(x) == self.find(y)
    
    def get_size(self, x):
        """
        Get the size of the set containing x.
        
        Args:
            x: Element to query
            
        Returns:
            The number of elements in x's set
        """
        root = self.find(x)
        return self.size[root]
    
    def num_sets(self):
        """
        Count the number of disjoint sets.
        
        Returns:
            The number of distinct sets
        """
        roots = set()
        for elem in self.parent:
            roots.add(self.find(elem))
        return len(roots)


if __name__ == "__main__":
    # Example usage
    print("Union-Find Example")
    print("-" * 50)
    
    # Create Union-Find with elements A through G
    elements = ["A", "B", "C", "D", "E", "F", "G"]
    uf = UnionFind(elements)
    
    print(f"Initial sets: {uf.num_sets()} (each element is its own set)")
    print()
    
    # Perform some unions
    print("Performing unions:")
    uf.union("A", "B")
    print("  Union(A, B)")
    
    uf.union("C", "D")
    print("  Union(C, D)")
    
    uf.union("E", "F")
    print("  Union(E, F)")
    
    uf.union("A", "C")
    print("  Union(A, C)")
    
    print(f"\nNumber of sets: {uf.num_sets()}")
    print()
    
    # Test connectivity
    print("Connectivity tests:")
    print(f"  A and D connected? {uf.connected('A', 'D')}")
    print(f"  A and E connected? {uf.connected('A', 'E')}")
    print(f"  E and F connected? {uf.connected('E', 'F')}")
    print()
    
    # Show set sizes
    print("Set sizes:")
    for elem in elements:
        root = uf.find(elem)
        if elem == root:  # Only print once per set
            print(f"  Set containing {elem}: {uf.get_size(elem)} elements")
