import networkx as nx

import fetch_data


class ArbitrageGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_exchanges(self, exchanges):
        for exchange in exchanges:
            if not self.graph.has_node(exchange):
                self.graph.add_node(exchange)