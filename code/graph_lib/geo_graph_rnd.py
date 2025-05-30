from .geo_graph import GeoGraph, Node
from itertools import combinations_with_replacement
from numpy.random import random, binomial
from collections import defaultdict
from math import sqrt, ceil


class Grid:
    def __init__(self, l):
        self.grid = defaultdict(list)
        self.l = l
        self.gen_nodes(self.l)

    def gen_nodes(self, l):
        for i in range(l):
            for j in range(l):
                self.grid[i, j].append(Node(i+random(), j+random()))

    def omega(self, i, j):
        omega = []
        for k in range(-2, 3):
            for m in range(-2, 3):
                if 0 < abs(m) + abs(k) <= 3:
                    if 0 <= i + k < self.l and 0 <= j+m < self.l:
                        omega.extend(self.grid[i+k, j+m])
        return omega


class GeoGraphRndModel:
    def __init__(self, r, n):
        self.n = n
        self.r = r
        self.l_step = r/(sqrt(2))
        self.l_size = int(sqrt(n))
        self.grid = Grid(self.l_size)
        self.gen_graph()

    def gen_graph(self):
        self.graph = GeoGraph()
        for lst in self.grid.grid.values():
            self.graph.add_vertecies(lst)
        for i in range(self.l_size):
            for j in range(self.l_size):
                for n1 in self.grid.grid[i, j]:
                    omega = self.grid.omega(i, j)
                    for n2 in omega:
                        if n1.dist(n2) <= self.r and n2 != n1:
                            self.graph.add_edge(n1, n2)
        N = self.n - self.l_size**2
        p = (1/self.l_size)**2
        n_curr = self.n - self.l_size**2
        for i in range(self.l_size):
            for j in range(self.l_size):
                s = binomial(N, p)
                s = min(s, n_curr)
                for _ in range(s):
                    n = Node(i+random(), j+random())
                    for n2 in self.grid.grid[i, j]:
                        self.graph.add_edge(n, n2)
                    omega = self.grid.omega(i, j)
                    for n2 in omega:
                        if n.dist(n2) <= self.r:
                            self.graph.add_edge(n, n2)
                    self.grid.grid[i, j].append(n)
                    self.graph.add_vertex(n)
                n_curr -= s
                if n_curr <= 0:
                    break
