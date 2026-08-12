import random

from creatures.brain import GENOME_LENGTH

NUM_LEGS = 4
WEIGHT_RANGE = (-2.0, 2.0)


def random_genome():
    lo, hi = WEIGHT_RANGE
    return [random.uniform(lo, hi) for _ in range(GENOME_LENGTH)]


def mutate(genome, rate=0.2, sigma=0.4):
    lo, hi = WEIGHT_RANGE
    return [
        min(hi, max(lo, w + random.gauss(0, sigma))) if random.random() < rate else w
        for w in genome
    ]


def crossover(genome_a, genome_b):
    return [random.choice([wa, wb]) for wa, wb in zip(genome_a, genome_b)]
