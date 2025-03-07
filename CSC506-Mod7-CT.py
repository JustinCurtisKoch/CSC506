# CSC506 Module 7 Critical Thinking.
# Algorithms: Dijkstra's Algorithm.

# Importing necessary libraries
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Define the Dijsktra's algorithm function
def dijkstra(graph, start):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # Initialize queue with start node having a distance of 0
    
    # Initialize shortest distance dictionary with infinite values except for the start node
    shortest_distances = {node: float('inf') for node in graph}
    shortest_distances[start] = 0
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)  # Retrieve node with shortest known distance
        
        # If the retrieved distance is greater than the recorded shortest distance, skip processing
        if current_distance > shortest_distances[current_node]:
            continue
        
        # Iterate through the neighbors of the current node
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight  # Calculate the new potential shortest distance
            
            # If the newly calculated distance is shorter, update and push to the queue
            if distance < shortest_distances[neighbor]:
                shortest_distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return shortest_distances

# Define function to visualize the graph
def visualize_graph(graph):
    G = nx.Graph()
    
    # Add edges to the graph from the dictionary representation
    for node, edges in graph.items():
        for neighbor, weight in edges:
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)  # Generate positions for visualization
    labels = nx.get_edge_attributes(G, 'weight')  # Retrieve edge labels (weights)
    
    # Draw nodes and edges with labels
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # Display weights on edges
    
    plt.show()

# Sample graph
graph = {
    'A': [('B', 4), ('C', 1)],
    'B': [('A', 4), ('C', 2), ('D', 5)],
    'C': [('A', 1), ('B', 2), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2), ('A', 11)]
}


start_node = 'C'  # Define the starting node
shortest_paths = dijkstra(graph, start_node)  # Compute shortest paths from the start node
print("Shortest paths from", start_node, ":", shortest_paths)
visualize_graph(graph)

