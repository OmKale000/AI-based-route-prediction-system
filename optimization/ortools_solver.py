import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from typing import List, Dict, Any

class ORToolsSolver:
    def __init__(self):
        pass
        
    def solve_tsp(self, distance_matrix: List[List[float]], num_vehicles: int = 1, depot: int = 0) -> List[int]:
        """
        Solves the Traveling Salesperson Problem using Google OR-Tools.
        """
        # Multiply by 1000 and convert to int for OR-Tools which requires integer weights
        int_distance_matrix = [[int(val * 1000) for val in row] for row in distance_matrix]
        
        manager = pywrapcp.RoutingIndexManager(len(int_distance_matrix), num_vehicles, depot)
        routing = pywrapcp.RoutingModel(manager)
        
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int_distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = 2

        solution = routing.SolveWithParameters(search_parameters)
        
        if not solution:
            # Fallback to simple order if no solution found
            return list(range(len(distance_matrix)))
            
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        
        return route
