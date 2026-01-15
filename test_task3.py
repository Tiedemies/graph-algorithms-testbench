#!/usr/bin/env python3
"""
Test script for Task 3: Algorithm of Choice

DO NOT MODIFY THIS FILE

Usage: 
  For centrality: python test_task3.py -A <graph_file>
  For community:  python test_task3.py -B <graph_file>

Example: python test_task3.py -A data/social_graph.json
"""

import sys
from graph import load_graph
from tasks.task3_choice import ALGORITHM_CHOICE, centralities, communities


def test_centrality(graph, graph_file):
    """Test betweenness centrality algorithm."""
    print(f"Testing: Betweenness Centrality")
    print("-" * 60)
    
    vertices = graph.vertices()
    if not vertices:
        print("ERROR: Graph has no vertices")
        return False
    
    try:
        result = centralities(graph)
        
        # Validate result
        if not isinstance(result, dict):
            print(f"ERROR: Expected dict, got {type(result)}")
            return False
        
        # Check all vertices are included
        vertex_set = set(vertices)
        result_set = set(result.keys())
        
        if result_set != vertex_set:
            missing = vertex_set - result_set
            extra = result_set - vertex_set
            if missing:
                print(f"ERROR: Missing vertices in result: {missing}")
            if extra:
                print(f"ERROR: Extra vertices in result: {extra}")
            return False
        
        # Check all values are non-negative numbers
        for vertex, centrality in result.items():
            if not isinstance(centrality, (int, float)):
                print(f"ERROR: Centrality for {vertex} is not a number: {centrality}")
                return False
            if centrality < 0:
                print(f"ERROR: Centrality for {vertex} is negative: {centrality}")
                return False
        
        # Display results
        print("Betweenness Centrality Results:")
        sorted_vertices = sorted(result.items(), key=lambda x: x[1], reverse=True)
        for vertex, centrality in sorted_vertices:
            print(f"  {vertex}: {centrality:.4f}")
        
        print()
        most_central = sorted_vertices[0]
        print(f"Most central vertex: {most_central[0]} (centrality: {most_central[1]:.4f})")
        
        print()
        print("✓ Centrality test PASSED")
        return True
        
    except NotImplementedError as e:
        print(f"ERROR: {e}")
        return False
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_community_detection(graph, graph_file):
    """Test community detection algorithm."""
    print(f"Testing: Community Detection")
    print("-" * 60)
    
    vertices = graph.vertices()
    if not vertices:
        print("ERROR: Graph has no vertices")
        return False
    
    if graph.directed:
        print("WARNING: Community detection typically works on undirected graphs")
    
    try:
        result = communities(graph)
        
        # Validate result
        if not isinstance(result, (list, tuple)):
            print(f"ERROR: Expected list/tuple of sets, got {type(result)}")
            return False
        
        # Check each community is a set
        all_vertices = set()
        for i, community in enumerate(result):
            if not isinstance(community, (set, frozenset, list, tuple)):
                print(f"ERROR: Community {i} is not iterable: {type(community)}")
                return False
            
            community_set = set(community)
            
            # Check for overlap
            overlap = all_vertices & community_set
            if overlap:
                print(f"ERROR: Communities overlap (vertex {list(overlap)[0]} in multiple communities)")
                return False
            
            all_vertices.update(community_set)
        
        # Check all vertices are assigned
        vertex_set = set(vertices)
        if all_vertices != vertex_set:
            missing = vertex_set - all_vertices
            extra = all_vertices - vertex_set
            if missing:
                print(f"ERROR: Some vertices not assigned to communities: {missing}")
            if extra:
                print(f"ERROR: Unknown vertices in communities: {extra}")
            return False
        
        # Display results
        print(f"Number of Communities: {len(result)}")
        print()
        
        for i, community in enumerate(result, 1):
            community_list = sorted(list(community))
            print(f"Community {i} ({len(community_list)} vertices):")
            print(f"  {', '.join(community_list)}")
        
        # Calculate some basic metrics
        print()
        print("Community Statistics:")
        sizes = [len(c) for c in result]
        print(f"  Average community size: {sum(sizes) / len(sizes):.2f}")
        print(f"  Largest community: {max(sizes)} vertices")
        print(f"  Smallest community: {min(sizes)} vertices")
        
        print()
        print("✓ Community detection test PASSED")
        print("Note: There is no single 'correct' answer for community detection.")
        print("      Your solution will be evaluated on quality metrics (modularity, etc.)")
        return True
        
    except NotImplementedError as e:
        print(f"ERROR: {e}")
        return False
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_algorithm_choice(option, graph_file):
    """
    Test the student's chosen algorithm.
    
    Args:
        option: "-A" for centrality, "-B" for community
        graph_file: Path to the graph file to test
    """
    print(f"Testing Task 3: Algorithm of Choice")
    print(f"Graph file: {graph_file}")
    print(f"Selected algorithm: {ALGORITHM_CHOICE}")
    print(f"Test option: {option}")
    print("=" * 60)
    print()
    
    # Validate option matches choice
    if option == "-A" and ALGORITHM_CHOICE != "centrality":
        print(f"ERROR: Test option is -A (centrality) but ALGORITHM_CHOICE is '{ALGORITHM_CHOICE}'")
        print(f"Please set ALGORITHM_CHOICE = 'centrality' in tasks/task3_choice.py")
        return False
    
    if option == "-B" and ALGORITHM_CHOICE != "community":
        print(f"ERROR: Test option is -B (community) but ALGORITHM_CHOICE is '{ALGORITHM_CHOICE}'")
        print(f"Please set ALGORITHM_CHOICE = 'community' in tasks/task3_choice.py")
        return False
    
    try:
        # Load the graph
        graph = load_graph(graph_file)
        print(f"Loaded graph: {graph}")
        print()
        
        # Test based on option
        if option == "-A":
            return test_centrality(graph, graph_file)
        elif option == "-B":
            return test_community_detection(graph, graph_file)
        else:
            print(f"ERROR: Unknown option: {option}")
            print("Use -A for centrality or -B for community detection")
            return False
            
    except FileNotFoundError:
        print(f"ERROR: Graph file not found: {graph_file}")
        return False
    except Exception as e:
        print(f"ERROR loading graph: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    if len(sys.argv) != 3:
        print("Usage:")
        print("  For centrality: python test_task3.py -A <graph_file>")
        print("  For community:  python test_task3.py -B <graph_file>")
        print()
        print("Examples:")
        print("  python test_task3.py -A data/social_graph.json")
        print("  python test_task3.py -B data/social_graph.json")
        sys.exit(1)
    
    option = sys.argv[1]
    graph_file = sys.argv[2]
    
    if option not in ["-A", "-B"]:
        print(f"ERROR: Invalid option '{option}'")
        print("Use -A for centrality or -B for community detection")
        sys.exit(1)
    
    success = test_algorithm_choice(option, graph_file)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
