# codegen-evolution

Genetic programming sandbox — evolves small arithmetic expression trees against
a fitness function until one solves the task, no gradient descent involved.

Programs are trees built from `+ - * /` and the variable `x`. Each generation:
score every tree against a set of examples, keep the best, breed the rest via
tournament selection + subtree crossover, then mutate.

## Run the example

```
python -m examples.square_plus_one
```

This evolves a random population toward `x^2 + 1` and prints the best
expression whenever fitness improves, e.g.:

```
gen 0:  fitness 1.00000   (x * x)
gen 5:  fitness 0.02170   ((x * x) - (3.01 / -3.53))
gen 11: fitness 0.00122   ((x * x) - (-4.42 / 4.58))
```

## Layout

- `genepool/node.py` — expression tree representation
- `genepool/generate.py` — random tree generation
- `genepool/fitness.py` — scores a tree against input/output examples
- `genepool/mutate.py` — random subtree replacement
- `genepool/crossover.py` — subtree swap between two parents
- `genepool/evolve.py` — the generation loop
- `examples/` — target problems to evolve toward
