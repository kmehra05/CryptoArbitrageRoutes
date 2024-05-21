import pathfinding
from fetch_data import ExchangeDataFetcher
from graph import ArbitrageGraph
import main_window


def main():

    data_fetcher = ExchangeDataFetcher()

    ticker_list = ['BTC', 'ETH', 'DOGE']

    tickers_data = data_fetcher.fetch_tickers(*ticker_list)

    arbitrage_graph = ArbitrageGraph()

    arbitrage_graph.populate_nodes(tickers_data)

    arbitrage_graph.update_edges(tickers_data)

    pathfinder = pathfinding.PathFinding(arbitrage_graph)
    pathfinder.print_paths('kraken/BTC/USD')
    starting_node = "kraken/BTC/USD"

    # best_path_graph = pathfinder.best_path_graph(starting_node) # returns networkx digraph of the best path


if __name__ == '__main__':
    main()
