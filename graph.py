import networkx as nx


class ArbitrageGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_exchanges(self, exchanges):
        for exchange in exchanges:
            if not self.graph.has_node(exchange):
                self.graph.add_node(exchange)

    def update_edges(self, tickers_data):
        # Iterate over each ticker and its data
        for symbol, exchanges_data in tickers_data.items():
            # Iterate through each pair of exchanges to create edges between them
            for from_exchange, from_data in exchanges_data.items():
                for to_exchange, to_data in exchanges_data.items():
                    if from_exchange != to_exchange:
                        # Calculate the arbitrage opportunity (buy at ask of from_exchange, sell at bid of to_exchange)
                        arbitrage_opportunity = to_data['bid'] - from_data['ask']
                        # Only add edge if the arbitrage opportunity is positive (profitable)
                        if arbitrage_opportunity > 0:
                            # The weight is still the reciprocal to prioritize higher opportunities when finding paths
                            weight = 1.0 / arbitrage_opportunity
                            self.graph.add_edge(from_exchange, to_exchange, weight=weight,
                                                arbitrage_opportunity=arbitrage_opportunity, symbol=symbol,
                                                from_ask=from_data['ask'], to_bid=to_data['bid'])
