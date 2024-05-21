import unittest
from graph import ArbitrageGraph


class TestArbitrageGraph(unittest.TestCase):
    def setUp(self):
        self.arbitrage_graph = ArbitrageGraph()

    def test_populate_nodes(self):
        # Simulate ticker data
        tickers_data = {
            'BTC/USD': {
                'kraken': {'symbol': 'BTC/USD', 'bid': 50000, 'ask': 50100},
                'gemini': {'symbol': 'BTC/USD', 'bid': 50010, 'ask': 50110}
            }
        }

        # Populate nodes
        self.arbitrage_graph.populate_nodes(tickers_data)

        # Check if nodes are created correctly
        expected_nodes = ['kraken/BTC/USD', 'gemini/BTC/USD']
        actual_nodes = [n for n in self.arbitrage_graph.graph.nodes]
        self.assertEqual(sorted(expected_nodes), sorted(actual_nodes))

    def test_update_edges(self):
        # Simulate ticker data
        tickers_data = {
            'BTC/USD': {
                'kraken': {'symbol': 'BTC/USD', 'bid': 50000, 'ask': 50100},
            },
            'ETH/USD': {
                'kraken': {'symbol': 'ETH/USD', 'bid': 2000, 'ask': 2020},
            },
            'BTC/ETH': {
                'kraken': {'symbol': 'BTC/ETH', 'bid': 25, 'ask': 26}
            }
        }

        # Populate nodes
        self.arbitrage_graph.populate_nodes(tickers_data)

        # Update edges
        self.arbitrage_graph.update_edges(tickers_data)

        # Check if edges are created correctly
        expected_edges = [
            ('kraken/BTC/USD', 'kraken/ETH/USD'),
            ('kraken/ETH/USD', 'kraken/BTC/USD'),
        ]
        actual_edges = [e for e in self.arbitrage_graph.graph.edges]
        self.assertEqual(len(expected_edges), len(actual_edges))  # Validates if edges count matches

        # Check weights and arbitrage_multipliers
        for from_node, to_node in expected_edges:
            weight = self.arbitrage_graph.graph[from_node][to_node]['weight']
            arbitrage_multiplier = self.arbitrage_graph.graph[from_node][to_node]['arbitrage_multiplier']
            self.assertTrue(weight > 0)
            self.assertTrue(arbitrage_multiplier > 0)


if __name__ == '__main__':
    unittest.main()
