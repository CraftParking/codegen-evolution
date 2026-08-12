def score(tree, examples):
    total_error = 0.0
    for x, expected in examples:
        try:
            actual = tree.evaluate(x)
        except (OverflowError, ZeroDivisionError):
            return float("inf")
        if not isinstance(actual, (int, float)) or actual != actual:
            return float("inf")
        total_error += (actual - expected) ** 2
    return total_error / len(examples)
