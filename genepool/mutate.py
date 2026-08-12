import random

from genepool.generate import random_tree


def mutate(tree, max_depth=3, rate=0.1):
    tree = tree.copy()
    for node in tree.nodes():
        if random.random() < rate:
            replacement = random_tree(max_depth)
            node.value = replacement.value
            node.children = replacement.children
    return tree
