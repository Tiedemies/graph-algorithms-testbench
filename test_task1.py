#!/usr/bin/env python3
"""
Test script for Task 1: Shortest Paths with Maximal Blue Nodes

DO NOT MODIFY THIS FILE

Usage: python test_task1.py <graph_file> <source> <target>
Example: python test_task1.py data/small_graph.json A E
"""

import sys
from graph import load_graph
from tasks.task1_bfs import max_blue_path


def test_max_blue_path(graph_file, source, target):
    """
    Test max_blue_path algorithm on the provided graph file.
    
    Args:
        graph_file: Path to the graph file to test
        source: Source vertex
        target: Target vertex
    """
    print(f"Testing Task 1: Shortest Paths with Maximal Blue Nodes")
    print(f"Graph file: {graph_file}")
    print(f"Source: {source}, Target: {target}")
    print("-" * 60)
    
    try:
        # Load the graph
        graph = load_graph(graph_file)
        print(f"Loaded graph: {graph}")
        print()
        
        # Check if graph has blue attribute
        if not hasattr(graph, 'blue'):
            print("ERROR: Graph does not have 'blue' attribute")
            print("Adding default blue vertices (empty set for testing)")
            graph.blue = set()
        
        print(f"Blue vertices: {sorted(graph.blue) if graph.blue else 'None'}")
        print()
        
        # Verify source and target exist
        if source not in graph.vertices():
            print(f"ERROR: Source vertex '{source}' not found in graph")
            return False
        
        if target not in graph.vertices():
            print(f"ERROR: Target vertex '{target}' not found in graph")
            return False
        
        # Run the algorithm
        try:
            result = max_blue_path(graph, source, target)
            
            # Validate result
            if not isinstance(result, int):
                print(f"ERROR: Expected int, got {type(result)}")
                return False
            
            if result < 0:
                print(f"ERROR: Result should be non-negative, got {result}")
                return False
            
            # Display result
            print(f"Maximum blue vertices on shortest path: {result}")
            print()
            
            if result == 0:
                print("No blue vertices on any shortest path (or no path exists)")
            else:
                print(f"✓ Found shortest path with {result} blue vertex/vertices")
            
            print()
            print("✓ Test PASSED")
            return True
            
        except KeyError as e:
            print(f"ERROR: KeyError - {e}")
            print("Check that source and target vertices are handled correctly")
            return False
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
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
    if len(sys.argv) != 4:
        print("Usage: python test_task1.py <graph_file> <source> <target>")
        print("Example: python test_task1.py data/small_graph.json A E")
        sys.exit(1)
    
    graph_file = sys.argv[1]
    source = sys.argv[2]
    target = sys.argv[3]
    
    success = test_max_blue_path(graph_file, source, target)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
