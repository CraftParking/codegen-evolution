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

## Walking creatures

A second sandbox: evolve stick-figure creatures (four fixed-length legs
driven by sine-wave "muscle" motors) in a 2D physics simulation, scored
purely on distance traveled. The torso can't rotate — it only translates —
so all locomotion has to come from the legs pushing against the ground.
Nobody designs the gait; evolution only tunes each leg's motor
amplitude/frequency/phase to find a timing pattern that works.

```
pip install -r requirements.txt
python -m examples.walking_creatures
```

It evolves a population for a bit (prints distance each time it improves),
then opens a window showing the winning creature in action. Needs
`pymunk` (physics) and `pygame-ce` (rendering) — installed via
`requirements.txt`.

- `creatures/genome.py` — per-leg genes: motor amplitude/frequency/phase
- `creatures/body.py` — builds a torso + legs in a pymunk physics space
- `creatures/simulate.py` — drives the motors and scores distance traveled
- `creatures/evolve_creatures.py` — the generation loop
