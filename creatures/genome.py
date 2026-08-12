import copy
import math
import random

NUM_LEGS = 4

GENE_RANGES = {
    "length": (20.0, 60.0),
    "amplitude": (0.5, 3.0),
    "frequency": (0.5, 2.5),
    "phase": (0.0, 2 * math.pi),
}


def _random_leg():
    return {name: random.uniform(lo, hi) for name, (lo, hi) in GENE_RANGES.items()}


def random_genome():
    return [_random_leg() for _ in range(NUM_LEGS)]


def mutate(genome, rate=0.3):
    genome = copy.deepcopy(genome)
    for leg in genome:
        for name, (lo, hi) in GENE_RANGES.items():
            if random.random() < rate:
                span = hi - lo
                leg[name] = min(hi, max(lo, leg[name] + random.gauss(0, span * 0.15)))
    return genome


def crossover(genome_a, genome_b):
    return [
        copy.deepcopy(random.choice([leg_a, leg_b]))
        for leg_a, leg_b in zip(genome_a, genome_b)
    ]
