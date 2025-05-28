from .graph import Graph
from random import random
from .graph_visualisation import GraphPlotter
import matplotlib.pyplot as plt
from itertools import combinations
from numpy.random import choice


class BarabashiAlbertModel:
    def __init__(self, k_vertex, m):
        edges = combinations(range(1, k_vertex+1), 2)
        self.graph = Graph()
        self.graph.add_edges(edges)
        self.gp = GraphPlotter(self.graph)
        self.m = m

    def add_vertex(self, vertex):
        if vertex not in self.graph.verticies():
            total_deg = sum(self.graph.deg(v) for v in self.graph.verticies())
            p = [self.graph.deg(v) / total_deg for v in self.graph.verticies()]
            end = choice(list(self.graph.verticies()),
                         p=p, size=self.m, replace=False)
            for v1 in end:
                self.graph.add_edge(vertex, v1)

    def add_vertecies(self, verticies):
        for v in verticies:
            self.add_vertex(v)

    def add_nxt(self):
        self.add_vertex(self.graph.k_vertecies()+1)
        self.gp = GraphPlotter(self.graph)

    def visualise(self):
        gp = GraphPlotter(self.graph)
        gp.visualise()
