#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:01:00 2019
Vanilla breadth-first search
- Relies on Puzzle8.py module

@author: milos
"""

from Puzzle8 import *
from collections import deque  # Import deque from collections


def breadth_first_search(problem):
    queue = deque()  # Initialize the queue
    root = TreeNode(problem, problem.initial_state)
    queue.append(root)

    while len(queue) > 0:
        next_node = queue.popleft()

        if next_node.goalp():
            # Return the path from the root to the goal node
            return next_node.path()

        # Generate new nodes and add them to the queue
        new_nodes = next_node.generate_new_tree_nodes()
        for new_node in new_nodes:
            queue.append(new_node)

    # Return None if no solution is found
    print('No solution')
    return None


# Define the examples
Example1 = (1, 2, 3, 4, 6, 0, 7, 5, 8)
Example2 = (2, 3, 0, 1, 5, 6, 4, 7, 8)
Example3 = (4, 1, 2, 7, 6, 3, 0, 5, 8)
Example4 = (4, 1, 2, 7, 6, 3, 5, 8, 0)
Example5 = (5, 3, 0, 4, 7, 6, 2, 1, 8)

# Solve and print the solutions for each example
for i, example in enumerate([Example1, Example2, Example3, Example4], start=1):
    problem = Puzzle8_Problem(example)
    output = breadth_first_search(problem)
    print(f'Solution Example {i}:')
    print_path(output)
    input("PRESS ENTER TO CONTINUE.")

# Solution to Example 5 may take too long to calculate using vanilla BFS
# problem = Puzzle8_Problem(Example5)
# output = breadth_first_search(problem)
# print('Solution Example 5:')
# print_path(output)

