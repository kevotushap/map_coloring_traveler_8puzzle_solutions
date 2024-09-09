class Puzzle8:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def is_goal(self, state):
        return state == self.goal_state

    def get_neighbors(self, state):
        neighbors = []
        zero_index = state.index(0)
        row, col = divmod(zero_index, 3)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_zero_index = new_row * 3 + new_col
                new_state = list(state)
                new_state[zero_index], new_state[new_zero_index] = new_state[new_zero_index], new_state[zero_index]
                neighbors.append(Node(None, tuple(new_state), None, 0))

        return neighbors

class Node:
    def __init__(self, parent, state, action, path_cost):
        self.parent = parent
        self.state = state
        self.action = action
        self.path_cost = path_cost

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

def depth_first_search_limit(problem, limit):
    stack = [Node(None, problem.initial_state, None, 0)]
    explored = set()
    state_min_path = {problem.initial_state: 0}
    nodes_expanded = 0
    max_stack_length = 1
    nodes_generated = 0
    optimal_solution_node = None

    while stack:
        node = stack.pop()
        nodes_expanded += 1

        if problem.is_goal(node.state):
            optimal_solution_node = node
            break

        if node.path_cost < limit:
            for neighbor in problem.get_neighbors(node.state):
                if (neighbor.state not in explored or state_min_path.get(neighbor.state, float('inf')) > node.path_cost + 1):
                    if neighbor.state not in state_min_path or state_min_path[neighbor.state] > node.path_cost + 1:
                        state_min_path[neighbor.state] = node.path_cost + 1
                        stack.append(Node(node, neighbor.state, None, node.path_cost + 1))
                        nodes_generated += 1
                        max_stack_length = max(max_stack_length, len(stack))
            explored.add(node.state)

    if optimal_solution_node:
        print(f"Solution path length: {optimal_solution_node.path_cost}")
        print("Solution path:")
        print_path(optimal_solution_node)
    else:
        print("No solution found within the depth limit")

    print(f"Total nodes expanded: {nodes_expanded}")
    print(f"Total nodes generated: {nodes_generated}")
    print(f"Max stack length: {max_stack_length}")

def print_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    for state in path:
        print(state)
    print('')

if __name__ == "__main__":
    initial_states = [
        (1, 2, 3, 4, 6, 0, 7, 5, 8),
        (2, 3, 0, 1, 5, 6, 4, 7, 8),
        (4, 1, 2, 7, 6, 3, 0, 5, 8)
    ]
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    for initial in initial_states:
        print(f"Starting Depth-Limited DFS with initial state: {initial}")
        puzzle = Puzzle8(initial, goal_state)
        depth_first_search_limit(puzzle, limit=10)
