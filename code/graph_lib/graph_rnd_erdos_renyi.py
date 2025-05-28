from .graph import Graph
from math import log
from random import random
from .graph_visualisation import GraphPlotter
import matplotlib.pyplot as plt


class ErdosRenyiGraph():
    def __init__(self, n, p):
        self.graph: Graph = ErdosRenyiGraph.erdos_renyi_random_graph(n, p)
        self.visualation: GraphPlotter = GraphPlotter(self.graph)

    @staticmethod
    def complete_graph_edges(k):
        edges = []
        for a in range(1, k+1):
            for b in range(a+1, k+1):
                edges.append((a, b))
                edges.append((b, a))
        return edges

    @staticmethod
    def erdos_renyi_random_graph(n, p):
        edges = [e for e in ErdosRenyiGraph.complete_graph_edges(
            n) if random() < p]
        g = Graph()
        g.add_edges(edges)
        g.add_vertecies(range(1, n+1))
        return g

    @staticmethod
    def connection_test(n, c, m):
        p = c * log(n) / n
        k = 0
        for _ in range(m):
            g = ErdosRenyiGraph(n, p)
            if g.graph.is_connected():
                k += 1
        return k/m

    @staticmethod
    def visualise_connection_test(n):
        c_list = list(range(1, 20))
        c_list.remove(10)
        results = [ErdosRenyiGraph.connection_test(
            n, c/10, 400) for c in c_list]
        plt.plot(list(map(lambda x: x/10, c_list)), results)
        plt.scatter(list(map(lambda x: x/10, c_list)), results)
        plt.xlabel("c")
        plt.ylabel(r"p_{connected}")
        plt.show()


if __name__ == "__main__":
    ErdosRenyiGraph.visualise_connection_test(20)
