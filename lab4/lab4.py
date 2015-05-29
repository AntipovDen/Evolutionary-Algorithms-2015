__author__ = 'dantipov'

from math import sin, cos, exp
from random import random, randint
from time import time

x = [0] * 9


def plus(x1, x2):
    return x1 + x2


def minus(x1, x2):
    return x1 - x2


def mul(x1, x2):
    return x1 * x2


def div(x1, x2):
    if x2 == 0: return float('nan')
    return x1 / x2


def pow(x1, x2):
    return x1 ** x2


functions = [plus, minus, mul, div, abs, sin, cos, exp, pow]
twoArgFunctions = [plus, minus, mul, div, pow]
oneArgFunctions = [abs, sin, cos, exp]
zeroArgFunctions = ['var', 'const']

maxDepth = 15

# constants
crossingoverProb = 0.9
mutationProb = 0.01
populationSize = 50
nextGenSize = 40
iterations = 100
#population format: [(fitness(p), p) for i in range(populationSize)]


class node:
    def __init__(self, function, children, parent=0):
        self.function = function
        self.children = children
        self.parent = parent


    def setChildrensParents(self):
        if self.function in oneArgFunctions:
            self.children.parent = self
        elif self.function in twoArgFunctions:
            self.children[0].parent = self
            self.children[1].parent = self

    def calc(self):
        if self.function in oneArgFunctions:
            try:
                return self.function(self.children.calc())
            except TypeError or OverflowError:
                print(self.function.__name__)
                self.print()
                print(self.children.calc())
                exit(0)
        elif self.function in twoArgFunctions:
            try:
                return self.function(self.children[0].calc(), self.children[1].calc())
            except TypeError or OverflowError:
                print(self.function.__name__)
                self.print()
                print(self.children[0].calc())
                print(self.children[1].calc())
                exit(0)
        elif self.function in zeroArgFunctions:
            if self.function == 'var':
                return x[self.children]
            else:
                return self.children

    def selectNode(self):
        if self.function in zeroArgFunctions:
            return self
        elif self.function in oneArgFunctions:
            if random() < 0.3:
                return self
            else:
                return self.children.selectNode()
        else:
            if random() < 0.3:
                return self
            elif random() < 0.5:
                return self.children[0].selectNode()
            else:
                return self.children[1].selectNode()

    def print(self):
        if self.function in oneArgFunctions:
            print('[.', self.function.__name__, end=' ', sep='')
            self.children.print()
            print(']', end=' ')
        elif self.function in twoArgFunctions:
            print('[.', self.function.__name__, end=' ', sep='')
            self.children[0].print()
            self.children[1].print()
            print(']', end=' ')
        elif self.function == 'var':
            print('x', self.children, end=' ', sep='')
        else:
            print(self.children, end=' ')

    def copy(self, parent = 0):
        n = node(self.function, self.children, self.parent)
        if self.function in oneArgFunctions:
            n.children = self.children.copy(n)
        elif self.function in twoArgFunctions:
            n.children[0] = self.children[0].copy(n)
            n.children[1] = self.children[1].copy(n)
        return n



def genTree(depth):
    if maxDepth == depth:
        if random() < 0.1:
            return node('const', randint(1, 9))
        else:
            return node('var', randint(0, 8))
    else:
        r = random()
        if r < 0.02:
            return node('const', randint(1, 9))
        elif r < 0.2:
            return node('var', randint(0, 8))
        else:
            f = functions[randint(0, 8)]
            if f in oneArgFunctions:
                return node(f, genTree(depth + 1))
            else:
                return node(f, [genTree(depth + 1), genTree(depth + 1)])


def crossingover(trees):
    t1, t2 = trees[0].copy(), trees[1].copy()
    if (random() > crossingoverProb):
        return t1, t2
    n1, n2 = t1.selectNode(), t2.selectNode()
    if n1.parent != 0:
        p1 = n1.parent
        if p1.function in oneArgFunctions:
            p1.children = n2
        elif p1.children[0] == n1:
            p1.children[0] = n2
        else:
            p1.children[1] = n2
    else:
        t1 = n2

    if n2.parent != 0:
        p2 = n2.parent
        if p2.function in oneArgFunctions:
            p2.children = n1
        elif p2.children[0] == n2:
            p2.children[0] = n1
        else:
            p2.children[1] = n1
    else:
        t2 = n1

    return t1, t2


def mutation(tree):
    if random() < mutationProb:
        n = tree.selectNode()
        if n.parent != 0:
            p = n.parent
            if p.function in oneArgFunctions:
                p.children = genTree(3)
            elif p.children[0] == 2:
                p.children[0] = genTree(3)
            else:
                p.children[1] = genTree(3)


def targetFunction():
    sum([(i + 1) * x[i] for i in range(9)])


def fitness(tree):
    start_time = time()
    global x
    res = 0
    for x1 in range(-5, 6):
        for x2 in range(-5, 6):
            for x3 in range(-5, 6):
                for x4 in range(-5, 6):
                    for x5 in range(-5, 6):
                        for x6 in range(-5, 6):
                            for x7 in range(-5, 6):
                                for x8 in range(-5, 6):
                                    for x9 in range(-5, 6):
                                        x = [x1, x2, x3, x4, x5, x6, x7, x8, x9]
                                        res += (tree.calc() - targetFunction()) ** 2

    print('fitness calculated in', time() - start_time, 'sec')
    return res / 10 ** 9





def reduction(population):
    distribution = [max(p[0], 0) for p in population]
    for i in range(1, populationSize):
        distribution[i] += distribution[i - 1]
    result = random() * distribution[-1]
    par1 = population[min([i for i in range(populationSize) if distribution[i] > result])]
    result = random() * distribution[-1]
    par2 = population[min([i for i in range(populationSize) if distribution[i] > result])]
    return par1, par2

def nextGen(population):
    next_gen = [0] * populationSize
    for i in range(nextGenSize // 2):
        next_gen[2 * i], next_gen[2 * i + 1] = crossingover(reduction(population))
        mutation(next_gen[2 * i])
        mutation(next_gen[2 * i + 1])
        next_gen[2 * i] = (fitness(next_gen[2 * i]), next_gen[2 * i])
        next_gen[2 * i + 1] = (fitness(next_gen[2 * i + 1]), next_gen[2 * i + 1])
    population.sort()
    for i in range(populationSize - nextGenSize):
        next_gen[i + nextGenSize] = population[i]
    return next_gen



population = [genTree(0) for i in range(populationSize)]
population = [(fitness(i), i) for i in population]
print('generated')
for i in iterations:
    population = nextGen(population)

population.sort()
population[0][1].print()