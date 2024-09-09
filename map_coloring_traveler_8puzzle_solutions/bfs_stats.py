from collections import deque


class Puzzle8:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def is_goal(self, state):
        return state == self.goal_state

    def get_neighbors(self, state):
        neighbors = []
        zero_index = state.index(0)  # Find the index of the blank tile
        valid_moves = [(-1, 3), (1, -3), (0, -1), (0, 1)]  # Up, Down, Left, Right (relative to zero_index position)
        row, col = zero_index // 3, zero_index % 3

        for drow, dcol in valid_moves:
            new_row, new_col = row + drow, col + dcol
            new_index = new_row * 3 + new_col
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Swap the blank tile with the adjacent tile
                new_state = list(state)
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                neighbors.append(tuple(new_state))

        return neighbors


def bfs_stats(puzzle):
    frontier = deque([puzzle.initial_state])
    explored = set()
    node_count_expanded = 0
    node_count_generated = 0
    max_queue_length = 1
    path = []
    parent_map = {puzzle.initial_state: None}

    while frontier:
        current_state = frontier.popleft()
        node_count_expanded += 1

        if puzzle.is_goal(current_state):
            path = reconstruct_path(current_state, parent_map)
            solution_path_length = len(path) - 1
            break

        explored.add(current_state)
        neighbors = puzzle.get_neighbors(current_state)
        if neighbors is None:
            continue  # Skip processing if neighbors are None
        for neighbor in neighbors:
            if neighbor not in explored and neighbor not in frontier:
                frontier.append(neighbor)
                explored.add(neighbor)
                parent_map[neighbor] = current_state
                node_count_generated += 1

        max_queue_length = max(max_queue_length, len(frontier))

    print(f"Total nodes expanded: {node_count_expanded}")
    print(f"Total nodes generated: {node_count_generated}")
    print(f"Max queue length: {max_queue_length}")
    print(f"Solution path length: {solution_path_length}")
    print("Solution path:")
    print_path(path)
    return node_count_expanded, node_count_generated, max_queue_length, solution_path_length


def reconstruct_path(state, parent_map):
    path = []
    while state is not None:
        path.append(state)
        state = parent_map[state]
    return list(reversed(path))


def print_path(path):
    for node in path:
        print(node)
    print('')


if __name__ == "__main__":
    # Example initial and goal states
    initial = (1, 2, 3, 4, 5, 6, 0, 7, 8)  # Example initial state
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # Example goal state
    puzzle = Puzzle8(initial, goal)
    bfs_stats(puzzle)
