from random import random, choice
from .graph import Graph
from .graph_visualisation import GraphPlotter
import matplotlib.pyplot as plt


class LCDModel:
    def __init__(self, n):
        k = 2*n
        nums = list(range(1, k+1))
        self.left = []
        self.right = []
        for _ in range(n):
            l = choice(nums)
            nums.remove(l)
            r = choice(nums)
            nums.remove(r)
            self.left.append(l)
            self.right.append(r)
        v = []
        curr = []
        nums = list(range(1, k+1))
        for i in nums:
            curr.append(i)
            if i in self.right:
                v.append(curr.copy())
                curr = []
        g = Graph()
        for i, lst in enumerate(v, 1):
            g.add_vertex(i)
            for j, v2 in enumerate(lst):
                if v2 in self.left:
                    r = self.right[j]
                    for k in range(len(v)):
                        if r in v[k]:
                            g.add_edge(i, k+1)
        self.graph = g
        self.gp = GraphPlotter(self.graph)

    def visualise(self):
        gp = GraphPlotter(self.graph)
        gp.visualise()


if __name__ == "__main__":
    m = LCDModel(20)
    m.visualise()
    plt.show()
