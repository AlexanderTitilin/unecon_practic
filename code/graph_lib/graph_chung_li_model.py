from .multigraph import MultiGraph
from itertools import combinations
from random import choice


class ChungLiModel:
    def __init__(self, d: [int]):
        self.d = d
        self.l_set = []
        for i, elem in enumerate(d, 1):
            for _ in range(elem):
                self.l_set.append(i)

        self.edges = []
        for _ in range(sum(d)//2):
            a = choice(self.l_set)
            self.l_set.remove(a)
            b = choice(self.l_set)
            self.l_set.remove(b)
            self.edges.append((a, b))
        self.graph = MultiGraph()
        self.graph.add_edges(self.edges)
