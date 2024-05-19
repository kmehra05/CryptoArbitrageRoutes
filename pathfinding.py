import networkx as nx


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