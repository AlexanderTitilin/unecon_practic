from .graph import Graph
from .graph_visualisation import GraphPlotter
from random import random
import matplotlib.pyplot as plt
from random import choices


class BolobasRiodanModel:
    def __init__(self, n):
        g = Graph()
        g.add_edge(1, 1)
        for v in range(2, n+1):
            p = [g.deg(vertex) / (2*n - 1) for vertex in g.verticies()]
            p.append(1 / (2*n - 1))
            g.add_vertex(v)
            end = choices(list(g.verticies()), weights=p, k=1)
            g.add_edge(v, end[0])
        self.graph = g
        self.gp = GraphPlotter(g)
