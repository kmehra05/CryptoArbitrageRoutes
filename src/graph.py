import networkx as nx


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
                        if from_exchange_currency_pair != to_exchange_currency_pair:
                            self._create_edge(from_exchange_currency_pair, to_exchange_currency_pair, to_data,
                                              from_data, tickers_data)

    def _create_edge(self, from_exchange_pair, to_exchange_pair, to_data, from_data, tickers_data):
        start_exchange, current_symbol, start_symbol = from_exchange_pair.split("/")
        end_exchange, to_symbol, base_to_symbol = to_exchange_pair.split("/")
        arbitrage_multiplier = 0
        weight = 0

        if current_symbol == to_symbol and start_symbol == base_to_symbol:
            arbitrage_multiplier = to_data['bid'] / from_data['ask']
            weight = 1 / arbitrage_multiplier

        elif current_symbol != to_symbol and start_symbol == base_to_symbol == "USD":
            try:  # consider BTC/USD to ETH/BTC to ETH/USD
                if f'{to_symbol}/{current_symbol}' in tickers_data and f'{end_exchange}' in tickers_data[
                    f'{to_symbol}/{current_symbol}']:
                    intermediate_data = tickers_data[f'{to_symbol}/{current_symbol}'][f'{end_exchange}']
                    #
                    total_usd_converted = ((1 / intermediate_data['ask']) * to_data['bid'])
                    arbitrage_multiplier = total_usd_converted / from_data['ask']
                    weight = 1 / arbitrage_multiplier

                elif f'{current_symbol}/{to_symbol}' in tickers_data and f'{end_exchange}' in tickers_data[
                    f'{current_symbol}/{to_symbol}']:
                    intermediate_data = tickers_data[f'{current_symbol}/{to_symbol}'][f'{end_exchange}']
                    total_usd_converted = intermediate_data['ask'] * to_data['bid']
                    arbitrage_multiplier = total_usd_converted / from_data['ask']
                    weight = 1 / arbitrage_multiplier

            except Exception:
                pass
        else:
            pass

        if arbitrage_multiplier != 0 and weight != 0:
            self.graph.add_edge(from_exchange_pair, to_exchange_pair, weight=weight,
                                arbitrage_multiplier=arbitrage_multiplier, from_ask=from_data['ask'],
                                to_bid=to_data['bid'])

    def print_graph(self):
        for edge in self.graph.edges(data=True):
            from_node, to_node, data = edge
            print(f"Edge from {from_node} (buy at ask) to {to_node} (sell at bid):")
            print(f"    Ask at {from_node}: {data['from_ask']} | Bid at {to_node}: {data['to_bid']}")
            print(f"    Arbitrage Multiplier: {data['arbitrage_multiplier']}")
            print(f"    Weight of: {data['weight']}")
