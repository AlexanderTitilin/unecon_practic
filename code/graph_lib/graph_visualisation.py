import matplotlib.pyplot as plt
from collections import namedtuple
from random import random
from .graph import Graph
from .geo_graph import GeoGraph
from .multigraph import MultiGraph
from math import cos, sin, pi
from functools import singledispatchmethod


class GraphPlotter:
    point = namedtuple("Point", ['x', 'y'])

    def __init__(self, g: Graph | GeoGraph | MultiGraph, orange_edges=[]):
        self.graph: Graph | GeoGraph | MultiGraph = g
        self.coords = {}
        self.gen_coords(g)
        self.orange_edges = orange_edges

    @singledispatchmethod
    def gen_coords(self, g):
        raise NotImplementedError()

    @gen_coords.register
    def __gen_coords(self, g: Graph | MultiGraph):
        for i, v in enumerate(g.verticies()):
            r = 2*i*pi / self.graph.k_vertecies()
            self.coords[v] = self.point(cos(r), sin(r))

    @gen_coords.register
    def __gen_coords(self, g: GeoGraph):
        for v in g.verticies():
            self.coords[v] = self.point(v.x, v.y)

    def visualise(self, orange=None):
        visited_centers = set()
        for v in self.graph.verticies():
            x, y = self.coords[v]
            color = "blue"
            if v in self.graph.neib(v):
                color = "red"
            if orange is not None and v == orange:
                color = "orange"
            plt.scatter(x, y, c=[color])
            for g in self.graph.neib(v):
                x2, y2 = self.coords[g]
                plt.plot([x, x2], [y, y2], color="blue")
                if type(self.graph) is MultiGraph:
                    c1, c2 = (x+x2) / 2, (y + y2) / 2
                    if v >= g:
                        plt.text(c1, c2, self.graph.count_edges(
                            v, g), va="top", fontsize=20)
                    visited_centers.add(c1)
                    visited_centers.add(c2)
            if type(self.graph) is not GeoGraph:
                plt.text(x, y, v, va='bottom', fontsize=14)
        plt.axis("off")

    def draw_on_ax(self, ax):
        for v in self.graph.verticies():
            x, y = self.coords[v]
            color = "red" if v in self.graph.neib(v) else "blue"
            if type(self.graph) is GeoGraph:
                ax.scatter(x, y, c=["blue"], s=100)
            else:
                ax.scatter(x, y, c=[color], s=10 if color == "blue" else 100)
            for g in self.graph.neib(v):
                x2, y2 = self.coords[g]
                ax.plot([x, x2], [y, y2],
                        color="orange" if (v, g) in self.orange_edges or (g, v) in self.orange_edges else "blue")
                if type(self.graph) is MultiGraph:
                    c1, c2 = (x+x2) / 2, (y + y2) / 2
                    if v >= g:
                        ax.text(c1, c2, self.graph.count_edges(
                            v, g), va="top", fontsize=20)
            if type(self.graph) is not GeoGraph:
                ax.text(x, y, v, va='bottom', fontsize=14)
        if type(self.graph) is GeoGraph:
            ax.grid(visible=True)
        else:
            ax.axis("off")
