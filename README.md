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
each with a thigh + shin joint) driven by sine-wave "muscle" motors, in a
2D physics simulation scored purely on distance traveled. The torso can't
rotate — it only translates — so all locomotion has to come from the legs
pushing against the ground. A ceiling above the arena hard-caps how high
anything can jump, so evolved hoppers stay within the visible window.
Nobody designs the gait; evolution only tunes each hip and knee motor's
amplitude/frequency/phase to find a stride that works.

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

- `creatures/genome.py` — per-leg genes: hip and knee motor amplitude/frequency/phase
- `creatures/body.py` — builds a torso + two-segment legs in a pymunk physics space
- `creatures/simulate.py` — drives the motors and scores distance traveled
- `creatures/evolve_creatures.py` — the generation loop
