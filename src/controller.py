from fetch_data import ExchangeDataFetcher
import graph
import pathfinding
import main_window


class ArbitrageController:
    def __init__(self):
        self.data_fetcher = ExchangeDataFetcher()
        self.view = main_window.MainWindow(self)
        self.view.update_exchange_list(self.data_fetcher.get_exchange_names())
        self.view.mainloop()

    def plot_graph(self):
        inputs = self.view.get_user_inputs()
        tickers_data = self.data_fetcher.fetch_tickers(*inputs['tickers'])

        arbitrage_graph = graph.ArbitrageGraph()
        arbitrage_graph.populate_nodes(tickers_data)
        arbitrage_graph.update_edges(tickers_data)

        self.pathfinder = pathfinding.PathFinding(arbitrage_graph)

        starting_node = f"{inputs['start_exchange']}/{inputs['start_ticker']}/USD"  # Assume USD as a base

        best_path_graph, multiplier = self.pathfinder.best_path_graph(starting_node)

        self.view.display_graph(best_path_graph, multiplier)


if __name__ == "__main__":
    controller = ArbitrageController()
