import networkx as nx

import graph

class Pathfinding:
    def __init__(self, graph):
        self.graph = graph

    def find_best_arbitrage(self):
        # Determine the starting node (exchange with the lowest ask price)
        lowest_ask_price = float('inf')
        start_exchange = 'kraken/BTC/USD'

        if start_exchange:
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
                    print(f"  Total $ Gained: {1/lengths[destination]}")
                    print(f"  Visualization: {' -> '.join(['(' + node + ')' for node in path])}")
                    print("-" * 50)
        else:
            print("No valid starting exchange found.")


