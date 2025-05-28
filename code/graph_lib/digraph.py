from .graph import Graph


class DiGraph(Graph):
    def __init__(self):
        super().__init__()

    def add_edge(self, a, b):
        self._adjacency_list[a].add(b)
        self.add_vertex(a)
        self.add_vertex(b)
