import random

OPERATORS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b if abs(b) > 1e-9 else 1.0,
}

TERMINALS = ["x", "const"]


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def is_leaf(self):
        return not self.children

    def evaluate(self, x):
        if self.value == "x":
            return x
        if self.value in OPERATORS:
            a = self.children[0].evaluate(x)
            b = self.children[1].evaluate(x)
            return OPERATORS[self.value](a, b)
        return self.value

    def to_str(self):
        if self.is_leaf():
            return str(self.value)
        left = self.children[0].to_str()
        right = self.children[1].to_str()
        return f"({left} {self.value} {right})"

    def copy(self):
        return Node(self.value, [c.copy() for c in self.children])

    def nodes(self):
        result = [self]
        for child in self.children:
            result.extend(child.nodes())
        return result

    @staticmethod
    def random_constant():
        return Node(round(random.uniform(-5, 5), 2))
