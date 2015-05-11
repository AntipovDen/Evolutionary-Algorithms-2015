__author__ = 'Den'


from random import randint, random, shuffle
from math import sqrt
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from numpy import arange, meshgrid, sum
from time import time

#constants
numberOfCities = 29
crossingoverProb = 0.9
mutationProb = 0.01
populationSize = 50
nextGenSize = 40
iterations = 10000

#reading cities coordinates
coord = [[float(i) for i in s.split(' ')] for s in open('cities.in', 'r').readlines()]
dist = [[sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) for c1 in coord] for c2 in coord]

def pathLen(path):
    return sum([dist[path[i]][path[i + 1]] for i in range(numberOfCities - 1)]) + dist[path[-1]][path[0]]

def reduction(population):
    lens = [pathLen(i) for i in population]
    lens = [sum(lens[:i + 1]) for i in range(populationSize)]
    result = random() * lens[-1]
    par1 = population[min([i for i in range(populationSize) if lens[i] > result])]
    result = random() * lens[-1]
    par2 = population[min([i for i in range(populationSize) if lens[i] > result])]
    return par1, par2

crossNumber = 0

def crossingoverPMX(parents):
    if random() > crossingoverProb:
        return parents
    par1, par2 = parents
    c1, c2 = [0]*numberOfCities, [0]*numberOfCities
    replace1, replace2 = [i for i in range(numberOfCities)], [i for i in range(numberOfCities)]
    start, end = randint(0, numberOfCities - 1), randint(0, numberOfCities - 1)
    if start > end:
        start, end = end, start
    for i in range(start, end + 1):
        replace1[par2[i]], replace2[par1[i]] = par1[i], par2[i]
    for i in range(start, end + 1):
        c1[i], c2[i] = par2[i], par1[i]
    for i in [j for j in range(start)] + [j for j in range(end + 1, numberOfCities)]:
        c1[i], c2[i] = par1[i], par2[i]
        while replace1[c1[i]] != c1[i]:
            c1[i] = replace1[c1[i]]
        while replace2[c2[i]] != c2[i]:
            c2[i] = replace2[c2[i]]
    return c1, c2

def crossingoverOX(parents):

    if random() > crossingoverProb:
        return parents
    par1, par2 = parents
    c1, c2 = [0]*numberOfCities, [0]*numberOfCities

    start, end = randint(0, numberOfCities - 1), randint(0, numberOfCities - 1)
    if start > end:
        start, end = end, start

    for i in range(start, end + 1):
        c1[i], c2[i] = par2[i], par1[i]

    j = end + 1 - numberOfCities
    for i in range(end + 1 - numberOfCities, start):
        while par1[j] in par2[start:end + 1]:
            j += 1
        c1[i] = par1[j]
        j += 1

    j = end + 1 - numberOfCities
    for i in range(end + 1 - numberOfCities, start):
        while par2[j] in par1[start:end + 1]:
            j += 1
        c2[i] = par2[j]
        j += 1

    return c1, c2

def mutation(individual):
    #there is no mutation in this problem
    if random() < mutationProb:
        i, j = randint(0, numberOfCities - 1), randint(0, numberOfCities - 1)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def nextGen(population):
    newGen =  [mutation(i) for j in range(nextGenSize // 2) for i in crossingoverOX(reduction(population))]
    tmp = [(pathLen(j), j) for j in population]
    tmp.sort()
    newGen += [i[1] for i in tmp[:(populationSize - nextGenSize)]]
    return newGen

def genPath():
    order = [randint(0, numberOfCities - 1 - i) for i in range(numberOfCities)]
    listOfCities = [i for i in range(numberOfCities)]
    path = []
    for i in order:
        path.append(listOfCities[i])
        listOfCities.remove(listOfCities[i])
    return path


# #testing crossover
# parents = [genPath(), genPath()]
# children = crossingoverOX(parents)
# print("parents:")
# print(parents[0])
# print(parents[1])
# print("children:")
# print(children[0])
# print(children[1])
#
# children[0].sort()
# children[1].sort()
#
# print()
# print()
# print("sortedchildren:")
# print(children[0])
# print(children[1])
# exit(0)


population = [genPath() for i in range(populationSize)]
for i in range(iterations):
    population = nextGen(population)

result = min([(pathLen(i), i) for i in population])
print(result[0])
x = [coord[i][0] for i in result[1] + [result[1][0]]]
y = [coord[i][1] for i in result[1] + [result[1][0]]]
plt.plot(x, y, 'b-')
plt.show()