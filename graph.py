import networkx as nx

import fetch_data


class ArbitrageGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_exchanges(self, tickers_data):
        # Create nodes for each exchange and each currency it supports
        for symbol, exchanges_data in tickers_data.items():
            for exchange, data in exchanges_data.items():
                exchange_currency_pair = f"{exchange}/{symbol}"
                if not self.graph.has_node(exchange_currency_pair):
                    self.graph.add_node(exchange_currency_pair, symbol=symbol, exchange=exchange)

    def update_edges(self, tickers_data):
        # Iterate over each ticker and its data
        for symbol, exchanges_data in tickers_data.items():
            # Create edges between every possible pair of exchange/currency nodes
            for from_exchange, from_data in exchanges_data.items():
                from_exchange_currency_pair = f"{from_exchange}/{symbol}"
                for to_exchange, to_data in exchanges_data.items():
                    to_exchange_currency_pair = f"{to_exchange}/{symbol}"
                    if from_exchange_currency_pair != to_exchange_currency_pair:
                        # Calculate the arbitrage opportunity (buy at ask of from_exchange, sell at bid of to_exchange)
                        arbitrage_opportunity = to_data['bid'] - from_data['ask']
                        # Only add edge if the arbitrage opportunity is positive (profitable)
                        if arbitrage_opportunity > 0:
                            weight = 1.0 / arbitrage_opportunity
                            self.graph.add_edge(from_exchange_currency_pair, to_exchange_currency_pair, weight=weight,
                                                arbitrage_opportunity=arbitrage_opportunity, symbol=symbol,
                                                from_ask=from_data['ask'], to_bid=to_data['bid'])

    def print_graph(self):
        for edge in self.graph.edges(data=True):
            from_node, to_node, data = edge
            print(f"Edge from {from_node} (buy at ask) to {to_node} (sell at bid) for {data['symbol']}:")
            print(f"    Ask at {from_node}: {data['from_ask']} | Bid at {to_node}: {data['to_bid']}")
            print(f"    Arbitrage Opportunity: {data['arbitrage_opportunity']}")
