#!/usr/bin/env python3
"""
Test script for Task 2: Minimum Spanning Trees

DO NOT MODIFY THIS FILE

Usage: python test_task2.py [-R] <graph_file>
  -R: Run reference implementation and compare results

Example: python test_task2.py data/weighted_graph.json
         python test_task2.py -R data/weighted_graph.json
"""

import sys
import os
from graph import load_graph
from tasks.task2_mst import MST, second_best_ST


def test_mst_algorithms(graph_file, run_reference=False):
    """
    Test MST and second-best spanning tree algorithms.
    
    Args:
        graph_file: Path to the graph file to test
        run_reference: If True, also run reference implementation and compare
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
            
            # Run reference implementation if requested
            if run_reference:
                print()
                print("Running Reference MST...")
                try:
                    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Reference implementations'))
                    from task2_reference import MST as ref_MST
                    
                    ref_mst = ref_MST(graph)
                    ref_weight = sum(w for _, _, w in ref_mst)
                    print(f"Reference MST Weight: {ref_weight}")
                    
                    # Compare weights (MST weight should be same)
                    if abs(total_weight - ref_weight) < 0.0001:
                        print("✓ MATCH: Your MST weight matches the reference")
                    else:
                        print(f"✗ MISMATCH: Your MST weight ({total_weight}) differs from reference ({ref_weight})")
                        return False
                        
                except ImportError as e:
                    print(f"WARNING: Could not load reference implementation: {e}")
                except Exception as e:
                    print(f"ERROR in reference implementation: {type(e).__name__}: {e}")
            
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
            
            # Run reference implementation if requested
            if run_reference and second_st is not None:
                print()
                print("Running Reference Second-Best ST...")
                try:
                    if 'task2_reference' not in sys.modules:
                        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Reference implementations'))
                        from task2_reference import second_best_ST as ref_second_best_ST
                    else:
                        from task2_reference import second_best_ST as ref_second_best_ST
                    
                    ref_second_st = ref_second_best_ST(graph)
                    if ref_second_st:
                        ref_weight_2 = sum(w for _, _, w in ref_second_st)
                        print(f"Reference Second-Best ST Weight: {ref_weight_2}")
                        
                        # Compare weights
                        if abs(total_weight_2 - ref_weight_2) < 0.0001:
                            print("✓ MATCH: Your second-best ST weight matches the reference")
                        else:
                            print(f"✗ MISMATCH: Your weight ({total_weight_2}) differs from reference ({ref_weight_2})")
                            print("Note: Multiple valid second-best STs may exist with the same weight")
                    else:
                        print("Reference also returned None")
                        
                except ImportError as e:
                    print(f"WARNING: Could not load reference implementation: {e}")
                except Exception as e:
                    print(f"ERROR in reference implementation: {type(e).__name__}: {e}")
            
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
    args = sys.argv[1:]
    
    # Check for -R flag
    run_reference = False
    if args and args[0] == "-R":
        run_reference = True
        args = args[1:]
    
    if len(args) != 1:
        print("Usage: python test_task2.py [-R] <graph_file>")
        print("  -R: Run reference implementation and compare results")
        print()
        print("Example: python test_task2.py data/weighted_graph.json")
        print("         python test_task2.py -R data/weighted_graph.json")
        sys.exit(1)
    
    graph_file = args[0]
    success = test_mst_algorithms(graph_file, run_reference)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
