## The example by the teacher that shows how the Blue path problem is solved
""" Run this instead of your own function to see how this solution works """

from graph import Graph

def max_blue_path(graph: Graph, s: str, t: str) -> int:
    from collections import deque, defaultdict

    if s not in graph._adjacency or t not in graph._adjacency:
        raise KeyError("Source or target vertex does not exist in graph")
    ## We use the deque as a queue for BFS:
    Q = deque([s])
    d = {s: 0}
    blue_counts = {s: 1 if s in graph.blue else 0}
    ## The BFS loop:
    while Q:
        u = Q.popleft()
        ## Early stopping if we reached t and its done. 
        if u == t:
            break
        for v in graph._adjacency[u]:
            # v is a newly discovered vertex:
            if v not in d:
                d[v] = d[u] + 1
                blue_counts[v] = blue_counts[u] + (1 if v in graph.blue else 0)
                Q.append(v)
            # v was already discovered, check for equal distance case, i.e., u is a predecessor of v:
            elif d[v] == d[u] + 1:
                blue_counts[v] = max(blue_counts[v], blue_counts[u] + (1 if v in graph.blue else 0))

    return blue_counts.get(t, 0)