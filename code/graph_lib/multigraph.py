from .graph import Graph
from collections import Counter, defaultdict


class MultiGraph(Graph):
    def __init__(self):
        super().__init__()
        self._adjacency_list = defaultdict(Counter)

    def add_edge(self, a, b):
        self._adjacency_list[a][b] += 1
        self._adjacency_list[b][a] += 1
        self.add_vertex(a)
        self.add_vertex(b)

    def count_edges(self, v1, v2):
        return self._adjacency_list[v1][v2]
