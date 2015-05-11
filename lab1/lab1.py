__author__ = 'dantipov'

from math import cos, sin, log, e
from numpy import sum
from random import random, randint
from matplotlib import pyplot as plt

precision = 10 #individual length == precision + 1

def f(x):
    return cos(e ** x) / sin(log(x))

def indToArg(individual):
    return sum([individual[i] * 2 ** i for i in range(precision + 1 )]) / 2 ** precision + 2

def argToInd(arg):
    individual = []
    x = int((arg - 2) * 2 ** precision)
    for i in range(precision + 1):
        individual.append(x % 2)
        x = x // 2

#parameters of algorithm
populationSize = 50
nextGenSize = 40
mutProb = 0.9
tournamentProb = 0.6
iterations = 50


def tournament(population):
    if len(population) == 2:
        return population
    next_tour = []
    for i in range(len(population) // 2):
        if f(indToArg(population[i * 2])) <= f(indToArg(population[i * 2 + 1])):
            if random() <= tournamentProb:
                next_tour.append(population[i * 2])
            else:
                next_tour.append(population[i * 2 + 1])
        else:
            if random() <= tournamentProb:
                next_tour.append(population[i * 2 + 1])
            else:
                next_tour.append(population[i * 2])
    if len(population) % 2 != 0:
        next_tour.append(population[-1])
    return tournament(next_tour)

def cross(population):
    next_gen = []
    for j in range(nextGenSize // 2):
        p1, p2 = tournament(population)
        k = randint(0, precision + 1)
        c1, c2 = [], []
        for i in range(k):
            c1.append(p1[i])
            c2.append(p2[i])
        for i in range(k, precision + 1):
            c1.append(p2[i])
            c2.append(p1[i])
        next_gen.append(c1)
        next_gen.append(c2)
    return next_gen

def mutate(population):
    for individual in population:
        k = randint(1, precision)
        individual[k] = 1 - individual[k]
    return population

def select(population):
     sorting_pop = [(f(indToArg(i)), i) for i in population]
     sorting_pop.sort()
     return [sorting_pop[i][1] for i in range(populationSize - nextGenSize)]

def showPopulation(population):
    x = [i / 100 for i in range(200, 400)]
    y = [f(i/100) for i in range(200, 400)]

    x1 = [indToArg(i) for i in population]
    y1 = [f(i) for i in x1]

    plt.plot(x1, [0] * len(x1), 'bo', x, y, 'b-', x1, y1, 'ro')
    plt.show()

def evoRun():
    population = [[randint(0, 1) for i in range(precision + 1)] for j in range(populationSize)]
    showPopulation(population)
    for i in range(iterations):
        population = mutate(cross(population)) + select(population)
        if i % 10 == 0:
            print(i)
            # showPopulation(population)
    showPopulation(population)

evoRun()