import random


def crossover(parent_a, parent_b):
    child = parent_a.copy()
    donor = parent_b.copy()

    child_node = random.choice(child.nodes())
    donor_node = random.choice(donor.nodes())

    child_node.value = donor_node.value
    child_node.children = donor_node.children
    return child
