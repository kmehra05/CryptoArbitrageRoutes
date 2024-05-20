from fetch_data import ExchangeDataFetcher
from graph import ArbitrageGraph
from pathfinding import Pathfinding

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

    # Initialize the pathfinding
    pathfinder = Pathfinding(arbitrage_graph)

    # Find the best arbitrage path
    start_exchange, paths, lengths = pathfinder.find_best_arbitrage()

    # Output the paths
    if start_exchange:
        arbitrage_graph.print_graph()
        pathfinder.print_paths(start_exchange, paths, lengths)
    else:
        print("No viable arbitrage paths found.")

if __name__ == "__main__":
    main()
