import pathfinding
from fetch_data import ExchangeDataFetcher
from graph import ArbitrageGraph


def main():
    # Instantiate the data fetcher
    data_fetcher = ExchangeDataFetcher()

    # Specify the symbols you're interested in
    symbols = ['BTC', 'ETH', 'DOGE', 'SOL', 'ADA', 'SHIB', 'AVAX']  # Add more symbols as required

    # Fetch ticker data for specified symbols
    tickers_data = data_fetcher.fetch_tickers(*symbols)

    # Initialize the arbitrage graph
    arbitrage_graph = ArbitrageGraph()

    # Populate the graph with nodes
    arbitrage_graph.populate_nodes(tickers_data)

    # Update the graph with edges representing arbitrage opportunities
    arbitrage_graph.update_edges(tickers_data)

    pathfinding.PathFinding(arbitrage_graph).print_paths("kraken/BTC/USD")


if __name__ == "__main__":
    main()
