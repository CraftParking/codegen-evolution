import random

from genepool.node import OPERATORS, Node


def random_terminal():
    if random.random() < 0.5:
        return Node("x")
    return Node.random_constant()


def random_tree(max_depth, depth=0):
    if depth >= max_depth or (depth > 0 and random.random() < 0.3):
        return random_terminal()
    op = random.choice(list(OPERATORS.keys()))
    left = random_tree(max_depth, depth + 1)
    right = random_tree(max_depth, depth + 1)
    return Node(op, [left, right])


def random_population(size, max_depth):
    return [random_tree(max_depth) for _ in range(size)]
