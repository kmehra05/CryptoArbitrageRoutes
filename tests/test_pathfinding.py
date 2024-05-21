import unittest
from graph import ArbitrageGraph
from pathfinding import PathFinding


class TestPathFinding(unittest.TestCase):
    def setUp(self):
        # Create a simple arbitrage graph to test pathfinding
        self.arbitrage_graph = ArbitrageGraph()
        self.arbitrage_graph.graph.add_edge('A', 'B', weight=0.9)
        self.arbitrage_graph.graph.add_edge('B', 'C', weight=0.95)
        self.arbitrage_graph.graph.add_edge('A', 'C', weight=0.85)
        self.path_finding = PathFinding(self.arbitrage_graph)

    def test_find_all_paths(self):
        distances, paths = self.path_finding.find_all_paths('A')
        expected_distances = {'A': 1, 'B': 0.9, 'C': 0.85}
        expected_paths = {'A': ['A'], 'B': ['A', 'B'], 'C': ['A', 'C']}
        self.assertEqual(distances, expected_distances)
        self.assertEqual(paths, expected_paths)

    def test_find_best_path(self):
        min_distance, best_path, total_multiplier = self.path_finding.find_best_path('A')
        expected_distance = 0.85
        expected_best_path = ['A', 'C']
        expected_multiplier = 1 / 0.85
        self.assertAlmostEqual(min_distance, expected_distance)
        self.assertEqual(best_path, expected_best_path)
        self.assertAlmostEqual(total_multiplier, expected_multiplier)


if __name__ == '__main__':
    unittest.main()
