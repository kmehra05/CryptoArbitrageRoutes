import networkx as nx

import fetch_data


class ArbitrageGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def populate_nodes(self, tickers_data):
        # Create nodes for each exchange and each currency it supports
        for symbol, exchanges_data in tickers_data.items():
            for exchange, data in exchanges_data.items():
                exchange_currency_pair = f"{exchange}/{symbol}"
                if not self.graph.has_node(exchange_currency_pair):
                    self.graph.add_node(exchange_currency_pair, symbol=symbol, exchange=exchange)

    def update_edges(self, tickers_data):
        # Iterate over each ticker and its data
        for from_pair, from_exchanges_data in tickers_data.items():
            current_symbol, from_symbol = from_pair.split("/")
            for from_exchange, from_data in from_exchanges_data.items():
                from_exchange_currency_pair = f"{from_exchange}/{from_pair}"
                for to_pair, to_exchanges_data in tickers_data.items():
                    to_symbol, base_conversion_symbol = to_pair.split("/")
                    for to_exchange, to_data in to_exchanges_data.items():
                        to_exchange_currency_pair = f"{to_exchange}/{to_pair}"

                        if current_symbol == base_conversion_symbol and from_symbol != to_symbol:
                            try:
                                total_to_symbol = 1.0 / to_data['bid']
                                total_from_symbol = total_to_symbol * tickers_data[f'{to_symbol}/{from_symbol}'][f'{to_exchange}']['bid']
                                arbitrage_opportunity = total_from_symbol - from_data['ask']
                                arbitrage_percentage = arbitrage_opportunity / from_data['ask']
                                if arbitrage_percentage > 0:
                                    weight = 1.0 / arbitrage_percentage
                                    self.graph.add_edge(from_exchange_currency_pair, to_exchange_currency_pair,
                                                        weight=weight,
                                                        arbitrage_opportunity=arbitrage_opportunity,
                                                        arbitrage_percentage=arbitrage_percentage,
                                                        from_pair=from_pair, to_pair=to_pair,
                                                        from_ask=from_data['ask'], to_bid=total_from_symbol,
                                                        from_symbol=from_symbol, to_symbol=to_symbol)
                            except Exception:
                                pass
                        elif current_symbol == to_symbol and from_symbol != base_conversion_symbol:
                            continue
                        elif current_symbol != to_symbol:
                            continue
                        elif from_exchange_currency_pair != to_exchange_currency_pair:
                            arbitrage_opportunity = to_data['bid'] - from_data['ask']
                            arbitrage_percentage = arbitrage_opportunity / from_data['ask']
                            # Only add edge if the arbitrage opportunity is positive (profitable)
                            if arbitrage_percentage > 0:
                                weight = 1.0 / arbitrage_percentage
                                self.graph.add_edge(from_exchange_currency_pair, to_exchange_currency_pair,
                                                    weight=weight,
                                                    arbitrage_opportunity=arbitrage_opportunity,
                                                    arbitrage_percentage=arbitrage_percentage,
                                                    from_pair=from_pair, to_pair=to_pair,
                                                    from_ask=from_data['ask'], to_bid=to_data['bid'],
                                                    from_symbol=from_symbol, to_symbol=to_symbol)

    def print_graph(self):
        for edge in self.graph.edges(data=True):
            from_node, to_node, data = edge
            print(f"Edge from {from_node} (buy at ask) to {to_node} (sell at bid):")
            print(f"    From Symbol: {data['from_symbol']} | To Symbol: {data['to_symbol']}")
            print(f"    Ask at {from_node}: {data['from_ask']} | Bid at {to_node}: {data['to_bid']}")
            print(f"    Arbitrage Opportunity: {data['arbitrage_opportunity']}")
            print(f"    Arbitrage Percentage: {data['arbitrage_percentage']}")
            print(f"    Weight of: {data['weight']}")