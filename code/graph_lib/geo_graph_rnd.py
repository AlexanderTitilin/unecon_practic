from .geo_graph import GeoGraph, Node
from itertools import combinations_with_replacement
from numpy.random import random, binomial
from math import sqrt


class Grid:
    def __init__(self, l):
        self.__grid = [(x, y) for x in range(0, l)
                       for y in range(0, l)]
        self.l = l

    def __getitem__(self, key: (int, int)):
        i, j = key
        return self.__grid[self.l*i + j]

    def grid(self):
        return self.__grid


class GeoGraphRndModel:
    def __init__(self, l_step, n, l_size):
        self.n = n
        self.l_step = l_step
        self.l_size = l_size
        self.r = sqrt(2)*l_step
        self.grid = Grid(l_size**2)
        self.graph = GeoGraph()
        self.__gen_nodes()
        self.__update_nodes()

    def __gen_nodes(self):
        self.nodes = {}
        for (i, j) in self.grid.grid():
            self.__upd_omega(i, j)

    def __update_nodes(self):
        n_curr = self.n - self.l_size**2
        print(n_curr)
        N = self.n - self.l_size**2
        if N <= 0:
            return
        p = 1 / (self.l_size)
        if p >= 1:
            return
        for (i, j) in self.grid.grid():
            s = min(binomial(N, p), n_curr)
            n_curr -= s
            if n_curr <= 0:
                break
            for _ in range(s):
                self.__upd_omega(i, j)

    def __upd_omega(self, i, j):
        self.nodes[(i, j)] = Node(i+random(), j+random())
        for (k, m) in self.omega(i, j):
            if (k, m) in self.nodes.keys():
                if self.nodes[(i, j)].dist(self.nodes[(k, m)]) <= self.r:
                    self.graph.add_edge(
                        self.nodes[(i, j)], self.nodes[(k, m)])

    def omega(self, i, j):
        nxt = [(k, m) for k in range(-2, 3)
               for m in range(-2, 3) if 0 < abs(k) + abs(m) <= 3]
        nxt = [(k, m) for (k, m) in nxt if 0 <= i +
               k < self.l_step and 0 <= j+m < self.l_step]
        return [self.grid[i+k, j+m] for (k, m) in nxt]
