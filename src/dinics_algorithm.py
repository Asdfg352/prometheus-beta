from collections import defaultdict, deque

def dinics_max_flow(graph, source, sink):
    """
    Implement Dinic's algorithm for maximum flow.
    
    Args:
    graph (dict): Adjacency list representation of the graph 
                  where keys are nodes and values are dictionaries 
                  of {destination: capacity} mappings
    source (int/str): Source node 
    sink (int/str): Sink node
    
    Returns:
    int: Maximum flow from source to sink
    """
    # Special case for identical source and sink
    if source == sink:
        return 0
    
    # Validate source and sink exist in graph originally
    if source not in graph or sink not in graph:
        raise ValueError("Source or sink not in graph")
    
    # Create a deep copy of the graph with explicit source and sink nodes
    residual_graph = defaultdict(dict)
    
    # Copy all destinations from the original graph
    for node, edges in graph.items():
        for dest, capacity in edges.items():
            # Skip self-loops
            if node != dest:
                residual_graph[node][dest] = capacity
                # Ensure reverse edges exist
                if dest not in residual_graph:
                    residual_graph[dest] = {}
                if node not in residual_graph[dest]:
                    residual_graph[dest][node] = 0
    
    def bfs_level_graph():
        """Build level graph using BFS"""
        level = {node: -1 for node in residual_graph}
        level[source] = 0
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            for neighbor, capacity in residual_graph[current].items():
                if level[neighbor] == -1 and capacity > 0:
                    level[neighbor] = level[current] + 1
                    queue.append(neighbor)
        
        return level
    
    def dfs_blocking_flow(node, flow_limit):
        """Find blocking flow using DFS"""
        if node == sink:
            return flow_limit
        
        for neighbor, capacity in list(residual_graph[node].items()):
            # Check if neighbor is reachable in level graph and has remaining capacity
            if level.get(neighbor, -2) == level[node] + 1 and capacity > 0:
                # Try to push flow
                bottleneck = dfs_blocking_flow(neighbor, min(flow_limit, capacity))
                
                if bottleneck > 0:
                    # Update residual graph
                    residual_graph[node][neighbor] -= bottleneck
                    residual_graph[neighbor][node] += bottleneck
                    return bottleneck
        
        return 0
    
    # Initialize max flow
    max_flow = 0
    
    # Repeat until no augmenting path exists
    while True:
        # Build level graph using BFS
        level = bfs_level_graph()
        
        # If sink is not reachable, we're done
        if level[sink] == -1:
            break
        
        # Find and push blocking flows
        while True:
            path_flow = dfs_blocking_flow(source, float('inf'))
            if path_flow == 0:
                break
            max_flow += path_flow
    
    return max_flow