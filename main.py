from typing import List, Tuple
from random import random, randint
from itertools import permutations
from time import time


class Knapsack:
    def __init__(self, n: int, b: int, sw: List[Tuple[int, int]]):
        self.n = n
        self.b = b
        self.sw = sw

    def heuristicHelp(self, key):
        ret: list = []
        sw = self.sw.copy()
        sw.sort(key=key, reverse=True)
        sumb = 0
        for e in sw:
            if sumb + e[0] <= self.b:
                ret.append(e)
                sumb += e[0]
        return sum(map(lambda x: x[1], ret))

    def heuristicRandom(self):
        return self.heuristicHelp(lambda x: random())

    def heuristicMaxW(self):
        return self.heuristicHelp(lambda x: x[1])

    def heuristicMinS(self):
        return self.heuristicHelp(lambda x: -x[0])

    def heuristicMaxWoS(self):
        return self.heuristicHelp(lambda x: x[1] / x[0])

    def bruteforce(self):
        bestW = 0
        bestC = []
        for i in range(1, self.n + 1):
            for p in permutations(self.sw, i):
                a = sum(map(lambda x: x[1], p))
                b = sum(map(lambda x: x[0], p))
                if a > bestW and b <= self.b:
                    bestW = a
                    bestC = p
        return bestC

    def restrictedBruteforce(self):
        maxW = 0
        bestC = []

        for p in permutations(self.sw):
            partSumB, partSumW, partRet = 0, 0, []
            for n in p:
                if partSumB + n[0] > self.b:
                    break
                partSumB += n[0]
                partSumW += n[1]
                partRet.append(n)
            if partSumW > maxW:
                bestC = partRet
                maxW = partSumW
        return bestC

    def dynamicProgramming(self):
        matrix = [[0] * (self.b + 1) for _ in range(self.n + 1)]
        for items in range(1, len(matrix)):
            for volume in range(1, len(matrix[items])):
                if volume >= self.sw[items - 1][0]:
                    matrix[items][volume] = max(
                        self.sw[items - 1][1] + matrix[items - 1][volume - self.sw[items - 1][0]],
                        matrix[items - 1][volume])
                else:
                    matrix[items][volume] = matrix[items - 1][volume]
        return matrix[-1][-1]
        # resultsM = []
        # ind = self.n
        # hp = self.b
        # while ind > 0:
        #     if matrix[ind][hp] != matrix[ind - 1][hp]:
        #         resultsM.append(1)
        #         ind -= 1
        #         while matrix[ind][hp]: hp -= 1
        #         hp += 1
        #     else:
        #         resultsM.append(0)
        #         ind -= 1
        #
        # ret, x = [], 0
        # for i in resultsM[::-1]:
        #     if i: ret.append(self.sw[x])
        #     x += 1
        # return ret


def generateKnapsack(n: int, v : float):
    sw = [(randint(10, 1000), randint(100, 10000)) for _ in range(n)]
    b = int(sum(map(lambda x: x[0], sw)) * v)
    return Knapsack(n, b, sw)


if __name__ == "__main__":
    func = [Knapsack.dynamicProgramming, Knapsack.heuristicRandom, Knapsack.heuristicMinS, Knapsack.heuristicMaxW,
            Knapsack.heuristicMaxWoS]
    print(tuple(f.__name__ for f in func))
    for b in (0.25, 0.5, 0.75):
        for n in range(20, 220, 20):
            for i in range(10):
                k = generateKnapsack(n, b)
                func = [k.dynamicProgramming, k.heuristicRandom, k.heuristicMinS, k.heuristicMaxW, k.heuristicMaxWoS]
                print("{}, {}".format(n, b), end=', ')
                for f in func:
                    print(f(), end=', ')
                print()

