import itertools
import os
import random
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from creatures.genome import crossover, mutate, random_genome
from creatures.simulate import evaluate


def tournament_select(population, fitnesses, k=3):
    contenders = random.sample(list(zip(population, fitnesses)), k)
    return max(contenders, key=lambda pair: pair[1])[0]


def run(population_size=40, generations=None, sim_time=6.0, workers=None):
    """generations=None runs forever; press Ctrl+C to stop and get the best so far.

    Each genome's physics simulation is independent, so fitness evaluation
    runs in parallel across CPU cores (workers, default: all of them) to get
    through generations as fast as possible. Playback via render() is a
    separate, single-process, real-time loop and is unaffected by this.
    """
    population = [random_genome() for _ in range(population_size)]
    best, best_distance = None, float("-inf")

    gen_iter = range(generations) if generations is not None else itertools.count()
    evaluate_genome = partial(evaluate, sim_time=sim_time)

    with ProcessPoolExecutor(max_workers=workers or os.cpu_count()) as pool:
        try:
            for gen in gen_iter:
                distances = list(pool.map(evaluate_genome, population))

                gen_best_idx = max(range(len(population)), key=lambda i: distances[i])
                if distances[gen_best_idx] > best_distance:
                    best, best_distance = population[gen_best_idx], distances[gen_best_idx]
                    print(f"gen {gen}: distance {best_distance:.1f}")

                next_population = [best]
                while len(next_population) < population_size:
                    parent_a = tournament_select(population, distances)
                    parent_b = tournament_select(population, distances)
                    child = crossover(parent_a, parent_b)
                    child = mutate(child)
                    next_population.append(child)

                population = next_population
        except KeyboardInterrupt:
            print("\nstopped - showing best so far")

    return best, best_distance
