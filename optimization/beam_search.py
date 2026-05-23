from typing import List, Dict

class BeamSearchOptimizer:
    def __init__(self, beam_width: int = 3):
        self.beam_width = beam_width

    def solve(self, distance_matrix: List[List[float]], start_node: int = 0) -> List[int]:
        """
        Heuristic beam search to find good candidate routes.
        Maintains `beam_width` partial routes at each step.
        """
        num_nodes = len(distance_matrix)
        if num_nodes == 0:
            return []
            
        # Initialize beam with the start node
        # Each beam state: (current_cost, route, visited_set)
        beam = [(0.0, [start_node], {start_node})]
        
        for _ in range(num_nodes - 1):
            next_beam = []
            for cost, route, visited in beam:
                current_node = route[-1]
                
                # Explore all unvisited neighbors
                for next_node in range(num_nodes):
                    if next_node not in visited:
                        new_cost = cost + distance_matrix[current_node][next_node]
                        new_route = route + [next_node]
                        new_visited = visited | {next_node}
                        next_beam.append((new_cost, new_route, new_visited))
            
            # Keep top K based on cost
            next_beam.sort(key=lambda x: x[0])
            beam = next_beam[:self.beam_width]
            
        # Return the best route found
        if beam:
            best_route = beam[0][1]
            return best_route
        return list(range(num_nodes))
