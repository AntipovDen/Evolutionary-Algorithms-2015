__author__ = 'dantipov'

from math import sin, cos, exp, isnan, isfinite
from random import random, randint
from time import time
from numpy import sum

x = [0] * 9
nan = float('nan')
inf = float('inf')


def plus(x1, x2):
    return x1 + x2


def minus(x1, x2):
    return x1 - x2


def mul(x1, x2):
    return x1 * x2


def div(x1, x2):
    if x2 == nan or x2 == 0: return nan
    return x1 / x2


def power(x1, x2):
    if x1 < 0 and x2 // 1 != x2 or x1 == 0 and x2 < 0: return nan
    return x1 ** x2


def myCos(x1):
    if x1 in [inf, -inf]: return nan
    return cos(x1)


def mySin(x1):
    if x1 in [inf, -inf]: return nan
    return sin(x1)


functions = [plus, minus, mul, div, abs, mySin, myCos, exp, power]
twoArgFunctions = [plus, minus, mul, div, power]
oneArgFunctions = [abs, mySin, myCos, exp]
zeroArgFunctions = ['var', 'const']

maxDepth = 7

# constants
crossingoverProb = 0.9
mutationProb = 0.01
populationSize = 250
nextGenSize = 200
iterations = 100
# population format: [(fitness(p), p) for i in range(populationSize)]


class node:
    def __init__(self, function, children, parent=0):
        self.function = function
        self.children = children
        self.parent = parent

    def __cmp__(self, other):
        return 0

    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __le__(self, other):
        return True

    def __ge__(self, other):
        return True

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
            except OverflowError:
                return inf

        elif self.function in twoArgFunctions:
            try:
                return self.function(self.children[0].calc(), self.children[1].calc())
            except OverflowError:
                return inf

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

    def copy(self, parent=0):
        n = node(self.function, self.children, parent)
        if self.function in oneArgFunctions:
            n.children = self.children.copy(n)
        elif self.function in twoArgFunctions:
            n.children[0] = self.children[0].copy(n)
            n.children[1] = self.children[1].copy(n)
        return n

    def cut(self, depth=0):
        if depth != maxDepth:
            if self.function in oneArgFunctions:
                self.children.cut(depth + 1)
            if self.function in twoArgFunctions:
                self.children[0].cut(depth + 1)
                self.children[1].cut(depth + 1)
        elif self.function in functions:
            if random() < 0.1:  #const
                self.function = 'const'
                children = randint(1, 9)
            else:  #var
                self.function = 'var'
                children = randint(0, 8)


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
                res = node(f, genTree(depth + 1))
                res.children.parent = res
                return res
            else:
                res = node(f, [genTree(depth + 1), genTree(depth + 1)])
                res.children[0].parent = res
                res.children[1].parent = res
                return res


def crossingover(trees):
    t1, t2 = trees[0].copy(), trees[1].copy()
    # if (random() > crossingoverProb):
    #     return t1, t2

    n1, n2 = t1.selectNode(), t2.selectNode()
    # print()
    # n1.print()
    # print(n1.parent)
    # n2.print()
    # print(n2.parent)

    if n1.parent != 0:
        if n1.parent.function in oneArgFunctions:
            n1.parent.children = n2
        elif n1.parent.children[0] == n1:
            n1.parent.children[0] = n2
        else:
            n1.parent.children[1] = n2
    else:
        t1 = n2

    if n2.parent != 0:
        if n2.parent.function in oneArgFunctions:
            n2.parent.children = n1
        elif n2.parent.children[0] == n2:
            n2.parent.children[0] = n1
        else:
            n2.parent.children[1] = n1
    else:
        t2 = n1

    n1.parent, n2.parent = n2.parent, n1.parent
    t1.cut()
    t2.cut()

    return t1, t2


def mutation(tree):
    # if random() < mutationProb:
    n = tree.selectNode()
    if n.parent != 0:
        p = n.parent
        if p.function in oneArgFunctions:
            p.children = genTree(3)
            p.children.parent = p
        elif p.children[0] == 2:
            p.children[0] = genTree(3)
            p.children[0].parent = p
        else:
            p.children[1] = genTree(3)
            p.children[1].parent = p


def targetFunction():
    return sum([(i + 1) * x[i] for i in range(9)])


testingSet = 200


def fitness(tree):
    #   start_time = time()
    global x
    res = 0
    # for x1 in range(-5, 6, 5):
    #     print('x1 =', x1)
    #     for x2 in range(-5, 6, 5):
    #         for x3 in range(-5, 6, 5):
    #             for x4 in range(-5, 6, 5):
    #                 for x5 in range(-5, 6, 5):
    #                     for x6 in range(-5, 6, 5):
    #                         for x7 in range(-5, 6, 5):
    #                             for x8 in range(-5, 6, 5):
    #                                 for x9 in range(-5, 6, 5):
    #                                     x = [x1, x2, x3, x4, x5, x6, x7, x8, x9]
    #                                     res += (tree.calc() - targetFunction()) ** 2
    for i in range(testingSet):
        x = [random() * 10.24 - 5.12 for j in range(9)]
        try:
            res += (tree.calc() - targetFunction()) ** 2
        except Exception:
            # tree.print()
            print('Exception')

            #   print('fitness calculated in', time() - start_time, 'sec')
    return res / testingSet


def reduction(population):
    distribution = [1 / p[0] for p in population if not isnan(p[0]) and isfinite(p[0])]

    for i in range(1, len(distribution)):
        distribution[i] += distribution[i - 1]
    result = random() * distribution[-1]

    par1 = population[min([i for i in range(len(distribution)) if distribution[i] > result])][1]

    result = random() * distribution[-1]
    par2 = population[min([i for i in range(len(distribution)) if distribution[i] > result])][1]
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

# p1, p2 = reduction(population)
# p1.print()
# print()
# mutation(p1)
# p1.print()
# exit(0)
print('generated')

for i in range(iterations):
    print('iteration', i)
    if i % 10 == 0:
        population.sort()
        population[0][1].print()
    population = nextGen(population)

population.sort()
for p in population[:10]:
    p[1].print()