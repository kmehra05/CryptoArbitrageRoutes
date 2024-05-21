import heapq
import networkx as nx


def generate_best_path_summary(best_path_graph, total_multiplier, investment_amount=100):
    path = [u for u, v in best_path_graph.edges()]

    # Adding the last node
    if best_path_graph.edges():
        last_node = list(best_path_graph.edges())[-1][1]
        path.append(last_node)

    final_amount = investment_amount * total_multiplier
    path_str = " --> ".join(path)
    return (f"Best path:\n"
            f"Path: {path_str} with a multiplier of: {total_multiplier:.12f}\n"
            f"Investment: ${investment_amount} --> ${final_amount:.2f}")


class PathFinding:
    def __init__(self, arbitrage_graph):
        self.graph = arbitrage_graph.graph  # Access the graph attribute of the ArbitrageGraph instance

    def find_all_paths(self, source):
        # Initialize distances with infinity and set source distance to 1
        distances = {node: float('inf') for node in self.graph.nodes}
        distances[source] = 1

        # Priority queue to manage the exploration of nodes
        queue = [(1, source)]

        # Record the paths
        paths = {node: [] for node in self.graph.nodes}
        paths[source] = [source]

        # Set to track visited nodes
        visited = set()

        while queue:
            # Extract the node with the smallest distance
            current_distance, current_node = heapq.heappop(queue)

            # Mark the node as visited
            visited.add(current_node)

            # Explore each neighbor of the current node
            for neighbor in self.graph[current_node]:
                if neighbor not in visited:
                    weight = self.graph[current_node][neighbor]['weight']
                    new_distance = current_distance * weight

                    # If a shorter path is found, update the distance and path
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        paths[neighbor] = paths[current_node] + [neighbor]
                        heapq.heappush(queue, (new_distance, neighbor))

        return distances, paths

    def find_best_path(self, source):
        distances, paths = self.find_all_paths(source)
        min_distance = float('inf')
        best_path = []
        for node, distance in distances.items():
            if distance < min_distance and node != source:
                min_distance = distance
                best_path = paths[node]
        total_multiplier = 1 / min_distance
        return min_distance, best_path, total_multiplier

    def best_path_graph(self, source):
        # Find the best path from the source
        _, best_path, total_multiplier = self.find_best_path(source)

        # Create a new graph based on the best path
        best_path_graph = nx.DiGraph()
        path_pairs = zip(best_path[:-1], best_path[1:])

        for u, v in path_pairs:
            weight = self.graph[u][v]['weight']
            best_path_graph.add_edge(u, v, weight=1 / weight)  # Use reciprocal of the original weight

        return best_path_graph, total_multiplier

    def print_paths(self, source):
        distances, all_paths = self.find_all_paths(source)
        best_distance, best_path, total_multiplier = self.find_best_path(source)

        print("All paths from source:", source)
        for node, path in all_paths.items():
            if distances[node] != float('inf'):
                print(f"Path to {node}: {path} with multiplicative weight: {distances[node]}")
        print("\nBest path:")
        print(f"Path: {best_path} with the best multiplicative weight: {best_distance}")
        print(f"Investment: $10 --> ${total_multiplier * 10}")
