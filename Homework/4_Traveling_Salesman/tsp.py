import itertools
import os
import random
import time
from math import sqrt

def dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def fitness(individual: list[int], places: list[tuple[float, float]]) -> float:
    return sum(dist(places[individual[i]], places[individual[i+1]]) for i in range(len(places) - 1))

def crossover(parent1: list[int], parent2: list[int]) -> tuple[list[int], list[int]]:
    size = len(parent1)

    l = random.randint(0, size - 1)
    r = random.randint(0, size - 1)
    l, r = min(l, r), max(l, r)

    child1: list[int] = [-1] * size
    child2: list[int] = [-1] * size

    child1[l:r+1] = parent1[l:r+1]
    child2[l:r+1] = parent2[l:r+1]
    child1_genes = set(child1)
    child2_genes = set(child2)

    parent1_ind = (r + 1) % size
    parent2_ind = (r + 1) % size
    for i in itertools.chain(range(r+1, size), range(l)):
        while parent2[parent2_ind] in child1_genes:
            parent2_ind = (parent2_ind + 1) % size

        child1[i] = parent2[parent2_ind]
        child1_genes.add(parent2[parent2_ind])

        while parent1[parent1_ind] in child2_genes:
            parent1_ind = (parent1_ind + 1) % size

        child2[i] = parent1[parent1_ind]
        child2_genes.add(parent1[parent1_ind])

    return child1, child2

def swap_mutate(individual: list[int]) -> None:
    i, j = sorted(random.sample(range(len(individual)), 2))
    individual[i], individual[j] = individual[j], individual[i]

def reverse_mutate(individual: list[int]) -> None:
    l, r = sorted(random.sample(range(len(individual)), 2))
    individual[l:r+1] = reversed(individual[l:r+1])

def solve_tsp(n: int, places: list[tuple[float, float]], printed: list, generations: int = 10) -> list[int]:
    Population_size = 10000
    Truncated_population = Population_size // 10
    Elitists = 1000 #even pls
    Chernobyl_rate = 0.5

    population: list[list[int]] = []

    for _ in range(Population_size):
        individual = list(range(n))
        random.shuffle(individual)
        population.append(individual)
        
    scores: list[float] = [fitness(ind, places) for ind in population]
    printed.append(min(scores))

    for _ in range(generations - 1):
        #Truncated selection
        parents: list[list[int]] = [
            ind 
            for _, ind in sorted(enumerate(population), key=lambda x: scores[x[0]])[:Truncated_population]
        ]

        population[:Elitists] = parents[:Elitists]

        for i in range(Elitists, Population_size, 2):
            parent1, parent2 = random.sample(range(Truncated_population), 2)
            population[i], population[i+1] = crossover(parents[parent1], parents[parent2])

            chernobyl = random.random()
            if chernobyl < Chernobyl_rate:
                reverse_mutate(population[i])

            chernobyl = random.random()
            if chernobyl < Chernobyl_rate:
                reverse_mutate(population[i+1])

        scores = [fitness(ind, places) for ind in population]
        printed.append(min(scores))

    return sorted(enumerate(population), key=lambda x: scores[x[0]])[0][1]
    

def main():
    data = input()
    named = False

    places: list[tuple[float, float]] = []

    try:
        n = int(data)

        for _ in range(n):
            x = random.random() * 1000 - 500
            y = random.random() * 1000 - 500
            places.append((x, y))
    except ValueError:
        named = True
        n = int(input())
        names: list[str] = []

        for _ in range(n):
            name, x, y = input().split()
            names.append(name)
            places.append((float(x), float(y)))

    printed = []
    start: float = time.perf_counter()
    order = solve_tsp(n, places, printed)

    length: float = (time.perf_counter() - start) * 1000
    print(f"# TIMES_MS: alg={length}")

    time_only = os.getenv("FMI_TIME_ONLY")
    if not time_only or time_only != "1":
        [print(x) for x in printed]
        print()

        if named:
            print(" -> ".join([names[i] for i in order]))

        print(printed[-1])


if __name__ == "__main__":
    main()