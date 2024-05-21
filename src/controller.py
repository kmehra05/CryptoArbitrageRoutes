import threading

from src.fetch_data import ExchangeDataFetcher
from src.graph import ArbitrageGraph
from src.pathfinding import *
from src.main_window import MainWindow


class ArbitrageController:
    def __init__(self):
        self.data_fetcher = ExchangeDataFetcher()
        self.view = MainWindow(self)
        self.view.update_exchange_list(self.data_fetcher.get_exchange_names())
        self.view.mainloop()

    def plot_graph(self):
        def run():
            inputs = self.view.get_user_inputs()
            tickers_data = self.data_fetcher.fetch_tickers(*inputs['tickers'])

            arbitrage_graph = ArbitrageGraph()
            arbitrage_graph.populate_nodes(tickers_data)
            arbitrage_graph.update_edges(tickers_data)

            self.pathfinder = PathFinding(arbitrage_graph)
            starting_node = f"{inputs['start_exchange']}/{inputs['start_ticker']}/USD"  # Assume USD as a base
            best_path_graph, multiplier = self.pathfinder.best_path_graph(starting_node)

            self.view.after(0, self.view.display_graph, best_path_graph, multiplier)
            self.view.after(0, self.view.loading_to_summary(generate_best_path_summary(best_path_graph, multiplier)))

        # Start the long-running task in a separate thread
        threading.Thread(target=run).start()