from typing import List, Dict, Any
from optimization.ortools_solver import ORToolsSolver
from optimization.beam_search import BeamSearchOptimizer
from services.google_maps_service import google_maps_client

class CandidateGenerator:
    def __init__(self):
        self.ortools = ORToolsSolver()
        self.beam = BeamSearchOptimizer(beam_width=3)

    async def generate_candidates(self, locations: List[str]) -> List[List[str]]:
        """
        Generate multiple route candidates.
        """
        if len(locations) <= 2:
            return [locations]

        # Fetch distance matrix
        matrix_response = await google_maps_client.get_distance_matrix(locations, locations)
        
        # Build numerical distance matrix
        n = len(locations)
        dist_matrix = [[0.0] * n for _ in range(n)]
        
        for i, row in enumerate(matrix_response.get("rows", [])):
            for j, element in enumerate(row.get("elements", [])):
                if element.get("status") == "OK":
                    dist_matrix[i][j] = element["distance"]["value"]
                else:
                    dist_matrix[i][j] = 99999.0 # Penalty for unreachable

        candidates = []
        
        # 1. OR-Tools Candidate
        ortools_indices = self.ortools.solve_tsp(dist_matrix)
        candidates.append([locations[i] for i in ortools_indices])
        
        # 2. Beam Search Candidate
        beam_indices = self.beam.solve(dist_matrix)
        candidates.append([locations[i] for i in beam_indices])
        
        # 3. Simple Greedy (nearest neighbor)
        greedy_indices = self._nearest_neighbor(dist_matrix)
        candidates.append([locations[i] for i in greedy_indices])
        
        # Remove duplicates
        unique_candidates = []
        seen = set()
        for c in candidates:
            c_tuple = tuple(c)
            if c_tuple not in seen:
                seen.add(c_tuple)
                unique_candidates.append(c)
                
        return unique_candidates

    def _nearest_neighbor(self, dist_matrix: List[List[float]]) -> List[int]:
        n = len(dist_matrix)
        visited = {0}
        route = [0]
        current = 0
        
        while len(visited) < n:
            next_node = None
            min_dist = float('inf')
            for i in range(n):
                if i not in visited and dist_matrix[current][i] < min_dist:
                    min_dist = dist_matrix[current][i]
                    next_node = i
            
            if next_node is not None:
                route.append(next_node)
                visited.add(next_node)
                current = next_node
            else:
                break
                
        return route
