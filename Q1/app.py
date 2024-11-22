import copy
import random
from typing import List, Tuple, Optional

class EightPuzzle:
    def __init__(self, initial_state: List[List[int]], goal_state: List[List[int]]):
        self.current_state = initial_state
        self.goal_state = goal_state
        self.size = 3
        
    def find_blank(self, state: List[List[int]]) -> Tuple[int, int]:
        """Find the position of the blank (0) in the puzzle."""
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    return i, j
        return -1, -1

    def get_manhattan_distance(self, state: List[List[int]]) -> int:
        """Calculate Manhattan distance heuristic."""
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] != 0:
                    value = state[i][j]
                    # Find goal position of current value
                    goal_i, goal_j = None, None
                    for x in range(self.size):
                        for y in range(self.size):
                            if self.goal_state[x][y] == value:
                                goal_i, goal_j = x, y
                                break
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return -distance  # Negative because we want to maximize

    def get_misplaced_tiles(self, state: List[List[int]]) -> int:
        """Calculate number of misplaced tiles heuristic."""
        misplaced = 0
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] != self.goal_state[i][j] and state[i][j] != 0:
                    misplaced += 1
        return -misplaced  # Negative because we want to maximize

    def get_neighbors(self, state: List[List[int]]) -> List[List[List[int]]]:
        """Generate all possible neighbor states."""
        neighbors = []
        blank_i, blank_j = self.find_blank(state)
        
        # Possible moves: up, down, left, right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for move_i, move_j in moves:
            new_i, new_j = blank_i + move_i, blank_j + move_j
            
            if 0 <= new_i < self.size and 0 <= new_j < self.size:
                new_state = copy.deepcopy(state)
                # Swap blank with neighbor
                new_state[blank_i][blank_j], new_state[new_i][new_j] = \
                    new_state[new_i][new_j], new_state[blank_i][blank_j]
                neighbors.append(new_state)
                
        return neighbors

    def hill_climbing(self, max_iterations: int = 1000) -> Tuple[bool, List[List[List[int]]], int]:
        """
        Perform hill climbing search.
        Returns: (success_flag, path_taken, iterations)
        """
        current = self.current_state
        path = [copy.deepcopy(current)]
        iterations = 0
        
        while iterations < max_iterations:
            iterations += 1
            
            # Get all neighbors
            neighbors = self.get_neighbors(current)
            if not neighbors:
                return False, path, iterations
            
            # Evaluate current state and neighbors using heuristic
            current_value = self.get_manhattan_distance(current)
            
            # Find the best neighbor
            best_neighbor = None
            best_value = float('-inf')
            
            for neighbor in neighbors:
                neighbor_value = self.get_manhattan_distance(neighbor)
                if neighbor_value > best_value:
                    best_value = neighbor_value
                    best_neighbor = neighbor
            
            # If no better neighbor found, we're at a local maximum
            if best_value <= current_value:
                return False, path, iterations
            
            # Move to the best neighbor
            current = best_neighbor
            path.append(copy.deepcopy(current))
            
            # Check if we've reached the goal
            if current == self.goal_state:
                return True, path, iterations
        
        return False, path, iterations

def print_state(state: List[List[int]]):
    """Pretty print a puzzle state."""
    for row in state:
        print(row)
    print()

# Test the implementation
if __name__ == "__main__":
    # Goal state
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    # Easy initial state (few moves from goal)
    initial_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    
    # Create puzzle instance
    puzzle = EightPuzzle(initial_state, goal_state)
    
    # Print initial state
    print("Initial State:")
    print_state(initial_state)
    
    # Solve puzzle
    success, path, iterations = puzzle.hill_climbing()
    
    # Print results
    print(f"Solution found: {success}")
    print(f"Iterations: {iterations}")
    print("\nSolution path:")
    for state in path:
        print_state(state)
