import random

from creatures.genome import crossover, mutate, random_genome
from creatures.simulate import evaluate


def tournament_select(population, fitnesses, k=3):
    contenders = random.sample(list(zip(population, fitnesses)), k)
    return max(contenders, key=lambda pair: pair[1])[0]


def run(population_size=40, generations=30, sim_time=6.0):
    population = [random_genome() for _ in range(population_size)]
    best, best_distance = None, float("-inf")

    for gen in range(generations):
        distances = [evaluate(genome, sim_time=sim_time) for genome in population]

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

    return best, best_distance
