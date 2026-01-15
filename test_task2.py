#!/usr/bin/env python3
"""
Test script for Task 2: Minimum Spanning Trees

DO NOT MODIFY THIS FILE

Usage: python test_task2.py <graph_file>
Example: python test_task2.py data/weighted_graph.json
"""

import sys
from graph import load_graph
from tasks.task2_mst import MST, second_best_ST


def test_mst_algorithms(graph_file):
    """
    Test MST and second-best spanning tree algorithms.
    
    Args:
        graph_file: Path to the graph file to test
    """
    print(f"Testing Task 2: Minimum Spanning Trees")
    print(f"Graph file: {graph_file}")
    print("-" * 60)
    
    try:
        # Load the graph
        graph = load_graph(graph_file)
        print(f"Loaded graph: {graph}")
        print()
        
        # Check graph properties
        if graph.directed:
            print("ERROR: MST algorithms require an undirected graph")
            return False
        
        if not graph.weighted:
            print("WARNING: Graph is not weighted, all edges will have weight 1.0")
        
        vertices = graph.vertices()
        edges = graph.edges()
        
        print(f"Vertices: {len(vertices)}")
        print(f"Edges: {len(edges)}")
        print()
        
        # Test MST
        print("=" * 60)
        print("Testing MST()...")
        print("-" * 60)
        
        try:
            mst = MST(graph)
            
            # Validate MST
            if not isinstance(mst, list):
                print(f"ERROR: Expected list, got {type(mst)}")
                return False
            
            # Check number of edges
            expected_edges = len(vertices) - 1 if len(vertices) > 0 else 0
            if len(mst) > expected_edges:
                print(f"ERROR: MST has too many edges: {len(mst)} (expected ≤ {expected_edges})")
                return False
            
            # Display MST
            print(f"MST Edges: {len(mst)}")
            total_weight = 0
            for u, v, weight in mst:
                print(f"  {u} -- {v}: {weight}")
                total_weight += weight
            
            print(f"\nTotal MST Weight: {total_weight}")
            print("✓ MST test PASSED")
            
        except ValueError as e:
            print(f"ERROR: ValueError - {e}")
            return False
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test Second-Best ST
        print()
        print("=" * 60)
        print("Testing second_best_ST()...")
        print("-" * 60)
        
        try:
            second_st = second_best_ST(graph)
            
            if second_st is None:
                print("Result: No second-best spanning tree exists")
                print("(This is valid for graphs with < 3 vertices or limited structure)")
            elif len(second_st) == 0:
                print("Result: No second-best spanning tree exists (empty list)")
            else:
                # Validate second ST
                if not isinstance(second_st, list):
                    print(f"ERROR: Expected list or None, got {type(second_st)}")
                    return False
                
                # Display second-best ST
                print(f"Second-Best ST Edges: {len(second_st)}")
                total_weight_2 = 0
                for u, v, weight in second_st:
                    print(f"  {u} -- {v}: {weight}")
                    total_weight_2 += weight
                
                print(f"\nTotal Second-Best ST Weight: {total_weight_2}")
                
                # Check that it's actually worse than MST
                if total_weight_2 <= total_weight:
                    print(f"WARNING: Second-best ST weight ({total_weight_2}) should be > MST weight ({total_weight})")
                else:
                    print(f"✓ Second-best ST has higher weight than MST ({total_weight_2} > {total_weight})")
            
            print("✓ Second-best ST test PASSED")
            
        except ValueError as e:
            print(f"ERROR: ValueError - {e}")
            return False
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print()
        print("✓ All Task 2 tests PASSED")
        return True
        
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
    if len(sys.argv) != 2:
        print("Usage: python test_task2.py <graph_file>")
        print("Example: python test_task2.py data/weighted_graph.json")
        sys.exit(1)
    
    graph_file = sys.argv[1]
    success = test_mst_algorithms(graph_file)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
