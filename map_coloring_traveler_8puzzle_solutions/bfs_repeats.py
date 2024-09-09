from collections import deque


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


class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.popleft()

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


def bfs_repeats(problem):
    frontier = Queue()
    explored = set()
    initial_node = Node(None, problem.initial_state, None, 0)
    frontier.enqueue(initial_node)

    nodes_expanded = 0
    max_queue_length = 0
    nodes_generated = 0

    while not frontier.is_empty():
        node = frontier.dequeue()
        nodes_expanded += 1

        # Removed the print statement for Enqueued node with state
        # print(f"Exploring node with state: {node.state}")

        if problem.is_goal(node.state):
            return node, nodes_expanded, nodes_generated, max_queue_length

        if node.state not in explored:
            explored.add(node.state)
            for child in problem.get_neighbors(node.state):
                nodes_generated += 1
                if child.state not in explored and child not in frontier.queue:
                    child.parent = node  # Set the parent for path reconstruction
                    frontier.enqueue(child)
                    # Removed the print statement for enqueued nodes
                    # print(f"Enqueued node with state: {child.state}")

        max_queue_length = max(max_queue_length, frontier.size())

    return None, nodes_expanded, nodes_generated, max_queue_length


def print_solution(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    print("Solution path length:", len(path) - 1)
    print("Solution path:")
    for state in path:
        print(state)


if __name__ == "__main__":
    initial_states = [
        (1, 2, 3, 4, 6, 0, 7, 5, 8),
        (2, 3, 0, 1, 5, 6, 4, 7, 8),
        (4, 1, 2, 7, 6, 3, 0, 5, 8),
        (4, 1, 2, 7, 6, 3, 5, 8, 0),
        (5, 3, 0, 4, 7, 6, 2, 1, 8)
    ]
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    for initial in initial_states:
        print(f"Starting BFS with initial state: {initial}")
        puzzle = Puzzle8(initial, goal_state)
        result, nodes_expanded, nodes_generated, max_queue_length = bfs_repeats(puzzle)
        if result:
            print_solution(result)
        else:
            print("No solution found")
        print(f"Total nodes expanded: {nodes_expanded}")
        print(f"Total nodes generated: {nodes_generated}")
        print(f"Max queue length: {max_queue_length}\n")
