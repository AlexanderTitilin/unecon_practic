from .graph import Graph
from random import choice, random


class CopyModel():
    def __init__(self, alpha, d):
        self.d = d
        self.alpha = alpha
        self.graph = self.generate_complete_graph()
        self.start_verticies = list(range(1, d+1))
        self.i = 0
        self.nxt = d+2

    def generate_complete_graph(self):
        g = Graph()
        edges = [(i, j) for i in range(1, self.d+2)
                 for j in range(i+1, self.d+2)]
        g.add_edges(edges)
        return g

    def add_vertex(self):
        for _ in range(self.d):
            p = choice(self.start_verticies)
            if random() < self.alpha:
                self.graph.add_edge(p, self.nxt)
            else:
                self.graph.add_edge(list(self.graph.neib(p))[self.i], self.nxt)
            self.nxt += 1
            self.i =  (self.i + 1) % len(self.start_verticies)
