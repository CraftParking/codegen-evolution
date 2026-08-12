import random

from genepool.crossover import crossover
from genepool.fitness import score
from genepool.generate import random_population
from genepool.mutate import mutate


def tournament_select(population, fitnesses, k=3):
    contenders = random.sample(list(zip(population, fitnesses)), k)
    return min(contenders, key=lambda pair: pair[1])[0]


def run(examples, population_size=200, generations=100, max_depth=4):
    population = random_population(population_size, max_depth)
    best, best_fitness = None, float("inf")

    for gen in range(generations):
        fitnesses = [score(tree, examples) for tree in population]

        gen_best_idx = min(range(len(population)), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] < best_fitness:
            best, best_fitness = population[gen_best_idx], fitnesses[gen_best_idx]
            print(f"gen {gen}: fitness {best_fitness:.5f}  {best.to_str()}")

        if best_fitness == 0:
            break

        next_population = [best]
        while len(next_population) < population_size:
            parent_a = tournament_select(population, fitnesses)
            parent_b = tournament_select(population, fitnesses)
            child = crossover(parent_a, parent_b)
            child = mutate(child, max_depth=max_depth)
            next_population.append(child)

        population = next_population

    return best, best_fitness
