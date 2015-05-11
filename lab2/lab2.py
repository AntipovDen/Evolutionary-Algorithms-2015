__author__ = 'Den'

#minimizing function f(x, y) = x^2 + y^2 on the sqare -5.12 <= x,y <= 5.12
#global minimum in x = y = 0

from random import randint, random, shuffle
from matplotlib import pyplot as plt
# from matplotlib import cm
# from mpl_toolkits.mplot3d import Axes3D
# from numpy import arange, meshgrid

#constants
tournamentProb = 0.75
crossingoverProb = 0.9
mutationProb = 0.01
border = 5.12
expansion = 0.5
populationSize = 50
nextGenSize = 40
iterations = 50

def f(x, y):
    return x ** 2 + y ** 2

def reduction(population):
    if len(population) == 2:
        return population
    shuffle(population)
    nextTour = []
    for i in range(len(population) // 2):
        if ((f(population[2 * i][0], population[2 * i][1]) < f(population[2 * i + 1][0], population[2 * i + 1][1])) != (random() < tournamentProb)):
            nextTour.append(population[2 * i + 1])
        else:
            nextTour.append(population[2 * i])
    if len(population) % 2 != 0:
        nextTour.append(population[-1])
    return reduction(nextTour)

def crossingover(parents):
    if random() > crossingoverProb:
        return parents
    par1, par2 = parents[0], parents[1]
    h1, h2 = [], []
    c1 = min(par1[0], par2[0])
    c2 = max(par1[0], par2[0])
    low, high = max(-border, c1 - expansion * (c2 - c1)), min(border, c2 + expansion * (c2 - c1))
    h1.append(low + random() * (high - low))
    h2.append(high + low - h1[0])

    c1 = min(par1[1], par2[1])
    c2 = max(par1[1], par2[1])
    low, high = max(-border, c1 - expansion * (c2 - c1)), min(border, c2 + expansion * (c2 - c1))
    h1.append(low + random() * (high - low))
    h2.append(high + low - h1[1])
    return [h1, h2]

def mutation(individual):
    if random() < mutationProb:
        individual[randint(0, 1)] = (random() - 0.5) * border
    return individual

def nextGen(population):
    newGen =  [mutation(i) for j in range(nextGenSize // 2) for i in crossingover(reduction(population))]
    tmp = [(f(j[0], j[1]), j) for j in population]
    tmp.sort()
    newGen += [i[1] for i in tmp[:(populationSize - nextGenSize)]]
    return newGen

population = [[(random() - 0.5) * border, (random() - 0.5) * 2 * border] for i in range(populationSize)]
x, y = [i[0] for i in population], [i[1] for i in population]
plt.plot(x, y, 'bo', [0], [0], 'rs')
plt.show()

for i in range(iterations):
    population = nextGen(population)
    # uncomment to see each generation
x, y = [i[0] for i in population], [i[1] for i in population]
plt.plot(x, y, 'bo', [0], [0], 'rs')
plt.show()


res = min([(f(i[0], i[1]), i) for i in population])
print("nearest point: ", res[1])
print("value: ", res[0])



#It's 3d plotting. But it's not visual.

# x = arange(-border, border, 0.1)
# y = arange(-border, border, 0.1)
# x, y = meshgrid(x, y)
# z = f(x, y)
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(x, y, z, cmap=cm.coolwarm, rstride=1, cstride=1, linewidth=0)
# bx = fig.add_subplot(111, projection='3d')
# ax.scatter([i[0] for i in population], [i[1] for i in population], [f(i[0], i[1]) for i in population], c='g')
# plt.show()
