import networkx as nx


class Pathfinding:
    def __init__(self, graph):
        self.graph = graph

    def find_best_arbitrage(self):
        # Determine the starting node (exchange with the lowest ask price)
        lowest_ask_price = float('inf')
        start_exchange = None

        for node, data in self.graph.graph.nodes(data=True):
            if 'BTC/USD' in data['symbol']:
                for _, _, edge_data in self.graph.graph.edges(node, data=True):
                    if edge_data['from_ask'] < lowest_ask_price:
                        lowest_ask_price = edge_data['from_ask']
                        start_exchange = node

        if start_exchange:
            lengths, paths = nx.single_source_dijkstra(self.graph.graph, start_exchange, weight='weight')
            return start_exchange, paths, lengths
        else:
            return None, {}, {}

    def print_paths(self, start_exchange, paths, lengths):
        if start_exchange:
            print(f"Starting Arbitrage at {start_exchange} with lowest ask price\n")
            for destination, path in paths.items():
                if destination != start_exchange and destination.endswith('/USD'):
                    path_description = " -> ".join([f"{node}" for node in path])
                    total_profit = 0
                    # Iterate through the path to calculate total profit
                    for i in range(len(path) - 1):
                        edge = self.graph.graph.get_edge_data(path[i], path[i + 1])
                        if edge:
                            total_profit += edge['arbitrage_opportunity']

                    print(f"Path to {destination}:")
                    print(f"  Route: {path_description}")
                    print(f"  Total weight (cost): {lengths[destination]:.4f}")
                    print(f"  Visualization: {' -> '.join(['(' + node + ')' for node in path])}")
                    print(f"Total profit is ${total_profit}")
                    print("-" * 50)
        else:
            print("No valid starting exchange found.")