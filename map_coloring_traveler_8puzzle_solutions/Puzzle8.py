#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 12:52:09 2019
Puzzle 8 problem.
This module includes:
     - Puzzle 8 problem definition
     - Search Tree
     - hash table implementation
     - 5 Examples of increasing complexity
@author: milos
"""
from collections import deque
from random import sample

NO_MOVE = -1
NULL = -1

# definition of the Puzzle 8 problem
class Puzzle8_Problem:
    initial_state = ''
    move_cost = 1
    end_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # defines end state
    valid_moves = [
        [NO_MOVE, 3, NO_MOVE, 1],
        [NO_MOVE, 4, 0, 2],
        [NO_MOVE, 5, 1, NO_MOVE],
        [0, 6, NO_MOVE, 4],
        [1, 7, 3, 5],
        [2, 8, 4, NO_MOVE],
        [3, NO_MOVE, NO_MOVE, 7],
        [4, NO_MOVE, 6, 8],
        [5, NO_MOVE, 7, NO_MOVE]
    ]

    def __init__(self, init_state=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        self.initial_state = init_state

    def shuffle_state(self, k):
        pick = self.end_state
        for _ in range(k):
            new = self.generate_all_neighbor_states(pick)
            pick, _ = sample(new, 1)[0]
            print(pick)
        return pick

    def goal_condition(self, state):
        return state == self.end_state

    def generate_all_neighbor_states(self, state):
        res = []
        zero_position = state.index(0)
        for i in range(4):
            next_position = self.valid_moves[zero_position][i]
            if next_position != NO_MOVE:
                new_state = list(state)
                new_state[zero_position], new_state[next_position] = state[next_position], state[zero_position]
                res.append((tuple(new_state), self.move_cost))
        return res

    def h_function(self, state):
        return 0


# definition of the TreeNode
class TreeNode:
    problem = NULL
    state = ''
    parent = NULL
    f = 0
    g = 0
    h = 0  # values of f, g, and h functions related to path

    def __init__(self, problem, state, parent=None, g_value=0):
        self.problem = problem
        self.state = state
        self.parent = parent
        self.g = g_value
        self.h = problem.h_function(state)
        self.f = self.g + self.h

    def goalp(self):
        return self.problem.goal_condition(self.state)

    def generate_new_tree_nodes(self):
        new_neighbors = self.problem.generate_all_neighbor_states(self.state)
        res = []
        for new_state in new_neighbors:
            new_node = TreeNode(self.problem, new_state[0], self, self.g + new_state[1])
            res.append(new_node)
        return res

    def print_state(self):
        for j in range(0, 9, 3):
            print((self.state[j], self.state[j + 1], self.state[j + 2]))
        print(' ')

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


# definition of the hash table that can be used to store Puzzle 8 states
class HashTable:
    def __init__(self):
        self.hash = {}

    def in_hashp(self, item):
        return item in self.hash

    def add_hash(self, item, value=0):
        self.hash[item] = value

    def get_hash_value(self, item):
        return self.hash.get(item, -1)

    def delete_hash(self):
        self.hash.clear()


def print_path(path):
    for node in path:
        node.print_state()


def main():
    problem = Puzzle8_Problem()
    shuffled_state = problem.shuffle_state(10)  # Shuffle the state with 10 moves
    print("Shuffled state:")
    print(shuffled_state)

    initial_node = TreeNode(problem, shuffled_state)
    path = initial_node.path()
    if path:
        print("Path from initial to goal state:")
        print_path(path)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
