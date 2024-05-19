import networkx as nx

import fetch_data
import graph

class Pathfinding:
    def __init__(self, graph):
        self.graph = graph

    def find_best_arbitrage(self):
        # Determine the starting node (exchange with the lowest ask price)
        lowest_ask_price = float('inf')
        start_exchange = None

        for node in self.graph.graph.nodes(data=True):
            # Check all edges from each node to find the lowest ask price
            for edge in self.graph.graph.edges(node[0], data=True):
                if edge[2]['from_ask'] < lowest_ask_price:
                    lowest_ask_price = edge[2]['from_ask']
                    start_exchange = node[0]

        # Use Dijkstra's algorithm to find the path with the highest arbitrage potential from the start node
        if start_exchange:
            # Using weight as a cost in Dijkstra's algorithm
            lengths, paths = nx.single_source_dijkstra(self.graph.graph, start_exchange, weight='weight')
            return start_exchange, paths, lengths
        else:
            return None, {}, {}

    def print_paths(self, start_exchange, paths, lengths):
        if start_exchange:
            print(f"Starting Arbitrage at {start_exchange} with lowest ask price\n")
            for destination, path in paths.items():
                if destination != start_exchange:
                    path_description = " -> ".join([f"{node}" for node in path])
                    print(f"Path to {destination}:")
                    print(f"  Route: {path_description}")
                    print(f"  Total weight (cost): {lengths[destination]:.4f}")
                    print(f"  Visualization: {' -> '.join(['(' + node + ')' for node in path])}")
                    print("-" * 50)
        else:
            print("No valid starting exchange found.")
