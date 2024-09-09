from collections import deque

class Puzzle8:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.valid_moves = [
            [-1, 3, -1, 1],
            [-1, 4, 0, 2],
            [-1, 5, 1, -1],
            [0, 6, -1, 4],
            [1, 7, 3, 5],
            [2, 8, 4, -1],
            [3, -1, -1, 7],
            [4, -1, 6, 8],
            [5, -1, 7, -1]
        ]

    def is_goal(self, state):
        return state == self.goal_state

    def get_neighbors(self, state):
        neighbors = []
        zero_index = state.index(0)
        for move in self.valid_moves[zero_index]:
            if move != -1:
                new_state = list(state)
                new_state[zero_index], new_state[move] = new_state[move], new_state[zero_index]
                neighbors.append(tuple(new_state))
        return neighbors

    def expand(self, node):
        neighbors = self.get_neighbors(node.state)
        return [TreeNode(self, neighbor, node, node.g + 1) for neighbor in neighbors]

class TreeNode:
    def __init__(self, problem, state, parent=None, g_value=0):
        self.problem = problem
        self.state = state
        self.parent = parent
        self.g = g_value
        self.h = 0  # Assuming heuristic function is not used in this case
        self.f = self.g + self.h

    def is_goal(self):
        return self.problem.is_goal(self.state)

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

def check_cyclic_repeats(node):
    current = node
    seen_states = set()

    while current.parent is not None:
        if current.state in seen_states:
            return True
        seen_states.add(current.state)
        current = current.parent

    return False

def bfs_cycles(problem):
    frontier = deque([TreeNode(problem, problem.initial_state)])
    explored = set()
    node_count = 0
    max_queue_length = 0
    nodes_generated = 0
    solution_path_length = -1

    while frontier:
        max_queue_length = max(max_queue_length, len(frontier))
        current_node = frontier.popleft()
        node_count += 1

        if current_node.is_goal():
            solution_path = current_node.path()
            solution_path_length = len(solution_path) - 1
            print(f"Solution path length: {solution_path_length}")
            print("Solution path:")
            for node in solution_path:
                print(node.state)
            break

        if not check_cyclic_repeats(current_node):
            for child in problem.expand(current_node):
                if child.state not in explored:
                    frontier.append(child)
                    explored.add(child.state)
                    nodes_generated += 1

    print(f"Total nodes expanded: {node_count}")
    print(f"Total nodes generated: {nodes_generated}")
    print(f"Max queue length: {max_queue_length}")

if __name__ == "__main__":
    # Example initial states
    examples = [
        (1, 2, 3, 4, 6, 0, 7, 5, 8),
        (2, 3, 0, 1, 5, 6, 4, 7, 8),
        (4, 1, 2, 7, 6, 3, 0, 5, 8),
        (4, 1, 2, 7, 6, 3, 5, 8, 0),
        (5, 3, 0, 4, 7, 6, 2, 1, 8)  # Example5
    ]

    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # Example goal state

    for initial in examples:
        puzzle = Puzzle8(initial, goal)
        print(f"\nStarting BFS with initial state: {initial}")
        bfs_cycles(puzzle)
