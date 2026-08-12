from genepool.evolve import run

TARGET = lambda x: x * x + 1

if __name__ == "__main__":
    examples = [(x, TARGET(x)) for x in range(-10, 11)]
    best, fitness = run(examples)
    print()
    print(f"best found: {best.to_str()}  (fitness {fitness:.5f})")
