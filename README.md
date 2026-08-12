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

A second sandbox: evolve stick-figure creatures (four fixed-length legs,
each with a thigh + shin joint) in a 2D physics simulation scored purely on
distance traveled. The torso can't rotate — it only translates — so all
locomotion has to come from the legs pushing against the ground. A ceiling
above the arena hard-caps how high anything can jump, so evolved hoppers
stay within the visible window, and the simulation stops early once a
creature is no longer making forward progress (whatever it's doing with its
legs at that point isn't being selected on, so there's no point watching it).

This is **neuroevolution**: each leg is driven by the same tiny neural
network (7 inputs — a time signal plus that leg's own joint angles/velocities
— through a hidden layer to 2 motor outputs), and the genome *is* that
network's weights (82 numbers). Nobody designs the gait or the control
logic; evolution shapes the network from scratch via mutation + crossover
on its weights, the same GA machinery as the rest of this repo.

```
pip install -r requirements.txt
python -m examples.walking_creatures
```

It evolves forever, printing distance each time it improves — press
Ctrl+C whenever you've seen enough, and it opens a window showing the best
creature found so far in action. Fitness evaluation runs in parallel across
all CPU cores while evolving (each genome's physics sim is independent), so
generations fly by; playback afterward is a separate, single-process,
real-time loop and isn't affected by that. Needs `pymunk` (physics) and
`pygame-ce` (rendering) — installed via `requirements.txt`.

- `creatures/brain.py` — the shared per-leg neural network (forward pass only)
- `creatures/genome.py` — the genome is just the network's flat weight vector
- `creatures/body.py` — builds a torso + two-segment legs in a pymunk physics space
- `creatures/simulate.py` — runs the network each step, scores distance, detects when it's stuck
- `creatures/evolve_creatures.py` — the generation loop
